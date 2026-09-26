from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.post_lock_phase_separation import (
    EXACT_BOUNDARY_COINCIDENCES,
    LOCK_STATES,
    enumerate_exact_boundary_coincidences,
    minimum_noncoincident_boundary_gap,
    phase_residue_certificate,
    run,
)


class PostLockPhaseSeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = run()

    def test_recorded_certificate_matches_exact_recomputation(self) -> None:
        recorded = json.loads(
            Path("data/post_lock_phase_separation.json").read_text()
        )
        self.assertEqual(self.payload, recorded)

    def test_phase_residue_certificates_recover_known_tails(self) -> None:
        expected = {
            "farey_candidate_1": (3, "2357"),
            "farey_candidate_2": (2, "357"),
            "tail_six_counterexample": (6, "1124691"),
        }
        for name, (tail, word) in expected.items():
            certificate = phase_residue_certificate(LOCK_STATES[name])
            self.assertEqual(certificate["status"], "RESIDUE_MISMATCH")
            self.assertEqual(certificate["certified_exact_r1_tail"], tail)
            self.assertEqual(certificate["forced_digits"], word)

    def test_scale_aware_noncoincident_gap_thresholds(self) -> None:
        self.assertEqual(
            minimum_noncoincident_boundary_gap(LOCK_STATES["farey_candidate_1"]),
            41,
        )
        self.assertEqual(
            minimum_noncoincident_boundary_gap(LOCK_STATES["farey_candidate_2"]),
            41,
        )
        self.assertEqual(
            minimum_noncoincident_boundary_gap(
                LOCK_STATES["tail_six_counterexample"]
            ),
            61,
        )

    def test_exact_coincident_boundary_chains(self) -> None:
        self.assertEqual(
            enumerate_exact_boundary_coincidences(),
            EXACT_BOUNDARY_COINCIDENCES,
        )


if __name__ == "__main__":
    unittest.main()
