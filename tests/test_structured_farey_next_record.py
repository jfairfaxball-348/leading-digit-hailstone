from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.structured_farey_next_record import run


class StructuredFareyNextRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(
            Path("data/structured_farey_next_record.json").read_text()
        )
        self.assertEqual(self.payload, recorded)

    def test_next_record_and_extended_block(self) -> None:
        record = self.payload["next_upper_record"]
        self.assertEqual(record["q"], 64_497_107)
        self.assertEqual(record["R"], 102_225_496)
        self.assertEqual(record["maximum_minimum_state"], 4_350_616_725)
        self.assertEqual(record["required_minimum_rise"], 26_768_718)
        self.assertEqual(
            self.payload["structured_q_excluded_through"],
            118_212_939,
        )
        self.assertEqual(
            self.payload["first_q_not_covered_by_farey_transfer"],
            118_212_940,
        )
        self.assertEqual(
            self.payload[
                "certified_minimum_rise_length_for_any_remaining_structured_cycle"
            ],
            49_062_802,
        )

    def test_symbolic_squeeze_persists(self) -> None:
        symbolic = self.payload["symbolic_range"]
        self.assertEqual(symbolic["first_impossible_rise_length"] if "first_impossible_rise_length" in symbolic else self.payload["next_upper_record"]["first_impossible_rise_length"], 31)
        self.assertEqual(symbolic["peak_cell_count"], 276)
        self.assertEqual(symbolic["peak_depths"], [16, 17])
        self.assertEqual(symbolic["cell_counts_by_rise_depth"][-2:], [3, 0])
        self.assertEqual(
            symbolic["depth_30_unique_representatives"],
            [1_229_721_173, 1_380_119_257, 1_637_781_257],
        )
        self.assertEqual(symbolic["valuation_on_step_31"], [5, 3, 2])
        self.assertEqual(
            symbolic["newly_added_interval"]["first_impossible_rise_length"],
            29,
        )


if __name__ == "__main__":
    unittest.main()
