import Mathlib.Tactic

namespace LeadingDigitHailstone

/-- Kernel-checked arithmetic proof of the Stage-1 valuation-burst family.
This theorem is deliberately independent of the unproved convergence
conjecture. -/
theorem valuationBurstFamily_proved (k : ℕ) :
    let n := 2 * 10 ^ k - 1
    10 ^ k ≤ n ∧
      n < 2 * 10 ^ k ∧
      3 * n + 3 = 6 * 10 ^ k ∧
      6 * 10 ^ k = 3 * 2 ^ (k + 1) * 5 ^ k ∧
      2 ^ (k + 1) ∣ 3 * n + 3 ∧
      ¬ 2 ^ (k + 2) ∣ 3 * n + 3 ∧
      (3 * n + 3) / 2 ^ (k + 1) = 3 * 5 ^ k := by
  dsimp
  have hpow10 : 0 < 10 ^ k := by
    positivity
  have hlow : 10 ^ k ≤ 2 * 10 ^ k - 1 := by
    omega
  have hhigh : 2 * 10 ^ k - 1 < 2 * 10 ^ k := by
    omega
  have hnum : 3 * (2 * 10 ^ k - 1) + 3 = 6 * 10 ^ k := by
    omega
  have hfactor : 6 * 10 ^ k = 3 * 2 ^ (k + 1) * 5 ^ k := by
    rw [show (10 : ℕ) = 2 * 5 by norm_num, mul_pow, pow_succ]
    ring
  have hcombined :
      3 * (2 * 10 ^ k - 1) + 3 = 2 ^ (k + 1) * (3 * 5 ^ k) := by
    calc
      3 * (2 * 10 ^ k - 1) + 3 = 6 * 10 ^ k := hnum
      _ = 3 * 2 ^ (k + 1) * 5 ^ k := hfactor
      _ = 2 ^ (k + 1) * (3 * 5 ^ k) := by ring
  have hdvd : 2 ^ (k + 1) ∣ 3 * (2 * 10 ^ k - 1) + 3 := by
    exact ⟨3 * 5 ^ k, hcombined⟩
  have hodd : Odd (3 * 5 ^ k) := by
    exact (show Odd (3 : ℕ) by norm_num).mul
      ((show Odd (5 : ℕ) by norm_num).pow)
  have hnot :
      ¬ 2 ^ (k + 2) ∣ 3 * (2 * 10 ^ k - 1) + 3 := by
    intro hbig
    have hpow :
        (2 : ℕ) ^ (k + 2) = 2 ^ (k + 1) * 2 := by
      rw [show k + 2 = (k + 1) + 1 by omega, pow_succ]
    rw [hpow, hcombined] at hbig
    have htwo : 2 ∣ 3 * 5 ^ k :=
      Nat.dvd_of_mul_dvd_mul_left (by positivity : 0 < 2 ^ (k + 1)) hbig
    exact hodd.not_two_dvd_nat htwo
  have hquot :
      (3 * (2 * 10 ^ k - 1) + 3) / 2 ^ (k + 1) = 3 * 5 ^ k := by
    rw [hcombined]
    exact Nat.mul_div_cancel_left (3 * 5 ^ k) (by positivity)
  exact ⟨hlow, hhigh, hnum, hfactor, hdvd, hnot, hquot⟩

end LeadingDigitHailstone
