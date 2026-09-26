# Research Rules

This repository is now a full mathematical research programme built on a completed conjecture-discovery pilot.

## Required claim labels

Every substantive claim should be identifiable as one of:

- **DEFINITION** — stipulated object or convention.
- **ELEMENTARY FACT** — proved directly with a complete argument.
- **THEOREM** — proved statement with a complete accepted argument.
- **FORMAL THEOREM** — theorem checked in Lean without sorry.
- **FINITE COMPUTATION** — exact result over a finite, explicitly stated protocol.
- **HEURISTIC** — statistical/model-based reasoning without proof.
- **CONJECTURE** — unproved mathematical statement.
- **LITERATURE FACT** — claim supported by a cited external source.
- **NOVELTY CLAIM** — prohibited until the final prior-art audit supports it.

## Hard constraints

1. Never convert a finite sweep into a universal convergence statement.
2. Never describe the frozen map or central conjecture as new, original, unique, or previously unknown while novelty_status is unresolved.
3. Equivalent mathematics under different notation counts as prior art.
4. Keep the frozen map exactly n/2 for even n and 3n+2L(n)+1 for odd n, with ordinary decimal leading digit L.
5. Nearby variants remain comparison objects, not replacements for the frozen map.
6. New computation must target a mathematical mechanism, falsification opportunity, or explicit bounded theorem; record domain/protocol, caps where applicable, and reproducible code.
7. Treat a step cap as unresolved within cap, never as divergence.
8. Absence of another cycle in a bounded search is only a bounded exclusion.
9. Prior-art notes must distinguish exact matches, equivalent formulations, direct superclasses, close analogues, thematic similarity, and irrelevant hits.
10. A failed proof strategy is useful research when the obstruction is stated rigorously.
11. Expand Lean alongside stable mathematics. Do not assert the central conjecture as a theorem, and do not use sorry merely to create the appearance of formal progress.
12. The familiar 1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1 cycle must be explicitly identified as 5x+1 prior art.
13. Keep PROJECT_STATUS.json synchronized with the actual epistemic state.
14. Do not begin paper/arXiv packaging before the final novelty/prior-art audit is complete and the formal/reproducibility state is ready. A proof of the central convergence conjecture is not a publication prerequisite.
15. Counterexamples, escaping orbits, competing cycles, weakened conjectures, and prior-art discoveries are positive research outcomes when correct.

## Reproducibility rule

Incoming numerical observations remain provisional until independently reproduced. New finite experiments and finite certificates must be clearly separated from universal mathematics.

## Stage discipline

The intended progression is now:

1. bounded red-team / mathematical exploration;
2. Lean formalisation;
3. Palomar;
4. final comprehensive novelty / prior-art audit;
5. research paper;
6. arXiv submission.

Stage 1 has a declared stopping gate. If the conjecture survives the agreed falsification programme without a competing cycle, apparent escape within the declared caps, structural contradiction, or statement defect, the stage may close while the conjecture remains unproved. An open-ended attempt to prove universal convergence is not a pipeline requirement.

Evidence may move the project backward. Stage labels must describe actual readiness, not aspiration.
