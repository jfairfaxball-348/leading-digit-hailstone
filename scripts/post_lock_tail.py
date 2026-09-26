from __future__ import annotations

import json
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, leading_digit
from scripts.structured_farey_extension import LOWER_1, UPPER_1
from scripts.structured_one_minimum_bound import MINIMUM_ODD_STATE, _first_congruent
from scripts.structured_record_chain import (
    cells_after_rises,
    maximum_minimum_state_log,
    next_upper_records,
    rise_residue_for_digits,
)

OUTPUT = Path("data/post_lock_tail.json")

# Finite exact diagnostic found while deliberately searching for long
# post-lock zero-lift tails.  This disproves any universal tail bound <= 5.
TAIL_COUNTEREXAMPLE = 43_574_304_770_317_398_119


def lock_depth(upper: int) -> int:
    """Return floor(log_2 upper), the bounded-range residue lock depth."""
    if upper < 1:
        raise ValueError("upper must be positive")
    return upper.bit_length() - 1


def direct_rise_profile(seed: int, cap: int = 256) -> dict[str, int]:
    """Follow one deterministic odd orbit until the first valuation != 1."""
    state = seed
    rises = 0

    for _ in range(cap):
        next_state, valuation = accelerated_odd_step(state)
        if valuation != 1:
            return {
                "total_exact_r1_rises": rises,
                "next_valuation": valuation,
                "terminal_rise_source": state,
                "next_odd_state": next_state,
            }
        state = next_state
        rises += 1

    raise AssertionError("direct rise cap is too small")


def state_after_exact_rises(seed: int, rises: int) -> int:
    """Return the state after a prescribed number of verified r=1 rises."""
    state = seed
    for _ in range(rises):
        state, valuation = accelerated_odd_step(state)
        if valuation != 1:
            raise AssertionError("seed does not realize the requested rise prefix")
    return state


def lock_and_follow(lo: int, hi: int, cap: int = 256) -> dict:
    """Exact finite-range certificate after bit-length locking.

    Symbolic decimal/2-adic coverage is used only through
    B=floor(log_2 hi).  At that depth every compatible start equals its
    canonical residue because 2^(B+1)>hi.  Each surviving start is therefore
    a concrete integer, so every later digit and valuation is obtained by
    deterministic direct continuation rather than further symbolic branching.
    """
    if not (1 <= lo <= hi):
        raise ValueError("require 1 <= lo <= hi")

    depth = lock_depth(hi)
    modulus = 1 << (depth + 1)
    if modulus <= hi:
        raise AssertionError("lock modulus must exceed upper endpoint")

    cells = cells_after_rises(lo, hi, depth)
    candidates: list[dict[str, int | str]] = []
    seen_starts: set[int] = set()

    for cell in cells:
        residue = rise_residue_for_digits(cell.digits)
        representative = _first_congruent(cell.lo, residue, modulus)
        if representative > cell.hi:
            raise AssertionError("surviving lock cell has no representative")

        # Both the representative and the canonical residue lie below modulus.
        # Hence bounded-range residue locking identifies them exactly.
        if representative != residue:
            raise AssertionError("lock representative did not equal canonical residue")
        if representative in seen_starts:
            raise AssertionError("duplicate locked start across symbolic cells")
        seen_starts.add(representative)

        profile = direct_rise_profile(representative, cap=cap)
        total_rises = profile["total_exact_r1_rises"]
        if total_rises < depth:
            raise AssertionError("locked candidate does not realize lock-depth rises")

        lock_state = state_after_exact_rises(representative, depth)
        if lock_state % 2 != 1:
            raise AssertionError("accelerated lock state must be odd")
        carry = (lock_state - 1) // 2
        if lock_state != 2 * carry + 1:
            raise AssertionError("post-lock state/carry identity failed")

        # Under zero lift, the exact carry recurrence is just the deterministic
        # odd-state recurrence rewritten with x=2H+1.
        if total_rises > depth:
            digit = leading_digit(lock_state)
            if (carry + digit) % 2 != 1:
                raise AssertionError("zero-lift parity disagrees with valuation one")
            next_state, valuation = accelerated_odd_step(lock_state)
            if valuation != 1:
                raise AssertionError("positive post-lock tail did not continue")
            next_carry = (1 + 3 * carry + digit) // 2
            if next_state != 2 * next_carry + 1:
                raise AssertionError("carry recurrence disagrees with direct orbit")

        candidates.append(
            {
                "start": representative,
                "lock_depth": depth,
                "digit_word_at_lock": "".join(str(digit) for digit in cell.digits),
                "state_at_lock": lock_state,
                "carry_at_lock": carry,
                "total_exact_r1_rises": total_rises,
                "post_lock_zero_lift_tail": total_rises - depth,
                "next_valuation": profile["next_valuation"],
                "terminal_rise_source": profile["terminal_rise_source"],
                "next_odd_state": profile["next_odd_state"],
            }
        )

    if not candidates:
        raise AssertionError(
            "lock-and-follow currently expects at least one lock-depth candidate"
        )

    candidates.sort(key=lambda row: int(row["start"]))
    maximum_rises = max(int(row["total_exact_r1_rises"]) for row in candidates)

    return {
        "range": [lo, hi],
        "lock_depth": depth,
        "lock_modulus": modulus,
        "locked_candidate_count": len(candidates),
        "locked_candidates": candidates,
        "maximum_exact_r1_rises": maximum_rises,
        "first_impossible_rise_length": maximum_rises + 1,
    }


