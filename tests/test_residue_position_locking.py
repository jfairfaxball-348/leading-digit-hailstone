from __future__ import annotations

import json
import unittest
from itertools import product
from pathlib import Path

from scripts.residue_position_locking import (
    MINIMUM_ODD_STATE,
    boundary_count_upper_bound,
    lift_profile,
    lock_depth,
    locked_candidate_upper_bound,
    locked_candidates,
    run,
)
from scripts.structured_record_chain import rise_residue_for_digits


class ResiduePositionLockingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(Path("data/residue_position_locking.json").read_text())
        self.assertEqual(self.payload, recorded)

    def test_lift_recurrence_matches_closed_residue_formula(self) -> None:
        for rises in range(1, 5):
            for digits in product(range(1, 10), repeat=rises):
                profile = lift_profile(tuple(digits))
                self.assertEqual(
                    profile["residue"],
                    rise_residue_for_digits(tuple(digits)),
                )
                reconstructed = 1 + sum(
                    int(bit) * (1 << (index + 1))
                    for index, bit in enumerate(profile["lift_bits_low_to_high"])
                )
                self.assertEqual(reconstructed, profile["residue"])

    def test_lock_depth_is_first_subrange_modulus(self) -> None:
        for upper in [1, 5_000_001, 21_238_350_355, 42_285_421_502_900]:
            depth = lock_depth(upper)
            self.assertLessEqual(1 << depth, upper)
            self.assertGreater(1 << (depth + 1), upper)

    def test_explicit_boundary_and_candidate_bounds(self) -> None:
        upper = 42_285_421_502_900
        depth = lock_depth(upper)
        self.assertEqual(depth, 45)
        self.assertEqual(
            boundary_count_upper_bound(MINIMUM_ODD_STATE, upper, depth),
            3_240,
        )
        self.assertEqual(
            locked_candidate_upper_bound(MINIMUM_ODD_STATE, upper),
            64_801,
        )

    def test_midrange_locks_to_one_start(self) -> None:
        self.assertEqual(
            locked_candidates(MINIMUM_ODD_STATE, 21_238_350_355),
            [
                {
                    "start": 16_670_166_793,
                    "lock_depth": 34,
                    "digit_word_at_lock": "1235811246912347112358112469123471",
                    "total_exact_r1_rises": 34,
                    "post_lock_zero_lift_tail": 0,
                    "next_valuation": 2,
                }
            ],
        )

    def test_largest_range_locks_to_two_starts(self) -> None:
        rows = locked_candidates(MINIMUM_ODD_STATE, 42_285_421_502_900)
        self.assertEqual(
            [row["start"] for row in rows],
            [26_501_219_601_103, 39_751_829_401_657],
        )
        self.assertEqual(
            [row["post_lock_zero_lift_tail"] for row in rows],
            [3, 2],
        )
        self.assertEqual(
            [row["total_exact_r1_rises"] for row in rows],
            [48, 47],
        )
        self.assertEqual([row["next_valuation"] for row in rows], [2, 2])

    def test_terminal_lift_bits_reconstruct_known_representative(self) -> None:
        diagnostic = self.payload["finite_exact_diagnostics"]
        self.assertEqual(
            diagnostic["largest_terminal_residue"],
            26_501_219_601_103,
        )
        self.assertEqual(
            diagnostic["largest_terminal_lift_bits_low_to_high"],
            "111001101010011111000111101001001011000000110000",
        )


if __name__ == "__main__":
    unittest.main()
