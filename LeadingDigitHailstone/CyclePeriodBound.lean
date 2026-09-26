import Mathlib

namespace LeadingDigitHailstone

open Finset BigOperators

set_option maxHeartbeats 4000000
set_option exponentiation.threshold 100000000

/-- The minimum odd-state floor supplied by the completed five-million-seed census. -/
def cycleMinimumFloor : ℕ := 5_000_001

/-- The largest possible correction 2L(n)+1 for an ordinary decimal leading digit. -/
def cycleCorrectionCeiling : ℕ := 19

/-- A Farey-neighbour denominator bound.  If p/q < x/y < p'/q' and the
cross-determinant is one, then y is at least q+q'. -/
theorem farey_denominator_bound {p q p' q' x y : ℕ}
    (hq : 0 < q) (hq' : 0 < q') (hy : 0 < y)
    (hfarey : p' * q - p * q' = 1)
    (hleft : (p : ℚ) / q < x / y)
    (hright : (x : ℚ) / y < p' / q') :
    q + q' ≤ y := by
  have h := (show p + p' ≤ x ∧ q + q' ≤ y by
    constructor <;> rw [div_lt_div_iff₀] at hleft hright <;> norm_cast at *
    · rw [Nat.sub_eq_iff_eq_add] at hfarey
      · nlinarith
      · exact le_of_lt (Nat.lt_of_sub_eq_succ hfarey)
    · nlinarith [Nat.sub_add_cancel (le_of_lt (Nat.lt_of_sub_eq_succ hfarey))])
  exact h.2

/-- Exact lower rational neighbour used for the five-million product window. -/
theorem lower_power_certificate :
    (2 : ℕ) ^ 1054 < 3 ^ 665 := by
  norm_num

/-- Exact upper rational neighbour used for the five-million product window. -/
theorem upper_power_certificate :
    (3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ 306 <
      2 ^ 485 * cycleMinimumFloor ^ 306 := by
  norm_num [cycleMinimumFloor, cycleCorrectionCeiling]

/-- The exact product window at the five-million minimum floor already forces
a period of at least 971.  This is the compact arithmetic core of the cycle
restriction: 1054/665 and 485/306 are Farey neighbours, so no rational R/q
strictly between them can have denominator below 665+306 = 971. -/
theorem periodLowerBound_of_productWindow {q R : ℕ}
    (hq : 0 < q)
    (hlower : (3 : ℕ) ^ q < 2 ^ R)
    (hupper :
      2 ^ R * cycleMinimumFloor ^ q ≤
        (3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q) :
    971 ≤ q := by
  have hlowRaised :
      (2 : ℕ) ^ (1054 * q) < 3 ^ (665 * q) := by
    have h := Nat.pow_lt_pow_left lower_power_certificate (Nat.ne_of_gt hq)
    simpa [pow_mul] using h

  have hcycleRaised :
      (3 : ℕ) ^ (665 * q) < 2 ^ (665 * R) := by
    have h := Nat.pow_lt_pow_left hlower (by norm_num : 665 ≠ 0)
    simpa [pow_mul, Nat.mul_comm] using h

  have htwoLow :
      (2 : ℕ) ^ (1054 * q) < 2 ^ (665 * R) :=
    hlowRaised.trans hcycleRaised

  have hcrossLow : 1054 * q < 665 * R :=
    (Nat.pow_lt_pow_iff_right (by norm_num : 1 < (2 : ℕ))).mp htwoLow

  have hupperRaised :
      ((2 ^ R * cycleMinimumFloor ^ q) : ℕ) ^ 306 ≤
        ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q) ^ 306 := by
    exact Nat.pow_le_pow_left hupper 306

  have hfixedRaised :
      ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ 306 : ℕ) ^ q <
        (2 ^ 485 * cycleMinimumFloor ^ 306) ^ q := by
    exact Nat.pow_lt_pow_left upper_power_certificate (Nat.ne_of_gt hq)

  have hupperRaw :
      ((2 : ℕ) ^ R) ^ 306 * (cycleMinimumFloor ^ q) ^ 306 ≤
        ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q) ^ 306 := by
    simpa only [mul_pow] using hupperRaised

  have hfixedRaw :
      ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ 306) ^ q <
        ((2 : ℕ) ^ 485) ^ q * (cycleMinimumFloor ^ 306) ^ q := by
    simpa only [mul_pow] using hfixedRaised

  have hmiddle :
      ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q) ^ 306 =
        ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ 306) ^ q := by
    rw [← pow_mul, ← pow_mul, Nat.mul_comm q 306]

  have hfloor :
      (cycleMinimumFloor ^ 306) ^ q = (cycleMinimumFloor ^ q) ^ 306 := by
    rw [← pow_mul, ← pow_mul, Nat.mul_comm 306 q]

  have hcombined :
      ((2 : ℕ) ^ R) ^ 306 * (cycleMinimumFloor ^ q) ^ 306 <
        ((2 : ℕ) ^ 485) ^ q * (cycleMinimumFloor ^ q) ^ 306 := by
    calc
      ((2 : ℕ) ^ R) ^ 306 * (cycleMinimumFloor ^ q) ^ 306
          ≤ ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q) ^ 306 :=
        hupperRaw
      _ = ((3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ 306) ^ q := hmiddle
      _ < ((2 : ℕ) ^ 485) ^ q * (cycleMinimumFloor ^ 306) ^ q := hfixedRaw
      _ = ((2 : ℕ) ^ 485) ^ q * (cycleMinimumFloor ^ q) ^ 306 := by rw [hfloor]

  have htwoHighRaw :
      ((2 : ℕ) ^ R) ^ 306 < ((2 : ℕ) ^ 485) ^ q := by
    exact (Nat.mul_lt_mul_right
      (by norm_num [cycleMinimumFloor] :
        0 < (cycleMinimumFloor ^ q) ^ 306)).mp hcombined

  have htwoHigh :
      (2 : ℕ) ^ (R * 306) < 2 ^ (485 * q) := by
    simpa only [pow_mul] using htwoHighRaw

  have hcrossHigh : R * 306 < 485 * q :=
    (Nat.pow_lt_pow_iff_right (by norm_num : 1 < (2 : ℕ))).mp htwoHigh

  have hleft : (1054 : ℚ) / 665 < R / q := by
    rw [div_lt_div_iff₀] <;> norm_num at *
    · exact_mod_cast (by simpa [Nat.mul_comm] using hcrossLow)
    · exact_mod_cast hq

  have hright : (R : ℚ) / q < 485 / 306 := by
    rw [div_lt_div_iff₀] <;> norm_num at *
    · exact_mod_cast hcrossHigh
    · exact_mod_cast hq

  have hfarey : 485 * 665 - 1054 * 306 = 1 := by
    norm_num

  have hden := farey_denominator_bound
    (p := 1054) (q := 665) (p' := 485) (q' := 306)
    (x := R) (y := q)
    (by norm_num) (by norm_num) hq hfarey hleft hright
  norm_num at hden ⊢
  exact hden

end LeadingDigitHailstone
