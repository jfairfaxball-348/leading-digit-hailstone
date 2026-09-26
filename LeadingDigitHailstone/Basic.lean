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

/-- Any positive-correction affine halving grows by strictly more than the
homogeneous factor 3/2. -/
theorem affine_half_strict_growth (x y correction : ℕ)
    (hstep : 2 * y = 3 * x + correction)
    (hcorrection : 0 < correction) :
    3 * x < 2 * y := by
  omega

/-- If a decimal-style sector has lower endpoint at least twice its width,
one positive-correction affine halving exits the sector upward.  For
[d*10^k,(d+1)*10^k), this applies to every d >= 2. -/
theorem affine_half_exits_wide_sector
    (x y lower width correction : ℕ)
    (hstep : 2 * y = 3 * x + correction)
    (hcorrection : 0 < correction)
    (hx : lower ≤ x)
    (hwide : 2 * width ≤ lower) :
    lower + width < y := by
  omega

/-- Two consecutive digit-one valuation-one affine steps leave the
digit-one sector [scale,2*scale). -/
theorem two_digit_one_halvings_exit_sector
    (x y z scale : ℕ)
    (hxy : 2 * y = 3 * x + 3)
    (hyz : 2 * z = 3 * y + 3)
    (hx : scale ≤ x) :
    2 * scale < z := by
  omega

/-- Six successive steps each growing strictly faster than 3/2 increase
the state by more than a factor ten. -/
theorem six_three_halves_growth_steps_cross_factor_ten
    (x0 x1 x2 x3 x4 x5 x6 : ℕ)
    (h01 : 3 * x0 < 2 * x1)
    (h12 : 3 * x1 < 2 * x2)
    (h23 : 3 * x2 < 2 * x3)
    (h34 : 3 * x3 < 2 * x4)
    (h45 : 3 * x4 < 2 * x5)
    (h56 : 3 * x5 < 2 * x6) :
    10 * x0 < x6 := by
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
