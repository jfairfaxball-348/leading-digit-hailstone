from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

MINIMUM_ODD_STATE = 5_000_001
PERIOD_SCAN_LIMIT = 400_000
RISING_CHECK_CAP = 128
OUTPUT = Path("data/structured_one_minimum_bound.json")


def uniform_bound_fraction(minimum: int = MINIMUM_ODD_STATE) -> tuple[int, int]:
    """Return numerator/denominator of the one-rise/one-fall product bound."""
    numerator = minimum * (minimum - 19)
    denominator = minimum * minimum - 57 * minimum + 361
    if denominator <= 0:
        raise ValueError("minimum is too small for the recorded rational bound")
    return numerator, denominator


def structured_window_allows(
    q: int, minimum: int = MINIMUM_ODD_STATE
) -> bool:
    """Exact necessary product-window test for a structured period q."""
    three_to_q = 3**q
    r = three_to_q.bit_length()
    numerator, denominator = uniform_bound_fraction(minimum)
    return (1 << r) * denominator <= three_to_q * numerator


def product_candidate_periods_through(
    limit: int = PERIOD_SCAN_LIMIT, minimum: int = MINIMUM_ODD_STATE
) -> list[tuple[int, int, int]]:
    """Enumerate every q<=limit surviving the uniform product window exactly.

    Returns (q, R, 3^q).  The 17-bit prefilter is only a safe rejection
    shortcut: the final decision is always the exact integer inequality.
    """
    numerator, denominator = uniform_bound_fraction(minimum)

    # The structured upper bound is <2, so at most one R can work.
    assert numerator < 2 * denominator

    # If the exact window works, D/2^R < 2^-17 for
    # D=2^R-3^q.  This gives a safe exact prefilter.
    assert (numerator - denominator) * (1 << 17) < numerator

    three_to_q = 1
    survivors: list[tuple[int, int, int]] = []

    for q in range(1, limit + 1):
        three_to_q *= 3
        r = three_to_q.bit_length()
        two_to_r = 1 << r

        if r > 17 and two_to_r - three_to_q >= (1 << (r - 17)):
            continue

        if two_to_r * denominator <= three_to_q * numerator:
            survivors.append((q, r, three_to_q))

    return survivors


def product_window_allows_at_state(
    r: int, three_to_q: int, minimum: int
) -> bool:
    numerator, denominator = uniform_bound_fraction(minimum)
    return (1 << r) * denominator <= three_to_q * numerator


def maximum_minimum_state(
    r: int, three_to_q: int, minimum: int = MINIMUM_ODD_STATE
) -> int:
    """Largest integer M>=minimum allowed by the structured product window.

    The rational bound B(M)=M(M-19)/(M^2-57M+361) is strictly decreasing
    on the relevant range.  Discretely,

      N(M+1)D(M)-N(M)D(M+1)
        = -38(M^2-18M+171) < 0,

    so binary search has exact coverage.
    """
    if not product_window_allows_at_state(r, three_to_q, minimum):
        raise ValueError("period is already excluded at the minimum premise")

    lo = minimum
    hi = 2 * minimum

    while product_window_allows_at_state(r, three_to_q, hi):
        lo = hi
        hi *= 2

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if product_window_allows_at_state(r, three_to_q, mid):
            lo = mid
        else:
            hi = mid

    return lo


@dataclass(frozen=True)
class RiseCell:
    """Initial-M cell for a fixed rise digit word and exact binary lift."""

    lo: int
    hi: int
    additive: int
    residue: int


def _ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def _first_congruent(lo: int, residue: int, modulus: int) -> int:
    return lo + ((residue - lo) % modulus)


def _digit_sector_intersections(xlo: int, xhi: int):
    """Yield exact leading-digit sectors meeting [xlo,xhi]."""
    first_decade = len(str(xlo)) - 1
    last_decade = len(str(xhi)) - 1

    for k in range(first_decade, last_decade + 1):
        scale = 10**k
        for digit in range(1, 10):
            lo = digit * scale
            hi = (digit + 1) * scale - 1
            if hi < xlo or lo > xhi:
                continue
            yield digit, max(lo, xlo), min(hi, xhi)


def _advance_rise_cells(cells: list[RiseCell], step: int) -> list[RiseCell]:
    """Impose one more exact r=1 step with full decimal consistency."""
    three_to_i = 3**step
    two_to_i = 1 << step
    modulus = 1 << (step + 1)
    next_modulus = modulus << 1
    out: list[RiseCell] = []

    for cell in cells:
        # The affine formula is
        #   2^i x_i = 3^i M + additive.
        # Endpoint evaluation is monotone in M; using all integer endpoints
        # is conservative before the residue filter and cannot lose a solution.
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

            correction = 2 * digit + 1
            next_additive = 3 * cell.additive + correction * two_to_i

            # Exact r=1 adds one binary digit to the unique lift.  The two
            # possible lifts of the previous class are tested exactly.
            for residue in (cell.residue, cell.residue + modulus):
                representative = _first_congruent(lo, residue, next_modulus)
                if representative > hi:
                    continue

                numerator = (
                    three_to_i * representative + cell.additive
                )
                assert numerator % two_to_i == 0
                x = numerator // two_to_i
                odd_numerator = 3 * x + correction

                if odd_numerator % 4 == 2:
                    out.append(
                        RiseCell(
                            lo=lo,
                            hi=hi,
                            additive=next_additive,
                            residue=residue % next_modulus,
                        )
                    )

    return out


