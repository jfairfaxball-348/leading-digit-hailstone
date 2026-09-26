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

The original exact product-window scan through q=400,000 left six periods, all removed by symbolic decimal-sector / 2-adic rise coverage. The next increment replaces further linear scanning by a Farey-neighbour transfer lemma for alpha=log_2(3): an exact upper approximation R_u/q_u and an exact lower Farey neighbour R_l/q_l certify that no better upper absolute error can occur for q_u<=q<q_u+q_l.

The record-to-record mechanism has now been iterated substantially further. Seven additional exact upper records, beginning at q=64,497,107, are certified using rigorous rational bounds for log 2, log 3, and the structured product envelope rather than constructing giant powers. Their theorem-derived M_max ranges are eliminated by complete decimal-sector / 2-adic symbolic coverage at rise depths 31, 31, 35, 38, 41, 41, and 49. The next upper record q=890,638,885,193 is now excluded by the post-lock deterministic-tail certificate: symbolic coverage stops at the bit-length lock depth and the finite locked candidate set is followed directly.

The resulting bounded structured consequence is

- q>=1,643,749,725,074;
- a>=682,217,775,335.

The largest fully symbolic record-chain range remains q=137,528,045,312 with M_max=42,285,421,502,900. The new post-lock certificate processes q=890,638,885,193 with M_max=48,737,068,628,469: lock occurs at depth 45, two concrete starts survive, and direct continuation shows that neither reaches 49 rises. The next unprocessed upper record is (q,R)=(1,643,749,725,074,2,605,281,674,813).

Two theorem-level scale statements now sharpen the interpretation. If t=log(2^R/3^q), then the structured envelope gives M<39/t for M>=5,000,001. For a determinant-one upper/lower Farey pair, p delta+q epsilon=1; at the final lower neighbour before the next upper mediant this gives delta>1/q_next, hence M_max<39 q_next/log 2. Separately, decimal-boundary localization gives only O(s) possible finite-range decimal-sector words at rise depth s for a fixed [L,U], up to an explicit boundary count.

The residue-position side is now more rigid. For a fixed rise word, write rho_s for the unique exact-r=1 start residue modulo 2^(s+1). Appending a digit chooses one bit b_s with rho_(s+1)=rho_s+b_s*2^(s+1); hence the lift bits are exactly the binary digits of the required start. If M<=U and B=floor(log_2 U), then 2^(B+1)>U, so any start surviving B rises satisfies M=rho_B. Every subsequent compatible lift bit must be zero. After lock the defining carry equation gives x_s=1+2H_s, and b_s=0 is exactly equivalent to v2(3x_s+2L(x_s)+1)=1. Thus there is no longer any symbolic lift or decimal-sector choice after B: the tail is the deterministic accelerated orbit of each locked start.

Combining this locking theorem with the finite-range boundary count gives at most 20*J_B(L,U)+1 possible starts at depth B and the explicit bound J_s(L,U)<=9*s*(ceil(log_10((U+19)/L))+1). For fixed L this is O((log U)^2) candidates at the locking depth. It is not an extinction theorem: no general bound on the zero-lift tail has been proved.

On the new product-window range 5,000,001<=M<=48,737,068,628,469, B=45 and exact symbolic coverage to lock still leaves exactly two starts, 26,501,219,601,103 and 39,751,829,401,657. Direct exact continuation gives total rise lengths 48 and 47 respectively, so the range is empty at rise 49. This is sufficient to exclude the record q=890,638,885,193 and transfer the structured frontier to q=1,643,749,725,073.

A purely range-independent finite acyclic transition graph also cannot finish the problem: arbitrarily long exact-r=1 runs already exist globally, so any finite exact graph encoding all such prefixes has arbitrarily long paths and therefore a directed cycle. A useful finite-state method must retain scale/range or another unbounded coordinate.

A second false route is now explicit. The start 43,574,304,770,317,398,119 has bit-length lock depth 65 and 71 initial exact-r=1 rises, so its deterministic post-lock tail has length 6 before valuation 7. Hence universal constant post-lock tail bounds <=5 are false. This finite exact example does not show unbounded tails.

A new post-lock scale coordinate sharpens the decimal side. Starting from a concrete lock state X, let X_j be an exact-r=1 tail and put Z_j=(2/3)^j X_j. Then

Z_(j+1)-Z_j=(c_j/3)(2/3)^j,

so

3(1-(2/3)^t) <= Z_t-X <= 19(1-(2/3)^t) < 19.

Thus all normalized post-lock states stay in a fixed corridor of width less than 19. If the actual leading digit at time t differs from that of the homogeneous rational (3/2)^t X, some decimal boundary C=d*10^k must satisfy the exact integer inequality

X 3^t < C 2^t < (X+19)3^t.

There are also exact local sector-exit bounds: an r=1 source with leading digit d>=2 leaves its sector in one step, a digit-1 sector supplies at most two consecutive source states, and six consecutive r=1 steps force a power-of-ten crossing.

There is now a complementary finite-horizon coordinate as well.  For any fixed exact-r=1 segment x_0,...,x_N, the terminally anchored guide g_s=x_N(2/3)^(N-s) satisfies

g_s-x_s=sum_(j=s)^(N-1) (c_j/3)(2/3)^(j-s),

hence 0<=g_s-x_s<19 uniformly in N and scale.  Thus one concrete homogeneous orbit stays within absolute distance 19 above every earlier state of the segment.  Any disagreement between x_s and this terminal guide again forces a decimal boundary inside a width-19 interval, now in the unscaled state coordinate.  This is useful for candidate-specific phase certificates, but the guide depends on the terminal state and therefore is not by itself a uniform F(B) theorem.

These geometric facts still do not force termination. The exact own-bit lock diagnostic through B=220 finds 96 locked candidates and 41 positive post-lock tails, with maximum observed tail 6. Every one of those 41 positive tails has zero scaled-boundary corridor hits and zero disagreement with its homogeneous leading-digit itinerary. This is finite exact computation only, but it shows that decimal-boundary near-hits are not necessary for the observed long tails.

The highest-value continuation is therefore not another broad q scan: seek a scale-aware parity or congruence obstruction along the phase-frozen homogeneous (3/2)^t digit itinerary, or rigorously construct a family showing why such a bound cannot be strong enough. Mixed 2^m5^n information, carry parity, or another unbounded scale coordinate are natural next targets.

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

## Phase-frozen boundary separation

The post-lock width-19 corridor now has an exact recurrence-spacing theorem. For a lock state `X>38`, two distinct scaled decimal-boundary hits `n` steps apart imply

`X <= 171*3^n`.

Equal scaled hits can recur only in the exact short chains `2->3` and `4->6->9`. Thus exceptional decimal ambiguity is separated on a logarithmic scale in `X`.

Between those exceptional hits, the digit word is forced by the homogeneous rational orbit `(3/2)^tX`. The full exact-r=1 prefix then collapses to the already proved terminal 2-adic residue condition for that one word.

The current candidate certificates terminate at forced words `2357`, `357`, and `1124691`, giving tails 3, 2, and 6. The noncoincident ambiguity thresholds for their lock states are 41, 41, and 61 steps.

The remaining theorem target is no longer decimal phase localization itself. It is a scale-aware bound on how long a **phase-frozen homogeneous digit word** can keep matching the required 2-adic residue prefixes.
