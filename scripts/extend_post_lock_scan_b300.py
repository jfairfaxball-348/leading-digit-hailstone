from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, leading_digit
from scripts.post_lock_scale_geometry import (
    homogeneous_leading_digit,
    own_bit_locked_candidates,
    scaled_boundary_hits,
)

OUTPUT = Path("data/post_lock_scan_extension_b300.json")
START_BIT_DEPTH = 221
END_BIT_DEPTH = 300


def run() -> dict[str, object]:
    rows: list[dict[str, object]] = []

    for bit_depth in range(START_BIT_DEPTH, END_BIT_DEPTH + 1):
        rows.extend(own_bit_locked_candidates(bit_depth))

    histogram = Counter(int(row["post_lock_tail"]) for row in rows)
    positive = [row for row in rows if int(row["post_lock_tail"]) > 0]

    mismatch_count = 0
    boundary_hit_count = 0
    tail_three_rows: list[dict[str, object]] = []

    for row in positive:
        lock_state = int(row["state_at_lock"])
        tail = int(row["post_lock_tail"])
        state = lock_state
        mismatch_steps: list[int] = []
        boundary_steps: list[int] = []

        for step in range(tail + 1):
            if leading_digit(state) != homogeneous_leading_digit(lock_state, step):
                mismatch_steps.append(step)
            if step > 0 and scaled_boundary_hits(lock_state, step):
                boundary_steps.append(step)

            if step < tail:
                state, valuation = accelerated_odd_step(state)
                if valuation != 1:
                    raise AssertionError("recorded tail ended too early")

        mismatch_count += bool(mismatch_steps)
        boundary_hit_count += bool(boundary_steps)

        if tail == 3:
            tail_three_rows.append(
                {
                    "bit_depth": int(row["bit_depth"]),
                    "start": str(row["start"]),
                    "state_at_lock": str(row["state_at_lock"]),
                    "total_exact_r1_rises": int(row["total_exact_r1_rises"]),
                    "post_lock_tail": tail,
                    "next_valuation": int(row["next_valuation"]),
                    "homogeneous_digit_mismatch_steps": mismatch_steps,
                    "boundary_hit_steps": boundary_steps,
                }
            )

    if len(rows) != 37:
        raise AssertionError("B=221..300 locked-candidate count changed")
    if len(positive) != 17:
        raise AssertionError("B=221..300 positive-tail count changed")
    if dict(sorted(histogram.items())) != {0: 20, 1: 11, 2: 4, 3: 2}:
        raise AssertionError("B=221..300 tail histogram changed")
    if mismatch_count != 0 or boundary_hit_count != 0:
        raise AssertionError("new positive tails lost phase freezing")

    return {
        "schema_version": 1,
        "date": "2026-09-26",
        "claim_type": "FINITE_EXACT_SYMBOLIC_AND_DIRECT_DIAGNOSTIC",
        "bit_depth_range": [START_BIT_DEPTH, END_BIT_DEPTH],
        "additional_locked_candidate_count": len(rows),
        "additional_positive_tail_candidate_count": len(positive),
        "tail_histogram": {
            str(tail): histogram[tail]
            for tail in sorted(histogram)
        },
        "maximum_post_lock_tail_in_extension": max(histogram, default=0),
        "previous_complete_scan_maximum_tail": 6,
        "combined_complete_scan_bit_depth_range": [1, END_BIT_DEPTH],
        "combined_observed_maximum_post_lock_tail": 6,
        "positive_tail_boundary_hit_candidate_count": boundary_hit_count,
        "positive_tail_homogeneous_digit_mismatch_candidate_count": mismatch_count,
        "tail_three_cases": tail_three_rows,
        "interpretation": (
            "The complete own-bit diagnostic is extended from B<=220 through B<=300. "
            "No post-lock tail longer than the previously observed record 6 is found. "
            "This is finite exact computation only and does not establish a universal tail bound."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
