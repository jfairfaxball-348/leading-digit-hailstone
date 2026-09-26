from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, analyze


def initial_v2_one_run(seed: int, limit: int = 100) -> tuple[int, list[dict]]:
    x = seed
    trace: list[dict] = []
    run = 0
    for _ in range(limit):
        nxt, valuation = accelerated_odd_step(x)
        trace.append({"state": x, "v2": valuation, "next_odd": nxt})
        if valuation != 1:
            break
        run += 1
        x = nxt
    return run, trace


def boundary_sweep() -> dict:
    rows = []
    for k in range(1, 201):
        for d in range(1, 10):
            boundary = d * 10**k
            for offset in (-1, 1):
                seed = boundary + offset
                r = analyze(seed, max_steps=200_000)
                rows.append(
                    {
                        "k": k,
                        "d": d,
                        "offset": offset,
                        "seed": seed,
                        "status": r.status,
                        "steps": r.cycle_entry_time,
                        "peak": r.max_excursion,
                    }
                )

    worst = max(rows, key=lambda row: row["steps"] if row["steps"] is not None else -1)
    ratio_case = max(rows, key=lambda row: Fraction(row["peak"], row["seed"]))
    return {
        "protocol": "d*10^k +/- 1 for d=1..9, k=1..200",
        "step_cap": 200_000,
        "tested_seed_count": len(rows),
        "all_entered_distinguished_cycle": all(row["status"] == "DISTINGUISHED_CYCLE" for row in rows),
        "worst_cycle_entry": worst,
        "max_excursion_ratio_case": ratio_case,
    }


def low_v2_scan() -> dict:
    best_run = -1
    best_seed = None
    best_trace = None
    for seed in range(1, 5_000_001, 2):
        run, trace = initial_v2_one_run(seed)
        if run > best_run:
            best_run = run
            best_seed = seed
            best_trace = trace
    return {"record_seed": best_seed, "run_length": best_run, "trace": best_trace}


def large_boundary_search() -> list[dict]:
    out = []
    for digits in (50, 100, 200):
        best = (-1, None, None)
        for d in range(1, 10):
            centre = d * 10 ** (digits - 1)
            for offset in range(-9999, 10000, 2):
                seed = centre + offset
                if seed <= 0 or seed % 2 == 0:
                    continue
                run, _ = initial_v2_one_run(seed)
                if run > best[0]:
                    best = (run, seed, (d, offset))

        run, seed, (d, offset) = best
        r = analyze(seed, max_steps=200_000)
        out.append(
            {
                "decimal_digits": digits,
                "seed": str(seed),
                "boundary_digit": d,
                "offset": offset,
                "initial_v2_one_run_length": run,
                "status": r.status,
                "cycle_entry_steps": r.cycle_entry_time,
                "peak": str(r.max_excursion),
            }
        )
    return out


def run() -> dict:
    return {
        "schema_version": 1,
        "evidence_type": "FINITE_COMPUTATION",
        "boundary_sweep": boundary_sweep(),
        "initial_v2_one_scan": low_v2_scan(),
        "large_boundary_engineering": large_boundary_search(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/adversarial_2026-09-26.full.json")
    args = parser.parse_args()
    payload = run()
    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
