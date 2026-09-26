# Research Programme Roadmap

The conjecture-discovery pilot is complete. The project gate remains **CANDIDATE_DISTINCTIVE_CONJECTURE**: the frozen object is sufficiently substantive to justify a full mathematical programme, while historical novelty remains unresolved.

The project is now organized as a staged research programme. These stages are not a one-way checklist: mathematical counterexamples, formalisation failures, or prior-art discoveries may send the work back to an earlier stage.

## Stage 1 — Mathematical proof / conjecture research — ACTIVE

Primary objective:

> Determine as much rigorous mathematics as possible about the frozen dynamical system, while continuously attempting to falsify or sharpen the universal-convergence conjecture.

Legitimate outcomes include a proof, a substantial partial theorem, exclusion of important counterexample classes, a stronger invariant, another cycle, an escaping orbit, a corrected conjecture, or a rigorous obstruction to a natural proof strategy.

Current parallel attack lines:

1. accelerated odd dynamics and deterministic descent mechanisms;
2. positive-cycle exclusion via valuation words, leading-digit words, and exact cycle identities;
3. inverse dynamics and inverse-tree coverage;
4. decimal-sector geometry and boundary crossing;
5. computation used only for theorem discovery and targeted falsification.

The theorem that arbitrarily long initial exact-v2=1 runs exist permanently rules out arguments that assume a uniform bound on weak-division streaks.

Current highest-value target: **Issue #10 — bound deterministic post-lock tails by scale**. Post-lock dynamics now has two complementary width-19 coordinates. Forward from a lock state X, (2/3)^t x_t stays inside a fixed normalized corridor above X. For any fixed finite exact-r=1 segment x_0,...,x_N, the terminally anchored guide g_s=x_N(2/3)^(N-s) stays within absolute distance 19 above every earlier x_s. Both coordinates localize possible decimal-itinerary disagreement to explicit width-19 boundary windows. Local geometry is also rigid: sectors with leading digit >=2 are exited in one r=1 step, the digit-1 sector supplies at most two consecutive source states, and six r=1 steps cross a power-of-ten boundary. These are theorem-level facts, but not a tail bound. A complete exact own-bit lock scan through B=220 finds 96 locked starts, 41 positive post-lock tails, maximum observed tail 6, and no forward-corridor decimal-boundary hit or homogeneous-digit disagreement in any positive tail; this is finite computation only. The sharper missing theorem is therefore scale-aware parity/congruence control along a phase-frozen homogeneous digit itinerary, or a rigorous family showing such control cannot give a useful F(B) or F(M). The one-rise/one-fall frontier remains q>=1,643,749,725,074 and a>=682,217,775,335 under the 5M premise; further Farey-record extension remains secondary.

## Stage 2 — Lean formalisation — ACTIVE ALONGSIDE STAGE 1

Formalisation proceeds with the mathematics rather than after it.

Keep separate:

- exact definitions/specification;
- elementary proved lemmas;
- substantial proved mathematics;
- finite computational statements;
- the unproved central conjecture.

Priorities are leading-digit interval lemmas, branch simplification theorems, fixed-leading-digit affine form, 2-adic congruence statements, decimal-boundary lemmas, inverse-image lemmas, accelerated-map definitions, the cycle equation, and stable Stage-1 theorems.

The universal conjecture remains a Prop. No sorry placeholders are permitted merely to simulate progress. Lean CI must remain green.

## Stage 3 — Final comprehensive prior-art audit — ACTIVE IN PARALLEL, NOT FINAL

The pilot audit is substantial but not a novelty determination.

Before any historical novelty or priority claim, search exact and mathematically equivalent descriptions across generalized Collatz/Syracuse literature, an+b and 3x+k systems, RCWA and periodically linear maps, state-dependent piecewise-affine maps, radix/digit dynamics, leading-digit rules, automata/transducers, OEIS, bibliographies, theses, books, proceedings, recreational sources, forums, code repositories, and non-English/poorly indexed literature where practical.

Classify plausible sources as exact match, equivalent formulation, direct superclass, close analogue, thematic only, or irrelevant.

The final assessment must distinguish novelty of the map, the universal-convergence conjecture, individual structural theorems, and the distinguished 7-cycle. The cycle is already known 5x+1 prior art.

## Stage 4 — Palomar — NOT STARTED

Do not infer or invent the meaning of Palomar. Inspect repository/project conventions or tooling when this stage becomes timely.

Entry conditions include stable definitions, numbered theorem/conjecture inventory, reproducible evidence, clean bibliographic records, explicit open questions, and machine-checkable formal statements where practical.

## Stage 5 — Research paper — NOT STARTED

Do not begin manuscript packaging while major mathematical or novelty questions remain unresolved.

A future manuscript should clearly separate definitions, theorems, conjectures, finite computation, heuristics, literature facts, and novelty claims. It should be a mathematical research paper rather than a computation-only note.

## Stage 6 — arXiv submission — NOT STARTED

Submission is the end of the pipeline, not a target driving the mathematics.

Prerequisites include a stable paper, complete bibliography, reproducible repository, explicit computational protocols, accurate Lean status, appropriate authorship/acknowledgements, and a final prior-art check with no unsupported novelty language.

## Current research gate

- Pilot gate: **CANDIDATE_DISTINCTIVE_CONJECTURE**
- Current phase: **STAGE_1_MATHEMATICAL_RESEARCH**
- Novelty status: **UNRESOLVED_DO_NOT_CLAIM**
- Central conjecture: unchanged and explicitly unproved.

The immediate programme is to deepen the mathematics and try to break the conjecture, not to rush toward publication packaging.

**Boundary-separation follow-up:** two distinct scaled decimal-boundary hits inside the post-lock width-19 corridor, separated by `n` steps, force `X<=171*3^n`; exact coincidences are limited to the short chains `2->3` and `4->6->9`. Hence long boundary-free blocks have a forced homogeneous digit word, and survival of such a block reduces to one terminal 2-adic residue congruence. The next target is to bound the length of these phase-frozen congruence-compatible blocks by scale.
