from __future__ import annotations

import json
from pathlib import Path

from compare_nearby_rules import FROZEN, cycle_census

SURVIVORS_AT_100K = (
    (2, 2),
    (3, 2),
    (4, 2),
    (5, -2),
    (6, -2),
    (8, 2),
    (9, 2),
)


def run() -> dict:
    payload = {
        "schema_version": 1,
        "evidence_type": "FINITE_COMPUTATION",
        "cycle_census_range": [1, 1_000_000],
        "cycle_detection_step_cap": 100_000,
        "global_shifts": [],
        "single_digit_survivors_from_100k": [],
    }

    for b in (-3, -1, 1, 3, 5):
        corrections = tuple(2 * d + b for d in range(1, 10))
        census = cycle_census(corrections, stop=1_000_000, cap=100_000)
        payload["global_shifts"].append(
            {
                "b": b,
                "num_cycles": census["num_cycles"],
                "unresolved": census["unresolved"],
                "basins": census["basins"],
            }
        )

    for digit, delta in SURVIVORS_AT_100K:
        corrections = list(FROZEN)
        corrections[digit - 1] += delta
        census = cycle_census(tuple(corrections), stop=1_000_000, cap=100_000)
        payload["single_digit_survivors_from_100k"].append(
            {
                "digit": digit,
                "delta": delta,
                "num_cycles": census["num_cycles"],
                "unresolved": census["unresolved"],
                "basins": census["basins"],
            }
        )

    return payload


def main() -> None:
    payload = run()
    out = Path("data/nearby_rule_extension_1m.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
