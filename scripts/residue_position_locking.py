from __future__ import annotations

import json
from pathlib import Path

from leading_digit_hailstone.core import accelerated_odd_step
from scripts.structured_one_minimum_bound import (
    MINIMUM_ODD_STATE,
    _first_congruent,
)
from scripts.structured_record_chain import (
    cells_after_rises,
    rise_residue_for_digits,
)

OUTPUT = Path("data/residue_position_locking.json")

PROCESSED_RECORDS = [
    (64_497_107, 4_350_616_725, 31),
    (118_212_940, 7_221_856_344, 31),
    (171_928_773, 21_238_350_355, 35),
    (397_573_379, 359_020_668_782, 38),
    (6_586_818_670, 3_753_781_445_604, 41),
    (72_057_431_991, 6_895_437_822_163, 41),
    (137_528_045_312, 42_285_421_502_900, 49),
]


def affine_additive(digits: tuple[int, ...]) -> int:
    additive = 0
    for step, digit in enumerate(digits):
        additive = 3 * additive + (2 * digit + 1) * (1 << step)
    return additive


def lift_profile(digits: tuple[int, ...]) -> dict:
    """Return the exact one-bit lift profile for a prescribed rise digit word.

    If rho_s is the unique exact-r=1 start residue modulo 2^(s+1), define

      H_s = (3^s rho_s + A_s - 2^s) / 2^(s+1).

    Appending digit d_s chooses the unique bit b_s in {0,1} with

      rho_(s+1) = rho_s + b_s 2^(s+1),
      b_s == 1 + H_s + d_s (mod 2),

    and the carry coordinate satisfies

      H_(s+1) = (1 + 3 H_s + d_s + b_s 3^(s+1)) / 2.
    """
    rho = 1
    carry = 0
    bits: list[int] = []
    rows: list[dict[str, int]] = []

    for step, digit in enumerate(digits):
        bit = (1 + carry + digit) % 2
        next_rho = rho + bit * (1 << (step + 1))
        next_carry = (
            1 + 3 * carry + digit + bit * 3 ** (step + 1)
        ) // 2

        prefix = digits[: step + 1]
        explicit = rise_residue_for_digits(prefix)
        if next_rho != explicit:
            raise AssertionError("one-bit recurrence disagrees with explicit residue")

        additive = affine_additive(prefix)
        left = 3 ** (step + 1) * next_rho + additive - (1 << (step + 1))
        if left != next_carry * (1 << (step + 2)):
            raise AssertionError("carry recurrence failed")

        bits.append(bit)
        rows.append(
            {
                "rise_depth": step + 1,
                "digit": digit,
                "lift_bit": bit,
                "residue": next_rho,
                "carry": next_carry,
            }
        )
        rho = next_rho
        carry = next_carry

    reconstructed = 1 + sum(
        bit * (1 << (index + 1)) for index, bit in enumerate(bits)
    )
    if reconstructed != rho:
        raise AssertionError("binary digit reconstruction failed")

    return {
        "residue": rho,
        "carry": carry,
        "lift_bits_low_to_high": "".join(str(bit) for bit in bits),
        "rows": rows,
    }


def lock_depth(upper: int) -> int:
    """Least rise depth B with 2^(B+1) > upper."""
    if upper < 1:
        raise ValueError("upper must be positive")
    return upper.bit_length() - 1


def ceil_log10_ratio(numerator: int, denominator: int) -> int:
    """Least k>=0 with numerator/denominator <= 10^k, using integers only."""
    if numerator <= 0 or denominator <= 0:
        raise ValueError("positive arguments required")
    if numerator <= denominator:
        return 0

    power = 1
    exponent = 0
    while denominator * power < numerator:
        power *= 10
        exponent += 1
    return exponent


def boundary_count_upper_bound(lo: int, hi: int, rises: int) -> int:
    """Explicit upper bound for J_s(lo,hi).

    At each rise depth, every relevant scaled decimal boundary lies in an
    interval whose endpoint ratio is at most (hi+19)/lo. Such an interval
    meets at most ceil(log_10((hi+19)/lo))+1 decimal decades, and each decade
    has at most nine leading-digit boundaries.
    """
    if not (1 <= lo <= hi):
        raise ValueError("require 1 <= lo <= hi")
    decades = ceil_log10_ratio(hi + 19, lo) + 1
    return 9 * rises * decades


