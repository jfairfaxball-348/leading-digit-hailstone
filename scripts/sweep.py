#!/usr/bin/env python3
"""Resumable exact batch sweep.

The checkpoint stores completed range and record summaries. Caches are rebuilt after
resume, which is slower than persisting a huge memo table but keeps checkpoints small,
portable, and auditable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from leading_digit_hailstone.core import analyze


def load_checkpoint(path: Path, start: int) -> dict:
    if not path.exists():
        return {
            "schema_version": 1,
            "start": start,
            "next_seed": start,
            "processed": 0,
            "status_counts": {},
            "record_cycle_entry_time": None,
            "record_excursion_ratio": None,
            "other_cycles": [],
        }
    return json.loads(path.read_text())


def save_checkpoint(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def better_ratio(candidate_peak: int, candidate_seed: int, current: dict | None) -> bool:
    if current is None:
        return True
    return candidate_peak * current["seed"] > current["max_excursion"] * candidate_seed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--stop", type=int, required=True)
    p.add_argument("--trajectory-cap", type=int, default=1_000_000)
    p.add_argument("--checkpoint", type=Path, default=Path("data/sweep_checkpoint.json"))
    p.add_argument("--checkpoint-every", type=int, default=10_000)
    args = p.parse_args()

    state = load_checkpoint(args.checkpoint, args.start)
    seed = max(args.start, int(state["next_seed"]))
    while seed <= args.stop:
        result = analyze(seed, max_steps=args.trajectory_cap)
        counts = state["status_counts"]
        counts[result.status] = counts.get(result.status, 0) + 1

        if result.status == "OTHER_CYCLE":
            cycle = list(result.detected_cycle)
            if cycle not in state["other_cycles"]:
                state["other_cycles"].append(cycle)

        if result.cycle_entry_time is not None:
            rec = state["record_cycle_entry_time"]
            if rec is None or result.cycle_entry_time > rec["steps"]:
                state["record_cycle_entry_time"] = {"seed": seed, "steps": result.cycle_entry_time}

        if better_ratio(result.max_excursion, seed, state["record_excursion_ratio"]):
            state["record_excursion_ratio"] = {
                "seed": seed,
                "max_excursion": result.max_excursion,
                "ratio_numerator": result.excursion_ratio_numerator,
                "ratio_denominator": result.excursion_ratio_denominator,
            }

        state["processed"] += 1
        state["next_seed"] = seed + 1
        if state["processed"] % args.checkpoint_every == 0:
            save_checkpoint(args.checkpoint, state)
        seed += 1

    save_checkpoint(args.checkpoint, state)
    print(json.dumps(state, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
