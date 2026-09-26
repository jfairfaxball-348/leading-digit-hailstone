from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from leading_digit_hailstone.verify import (
    VERIFY_CYCLE,
    leading_digit_independent,
    step_independent,
)
from scripts.construct_low_v2_runs import homogeneous_digit_word, forced_residue

OUTPUT = Path("data/stage1_final_red_team.json")
RAW_STEP_CAP = 200_000

BOUNDARY_EXPONENTS = (600, 800, 1000, 1200, 1500, 1800, 2000)
BOUNDARY_OFFSETS = (-999, -99, -19, -9, -3, -1, 1, 3, 9, 19, 99, 999)

RANDOM_SEED = 20_260_926
RANDOM_DIGITS = (20, 50, 100, 250, 500, 1000, 2000)
RANDOM_PER_SCALE = 50

INVERSE_DEPTH = 45
INVERSE_SAMPLE = 250
INVERSE_OFFSETS = (-5, -3, -1, 1, 3, 5)

WEAK_RUN_CASES = (
    (150, 350),
    (300, 710),
    (500, 1190),
    (750, 1790),
    (1000, 2390),
)


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    return (n & -n).bit_length() - 1


def analyze_adversarial(seed: int, cap: int = RAW_STEP_CAP) -> dict[str, int | str | None]:
    """Independent exact trajectory diagnostics for one positive seed."""
    x = seed
    peak = seed
    first_descent: int | None = None
    max_valuation = 0
    current_r1 = 0
    max_r1 = 0
    seen: set[int] = set()

    for steps in range(cap + 1):
        if x in VERIFY_CYCLE:
            return {
                "status": "DISTINGUISHED_CYCLE",
                "cycle_entry_steps": steps,
                "first_descent_steps": first_descent,
                "max_excursion": peak,
                "max_odd_branch_valuation": max_valuation,
                "max_consecutive_r1": max_r1,
            }
        if x in seen:
            return {
                "status": "OTHER_CYCLE",
                "cycle_entry_steps": None,
                "first_descent_steps": first_descent,
                "max_excursion": peak,
                "max_odd_branch_valuation": max_valuation,
                "max_consecutive_r1": max_r1,
                "repeated_state": x,
            }
        if steps == cap:
            return {
                "status": "STEP_CAP",
                "cycle_entry_steps": None,
                "first_descent_steps": first_descent,
                "max_excursion": peak,
                "max_odd_branch_valuation": max_valuation,
                "max_consecutive_r1": max_r1,
            }

        seen.add(x)
        if x & 1:
            numerator = step_independent(x)
            valuation = v2(numerator)
            max_valuation = max(max_valuation, valuation)
            if valuation == 1:
                current_r1 += 1
                max_r1 = max(max_r1, current_r1)
            else:
                current_r1 = 0

        x = step_independent(x)
        peak = max(peak, x)
        if first_descent is None and x < seed:
            first_descent = steps + 1

    raise AssertionError("unreachable")


def compact_integer(n: int) -> str | dict[str, int | str]:
    text = str(n)
    if len(text) <= 90:
        return text
    return {
        "decimal_digits": len(text),
        "prefix_40": text[:40],
        "suffix_40": text[-40:],
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
    }


def seed_set_sha256(seeds: list[int]) -> str:
    payload = "\n".join(sorted(str(seed) for seed in seeds)) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def compact_case(case: dict[str, object]) -> dict[str, object]:
    result = dict(case["result"])
    peak = int(result.pop("max_excursion"))
    row = {
        key: case[key]
        for key in ("k", "d", "offset", "digits", "index", "source")
        if key in case
    }
    row["seed"] = compact_integer(int(case["seed"]))
    row.update(result)
    row["max_excursion"] = compact_integer(peak)
    return row


