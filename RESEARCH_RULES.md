# Research Rules

This repository is an object-discovery pilot, not a proof-by-computation project.

## Required claim labels

Every substantive research note or result should be identifiable as one of:

- **DEFINITION** — stipulated object or convention.
- **ELEMENTARY FACT** — proved directly in the repository with a complete argument.
- **FINITE COMPUTATION** — exact result over a finite, explicitly stated domain/protocol.
- **HEURISTIC** — statistical/model-based reasoning without proof.
- **CONJECTURE** — unproved mathematical statement.
- **LITERATURE FACT** — claim supported by a cited external source.
- **THEOREM** — proved statement with a complete accepted argument.
- **NOVELTY CLAIM** — prohibited until Task 5 reaches an adequate prior-art conclusion.

## Hard constraints

1. Never convert a finite sweep into a universal convergence statement.
2. Never describe the frozen map as new, original, unique, or previously unknown before the prior-art gate.
3. Equivalent formulations under different notation count as prior art.
4. Keep the frozen map exactly `n/2` for even `n` and `3n+2L(n)+1` for odd `n`, with ordinary decimal leading digit `L`.
5. Put nearby parameter variants in a separate exploratory layer and do not let search over variants replace analysis of the frozen object.
6. Record code version, range, cap, RNG seed/sample protocol, and output summary for computational evidence.
7. Treat a step cap as `UNRESOLVED_WITHIN_CAP`, never as divergence.
8. Detecting no other cycle in a bounded sweep is not evidence that no other cycle exists globally.
9. Literature notes must distinguish exact matches, special cases of known classes, close analogues, and merely thematic similarity.
10. Formalisation, paper drafting, priority claims, and broad generalisation wait until Task 6.

## Reproducibility rule

Incoming numerical observations are provisional until independently reproduced by repository code. If the original protocol lacks enough information for exact replay (for example an unspecified random seed), say so explicitly and substitute only a separately labelled new experiment.
