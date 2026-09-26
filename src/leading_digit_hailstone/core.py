from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Iterable, Optional

DISTINGUISHED_CYCLE = (1, 6, 3, 16, 8, 4, 2)
DISTINGUISHED_CYCLE_SET = frozenset(DISTINGUISHED_CYCLE)


def _require_positive_int(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")


def leading_digit(n: int) -> int:
    """Return the leading base-10 digit of a positive integer exactly.

    This arithmetic implementation avoids dependence on Python's integer-to-string
    digit safety limit and therefore works for arbitrary-size Python integers.
    """
    _require_positive_int(n)
    p = 1
    while n >= 10 * p:
        p *= 10
    return n // p


def step(n: int) -> int:
    """Apply the frozen Leading-Digit Hailstone map T once."""
    _require_positive_int(n)
    if n % 2 == 0:
        return n // 2
    return 3 * n + 2 * leading_digit(n) + 1


def v2(n: int) -> int:
    """Return the exponent of 2 dividing a positive integer."""
    _require_positive_int(n)
    return (n & -n).bit_length() - 1


def accelerated_odd_step(n: int) -> tuple[int, int]:
    """For odd n, apply the odd branch then divide out the full power of 2.

    Returns (next_odd, valuation), where valuation = v2(3n + 2L(n) + 1).
    """
    _require_positive_int(n)
    if n % 2 == 0:
        raise ValueError("accelerated_odd_step requires an odd input")
    m = 3 * n + 2 * leading_digit(n) + 1
    valuation = v2(m)
    return m >> valuation, valuation


def canonical_cycle(cycle: Iterable[int]) -> tuple[int, ...]:
    values = tuple(cycle)
    if not values:
        return ()
    rotations = [values[i:] + values[:i] for i in range(len(values))]
    return min(rotations)


@dataclass(frozen=True)
class TrajectoryResult:
    seed: int
    status: str
    cycle_entry_time: Optional[int]
    cycle_entry_value: Optional[int]
    stopping_time: Optional[int]
    max_excursion: int
    excursion_ratio_numerator: int
    excursion_ratio_denominator: int
    detected_cycle: tuple[int, ...]
    steps_examined: int

    def as_dict(self) -> dict:
        out = asdict(self)
        out["detected_cycle"] = list(self.detected_cycle)
        return out


def analyze(seed: int, max_steps: Optional[int] = None) -> TrajectoryResult:
    """Analyze one exact trajectory.

    Definitions used by this repository:
      * stopping_time: first k >= 1 with T^k(seed) < seed;
      * cycle_entry_time: first k >= 0 with T^k(seed) in the distinguished cycle;
      * max_excursion: max T^j(seed) up to first distinguished-cycle entry,
        or over the examined prefix if another cycle/cap is reached.
    """
    _require_positive_int(seed)
    if max_steps is not None and max_steps < 0:
        raise ValueError("max_steps must be nonnegative or None")

    x = seed
    peak = seed
    stopping_time: Optional[int] = None
    seen: dict[int, int] = {}
    k = 0

    while True:
        if x in DISTINGUISHED_CYCLE_SET:
            ratio = Fraction(peak, seed)
            return TrajectoryResult(
                seed=seed,
                status="DISTINGUISHED_CYCLE",
                cycle_entry_time=k,
                cycle_entry_value=x,
                stopping_time=stopping_time,
                max_excursion=peak,
                excursion_ratio_numerator=ratio.numerator,
                excursion_ratio_denominator=ratio.denominator,
                detected_cycle=(),
                steps_examined=k,
            )

        if x in seen:
            start = seen[x]
            ordered = tuple(list(seen.keys())[start:])
            ratio = Fraction(peak, seed)
            return TrajectoryResult(
                seed=seed,
                status="OTHER_CYCLE",
                cycle_entry_time=None,
                cycle_entry_value=None,
                stopping_time=stopping_time,
                max_excursion=peak,
                excursion_ratio_numerator=ratio.numerator,
                excursion_ratio_denominator=ratio.denominator,
                detected_cycle=canonical_cycle(ordered),
                steps_examined=k,
            )

        if max_steps is not None and k >= max_steps:
            ratio = Fraction(peak, seed)
            return TrajectoryResult(
                seed=seed,
                status="STEP_CAP",
                cycle_entry_time=None,
                cycle_entry_value=None,
                stopping_time=stopping_time,
                max_excursion=peak,
                excursion_ratio_numerator=ratio.numerator,
                excursion_ratio_denominator=ratio.denominator,
                detected_cycle=(),
                steps_examined=k,
            )

        seen[x] = k
        x = step(x)
        k += 1
        peak = max(peak, x)
        if stopping_time is None and x < seed:
            stopping_time = k


def inverse_preimages(m: int) -> tuple[int, ...]:
    """Return all one-step positive preimages under the frozen map."""
    _require_positive_int(m)
    candidates = {2 * m}
    if m % 2 == 0:
        for d in range(1, 10):
            numerator = m - 2 * d - 1
            if numerator <= 0 or numerator % 3:
                continue
            n = numerator // 3
            if n % 2 == 1 and leading_digit(n) == d and step(n) == m:
                candidates.add(n)
    return tuple(sorted(candidates))
