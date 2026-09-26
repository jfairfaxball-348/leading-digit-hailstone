# Research Programme Roadmap

The frozen object remains the positive-integer map

T(n) = n/2 for even n, and T(n) = 3n + 2L(n) + 1 for odd n,

where L(n) is the leading ordinary decimal digit.

The central statement remains the unproved **Leading-Digit Hailstone Conjecture**: every positive integer eventually enters

1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1.

Historical novelty remains **UNRESOLVED_DO_NOT_CLAIM**. The distinguished cycle is known 5x+1 behavior and is not novel.

## Stage 1 — Red-team / mathematical exploration — COMPLETE

**Status:** COMPLETE_CONJECTURE_SURVIVES_DECLARED_STRESS_TEST

Stage 1 is intentionally frozen. Its purpose was to stress-test the conjecture, search for counterexamples and pathological behavior, and preserve worthwhile rigorous mathematics discovered in the process. It was not a requirement to prove a Collatz-adjacent universal convergence statement.

The final bounded red-team increment adds:

- 756 exact multi-offset decimal-boundary starts at exponents 600 through 2000;
- 350 deterministic large random odd starts at 20 through 2000 decimal digits;
- 1,476 inverse-tree-derived hostile starts from sparse depth-45 frontier points;
- residue-engineered starts requesting 150, 300, 500, 750 and 1000 initial valuation-one accelerated steps;
- an exact extension of the complete own-bit post-lock diagnostic from B <= 220 through B <= 300, with no tail longer than the previously observed record 6;
- the elementary family n = 2*10^k - 1, whose odd-branch valuation is exactly k+1, proving that single valuation bursts are unbounded.

Every trajectory outcome above is finite computation over its declared protocol. None proves universal convergence.

Existing supporting mathematics remains part of the project, including:

- arbitrary competing accelerated cycles must satisfy q >= 971, conditional on the established exhaustive 5,000,000-seed minimum exclusion;
- for the structured one-rise/one-fall class under the same premise, q >= 1,643,749,725,074 and a >= 682,217,775,335;
- exact residue locking and deterministic post-lock reduction;
- the width-19 normalized corridor and terminally anchored guide;
- arbitrarily long initial exact-v2=1 runs;
- the exact tail-6 counterexample to proposed universal post-lock bounds <= 5.

These are supporting results, not unfinished obligations that must be pushed to infinity.

See notes/STAGE_1_FINAL_STRESS_TEST.md for the exit-gate assessment.

## Stage 2 — Lean formalisation — COMPLETE

Stage 2 consolidated and audited the formal specification of the research object.

Lean should clearly and sorry-freely expose:

1. the positive-integer domain convention;
2. decimal leading digit;
3. the frozen map T;
4. the distinguished 7-cycle;
5. iterates of T;
6. the Leading-Digit Hailstone Conjecture as an **unproved proposition**;
7. selected stable supporting lemmas already established mathematically.

The conjecture is not to be asserted as a theorem and no placeholder proof is permitted.

The completed audit retains the compact single-file organisation in LeadingDigitHailstone/Basic.lean. It formally certifies the positive-domain convention; decimal-scale and 1..9 leading-digit semantics; exact even/odd map branches; positivity preservation; the exact distinguished cycle and its one-step/iterate invariance; and equivalence of the Nat-plus-positivity and PositiveNat formulations of the central unproved proposition. Existing stable affine/post-lock lemmas are retained without accidental strengthening. See notes/STAGE_2_LEAN_FORMALISATION.md.

## Stage 3 — Palomar — INITIAL MECHANICAL PASS; EDITORIAL REJECTION RECORDED

The immutable Stage-3 snapshot `f3309bd7d47da7cc3f1a12119aea8022b8f6c98a`
passed Palomar's full mechanical verifier. The subsequent automated editorial
review rejected registration because the sole selected theorem
`valuationBurstFamily` was an elementary substitution whose research interest
had not been established. The failed attempt is part of project history and
must not be erased or rewritten.

## Stage 3B — Palomar editorial remediation — ACTIVE

The remediation target is the conditional arbitrary-cycle restriction:
every positive accelerated Leading-Digit Hailstone periodic orbit whose odd
states are all at least 5,000,001 has at least 971 odd states.

The Lean proof must kernel-check the theorem itself. The 5,000,000-seed census
is not imported as a theorem or axiom; instead the minimum threshold is exposed
as a hypothesis. The proof uses the exact cyclic product identity, the
correction bound 3..19, the resulting product window, exact power comparisons,
and a Farey-neighbour denominator gap. The much larger structured
one-rise/one-fall frontier remains outside the selected theorem because its
headline currently depends on extensive Python-only finite certificates.

Historical novelty remains unresolved. A targeted theorem-specific literature
audit is required before the replacement snapshot is frozen, followed by
ordinary CI and the current official Palomar full predictive preflight.
Manual registration remains an owner action.

## Stage 4 — Final comprehensive novelty / prior-art audit — AFTER PALOMAR

This is the stage where historical novelty must actually be resolved.

Search exact and mathematically equivalent formulations across:

- generalized Collatz/Syracuse systems;
- an+b and 3x+k systems;
- residue-class-wise affine maps;
- radix- and digit-dependent integer dynamics;
- leading-digit-dependent recurrences;
- automata/transducer integer dynamics;
- OEIS and sequence databases;
- theses, proceedings, books and bibliographies;
- recreational sources, forums and code repositories;
- poorly indexed and non-English literature where practical.

The final assessment must separately evaluate novelty of:

- the full map;
- the convergence conjecture;
- individual structural lemmas;
- the distinguished 7-cycle.

The 7-cycle is already known 5x+1 prior art. Until this audit is complete, novelty status remains UNRESOLVED_DO_NOT_CLAIM.

## Stage 5 — Research paper — AFTER FINAL NOVELTY AUDIT

A paper does **not** require a proof of the universal convergence conjecture.

If novelty and scholarly checks support publication, a legitimate paper may present the frozen map, central conjecture, exhaustive and adversarial finite testing, nearby-rule comparisons, rigorous structural mathematics, restrictions on hypothetical competing cycles, the Lean formal specification, explicit limitations, and open problems.

The manuscript must distinguish definitions, theorems, formal theorems, finite computation, heuristics, conjectures, literature facts and novelty assessments.

## Stage 6 — arXiv submission — AFTER PAPER READINESS

Submission is appropriate only after a stable manuscript, final bibliography, reproducible code and compact certificates, clean Lean state, correct authorship/acknowledgements, and a completed final novelty check.

## Current programme gate

- Pilot gate: **CANDIDATE_DISTINCTIVE_CONJECTURE**
- Stage 1: **COMPLETE_CONJECTURE_SURVIVES_DECLARED_STRESS_TEST**
- Stage 2: **COMPLETE_FORMAL_SPECIFICATION_AUDITED**
- Current primary stage: **STAGE_3B_PALOMAR_EDITORIAL_REMEDIATION**
- Novelty status: **UNRESOLVED_DO_NOT_CLAIM**
- Central conjecture: **CONJECTURE — UNPROVED**

Future proof advances remain welcome, but they are no longer prerequisites for moving the research pipeline forward.
