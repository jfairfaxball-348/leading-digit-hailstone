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

## Stage 2 — Lean formalisation — NEXT PRIMARY STAGE

The next primary task is to consolidate and audit the formal specification of the research object.

Lean should clearly and sorry-freely expose:

1. the positive-integer domain convention;
2. decimal leading digit;
3. the frozen map T;
4. the distinguished 7-cycle;
5. iterates of T;
6. the Leading-Digit Hailstone Conjecture as an **unproved proposition**;
7. selected stable supporting lemmas already established mathematically.

The conjecture is not to be asserted as a theorem and no placeholder proof is permitted.

A substantial base already exists in LeadingDigitHailstone/Basic.lean; Stage 2 should audit completeness, interfaces and exact agreement with the frozen mathematical statement rather than reopening Stage 1 proof research.

## Stage 3 — Palomar — AFTER FORMALISATION

Do not infer what Palomar means from the name. When Stage 2 is complete, inspect repository/project conventions and available tooling before defining and running this stage.

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
- Current primary stage: **STAGE_2_LEAN_FORMALISATION**
- Novelty status: **UNRESOLVED_DO_NOT_CLAIM**
- Central conjecture: **CONJECTURE — UNPROVED**

Future proof advances remain welcome, but they are no longer prerequisites for moving the research pipeline forward.
