from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, leading_digit
from scripts.post_lock_tail import direct_rise_profile
from scripts.structured_one_minimum_bound import _first_congruent
from scripts.structured_record_chain import cells_after_rises, rise_residue_for_digits

OUTPUT = Path("data/post_lock_geometry.json")
MAX_BIT_LENGTH = 100


def exact_r1_prefix(seed: int, rises: int) -> tuple[list[int], list[int]]:
    """Return states and source digits for a verified exact-r=1 prefix."""
    if seed <= 0 or seed % 2 == 0:
        raise ValueError("seed must be positive and odd")
    if rises < 0:
        raise ValueError("rises must be nonnegative")

    states = [seed]
    digits: list[int] = []
    state = seed

    for _ in range(rises):
        digit = leading_digit(state)
        next_state, valuation = accelerated_odd_step(state)
        if valuation != 1:
            raise AssertionError("seed does not realize the requested r=1 prefix")
        digits.append(digit)
        states.append(next_state)
        state = next_state

    return states, digits


def leading_digit_fraction(value: Fraction) -> int:
    """Leading decimal digit of a positive rational at least one."""
    if value < 1:
        raise ValueError("value must be at least one")

    integer_part = value.numerator // value.denominator
    scale = 10 ** (len(str(integer_part)) - 1)
    return value.numerator // (value.denominator * scale)


def finite_horizon_guide(seed: int, rises: int) -> dict:
    """Exact terminally anchored homogeneous guide for a finite r=1 prefix.

    If x_0,...,x_r is an exact-r=1 prefix, define

      g_s = x_r (2/3)^(r-s).

    Backward substitution in x_(j+1)=(3x_j+c_j)/2 gives

      g_s - x_s
        = sum_{j=s}^{r-1} (c_j/3) (2/3)^(j-s),

    so 0 <= g_s-x_s < 19. This is a finite-horizon identity and does
    not assume an infinite valuation-one orbit.
    """
    states, digits = exact_r1_prefix(seed, rises)
    terminal = states[-1]
    rows: list[dict[str, object]] = []
    maximum_gap = Fraction(0)
    mismatch_depths: list[int] = []

    for depth, state in enumerate(states):
        remaining = rises - depth
        guide = Fraction(
            terminal * (1 << remaining),
            3**remaining,
        )
        gap = guide - state

        if gap < 0 or gap >= 19:
            raise AssertionError("uniform finite-horizon discrepancy bound failed")

        if gap > maximum_gap:
            maximum_gap = gap

        actual_digit = leading_digit(state)
        guide_digit = leading_digit_fraction(guide)
        mismatch = actual_digit != guide_digit
        if mismatch:
            mismatch_depths.append(depth)

        rows.append(
            {
                "depth": depth,
                "state": state,
                "guide_numerator": guide.numerator,
                "guide_denominator": guide.denominator,
                "gap_numerator": gap.numerator,
                "gap_denominator": gap.denominator,
                "actual_leading_digit": actual_digit,
                "guide_leading_digit": guide_digit,
                "leading_digit_mismatch": mismatch,
            }
        )

    return {
        "seed": seed,
        "rises": rises,
        "terminal_state": terminal,
        "maximum_gap_numerator": maximum_gap.numerator,
        "maximum_gap_denominator": maximum_gap.denominator,
        "maximum_gap_less_than_19": maximum_gap < 19,
        "leading_digit_mismatch_depths": mismatch_depths,
        "rows": rows,
    }


def locked_candidates_for_bit_length(bit_length: int) -> list[dict[str, int]]:
    """Exhaust one exact bit-length interval through its lock depth.

    Here bit_length means B=floor(log_2 M), so the interval is
    2^B < M < 2^(B+1). Its lock depth is exactly B.
    """
    if bit_length < 1:
        raise ValueError("bit_length must be positive")

    lower = (1 << bit_length) + 1
    upper = (1 << (bit_length + 1)) - 1
    modulus = 1 << (bit_length + 1)

    cells = cells_after_rises(lower, upper, bit_length)
    rows: list[dict[str, int]] = []
    seen: set[int] = set()

    for cell in cells:
        residue = rise_residue_for_digits(cell.digits)
        representative = _first_congruent(cell.lo, residue, modulus)
        if representative > cell.hi:
            raise AssertionError("surviving lock cell has no representative")
        if representative != residue:
            raise AssertionError("bit-length locking did not identify the residue")
        if representative in seen:
            raise AssertionError("duplicate representative across lock cells")
        seen.add(representative)

        profile = direct_rise_profile(representative, cap=bit_length + 256)
        total = profile["total_exact_r1_rises"]
        if total < bit_length:
            raise AssertionError("lock candidate fails its certified rise prefix")

        rows.append(
            {
                "start": representative,
                "bit_length_lock_depth": bit_length,
                "total_exact_r1_rises": total,
                "post_lock_tail": total - bit_length,
                "next_valuation": profile["next_valuation"],
            }
        )

    rows.sort(key=lambda row: row["start"])
    return rows


