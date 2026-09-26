import LeadingDigitHailstone.CycleRestriction

/-!
# Proved Palomar solution

The compared declaration has exactly the Mathlib-only Challenge type.  The
proof rewrites the direct decimal-leading-digit formula to the substantive
`leadingDigit` definition and invokes the kernel-checked cyclic-period
restriction.

The substantive proof derives the exact cyclic product identity, bounds the
leading-digit correction in [3,19], obtains the product window at the explicit
minimum 5,000,001, and uses the Farey-neighbour gap between 1054/665 and
485/306.  The two large power comparisons are checked by Lean's exact
`norm_num` arithmetic.

Oddness, positive valuation exponents and injective state indexing are explicit
on the Challenge surface so that `q` genuinely denotes the number of distinct
odd states in one minimal accelerated cycle. No finite Python certificate,
census result, or universal-convergence assumption is imported into this proof.
-/

namespace LeadingDigitHailstonePalomar

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
  have hstep' : ∀ i,
      2 ^ valuation i * state (LeadingDigitHailstone.cycleSucc hq i) =
        3 * state i + 2 * LeadingDigitHailstone.leadingDigit (state i) + 1 := by
    intro i
    rw [LeadingDigitHailstone.leadingDigit_eq_div_pow_log (state i) (hstatePos i)]
    simpa [LeadingDigitHailstone.cycleSucc] using hstep i
  apply LeadingDigitHailstone.leadingDigitCyclicPeriodLowerBound
    hq state valuation hstatePos hstateOdd hvaluationPos hstateInj
  · simpa [LeadingDigitHailstone.cycleMinimumFloor] using hmin
  · exact hstep'

#print axioms LeadingDigitHailstonePalomar.leadingDigitCyclePeriodLowerBound

end LeadingDigitHailstonePalomar
