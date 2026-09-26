from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.post_lock_terminal_guide import (
    KNOWN_TAIL_SIX_LENGTH,
    KNOWN_TAIL_SIX_LOCK_STATE,
    run,
    terminal_guide_profile,
)


class PostLockTerminalGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(Path("data/post_lock_terminal_guide.json").read_text())
        self.assertEqual(self.payload, recorded)

    def test_known_tail_six_uniform_absolute_gap(self) -> None:
        profile = terminal_guide_profile(
            KNOWN_TAIL_SIX_LOCK_STATE,
            KNOWN_TAIL_SIX_LENGTH,
        )
        maximum_gap = Fraction(
            profile["maximum_gap_numerator"],
            profile["maximum_gap_denominator"],
        )
        self.assertEqual(maximum_gap, Fraction(235, 27))
        self.assertLess(maximum_gap, 19)
        self.assertEqual(profile["leading_digit_mismatch_depths"], [])

    def test_known_tail_six_guide_digit_word(self) -> None:
        diagnostic = self.payload["finite_exact_diagnostic"]
        self.assertEqual(diagnostic["actual_digits"], [1, 1, 2, 4, 6, 9, 1])
        self.assertEqual(diagnostic["guide_digits"], [1, 1, 2, 4, 6, 9, 1])
        self.assertEqual(diagnostic["next_valuation"], 7)


if __name__ == "__main__":
    unittest.main()
