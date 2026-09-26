from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step
from scripts.structured_farey_extension import (
    LOWER_1,
    UPPER_1,
    PowerApproximation,
    farey_determinant,
)
from scripts.structured_one_minimum_bound import (
    MINIMUM_ODD_STATE,
    _ceil_div,
    _digit_sector_intersections,
    _first_congruent,
)

OUTPUT = Path("data/structured_record_chain.json")
LOG_TERMS = 90
PRODUCT_LOG_TERMS = 4
NEW_RECORDS_TO_CERTIFY = 7


@dataclass(frozen=True)
class TrackedRiseCell:
    """A symbolic rise cell with its exact leading-digit word attached."""

    lo: int
    hi: int
    additive: int
    residue: int
    digits: tuple[int, ...]


def log_bounds_fraction(
    numerator: int,
    denominator: int = 1,
    terms: int = LOG_TERMS,
) -> tuple[Fraction, Fraction]:
    """Rigorous rational bounds for log(numerator/denominator), ratio > 1.

    With z=(x-1)/(x+1),

      log x = 2 * sum_{k>=0} z^(2k+1)/(2k+1).

    The omitted positive tail after N summands is at most

      2 z^(2N+1) / ((2N+1)(1-z^2)).

    Everything here is exact rational arithmetic.
    """
    if numerator <= denominator or denominator <= 0:
        raise ValueError("log_bounds_fraction requires numerator/denominator > 1")

    z = Fraction(numerator - denominator, numerator + denominator)
    z_squared = z * z
    term = z
    partial = Fraction(0)

    for k in range(terms):
        partial += term / (2 * k + 1)
        term *= z_squared

    lower = 2 * partial
    remainder = 2 * term / ((2 * terms + 1) * (1 - z_squared))
    return lower, lower + remainder


LOG_TWO_BOUNDS = log_bounds_fraction(2)
LOG_THREE_BOUNDS = log_bounds_fraction(3)


def power_log_bounds(pair: PowerApproximation) -> tuple[Fraction, Fraction]:
    """Bounds for log(2^R/3^q)=R log 2-q log 3."""
    lower = pair.r * LOG_TWO_BOUNDS[0] - pair.q * LOG_THREE_BOUNDS[1]
    upper = pair.r * LOG_TWO_BOUNDS[1] - pair.q * LOG_THREE_BOUNDS[0]
    return lower, upper


def certified_power_side(pair: PowerApproximation) -> int:
    """Return +1 for 2^R>3^q, -1 for 2^R<3^q, using exact bounds."""
    lower, upper = power_log_bounds(pair)
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise AssertionError("rational logarithm bounds do not certify the power side")


def structured_bound_fraction(minimum: int) -> tuple[int, int]:
    numerator = minimum * (minimum - 19)
    denominator = minimum * minimum - 57 * minimum + 361
    if denominator <= 0:
        raise ValueError("minimum is too small for the structured product bound")
    return numerator, denominator


def structured_log_bounds(minimum: int) -> tuple[Fraction, Fraction]:
    numerator, denominator = structured_bound_fraction(minimum)
    return log_bounds_fraction(
        numerator,
        denominator,
        PRODUCT_LOG_TERMS,
    )


def product_window_allows(pair: PowerApproximation, minimum: int) -> bool:
    """Decide 2^R/3^q <= B(minimum) by rigorous rational log bounds."""
    product_lower, product_upper = power_log_bounds(pair)
    bound_lower, bound_upper = structured_log_bounds(minimum)

    if product_upper <= bound_lower:
        return True
    if product_lower > bound_upper:
        return False

    bound_lower, bound_upper = log_bounds_fraction(
        *structured_bound_fraction(minimum),
        terms=8,
    )
    if product_upper <= bound_lower:
        return True
    if product_lower > bound_upper:
        return False

    raise AssertionError("exact log intervals overlap at product-window decision")


