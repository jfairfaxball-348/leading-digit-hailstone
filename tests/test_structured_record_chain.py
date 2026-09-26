from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.structured_farey_extension import UPPER_0, UPPER_1
from scripts.structured_record_chain import (
    cells_after_rises,
    certified_power_side,
    maximum_minimum_state_log,
    rise_residue_for_digits,
    run,
)


class StructuredRecordChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(
            Path("data/structured_record_chain.json").read_text()
        )
        self.assertEqual(self.payload, recorded)

    def test_rational_log_certificate_regresses_prior_exact_integer_results(self) -> None:
        self.assertEqual(certified_power_side(UPPER_0), 1)
        self.assertEqual(certified_power_side(UPPER_1), 1)
        self.assertGreater(1 << UPPER_0.r, 3**UPPER_0.q)
        self.assertEqual(maximum_minimum_state_log(UPPER_1), 3_112_972_388)

    def test_first_new_record_is_exact_mediant_and_is_excluded(self) -> None:
        record = self.payload["new_upper_records"][0]
        self.assertEqual((record["q"], record["R"]), (64_497_107, 102_225_496))
        self.assertEqual(record["farey_determinant"], 1)
        self.assertEqual(record["maximum_minimum_state"], 4_350_616_725)
        self.assertEqual(record["required_minimum_rise"], 26_768_718)
        self.assertEqual(record["first_impossible_rise_length"], 31)

    def test_previous_terminal_words_match_direct_symbolic_cells(self) -> None:
        cells = cells_after_rises(5_000_001, 3_112_972_388, 30)
        observed = sorted(
            (
                "".join(str(digit) for digit in cell.digits),
                cell.residue,
            )
            for cell in cells
        )
        self.assertEqual(
            [word for word, _ in observed],
            [
                "112469123471123581124691234611",
                "123461123571124691234611235711",
                "123581124691234711235811246912",
            ],
        )

    def test_extended_structured_bound(self) -> None:
        self.assertEqual(
            self.payload["structured_q_excluded_through"],
            890_638_885_192,
        )
        self.assertEqual(
            self.payload["first_q_not_covered_by_this_certificate"],
            890_638_885_193,
        )
        self.assertEqual(
            self.payload[
                "certified_minimum_rise_length_for_any_remaining_structured_cycle"
            ],
            369_648_535_671,
        )

    def test_largest_processed_range_has_single_terminal_representative(self) -> None:
        symbolic = self.payload["largest_processed_symbolic_range"]
        self.assertEqual(symbolic["maximum"], 42_285_421_502_900)
        self.assertEqual(symbolic["first_impossible_rise_length"], 49)
        self.assertEqual(symbolic["cell_counts_by_rise_depth"][-2:], [1, 0])
        self.assertEqual(
            symbolic["terminal_representatives"],
            [
                {
                    "cell_lo": 26_465_544_205_035,
                    "cell_hi": 26_666_666_666_617,
                    "cell_width": 201_122_461_583,
                    "representative": 26_501_219_601_103,
                    "digit_word": (
                        "235812346112357112358112461123571123581124691235"
                    ),
                    "state_after_rises": 7_510_109_955_360_948_316_615,
                    "next_valuation": 2,
                }
            ],
        )

    def test_explicit_rise_word_residue_formula(self) -> None:
        from itertools import product

        for rises in range(1, 5):
            modulus = 1 << (rises + 1)
            for digits in product(range(1, 10), repeat=rises):
                residue = rise_residue_for_digits(digits)
                self.assertEqual(residue % 2, 1)

                x = residue
                for digit in digits:
                    numerator = 3 * x + 2 * digit + 1
                    self.assertEqual(numerator % 4, 2)
                    x = numerator // 2

                additive = 0
                for step, digit in enumerate(digits):
                    additive = 3 * additive + (2 * digit + 1) * (1 << step)
                self.assertEqual(
                    (pow(3, rises, modulus) * residue + additive) % modulus,
                    1 << rises,
                )

    def test_boundary_window_diagnostic_is_sub_modulus_but_not_empty(self) -> None:
        diagnostic = self.payload["finite_range_symbolic_complexity_diagnostic"]
        self.assertEqual(diagnostic["scaled_decimal_boundary_count_J"], 2_997)
        self.assertEqual(
            diagnostic["proved_decimal_sector_word_bound_1_plus_20J"],
            59_941,
        )
        self.assertEqual(diagnostic["residue_capacity_per_fixed_word"], 1)


if __name__ == "__main__":
    unittest.main()
