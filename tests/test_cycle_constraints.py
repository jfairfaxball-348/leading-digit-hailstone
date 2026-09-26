from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.analyze_weak_run_recovery import run as run_weak_recovery
from scripts.cycle_minimum_length_bound import (
    coarse_product_window_allows,
    minimal_r_for_q,
    run as run_cycle_bound,
)
from scripts.structured_one_minimum_bound import (
    run as run_structured_bound,
    structured_window_allows,
    uniform_bound_fraction,
)


class CycleMinimumLengthBoundTests(unittest.TestCase):
    def test_boundary_between_excluded_and_not_excluded(self) -> None:
        self.assertFalse(coarse_product_window_allows(970))
        self.assertTrue(coarse_product_window_allows(971))
        self.assertEqual(minimal_r_for_q(971), 1539)

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        payload = run_cycle_bound()
        recorded = json.loads(
            Path("data/cycle_minimum_length_bound.json").read_text()
        )
        self.assertEqual(payload, recorded)
        self.assertEqual(payload["q_excluded_through"], 970)
        self.assertEqual(
            payload["first_q_not_excluded_by_this_coarse_inequality"], 971
        )


class StructuredOneMinimumBoundTests(unittest.TestCase):
    def test_boundary_between_excluded_and_first_survivor(self) -> None:
        self.assertFalse(structured_window_allows(79_334))
        self.assertTrue(structured_window_allows(79_335))
        numerator, denominator = uniform_bound_fraction()
        self.assertEqual(numerator, 24_999_914_999_982)
        self.assertEqual(denominator, 24_999_725_000_305)
        self.assertLess(numerator, 2 * denominator)

    def test_recorded_structured_certificate_matches_exact_recomputation(self) -> None:
        payload = run_structured_bound()
        recorded = json.loads(
            Path("data/structured_one_minimum_bound.json").read_text()
        )
        self.assertEqual(payload, recorded)
        self.assertEqual(payload["q_excluded_through"], 79_334)
        self.assertEqual(payload["first_q_not_excluded_by_uniform_window"], 79_335)
        self.assertEqual(payload["unique_R_at_first_not_excluded_q"], 125_743)
        self.assertEqual(
            payload["minimum_rise_length_for_any_surviving_structured_cycle"],
            32_927,
        )


class WeakRunRecoveryTests(unittest.TestCase):
    def test_recorded_profiles_match_recomputation(self) -> None:
        payload = run_weak_recovery()
        recorded = json.loads(Path("data/weak_run_recovery.json").read_text())
        self.assertEqual(payload, recorded)
        self.assertEqual(
            [x["first_non_one_valuation"] for x in payload["examples"]],
            [2, 3, 2],
        )
        self.assertEqual(
            [x["accelerated_steps_to_first_below_seed"] for x in payload["examples"]],
            [51, 128, 304],
        )


if __name__ == "__main__":
    unittest.main()
