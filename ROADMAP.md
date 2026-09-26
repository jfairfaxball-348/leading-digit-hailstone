# Research Programme Roadmap

The frozen object remains the positive-integer map

T(n) = n/2 for even n, and T(n) = 3n + 2L(n) + 1 for odd n,

where L(n) is the leading ordinary decimal digit. The central statement remains the unproved **Leading-Digit Hailstone Conjecture**: every positive integer eventually enters the distinguished cycle

1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1.

Historical novelty remains **UNRESOLVED_DO_NOT_CLAIM**.

## Stage 1 — Red-team / mathematical exploration — COMPLETE

**Status:** `COMPLETE_CONJECTURE_SURVIVES_DECLARED_STRESS_TEST`

Stage 1 was a bounded falsification and structural-research programme, not a requirement to prove universal convergence. The conjecture survived the declared programme: no competing positive cycle, tested escaping/cap-hit orbit, structural contradiction, implementation ambiguity, or need to change the positive-integer statement was found.

The closeout campaign is recorded in `notes/STAGE_1_STRESS_TEST_CLOSEOUT.md` and `data/final_stage1_stress_test.json`. It includes large random starts, much larger decimal-boundary adversaries, engineered long exact-v2=1 starts, inverse-tree-derived hostile residues, and an exact phase/residue challenge aimed at beating the observed post-lock tail record.

All trajectory outcomes remain finite computation. The absence of a counterexample in the declared campaign is not a proof.

Stage 1 also produced rigorous supporting mathematics that remains part of the project, including the exact accelerated cycle identity, the arbitrary-cycle consequence q>=971 under the established 5,000,000-seed minimum exclusion, the structured one-rise/one-fall restrictions q>=1,643,749,725,074 and a>=682,217,775,335 under the same premise, exact decimal/2-adic machinery, arbitrarily long initial exact-v2=1 runs, residue locking, deterministic post-lock reduction, the width-19 normalized corridor, sector/decade lemmas, and the terminally anchored guide.

Those results are supporting mathematics. They are not a ladder that must be pushed to infinity before the project can proceed.

## Stage 2 — Lean formalisation — NEXT PRIMARY STAGE

Primary objective:

> Consolidate and audit an exact, sorry-free formal specification of the frozen research object and its unproved central conjecture.

The Lean layer should clearly cover:

1. the positive-integer domain convention;
2. the decimal leading-digit function;
3. the frozen map T;
4. the distinguished 7-cycle;
5. iterates of T;
6. the Leading-Digit Hailstone Conjecture as an unproved proposition;
7. selected stable supporting lemmas proved during Stage 1.

Existing Lean work already contains much of this specification. Stage 2 should verify definitions, close specification gaps, organize theorem namespaces/files if useful, and ensure all retained lemmas are accurately stated and sorry-free. It should not turn the conjecture itself into a proof obligation.

## Stage 3 — Palomar — AFTER FORMALISATION

Do not infer or invent what Palomar means. When Stage 2 is complete, inspect repository/project conventions and available tooling before defining this stage's execution plan.

## Stage 4 — Final comprehensive novelty audit — AFTER PALOMAR

This is the stage where novelty must actually be resolved. The audit must search both exact and mathematically equivalent formulations across generalized Collatz/Syracuse systems, an+b and 3x+k maps, residue-class-wise affine maps, radix- and digit-dependent dynamics, leading-digit recurrences, automata/transducers, OEIS, theses, proceedings, books, historical bibliographies, code repositories, forums, recreational sources, and non-English or poorly indexed literature where practical.

The final assessment must separately address novelty of:

- the full map;
- the convergence conjecture;
- individual structural lemmas;
- the distinguished 7-cycle.

The distinguished cycle is already known 5x+1 behaviour and must not be presented as novel.

## Stage 5 — Research paper — AFTER FINAL NOVELTY AUDIT

A legitimate paper does not require a proof of universal convergence. Subject to the novelty audit, it may present the map, conjecture, computational census, adversarial falsification programme, nearby-rule comparisons, rigorous structural results and cycle restrictions, Lean specification, limitations, and open problems.

The manuscript must keep theorem, finite computation, heuristic observation, conjecture, literature fact, and novelty assessment clearly separated.

## Stage 6 — arXiv submission — FINAL PIPELINE STAGE

Submission follows only after a stable manuscript, final bibliography and novelty check, reproducible code/data, clean Lean state, and correct authorship/acknowledgements.

## Current research gate

- Pilot gate: **CANDIDATE_DISTINCTIVE_CONJECTURE**
- Stage 1: **COMPLETE_CONJECTURE_SURVIVES_DECLARED_STRESS_TEST**
- Current primary stage: **STAGE_2_LEAN_FORMALISATION**
- Novelty status: **UNRESOLVED_DO_NOT_CLAIM**
- Central conjecture: unchanged and explicitly unproved.

Future mathematical breakthroughs are welcome, but an open-ended universal-convergence proof attempt is no longer a prerequisite for progress through the research pipeline.
