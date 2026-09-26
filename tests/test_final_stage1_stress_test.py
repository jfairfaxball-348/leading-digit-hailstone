from __future__ import annotations

import json
import unittest
from pathlib import Path

from leading_digit_hailstone.core import step
from scripts.final_stage1_stress_test import (
    analyze_independent,
    construct_long_r1_case,
    inverse_tree_stress,
    phase_tail_search,
    step_independent,
)


class FinalStage1StressTestTests(unittest.TestCase):
    def test_recorded_gate_summary(self) -> None:
        payload = json.loads(Path("data/final_stage1_stress_test.json").read_text())
        gate = payload["gate_observations"]
        self.assertFalse(gate["competing_positive_cycle_found"])
        self.assertFalse(gate["apparent_escaping_orbit_or_cap_hit_found"])
        self.assertFalse(gate["post_lock_tail_longer_than_six_found"])
        self.assertFalse(gate["conjecture_statement_requires_change"])
        self.assertFalse(gate["implementation_ambiguity_found"])

    def test_independent_step_agrees_with_reference_on_large_edges(self) -> None:
        cases = [
            5 * 10**1500 - 9,
            9 * 10**1000 + 99,
            10**600 + 1,
            43_574_304_770_317_398_119,
        ]
        for value in cases:
            self.assertEqual(step_independent(value), step(value))

    def test_new_large_boundary_record_converges(self) -> None:
        result = analyze_independent(5 * 10**1500 - 9, cap=100_000)
        self.assertEqual(result["status"], "DISTINGUISHED_CYCLE")
        self.assertEqual(result["cycle_entry_steps"], 37_939)

    def test_longer_engineered_weak_run_converges(self) -> None:
        case = construct_long_r1_case(150, 350)
        self.assertEqual(case["observed_initial_r1_run"], 150)
        self.assertEqual(case["terminating_valuation"], 4)
        self.assertEqual(case["status"], "DISTINGUISHED_CYCLE")
        self.assertEqual(case["cycle_entry_steps"], 8_590)

    def test_phase_residue_challenge_recovers_tail_six(self) -> None:
        result = phase_tail_search(
            grid_start=4200,
            grid_stop=4400,
            random_phase_count=0,
            maximum_prefix=96,
        )
        self.assertEqual(result["maximum_observed_post_lock_tail"], 6)
        self.assertEqual(result["record"]["start"], "43574304770317398119")
        self.assertFalse(result["found_tail_longer_than_six"])

    def test_inverse_tree_hostile_residue_profile(self) -> None:
        result = inverse_tree_stress()
        self.assertEqual(result["unique_nodes_through_depth"], 567)
        self.assertEqual(result["odd_nodes_through_depth"], 127)
        self.assertEqual(result["hostile_seed_count"], 39)
        self.assertEqual(result["hostile_failure_count"], 0)
        self.assertEqual(
            result["missing_odd_residues_mod_128"],
            [7, 17, 29, 43, 45, 51, 53, 55, 67, 85, 91, 111, 123],
        )


if __name__ == "__main__":
    unittest.main()