def summarize_cases(cases: list[dict[str, object]]) -> dict[str, object]:
    failures = [
        case
        for case in cases
        if case["result"]["status"] != "DISTINGUISHED_CYCLE"
    ]
    worst_entry = max(
        cases,
        key=lambda case: int(case["result"]["cycle_entry_steps"] or -1),
    )
    longest_descent = max(
        cases,
        key=lambda case: int(case["result"]["first_descent_steps"] or -1),
    )
    largest_valuation = max(
        cases,
        key=lambda case: int(case["result"]["max_odd_branch_valuation"]),
    )
    longest_r1 = max(
        cases,
        key=lambda case: int(case["result"]["max_consecutive_r1"]),
    )

    return {
        "tested_seed_count": len(cases),
        "all_entered_distinguished_cycle": not failures,
        "failure_count": len(failures),
        "failures": [compact_case(case) for case in failures[:10]],
        "seed_set_sha256": seed_set_sha256(
            [int(case["seed"]) for case in cases]
        ),
        "worst_cycle_entry": compact_case(worst_entry),
        "longest_first_descent": compact_case(longest_descent),
        "largest_valuation": compact_case(largest_valuation),
        "longest_consecutive_r1": compact_case(longest_r1),
    }


def boundary_campaign() -> dict[str, object]:
    cases: list[dict[str, object]] = []
    for k in BOUNDARY_EXPONENTS:
        scale = 10**k
        for d in range(1, 10):
            for offset in BOUNDARY_OFFSETS:
                seed = d * scale + offset
                cases.append(
                    {
                        "k": k,
                        "d": d,
                        "offset": offset,
                        "seed": seed,
                        "result": analyze_adversarial(seed),
                    }
                )

    out = summarize_cases(cases)
    out["protocol"] = {
        "decimal_exponents": list(BOUNDARY_EXPONENTS),
        "boundary_digits": list(range(1, 10)),
        "offsets": list(BOUNDARY_OFFSETS),
        "raw_step_cap": RAW_STEP_CAP,
    }
    return out


def random_campaign() -> dict[str, object]:
    rng = random.Random(RANDOM_SEED)
    cases: list[dict[str, object]] = []

    for digits in RANDOM_DIGITS:
        lower = 10 ** (digits - 1)
        for index in range(RANDOM_PER_SCALE):
            seed = lower + rng.randrange(9 * lower)
            if seed % 2 == 0:
                seed += 1
            cases.append(
                {
                    "digits": digits,
                    "index": index,
                    "seed": seed,
                    "result": analyze_adversarial(seed),
                }
            )

    out = summarize_cases(cases)
    out["protocol"] = {
        "python_random_seed": RANDOM_SEED,
        "decimal_digit_scales": list(RANDOM_DIGITS),
        "odd_samples_per_scale": RANDOM_PER_SCALE,
        "raw_step_cap": RAW_STEP_CAP,
    }
    return out


def inverse_preimages(m: int) -> tuple[int, ...]:
    candidates = {2 * m}

    if m % 2 == 0:
        for d in range(1, 10):
            numerator = m - 2 * d - 1
            if numerator <= 0 or numerator % 3:
                continue
            n = numerator // 3
            if (
                n % 2 == 1
                and leading_digit_independent(n) == d
                and step_independent(n) == m
            ):
                candidates.add(n)

    return tuple(sorted(candidates))


def inverse_frontier(
    depth: int,
) -> tuple[set[int], set[int], list[dict[str, int]]]:
    seen = set(VERIFY_CYCLE)
    frontier = set(VERIFY_CYCLE)
    profile: list[dict[str, int]] = []

    for level in range(1, depth + 1):
        next_frontier: set[int] = set()
        odd_edges = 0

        for value in frontier:
            for predecessor in inverse_preimages(value):
                if predecessor & 1:
                    odd_edges += 1
                if predecessor not in seen:
                    next_frontier.add(predecessor)

        seen.update(next_frontier)
        frontier = next_frontier
        profile.append(
            {
                "depth": level,
                "new_nodes": len(frontier),
                "odd_preimage_edges": odd_edges,
                "maximum_node": max(frontier) if frontier else 0,
            }
        )

    return seen, frontier, profile


