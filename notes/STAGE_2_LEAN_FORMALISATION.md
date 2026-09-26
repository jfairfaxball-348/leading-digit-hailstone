# Stage 2 — Lean Formalisation Audit

## Status

**COMPLETE_FORMAL_SPECIFICATION_AUDITED**

Stage 2 formalises and audits the frozen mathematical object. It does **not** prove universal convergence. The central statement remains an unproved proposition.

## Domain convention

The mathematical domain is the positive integers. Lean keeps the computational definitions total on `ℕ` and exposes

```lean
abbrev PositiveNat := {n : ℕ // 0 < n}
```

The value at zero is therefore an implementation totalisation, not part of the mathematical conjecture. In particular `leadingDigit 0 = 0`, while every statement interpreting `leadingDigit` as an ordinary decimal first digit assumes `0 < n`.

The frozen map preserves positivity:

```lean
theorem T_pos (n : ℕ) (hn : 0 < n) : 0 < T n
```

and is also available as the positive-domain wrapper

```lean
def TPositive (n : PositiveNat) : PositiveNat
```

The existing `Nat` convention was retained because it keeps computation and iteration simple while the positivity boundary is now explicit and formally checked.

## Decimal leading digit

The definition remains

```lean
def leadingDigit (n : ℕ) : ℕ :=
  if n = 0 then 0 else n / (10 ^ Nat.log 10 n)
```

For every positive `n`, Stage 2 now proves:

```lean
10 ^ Nat.log 10 n ≤ n
n < 10 ^ (Nat.log 10 n).succ
leadingDigit n = n / (10 ^ Nat.log 10 n)
0 < leadingDigit n
1 ≤ leadingDigit n
leadingDigit n < 10
leadingDigit n ≤ 9
```

These are consolidated by `leadingDigit_spec`. Thus `Nat.log 10 n` identifies the decimal decade containing `n`, and division by that power of ten is formally certified to produce a digit in `1,...,9`. The semantic justification no longer rests on `native_decide` examples.

## Frozen map

The definition is unchanged:

```lean
def T (n : ℕ) : ℕ :=
  if n % 2 = 0 then
    n / 2
  else
    3 * n + 2 * leadingDigit n + 1
```

The existing theorems `T_of_even` and `T_of_odd` continue to expose the two mathematical branches exactly. `T_pos` adds only the positive-domain closure property.

## Distinguished cycle and iterates

The cycle remains exactly

```lean
[1, 6, 3, 16, 8, 4, 2]
```

with the seven existing edge theorems and `distinguished_cycle_closes : (T^[7]) 1 = 1`.

Stage 2 also adds:

- `inDistinguishedCycle_iff`, giving explicit membership in the seven-element list;
- `T_mem_distinguishedCycle`, proving one-step invariance;
- `iterate_mem_distinguishedCycle`, proving invariance under every later iterate.

These are interface facts about the already verified cycle, not convergence claims.

## Central conjecture

The central proposition remains exactly:

```lean
def LeadingDigitHailstoneConjecture : Prop :=
  ∀ n : ℕ, 0 < n → ∃ k : ℕ, inDistinguishedCycle ((T^[k]) n)
```

This states that every positive natural has some finite iterate in the distinguished cycle. Because cycle membership is invariant under `T`, "eventually enters" has the intended dynamical meaning.

Stage 2 additionally proves only the equivalence of this formulation with the positive-subtype formulation:

```lean
theorem leadingDigitHailstoneConjecture_iff_positiveNat :
    LeadingDigitHailstoneConjecture ↔
      ∀ n : PositiveNat, ∃ k : ℕ,
        inDistinguishedCycle ((T^[k]) n.1)
```

This theorem does **not** prove either side.

## Supporting mathematics retained

The existing compact, proved Stage-1 lemmas in `Basic.lean` were retained without scope inflation, including:

- fixed-leading-digit odd affine form;
- correction bound conditional on `leadingDigit n ≤ 9`;
- elementary affine growth bounds;
- bounded congruence uniqueness;
- carry/valuation-one recurrence identities;
- sector-exit lemmas;
- six-step factor-ten growth;
- the rational backward homogeneous-gap identity.

A small interface theorem now derives the correction bound directly from positivity via `leadingDigit_le_nine`.

## Deliberately not formalised

Stage 2 does not translate the large finite census, adversarial campaigns, structured-cycle frontier, post-lock scan certificates, or other large exact computations wholesale into Lean. They remain reproducible finite-computation evidence with their existing certificates.

The stronger Stage-1 cycle restrictions and long-run constructions are also not made prerequisites for this formal-specification layer unless they already had compact, stable formal counterparts.

No attempt was made to prove universal convergence, construct a uniform post-lock bound, or continue the Stage-1 proof-search programme.

## Organisation

`LeadingDigitHailstone/Basic.lean` remains a single compact file. The audited layer is still small enough that splitting definitions, cycle facts, and elementary lemmas would add navigation overhead without improving mathematical clarity.

## Formal claim discipline

- No `sorry` is present.
- The central conjecture is a `Prop`, not an axiom or theorem.
- Universal convergence is neither assumed nor faked.
- Finite computations are not promoted to universal mathematics.
- Novelty remains **UNRESOLVED_DO_NOT_CLAIM**.
- The distinguished 7-cycle is known 5x+1 behaviour and is not claimed as novel.

## Stage-2 exit gate

The semantic specification, positive-domain convention, decimal leading-digit bounds, frozen map branches, cycle, iterates, and unproved conjecture are all represented explicitly. Stage 2 is complete once the final PR head has passed both repository CI workflows and is merged to `main`.

The next stage is Palomar. Its meaning, repository conventions, and available tooling must be inspected before that stage is defined or run.
