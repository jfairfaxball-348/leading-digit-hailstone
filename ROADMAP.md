# Conjecture-Discovery Roadmap

This project is not gated on proof readiness. Its purpose is to decide whether the frozen rule supports a worthwhile, distinctive, and plausibly novel Collatz-adjacent conjecture.

## Tasks

### 0 — Scaffold and exact reproduction
Freeze the object, implement it independently twice, reproduce incoming finite claims, and make all finite evidence reproducible.

### 1 — Finite census and adversarial testing
Extend exact finite testing, but prioritize falsification: competing cycles, decimal boundaries, long first descents, high excursions, low-v2 growth, inverse searches, and constructed large starts.

### 2 — Structural mathematics
Record elementary exact facts about decimal sectors, parity, 2-adic valuation, inverse images, accelerated cycles, and boundary jumps. Structural work is valuable because it diagnoses whether the object is mathematically substantive, not because a proof is required.

### 3 — Prior-art audit
Search for exact and equivalent constructions across generalized Collatz maps, state-dependent and piecewise-affine maps, radix/digit dynamics, automata/transducers, OEIS, papers, theses, recreational sources, repositories, MathOverflow/Math StackExchange, and older bibliographies.

Classify every serious candidate as: exact match; equivalent formulation; direct superclass containing the object essentially for free; close analogue; thematic only; irrelevant.

### 4 — Nearby-rule comparison
Use a small principled comparison family fixed in advance. Do not parameter-fish. The frozen rule remains primary.

### 5 — Compact formal specification
Formalise the domain, leading digit, map, iteration, cycle, conjecture proposition, seven cycle transitions, and elementary facts such as odd inputs mapping to even outputs. Do not turn the pilot into a Lean proof programme.

### 6 — Candidate assessment
Choose exactly one current gate:

- REJECT_PRIOR_ART
- REJECT_GENERIC
- REJECT_UNINTERESTING
- CONTINUE_AUDIT
- CANDIDATE_DISTINCTIVE_CONJECTURE
- CANDIDATE_NOVEL_CONJECTURE

CANDIDATE_DISTINCTIVE_CONJECTURE means the object is worth presenting and continuing to test as a named conjecture candidate, while novelty remains unresolved.

CANDIDATE_NOVEL_CONJECTURE requires a substantially stronger prior-art audit than failure of literal-formula searches.

## Current gate

CANDIDATE_DISTINCTIVE_CONJECTURE, dated 2026-09-26.

The next highest-value work is continued equivalence-focused prior-art audit and targeted falsification, not an attempt to prove universal convergence.
