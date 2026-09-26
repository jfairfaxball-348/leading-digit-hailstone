import random
import unittest

from leading_digit_hailstone.core import (
    DISTINGUISHED_CYCLE,
    accelerated_odd_step,
    analyze,
    inverse_preimages,
    leading_digit,
    step,
    v2,
)
from leading_digit_hailstone.verify import step_independent


class CoreTests(unittest.TestCase):
    def test_distinguished_cycle_edges(self):
        expected = (6, 3, 16, 8, 4, 2, 1)
        self.assertEqual(tuple(step(n) for n in DISTINGUISHED_CYCLE), expected)

    def test_leading_digit(self):
        cases = {1: 1, 9: 9, 10: 1, 99: 9, 100: 1, 508701: 5, 10**200 + 7: 1}
        for n, d in cases.items():
            self.assertEqual(leading_digit(n), d)

    def test_odd_branch_is_even(self):
        for n in range(1, 5000, 2):
            self.assertEqual(step(n) % 2, 0)

    def test_accelerated_odd_step(self):
        for n in range(1, 1000, 2):
            m = step(n)
            y, valuation = accelerated_odd_step(n)
            self.assertEqual(valuation, v2(m))
            self.assertEqual(y, m >> valuation)
            self.assertEqual(y % 2, 1)

    def test_known_incoming_records(self):
        a = analyze(917173, max_steps=10_000)
        self.assertEqual(a.cycle_entry_time, 584)
        b = analyze(508701, max_steps=10_000)
        self.assertEqual(b.max_excursion, 133635233424)
        self.assertEqual(b.cycle_entry_time, 508)

    def test_independent_step_agreement(self):
        rng = random.Random(20260926)
        seeds = list(range(1, 5000))
        seeds.extend(rng.randrange(1, 10**80) for _ in range(500))
        for n in seeds:
            self.assertEqual(step(n), step_independent(n))

    def test_inverse_preimages(self):
        for m in range(1, 1000):
            for n in inverse_preimages(m):
                self.assertEqual(step(n), m)
            self.assertIn(2 * m, inverse_preimages(m))

    def test_single_digit_odd_branch_matches_5x_plus_1(self):
        for n in (1, 3, 5, 7, 9):
            self.assertEqual(step(n), 5 * n + 1)

    def test_decimal_boundary_jumps(self):
        for k in range(1, 7):
            power = 10 ** k
            self.assertEqual(step(power + 1) - step(power - 1), -10)
            for d in range(2, 10):
                boundary = d * power
                self.assertEqual(step(boundary + 1) - step(boundary - 1), 8)

    def test_odd_preimage_exception(self):
        for m in range(1, 100_001):
            odd = [n for n in inverse_preimages(m) if n % 2 == 1]
            if m == 36:
                self.assertEqual(odd, [7, 11])
            else:
                self.assertLessEqual(len(odd), 1)


if __name__ == "__main__":
    unittest.main()
