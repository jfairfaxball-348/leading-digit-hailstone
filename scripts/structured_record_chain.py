from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from scripts.structured_farey_extension import (
    LOWER_1,
    UPPER_1,
    PowerApproximation,
    next_valuation_after_rises,
    symbolic_cell_count_profile,
    terminal_representatives,
)
from scripts.structured_one_minimum_bound import (
    MINIMUM_ODD_STATE,
    first_impossible_rise_length,
    maximum_minimum_state,
)

OUTPUT = Path("data/structured_record_chain.json")
PREEXISTING_EXCLUSION = 64_497_106
LN2_TERMS = 60
LN3_TERMS = 80

EXPECTED_UPPER_Q = [
    64_497_107,
    118_212_940,
    171_928_773,
    397_573_379,
    6_586_818_670,
    72_057_431_991,
    137_528_045_312,
    890_638_885_193,
]


def log_bounds_ratio(
    numerator: int, denominator: int = 1, terms: int = 32
) -> tuple[Fraction, Fraction]:
    """Exact rational enclosure for log(numerator / denominator).

    For x>1 and z=(x-1)/(x+1),

      log(x) = 2 * sum_{k>=0} z^(2k+1)/(2k+1).

    All terms are positive, and after N terms the tail is at most

      2*z^(2N+1) / ((2N+1)*(1-z^2)).

    Hence this routine uses only exact rational arithmetic.
    """
    if numerator <= denominator or denominator <= 0:
        raise ValueError("require numerator > denominator > 0")

    z = Fraction(numerator - denominator, numerator + denominator)
    z2 = z * z
    power = z
    partial = Fraction(0)

    for k in range(terms):
        partial += power / (2 * k + 1)
        power *= z2

    lower = 2 * partial
    upper = lower + 2 * power / ((2 * terms + 1) * (1 - z2))
    return lower, upper


LN2_LOWER, LN2_UPPER = log_bounds_ratio(2, 1, LN2_TERMS)
LN3_LOWER, LN3_UPPER = log_bounds_ratio(3, 1, LN3_TERMS)
ALPHA_LOWER = LN3_LOWER / LN2_UPPER
ALPHA_UPPER = LN3_UPPER / LN2_LOWER


def farey_determinant(
    upper: PowerApproximation, lower: PowerApproximation
) -> int:
    return upper.r * lower.q - lower.r * upper.q


def mediant(
    a: PowerApproximation, b: PowerApproximation
) -> PowerApproximation:
    return PowerApproximation(q=a.q + b.q, r=a.r + b.r)


def alpha_side(pair: PowerApproximation) -> int:
    """Return +1 above log_2(3), -1 below, using exact rational bounds."""
    slope = Fraction(pair.r, pair.q)
    if slope > ALPHA_UPPER:
        return 1
    if slope < ALPHA_LOWER:
        return -1
    raise AssertionError("log enclosure too coarse to decide side")


def is_exact_ceiling(pair: PowerApproximation) -> bool:
    """Certify R=ceil(q log_2 3) from the exact alpha enclosure."""
    return (
        Fraction(pair.r - 1, pair.q) < ALPHA_LOWER
        and Fraction(pair.r, pair.q) > ALPHA_UPPER
    )


def product_log_gap_bounds(
    pair: PowerApproximation,
) -> tuple[Fraction, Fraction]:
    """Bounds for R log 2 - q log 3."""
    lower = pair.r * LN2_LOWER - pair.q * LN3_UPPER
    upper = pair.r * LN2_UPPER - pair.q * LN3_LOWER
    return lower, upper


def product_window_allows_via_logs(
    pair: PowerApproximation, minimum: int
) -> bool:
    """Exact decision of 2^R/3^q <= B(M) by rational log enclosures."""
    gap_lower, gap_upper = product_log_gap_bounds(pair)
    if gap_lower <= 0:
        raise AssertionError("expected an exact upper approximation")

    numerator = minimum * (minimum - 19)
    denominator = minimum * minimum - 57 * minimum + 361

    for terms in (2, 4, 8, 16):
        bound_lower, bound_upper = log_bounds_ratio(
            numerator, denominator, terms
        )
        if gap_upper <= bound_lower:
            return True
        if gap_lower > bound_upper:
            return False

    raise AssertionError("log enclosure too coarse for product-window decision")


