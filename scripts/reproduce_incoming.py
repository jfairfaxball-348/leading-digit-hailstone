#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from leading_digit_hailstone.core import DISTINGUISHED_CYCLE_SET, analyze, step

DEFAULT_RANDOM_SEED = 20260926


def exhaustive_census(stop: int) -> dict:
    steps_cache = {x: 0 for x in DISTINGUISHED_CYCLE_SET}
    peak_cache = {x: x for x in DISTINGUISHED_CYCLE_SET}
    entry_cache = {x: x for x in DISTINGUISHED_CYCLE_SET}
    best_steps = (-1, None)
    best_ratio = (0, 1, None, None)

    for seed in range(1, stop + 1):
        x = seed
        path: list[int] = []
        positions: dict[int, int] = {}
        while x not in steps_cache:
            if x in positions:
                cycle = path[positions[x]:]
                return {
                    "range": [1, stop],
                    "all_enter_distinguished_cycle": False,
                    "other_cycle": cycle,
                    "witness_seed": seed,
                }
            positions[x] = len(path)
            path.append(x)
            x = step(x)

        tail_steps = steps_cache[x]
        tail_peak = peak_cache[x]
        tail_entry = entry_cache[x]
        running_peak = tail_peak
        for value in reversed(path):
            running_peak = max(value, running_peak)
            tail_steps += 1
            steps_cache[value] = tail_steps
            peak_cache[value] = running_peak
            entry_cache[value] = tail_entry

        s = steps_cache[seed]
        p = peak_cache[seed]
        if s > best_steps[0]:
            best_steps = (s, seed)
        if p * best_ratio[1] > best_ratio[0] * seed:
            best_ratio = (p, seed, seed, p)

    return {
        "range": [1, stop],
        "all_enter_distinguished_cycle": True,
        "other_cycle": None,
        "max_cycle_entry_time": {"steps": best_steps[0], "seed": best_steps[1]},
        "max_excursion_ratio": {
            "seed": best_ratio[2],
            "max_excursion": best_ratio[3],
            "ratio_numerator": best_ratio[3],
            "ratio_denominator": best_ratio[2],
        },
    }


def deterministic_large_sample(count: int, min_digits: int, max_digits: int, cap: int) -> dict:
    rng = random.Random(DEFAULT_RANDOM_SEED)
    max_entry = (-1, None, None)
    failures: list[dict] = []
    entry_times: list[int] = []

    for i in range(count):
        digits = rng.randint(min_digits, max_digits)
        seed = int(str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(digits - 1)))
        result = analyze(seed, max_steps=cap)
        if result.status != "DISTINGUISHED_CYCLE":
            failures.append({"sample_index": i, "seed": str(seed), "status": result.status})
            continue
        assert result.cycle_entry_time is not None
        entry_times.append(result.cycle_entry_time)
        if result.cycle_entry_time > max_entry[0]:
            max_entry = (result.cycle_entry_time, i, seed)

    ordered = sorted(entry_times)
    median = None
    if ordered:
        mid = len(ordered) // 2
        median = ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2

    return {
        "exact_reproduction_of_incoming_random_sample": False,
        "reason": "The incoming observation did not provide an RNG seed or sample list.",
        "replacement_protocol": {
            "rng": "Python random.Random (Mersenne Twister)",
            "rng_seed": DEFAULT_RANDOM_SEED,
            "sample_count": count,
            "decimal_digits_inclusive": [min_digits, max_digits],
            "step_cap": cap,
        },
        "all_enter_distinguished_cycle": not failures,
        "failure_count": len(failures),
        "max_cycle_entry_time": {
            "steps": max_entry[0],
            "sample_index": max_entry[1],
            "seed": str(max_entry[2]) if max_entry[2] is not None else None,
        },
        "median_cycle_entry_time": median,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stop", type=int, default=1_000_000)
    parser.add_argument("--random-count", type=int, default=1000)
    parser.add_argument("--random-cap", type=int, default=100_000)
    parser.add_argument("--output", type=Path, default=Path("data/task1_reproduction.json"))
    args = parser.parse_args()

    exhaustive = exhaustive_census(args.stop)
    seed_917173 = analyze(917173, max_steps=args.random_cap).as_dict()
    seed_508701 = analyze(508701, max_steps=args.random_cap).as_dict()
    random_sample = deterministic_large_sample(args.random_count, 10, 200, args.random_cap)

    summary = {
        "schema_version": 1,
        "map": "T(n)=n/2 if even; 3n+2L(n)+1 if odd, decimal leading digit L",
        "exhaustive": exhaustive,
        "specific_seeds": {"917173": seed_917173, "508701": seed_508701},
        "large_random_sample": random_sample,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
