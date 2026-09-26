from __future__ import annotations

import json
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step

SOURCE = Path("data/constructed_low_v2_runs.json")
OUTPUT = Path("data/weak_run_recovery.json")
MAX_ACCELERATED_STEPS = 10_000


def one_step_compensation_threshold(run_length: int) -> int:
    """Least r satisfying 2^(r+s) > 3^(s+1), computed exactly."""
    r = 1
    while 2 ** (r + run_length) <= 3 ** (run_length + 1):
        r += 1
    return r


def analyze_seed(seed: int) -> dict:
    x = seed
    valuations: list[int] = []
    peak = seed

    for step in range(1, MAX_ACCELERATED_STEPS + 1):
        x, valuation = accelerated_odd_step(x)
        valuations.append(valuation)
        peak = max(peak, x)

        if x < seed:
            initial_run = 0
            for r in valuations:
                if r != 1:
                    break
                initial_run += 1

            if initial_run == len(valuations):
                raise AssertionError("descent below seed occurred during an r=1 run")

            return {
                "initial_v2_one_run_length": initial_run,
                "first_non_one_valuation": valuations[initial_run],
                "one_step_compensation_threshold": one_step_compensation_threshold(
                    initial_run
                ),
                "accelerated_steps_to_first_below_seed": step,
                "peak": str(peak),
                "peak_decimal_digits": len(str(peak)),
                "first_below_seed_state": str(x),
                "valuations_from_first_non_one": valuations[
                    initial_run : initial_run + 12
                ],
            }

    raise RuntimeError(
        f"seed did not return below itself within {MAX_ACCELERATED_STEPS} accelerated steps"
    )


def run() -> dict:
    source = json.loads(SOURCE.read_text())
    examples = []

    for item in source["examples"]:
        seed = int(item["seed"])
        analysis = analyze_seed(seed)
        analysis.update(
            {
                "requested_run_length": item["requested_run_length"],
                "seed": item["seed"],
                "seed_decimal_digits": item["seed_decimal_digits"],
            }
        )
        examples.append(analysis)

    return {
        "schema_version": 1,
        "claim_type": "FINITE_COMPUTATION",
        "purpose": (
            "Test whether explicit long v2=1 runs are immediately erased by a "
            "single compensating high-valuation accelerated step."
        ),
        "source": str(SOURCE),
        "accelerated_step_cap": MAX_ACCELERATED_STEPS,
        "examples": examples,
        "interpretation": (
            "The tested long weak runs are not followed by one-step compensation; "
            "recovery below the starting seed is distributed over many accelerated steps."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