def maximum_minimum_state_log(
    pair: PowerApproximation,
    minimum: int = MINIMUM_ODD_STATE,
) -> int:
    """Largest integer M allowed by the structured window, exactly certified."""
    if not product_window_allows(pair, minimum):
        raise ValueError("record is excluded already at the minimum premise")

    lo = minimum
    hi = 2 * minimum

    while product_window_allows(pair, hi):
        lo = hi
        hi *= 2

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if product_window_allows(pair, mid):
            lo = mid
        else:
            hi = mid

    assert product_window_allows(pair, lo)
    assert not product_window_allows(pair, lo + 1)
    return lo


def _advance_tracked_cells(
    cells: list[TrackedRiseCell],
    step: int,
) -> tuple[list[TrackedRiseCell], dict[str, int]]:
    """Impose one exact r=1 rise and record exact branching diagnostics."""
    three_to_i = 3**step
    two_to_i = 1 << step
    modulus = 1 << (step + 1)
    next_modulus = modulus << 1
    out: list[TrackedRiseCell] = []

    decimal_fragments = 0
    lift_attempts = 0
    range_compatible_lifts = 0

    for cell in cells:
        xlo = (three_to_i * cell.lo + cell.additive) // two_to_i
        xhi = (three_to_i * cell.hi + cell.additive) // two_to_i

        for digit, sector_lo, sector_hi in _digit_sector_intersections(xlo, xhi):
            lo = max(
                cell.lo,
                _ceil_div(
                    sector_lo * two_to_i - cell.additive,
                    three_to_i,
                ),
            )
            hi = min(
                cell.hi,
                (sector_hi * two_to_i - cell.additive) // three_to_i,
            )
            if lo > hi:
                continue

            decimal_fragments += 1
            correction = 2 * digit + 1
            next_additive = 3 * cell.additive + correction * two_to_i

            for residue in (cell.residue, cell.residue + modulus):
                lift_attempts += 1
                representative = _first_congruent(
                    lo,
                    residue,
                    next_modulus,
                )
                if representative > hi:
                    continue

                range_compatible_lifts += 1
                numerator = three_to_i * representative + cell.additive
                assert numerator % two_to_i == 0
                x = numerator // two_to_i
                odd_numerator = 3 * x + correction

                if odd_numerator % 4 == 2:
                    out.append(
                        TrackedRiseCell(
                            lo=lo,
                            hi=hi,
                            additive=next_additive,
                            residue=residue % next_modulus,
                            digits=cell.digits + (digit,),
                        )
                    )

    return out, {
        "source_cells": len(cells),
        "decimal_fragments": decimal_fragments,
        "lift_attempts": lift_attempts,
        "range_compatible_lifts": range_compatible_lifts,
        "binary_range_misses": lift_attempts - range_compatible_lifts,
        "valuation_misses": range_compatible_lifts - len(out),
    }


def symbolic_profile(
    lo: int,
    hi: int,
    cap: int = 128,
) -> tuple[int, list[dict[str, int]], list[TrackedRiseCell]]:
    """Exact symbolic profile until the first impossible rise length."""
    cells = [TrackedRiseCell(lo=lo, hi=hi, additive=0, residue=1, digits=())]
    profile: list[dict[str, int]] = []

    for step in range(cap):
        cells, diagnostics = _advance_tracked_cells(cells, step)
        modulus = 1 << (step + 2)
        cells = [
            cell
            for cell in cells
            if _first_congruent(cell.lo, cell.residue, modulus) <= cell.hi
        ]

        widths = [cell.hi - cell.lo + 1 for cell in cells]
        profile.append(
            {
                "rise_depth": step + 1,
                "cells": len(cells),
                "total_cell_width": sum(widths),
                "minimum_cell_width": min(widths) if widths else 0,
                "maximum_cell_width": max(widths) if widths else 0,
                "distinct_digit_words": len({cell.digits for cell in cells}),
                "distinct_residues": len({cell.residue for cell in cells}),
                "residue_modulus": modulus,
                **diagnostics,
            }
        )

        if not cells:
            return step + 1, profile, cells

    raise AssertionError("symbolic rise cap is too small")


