from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.post_lock_scale_geometry import (
    homogeneous_leading_digit,
    own_bit_interval,
    run,
    scaled_boundary_hits,
)


class PostLockScaleGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(Path("data/post_lock_scale_geometry.json").read_text())
        self.assertEqual(self.payload, recorded)

    def test_complete_own_bit_scan_through_220(self) -> None:
        scan = self.payload["finite_exact_bit_depth_scan"]
        self.assertEqual(scan["bit_depth_range"], [1, 220])
        self.assertEqual(scan["own_bit_locked_candidate_count"], 96)
        self.assertEqual(scan["positive_tail_candidate_count"], 41)
        self.assertEqual(
            scan["tail_histogram"],
            {"0": 55, "1": 16, "2": 13, "3": 7, "4": 1, "5": 3, "6": 1},
        )
        self.assertEqual(scan["maximum_post_lock_tail"], 6)

    def test_positive_scanned_tails_have_no_boundary_ambiguity(self) -> None:
        scan = self.payload["finite_exact_bit_depth_scan"]
        self.assertEqual(scan["positive_tail_boundary_hit_candidate_count"], 0)
        self.assertEqual(
            scan["positive_tail_homogeneous_digit_mismatch_candidate_count"],
            0,
        )

    def test_known_tail_six_has_frozen_homogeneous_digits(self) -> None:
        lock_state = 12_166_406_006_866_046_930_622_304_922_581
        self.assertEqual(
            [homogeneous_leading_digit(lock_state, step) for step in range(1, 7)],
            [1, 2, 4, 6, 9, 1],
        )
        self.assertEqual(
            [scaled_boundary_hits(lock_state, step) for step in range(1, 7)],
            [[], [], [], [], [], []],
        )

    def test_own_bit_interval_is_exact(self) -> None:
        self.assertEqual(
            own_bit_interval(44),
            (17_592_186_044_417, 35_184_372_088_831),
        )


if __name__ == "__main__":
    unittest.main()
