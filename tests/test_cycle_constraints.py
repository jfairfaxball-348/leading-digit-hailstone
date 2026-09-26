from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.cycle_minimum_length_bound import (
    coarse_product_window_allows,
    minimal_r_for_q,
    run,
)


class CycleMinimumLengthBoundTests(unittest.TestCase):
    def test_boundary_between_excluded_and_not_excluded(self) -> None:
        self.assertFalse(coarse_product_window_allows(970))
        self.assertTrue(coarse_product_window_allows(971))
        self.assertEqual(minimal_r_for_q(971), 1539)

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        payload = run()
        recorded = json.loads(
            Path("data/cycle_minimum_length_bound.json").read_text()
        )
        self.assertEqual(payload, recorded)
        self.assertEqual(payload["q_excluded_through"], 970)
        self.assertEqual(
            payload["first_q_not_excluded_by_this_coarse_inequality"], 971
        )


if __name__ == "__main__":
    unittest.main()
