import Mathlib.Data.Nat.Log
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic

namespace LeadingDigitHailstone

/-- Positive naturals are the intended mathematical domain. -/
abbrev PositiveNat := {n : ℕ // 0 < n}

/-- Decimal leading digit, totalized by leadingDigit 0 = 0.
For positive n this is the first digit of the ordinary base-10 expansion. -/
def leadingDigit (n : ℕ) : ℕ :=
  if n = 0 then 0 else n / (10 ^ Nat.log 10 n)

/-- The frozen Leading-Digit Hailstone map. -/
def T (n : ℕ) : ℕ :=
  if n % 2 = 0 then
    n / 2
  else
    3 * n + 2 * leadingDigit n + 1

def distinguishedCycle : List ℕ := [1, 6, 3, 16, 8, 4, 2]

def inDistinguishedCycle (n : ℕ) : Prop :=
  n ∈ distinguishedCycle

/-- The central conjecture is specified as a proposition, not asserted as a theorem. -/
def LeadingDigitHailstoneConjecture : Prop :=
  ∀ n : ℕ, 0 < n → ∃ k : ℕ, inDistinguishedCycle ((T^[k]) n)

/-- The even branch simplifies exactly to division by two. -/
theorem T_of_even (n : ℕ) (heven : n % 2 = 0) : T n = n / 2 := by
  simp [T, heven]

/-- The odd branch simplifies exactly to the leading-digit affine rule. -/
theorem T_of_odd (n : ℕ) (hodd : n % 2 = 1) :
    T n = 3 * n + 2 * leadingDigit n + 1 := by
  have hne : n % 2 ≠ 0 := by omega
  simp [T, hne]

/-- On a fixed leading-digit sector, the odd branch is affine with constant correction. -/
theorem T_of_odd_leadingDigit (n d : ℕ) (hodd : n % 2 = 1)
    (hld : leadingDigit n = d) :
    T n = 3 * n + 2 * d + 1 := by
  rw [T_of_odd n hodd, hld]

/-- The odd-branch additive correction is at most 19 once the leading digit is known to be at most 9. -/
theorem odd_correction_le_nineteen (n : ℕ) (hld : leadingDigit n ≤ 9) :
    2 * leadingDigit n + 1 ≤ 19 := by
  omega

/-- The odd affine numerator is always strictly larger than twice the input. -/
theorem odd_affine_gt_two_mul (n : ℕ) :
    2 * n < 3 * n + 2 * leadingDigit n + 1 := by
  omega

/-- Above 19, a leading digit at most 9 makes the odd affine numerator strictly less than four times the input. -/
theorem odd_affine_lt_four_mul (n : ℕ) (hlarge : 19 < n)
    (hld : leadingDigit n ≤ 9) :
    3 * n + 2 * leadingDigit n + 1 < 4 * n := by
  omega

theorem odd_maps_to_even (n : ℕ) (hodd : n % 2 = 1) : T n % 2 = 0 := by
  rw [T_of_odd n hodd]
  omega

/-- Two values below the same positive modulus are equal once their residues
modulo that modulus agree. This is the formal core used by bounded-range
residue locking. -/
theorem bounded_congruence_unique (a b modulus : ℕ)
    (ha : a < modulus) (hb : b < modulus)
    (hres : a % modulus = b % modulus) : a = b := by
  rw [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at hres
  exact hres

/-- Writing an odd state as x = 2H+1 turns one valuation-one affine
halving into the post-lock carry/state recurrence. -/
theorem odd_affine_half_from_carry (H d : ℕ) :
    (3 * (2 * H + 1) + 2 * d + 1) / 2 = 3 * H + d + 2 := by
  omega

/-- For x = 2H+1, exact valuation one of the odd affine numerator is
equivalent to the post-lock zero-lift parity H+d odd. -/
theorem exact_one_halving_mod_four_iff (H d : ℕ) :
    (3 * (2 * H + 1) + 2 * d + 1) % 4 = 2 ↔
      (H + d) % 2 = 1 := by
  omega

/-- Under the valuation-one parity, the next odd state is again one plus
twice the next carry. -/
theorem next_state_is_twice_next_carry_plus_one (H d : ℕ)
    (hr1 : (3 * (2 * H + 1) + 2 * d + 1) % 4 = 2) :
    (3 * (2 * H + 1) + 2 * d + 1) / 2 =
      2 * ((1 + 3 * H + d) / 2) + 1 := by
  omega

/-- In any fixed decimal sector with leading digit d >= 2, one
valuation-one affine halving already reaches the next sector boundary.
The scale parameter can be any natural number; decimal applications use
scale = 10^k. -/
theorem affine_half_exits_nonone_sector (x d scale : ℕ)
    (hdlo : 2 ≤ d) (hdhi : d ≤ 9) (hx : d * scale ≤ x) :
    (d + 1) * scale ≤ (3 * x + 2 * d + 1) / 2 := by
  interval_cases d <;> omega

/-- In the leading-digit-one sector, two repeated affine halvings with
correction 3 necessarily reach the next sector boundary. Hence digit 1
can occur as the source digit of at most two consecutive valuation-one
steps within one decimal decade. -/
theorem affine_half_twice_exits_one_sector (x scale : ℕ)
    (hx : scale ≤ x) :
    2 * scale ≤
      (3 * ((3 * x + 3) / 2) + 3) / 2 := by
  omega

theorem cycle_1_to_6 : T 1 = 6 := by native_decide
theorem cycle_6_to_3 : T 6 = 3 := by native_decide
theorem cycle_3_to_16 : T 3 = 16 := by native_decide
theorem cycle_16_to_8 : T 16 = 8 := by native_decide
theorem cycle_8_to_4 : T 8 = 4 := by native_decide
theorem cycle_4_to_2 : T 4 = 2 := by native_decide
theorem cycle_2_to_1 : T 2 = 1 := by native_decide

theorem distinguished_cycle_closes : (T^[7]) 1 = 1 := by native_decide

example : leadingDigit 7 = 7 := by native_decide
example : leadingDigit 16 = 1 := by native_decide
example : leadingDigit 4_625_895 = 4 := by native_decide

end LeadingDigitHailstone
