# Lean specification

This directory is intentionally small. Its job is to make the frozen mathematical object exact and machine-check elementary facts, not to launch a proof programme.

The Lean layer:

- totalizes the decimal leading digit at 0 only for convenience;
- keeps the intended domain convention 0 < n in the conjecture;
- defines the frozen map T and function iteration;
- defines the distinguished cycle;
- states LeadingDigitHailstoneConjecture as a Prop;
- verifies all seven cycle transitions and seven-step closure by computation;
- proves that an odd input maps to an even output;
- contains no theorem asserting the central conjecture and no sorry placeholder.

The project is pinned to the Lean/mathlib v4.34.0 release pair. CI builds the specification and asks nanoda to reject sorryAx.
