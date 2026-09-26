from __future__ import annotations

import argparse
import json
import math
import random
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

CYCLE = frozenset({1, 2, 3, 4, 6, 8, 16})
RANDOM_SEED = 20_260_926
INVERSE_SEED = 20_260_927


def leading_digit_independent(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    return ord(str(n)[0]) - 48


def step_independent(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    return n // 2 if n % 2 == 0 else 3 * n + 2 * leading_digit_independent(n) + 1


def accelerated_step_independent(n: int) -> tuple[int, int]:
    if n <= 0 or n % 2 == 0:
        raise ValueError("accelerated step requires positive odd input")
    y = 3 * n + 2 * leading_digit_independent(n) + 1
    r = (y & -y).bit_length() - 1
    return y >> r, r


def compact(n: int) -> str | dict[str, object]:
    s = str(n)
    if len(s) <= 88:
        return s
    return {"decimal_digits": len(s), "prefix": s[:40], "suffix": s[-40:]}


def analyze_independent(seed: int, cap: int = 200_000, detailed: bool = False) -> dict[str, object]:
    x = seed
    peak = seed
    seen: set[int] = set()
    first_descent = None
    r1 = max_r1 = growth = max_growth = max_v = 0
    for k in range(cap + 1):
        if x in CYCLE:
            return {"status": "DISTINGUISHED_CYCLE", "cycle_entry_steps": k,
                    "first_descent_steps": first_descent, "peak": peak,
                    "maximum_consecutive_r1": max_r1,
                    "maximum_accelerated_valuation": max_v,
                    "maximum_monotone_accelerated_growth_block": max_growth}
        if x in seen:
            return {"status": "OTHER_CYCLE", "cycle_entry_steps": None,
                    "first_descent_steps": first_descent, "peak": peak,
                    "maximum_consecutive_r1": max_r1,
                    "maximum_accelerated_valuation": max_v,
                    "maximum_monotone_accelerated_growth_block": max_growth}
        if k == cap:
            return {"status": "STEP_CAP", "cycle_entry_steps": None,
                    "first_descent_steps": first_descent, "peak": peak,
                    "maximum_consecutive_r1": max_r1,
                    "maximum_accelerated_valuation": max_v,
                    "maximum_monotone_accelerated_growth_block": max_growth}
        seen.add(x)
        if detailed and x % 2:
            y = 3 * x + 2 * leading_digit_independent(x) + 1
            v = (y & -y).bit_length() - 1
            z = y >> v
            max_v = max(max_v, v)
            r1 = r1 + 1 if v == 1 else 0
            growth = growth + 1 if z > x else 0
            max_r1 = max(max_r1, r1)
            max_growth = max(max_growth, growth)
        x = step_independent(x)
        peak = max(peak, x)
        if first_descent is None and x < seed:
            first_descent = k + 1
    raise AssertionError("unreachable")


def _row(digits: int, seed: int, result: dict[str, object]) -> dict[str, object]:
    return {"decimal_digits": digits, "seed": compact(seed), "status": result["status"],
            "cycle_entry_steps": result["cycle_entry_steps"],
            "first_descent_steps": result["first_descent_steps"],
            "peak": compact(int(result["peak"])), "peak_decimal_digits": len(str(result["peak"])),
            "maximum_consecutive_r1": result["maximum_consecutive_r1"],
            "maximum_accelerated_valuation": result["maximum_accelerated_valuation"],
            "maximum_monotone_accelerated_growth_block": result["maximum_monotone_accelerated_growth_block"]}


def random_large_start_stress() -> dict[str, object]:
    rng = random.Random(RANDOM_SEED)
    rows = []
    for digits in (20, 50, 100, 250, 500, 1000):
        for _ in range(50):
            seed = int(str(rng.randrange(1, 10)) +
                       "".join(str(rng.randrange(10)) for _ in range(digits - 2)) +
                       str(rng.choice((1, 3, 5, 7, 9))))
            rows.append((digits, seed, analyze_independent(seed, detailed=True)))
    failures = [r for r in rows if r[2]["status"] != "DISTINGUISHED_CYCLE"]
    return {"protocol": "50 deterministic random odd starts at each of 20,50,100,250,500,1000 decimal digits",
            "rng_seed": RANDOM_SEED, "step_cap": 200_000, "tested_seed_count": len(rows),
            "failure_count": len(failures), "all_entered_distinguished_cycle": not failures,
            "worst_cycle_entry": _row(*max(rows, key=lambda r: int(r[2]["cycle_entry_steps"] or -1))),
            "worst_first_descent": _row(*max(rows, key=lambda r: int(r[2]["first_descent_steps"] or -1))),
            "largest_consecutive_r1_case": _row(*max(rows, key=lambda r: int(r[2]["maximum_consecutive_r1"]))),
            "largest_accelerated_valuation_case": _row(*max(rows, key=lambda r: int(r[2]["maximum_accelerated_valuation"])))}


def decimal_boundary_stress() -> dict[str, object]:
    cases = []
    for k in (600, 1000, 1500):
        cases += [(k, d, c) for d in range(1, 10) for c in (-1, 1)]
        cases += [(k, d, c) for d in (1, 5, 9) for c in (-99, -9, 9, 99)]
    rows = []
    for k, d, c in cases:
        result = analyze_independent(d * 10**k + c, cap=100_000)
        rows.append((k, d, c, result))
    failures = [r for r in rows if r[3]["status"] != "DISTINGUISHED_CYCLE"]
    def fmt(r):
        k, d, c, x = r
        return {"seed_form": f"{d}*10^{k}{c:+d}", "status": x["status"],
                "cycle_entry_steps": x["cycle_entry_steps"], "first_descent_steps": x["first_descent_steps"],
                "peak": compact(int(x["peak"])), "peak_decimal_digits": len(str(x["peak"]))}
    return {"protocol": "k in {600,1000,1500}; all d=1..9 at offsets +/-1; d in {1,5,9} also at +/-9,+/-99",
            "step_cap": 100_000, "tested_seed_count": len(rows), "failure_count": len(failures),
            "all_entered_distinguished_cycle": not failures,
            "worst_cycle_entry": fmt(max(rows, key=lambda r: int(r[3]["cycle_entry_steps"] or -1))),
            "largest_peak_decimal_digits_case": fmt(max(rows, key=lambda r: len(str(r[3]["peak"]))))}


def homogeneous_digit_word(length: int) -> list[int]:
    p, q, out = 7, 3, []
    for _ in range(length):
        out.append(leading_digit_independent(p // q))
        p, q = 3 * p, 2 * q
        g = math.gcd(p, q)
        p, q = p // g, q // g
    return out


def forced_residue(digits: list[int]) -> tuple[int, int]:
    a = 0
    for i, d in enumerate(digits):
        a = 3 * a + (2 * d + 1) * (1 << i)
    m = len(digits)
    modulus = 1 << (m + 1)
    return (pow(pow(3, m, modulus), -1, modulus) * ((1 << m) - a)) % modulus, modulus


def construct_long_r1_case(requested_run: int, decimal_scale: int) -> dict[str, object]:
    digits = homogeneous_digit_word(requested_run)
    residue, modulus = forced_residue(digits)
    target = 7 * 10**decimal_scale // 3
    seed = target + ((residue - target) % modulus)
    x, observed, terminating = seed, 0, None
    actual = []
    for _ in range(requested_run + 200):
        actual.append(leading_digit_independent(x))
        x, v = accelerated_step_independent(x)
        if v != 1:
            terminating = v
            break
        observed += 1
    if actual[:requested_run] != digits or observed < requested_run:
        raise AssertionError("construction failed")
    result = analyze_independent(seed)
    return {"requested_run_length": requested_run, "decimal_scale": decimal_scale,
            "seed": compact(seed), "seed_decimal_digits": len(str(seed)),
            "observed_initial_r1_run": observed, "terminating_valuation": terminating,
            "status": result["status"], "cycle_entry_steps": result["cycle_entry_steps"],
            "peak": compact(int(result["peak"])), "peak_decimal_digits": len(str(result["peak"]))}


def long_r1_stress() -> dict[str, object]:
    rows = [construct_long_r1_case(*x) for x in ((150, 350), (200, 470), (256, 610), (384, 920))]
    return {"construction": "phase 7/3 homogeneous word plus unique residue modulo 2^(m+1)",
            "cases": rows, "all_entered_distinguished_cycle": all(r["status"] == "DISTINGUISHED_CYCLE" for r in rows)}


def inverse_preimages_independent(m: int) -> tuple[int, ...]:
    out = {2 * m}
    if m % 2 == 0:
        for d in range(1, 10):
            z = m - 2 * d - 1
            if z > 0 and z % 3 == 0:
                n = z // 3
                if n % 2 and leading_digit_independent(n) == d and step_independent(n) == m:
                    out.add(n)
    return tuple(sorted(out))


def inverse_tree_stress() -> dict[str, object]:
    seen, frontier = set(CYCLE), set(CYCLE)
    for _ in range(20):
        nxt = set()
        for m in frontier:
            for n in inverse_preimages_independent(m):
                if n not in seen:
                    seen.add(n); nxt.add(n)
        frontier = nxt
    odd = [x for x in seen if x % 2]
    missing = [r for r in range(1, 128, 2) if r not in {x % 128 for x in odd}]
    rng, rows = random.Random(INVERSE_SEED), []
    for digits in (50, 100, 250):
        lo = 10 ** (digits - 1)
        for residue in missing:
            base = lo + rng.randrange(9 * lo)
            seed = base + ((residue - base) % 128)
            rows.append((digits, residue, seed, analyze_independent(seed, cap=100_000)))
    failures = [r for r in rows if r[3]["status"] != "DISTINGUISHED_CYCLE"]
    worst = max(rows, key=lambda r: int(r[3]["cycle_entry_steps"] or -1))
    return {"backward_depth": 20, "unique_nodes_through_depth": len(seen), "odd_nodes_through_depth": len(odd),
            "missing_odd_residues_mod_128": missing, "hostile_seed_count": len(rows),
            "hostile_failure_count": len(failures), "all_hostile_seeds_entered_distinguished_cycle": not failures,
            "hostile_worst_cycle_entry": {"decimal_digits": worst[0], "residue_mod_128": worst[1],
                "seed": compact(worst[2]), "cycle_entry_steps": worst[3]["cycle_entry_steps"],
                "peak": compact(int(worst[3]["peak"])), "peak_decimal_digits": len(str(worst[3]["peak"]))}}


def _phase_word(p: int, q: int, length: int) -> list[int]:
    out = []
    for _ in range(length):
        out.append(leading_digit_independent(p // q))
        p, q = 3 * p, 2 * q
        g = math.gcd(p, q)
        p, q = p // g, q // g
    return out


def _prefix_realized(seed: int, digits: list[int]) -> bool:
    x = seed
    for d in digits:
        if leading_digit_independent(x) != d:
            return False
        x, v = accelerated_step_independent(x)
        if v != 1:
            return False
    return True


def phase_tail_search(grid_start: int = 1000, grid_stop: int = 6000,
                      random_phase_count: int = 1000, maximum_prefix: int = 256) -> dict[str, object]:
    phases = [(p, 1000) for p in range(grid_start, grid_stop)]
    rng = random.Random(RANDOM_SEED)
    phases += [(rng.randrange(10**9, 10**10), 10**9) for _ in range(random_phase_count)]
    best_tail, best = -1, None
    for p, q in phases:
        digits, a = _phase_word(p, q, maximum_prefix), 0
        for m, d in enumerate(digits, 1):
            a = 3 * a + (2 * d + 1) * (1 << (m - 1))
            if m < 20:
                continue
            modulus = 1 << (m + 1)
            rho = (pow(pow(3, m, modulus), -1, modulus) * ((1 << m) - a)) % modulus
            if rho <= 0 or rho % 2 == 0:
                continue
            B = rho.bit_length() - 1
            if m - B <= best_tail or not _prefix_realized(rho, digits[:m]):
                continue
            x, run, terminating = rho, 0, None
            for _ in range(m + 200):
                x, v = accelerated_step_independent(x)
                if v != 1:
                    terminating = v; break
                run += 1
            tail = run - B
            if tail > best_tail:
                best_tail = tail
                best = {"phase_numerator": p, "phase_denominator": q, "certified_prefix_length": m,
                        "start": str(rho), "bit_length_lock_depth": B, "total_initial_r1_run": run,
                        "post_lock_tail": tail, "terminating_valuation": terminating}
    return {"claim_type": "FINITE_EXACT_PHASE_RESIDUE_SEARCH", "phase_count": len(phases),
            "maximum_prefix_length": maximum_prefix, "grid_numerators": [grid_start, grid_stop - 1],
            "grid_denominator": 1000, "random_phase_count": random_phase_count, "rng_seed": RANDOM_SEED,
            "maximum_observed_post_lock_tail": best_tail, "record": best,
            "found_tail_longer_than_six": best_tail > 6}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("section", choices=("random", "boundary", "long", "inverse", "phase"))
    args = parser.parse_args()
    functions = {"random": random_large_start_stress, "boundary": decimal_boundary_stress,
                 "long": long_r1_stress, "inverse": inverse_tree_stress, "phase": phase_tail_search}
    print(json.dumps(functions[args.section](), indent=2))


if __name__ == "__main__":
    main()
