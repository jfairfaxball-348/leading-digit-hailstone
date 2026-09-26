# Proof / Conjecture Attack Map

**Phase:** Stage 1 mathematical research.

**Central conjecture (CONJECTURE):** every positive integer eventually enters the distinguished 7-cycle.

The purpose of this note is not to select a preferred proof narrative. It records what is already exact, what each plausible strategy would need, what is known to obstruct it, and what observation would falsify or materially weaken the strategy.

## Strongest current exact facts

### Arithmetic / valuation structure — ELEMENTARY FACTS

- Every odd raw step is even.
- In a fixed leading-digit sector d, the conditions v2(3n+2d+1) >= r and = r are exact single 2-adic residue classes of the expected moduli.
- Every fixed finite valuation occurs infinitely often in every leading-digit sector.
- Fixed-sector interval densities of exact valuations are geometric, with mean valuation tending to 2. This is an interval-counting fact, not a trajectory-independence theorem.
- Arbitrarily long initial accelerated runs with exact v2=1 exist. Therefore no proof can assume a uniform upper bound on consecutive weak divisions.

### Decimal geometry — ELEMENTARY FACTS

- On each decimal leading-digit sector the odd branch is affine: 3n+(2d+1).
- Internal leading-digit boundaries give an odd-branch jump of +8; powers of ten give a jump of -10.
- The full map is not affine on residue classes modulo any fixed finite modulus.

### Inverse structure — ELEMENTARY FACTS

- Every target has the even predecessor 2m.
- There are at most three arithmetic odd-predecessor candidates before digit consistency is imposed.
- Every target other than 36 has at most one valid odd predecessor; 36 has the two odd predecessors 7 and 11.

### Cycle structure — ELEMENTARY FACTS / EXACT IDENTITIES

For an accelerated odd cycle x_0,...,x_(q-1), with

x_(i+1)=(3x_i+c_i)/2^(r_i),  c_i=2L(x_i)+1,  R=sum r_i,

the additive cycle equation is

(2^R-3^q)x_0 = sum_j 3^(q-1-j)c_j 2^(R_j),

so 2^R>3^q.

New Stage-1 work adds the exact multiplicative identity

2^R / 3^q = product_i (1 + c_i/(3x_i)).

If M=min_i x_i, then

1 < 2^R/3^q <= (1 + 19/(3M))^q.

Thus large-minimum cycles force R/q to be an exceptionally close upper rational approximation to log_2(3).

Also, for any odd state x>19:

- r=1 implies the accelerated step strictly increases;
- r>=2 implies the accelerated step strictly decreases.

Hence a large cycle minimum must leave by r=1, and the step entering that minimum must have r>=2.

### Finite evidence — FINITE COMPUTATION

- Every seed 1..5,000,000 enters the distinguished cycle.
- Any different positive cycle therefore has minimum element >5,000,000.
- Targeted decimal-boundary and constructed long-v2=1 tests have not produced a counterexample.
- These are bounded facts only.

## Attack A — Deterministic accelerated descent

### Aim

Find finite valuation/leading-digit blocks whose combined action provably sends the current odd state below a previous reference level, then prove that every sufficiently large trajectory must encounter such a block.

### Why plausible

An r>=2 accelerated step is strictly descending once x>19, while the heuristic average valuation is 2. The additive correction is O(1) relative to x.

### Main obstruction

Arbitrarily long r=1 runs exist. Therefore descent cannot follow from a bounded waiting time for r>=2, nor from a claim that growth streaks are uniformly short.

### Concrete next lemmas

1. **Completed first lemma:** after s weak divisions, one-step return to the pre-run height requires 2^(r+s)>3^(s+1); see notes/weak_run_compensation.md.
2. Extend this to **multi-step compensation blocks**, because the constructed 32-, 50-, and 100-step weak runs are not followed by immediate large valuations and recover below their starts only after 51, 128, and 304 accelerated steps.
3. Classify short valuation words by exact affine multiplier/additive term.
4. Add leading-digit consistency and determine which net-growth words are actually realizable.
5. Seek a finite family of multi-step "reset" blocks whose occurrence implies descent below the start of the preceding weak run.

### What would weaken/falsify this approach

- construction of arbitrarily long realizable valuation/digit words with positive net multiplier and no compensating deterministic restriction;
- trajectories whose word complexity defeats any finite reset-family formulation.

## Attack B — Positive-cycle exclusion

### Aim

Turn the additive and multiplicative cycle identities into rigorous exclusions for large classes of q,R, valuation words, and leading-digit words.

### Why plausible

The 5M census already forces any competing cycle to have very large minimum. The multiplicative identity then makes the allowed ratio 2^R/3^q extremely close to 1.

