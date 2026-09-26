# Research Rules

This repository is a conjecture-discovery and falsification pilot, not a proof-by-computation project.

## Required claim labels

Every substantive claim should be identifiable as one of:

- DEFINITION — stipulated object or convention.
- ELEMENTARY FACT — proved directly with a complete argument.
- FINITE COMPUTATION — exact result over a finite, explicitly stated protocol.
- HEURISTIC — statistical/model-based reasoning without proof.
- CONJECTURE — unproved mathematical statement.
- LITERATURE FACT — claim supported by a cited external source.
- THEOREM — proved statement with a complete accepted argument.
- NOVELTY CLAIM — prohibited until the prior-art audit supports it.

## Hard constraints

1. Never convert a finite sweep into a universal convergence statement.
2. Never describe the frozen map as new, original, unique, or previously unknown while novelty_status is unresolved.
3. Equivalent mathematics under different notation counts as prior art.
4. Keep the frozen map exactly n/2 for even n and 3n+2L(n)+1 for odd n, with ordinary decimal leading digit L.
5. Put nearby variants in a separate comparison layer. Fix small comparison families before running them; do not search thousands of rules and retroactively select a visually attractive one.
6. Record the finite domain or sampling protocol, cap, RNG seed where applicable, and a reproducible script for computational evidence.
7. Treat a step cap as unresolved within cap, never as divergence.
8. Absence of another cycle in a bounded search is only a bounded exclusion.
9. Prior-art notes must distinguish exact matches, equivalent formulations, direct superclasses, close analogues, thematic similarity, and irrelevant hits.
10. Structural mathematics is pursued to understand distinctiveness and nontriviality; proof readiness is not the project gate.
11. A compact Lean specification is allowed and encouraged as an exact executable specification. Do not declare the central conjecture as an unproved theorem with sorry, and do not let formal proof work dominate the pilot.
12. The familiar 1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1 cycle must be explicitly identified as 5x+1 prior art.

## Reproducibility rule

Incoming numerical observations remain provisional until independently reproduced. New experiments must be clearly separated from incoming claims and labelled FINITE COMPUTATION.