def locked_candidate_upper_bound(lo: int, hi: int) -> int:
    """Bound starts surviving to the bit-length lock depth."""
    depth = lock_depth(hi)
    return 20 * boundary_count_upper_bound(lo, hi, depth) + 1


def direct_rise_length(seed: int, cap: int = 256) -> tuple[int, int]:
    """Return (number of initial exact-r=1 rises, first later valuation)."""
    state = seed
    rises = 0
    for _ in range(cap):
        state, valuation = accelerated_odd_step(state)
        if valuation != 1:
            return rises, valuation
        rises += 1
    raise AssertionError("direct rise cap is too small")


def locked_candidates(lo: int, hi: int) -> list[dict[str, int | str]]:
    """Enumerate exact symbolic candidates at the bit-length lock depth."""
    depth = lock_depth(hi)
    modulus = 1 << (depth + 1)
    if modulus <= hi:
        raise AssertionError("lock modulus must exceed interval upper endpoint")

    cells = cells_after_rises(lo, hi, depth)
    rows: list[dict[str, int | str]] = []

    for cell in cells:
        explicit_residue = rise_residue_for_digits(cell.digits)
        representative = _first_congruent(cell.lo, explicit_residue, modulus)
        if representative > cell.hi:
            raise AssertionError("surviving cell has no residue representative")
        if representative != explicit_residue:
            raise AssertionError(
                "bounded-range locking should identify the start with its residue"
            )

        total_rises, next_valuation = direct_rise_length(representative)
        if total_rises < depth:
            raise AssertionError("locked candidate does not realize lock-depth run")

        profile = lift_profile(cell.digits)
        if profile["residue"] != representative:
            raise AssertionError("lift profile does not reconstruct locked start")

        rows.append(
            {
                "start": representative,
                "lock_depth": depth,
                "digit_word_at_lock": "".join(str(digit) for digit in cell.digits),
                "total_exact_r1_rises": total_rises,
                "post_lock_zero_lift_tail": total_rises - depth,
                "next_valuation": next_valuation,
            }
        )

    return sorted(rows, key=lambda row: int(row["start"]))


