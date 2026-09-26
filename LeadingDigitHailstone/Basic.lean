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

theorem odd_maps_to_even (n : ℕ) (hodd : n % 2 = 1) : T n % 2 = 0 := by
  rw [T_of_odd n hodd]
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
