# Pilot Decision

## Gate

`CONTINUE_STRUCTURAL`

Date: 2026-09-26.

This gate says the frozen object is sufficiently mathematically structured to justify a deeper structural phase. It is **not** a theorem claim, a novelty claim, or a decision to target a proof immediately.

## Evidence supporting continuation

### Exact finite computation

- Every start `1 <= n <= 5,000,000` entered the distinguished cycle in the exact census.
- No competing cycle was observed in that finite range.
- The largest cycle-entry time in that range is currently 713 raw steps at seed `4625895`.
- The current excursion-ratio record in that range is seed `4449695`, reaching `1265270503548`.
- Therefore any other positive cycle, if one exists, has minimum element above `5,000,000`.
- A deterministic replacement sample of 1,000 starts with 10–200 decimal digits also entered the distinguished cycle within its explicit cap. This replacement is not presented as replay of the original unspecified random experiment.

These are finite results only.

### Structural content already obtained

The frozen map has several exact features that make it more than a bare parameter search:

- inside each decimal leading-digit sector, the odd branch is one of nine affine rules `3n+(2d+1)`;
- exact 2-adic valuation classes can be described by one residue class modulo powers of two, with conditional interval density `2^(-r)`;
- the odd branch has a characteristic downward jump across powers of ten and different jumps at other leading-digit boundaries;
- the inverse graph is highly constrained: every target has its even predecessor, and all but target `36` have at most one odd predecessor; `36` has exactly `7` and `11`;
- the map has no finite-modulus residue-class-wise affine representation on the positive integers;
- accelerated cycles satisfy an exact state-dependent cycle equation and the necessary inequality `2^R>3^q`.

These properties support a structural programme in their own right.

## Prior-art effect on the decision

The prior-art audit changes how the object should be described.

The distinguished cycle is not distinctive to this map: on single-digit odd inputs the frozen rule is `5n+1`, and the cycle

`1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1`

is a standard `5x+1` cycle.

The full rule also has close local `3x+k` analogues, and there is established literature both on digit-dependent integer dynamics and on leading digits of ordinary Collatz trajectories.

However, the initial equivalence audit has not identified the full frozen map as an exact known construction, and the elementary non-RCWA result shows it is not contained in the usual finite-modulus residue-class-wise affine class merely by changing notation.

**Novelty remains unresolved.** The gate does not upgrade the object to `new`, `original`, `unique`, or `previously unknown`.

## Why not the other continuation gate yet?

### Not `CONTINUE_PROOF_TARGET`

The negative-drift model is still heuristic, the finite census is tiny relative to a universal claim, and no global Lyapunov/descent mechanism or complete cycle exclusion is known. Proof-directed work may become justified later, but making it the pilot target now would overstate the evidence.

### Why `CONTINUE_STRUCTURAL` rather than only `CONTINUE_COMPUTATIONAL`

More computation is useful, but the pilot has already exposed exact mechanisms that deserve analysis independently of larger sweeps: the decimal-sector partition, power-of-ten discontinuities, rigid inverse branching, exact valuation classes, and state-consistent cycle equations. The next marginal value is therefore structural analysis coupled to targeted computation, rather than scale alone.

## Next structural phase

The next phase should concentrate on four linked questions:

1. quantify how actual trajectories sample the exact `v2` classes and leading-digit sectors, testing where the geometric heuristic fails;
2. exploit the near-unique inverse graph and cycle equation for rigorous bounded cycle exclusions;
3. develop decimal-boundary transition lemmas strong enough to control changes of leading digit under the accelerated map;
4. continue the equivalence audit in parallel, especially broader radix-dependent/state-dependent affine systems and sequence databases.

The frozen rule remains unchanged throughout this phase.
