import Mathlib

/-!
# Leading-Digit Hailstone: conditional accelerated-cycle lower bound

For a positive accelerated periodic orbit, write the odd states as `state i`
and let `valuation i` be the power of two removed from the corresponding
odd-branch numerator.  The successor is represented by a permutation of the
finite index set, which is all the product argument needs.

The decimal leading digit is written directly as
`state i / 10^(Nat.log 10 (state i))`, so this Challenge depends only on
Mathlib.  Under the explicit hypothesis that every state is at least 5,000,001,
the theorem proves that the accelerated cycle has at least 971 odd states.

The lower bound is conditional on that minimum-state hypothesis.  This theorem
does not formalize the repository's finite census through 5,000,000, does not
exclude every competing cycle, and does not prove the universal convergence
conjecture.
-/

namespace LeadingDigitHailstonePalomar

/-- Any positive accelerated Leading-Digit Hailstone cycle whose odd states are
all at least 5,000,001 contains at least 971 odd states. -/
theorem leadingDigitCyclePeriodLowerBound
    {q : ℕ}
    (hq : 0 < q)
    (state valuation : Fin q → ℕ)
    (next : Equiv.Perm (Fin q))
    (hstatePos : ∀ i, 0 < state i)
    (hmin : ∀ i, 5_000_001 ≤ state i)
    (hstep : ∀ i,
      2 ^ valuation i * state (next i) =
        3 * state i +
          2 * (state i / (10 ^ Nat.log 10 (state i))) + 1) :
    971 ≤ q := by
  sorry

end LeadingDigitHailstonePalomar
