from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, leading_digit

OUTPUT = Path("data/post_lock_terminal_guide.json")
KNOWN_TAIL_SIX_LOCK_STATE = 12_166_406_006_866_046_930_622_304_922_581
KNOWN_TAIL_SIX_LENGTH = 6


def leading_digit_fraction(value: Fraction) -> int:
    """Return the leading decimal digit of a positive rational >= 1."""
    if value < 1:
        raise ValueError("value must be at least one")

    integer_part = value.numerator // value.denominator
    scale = 10 ** (len(str(integer_part)) - 1)
    return value.numerator // (value.denominator * scale)


def exact_r1_segment(start: int, rises: int) -> tuple[list[int], list[int]]:
    """Return states and source corrections for a verified exact-r=1 segment."""
    if start <= 0 or start % 2 == 0:
        raise ValueError("start must be positive and odd")
    if rises < 0:
        raise ValueError("rises must be nonnegative")

    states = [start]
    corrections: list[int] = []
    state = start

    for _ in range(rises):
        digit = leading_digit(state)
        correction = 2 * digit + 1
        next_state, valuation = accelerated_odd_step(state)
        if valuation != 1:
            raise AssertionError("segment ended before the requested rise length")

        corrections.append(correction)
        states.append(next_state)
        state = next_state

    return states, corrections


def terminal_guide_profile(start: int, rises: int) -> dict[str, object]:
    """Exact finite-horizon homogeneous guide anchored at the terminal state.

    Let x_0,...,x_N be an exact-r=1 segment and define

      g_s = x_N (2/3)^(N-s).

    Backward substitution in

      x_(j+1) = (3 x_j + c_j)/2

    gives

      g_s - x_s
        = sum_(j=s)^(N-1) (c_j/3) (2/3)^(j-s).

    Since 3 <= c_j <= 19, every gap lies in [0,19).
    """
    states, corrections = exact_r1_segment(start, rises)
    terminal = states[-1]
    rows: list[dict[str, object]] = []
    maximum_gap = Fraction(0)
    mismatch_depths: list[int] = []

    for depth, state in enumerate(states):
        remaining = rises - depth
        guide = Fraction(terminal * (1 << remaining), 3**remaining)
        gap = guide - state

        if gap < 0 or gap >= 19:
            raise AssertionError("terminal guide left the uniform width-19 corridor")

        if depth < rises:
            weighted_gap = Fraction(0)
            weight = Fraction(1)
            for correction in corrections[depth:]:
                weighted_gap += Fraction(correction, 3) * weight
                weight *= Fraction(2, 3)
            if weighted_gap != gap:
                raise AssertionError("backward weighted-sum identity failed")
        elif gap != 0:
            raise AssertionError("terminal guide must equal the terminal state")

        actual_digit = leading_digit(state)
        guide_digit = leading_digit_fraction(guide)
        if actual_digit != guide_digit:
            mismatch_depths.append(depth)

        maximum_gap = max(maximum_gap, gap)
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
            }
        )

    return {
        "start": start,
        "rises": rises,
        "terminal_state": terminal,
        "maximum_gap_numerator": maximum_gap.numerator,
        "maximum_gap_denominator": maximum_gap.denominator,
        "leading_digit_mismatch_depths": mismatch_depths,
        "rows": rows,
    }


def run() -> dict[str, object]:
    profile = terminal_guide_profile(
        KNOWN_TAIL_SIX_LOCK_STATE,
        KNOWN_TAIL_SIX_LENGTH,
    )
    terminal = int(profile["terminal_state"])
    _, next_valuation = accelerated_odd_step(terminal)

    maximum_gap = Fraction(
        int(profile["maximum_gap_numerator"]),
        int(profile["maximum_gap_denominator"]),
    )
    if maximum_gap != Fraction(235, 27):
        raise AssertionError("known tail-six terminal-guide maximum changed")
    if profile["leading_digit_mismatch_depths"] != []:
        raise AssertionError("known tail-six terminal guide changed digit itinerary")
    if next_valuation != 7:
        raise AssertionError("known tail-six terminal valuation changed")

    return {
        "schema_version": 1,
        "claim_type": "ELEMENTARY_THEOREM_PLUS_FINITE_EXACT_DIAGNOSTIC",
        "theorem_level_results": {
            "terminally_anchored_homogeneous_guide": (
                "For every finite exact-r=1 segment x_0,...,x_N, define "
                "g_s=x_N*(2/3)^(N-s). Then "
                "g_s-x_s=sum_{j=s}^{N-1}(c_j/3)*(2/3)^(j-s), so "
                "0<=g_s-x_s<19 for every s<=N."
            ),
            "terminal_boundary_localization": (
                "If x_s and g_s have different leading-digit sectors, some "
                "decimal boundary C=d*10^k lies in (x_s,g_s], hence "
                "0<=g_s-C<19."
            ),
        },
        "finite_exact_diagnostic": {
            "lock_state": str(KNOWN_TAIL_SIX_LOCK_STATE),
            "post_lock_tail_length": KNOWN_TAIL_SIX_LENGTH,
            "terminal_state": str(profile["terminal_state"]),
            "next_valuation": next_valuation,
            "maximum_terminal_guide_gap": {
                "numerator": profile["maximum_gap_numerator"],
                "denominator": profile["maximum_gap_denominator"],
            },
            "leading_digit_mismatch_depths": profile[
                "leading_digit_mismatch_depths"
            ],
            "guide_digits": [
                row["guide_leading_digit"] for row in profile["rows"]
            ],
            "actual_digits": [
                row["actual_leading_digit"] for row in profile["rows"]
            ],
        },
        "interpretation": (
            "The forward normalized corridor from PR #17 and this terminally "
            "anchored guide are complementary. The forward coordinate keeps "
            "(2/3)^s x_s inside a fixed width-19 interval above the lock state; "
            "the terminal guide instead keeps one concrete homogeneous orbit "
            "within absolute distance 19 above every earlier state of any finite "
            "r=1 segment. This sharpens candidate-specific decimal-phase "
            "certification but does not prove a uniform F(B) or F(M) tail bound."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
