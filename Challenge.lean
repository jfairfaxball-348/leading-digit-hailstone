import Mathlib.Tactic

/-!
# Leading-Digit Hailstone valuation-burst family

This is the small Palomar statement surface.  It uses only ordinary Mathlib
arithmetic.  For `n = 2 * 10^k - 1`, the first two inequalities place `n`
in the decimal sector `[10^k, 2*10^k)`, so its ordinary leading decimal digit
is 1.  The Leading-Digit Hailstone odd-branch numerator is therefore
`3*n + 2*1 + 1 = 3*n + 3`.

The remaining clauses give its exact factorisation, exact power of two, and
accelerated quotient.  Since `k` is arbitrary, this records unbounded
single-odd-branch 2-adic valuation bursts.  It says nothing about universal
convergence.
-/

namespace LeadingDigitHailstonePalomar

/-- For every `k`, the hostile family `2*10^k-1` lies in leading-digit
sector 1 and its odd-branch numerator has exact 2-adic valuation `k+1`,
with quotient `3*5^k`. -/
theorem valuationBurstFamily (k : ℕ) :
    let n := 2 * 10 ^ k - 1
    10 ^ k ≤ n ∧
      n < 2 * 10 ^ k ∧
      3 * n + 3 = 6 * 10 ^ k ∧
      6 * 10 ^ k = 3 * 2 ^ (k + 1) * 5 ^ k ∧
      2 ^ (k + 1) ∣ 3 * n + 3 ∧
      ¬ 2 ^ (k + 2) ∣ 3 * n + 3 ∧
      (3 * n + 3) / 2 ^ (k + 1) = 3 * 5 ^ k := by
  sorry

end LeadingDigitHailstonePalomar
