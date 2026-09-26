import LeadingDigitHailstone.ValuationBurst

/-!
# Proved Palomar solution

The compared declaration has exactly the Challenge type and delegates only to
the kernel-checked arithmetic theorem in the substantive development.  It does
not import or assert the universal convergence conjecture.
-/

namespace LeadingDigitHailstonePalomar

theorem valuationBurstFamily (k : ℕ) :
    let n := 2 * 10 ^ k - 1
    10 ^ k ≤ n ∧
      n < 2 * 10 ^ k ∧
      3 * n + 3 = 6 * 10 ^ k ∧
      6 * 10 ^ k = 3 * 2 ^ (k + 1) * 5 ^ k ∧
      2 ^ (k + 1) ∣ 3 * n + 3 ∧
      ¬ 2 ^ (k + 2) ∣ 3 * n + 3 ∧
      (3 * n + 3) / 2 ^ (k + 1) = 3 * 5 ^ k := by
  exact LeadingDigitHailstone.valuationBurstFamily_proved k

#print axioms LeadingDigitHailstonePalomar.valuationBurstFamily

end LeadingDigitHailstonePalomar
