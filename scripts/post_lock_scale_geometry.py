from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, leading_digit
from scripts.post_lock_tail import direct_rise_profile, state_after_exact_rises
from scripts.structured_one_minimum_bound import _first_congruent
from scripts.structured_record_chain import cells_after_rises, rise_residue_for_digits

OUTPUT = Path("data/post_lock_scale_geometry.json")
BIT_DEPTH_SCAN_MAX = 220


def own_bit_interval(bit_depth: int) -> tuple[int, int]:
    """Return the odd-start interval having floor(log_2 M)=bit_depth."""
    if bit_depth < 1:
        raise ValueError("bit_depth must be at least 1")
    return (1 << bit_depth) + 1, (1 << (bit_depth + 1)) - 1


def homogeneous_leading_digit(lock_state: int, step: int) -> int:
    """Leading digit of the exact rational (3/2)^step * lock_state."""
    if lock_state < 1 or step < 0:
        raise ValueError("require a positive lock_state and nonnegative step")
    numerator = 3**step * lock_state
    denominator = 1 << step
    integer_part = numerator // denominator
    return leading_digit(integer_part)


def scaled_boundary_hits(lock_state: int, step: int) -> list[int]:
    """Return decimal boundaries in the exact post-lock length-19 corridor.

    A boundary C=d*10^k is a possible source of disagreement between the
    homogeneous digit of (3/2)^step*X and an r=1 orbit state only if

        X*3^step < C*2^step < (X+19)*3^step.

    The comparison is exact integer arithmetic.
    """
    if lock_state < 1 or step < 1:
        raise ValueError("require a positive lock_state and step")

    three_to_step = 3**step
    two_to_step = 1 << step
    lower = lock_state * three_to_step
    upper = (lock_state + 19) * three_to_step

    minimum_boundary = lower // two_to_step + 1
    maximum_boundary = (upper - 1) // two_to_step
    if minimum_boundary > maximum_boundary:
        return []

    first_decade = max(0, len(str(minimum_boundary)) - 2)
    last_decade = len(str(maximum_boundary))
    hits: list[int] = []

    for exponent in range(first_decade, last_decade + 1):
        scale = 10**exponent
        for digit in range(1, 10):
            boundary = digit * scale
            if not (minimum_boundary <= boundary <= maximum_boundary):
                continue
            scaled = boundary * two_to_step
            if lower < scaled < upper:
                hits.append(boundary)

    return hits


def own_bit_locked_candidates(bit_depth: int) -> list[dict[str, object]]:
    """Exactly enumerate starts of one bit depth that survive to their lock.

    On [2^B+1, 2^(B+1)-1], the exact rise residue modulus at depth B is
    2^(B+1), strictly larger than every start. Hence every surviving symbolic
    cell has at most one concrete start, equal to its canonical residue.
    """
    lo, hi = own_bit_interval(bit_depth)
    modulus = 1 << (bit_depth + 1)
    cells = cells_after_rises(lo, hi, bit_depth)

    rows: list[dict[str, object]] = []
    seen_starts: set[int] = set()

    for cell in cells:
        residue = rise_residue_for_digits(cell.digits)
        if residue != cell.residue % modulus:
            raise AssertionError("iterated lift disagrees with closed residue formula")

        representative = _first_congruent(cell.lo, residue, modulus)
        if representative > cell.hi:
            raise AssertionError("surviving lock cell has no representative")
        if representative != residue:
            raise AssertionError("own-bit lock representative is not canonical residue")
        if representative in seen_starts:
            raise AssertionError("duplicate own-bit locked start")
        seen_starts.add(representative)

        profile = direct_rise_profile(representative, cap=bit_depth + 4096)
        total_rises = profile["total_exact_r1_rises"]
        if total_rises < bit_depth:
            raise AssertionError("locked candidate fails its certified prefix")

        lock_state = state_after_exact_rises(representative, bit_depth)
        tail = total_rises - bit_depth
        state = lock_state
        boundary_hit_steps: list[int] = []
        homogeneous_digit_mismatch_steps: list[int] = []

        for step in range(tail + 1):
            if leading_digit(state) != homogeneous_leading_digit(lock_state, step):
                homogeneous_digit_mismatch_steps.append(step)
            if step > 0 and scaled_boundary_hits(lock_state, step):
                boundary_hit_steps.append(step)

            if step < tail:
                state, valuation = accelerated_odd_step(state)
                if valuation != 1:
                    raise AssertionError("post-lock tail ended before recorded length")

        rows.append(
            {
                "bit_depth": bit_depth,
                "start": representative,
                "state_at_lock": lock_state,
                "total_exact_r1_rises": total_rises,
                "post_lock_tail": tail,
                "next_valuation": profile["next_valuation"],
                "boundary_hit_steps": boundary_hit_steps,
                "homogeneous_digit_mismatch_steps": homogeneous_digit_mismatch_steps,
            }
        )

    rows.sort(key=lambda row: int(row["start"]))
    return rows


