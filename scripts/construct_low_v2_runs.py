from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, analyze, leading_digit

ALPHA = Fraction(7, 3)


def leading_digit_fraction(x: Fraction) -> int:
    if x < 1:
        raise ValueError("this constructor expects x >= 1")
    integer_part = x.numerator // x.denominator
    power = 10 ** (len(str(integer_part)) - 1)
    return x.numerator // (x.denominator * power)


def homogeneous_digit_word(length: int) -> list[int]:
    x = ALPHA
    out: list[int] = []
    for _ in range(length):
        out.append(leading_digit_fraction(x))
        x *= Fraction(3, 2)
    return out


def fixed_word_has_run(seed: int, digits: list[int]) -> bool:
    x = seed
    for d in digits:
        y = 3 * x + 2 * d + 1
        if y % 4 != 2:
            return False
        x = y // 2
    return True


def forced_residue(digits: list[int]) -> tuple[int, int]:
    residue = 1
    modulus = 2
    for depth in range(len(digits)):
        candidates = (residue, residue + modulus)
        good = [
            candidate
            for candidate in candidates
            if fixed_word_has_run(candidate, digits[: depth + 1])
        ]
        if len(good) != 1:
            raise AssertionError((depth, candidates, good))
        residue = good[0]
        modulus *= 2
    return residue, modulus


def initial_v2_one_run(seed: int, cap: int) -> int:
    x = seed
    run = 0
    for _ in range(cap):
        nxt, valuation = accelerated_odd_step(x)
        if valuation != 1:
            break
        run += 1
        x = nxt
    return run


def construct(length: int, decimal_scale: int) -> dict:
    digits = homogeneous_digit_word(length)
    residue, modulus = forced_residue(digits)
    target = (ALPHA.numerator * 10**decimal_scale) // ALPHA.denominator
    seed = target + ((residue - target) % modulus)

    actual_digits: list[int] = []
    x = seed
    for _ in range(length):
        actual_digits.append(leading_digit(x))
        nxt, valuation = accelerated_odd_step(x)
        if valuation != 1:
            raise AssertionError("constructed run terminated too early")
        x = nxt

    if actual_digits != digits:
        raise AssertionError("leading-digit word was not preserved")

    run = initial_v2_one_run(seed, length + 20)
    result = analyze(seed, max_steps=200_000)
    return {
        "requested_run_length": length,
        "decimal_scale": decimal_scale,
        "seed": str(seed),
        "seed_decimal_digits": len(str(seed)),
        "forced_residue_modulus": str(modulus),
        "initial_v2_one_run_length_observed": run,
        "trajectory_status": result.status,
        "cycle_entry_steps": result.cycle_entry_time,
        "peak": str(result.max_excursion),
        "peak_decimal_digits": len(str(result.max_excursion)),
    }


def run() -> dict:
    cases = [(30, 60), (50, 110), (100, 230)]
    return {
        "schema_version": 1,
        "evidence_type": "FINITE_COMPUTATION_SUPPORTING_AN_ELEMENTARY_CONSTRUCTION",
        "construction": "bit-lift unique residue modulo 2^(m+1) for a fixed safe leading-digit word from alpha=7/3",
        "examples": [construct(length, scale) for length, scale in cases],
    }


def main() -> None:
    payload = run()
    out = Path("data/constructed_low_v2_runs.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
