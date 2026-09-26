from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.structured_farey_extension import run


class StructuredFareyExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(
            Path("data/structured_farey_extension.json").read_text()
        )
        self.assertEqual(self.payload, recorded)

    def test_extended_structured_bound(self) -> None:
        self.assertEqual(
            self.payload["structured_q_excluded_through"],
            64_497_106,
        )
        self.assertEqual(
            self.payload["first_q_not_covered_by_farey_transfer"],
            64_497_107,
        )
        self.assertEqual(
            self.payload[
                "certified_minimum_rise_length_for_any_remaining_structured_cycle"
            ],
            26_768_717,
        )

    def test_new_symbolic_extinction_profile(self) -> None:
        symbolic = self.payload["new_symbolic_range"]
        self.assertEqual(symbolic["maximum"], 3_112_972_388)
        self.assertEqual(symbolic["first_impossible_rise_length"], 31)
        self.assertEqual(symbolic["cell_counts_by_rise_depth"][-2:], [3, 0])
        self.assertEqual(
            symbolic["depth_30_unique_representatives"],
            [1_229_721_173, 1_380_119_257, 1_637_781_257],
        )
        self.assertEqual(symbolic["valuation_on_step_31"], [5, 3, 2])


if __name__ == "__main__":
    unittest.main()