def cells_after_rises(
    lo: int,
    hi: int,
    rises: int,
) -> list[TrackedRiseCell]:
    cells = [TrackedRiseCell(lo=lo, hi=hi, additive=0, residue=1, digits=())]

    for step in range(rises):
        cells, _ = _advance_tracked_cells(cells, step)
        modulus = 1 << (step + 2)
        cells = [
            cell
            for cell in cells
            if _first_congruent(cell.lo, cell.residue, modulus) <= cell.hi
        ]
        if not cells:
            break

    return cells


def terminal_representatives(
    lo: int,
    hi: int,
    rises: int,
) -> list[dict[str, int | str]]:
    """Extract exact representatives once each surviving cell is sub-modulus."""
    cells = cells_after_rises(lo, hi, rises)
    modulus = 1 << (rises + 1)
    rows: list[dict[str, int | str]] = []

    for cell in cells:
        width = cell.hi - cell.lo + 1
        if width >= modulus:
            raise AssertionError("terminal cell is not narrower than its modulus")

        representative = _first_congruent(cell.lo, cell.residue, modulus)
        if representative > cell.hi:
            raise AssertionError("surviving terminal cell has no representative")

        x = representative
        for _ in range(rises):
            x, valuation = accelerated_odd_step(x)
            if valuation != 1:
                raise AssertionError("terminal representative fails its rise word")

        _, next_valuation = accelerated_odd_step(x)
        rows.append(
            {
                "cell_lo": cell.lo,
                "cell_hi": cell.hi,
                "cell_width": width,
                "representative": representative,
                "digit_word": "".join(str(digit) for digit in cell.digits),
                "state_after_rises": x,
                "next_valuation": next_valuation,
            }
        )

    return rows


def decimal_boundary_count(lo: int, hi: int, rises: int) -> int:
    """Count scaled decimal-sector boundaries relevant to localization."""
    total = 0

    for i in range(rises):
        three_to_i = 3**i
        two_to_i = 1 << i
        lower_scaled = lo * three_to_i
        upper_scaled = (hi + 19) * three_to_i
        maximum_boundary = upper_scaled // two_to_i
        largest_decade = len(str(maximum_boundary)) - 1

        for k in range(largest_decade + 1):
            scale = 10**k
            for digit in range(1, 10):
                boundary = digit * scale
                scaled = boundary * two_to_i
                if lower_scaled <= scaled <= upper_scaled:
                    total += 1

    return total


def _mediant(
    upper: PowerApproximation,
    lower: PowerApproximation,
) -> PowerApproximation:
    return PowerApproximation(
        q=upper.q + lower.q,
        r=upper.r + lower.r,
    )


def next_upper_records(
    start_upper: PowerApproximation,
    start_lower: PowerApproximation,
    count: int,
) -> list[dict[str, object]]:
    """Generate upper records by exact Farey/Stern-Brocot mediant steps."""
    if certified_power_side(start_upper) != 1:
        raise AssertionError("starting upper is not above log_2(3)")
    if certified_power_side(start_lower) != -1:
        raise AssertionError("starting lower is not below log_2(3)")
    if farey_determinant(start_upper, start_lower) != 1:
        raise AssertionError("starting fractions are not Farey neighbours")

    upper = start_upper
    lower = start_lower
    events: list[dict[str, object]] = []
    lower_updates = 0

    while len(events) < count + 1:
        candidate = _mediant(upper, lower)
        candidate_side = certified_power_side(candidate)

        if candidate_side == 1:
            upper = candidate
            events.append(
                {
                    "upper": upper,
                    "lower_at_record": lower,
                    "lower_updates_before_record": lower_updates,
                }
            )
            lower_updates = 0
        else:
            if candidate_side != -1:
                raise AssertionError("unexpected uncertified mediant")
            lower = candidate
            lower_updates += 1

        if farey_determinant(upper, lower) != 1:
            raise AssertionError("Farey determinant changed")

    return events


