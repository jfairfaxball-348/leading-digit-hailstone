from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step
from scripts.structured_one_minimum_bound import (
    MINIMUM_ODD_STATE,
    RiseCell,
    _advance_rise_cells,
    _first_congruent,
    first_impossible_rise_length,
    maximum_minimum_state,
)

OUTPUT = Path("data/structured_farey_extension.json")
PREEXISTING_EXCLUSION = 400_000


@dataclass(frozen=True)
class PowerApproximation:
    q: int
    r: int


# Exact upper/lower approximations to log_2(3), recorded as R/q.
UPPER_0 = PowerApproximation(q=190_537, r=301_994)
LOWER_0 = PowerApproximation(q=10_590_737, r=16_785_921)
UPPER_1 = PowerApproximation(q=10_781_274, r=17_087_915)
LOWER_1 = PowerApproximation(q=53_715_833, r=85_137_581)


def power_relation(pair: PowerApproximation) -> tuple[int, int]:
    """Compare 2^R with 3^q exactly and return (sign, 3^q)."""
    three_to_q = 3**pair.q
    two_to_r = 1 << pair.r
    sign = (two_to_r > three_to_q) - (two_to_r < three_to_q)
    return sign, three_to_q


def farey_determinant(
    upper: PowerApproximation, lower: PowerApproximation
) -> int:
    """Return R_u q_l - R_l q_u."""
    return upper.r * lower.q - lower.r * upper.q


def cells_after_rises(lo: int, hi: int, steps: int) -> list[RiseCell]:
    """Return exact symbolic cells surviving a prescribed number of r=1 rises."""
    cells = [RiseCell(lo=lo, hi=hi, additive=0, residue=1)]

    for step in range(steps):
        cells = _advance_rise_cells(cells, step)
        modulus = 1 << (step + 2)
        cells = [
            cell
            for cell in cells
            if _first_congruent(cell.lo, cell.residue, modulus) <= cell.hi
        ]
        if not cells:
            break

    return cells


def symbolic_cell_count_profile(lo: int, hi: int, cap: int) -> list[int]:
    """Record the exact surviving symbolic-cell count after each rise depth."""
    cells = [RiseCell(lo=lo, hi=hi, additive=0, residue=1)]
    counts: list[int] = []

    for step in range(cap):
        cells = _advance_rise_cells(cells, step)
        modulus = 1 << (step + 2)
        cells = [
            cell
            for cell in cells
            if _first_congruent(cell.lo, cell.residue, modulus) <= cell.hi
        ]
        counts.append(len(cells))
        if not cells:
            break

    return counts


def terminal_representatives(lo: int, hi: int, steps: int) -> list[int]:
    """Extract unique representatives when every surviving cell is narrower than the modulus."""
    cells = cells_after_rises(lo, hi, steps)
    modulus = 1 << (steps + 1)
    representatives: list[int] = []

    for cell in cells:
        if cell.hi - cell.lo + 1 >= modulus:
            raise AssertionError("terminal cell is not narrower than the residue modulus")
        representative = _first_congruent(cell.lo, cell.residue, modulus)
        if representative > cell.hi:
            raise AssertionError("surviving cell has no residue representative")
        representatives.append(representative)

    return sorted(set(representatives))


def next_valuation_after_rises(seed: int, rises: int) -> int:
    """Validate a terminal seed directly and return the valuation of the next step."""
    x = seed
    for _ in range(rises):
        x, valuation = accelerated_odd_step(x)
        if valuation != 1:
            raise AssertionError("terminal representative does not realize the claimed rise run")
    _, valuation = accelerated_odd_step(x)
    return valuation


