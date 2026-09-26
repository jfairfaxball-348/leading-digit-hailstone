from __future__ import annotations

import json
from pathlib import Path

from scripts.structured_farey_extension import (
    LOWER_1,
    UPPER_1,
    PowerApproximation,
    farey_determinant,
    next_valuation_after_rises,
    power_relation,
    symbolic_cell_count_profile,
    terminal_representatives,
)
from scripts.structured_one_minimum_bound import (
    MINIMUM_ODD_STATE,
    first_impossible_rise_length,
    maximum_minimum_state,
)

OUTPUT = Path("data/structured_farey_next_record.json")
PREVIOUS_MAXIMUM_MINIMUM_STATE = 3_112_972_388

UPPER_2 = PowerApproximation(
    q=UPPER_1.q + LOWER_1.q,
    r=UPPER_1.r + LOWER_1.r,
)


def run() -> dict:
    # The first denominator outside the PR #12 transfer block is exactly the
    # mediant of the current upper/lower Farey neighbours.
    assert UPPER_2 == PowerApproximation(q=64_497_107, r=102_225_496)
    assert farey_determinant(UPPER_2, LOWER_1) == 1

    # Exact integer arithmetic decides which side of log_2(3) the mediant lies.
    upper_2_sign, three_upper_2 = power_relation(UPPER_2)
    assert upper_2_sign == 1
    assert three_upper_2.bit_length() == UPPER_2.r

    maximum_minimum = maximum_minimum_state(
        UPPER_2.r, three_upper_2, MINIMUM_ODD_STATE
    )
    assert maximum_minimum == 4_350_616_725

    required_minimum_rise = 2 * UPPER_2.q - UPPER_2.r
    assert required_minimum_rise == 26_768_718

    first_impossible = first_impossible_rise_length(
        MINIMUM_ODD_STATE, maximum_minimum
    )
    assert first_impossible == 31
    assert required_minimum_rise > first_impossible

    profile = symbolic_cell_count_profile(
        MINIMUM_ODD_STATE, maximum_minimum, first_impossible
    )
    assert profile == [
        27, 47, 61, 79, 97, 115, 132, 149, 167, 185, 203, 220, 238,
        256, 270, 276, 276, 271, 259, 233, 194, 151, 124, 87, 50, 32,
        20, 13, 6, 3, 0,
    ]

    representatives = terminal_representatives(
        MINIMUM_ODD_STATE, maximum_minimum, first_impossible - 1
    )
    assert representatives == [
        1_229_721_173,
        1_380_119_257,
        1_637_781_257,
    ]
    next_valuations = [
        next_valuation_after_rises(seed, first_impossible - 1)
        for seed in representatives
    ]
    assert next_valuations == [5, 3, 2]

    # The enlargement beyond the preceding record range dies even earlier,
    # explaining why the same three depth-30 representatives remain.
    extra_interval_first_impossible = first_impossible_rise_length(
        PREVIOUS_MAXIMUM_MINIMUM_STATE + 1,
        maximum_minimum,
    )
    assert extra_interval_first_impossible == 29

    block_start = UPPER_2.q
    block_end = UPPER_2.q + LOWER_1.q - 1
    first_not_covered = block_end + 1
    assert block_end == 118_212_939
    assert first_not_covered == 118_212_940

    # At the next possible better-upper denominator, the mediant numerator is
    # within one of q*alpha because it is the sum of one upper and one lower
    # error, each strictly between -1 and 1. Hence ceil(q*alpha) is at most
    # mediant_numerator+1. Monotonicity of 2q-ceil(q*alpha) transfers the
    # resulting rise lower bound to all larger q.
    next_mediant_numerator = UPPER_2.r + LOWER_1.r
    assert next_mediant_numerator == 187_363_077
    remaining_minimum_rise = (
        2 * first_not_covered - (next_mediant_numerator + 1)
    )
    assert remaining_minimum_rise == 49_062_802

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
        "previous_upper": {"q": UPPER_1.q, "R": UPPER_1.r},
        "lower_neighbour": {
            "q": LOWER_1.q,
            "R": LOWER_1.r,
            "power_relation": "2^R < 3^q",
        },
        "next_upper_record": {
            "q": UPPER_2.q,
            "R": UPPER_2.r,
            "power_relation": "2^R > 3^q",
            "is_mediant_of_previous_upper_and_lower": True,
            "determinant_with_lower_neighbour": 1,
            "required_minimum_rise": required_minimum_rise,
            "maximum_minimum_state": maximum_minimum,
            "first_impossible_rise_length": first_impossible,
        },
        "symbolic_range": {
            "minimum": MINIMUM_ODD_STATE,
            "maximum": maximum_minimum,
            "first_impossible_rise_length": first_impossible,
            "cell_counts_by_rise_depth": profile,
            "peak_cell_count": max(profile),
            "peak_depths": [
                i + 1 for i, count in enumerate(profile)
                if count == max(profile)
            ],
            "depth_30_unique_representatives": representatives,
            "valuation_on_step_31": next_valuations,
            "newly_added_interval": {
                "minimum": PREVIOUS_MAXIMUM_MINIMUM_STATE + 1,
                "maximum": maximum_minimum,
                "first_impossible_rise_length": extra_interval_first_impossible,
            },
        },
        "farey_transfer_block": {
            "covered_q_start": block_start,
            "covered_q_end": block_end,
            "next_possible_better_upper_denominator": first_not_covered,
        },
        "structured_q_excluded_through": block_end,
        "first_q_not_covered_by_farey_transfer": first_not_covered,
        "certified_minimum_rise_length_for_any_remaining_structured_cycle": (
            remaining_minimum_rise
        ),
        "rise_bound_note": (
            "At q=118212940 the next mediant numerator is 187363077. "
            "From the exact signs of the current upper and lower neighbours, "
            "its absolute error is between -1 and 1, hence "
            "ceil(q log_2 3) <= 187363078. Monotonicity of "
            "2q-ceil(q log_2 3) gives a >= 49062802 for every remaining q."
        ),
        "mechanism_note": (
            "Expanding M_max from 3112972388 to 4350616725 introduces no "
            "new depth-30 representatives: the added interval is already "
            "empty after 29 rises. The full enlarged range still has the "
            "same three depth-30 representatives and becomes empty at rise 31."
        ),
        "interpretation": (
            "The first previously uncovered denominator is itself the next "
            "exact upper Farey record. Its theorem-derived minimum range is "
            "eliminated by the same finite-range decimal-sector/binary-lift "
            "squeeze, extending the one-rise/one-fall exclusion through "
            "q=118212939 under the 5M premise. This is not a global "
            "structured-cycle exclusion and does not change the arbitrary-"
            "cycle q>=971 bound."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
