from __future__ import annotations

import json
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step, leading_digit
from scripts.post_lock_scale_geometry import (
    homogeneous_leading_digit,
    scaled_boundary_hits,
)
from scripts.structured_record_chain import rise_residue_for_digits

OUTPUT = Path("data/post_lock_phase_separation.json")

LOCK_STATES = {
    "farey_candidate_1": 2_225_217_764_551_392_093_807,
    "farey_candidate_2": 3_337_826_646_827_088_140_713,
    "tail_six_counterexample": 12_166_406_006_866_046_930_622_304_922_581,
}

EXACT_BOUNDARY_COINCIDENCES = [
    {"time_gap": 1, "decade_gap": 0, "from_digit": 2, "to_digit": 3},
    {"time_gap": 1, "decade_gap": 0, "from_digit": 4, "to_digit": 6},
    {"time_gap": 1, "decade_gap": 0, "from_digit": 6, "to_digit": 9},
    {"time_gap": 2, "decade_gap": 0, "from_digit": 4, "to_digit": 9},
]


def phase_residue_certificate(lock_state: int, horizon: int = 128) -> dict:
    """Terminate a phase-frozen post-lock tail by its terminal 2-adic residue.

    PR #17 proves that an actual/homogeneous digit mismatch at positive time
    requires a scaled decimal-boundary hit inside the width-19 corridor.
    Therefore, while no such hit occurs, the digit word is forced by the exact
    homogeneous rational (3/2)^t * lock_state.

    For a fixed digit word, the established terminal residue formula is
    equivalent to all exact-r=1 parity conditions in that prefix. The first
    residue mismatch therefore proves the deterministic tail cannot extend to
    that prefix length.
    """
    if lock_state < 1 or horizon < 1:
        raise ValueError("require a positive lock_state and positive horizon")

    digits: list[int] = []
    rows: list[dict[str, int | bool | list[int]]] = []

    for time in range(horizon):
        hits = [] if time == 0 else scaled_boundary_hits(lock_state, time)
        if hits:
            return {
                "lock_state": lock_state,
                "status": "PHASE_AMBIGUITY",
                "forced_prefix_length": len(digits),
                "forced_digits": "".join(str(d) for d in digits),
                "ambiguity_time": time,
                "boundary_hits": hits,
                "rows": rows,
            }

        digit = (
            leading_digit(lock_state)
            if time == 0
            else homogeneous_leading_digit(lock_state, time)
        )
        digits.append(digit)

        prefix_length = len(digits)
        modulus = 1 << (prefix_length + 1)
        required_residue = rise_residue_for_digits(tuple(digits))
        actual_residue = lock_state % modulus
        matches = required_residue == actual_residue

        rows.append(
            {
                "prefix_length": prefix_length,
                "digit": digit,
                "boundary_hits": hits,
                "residue_modulus": modulus,
                "required_residue": required_residue,
                "lock_state_residue": actual_residue,
                "matches": matches,
            }
        )

        if not matches:
            return {
                "lock_state": lock_state,
                "status": "RESIDUE_MISMATCH",
                "forced_prefix_length": prefix_length,
                "forced_digits": "".join(str(d) for d in digits),
                "certified_exact_r1_tail": prefix_length - 1,
                "first_impossible_r1_prefix": prefix_length,
                "mismatch_modulus": modulus,
                "required_residue": required_residue,
                "lock_state_residue": actual_residue,
                "rows": rows,
            }

    return {
        "lock_state": lock_state,
        "status": "HORIZON_SURVIVED",
        "forced_prefix_length": horizon,
        "forced_digits": "".join(str(d) for d in digits),
        "rows": rows,
    }


def direct_r1_tail(lock_state: int, cap: int = 256) -> dict[str, int]:
    """Independent finite cross-check; not part of the phase/residue proof."""
    state = lock_state
    tail = 0
    for _ in range(cap):
        next_state, valuation = accelerated_odd_step(state)
        if valuation != 1:
            return {
                "exact_r1_tail": tail,
                "next_valuation": valuation,
                "terminal_source": state,
                "next_odd_state": next_state,
            }
        state = next_state
        tail += 1
    raise AssertionError("cap too small")


