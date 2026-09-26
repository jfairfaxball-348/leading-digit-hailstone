from __future__ import annotations

import json
from pathlib import Path

MINIMUM_ODD_STATE = 5_000_001
MAX_CORRECTION = 19
SEARCH_LIMIT = 5_000


def minimal_r_for_q(q: int) -> int:
    """Smallest integer R with 2^R > 3^q, computed exactly."""
    return (3**q).bit_length()


def coarse_product_window_allows(q: int, minimum: int = MINIMUM_ODD_STATE) -> bool:
    """Test the necessary product-window inequality using exact integers.

    For a q-state odd cycle with minimum M and total valuation R,

        1 < 2^R / 3^q <= ((3M+19)/(3M))^q.

    The left side is smallest at the minimal integer R with 2^R > 3^q.
    If that minimal R already violates the upper bound, every larger R does too.
    """
    r = minimal_r_for_q(q)
    left = (2**r) * ((3 * minimum) ** q)
    right = (3**q) * ((3 * minimum + MAX_CORRECTION) ** q)
    return left <= right


def run() -> dict:
    first_not_excluded = None
    excluded_through = 0

    for q in range(1, SEARCH_LIMIT + 1):
        if coarse_product_window_allows(q):
            first_not_excluded = q
            break
        excluded_through = q

    if first_not_excluded is None:
        raise AssertionError("increase SEARCH_LIMIT before interpreting the result")

    # Regression locks for the current 5M census consequence.
    assert excluded_through == 970
    assert first_not_excluded == 971
    assert minimal_r_for_q(971) == 1539

    return {
        "schema_version": 1,
        "claim_type": "FINITE_EXACT_ARITHMETIC_CERTIFICATE",
        "premise": "any different positive cycle has minimum odd state >= 5000001",
        "premise_source": "exhaustive seed census through 5000000",
        "necessary_inequality": "1 < 2^R/3^q <= ((3M+19)/(3M))^q",
        "minimum_odd_state_used": MINIMUM_ODD_STATE,
        "max_correction_used": MAX_CORRECTION,
        "q_excluded_through": excluded_through,
        "first_q_not_excluded_by_this_coarse_inequality": first_not_excluded,
        "minimal_R_at_first_not_excluded_q": minimal_r_for_q(first_not_excluded),
        "interpretation": (
            "Any different positive accelerated cycle consistent with the 5M "
            "minimum-element exclusion must contain at least 971 odd states. "
            "q=971 is not asserted to be realizable."
        ),
    }


def main() -> None:
    payload = run()
    out = Path("data/cycle_minimum_length_bound.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
