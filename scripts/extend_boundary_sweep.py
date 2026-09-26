from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.verify import VERIFY_CYCLE, step_independent


def analyze_independent(seed: int, cap: int = 200_000) -> dict:
    x = seed
    peak = seed
    seen: set[int] = set()

    for k in range(cap + 1):
        if x in VERIFY_CYCLE:
            return {"status": "DISTINGUISHED_CYCLE", "steps": k, "peak": peak}
        if x in seen:
            return {"status": "OTHER_CYCLE", "steps": None, "peak": peak}
        if k == cap:
            return {"status": "STEP_CAP", "steps": None, "peak": peak}
        seen.add(x)
        x = step_independent(x)
        peak = max(peak, x)

    raise AssertionError("unreachable")


def run(max_k: int = 500) -> dict:
    count = 0
    failures: list[dict] = []
    worst = None
    max_ratio = None

    for k in range(1, max_k + 1):
        power = 10**k
        for d in range(1, 10):
            for offset in (-1, 1):
                seed = d * power + offset
                result = analyze_independent(seed)
                count += 1

                row = {
                    "k": k,
                    "d": d,
                    "offset": offset,
                    "seed": str(seed),
                    **result,
                }

                if result["status"] != "DISTINGUISHED_CYCLE":
                    failures.append(row)

                if worst is None or (result["steps"] or -1) > (worst["steps"] or -1):
                    worst = row

                ratio = Fraction(result["peak"], seed)
                if max_ratio is None or ratio > max_ratio[0]:
                    max_ratio = (ratio, row)

    ratio, ratio_row = max_ratio
    return {
        "schema_version": 1,
        "evidence_type": "FINITE_COMPUTATION",
        "protocol": f"d*10^k +/- 1 for d=1..9, k=1..{max_k}",
        "implementation": "independent string-leading-digit verifier",
        "step_cap": 200_000,
        "tested_seed_count": count,
        "all_entered_distinguished_cycle": not failures,
        "failure_count": len(failures),
        "worst_cycle_entry": worst,
        "max_excursion_ratio_case": {
            **ratio_row,
            "ratio_numerator": ratio.numerator,
            "ratio_denominator": ratio.denominator,
        },
    }


def main() -> None:
    payload = run()
    out = Path("data/boundary_sweep_k500.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
