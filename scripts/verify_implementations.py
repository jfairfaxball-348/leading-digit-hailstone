#!/usr/bin/env python3
from __future__ import annotations

import random

from leading_digit_hailstone.core import step
from leading_digit_hailstone.verify import step_independent


def main() -> None:
    rng = random.Random(20260926)
    checked = 0
    for n in range(1, 100_001):
        assert step(n) == step_independent(n)
        checked += 1
    for _ in range(10_000):
        digits = rng.randint(1, 500)
        n = int(str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(digits - 1)))
        assert step(n) == step_independent(n)
        checked += 1
    print(f"independent implementations agree on {checked} tested inputs")


if __name__ == "__main__":
    main()