def inverse_campaign() -> dict[str, object]:
    seen, frontier, profile = inverse_frontier(INVERSE_DEPTH)
    dead_ends = [
        value
        for value in frontier
        if not any(predecessor & 1 for predecessor in inverse_preimages(value))
    ]
    selected = sorted(dead_ends, reverse=True)[:INVERSE_SAMPLE]

    by_seed: dict[int, dict[str, object]] = {}
    for source in selected:
        for offset in INVERSE_OFFSETS:
            seed = source + offset
            if seed <= 0:
                continue
            if seed % 2 == 0:
                seed += 1
            by_seed[seed] = {
                "source": source,
                "offset": offset,
                "seed": seed,
                "result": analyze_adversarial(seed),
            }

    out = summarize_cases(
        [by_seed[seed] for seed in sorted(by_seed)]
    )
    out["protocol"] = {
        "inverse_depth": INVERSE_DEPTH,
        "total_distinct_nodes_through_depth": len(seen),
        "frontier_nodes": len(frontier),
        "frontier_nodes_without_odd_preimage": len(dead_ends),
        "selected_largest_dead_ends": len(selected),
        "requested_offsets": list(INVERSE_OFFSETS),
        "odd_seed_adjustment": (
            "add 1 when source+offset is even, then deduplicate"
        ),
        "raw_step_cap": RAW_STEP_CAP,
        "terminal_frontier_profile": profile[-1],
    }
    return out


def accelerated_odd_independent(n: int) -> tuple[int, int]:
    if n <= 0 or n % 2 == 0:
        raise ValueError("accelerated odd step requires a positive odd input")
    numerator = step_independent(n)
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def initial_r1_run(seed: int, cap: int) -> int:
    state = seed
    for run in range(cap):
        state, valuation = accelerated_odd_independent(state)
        if valuation != 1:
            return run
    raise AssertionError("r1 cap too small")


def weak_run_case(length: int, decimal_scale: int) -> dict[str, object]:
    digits = homogeneous_digit_word(length)
    residue, modulus = forced_residue(digits)
    target = 7 * 10**decimal_scale // 3
    seed = target + ((residue - target) % modulus)

    state = seed
    for digit in digits:
        if leading_digit_independent(state) != digit:
            raise AssertionError("constructed digit word changed")
        state, valuation = accelerated_odd_independent(state)
        if valuation != 1:
            raise AssertionError("constructed run ended early")

    observed = initial_r1_run(seed, length + 100)
    result = analyze_adversarial(seed)

    return {
        "requested_r1_run": length,
        "decimal_scale": decimal_scale,
        "seed": compact_integer(seed),
        "observed_initial_r1_run": observed,
        "trajectory_status": result["status"],
        "cycle_entry_steps": result["cycle_entry_steps"],
        "first_descent_steps": result["first_descent_steps"],
        "max_odd_branch_valuation": result["max_odd_branch_valuation"],
        "max_consecutive_r1": result["max_consecutive_r1"],
        "max_excursion": compact_integer(int(result["max_excursion"])),
    }


def weak_run_campaign() -> dict[str, object]:
    cases = [
        weak_run_case(length, decimal_scale)
        for length, decimal_scale in WEAK_RUN_CASES
    ]

    return {
        "protocol": {
            "construction": (
                "unique 2-adic residue for the alpha=7/3 "
                "homogeneous leading-digit word"
            ),
            "requested_run_and_decimal_scale": [
                list(case) for case in WEAK_RUN_CASES
            ],
            "raw_step_cap": RAW_STEP_CAP,
        },
        "all_entered_distinguished_cycle": all(
            case["trajectory_status"] == "DISTINGUISHED_CYCLE"
            for case in cases
        ),
        "cases": cases,
    }