def symbolic_rise_exists(lo: int, hi: int, steps: int) -> bool:
    """Exact existence test for an odd M in [lo,hi] with steps r=1 rises.

    Coverage is symbolic rather than seed-by-seed: cells split on every
    decimal leading-digit sector and retain exactly the compatible residue
    class modulo the next power of two.
    """
    if steps == 0:
        return lo <= hi

    cells = [RiseCell(lo=lo, hi=hi, additive=0, residue=1)]

    for step in range(steps):
        cells = _advance_rise_cells(cells, step)
        modulus = 1 << (step + 2)
        cells = [
            cell
            for cell in cells
            if _first_congruent(cell.lo, cell.residue, modulus) <= cell.hi
        ]
        if not cells:
            return False

    return True


def first_impossible_rise_length(
    lo: int, hi: int, cap: int = RISING_CHECK_CAP
) -> int | None:
    """First s<=cap for which no M in [lo,hi] has s exact r=1 rises."""
    cells = [RiseCell(lo=lo, hi=hi, additive=0, residue=1)]

    for step in range(cap):
        cells = _advance_rise_cells(cells, step)
        modulus = 1 << (step + 2)
        cells = [
            cell
            for cell in cells
            if _first_congruent(cell.lo, cell.residue, modulus) <= cell.hi
        ]
        if not cells:
            return step + 1

    return None


def run() -> dict:
    minimum = MINIMUM_ODD_STATE
    numerator, denominator = uniform_bound_fraction(minimum)
    survivors = product_candidate_periods_through()

    rows = []
    for q, r, three_to_q in survivors:
        minimum_rise = 2 * q - r
        max_minimum = maximum_minimum_state(r, three_to_q, minimum)
        first_impossible = first_impossible_rise_length(
            minimum, max_minimum
        )

        if first_impossible is None:
            raise AssertionError(
                "symbolic rise check cap is too small for exhaustive exclusion"
            )
        if first_impossible > minimum_rise:
            raise AssertionError(
                "product survivor was not excluded by the required rise length"
            )

        rows.append(
            {
                "q": q,
                "R": r,
                "required_minimum_rise": minimum_rise,
                "maximum_minimum_state": max_minimum,
                "first_impossible_rise_length": first_impossible,
            }
        )

    # Regression locks for the present bounded certificate.
    assert [(x["q"], x["R"]) for x in rows] == [
        (79_335, 125_743),
        (158_670, 251_486),
        (190_537, 301_994),
        (269_872, 427_737),
        (349_207, 553_480),
        (381_074, 603_988),
    ]
    assert [x["maximum_minimum_state"] for x in rows] == [
        10_369_168,
        5_184_598,
        589_078_792,
        10_189_804,
        5_139_366,
        294_539_410,
    ]
    assert [x["first_impossible_rise_length"] for x in rows] == [
        21,
        17,
        29,
        21,
        17,
        28,
    ]

    # For any remaining cycle q>=PERIOD_SCAN_LIMIT+1.  Since the structured
    # bound is <2, its R is bit_length(3^q).  Multiplication by 3 changes
    # bit_length by only 1 or 2, so k(q)=2q-R is nondecreasing.  Hence the
    # value at the next q is a valid uniform lower bound for the rise length.
    next_q = PERIOD_SCAN_LIMIT + 1
    next_r = (3**next_q).bit_length()
    remaining_minimum_rise = 2 * next_q - next_r
    assert remaining_minimum_rise == 166_015

    return {
        "schema_version": 2,
        "claim_type": "FINITE_EXACT_SYMBOLIC_ENUMERATION",
        "premise": (
            "one-rise/one-fall accelerated cycle entirely above 19 with "
            "minimum odd state >= 5000001"
        ),
        "premise_source": (
            "structured product envelope plus exhaustive seed census "
            "through 5000000"
        ),
        "uniform_product_bound": (
            "1 < 2^R/3^q <= M(M-19)/(M^2-57M+361)"
        ),
        "minimum_odd_state_used": minimum,
        "uniform_bound_numerator": numerator,
        "uniform_bound_denominator": denominator,
        "period_scan_limit": PERIOD_SCAN_LIMIT,
        "exact_product_window_survivors_through_limit": rows,
        "all_product_window_survivors_through_limit_fail_required_rise": True,
        "structured_q_excluded_through": PERIOD_SCAN_LIMIT,
        "minimum_rise_length_for_any_remaining_structured_cycle": (
            remaining_minimum_rise
        ),
        "symbolic_method": (
            "exact affine decimal-sector interval splitting plus exact "
            "residue lifting modulo successive powers of two for r=1"
        ),
        "symbolic_rise_check_cap": RISING_CHECK_CAP,
        "interpretation": (
            "Any different positive one-rise/one-fall accelerated cycle "
            "consistent with the 5M minimum-element exclusion must have "
            "q >= 400001 and at least 166015 consecutive r=1 rise steps. "
            "This remains a finite structured-class exclusion, not a "
            "global no-cycle theorem."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
