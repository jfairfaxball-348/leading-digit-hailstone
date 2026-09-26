"""Independent verification implementation.

This module intentionally does not call core.leading_digit or core.step.
It uses a different leading-digit method to cross-check the frozen rule.
"""
from __future__ import annotations

import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

VERIFY_CYCLE = frozenset({1, 2, 3, 4, 6, 8, 16})


def leading_digit_independent(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")
    return ord(str(n)[0]) - ord("0")


def step_independent(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")
    return n >> 1 if (n & 1) == 0 else n * 3 + leading_digit_independent(n) * 2 + 1


def cycle_entry_time_independent(seed: int, cap: int = 100_000) -> int | None:
    x = seed
    seen: set[int] = set()
    for k in range(cap + 1):
        if x in VERIFY_CYCLE:
            return k
        if x in seen:
            return None
        seen.add(x)
        x = step_independent(x)
    return None