def run() -> dict:
    record_rows = []
    for q, maximum, first_impossible in PROCESSED_RECORDS:
        depth = lock_depth(maximum)
        j_bound = boundary_count_upper_bound(
            MINIMUM_ODD_STATE,
            maximum,
            depth,
        )
        record_rows.append(
            {
                "q": q,
                "maximum_minimum_state": maximum,
                "first_impossible_rise_length": first_impossible,
                "lock_depth": depth,
                "residue_modulus": 1 << (depth + 1),
                "boundary_count_upper_bound": j_bound,
                "candidate_start_upper_bound": 20 * j_bound + 1,
                "extinction_depth_minus_lock_depth": first_impossible - depth,
            }
        )

    expected_rows = [
        (64_497_107, 32, 23_041),
        (118_212_940, 32, 28_801),
        (171_928_773, 34, 30_601),
        (397_573_379, 38, 41_041),
        (6_586_818_670, 41, 51_661),
        (72_057_431_991, 42, 60_481),
        (137_528_045_312, 45, 64_801),
    ]
    if [
        (row["q"], row["lock_depth"], row["candidate_start_upper_bound"])
        for row in record_rows
    ] != expected_rows:
        raise AssertionError("processed-record lock diagnostics changed")

    midrange = locked_candidates(MINIMUM_ODD_STATE, 21_238_350_355)
    if midrange != [
        {
            "start": 16_670_166_793,
            "lock_depth": 34,
            "digit_word_at_lock": "1235811246912347112358112469123471",
            "total_exact_r1_rises": 34,
            "post_lock_zero_lift_tail": 0,
            "next_valuation": 2,
        }
    ]:
        raise AssertionError("midrange lock diagnostic changed")

    largest = locked_candidates(MINIMUM_ODD_STATE, 42_285_421_502_900)
    if largest != [
        {
            "start": 26_501_219_601_103,
            "lock_depth": 45,
            "digit_word_at_lock": "235812346112357112358112461123571123581124691",
            "total_exact_r1_rises": 48,
            "post_lock_zero_lift_tail": 3,
            "next_valuation": 2,
        },
        {
            "start": 39_751_829_401_657,
            "lock_depth": 45,
            "digit_word_at_lock": "358123461123571123581124611235711235811246912",
            "total_exact_r1_rises": 47,
            "post_lock_zero_lift_tail": 2,
            "next_valuation": 2,
        },
    ]:
        raise AssertionError("largest-range lock diagnostic changed")

    terminal_word = tuple(
        int(digit)
        for digit in "235812346112357112358112461123571123581124691235"
    )
    terminal_profile = lift_profile(terminal_word)
    if terminal_profile["residue"] != 26_501_219_601_103:
        raise AssertionError("terminal residue changed")
    if terminal_profile["lift_bits_low_to_high"] != (
        "111001101010011111000111101001001011000000110000"
    ):
        raise AssertionError("terminal lift-bit word changed")

    return {
        "schema_version": 1,
        "claim_type": "THEOREM_PLUS_FINITE_EXACT_SYMBOLIC_AND_DIRECT_DIAGNOSTIC",
        "theorem_level_results": {
            "lift_update": (
                "For a prescribed rise word, if "
                "H_s=(3^s*rho_s+A_s-2^s)/2^(s+1), then the appended "
                "digit d_s selects the unique b_s in {0,1} satisfying "
                "b_s == 1+H_s+d_s (mod 2), and "
                "rho_(s+1)=rho_s+b_s*2^(s+1)."
            ),
            "binary_digit_identity": (
                "rho_s = 1 + sum_{j=0}^{s-1} b_j*2^(j+1); the lift bits "
                "are exactly the successive binary digits of the required "
                "starting residue above its forced odd least-significant bit."
            ),
            "normalized_update": (
                "theta_s=rho_s/2^(s+1) satisfies "
                "theta_(s+1)=(theta_s+b_s)/2."
            ),
            "bounded_range_locking": (
                "For 1<=M<=U, let B=floor(log_2 U), equivalently "
                "2^(B+1)>U. If M realizes B prescribed exact-r=1 rises, "
                "then M=rho_B. Any further compatible extension must keep "
                "the same residue and therefore has lift bits b_B=b_(B+1)=...=0."
            ),
            "candidate_compression": (
                "At B=floor(log_2 U), starts in [L,U] surviving B rises are "
                "at most 20*J_B(L,U)+1. Moreover "
                "J_s(L,U)<=9*s*(ceil(log_10((U+19)/L))+1), so the explicit "
                "lock-depth candidate bound is "
                "180*B*(ceil(log_10((U+19)/L))+1)+1."
            ),
        },
        "processed_record_lock_bounds": record_rows,
        "finite_exact_diagnostics": {
            "midrange_lock_candidates": midrange,
            "largest_processed_range_lock_candidates": largest,
            "largest_terminal_word": (
                "235812346112357112358112461123571123581124691235"
            ),
            "largest_terminal_residue": terminal_profile["residue"],
            "largest_terminal_lift_bits_low_to_high": terminal_profile[
                "lift_bits_low_to_high"
            ],
        },
        "interpretation": (
            "The residue-position problem is now rigid after the bit-length "
            "threshold: modular lift ambiguity disappears and only zero-lift "
            "tails remain. This is a genuine deterministic residue-position "
            "theorem and gives polylogarithmic candidate compression for fixed "
            "lower endpoint, but it does not bound the possible zero-lift tail "
            "length. Therefore it does not prove an explicit global finite-range "
            "rise bound, does not globally exclude one-rise/one-fall cycles, "
            "and does not alter the arbitrary-cycle q>=971 bound."
        ),
    }


def main() -> None:
    payload = run()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
