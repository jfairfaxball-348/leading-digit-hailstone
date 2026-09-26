import Mathlib
import LeadingDigitHailstone.Basic
import LeadingDigitHailstone.CyclePeriodBound

namespace LeadingDigitHailstone

open Finset BigOperators

set_option maxHeartbeats 4000000
set_option exponentiation.threshold 100000000


/-- Cyclic successor on the q indexed odd states of a nonempty periodic orbit. -/
def cycleSucc {q : ℕ} (hq : 0 < q) (i : Fin q) : Fin q :=
  ⟨(i.val + 1) % q, Nat.mod_lt _ hq⟩

/-- Cyclic successor is a permutation of the finite orbit positions. -/
theorem cycleSucc_bijective (q : ℕ) (hq : 0 < q) :
    Function.Bijective (fun i : Fin q => cycleSucc hq i) := by
  constructor
  · intro i j
    simp +decide [cycleSucc]
    exact fun h => Fin.ext <|
      Nat.mod_eq_of_lt i.2 ▸ Nat.mod_eq_of_lt j.2 ▸
        (by simpa [← ZMod.natCast_eq_natCast_iff'] using h)
  · intro i
    use ⟨(i + q - 1) % q, Nat.mod_lt _ hq⟩
    simp +decide [Fin.ext_iff, cycleSucc]
    rw [Nat.sub_add_cancel (by linarith [Fin.is_lt i])]
    simp +decide [Nat.mod_eq_of_lt]

/-- Cyclic successor packaged as an equivalence for product reindexing. -/
def cycleSuccEquiv {q : ℕ} (hq : 0 < q) : Equiv.Perm (Fin q) :=
  Equiv.ofBijective (fun i : Fin q => cycleSucc hq i) (cycleSucc_bijective q hq)

/-- A finite accelerated affine cycle with corrections in the decimal
leading-digit range.  The successor is supplied as a permutation because the
product argument only needs cyclic reindexing; an ordinary q-cycle is a
special case. -/
theorem boundedCorrectionCyclePeriodLowerBound
    {q : ℕ}
    (hq : 0 < q)
    (state valuation correction : Fin q → ℕ)
    (next : Equiv.Perm (Fin q))
    (hstatePos : ∀ i, 0 < state i)
    (hmin : ∀ i, cycleMinimumFloor ≤ state i)
    (hcorrLower : ∀ i, 3 ≤ correction i)
    (hcorrUpper : ∀ i, correction i ≤ cycleCorrectionCeiling)
    (hstep : ∀ i,
      2 ^ valuation i * state (next i) =
        3 * state i + correction i) :
    971 ≤ q := by
  let R : ℕ := ∑ i : Fin q, valuation i
  let P : ℕ := ∏ i : Fin q, state i

  have hnext :
      (∏ i : Fin q, state (next i)) = P := by
    dsimp [P]
    exact Equiv.prod_comp next state

  have hpows :
      (∏ i : Fin q, (2 : ℕ) ^ valuation i) = 2 ^ R := by
    dsimp [R]
    simpa using (Finset.prod_pow_eq_pow_sum Finset.univ valuation (2 : ℕ))

  have hprodIdentity :
      (∏ i : Fin q, (3 * state i + correction i)) =
        2 ^ R * P := by
    calc
      (∏ i : Fin q, (3 * state i + correction i))
          = ∏ i : Fin q, (2 ^ valuation i * state (next i)) := by
              apply Finset.prod_congr rfl
              intro i hi
              exact (hstep i).symm
      _ = (∏ i : Fin q, 2 ^ valuation i) *
            (∏ i : Fin q, state (next i)) := by
              rw [Finset.prod_mul_distrib]
      _ = 2 ^ R * P := by rw [hpows, hnext]

  have hprodPos : 0 < P := by
    dsimp [P]
    exact Finset.prod_pos (fun i hi => hstatePos i)

  have hlowerProducts :
      (∏ i : Fin q, 3 * state i) <
        ∏ i : Fin q, (3 * state i + correction i) := by
    apply Finset.prod_lt_prod_of_nonempty₀
    · intro i hi
      exact Nat.mul_pos (by norm_num) (hstatePos i)
    · intro i hi
      have hc := hcorrLower i
      omega
    · exact ⟨⟨0, hq⟩, Finset.mem_univ _⟩

  have hlowerScaled :
      (3 : ℕ) ^ q * P < 2 ^ R * P := by
    calc
      (3 : ℕ) ^ q * P
          = ∏ i : Fin q, 3 * state i := by
              dsimp [P]
              rw [Finset.prod_mul_distrib, Finset.prod_const, Finset.card_fin]
      _ < ∏ i : Fin q, (3 * state i + correction i) := hlowerProducts
      _ = 2 ^ R * P := hprodIdentity

  have hlower : (3 : ℕ) ^ q < 2 ^ R :=
    (Nat.mul_lt_mul_right hprodPos).mp hlowerScaled

  have hfactorUpper :
      ∀ i : Fin q,
        (3 * state i + correction i) * cycleMinimumFloor ≤
          state i * (3 * cycleMinimumFloor + cycleCorrectionCeiling) := by
    intro i
    have hcA :
        correction i * cycleMinimumFloor ≤
          cycleCorrectionCeiling * state i :=
      Nat.mul_le_mul (hcorrUpper i) (hmin i)
    nlinarith

  have hupperProducts :
      (∏ i : Fin q,
        ((3 * state i + correction i) * cycleMinimumFloor)) ≤
      ∏ i : Fin q,
        (state i * (3 * cycleMinimumFloor + cycleCorrectionCeiling)) := by
    apply Finset.prod_le_prod₀
    · intro i hi
      positivity
    · intro i hi
      exact hfactorUpper i

  have hupperScaled :
      (2 ^ R * P) * cycleMinimumFloor ^ q ≤
        P * (3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q := by
    calc
      (2 ^ R * P) * cycleMinimumFloor ^ q
          = (∏ i : Fin q, (3 * state i + correction i)) *
              cycleMinimumFloor ^ q := by rw [hprodIdentity]
      _ = ∏ i : Fin q,
            ((3 * state i + correction i) * cycleMinimumFloor) := by
              rw [Finset.prod_mul_distrib, Finset.prod_const, Finset.card_fin]
      _ ≤ ∏ i : Fin q,
            (state i * (3 * cycleMinimumFloor + cycleCorrectionCeiling)) :=
              hupperProducts
      _ = P * (3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q := by
              dsimp [P]
              rw [Finset.prod_mul_distrib, Finset.prod_const, Finset.card_fin]

  have hupperCommon :
      P * (2 ^ R * cycleMinimumFloor ^ q) ≤
        P * (3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q := by
    simpa [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using hupperScaled

  have hupper :
      2 ^ R * cycleMinimumFloor ^ q ≤
        (3 * cycleMinimumFloor + cycleCorrectionCeiling) ^ q := by
    exact Nat.le_of_mul_le_mul_left hupperCommon hprodPos

  exact periodLowerBound_of_productWindow hq hlower hupper

/-- Specialization to the actual Leading-Digit Hailstone accelerated odd-step
numerators.  The only map-specific input is that a positive decimal leading
digit lies in 1..9, hence the correction 2L(n)+1 lies in 3..19. -/
theorem leadingDigitCyclePeriodLowerBound
    {q : ℕ}
    (hq : 0 < q)
    (state valuation : Fin q → ℕ)
    (next : Equiv.Perm (Fin q))
    (hstatePos : ∀ i, 0 < state i)
    (hmin : ∀ i, cycleMinimumFloor ≤ state i)
    (hstep : ∀ i,
      2 ^ valuation i * state (next i) =
        3 * state i + 2 * leadingDigit (state i) + 1) :
    971 ≤ q := by
  let correction : Fin q → ℕ :=
    fun i => 2 * leadingDigit (state i) + 1
  apply boundedCorrectionCyclePeriodLowerBound
    hq state valuation correction next hstatePos hmin
  · intro i
    have hld := one_le_leadingDigit (state i) (hstatePos i)
    dsimp [correction]
    omega
  · intro i
    dsimp [correction]
    exact odd_correction_le_nineteen_of_pos (state i) (hstatePos i)
  · intro i
    simpa [correction, Nat.add_assoc] using hstep i


/-- Cycle-facing specialization with the hypotheses that make `q` the number
of distinct odd positions in one accelerated periodic orbit.  Oddness,
positive valuation exponents and injective state indexing are explicit even
though the product/Farey argument itself only needs positivity, the minimum
floor and the exact step equations. -/
theorem leadingDigitCyclicPeriodLowerBound
    {q : ℕ}
    (hq : 0 < q)
    (state valuation : Fin q → ℕ)
    (hstatePos : ∀ i, 0 < state i)
    (hstateOdd : ∀ i, state i % 2 = 1)
    (hvaluationPos : ∀ i, 0 < valuation i)
    (hstateInj : Function.Injective state)
    (hmin : ∀ i, cycleMinimumFloor ≤ state i)
    (hstep : ∀ i,
      2 ^ valuation i * state (cycleSucc hq i) =
        3 * state i + 2 * leadingDigit (state i) + 1) :
    971 ≤ q := by
  let next : Equiv.Perm (Fin q) := cycleSuccEquiv hq
  apply leadingDigitCyclePeriodLowerBound
    hq state valuation next hstatePos hmin
  intro i
  simpa [next, cycleSuccEquiv] using hstep i

end LeadingDigitHailstone
