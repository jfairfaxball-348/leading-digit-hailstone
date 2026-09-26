from __future__ import annotations

import json
from pathlib import Path

MINIMUM_ODD_STATE = 5_000_001
SEARCH_LIMIT = 1_000_000
OUTPUT = Path("data/structured_one_minimum_bound.json")


def uniform_bound_fraction(minimum: int = MINIMUM_ODD_STATE) -> tuple[int, int]:
    """Return numerator/denominator of the one-rise/one-fall product bound.

    The elementary structured-cycle theorem gives

        1 < 2^R / 3^q <= M(M-19)/(M^2-57M+361).

    The denominator is positive for the minimum values used here.
    """
    numerator = minimum * (minimum - 19)
    denominator = minimum * minimum - 57 * minimum + 361
    if denominator <= 0:
        raise ValueError("minimum is too small for the recorded rational bound")
    return numerator, denominator


def structured_window_allows(
    q: int, minimum: int = MINIMUM_ODD_STATE
) -> bool:
    """Exact necessary-window test for a structured period q."""
    three_to_q = 3**q
    r = three_to_q.bit_length()
    numerator, denominator = uniform_bound_fraction(minimum)
    return (1 << r) * denominator <= three_to_q * numerator


def run() -> dict:
    minimum = MINIMUM_ODD_STATE
    numerator, denominator = uniform_bound_fraction(minimum)

    # B<2 means at most one integer R can lie in
    #     1 < 2^R/3^q <= B.
    assert numerator < 2 * denominator

    three_to_q = 1
    first_q = None
    first_r = None

    for q in range(1, SEARCH_LIMIT + 1):
        three_to_q *= 3
        r = three_to_q.bit_length()  # least integer R with 2^R > 3^q

        if (1 << r) * denominator <= three_to_q * numerator:
            first_q = q
            first_r = r
            break

    if first_q is None or first_r is None:
        raise AssertionError("increase SEARCH_LIMIT before interpreting the result")

    excluded_through = first_q - 1
    minimum_rise = 2 * first_q - first_r

    # Regression locks for the current 5M structured-cycle consequence.
    assert excluded_through == 79_334
    assert first_q == 79_335
    assert first_r == 125_743
    assert minimum_rise == 32_927

    # If a <= minimum_rise-1 at q=first_q, then even the homogeneous
    # lower ratio 2^(2q-a)/3^q already exceeds the uniform upper bound.
    # For larger q that lower ratio grows by a factor 4/3 per added state,
    # so this proves a>=minimum_rise for every surviving q>=first_q.
    max_forbidden_rise = minimum_rise - 1
    assert (
        (4**first_q) * denominator
        > (3**first_q) * (2**max_forbidden_rise) * numerator
    )

    return {
        "schema_version": 1,
        "claim_type": "FINITE_EXACT_ARITHMETIC_CONSEQUENCE",
        "premise": (
            "one-rise/one-fall accelerated cycle entirely above 19 with "
            "minimum odd state >= 5000001"
        ),
        "premise_source": (
            "one-minimum block theorem plus exhaustive seed census through 5000000"
        ),
        "uniform_product_bound": (
            "1 < 2^R/3^q <= M(M-19)/(M^2-57M+361)"
        ),
        "minimum_odd_state_used": minimum,
        "uniform_bound_numerator": numerator,
        "uniform_bound_denominator": denominator,
        "q_excluded_through": excluded_through,
        "first_q_not_excluded_by_uniform_window": first_q,
        "unique_R_at_first_not_excluded_q": first_r,
        "minimum_rise_length_for_any_surviving_structured_cycle": minimum_rise,
        "first_survivor_relation": (
            "for q=79335, write E=sum_fall(r_i-2); "
            "then a=32927+E and b=46408-E"
        ),
        "interpretation": (
            "Any different positive one-rise/one-fall accelerated cycle "
            "consistent with the 5M minimum-element exclusion must have at "
            "least 79335 odd states and at least 32927 consecutive r=1 rise "
            "steps. q=79335 is not asserted to be realizable."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