def maximum_minimum_state_via_logs(
    pair: PowerApproximation, minimum: int = MINIMUM_ODD_STATE
) -> int:
    """Exact M_max using only rational logarithmic enclosures."""
    if not product_window_allows_via_logs(pair, minimum):
        raise ValueError("record already excluded at the minimum premise")

    lo = minimum
    hi = 2 * minimum
    while product_window_allows_via_logs(pair, hi):
        lo = hi
        hi *= 2

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if product_window_allows_via_logs(pair, mid):
            lo = mid
        else:
            hi = mid

    return lo


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def ceil_log10_ratio(numerator: int, denominator: int) -> int:
    """Smallest h>=0 with numerator <= denominator*10^h."""
    if numerator <= denominator:
        return 0
    h = 0
    scaled = denominator
    while scaled < numerator:
        scaled *= 10
        h += 1
    return h


def symbolic_complexity_bound(
    lo: int, hi: int, rises: int
) -> dict[str, int]:
    """Explicit bound from the normalized weak-run strip theorem."""
    h = ceil_log10_ratio(hi + 19, lo)
    decimal_boundary_cap = 9 * (h + 2)
    return {
        "ceil_log10_range_ratio": h,
        "decimal_boundary_cap_per_depth": decimal_boundary_cap,
        "cell_count_upper_bound": 17 * rises * decimal_boundary_cap + 1,
    }


@dataclass(frozen=True)
class RecordBlock:
    upper: PowerApproximation
    next_upper: PowerApproximation
    intervening_lower_mediants: int


def record_blocks() -> list[RecordBlock]:
    """Follow the exact Stern-Brocot bracket until the eighth new upper."""
    upper = UPPER_1
    lower = LOWER_1
    lower_updates = 0
    blocks: list[RecordBlock] = []

    assert farey_determinant(upper, lower) == 1
    assert alpha_side(upper) == 1
    assert alpha_side(lower) == -1

    while len(blocks) < 7:
        candidate = mediant(upper, lower)
        candidate_side = alpha_side(candidate)

        if candidate_side == 1:
            if upper.q > PREEXISTING_EXCLUSION:
                blocks.append(
                    RecordBlock(
                        upper=upper,
                        next_upper=candidate,
                        intervening_lower_mediants=lower_updates,
                    )
                )
            upper = candidate
            lower_updates = 0
        else:
            lower = candidate
            lower_updates += 1

        assert farey_determinant(upper, lower) == 1

    observed_upper_q = [block.upper.q for block in blocks]
    observed_upper_q.append(blocks[-1].next_upper.q)
    assert observed_upper_q == EXPECTED_UPPER_Q
    return blocks


def direct_first_record_integer_check(
    pair: PowerApproximation, expected_m_max: int
) -> None:
    """Independent exact-integer regression for q=64,497,107."""
    assert pair.q == 64_497_107
    assert pair.r == 102_225_496

    three_to_q = 3**pair.q
    # bit_length(3^q)=R is exactly 2^(R-1) <= 3^q < 2^R.
    assert three_to_q.bit_length() == pair.r
    assert (
        maximum_minimum_state(pair.r, three_to_q, MINIMUM_ODD_STATE)
        == expected_m_max
    )