def scan_own_bit_locks(max_bit_depth: int = BIT_DEPTH_SCAN_MAX) -> dict[str, object]:
    """Finite exact diagnostic across complete own-bit lock intervals."""
    if max_bit_depth < 1:
        raise ValueError("max_bit_depth must be positive")

    rows: list[dict[str, object]] = []
    for bit_depth in range(1, max_bit_depth + 1):
        rows.extend(own_bit_locked_candidates(bit_depth))

    histogram = Counter(int(row["post_lock_tail"]) for row in rows)
    positive = [row for row in rows if int(row["post_lock_tail"]) > 0]

    record_milestones: list[dict[str, object]] = []
    best_tail = 0
    for row in rows:
        tail = int(row["post_lock_tail"])
        if tail > best_tail:
            best_tail = tail
            record_milestones.append(
                {
                    "bit_depth": row["bit_depth"],
                    "start": str(row["start"]),
                    "total_exact_r1_rises": row["total_exact_r1_rises"],
                    "post_lock_tail": tail,
                    "next_valuation": row["next_valuation"],
                }
            )

    long_rows = [
        {
            "bit_depth": row["bit_depth"],
            "start": str(row["start"]),
            "total_exact_r1_rises": row["total_exact_r1_rises"],
            "post_lock_tail": row["post_lock_tail"],
            "next_valuation": row["next_valuation"],
        }
        for row in rows
        if int(row["post_lock_tail"]) >= 4
    ]

    return {
        "bit_depth_range": [1, max_bit_depth],
        "maximum_start_exclusive": str(1 << (max_bit_depth + 1)),
        "own_bit_locked_candidate_count": len(rows),
        "positive_tail_candidate_count": len(positive),
        "tail_histogram": {
            str(tail): histogram[tail]
            for tail in sorted(histogram)
        },
        "maximum_post_lock_tail": max(histogram, default=0),
        "record_tail_milestones": record_milestones,
        "tail_at_least_four": long_rows,
        "positive_tail_boundary_hit_candidate_count": sum(
            bool(row["boundary_hit_steps"]) for row in positive
        ),
        "positive_tail_homogeneous_digit_mismatch_candidate_count": sum(
            bool(row["homogeneous_digit_mismatch_steps"]) for row in positive
        ),
    }


def run() -> dict[str, object]:
    scan = scan_own_bit_locks()
    if scan["own_bit_locked_candidate_count"] != 96:
        raise AssertionError("own-bit locked candidate count changed")
    if scan["positive_tail_candidate_count"] != 41:
        raise AssertionError("positive-tail candidate count changed")
    if scan["maximum_post_lock_tail"] != 6:
        raise AssertionError("finite scan tail record changed")
    if scan["positive_tail_boundary_hit_candidate_count"] != 0:
        raise AssertionError("finite scan found a boundary-corridor hit")
    if scan["positive_tail_homogeneous_digit_mismatch_candidate_count"] != 0:
        raise AssertionError("finite scan found a homogeneous digit mismatch")

    return {
        "schema_version": 1,
        "claim_type": (
            "ELEMENTARY_THEOREMS_PLUS_FINITE_EXACT_SYMBOLIC_AND_DIRECT_DIAGNOSTIC"
        ),
        "theorem_level_results": {
            "normalized_corridor": (
                "For a post-lock exact-r=1 segment X_0=X with "
                "2*X_(j+1)=3*X_j+c_j and 3<=c_j<=19, "
                "Z_j=(2/3)^j X_j satisfies "
                "Z_(j+1)-Z_j=(c_j/3)(2/3)^j. Hence "
                "3(1-(2/3)^t)<=Z_t-X<=19(1-(2/3)^t)<19."
            ),
            "decimal_boundary_corridor": (
                "If the actual leading digit at post-lock time t differs from "
                "the leading digit of the homogeneous rational (3/2)^t X, then "
                "some decimal boundary C=d*10^k satisfies "
                "X*3^t < C*2^t < (X+19)*3^t."
            ),
            "same_sector_exit": (
                "During exact-r=1 dynamics, a leading-digit sector d*10^k "
                "with d>=2 is left after one step; the digit-1 sector can supply "
                "at most two consecutive source states."
            ),
            "six_step_decade_crossing": (
                "Six consecutive exact-r=1 steps increase the state by a "
                "factor strictly greater than (3/2)^6=729/64>10, so at least "
                "one power-of-ten boundary is crossed."
            ),
        },
        "finite_exact_bit_depth_scan": scan,
        "interpretation": (
            "The post-lock decimal itinerary is confined to an exact normalized "
            "corridor of width less than 19. In the complete own-bit lock scan "
            "through B=220, every positive post-lock tail already follows the "
            "homogeneous (3/2)^t leading-digit itinerary without a decimal-boundary "
            "corridor hit. Thus boundary proximity is not a necessary mechanism "
            "for the observed long tails; parity/congruence along a phase-frozen "
            "digit itinerary remains the sharper obstruction. The observed maximum "
            "tail 6 is finite computation, not a universal bound."
        ),
        "limitations": (
            "No scale-aware F(B) or F(M) tail theorem is proved. The structured "
            "one-rise/one-fall frontier and the arbitrary-cycle q>=971 bound are "
            "unchanged."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