def _seed_form(row: dict[str, object]) -> str:
    offset = int(row["offset"])
    return f'{row["d"]}*10^{row["k"]}{offset:+d}'


def _compact_random_record(row: dict[str, object]) -> dict[str, object]:
    seed = row["seed"]
    if not isinstance(seed, dict):
        raise AssertionError("large random record unexpectedly has a short seed")
    return {
        "decimal_digits": row["digits"],
        "index": row["index"],
        "cycle_entry_steps": row["cycle_entry_steps"],
        "seed_prefix_40": seed["prefix_40"],
        "seed_suffix_40": seed["suffix_40"],
        "seed_sha256": seed["sha256"],
    }


def run() -> dict[str, object]:
    boundary = boundary_campaign()
    random_large = random_campaign()
    inverse_derived = inverse_campaign()
    weak_runs = weak_run_campaign()

    boundary_worst = boundary["worst_cycle_entry"]
    boundary_descent = boundary["longest_first_descent"]
    boundary_valuation = boundary["largest_valuation"]
    boundary_r1 = boundary["longest_consecutive_r1"]

    random_worst = random_large["worst_cycle_entry"]
    random_descent = random_large["longest_first_descent"]

    inverse_worst = inverse_derived["worst_cycle_entry"]
    inverse_descent = inverse_derived["longest_first_descent"]
    inverse_r1 = inverse_derived["longest_consecutive_r1"]

    weak_cases: list[dict[str, object]] = []
    for case in weak_runs["cases"]:
        seed = case["seed"]
        peak = case["max_excursion"]
        if not isinstance(seed, dict) or not isinstance(peak, dict):
            raise AssertionError("engineered red-team case should be a large integer")
        weak_cases.append(
            {
                "requested_r1_run": case["requested_r1_run"],
                "decimal_scale": case["decimal_scale"],
                "observed_initial_r1_run": case["observed_initial_r1_run"],
                "cycle_entry_steps": case["cycle_entry_steps"],
                "first_descent_steps": case["first_descent_steps"],
                "max_excursion_decimal_digits": peak["decimal_digits"],
                "seed": seed,
            }
        )

    return {
        "schema_version": 1,
        "date": "2026-09-26",
        "claim_type": (
            "ELEMENTARY_THEOREM_PLUS_FINITE_EXACT_FALSIFICATION_CAMPAIGN"
        ),
        "purpose": (
            "Final declared Stage-1 adversarial stress test; "
            "not a proof of universal convergence."
        ),
        "theorem_level_result": {
            "unbounded_single_valuation_family": {
                "statement": (
                    "For every k>=0, n=2*10^k-1 has leading digit 1 and "
                    "3n+2L(n)+1=6*10^k=3*2^(k+1)*5^k. Hence its odd-branch "
                    "valuation is exactly k+1 and its accelerated successor "
                    "is 3*5^k."
                ),
                "consequence": "Odd-branch valuation bursts are unbounded.",
            }
        },
        "finite_exact_campaigns": {
            "decimal_boundary_adversaries": {
                "protocol": boundary["protocol"],
                "tested_seed_count": boundary["tested_seed_count"],
                "seed_set_sha256": boundary["seed_set_sha256"],
                "all_entered_distinguished_cycle": (
                    boundary["all_entered_distinguished_cycle"]
                ),
                "competing_cycle_found": False,
                "step_cap_hit": False,
                "records": {
                    "worst_cycle_entry": {
                        "seed_form": _seed_form(boundary_worst),
                        "cycle_entry_steps": boundary_worst["cycle_entry_steps"],
                    },
                    "longest_first_descent": {
                        "seed_form": _seed_form(boundary_descent),
                        "first_descent_steps": boundary_descent["first_descent_steps"],
                        "cycle_entry_steps": boundary_descent["cycle_entry_steps"],
                    },
                    "largest_valuation": {
                        "seed_form": _seed_form(boundary_valuation),
                        "valuation": boundary_valuation["max_odd_branch_valuation"],
                        "cycle_entry_steps": boundary_valuation["cycle_entry_steps"],
                    },
                    "longest_consecutive_r1": {
                        "seed_form": _seed_form(boundary_r1),
                        "run_length": boundary_r1["max_consecutive_r1"],
                        "cycle_entry_steps": boundary_r1["cycle_entry_steps"],
                    },
                },
            },
            "deterministic_large_random_odds": {
                "protocol": random_large["protocol"],
                "tested_seed_count": random_large["tested_seed_count"],
                "seed_set_sha256": random_large["seed_set_sha256"],
                "all_entered_distinguished_cycle": (
                    random_large["all_entered_distinguished_cycle"]
                ),
                "competing_cycle_found": False,
                "step_cap_hit": False,
                "records": {
                    "worst_cycle_entry": _compact_random_record(random_worst),
                    "longest_first_descent": {
                        **_compact_random_record(random_descent),
                        "first_descent_steps": random_descent["first_descent_steps"],
                    },
                    "largest_observed_valuation": (
                        random_large["largest_valuation"][
                            "max_odd_branch_valuation"
                        ]
                    ),
                    "longest_consecutive_r1": (
                        random_large["longest_consecutive_r1"][
                            "max_consecutive_r1"
                        ]
                    ),
                },
            },
            "inverse_tree_derived_adversaries": {
                "protocol": inverse_derived["protocol"],
                "tested_seed_count": inverse_derived["tested_seed_count"],
                "seed_set_sha256": inverse_derived["seed_set_sha256"],
                "all_entered_distinguished_cycle": (
                    inverse_derived["all_entered_distinguished_cycle"]
                ),
                "competing_cycle_found": False,
                "step_cap_hit": False,
                "records": {
                    "worst_cycle_entry": {
                        "source": inverse_worst["source"],
                        "requested_offset": inverse_worst["offset"],
                        "seed": inverse_worst["seed"],
                        "cycle_entry_steps": inverse_worst["cycle_entry_steps"],
                    },
                    "longest_first_descent": {
                        "source": inverse_descent["source"],
                        "requested_offset": inverse_descent["offset"],
                        "seed": inverse_descent["seed"],
                        "first_descent_steps": inverse_descent["first_descent_steps"],
                        "cycle_entry_steps": inverse_descent["cycle_entry_steps"],
                    },
                    "longest_consecutive_r1": {
                        "source": inverse_r1["source"],
                        "requested_offset": inverse_r1["offset"],
                        "seed": inverse_r1["seed"],
                        "run_length": inverse_r1["max_consecutive_r1"],
                        "cycle_entry_steps": inverse_r1["cycle_entry_steps"],
                    },
                    "largest_observed_valuation": (
                        inverse_derived["largest_valuation"][
                            "max_odd_branch_valuation"
                        ]
                    ),
                },
            },
            "engineered_long_r1_runs": {
                "protocol": weak_runs["protocol"],
                "all_entered_distinguished_cycle": (
                    weak_runs["all_entered_distinguished_cycle"]
                ),
                "cases": weak_cases,
            },
        },
        "campaign_outcome": {
            "all_tested_seeds_entered_distinguished_cycle": all(
                campaign["all_entered_distinguished_cycle"]
                for campaign in (
                    boundary,
                    random_large,
                    inverse_derived,
                    weak_runs,
                )
            ),
            "competing_cycle_found": False,
            "step_cap_hit": False,
            "apparent_escape_found": False,
            "structural_contradiction_found": False,
            "conjecture_wording_change_required": False,
        },
        "limitations": (
            "Every convergence statement in this certificate is finite exact "
            "computation over the declared protocol. None proves the central "
            "conjecture."
        ),
    }

def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
