import Mathlib

/-!
# Leading-Digit Hailstone: conditional accelerated-cycle lower bound

Consider one minimal positive periodic orbit of the accelerated odd-state
dynamics.  Its `q` distinct odd states are indexed cyclically by `Fin q`;
`valuation i > 0` is the exact power-of-two exponent removed from the
odd-branch numerator at position `i`.

The decimal leading digit is written directly as
`state i / 10^(Nat.log 10 (state i))`, so this Challenge depends only on
Mathlib.  Under the explicit hypothesis that every odd state is at least
5,000,001, the theorem proves that the accelerated period contains at least
971 distinct odd states.

The lower bound is conditional on that minimum-state hypothesis.  This theorem
does not formalize the repository's finite census through 5,000,000, does not
exclude every competing cycle, and does not prove the universal convergence
conjecture.
-/

namespace LeadingDigitHailstonePalomar

/-- Any minimal positive accelerated Leading-Digit Hailstone periodic orbit
whose odd states are all at least 5,000,001 contains at least 971 distinct odd
states. -/
theorem leadingDigitCyclePeriodLowerBound
    {q : ℕ}
    (hq : 0 < q)
    (state valuation : Fin q → ℕ)
    (hstatePos : ∀ i, 0 < state i)
    (hstateOdd : ∀ i, state i % 2 = 1)
    (hvaluationPos : ∀ i, 0 < valuation i)
    (hstateInj : Function.Injective state)
    (hmin : ∀ i, 5_000_001 ≤ state i)
    (hstep : ∀ i,
      2 ^ valuation i *
          state ⟨(i.val + 1) % q, Nat.mod_lt _ hq⟩ =
        3 * state i +
          2 * (state i / (10 ^ Nat.log 10 (state i))) + 1) :
    971 ≤ q := by
  sorry

end LeadingDigitHailstonePalomar