def run() -> dict:
    # Exact Farey-neighbour certificates.
    assert farey_determinant(UPPER_0, LOWER_0) == 1
    assert farey_determinant(UPPER_1, LOWER_1) == 1

    # The first new upper approximation is the mediant of the first pair.
    assert UPPER_1.q == UPPER_0.q + LOWER_0.q
    assert UPPER_1.r == UPPER_0.r + LOWER_0.r

    # The next lower neighbour is four upper steps beyond LOWER_0.
    assert LOWER_1.q == LOWER_0.q + 4 * UPPER_1.q
    assert LOWER_1.r == LOWER_0.r + 4 * UPPER_1.r

    upper_0_sign, three_upper_0 = power_relation(UPPER_0)
    lower_0_sign, three_lower_0 = power_relation(LOWER_0)
    upper_1_sign, three_upper_1 = power_relation(UPPER_1)
    lower_1_sign, three_lower_1 = power_relation(LOWER_1)

    assert upper_0_sign == 1
    assert lower_0_sign == -1
    assert upper_1_sign == 1
    assert lower_1_sign == -1

    # These bit-length checks show that the recorded numerators are the
    # immediate floor/ceiling integers around q*log_2(3).
    assert three_upper_0.bit_length() == UPPER_0.r
    assert three_lower_0.bit_length() == LOWER_0.r + 1
    assert three_upper_1.bit_length() == UPPER_1.r
    assert three_lower_1.bit_length() == LOWER_1.r + 1

    max_minimum_0 = maximum_minimum_state(
        UPPER_0.r, three_upper_0, MINIMUM_ODD_STATE
    )
    max_minimum_1 = maximum_minimum_state(
        UPPER_1.r, three_upper_1, MINIMUM_ODD_STATE
    )
    assert max_minimum_0 == 589_078_792
    assert max_minimum_1 == 3_112_972_388

    impossible_0 = first_impossible_rise_length(
        MINIMUM_ODD_STATE, max_minimum_0
    )
    impossible_1 = first_impossible_rise_length(
        MINIMUM_ODD_STATE, max_minimum_1
    )
    assert impossible_0 == 29
    assert impossible_1 == 31

    first_block_start = PREEXISTING_EXCLUSION + 1
    first_block_end = UPPER_1.q - 1
    second_block_start = UPPER_1.q
    second_block_end = UPPER_1.q + LOWER_1.q - 1

    # k(q)=2q-ceil(q log_2 3) is nondecreasing.  The first block therefore
    # inherits the already-recorded q=400001 lower bound.
    first_block_minimum_rise = 166_015
    assert first_block_minimum_rise > impossible_0

    # UPPER_1 is itself the unique possible R at its q.
    second_block_minimum_rise = 2 * UPPER_1.q - UPPER_1.r
    assert second_block_minimum_rise == 4_474_633
    assert second_block_minimum_rise > impossible_1

    profile = symbolic_cell_count_profile(
        MINIMUM_ODD_STATE, max_minimum_1, impossible_1
    )
    assert profile[-1] == 0
    assert profile[-2] == 3

    representatives = terminal_representatives(
        MINIMUM_ODD_STATE, max_minimum_1, impossible_1 - 1
    )
    assert representatives == [
        1_229_721_173,
        1_380_119_257,
        1_637_781_257,
    ]

    next_valuations = [
        next_valuation_after_rises(seed, impossible_1 - 1)
        for seed in representatives
    ]
    assert next_valuations == [5, 3, 2]

    first_not_covered = second_block_end + 1
    mediant_numerator = UPPER_1.r + LOWER_1.r

    # Since UPPER_1.r - q_u*alpha is in (0,1) and
    # LOWER_1.r - q_l*alpha is in (-1,0), their sum differs from
    # first_not_covered*alpha by less than 1.  Therefore
    # ceil(first_not_covered*alpha) <= mediant_numerator+1.
    remaining_minimum_rise = (
        2 * first_not_covered - (mediant_numerator + 1)
    )
    assert remaining_minimum_rise == 26_768_717

    return {
        "schema_version": 1,
        "claim_type": (
            "THEOREM_PLUS_FINITE_EXACT_ARITHMETIC_AND_SYMBOLIC_CERTIFICATE"
        ),
        "premise": (
            "one-rise/one-fall accelerated cycle entirely above 19 with "
            "minimum odd state >= 5000001"
        ),
        "premise_source": (
            "structured product envelope plus exhaustive seed census "
            "through 5000000"
        ),
        "transfer_lemma": (
            "If R_u/q_u > log_2(3) > R_l/q_l are Farey neighbours and "
            "q_u <= q < q_u+q_l, then every upper approximation R/q has "
            "R-q log_2(3) >= R_u-q_u log_2(3)."
        ),
        "preexisting_structured_q_excluded_through": PREEXISTING_EXCLUSION,
        "farey_blocks": [
            {
                "upper": {
                    "q": UPPER_0.q,
                    "R": UPPER_0.r,
                    "power_relation": "2^R > 3^q",
                    "maximum_minimum_state": max_minimum_0,
                    "first_impossible_rise_length": impossible_0,
                },
                "lower": {
                    "q": LOWER_0.q,
                    "R": LOWER_0.r,
                    "power_relation": "2^R < 3^q",
                },
                "determinant": 1,
                "covered_q_start": first_block_start,
                "covered_q_end": first_block_end,
                "next_possible_better_upper_denominator": UPPER_1.q,
                "required_rise_lower_bound_at_block_start": (
                    first_block_minimum_rise
                ),
            },
            {
                "upper": {
                    "q": UPPER_1.q,
                    "R": UPPER_1.r,
                    "power_relation": "2^R > 3^q",
                    "maximum_minimum_state": max_minimum_1,
                    "first_impossible_rise_length": impossible_1,
                },
                "lower": {
                    "q": LOWER_1.q,
                    "R": LOWER_1.r,
                    "power_relation": "2^R < 3^q",
                },
                "determinant": 1,
                "covered_q_start": second_block_start,
                "covered_q_end": second_block_end,
                "next_possible_better_upper_denominator": first_not_covered,
                "required_rise_lower_bound_at_block_start": (
                    second_block_minimum_rise
                ),
            },
        ],
        "new_record_upper_is_mediant_of_first_pair": True,
        "new_record_upper": {"q": UPPER_1.q, "R": UPPER_1.r},
        "new_symbolic_range": {
            "minimum": MINIMUM_ODD_STATE,
            "maximum": max_minimum_1,
            "first_impossible_rise_length": impossible_1,
            "cell_counts_by_rise_depth": profile,
            "depth_30_unique_representatives": representatives,
            "valuation_on_step_31": next_valuations,
        },
        "structured_q_excluded_through": second_block_end,
        "first_q_not_covered_by_farey_transfer": first_not_covered,
        "certified_minimum_rise_length_for_any_remaining_structured_cycle": (
            remaining_minimum_rise
        ),
        "rise_bound_note": (
            "At q=64497107 the mediant numerator 102225496 is within one "
            "of q*log_2(3), so ceil(q log_2(3)) <= 102225497; monotonicity "
            "of 2q-bit_length(3^q) then gives a >= 26768717 for every "
            "remaining q."
        ),
        "interpretation": (
            "The Farey-neighbour transfer eliminates whole period blocks "
            "without scanning each q. Any different positive one-rise/"
            "one-fall accelerated cycle consistent with the 5M minimum-"
            "element exclusion must have q >= 64497107 and at least "
            "26768717 consecutive r=1 rise steps. This remains a "
            "structured-class result, not a global cycle exclusion."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
