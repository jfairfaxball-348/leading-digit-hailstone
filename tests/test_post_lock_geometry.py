from __future__ import annotations

import json
import unittest
from fractions import Fraction
from pathlib import Path

from scripts.post_lock_geometry import (
    bit_length_scan,
    finite_horizon_guide,
    locked_candidates_for_bit_length,
    run,
)


class PostLockGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(Path("data/post_lock_geometry.json").read_text())
        self.assertEqual(self.payload, recorded)

    def test_terminally_anchored_guide_stays_within_nineteen(self) -> None:
        guide = finite_horizon_guide(43_574_304_770_317_398_119, 71)
        self.assertTrue(guide["maximum_gap_less_than_19"])
        maximum_gap = Fraction(
            guide["maximum_gap_numerator"],
            guide["maximum_gap_denominator"],
        )
        self.assertGreaterEqual(maximum_gap, 0)
        self.assertLess(maximum_gap, 19)
        self.assertEqual(guide["leading_digit_mismatch_depths"], [])

    def test_tail_six_is_exact_bit_length_record_through_100(self) -> None:
        scan = bit_length_scan(100)
        self.assertEqual(scan["maximum_post_lock_tail"], 6)
        self.assertEqual(
            [
                (row["bit_length"], row["post_lock_tail"])
                for row in scan["record_tails"]
            ],
            [(2, 0), (33, 1), (44, 4), (65, 6)],
        )
        self.assertEqual(
            scan["record_tails"][-1]["start"],
            43_574_304_770_317_398_119,
        )

    def test_bit_length_65_candidates_are_exact(self) -> None:
        rows = locked_candidates_for_bit_length(65)
        self.assertEqual(
            [row["start"] for row in rows],
            [
                41_866_706_037_776_625_767,
                43_574_304_770_317_398_119,
                65_361_457_155_476_097_183,
            ],
        )
        self.assertEqual([row["post_lock_tail"] for row in rows], [0, 6, 5])
        self.assertEqual([row["next_valuation"] for row in rows], [2, 7, 7])


if __name__ == "__main__":
    unittest.main()
