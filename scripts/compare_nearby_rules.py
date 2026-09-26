from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.core import leading_digit

FROZEN = tuple(2 * d + 1 for d in range(1, 10))


def step_with(n: int, corrections: tuple[int, ...]) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    if n % 2 == 0:
        return n // 2
    return 3 * n + corrections[leading_digit(n) - 1]


def canonical_cycle(values: tuple[int, ...]) -> tuple[int, ...]:
    return min(values[i:] + values[:i] for i in range(len(values)))


def cycle_census(corrections: tuple[int, ...], stop: int = 100_000, cap: int = 100_000) -> dict:
    known: dict[int, tuple[int, ...]] = {}
    basins: Counter[tuple[int, ...]] = Counter()
    unresolved = 0

    for seed in range(1, stop + 1):
        x = seed
        path: list[int] = []
        index: dict[int, int] = {}

        while x not in known and x not in index and len(path) < cap:
            index[x] = len(path)
            path.append(x)
            x = step_with(x, corrections)

        if x in known:
            cycle = known[x]
        elif x in index:
            cycle = canonical_cycle(tuple(path[index[x] :]))
        else:
            unresolved += 1
            continue

        for value in path:
            known[value] = cycle
        basins[cycle] += 1

    return {
        "num_cycles": len(basins),
        "unresolved": unresolved,
        "basins": [
            {"cycle": list(cycle), "count": count}
            for cycle, count in sorted(basins.items(), key=lambda item: (-item[1], item[0]))
        ],
    }


def analyze_to_cycle(seed: int, corrections: tuple[int, ...], cap: int = 100_000) -> tuple[tuple[int, ...], int, int]:
    x = seed
    path: list[int] = []
    index: dict[int, int] = {}

    for _ in range(cap + 1):
        if x in index:
            entry = index[x]
            cycle = canonical_cycle(tuple(path[entry:]))
            peak_to_entry = max(path[: entry + 1])
            return cycle, entry, peak_to_entry
        if len(path) >= cap:
            raise RuntimeError(f"cap hit for seed {seed}")
        index[x] = len(path)
        path.append(x)
        x = step_with(x, corrections)

    raise AssertionError("unreachable")


def metric_summary(corrections: tuple[int, ...], stop: int = 10_000) -> dict:
    total = 0
    max_preperiod = (-1, None)
    max_ratio = (Fraction(0), None, None)

    for seed in range(1, stop + 1):
        _, entry, peak = analyze_to_cycle(seed, corrections)
        total += entry
        if entry > max_preperiod[0]:
            max_preperiod = (entry, seed)
        ratio = Fraction(peak, seed)
        if ratio > max_ratio[0]:
            max_ratio = (ratio, seed, peak)

    return {
        "mean_preperiod": total / stop,
        "max_preperiod": {"steps": max_preperiod[0], "seed": max_preperiod[1]},
        "max_excursion_ratio": {
            "seed": max_ratio[1],
            "peak": max_ratio[2],
            "numerator": max_ratio[0].numerator,
            "denominator": max_ratio[0].denominator,
        },
    }


def run() -> dict:
    result = {
        "schema_version": 1,
        "evidence_type": "FINITE_COMPUTATION",
        "cycle_census_range": [1, 100_000],
        "cycle_detection_step_cap": 100_000,
        "global_shifts": [],
        "single_digit_perturbations": [],
    }

    for b in (-3, -1, 1, 3, 5):
        corrections = tuple(2 * d + b for d in range(1, 10))
        item = {"b": b, "corrections": list(corrections)}
        item.update(cycle_census(corrections))
        item["metrics_1_to_10000"] = metric_summary(corrections)
        result["global_shifts"].append(item)

    for digit in range(1, 10):
        for delta in (-2, 2):
            corrections = list(FROZEN)
            corrections[digit - 1] += delta
            census = cycle_census(tuple(corrections))
            result["single_digit_perturbations"].append(
                {"digit": digit, "delta": delta, "corrections": corrections, **census}
            )

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/nearby_rule_comparison.full.json")
    args = parser.parse_args()
    payload = run()
    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload["global_shifts"], indent=2))


if __name__ == "__main__":
    main()
