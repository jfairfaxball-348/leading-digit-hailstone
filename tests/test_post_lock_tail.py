from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.post_lock_tail import (
    MINIMUM_ODD_STATE,
    TAIL_COUNTEREXAMPLE,
    direct_rise_profile,
    lock_and_follow,
    next_record_certificate,
    run,
)


class PostLockTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(Path("data/post_lock_tail.json").read_text())
        self.assertEqual(self.payload, recorded)

    def test_known_tail_six_falsifies_constant_five_bound(self) -> None:
        profile = direct_rise_profile(TAIL_COUNTEREXAMPLE)
        depth = TAIL_COUNTEREXAMPLE.bit_length() - 1
        self.assertEqual(depth, 65)
        self.assertEqual(profile["total_exact_r1_rises"], 71)
        self.assertEqual(profile["total_exact_r1_rises"] - depth, 6)
        self.assertEqual(profile["next_valuation"], 7)

    def test_largest_previous_range_collapses_to_direct_following(self) -> None:
        certificate = lock_and_follow(
            MINIMUM_ODD_STATE,
            42_285_421_502_900,
        )
        self.assertEqual(certificate["lock_depth"], 45)
        self.assertEqual(
            [row["start"] for row in certificate["locked_candidates"]],
            [26_501_219_601_103, 39_751_829_401_657],
        )
        self.assertEqual(
            [
                row["post_lock_zero_lift_tail"]
                for row in certificate["locked_candidates"]
            ],
            [3, 2],
        )
        self.assertEqual(certificate["first_impossible_rise_length"], 49)

    def test_next_record_uses_same_two_locked_starts(self) -> None:
        certificate = next_record_certificate()
        self.assertEqual(
            certificate["record"]["maximum_minimum_state"],
            48_737_068_628_469,
        )
        locked = certificate["lock_and_follow"]["locked_candidates"]
        self.assertEqual(
            [row["start"] for row in locked],
            [26_501_219_601_103, 39_751_829_401_657],
        )
        self.assertEqual(
            [row["total_exact_r1_rises"] for row in locked],
            [48, 47],
        )
        self.assertEqual(
            certificate["structured_q_excluded_through"],
            1_643_749_725_073,
        )
        self.assertEqual(
            certificate["remaining_minimum_rise"],
            682_217_775_335,
        )


if __name__ == "__main__":
    unittest.main()
