from __future__ import annotations

import json
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step
from scripts.structured_record_chain import rise_residue_for_digits

OUTPUT = Path("data/post_lock_phase.json")

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


def rational_leading_sector(
    numerator: int,
    denominator: int,
) -> tuple[int, int, int]:
    """Return (leading digit, decimal scale, integer part) exactly."""
    if numerator < denominator or denominator <= 0:
        raise ValueError("require numerator/denominator >= 1")
    integer_part = numerator // denominator
    scale = 10 ** (len(str(integer_part)) - 1)
    digit = numerator // (denominator * scale)
    if not 1 <= digit <= 9:
        raise AssertionError("invalid leading digit")
    return digit, scale, integer_part


def forced_tube_digit(lock_state: int, time: int) -> dict[str, int | bool]:
    """Test whether the width-19 post-lock tube lies in one digit sector.

    Conditional on valuation one through `time`, the normalized state obeys

        lock_state <= (2/3)^time x_time < lock_state + 19.

    Hence x_time lies in the conservative rational tube with endpoints

        (3/2)^time lock_state,
        (3/2)^time (lock_state + 19).

    If that whole tube lies inside one decimal sector, the actual leading digit
    is forced without following the actual post-lock orbit.
    """
    if lock_state < 1 or time < 0:
        raise ValueError("require positive lock state and nonnegative time")

    three = 3**time
    two = 1 << time
    lower_num = three * lock_state
    upper_num = three * (lock_state + 19)
    digit, scale, _ = rational_leading_sector(lower_num, two)
    sector_lo = digit * scale
    sector_hi = (digit + 1) * scale

    forced = sector_lo * two <= lower_num and upper_num < sector_hi * two
    return {
        "time": time,
        "digit": digit,
        "decimal_scale": scale,
        "forced": forced,
        "lower_numerator": lower_num,
        "upper_numerator": upper_num,
        "denominator": two,
    }


def phase_residue_certificate(lock_state: int, horizon: int = 128) -> dict:
    """Certify a post-lock tail by homogeneous phase plus one congruence.

    As long as every width-19 tube lies inside one decimal sector, the digit
    word is forced by the homogeneous (3/2)^t phase. The established terminal
    residue formula then decides whether all exact-r=1 conditions through a
    given prefix can hold. The first mismatch proves termination before that
    prefix length without direct post-lock orbit following.
    """
    if horizon < 1:
        raise ValueError("horizon must be positive")

    digits: list[int] = []
    rows: list[dict[str, int | bool]] = []

    for time in range(horizon):
        phase = forced_tube_digit(lock_state, time)
        if not phase["forced"]:
            return {
                "lock_state": lock_state,
                "status": "PHASE_AMBIGUITY",
                "forced_prefix_length": len(digits),
                "forced_digits": "".join(str(d) for d in digits),
                "ambiguity_time": time,
                "rows": rows,
            }

        digit = int(phase["digit"])
        digits.append(digit)
        prefix_length = len(digits)
        modulus = 1 << (prefix_length + 1)
        residue = rise_residue_for_digits(tuple(digits))
        start_modulus = lock_state % modulus
        matches = residue == start_modulus

        rows.append(
            {
                "prefix_length": prefix_length,
                "digit": digit,
                "residue_modulus": modulus,
                "required_residue": residue,
                "lock_state_residue": start_modulus,
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
                "required_residue": residue,
                "lock_state_residue": start_modulus,
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
    """Direct orbit following, retained only as an independent cross-check."""
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
    """Smallest n with lock_state <= 171*3^n.

    The boundary-separation theorem proves that two distinct scaled decimal
    boundary hits cannot occur with a smaller positive time gap.
    """
    if lock_state <= 0:
        raise ValueError("lock_state must be positive")
    n = 1
    while 171 * 3**n < lock_state:
        n += 1
    return n


def enumerate_exact_boundary_coincidences(
    max_gap: int = 8,
) -> list[dict[str, int]]:
    """Finite exact cross-check of the theorem-level coincidence classification."""
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
    certificates = {}
    expected_tails = {
        "farey_candidate_1": 3,
        "farey_candidate_2": 2,
        "tail_six_counterexample": 6,
    }

    for name, lock_state in LOCK_STATES.items():
        phase = phase_residue_certificate(lock_state)
        direct = direct_r1_tail(lock_state)
        if phase["status"] != "RESIDUE_MISMATCH":
            raise AssertionError(f"phase certificate did not terminate for {name}")
        if phase["certified_exact_r1_tail"] != expected_tails[name]:
            raise AssertionError(f"phase tail changed for {name}")
        if direct["exact_r1_tail"] != expected_tails[name]:
            raise AssertionError(f"direct tail changed for {name}")
        if phase["certified_exact_r1_tail"] != direct["exact_r1_tail"]:
            raise AssertionError("phase-residue and direct certificates disagree")

        certificates[name] = {
            "lock_state": lock_state,
            "lock_state_bit_length": lock_state.bit_length(),
            "minimum_noncoincident_boundary_gap": (
                minimum_noncoincident_boundary_gap(lock_state)
            ),
            "phase_residue": phase,
            "direct_cross_check": direct,
        }

    coincidences = enumerate_exact_boundary_coincidences()
    if coincidences != EXACT_BOUNDARY_COINCIDENCES:
        raise AssertionError("exact boundary coincidence classification changed")

    return {
        "schema_version": 1,
        "claim_type": "THEOREM_PLUS_FINITE_EXACT_PHASE_RESIDUE_CERTIFICATES",
        "theorem_level_results": {
            "normalized_post_lock_tube": (
                "For a valuation-one tail from lock state X, "
                "Y_t=(2/3)^t x_t is increasing and remains in [X,X+19). "
                "Equivalently the true state lies in a multiplicative "
                "(3/2)^t image of one fixed width-19 interval."
            ),
            "sector_escape": (
                "Within one decimal leading-digit sector, digit d>=2 exits "
                "in one valuation-one step; digit 1 exits within two. Six "
                "valuation-one steps increase the state by a factor greater "
                "than 10, so a single decimal decade cannot contain a longer "
                "source run."
            ),
            "boundary_separation": (
                "If two distinct scaled decimal-boundary hits occur n steps "
                "apart inside [X,X+19], then X<=171*3^n. Exact coincident "
                "scaled hits are only 2->3, 4->6, 6->9 at gap 1 and 4->9 "
                "at gap 2."
            ),
            "phase_residue_reduction": (
                "On any horizon with no tube/boundary ambiguity, the decimal "
                "digit word is forced by the homogeneous (3/2)^t phase, and "
                "exact-r=1 survival of a prefix reduces to the established "
                "single terminal 2-adic residue congruence."
            ),
        },
        "finite_exact_certificates": certificates,
        "exact_boundary_coincidences": coincidences,
        "interpretation": (
            "The phase route now has a rigorous scale-aware sparsity theorem "
            "for decimal ambiguity and a candidate-specific phase/residue "
            "termination certificate. It does not yet bound the total "
            "deterministic post-lock tail: long intervals with a fully forced "
            "homogeneous digit word can still satisfy successive 2-adic "
            "conditions."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
