from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.structured_record_chain import (
    ALPHA_LOWER,
    ALPHA_UPPER,
    LN2_LOWER,
    LN2_UPPER,
    LN3_LOWER,
    LN3_UPPER,
    PowerApproximation,
    alpha_side,
    maximum_minimum_state_via_logs,
    record_blocks,
    run,
)


class StructuredRecordChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_log_enclosures_are_ordered(self) -> None:
        self.assertLess(LN2_LOWER, LN2_UPPER)
        self.assertLess(LN3_LOWER, LN3_UPPER)
        self.assertLess(ALPHA_LOWER, ALPHA_UPPER)

    def test_log_window_matches_previous_exact_big_integer_records(self) -> None:
        self.assertEqual(
            maximum_minimum_state_via_logs(
                PowerApproximation(q=190_537, r=301_994)
            ),
            589_078_792,
        )
        self.assertEqual(
            maximum_minimum_state_via_logs(
                PowerApproximation(q=10_781_274, r=17_087_915)
            ),
            3_112_972_388,
        )

    def test_stern_brocot_upper_record_chain(self) -> None:
        blocks = record_blocks()
        observed = [block.upper.q for block in blocks]
        observed.append(blocks[-1].next_upper.q)
        self.assertEqual(
            observed,
            [
                64_497_107,
                118_212_940,
                171_928_773,
                397_573_379,
                6_586_818_670,
                72_057_431_991,
                137_528_045_312,
                890_638_885_193,
            ],
        )
        self.assertEqual(
            [block.intervening_lower_mediants for block in blocks],
            [0, 0, 1, 15, 9, 0, 5],
        )
        self.assertTrue(all(alpha_side(block.upper) == 1 for block in blocks))

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(
            Path("data/structured_record_chain.json").read_text()
        )
        self.assertEqual(self.payload, recorded)

    def test_extended_structured_bound(self) -> None:
        self.assertEqual(
            self.payload["structured_q_excluded_through"],
            890_638_885_192,
        )
        self.assertEqual(
            self.payload["first_q_not_covered_by_current_certificate"],
            890_638_885_193,
        )
        self.assertEqual(
            self.payload[
                "certified_minimum_rise_length_for_any_remaining_structured_cycle"
            ],
            369_648_535_671,
        )

    def test_symbolic_extinction_stays_logarithmic_scale_in_certificate(self) -> None:
        rows = self.payload["record_blocks"]
        self.assertEqual(
            [row["first_impossible_rise_length"] for row in rows],
            [31, 31, 35, 38, 41, 41, 49],
        )
        self.assertEqual(
            [row["peak_symbolic_cell_count"] for row in rows],
            [276, 301, 350, 485, 603, 636, 727],
        )
        for row in rows:
            self.assertLess(
                row["first_impossible_rise_length"],
                row["required_minimum_rise_at_block_start"],
            )
            self.assertLessEqual(
                row["peak_symbolic_cell_count"],
                row["symbolic_complexity_bound_at_terminal_depth"][
                    "cell_count_upper_bound"
                ],
            )


if __name__ == "__main__":
    unittest.main()
