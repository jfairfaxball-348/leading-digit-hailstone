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

Current highest-value target: **Issue #10 — control post-lock zero-lift tails**. Exact Farey record transfer plus complete symbolic certificates exclude one-rise/one-fall periods through q=890,638,885,192 under the 5M minimum premise. The residue side is now sharper: for starts M<=U, at B=floor(log_2 U) the exact residue congruence locks M to the canonical residue itself, and every later compatible binary lift bit must be zero. Together with finite-range decimal-boundary localization this compresses the candidates surviving to B to an explicit O((log U)^2) bound for fixed lower endpoint. What remains unproved is a uniform bound on how long those locked starts can continue selecting zero lifts. Prove such a zero-lift-tail theorem, or isolate a rigorous family preventing it. Further Farey-record extension is secondary unless needed to test that theorem.

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