def bit_length_scan(max_bit_length: int = MAX_BIT_LENGTH) -> dict:
    """Finite exact scan of complete bit-length intervals."""
    if max_bit_length < 1:
        raise ValueError("max_bit_length must be positive")

    nonempty: list[dict[str, object]] = []
    record_tails: list[dict[str, int]] = []
    record_tail = -1

    for bit_length in range(1, max_bit_length + 1):
        rows = locked_candidates_for_bit_length(bit_length)
        if not rows:
            continue

        interval_max = max(row["post_lock_tail"] for row in rows)
        nonempty.append(
            {
                "bit_length": bit_length,
                "locked_candidate_count": len(rows),
                "maximum_post_lock_tail": interval_max,
                "candidates": rows,
            }
        )

        if interval_max > record_tail:
            record_tail = interval_max
            winners = [
                row for row in rows if row["post_lock_tail"] == interval_max
            ]
            record_tails.append(
                {
                    "bit_length": bit_length,
                    "post_lock_tail": interval_max,
                    "start": winners[0]["start"],
                    "total_exact_r1_rises": winners[0]["total_exact_r1_rises"],
                    "next_valuation": winners[0]["next_valuation"],
                }
            )

    return {
        "maximum_bit_length_checked": max_bit_length,
        "nonempty_bit_length_count": len(nonempty),
        "maximum_post_lock_tail": max(
            row["maximum_post_lock_tail"] for row in nonempty
        ) if nonempty else None,
        "record_tails": record_tails,
        "nonempty_bit_lengths": nonempty,
    }


def run() -> dict:
    counterexample = 43_574_304_770_317_398_119
    profile = direct_rise_profile(counterexample)
    rises = profile["total_exact_r1_rises"]
    if rises != 71:
        raise AssertionError("known long-tail rise length changed")

    guide = finite_horizon_guide(counterexample, rises)
    scan = bit_length_scan()

    if scan["maximum_post_lock_tail"] != 6:
        raise AssertionError("bit-length scan tail record changed")
    if scan["record_tails"][-1]["start"] != counterexample:
        raise AssertionError("known tail-six example is no longer the scan record")

    return {
        "schema_version": 1,
        "claim_type": "THEOREM_PLUS_FINITE_EXACT_SYMBOLIC_AND_DIRECT_DIAGNOSTIC",
        "theorem_level_results": {
            "terminally_anchored_homogeneous_guide": (
                "For any finite exact-r=1 run x_0,...,x_N, the rational guide "
                "g_s=x_N*(2/3)^(N-s) satisfies "
                "g_s-x_s=sum_{j=s}^{N-1}(c_j/3)*(2/3)^(j-s), hence "
                "0<=g_s-x_s<19 for every s<=N."
            ),
            "decimal_boundary_separation": (
                "If x_s and its guide g_s have different leading-digit sectors, "
                "some decimal boundary C=d*10^k lies in (x_s,g_s], so "
                "0<=g_s-C<19."
            ),
            "same_sector_run_bound": (
                "During exact-r=1 dynamics, a fixed leading-digit sector with "
                "digit d>=2 is exited after one step; the digit-1 sector is "
                "exited after at most two steps. Thus no fixed leading digit can "
                "persist for more than two consecutive rise sources."
            ),
        },
        "finite_exact_diagnostics": {
            "known_tail_six_guide": {
                "seed": counterexample,
                "rises": rises,
                "maximum_gap_numerator": guide["maximum_gap_numerator"],
                "maximum_gap_denominator": guide["maximum_gap_denominator"],
                "leading_digit_mismatch_depths": guide[
                    "leading_digit_mismatch_depths"
                ],
            },
            "bit_length_scan": scan,
        },
        "interpretation": (
            "The terminally anchored guide gives a uniform absolute discrepancy "
            "bound of 19, stronger for finite runs than comparing every later "
            "state to the fixed lock-depth D_B coordinate. It localizes every "
            "possible digit-itinerary disagreement to a <19 window above a "
            "decimal boundary. The same-sector lemma removes sector persistence "
            "as the source of long tails. However, the exact scan through "
            "B<=100 still has record post-lock tail 6, and no uniform F(B) or "
            "F(M) tail theorem is proved."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