### Concrete next lemmas

1. Use M>5,000,000 to exclude small q exactly from the multiplicative window.
2. Couple the minimum anchor (..., r>=2, r=1, ...) to admissible valuation words.
3. Use exact congruence lifting to enumerate valuation words only when their parameter bounds are proved complete.
4. Add decimal interval consistency to eliminate formally possible but unrealizable words.
5. Search for modular obstructions to the cycle equation after digit-word fixing.

### Current bounded consequences

For arbitrary accelerated cycles, the exact-integer certificate in scripts/cycle_minimum_length_bound.py verifies that the general multiplicative window excludes q<=970 when M>=5,000,001. Therefore any different positive cycle consistent with the 5M census must contain at least 971 odd states.

For the narrower one-rise/one-fall class of Issue #10, geometric state bounds on both sides of the unique turning pair give the period-independent envelope

1 < 2^R/3^q <= M(M-19)/(M^2-57M+361).

Exact product-window enumeration through q=400,000 leaves six periods. For each, the same envelope gives an exact finite M_max; exact symbolic decimal-sector interval splitting plus exact binary lifting shows that no M in its complete allowed range sustains the required r=1 rise block.

Therefore the structured class is excluded through q=400,000 under the 5M premise. Any remaining structured cycle has q>=400,001 and a>=166,015.

This substantially strengthens Issue #10 without closing it. The next precise target is to extend the theorem-driven survivor analysis beyond q=400,000, stopping if a product survivor produces a nonempty long-rise symbolic family rather than escalating to an undirected scan.

### What would weaken/falsify this approach

- a competing cycle found computationally;
- existence of many long q for which the approximation window is easily met and digit/valuation constraints provide little further pruning.

## Attack C — Inverse-tree coverage

### Aim

Show that large classes of positive integers lie in the inverse tree of the distinguished cycle, ideally through an induction or density argument.

### Why plausible

Odd predecessors are almost unique. This makes the inverse graph much less branchy than a generic state-dependent affine system.

### Main obstruction

An inverse tree can be sparse even with low branching. Local predecessor uniqueness does not imply global coverage.

### Concrete next lemmas

1. Characterize exactly when an odd predecessor exists in terms of m modulo 3 plus a decimal interval inequality.
2. Study the density of targets admitting an odd predecessor by decimal scale.
3. Identify monotone or scale-reducing inverse constructions.
4. Determine the precise role of the exceptional double branch at 36.

### What would weaken/falsify this approach

- rigorous evidence that large residue/digit classes systematically fail to appear in the distinguished inverse tree;
- inverse growth too sparse for any plausible induction.

## Attack D — Decimal-sector geometry

### Aim

Exploit the fact that digit changes occur only at explicit decimal boundaries while the within-sector dynamics is affine.

### Why plausible

The map is neither arbitrary nor finite-modulus: it has large affine intervals separated by controlled jumps.

### Main obstruction

Accelerated division by variable powers of two can cross many sector boundaries at once, and powers-of-ten boundaries are non-monotone.

### Concrete next lemmas

1. Give exact interval images for one accelerated step at fixed (d,r).
2. Bound the number and location of possible output leading digits.
3. Derive symbolic consistency inequalities for finite (digit,valuation) words.
4. Prove stability of realizable words under sufficiently large decimal scaling when additive corrections are controlled.

### What would weaken/falsify this approach

- sector transition graphs becoming essentially complete at moderate word length;
- boundary effects remaining too unconstrained to improve over valuation-only analysis.

## Attack E — Rigorous drift

### Aim

Replace heuristic log drift by a deterministic or measure-theoretic statement strong enough to imply recurrent descent.

### Why plausible

Fixed-sector valuation densities have mean 2, giving the familiar negative heuristic multiplier 3/4.

### Main obstruction

Trajectory states are not known to sample residue classes independently or equidistributedly. Leading-digit feedback can create correlations.

### Concrete next lemmas

1. Test conditional valuation distributions along carefully defined finite state classes.
2. Search for exact block averages over complete residue sets intersected with decimal sectors.
3. Identify whether a finite-state extension can capture enough dependence for a rigorous averaged contraction result.

### What would weaken/falsify this approach

- persistent trajectory bias toward r=1 classes;
- digit/valuation correlations strong enough to reverse every natural averaged estimate.

## Research policy

Computation should now be attached to a specific lemma, obstruction, or bounded exclusion. Larger undirected sweeps are lower value than exact certificates that close a mathematically stated case.

The central conjecture remains the right working statement only so long as falsification attempts do not produce a competing cycle, escaping orbit, or structural reason to weaken it.