def next_record_certificate() -> dict:
    """Certify the first Farey record beyond the PR #15 frontier."""
    # The established record-chain generator returns count+1 upper events so
    # that the final event supplies the right endpoint of the transfer block.
    events = next_upper_records(UPPER_1, LOWER_1, 8)
    event = events[7]
    next_event = events[8]

    upper = event["upper"]
    lower = event["lower_at_record"]
    next_upper = next_event["upper"]
    final_lower = next_event["lower_at_record"]

    maximum = maximum_minimum_state_log(upper)
    required_rise = 2 * upper.q - upper.r
    certificate = lock_and_follow(MINIMUM_ODD_STATE, maximum)

    if (upper.q, upper.r) != (890_638_885_193, 1_411_629_234_715):
        raise AssertionError("next record changed")
    if (lower.q, lower.r) != (753_110_839_881, 1_193_652_440_098):
        raise AssertionError("record lower neighbour changed")
    if (next_upper.q, next_upper.r) != (
        1_643_749_725_074,
        2_605_281_674_813,
    ):
        raise AssertionError("following upper record changed")
    if (final_lower.q, final_lower.r) != (
        753_110_839_881,
        1_193_652_440_098,
    ):
        raise AssertionError("final lower neighbour changed")
    if next_event["lower_updates_before_record"] != 0:
        raise AssertionError("unexpected lower update before following record")
    if maximum != 48_737_068_628_469:
        raise AssertionError("next-record product-window maximum changed")
    if required_rise != 369_648_535_671:
        raise AssertionError("next-record required rise changed")
    if certificate["first_impossible_rise_length"] != 49:
        raise AssertionError("next-record lock-and-follow extinction changed")
    if certificate["first_impossible_rise_length"] > required_rise:
        raise AssertionError("rise extinction is too late to exclude the record")

    excluded_through = next_upper.q - 1
    next_required_rise = 2 * next_upper.q - next_upper.r

    if excluded_through != 1_643_749_725_073:
        raise AssertionError("transferred period frontier changed")
    if next_required_rise != 682_217_775_335:
        raise AssertionError("next minimum rise bound changed")

    return {
        "record": {
            "q": upper.q,
            "R": upper.r,
            "lower_neighbor": {"q": lower.q, "R": lower.r},
            "maximum_minimum_state": maximum,
            "required_minimum_rise": required_rise,
        },
        "lock_and_follow": certificate,
        "following_upper_record": {
            "q": next_upper.q,
            "R": next_upper.r,
            "final_lower_neighbor": {"q": final_lower.q, "R": final_lower.r},
            "lower_updates_before_record": next_event["lower_updates_before_record"],
        },
        "structured_q_excluded_through": excluded_through,
        "first_q_not_covered_by_this_certificate": next_upper.q,
        "remaining_minimum_rise": next_required_rise,
    }


def run() -> dict:
    counter = direct_rise_profile(TAIL_COUNTEREXAMPLE)
    counter_depth = TAIL_COUNTEREXAMPLE.bit_length() - 1
    if counter_depth != 65:
        raise AssertionError("counterexample lock depth changed")
    if counter["total_exact_r1_rises"] != 71:
        raise AssertionError("counterexample rise length changed")
    if counter["next_valuation"] != 7:
        raise AssertionError("counterexample terminal valuation changed")

    counter_lock_state = state_after_exact_rises(
        TAIL_COUNTEREXAMPLE,
        counter_depth,
    )
    counter_carry = (counter_lock_state - 1) // 2

    record = next_record_certificate()

    return {
        "schema_version": 1,
        "claim_type": (
            "THEOREM_PLUS_FINITE_EXACT_SYMBOLIC_AND_DIRECT_CERTIFICATE"
        ),
        "theorem_level_results": {
            "post_lock_state_identity": (
                "Once a bounded start is locked, rho_s=M and "
                "3^s*M+A_s=2^s+H_s*2^(s+1), so the actual accelerated "
                "state is exactly x_s=1+2*H_s."
            ),
            "zero_lift_equivalence": (
                "With x_s=1+2*H_s and d_s=L(x_s), b_s=0 is equivalent to "
                "H_s+d_s being odd, which is exactly equivalent to "
                "v2(3*x_s+2*d_s+1)=1."
            ),
            "deterministic_tail_reduction": (
                "After lock depth B=floor(log_2 U), every compatible later "
                "zero lift is exactly one deterministic r=1 accelerated step "
                "of the locked integer. Symbolic decimal/2-adic branching is "
                "therefore unnecessary after B."
            ),
            "carry_is_half_state": (
                "Throughout a compatible post-lock tail, H_s=(x_s-1)/2 and "
                "H_(s+1)=(1+3*H_s+d_s)/2."
            ),
        },
        "finite_exact_route_falsification": {
            "statement": (
                "A universal constant post-lock tail bound <=5 is false."
            ),
            "start": TAIL_COUNTEREXAMPLE,
            "bit_length_lock_depth": counter_depth,
            "state_at_lock": counter_lock_state,
            "carry_at_lock": counter_carry,
            "total_exact_r1_rises": counter["total_exact_r1_rises"],
            "post_lock_zero_lift_tail": (
                counter["total_exact_r1_rises"] - counter_depth
            ),
            "next_valuation": counter["next_valuation"],
            "terminal_rise_source": counter["terminal_rise_source"],
            "next_odd_state": counter["next_odd_state"],
        },
        "next_farey_record_certificate": record,
        "interpretation": (
            "Post-lock dynamics has been reduced exactly to direct deterministic "
            "orbit following. This does not give a uniform F(B) tail bound: an "
            "explicit finite counterexample already has tail length 6. The new "
            "lock-and-follow certificate nevertheless eliminates the next Farey "
            "record and transfers the one-rise/one-fall period exclusion through "
            "q=1,643,749,725,073 under the existing 5,000,000-seed minimum premise. "
            "The arbitrary-cycle q>=971 consequence is unchanged."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