def run() -> dict:
    blocks = record_blocks()
    rows: list[dict] = []

    for index, block in enumerate(blocks):
        pair = block.upper
        next_upper = block.next_upper

        assert alpha_side(pair) == 1
        assert is_exact_ceiling(pair)

        m_max = maximum_minimum_state_via_logs(pair)
        impossible = first_impossible_rise_length(
            MINIMUM_ODD_STATE, m_max
        )
        if impossible is None:
            raise AssertionError("symbolic rise cap did not close the record")

        required_rise = 2 * pair.q - pair.r
        assert required_rise > impossible

        profile = symbolic_cell_count_profile(
            MINIMUM_ODD_STATE, m_max, impossible
        )
        assert profile[-1] == 0

        terminal_depth = impossible - 1
        representatives = terminal_representatives(
            MINIMUM_ODD_STATE, m_max, terminal_depth
        )
        next_valuations = [
            next_valuation_after_rises(seed, terminal_depth)
            for seed in representatives
        ]
        assert all(valuation != 1 for valuation in next_valuations)

        # If U is the current upper neighbour and U' is the next upper
        # Stern-Brocot record, the final lower neighbour L before U' obeys
        # delta(U) > eta(L).  Together with determinant 1 this gives
        # delta(U) > 1/q(U').  Verify that exact lower bound here.
        delta_lower = Fraction(pair.r, 1) - pair.q * ALPHA_UPPER
        assert delta_lower > Fraction(1, next_upper.q)

        # From B(M)-1 < 38/(M-57) and 2^delta-1 > delta*ln(2):
        # M < 57 + 38*q_next/ln(2).  Replacing ln(2) by its exact lower
        # bound gives a conservative integer cap.
        record_linear_bound = ceil_fraction(
            Fraction(57, 1)
            + Fraction(38 * next_upper.q, 1) / LN2_LOWER
        ) - 1
        assert m_max <= record_linear_bound

        complexity = symbolic_complexity_bound(
            MINIMUM_ODD_STATE, m_max, terminal_depth
        )
        assert max(profile) <= complexity["cell_count_upper_bound"]

        rows.append(
            {
                "upper": {
                    "q": pair.q,
                    "R": pair.r,
                    "power_relation": "2^R > 3^q",
                },
                "covered_q_start": pair.q,
                "covered_q_end": next_upper.q - 1,
                "next_upper_denominator": next_upper.q,
                "intervening_lower_mediants": (
                    block.intervening_lower_mediants
                ),
                "required_minimum_rise_at_block_start": required_rise,
                "maximum_minimum_state": m_max,
                "record_to_record_linear_M_cap": record_linear_bound,
                "first_impossible_rise_length": impossible,
                "peak_symbolic_cell_count": max(profile),
                "cell_counts_by_rise_depth": profile,
                "terminal_depth": terminal_depth,
                "terminal_representatives": representatives,
                "next_valuations": next_valuations,
                "symbolic_complexity_bound_at_terminal_depth": complexity,
            }
        )

        if index == 0:
            direct_first_record_integer_check(pair, m_max)

    first_uncovered = blocks[-1].next_upper
    remaining_rise = 2 * first_uncovered.q - first_uncovered.r

    return {
        "schema_version": 1,
        "claim_type": (
            "THEOREM_PLUS_FINITE_EXACT_RATIONAL_ARITHMETIC_"
            "AND_SYMBOLIC_CERTIFICATE"
        ),
        "premise": (
            "one-rise/one-fall accelerated cycle entirely above 19 with "
            "minimum odd state >= 5000001"
        ),
        "preexisting_structured_q_excluded_through": PREEXISTING_EXCLUSION,
        "exact_log_method": {
            "identity": (
                "log(x)=2*sum_{k>=0} z^(2k+1)/(2k+1), "
                "z=(x-1)/(x+1)"
            ),
            "tail_bound": (
                "tail after N terms <= "
                "2*z^(2N+1)/((2N+1)*(1-z^2))"
            ),
            "ln2_terms": LN2_TERMS,
            "ln3_terms": LN3_TERMS,
            "role": (
                "exact rational enclosures certify the side of log_2(3) "
                "and exact product-window comparisons without materializing "
                "giant powers"
            ),
        },
        "theorem_level_scaling": {
            "weak_run_normalized_strip": (
                "For an exact r=1 run from M, beta_i=(2/3)^i*x_i-M lies "
                "between 3*(1-(2/3)^i) and 19*(1-(2/3)^i), so the "
                "uncertainty width is <16."
            ),
            "symbolic_cell_bound": (
                "For M in [L,U], let "
                "D=9*(ceil(log10((U+19)/L))+2). After s exact r=1 rises, "
                "the number of decimal-sector/binary-lift cells is at most "
                "17*s*D+1."
            ),
            "residue_sparsification": (
                "If 2^(s+1)>U-L, each surviving cell contains at most one "
                "seed, so the surviving seed count is at most 17*s*D+1."
            ),
            "record_growth_bound": (
                "For consecutive upper Farey records with denominators q "
                "and q_next, delta=R-q*log_2(3)>1/q_next. Hence any "
                "structured-cycle minimum satisfies "
                "M < 57 + 38*q_next/ln(2)."
            ),
        },
        "record_blocks": rows,
        "structured_q_excluded_through": first_uncovered.q - 1,
        "first_q_not_covered_by_current_certificate": first_uncovered.q,
        "first_uncovered_upper_record": {
            "q": first_uncovered.q,
            "R": first_uncovered.r,
            "power_relation": "2^R > 3^q",
        },
        "certified_minimum_rise_length_for_any_remaining_structured_cycle": (
            remaining_rise
        ),
        "interpretation": (
            "The Farey mechanism now iterates record-to-record across "
            "several continued-fraction blocks, while a theorem bounds "
            "symbolic cell growth linearly in rise depth for each fixed "
            "finite minimum range. Exact symbolic extinction still occurs "
            "after at most 49 rises on every certified record range here. "
            "This is a finite structured-class exclusion, not a global "
            "exclusion; the unresolved asymptotic obstruction is to control "
            "the positions of the final residue representatives uniformly "
            "as the record ranges grow."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
