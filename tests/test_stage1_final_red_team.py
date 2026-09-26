from __future__ import annotations

import json
import unittest
from pathlib import Path

from leading_digit_hailstone.verify import (
    leading_digit_independent,
    step_independent,
)
from scripts.post_lock_scale_geometry import own_bit_locked_candidates
from scripts.stage1_final_red_team import (
    analyze_adversarial,
    inverse_frontier,
    v2,
    weak_run_case,
)


class Stage1FinalRedTeamTests(unittest.TestCase):
    def test_unbounded_valuation_family_instances(self) -> None:
        for k in (0, 1, 10, 100, 500):
            seed = 2 * 10**k - 1
            numerator = step_independent(seed)
            self.assertEqual(leading_digit_independent(seed), 1)
            self.assertEqual(numerator, 6 * 10**k)
            self.assertEqual(v2(numerator), k + 1)
            self.assertEqual(numerator >> (k + 1), 3 * 5**k)

    def test_independent_adversarial_analyzer_matches_known_boundary_case(self) -> None:
        result = analyze_adversarial(900_000_000_000_001)
        self.assertEqual(result["status"], "DISTINGUISHED_CYCLE")
        self.assertEqual(result["cycle_entry_steps"], 520)

    def test_inverse_tree_depth_ten_profile(self) -> None:
        seen, frontier, profile = inverse_frontier(10)
        self.assertEqual(len(seen), 52)
        self.assertEqual(len(frontier), 11)
        self.assertEqual(
            profile[-1],
            {
                "depth": 10,
                "new_nodes": 11,
                "odd_preimage_edges": 4,
                "maximum_node": 16_384,
            },
        )

    def test_residue_engineered_smoke_case(self) -> None:
        case = weak_run_case(30, 60)
        self.assertGreaterEqual(case["observed_initial_r1_run"], 30)
        self.assertEqual(case["trajectory_status"], "DISTINGUISHED_CYCLE")
        self.assertEqual(case["cycle_entry_steps"], 1771)

    def test_post_lock_extension_has_exact_tail_three_case(self) -> None:
        rows = own_bit_locked_candidates(269)
        matches = [
            row
            for row in rows
            if int(row["post_lock_tail"]) == 3
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(
            matches[0]["start"],
            1_056_351_908_313_112_224_451_188_801_200_261_182_454_967_607_202_503_176_425_731_685_505_998_071_295_969_797,
        )
        self.assertEqual(matches[0]["next_valuation"], 2)

    def test_compact_certificates_record_stage1_outcome(self) -> None:
        red_team = json.loads(Path("data/stage1_final_red_team.json").read_text())
        post_lock = json.loads(
            Path("data/post_lock_scan_extension_b300.json").read_text()
        )
        self.assertTrue(
            red_team["campaign_outcome"][
                "all_tested_seeds_entered_distinguished_cycle"
            ]
        )
        self.assertFalse(red_team["campaign_outcome"]["competing_cycle_found"])
        self.assertEqual(
            post_lock["combined_complete_scan_bit_depth_range"],
            [1, 300],
        )
        self.assertEqual(
            post_lock["combined_observed_maximum_post_lock_tail"],
            6,
        )


if __name__ == "__main__":
    unittest.main()