def run() -> dict:
    assert maximum_minimum_state_log(UPPER_1) == 3_112_972_388

    events = next_upper_records(
        UPPER_1,
        LOWER_1,
        NEW_RECORDS_TO_CERTIFY,
    )

    records: list[dict[str, object]] = []

    for index in range(NEW_RECORDS_TO_CERTIFY):
        event = events[index]
        next_event = events[index + 1]
        upper = event["upper"]
        lower_at_record = event["lower_at_record"]
        next_upper = next_event["upper"]
        final_lower = next_event["lower_at_record"]

        assert isinstance(upper, PowerApproximation)
        assert isinstance(lower_at_record, PowerApproximation)
        assert isinstance(next_upper, PowerApproximation)
        assert isinstance(final_lower, PowerApproximation)

        maximum_minimum = maximum_minimum_state_log(upper)
        required_rise = 2 * upper.q - upper.r
        impossible, profile, _ = symbolic_profile(
            MINIMUM_ODD_STATE,
            maximum_minimum,
        )
        if impossible > required_rise:
            raise AssertionError("symbolic extinction is too late to exclude the record")

        records.append(
            {
                "q": upper.q,
                "R": upper.r,
                "power_relation": "2^R > 3^q",
                "lower_neighbor_at_record": {
                    "q": lower_at_record.q,
                    "R": lower_at_record.r,
                },
                "final_lower_neighbor_before_next_upper": {
                    "q": final_lower.q,
                    "R": final_lower.r,
                },
                "lower_updates_before_next_upper": next_event[
                    "lower_updates_before_record"
                ],
                "farey_determinant": farey_determinant(upper, final_lower),
                "next_upper_record": {
                    "q": next_upper.q,
                    "R": next_upper.r,
                },
                "covered_q_start": upper.q,
                "covered_q_end": next_upper.q - 1,
                "maximum_minimum_state": maximum_minimum,
                "required_minimum_rise": required_rise,
                "first_impossible_rise_length": impossible,
                "peak_symbolic_cells": max(row["cells"] for row in profile),
            }
        )

    assert [
        (record["q"], record["R"])
        for record in records
    ] == [
        (64_497_107, 102_225_496),
        (118_212_940, 187_363_077),
        (171_928_773, 272_500_658),
        (397_573_379, 630_138_897),
        (6_586_818_670, 10_439_860_591),
        (72_057_431_991, 114_208_327_604),
        (137_528_045_312, 217_976_794_617),
    ]

    assert [record["maximum_minimum_state"] for record in records] == [
        4_350_616_725,
        7_221_856_344,
        21_238_350_355,
        359_020_668_782,
        3_753_781_445_604,
        6_895_437_822_163,
        42_285_421_502_900,
    ]
    assert [record["first_impossible_rise_length"] for record in records] == [
        31,
        31,
        35,
        38,
        41,
        41,
        49,
    ]
    assert [record["peak_symbolic_cells"] for record in records] == [
        276,
        301,
        350,
        485,
        603,
        636,
        727,
    ]

    lookahead = events[-1]["upper"]
    lookahead_lower = events[-1]["lower_at_record"]
    assert isinstance(lookahead, PowerApproximation)
    assert isinstance(lookahead_lower, PowerApproximation)
    assert (lookahead.q, lookahead.r) == (
        890_638_885_193,
        1_411_629_234_715,
    )
    assert (lookahead_lower.q, lookahead_lower.r) == (
        753_110_839_881,
        1_193_652_440_098,
    )
    assert certified_power_side(lookahead) == 1
    assert farey_determinant(lookahead, lookahead_lower) == 1

    structured_q_excluded_through = lookahead.q - 1
    remaining_minimum_rise = 2 * lookahead.q - lookahead.r
    assert remaining_minimum_rise == 369_648_535_671

    largest = records[-1]
    largest_hi = int(largest["maximum_minimum_state"])
    largest_impossible = int(largest["first_impossible_rise_length"])
    _, largest_profile, _ = symbolic_profile(
        MINIMUM_ODD_STATE,
        largest_hi,
        largest_impossible,
    )
    terminal = terminal_representatives(
        MINIMUM_ODD_STATE,
        largest_hi,
        largest_impossible - 1,
    )
    assert terminal == [
        {
            "cell_lo": 26_465_544_205_035,
            "cell_hi": 26_666_666_666_617,
            "cell_width": 201_122_461_583,
            "representative": 26_501_219_601_103,
            "digit_word": (
                "235812346112357112358112461123571123581124691235"
            ),
            "state_after_rises": 7_510_109_955_360_948_316_615,
            "next_valuation": 2,
        }
    ]

    boundary_count = decimal_boundary_count(
        MINIMUM_ODD_STATE,
        largest_hi,
        largest_impossible - 1,
    )
    word_bound = 1 + 20 * boundary_count
    residue_capacity_per_word = (
        (largest_hi - MINIMUM_ODD_STATE)
        // (1 << largest_impossible)
        + 1
    )
    assert boundary_count == 2_997
    assert word_bound == 59_941
    assert residue_capacity_per_word == 1

    return {
        "schema_version": 1,
        "claim_type": (
            "THEOREM_PLUS_FINITE_EXACT_RATIONAL_ARITHMETIC_AND_SYMBOLIC_CERTIFICATE"
        ),
        "premise": (
            "one-rise/one-fall accelerated cycle entirely above 19 with "
            "minimum odd state >= 5000001"
        ),
        "exact_log_certificate": {
            "identity": (
                "log(x)=2*sum_{k>=0} z^(2k+1)/(2k+1), "
                "z=(x-1)/(x+1)"
            ),
            "tail_bound": (
                "tail_N <= 2*z^(2N+1)/((2N+1)*(1-z^2))"
            ),
            "log_2_and_log_3_terms": LOG_TERMS,
            "structured_bound_log_terms": PRODUCT_LOG_TERMS,
            "arithmetic": "fractions.Fraction exact rational arithmetic",
        },
        "starting_upper": {"q": UPPER_1.q, "R": UPPER_1.r},
        "starting_lower": {"q": LOWER_1.q, "R": LOWER_1.r},
        "new_upper_records": records,
        "structured_q_excluded_through": structured_q_excluded_through,
        "first_q_not_covered_by_this_certificate": lookahead.q,
        "next_unprocessed_upper_record": {
            "q": lookahead.q,
            "R": lookahead.r,
            "lower_neighbor": {
                "q": lookahead_lower.q,
                "R": lookahead_lower.r,
            },
            "power_relation": "2^R > 3^q",
            "farey_determinant": 1,
        },
        "certified_minimum_rise_length_for_any_remaining_structured_cycle": (
            remaining_minimum_rise
        ),
        "largest_processed_symbolic_range": {
            "minimum": MINIMUM_ODD_STATE,
            "maximum": largest_hi,
            "first_impossible_rise_length": largest_impossible,
            "cell_counts_by_rise_depth": [
                row["cells"] for row in largest_profile
            ],
            "profile_tail_from_depth_32": [
                {
                    key: row[key]
                    for key in (
                        "rise_depth",
                        "cells",
                        "total_cell_width",
                        "minimum_cell_width",
                        "maximum_cell_width",
                        "distinct_digit_words",
                        "distinct_residues",
                        "binary_range_misses",
                        "valuation_misses",
                    )
                }
                for row in largest_profile
                if row["rise_depth"] >= 32
            ],
            "terminal_depth": largest_impossible - 1,
            "terminal_representatives": terminal,
        },
        "finite_range_symbolic_complexity_diagnostic": {
            "rise_depth": largest_impossible - 1,
            "scaled_decimal_boundary_count_J": boundary_count,
            "proved_decimal_sector_word_bound_1_plus_20J": word_bound,
            "residue_capacity_per_fixed_word": residue_capacity_per_word,
            "interpretation": (
                "The boundary-window lemma gives polynomial/linear finite-range "
                "word complexity, but at sub-modulus scale it only bounds each "
                "word to at most one residue representative. It does not force "
                "that representative to miss its decimal cell."
            ),
        },
        "interpretation": (
            "Seven further exact upper Farey records are eliminated by their "
            "theorem-derived product windows and complete decimal-sector/2-adic "
            "symbolic rise coverage. Any different positive one-rise/one-fall "
            "accelerated cycle consistent with the 5M minimum-element exclusion "
            "must have q >= 890638885193 and at least 369648535671 consecutive "
            "r=1 rise steps. This remains a finite structured-class result, not "
            "a global cycle exclusion and not a result for arbitrary cycles."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
