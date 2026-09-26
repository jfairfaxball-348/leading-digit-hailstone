# Stage 1 Stress-Test Closeout — 2026-09-26

**Project gate:** `STAGE_1_STRESS_TEST_COMPLETE_CONJECTURE_SURVIVES`  
**Central statement:** still a `CONJECTURE`, not a theorem.  
**Novelty:** `UNRESOLVED_DO_NOT_CLAIM`.

Stage 1 is intentionally frozen after a declared falsification programme. The objective was to find a compelling reason not to keep the Leading-Digit Hailstone Conjecture as the central research conjecture. No such reason was found in the declared campaign. This is a research-programme stopping decision, not a proof of universal convergence.

## New finite adversarial campaign

The machine-readable certificate is `data/final_stage1_stress_test.json`, reproduced section-by-section by `scripts/final_stage1_stress_test.py`. All trajectory statements in this section are **FINITE EXACT COMPUTATION**.

### Large random odd starts

A deterministic sample used 50 random odd starts at each of 20, 50, 100, 250, 500, and 1000 decimal digits: 300 starts total, with a 200,000-step cap. Every tested start entered the distinguished cycle. The slowest took 25,426 raw steps. The sample also contained a 21-step consecutive accelerated `r=1` block and an accelerated valuation burst of 20.

### Decimal-boundary adversaries beyond the previous sweep

The previous exhaustive boundary family already covered all `d*10^k +/- 1` for `d=1..9`, `k<=500`. The closeout campaign moved to much larger scales: `k in {600,1000,1500}`, all digits at offsets `+/-1`, plus digits `1,5,9` at offsets `+/-9` and `+/-99`. All 90 starts entered the distinguished cycle within 100,000 raw steps.

The slowest was `5*10^1500-9`, which entered after 37,939 raw steps. The largest peak by decimal length occurred for `8*10^1500+1`, whose tested trajectory reached a 1504-digit value.

### Engineered long weak-division runs

Using the existing exact fixed-word residue construction based on the homogeneous phase `7/3`, new requested initial exact-`r=1` lengths were 150, 200, 256, and 384. The observed lengths were 150, 205, 259, and 384, respectively. All four hostile starts entered the distinguished cycle within the 200,000-step cap.

This strengthens the intended negative lesson: the conjecture is not surviving merely because exact-`r=1` growth streaks are short. Arbitrarily long such initial streaks are already a theorem-level fact; these new outcomes concern only the finite global fate of explicit hostile examples.

### Inverse-tree hostile residues

The distinguished cycle's exact inverse tree was expanded through raw depth 20. It contains 567 distinct nodes, including 127 odd nodes. Those odd nodes cover every odd residue modulo 64 but miss 13 odd residues modulo 128:

`7,17,29,43,45,51,53,55,67,85,91,111,123`.

Those shallow-coverage gaps were used only as a hostile seed generator. For each missing residue, one 50-, 100-, and 250-digit start was generated, giving 39 starts. All 39 entered the distinguished cycle. Lack of shallow inverse-tree coverage is not being interpreted as evidence of non-convergence.

### Post-lock tail challenge

A separate exact phase/residue challenge sampled 6,000 homogeneous phases: a dense `p/1000` grid for `1000<=p<=5999` plus 1,000 deterministic random phases with denominator `10^9`. Required exact-`r=1` residues were tested through phase-word prefixes of length 256.

No post-lock tail longer than 6 was found. The record was the already known start

`43,574,304,770,317,398,119`,

with bit-length lock depth 65, total initial exact-`r=1` run 71, post-lock tail 6, followed by valuation 7.

This is deliberately **not** promoted to a universal bound. The search is finite and non-exhaustive outside its declared phase family.

## Reused nearby-rule evidence

No major new nearby-rule campaign was run because the existing one-million-seed certificate already answers the intended sanity question. In the predeclared global-shift family, the frozen rule has one observed cycle through 1,000,000 while all four nonfrozen shifts have multiple observed cycles. However, several one-coordinate perturbations also remain single-attractor through 1,000,000. The honest conclusion remains: the frozen rule is behaviourally interesting in its tested neighborhood, but finite single-attractor behaviour is not unique to it.

## Conjecture-statement audit

No wording change is required. The intended domain is the positive integers; zero and signed extensions are outside the conjecture. `L(n)` is the first digit of the ordinary base-10 expansion, so leading zeroes are irrelevant. The independent string-based verifier agrees with the reference arithmetic implementation on large boundary cases included in the new tests.

## Rigorous mathematics retained from Stage 1

Stage 1 is frozen, not erased. The repository retains the useful exact mathematics developed during the proof-oriented exploration, including:

- the exact accelerated cycle identity and the arbitrary-cycle consequence `q>=971` under the 5,000,000-seed minimum exclusion;
- the one-rise/one-fall structured restriction `q>=1,643,749,725,074` and `a>=682,217,775,335` under the same premise;
- exact decimal-sector and 2-adic residue machinery;
- the theorem that arbitrarily long initial exact-`r=1` runs exist;
- residue-position locking and deterministic post-lock reduction;
- the width-19 forward normalized corridor;
- exact sector-exit and decade-crossing lemmas;
- the terminally anchored homogeneous guide from PR #19;
- finite counterexamples to simplistic auxiliary claims, including universal post-lock tail bounds `<=5`.

None of these is a proof of the central conjecture, and Stage 1 will not be extended merely to push the structured frontier farther.

## Declared exit gate

The ten declared conditions are treated as passed for the purpose of the research pipeline:

1. no competing positive cycle was found;
2. no tested orbit escaped or hit its declared cap;
3. no structural contradiction to the conjecture was found;
4. adversarial decimal-boundary families converged in every tested case;
5. engineered long weak-division starts converged in every tested case;
6. no implementation ambiguity was found;
7. existing nearby-rule comparisons still show nontrivial local behavioural contrast, with the important caveat that single-attractor behaviour is not unique;
8. the object retains substantial exact mathematical structure;
9. the conjecture remains simple and sharply stated;
10. computational evidence remains explicitly labelled finite computation.

Therefore the project status advances to:

`STAGE_1_STRESS_TEST_COMPLETE_CONJECTURE_SURVIVES`

This means only that the conjecture survived the declared falsification programme. It remains unproved.

## Next primary stage

The next primary stage is Lean formalisation of the frozen research object and conjecture. The existing Lean layer already contains the map, positive-domain convention, the conjecture as an unproved proposition, the distinguished cycle, and several stable lemmas. The formalisation stage should now consolidate and audit that specification rather than resume an open-ended convergence proof attempt.