def minimum_noncoincident_boundary_gap(lock_state: int) -> int:
    """Least n>=1 for which the separation theorem no longer forbids a hit.

    If two *distinct* scaled boundary hits occur n steps apart inside the
    width-19 corridor, the theorem proves lock_state <= 171*3^n.
    """
    if lock_state < 1:
        raise ValueError("lock_state must be positive")
    n = 1
    while 171 * 3**n < lock_state:
        n += 1
    return n


def enumerate_exact_boundary_coincidences(
    max_gap: int = 8,
) -> list[dict[str, int]]:
    """Finite cross-check of the theorem-level exact-coincidence classification."""
    out: list[dict[str, int]] = []
    for n in range(1, max_gap + 1):
        for m in range(0, 4):
            for d in range(1, 10):
                for e in range(1, 10):
                    if e * (2**n) * (10**m) == d * (3**n):
                        out.append(
                            {
                                "time_gap": n,
                                "decade_gap": m,
                                "from_digit": d,
                                "to_digit": e,
                            }
                        )
    return out


def run() -> dict:
    expected = {
        "farey_candidate_1": (3, "2357", 41),
        "farey_candidate_2": (2, "357", 41),
        "tail_six_counterexample": (6, "1124691", 61),
    }
    certificates: dict[str, object] = {}

    for name, lock_state in LOCK_STATES.items():
        tail, word, gap = expected[name]
        phase = phase_residue_certificate(lock_state)
        direct = direct_r1_tail(lock_state)

        if phase["status"] != "RESIDUE_MISMATCH":
            raise AssertionError(f"phase certificate did not terminate for {name}")
        if phase["certified_exact_r1_tail"] != tail:
            raise AssertionError(f"phase tail changed for {name}")
        if phase["forced_digits"] != word:
            raise AssertionError(f"forced phase word changed for {name}")
        if direct["exact_r1_tail"] != tail:
            raise AssertionError(f"direct cross-check changed for {name}")
        if minimum_noncoincident_boundary_gap(lock_state) != gap:
            raise AssertionError(f"boundary separation threshold changed for {name}")

        certificates[name] = {
            "lock_state": lock_state,
            "lock_state_bit_length": lock_state.bit_length(),
            "minimum_noncoincident_boundary_gap": gap,
            "forced_digits_through_failure": phase["forced_digits"],
            "certified_exact_r1_tail": phase["certified_exact_r1_tail"],
            "first_impossible_r1_prefix": phase["first_impossible_r1_prefix"],
            "mismatch_modulus": phase["mismatch_modulus"],
            "required_residue": phase["required_residue"],
            "lock_state_residue": phase["lock_state_residue"],
            "direct_next_valuation_cross_check": direct["next_valuation"],
        }

    coincidences = enumerate_exact_boundary_coincidences()
    if coincidences != EXACT_BOUNDARY_COINCIDENCES:
        raise AssertionError("boundary coincidence classification changed")

    return {
        "schema_version": 1,
        "claim_type": "THEOREM_PLUS_FINITE_EXACT_PHASE_RESIDUE_CERTIFICATES",
        "theorem_level_results": {
            "boundary_hit_separation": (
                "For X>38, if two distinct scaled decimal-boundary hits inside "
                "(X,X+19) occur n steps apart, then X<=171*3^n."
            ),
            "exact_boundary_coincidences": (
                "The only equal scaled-boundary hits at different times are "
                "2->3, 4->6, 6->9 at gap 1 and 4->9 at gap 2."
            ),
            "phase_residue_reduction": (
                "On a horizon with no scaled boundary hit, PR #17 forces the "
                "actual digit word to equal the homogeneous (3/2)^t digit word; "
                "exact-r=1 survival then reduces to the established single "
                "terminal 2-adic residue congruence."
            ),
        },
        "finite_exact_certificates": certificates,
        "exact_boundary_coincidences": coincidences,
        "interpretation": (
            "PR #17 showed that observed positive post-lock tails through B=220 "
            "are phase-frozen. This increment proves a scale-aware separation law "
            "for the exceptional boundary-hit times and turns phase-frozen blocks "
            "into direct 2-adic residue certificates. It still does not give a "
            "uniform F(B) or F(M) tail bound."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
