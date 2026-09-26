# Pilot Roadmap

## Task 0 — Scaffold

Create the research rules, status schema, exact definition, two implementations, regression tests, reproducible scripts, and machine-readable data conventions.

**Exit condition:** repository can execute and cross-check the frozen map without ambiguity.

## Task 1 — Independent reproduction

Re-run the incoming sweep through `10^6`, verify the two named record seeds, and run a new deterministic 1,000-sample experiment for 10–200 digit starts because the original random sample is not exactly replayable from the supplied information.

**Exit condition:** exact claims are either reproduced, contradicted, or explicitly marked non-replayable.

## Task 2 — Dynamical census

Extend exhaustive testing substantially beyond `10^6`; catalogue cycle-entry time records, first-descent records, maximum excursions, excursion ratios, cap hits, and leading-digit boundary effects. Use checkpoints for large runs.

## Task 3 — Structural decomposition

Develop exact elementary results for parity, `v2(3n+2L(n)+1)`, fixed-leading-digit intervals, decimal-boundary transitions, the accelerated odd-to-odd map, and inverse images.

## Task 4 — Cycle search

Use both forward enumeration and inverse constraints to find or exclude bounded nontrivial cycles. Any exclusion must state its exact bound and assumptions.

## Task 5 — Prior-art audit

Search generalized `an+b` and piecewise affine Collatz maps, residue-class-dependent maps, digit-dependent arithmetic dynamical systems, digit-sum/reversal dynamics, and leading-digit/Benford work around classical Collatz. Search for mathematical equivalence, not just the literal formula.

## Task 6 — Pilot decision

Choose exactly one gate value:

- `STOP_TRIVIAL`
- `STOP_PRIOR_ART`
- `STOP_UNINTERESTING`
- `CONTINUE_COMPUTATIONAL`
- `CONTINUE_STRUCTURAL`
- `CONTINUE_PROOF_TARGET`

No paper/priority/formalisation programme begins before this gate is documented with reasons.
