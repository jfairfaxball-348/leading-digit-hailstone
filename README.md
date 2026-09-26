# Leading-Digit Hailstone Dynamics

A mathematical research programme studying the frozen map

T(n) = n/2 when n is even, and T(n) = 3n + 2L(n) + 1 when n is odd,

where L(n) is the leading decimal digit of the positive integer n.

The distinguished observed cycle is

1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1.

## Central conjecture

**Leading-Digit Hailstone Conjecture.** Every positive integer eventually enters the distinguished 7-cycle.

This is a conjecture, not a theorem.

The completed discovery pilot reached the gate **CANDIDATE_DISTINCTIVE_CONJECTURE**. The project has therefore moved into **Stage 1: mathematical proof/conjecture research**, with Lean formalisation and prior-art work continuing in parallel.

The map is **not claimed to be new or previously unknown**. Historical novelty remains unresolved, and mathematically equivalent prior art under different notation counts.

The distinguished cycle itself is not novel: on single-digit odd inputs L(n)=n, so the odd rule is 5n+1 and the displayed cycle is the familiar positive 5x+1 cycle.

## Current evidence, kept separate by type

**FINITE COMPUTATION.** Exact exhaustive testing through 5,000,000 found every tested seed entering the distinguished cycle and no competing positive cycle. The cycle-entry record is seed 4,625,895 at 713 raw iterations; the maximum-excursion record is seed 4,449,695 reaching 1,265,270,503,548. Consequently any different positive cycle, if one exists, has minimum element greater than 5,000,000.

**ELEMENTARY FACTS.** The repository records exact 2-adic residue classes, decimal-sector affine structure and boundary jumps, strong inverse-image restrictions, an accelerated-cycle equation, a proof that the full map is not a finite-modulus residue-class-wise affine map, and a constructive proof that arbitrarily long initial runs with exact accelerated valuation v2=1 exist.

**FINITE COMPARISON.** In the predeclared family c_b(d)=2d+b with b in {-3,-1,1,3,5}, all four nonfrozen shifts had multiple observed cycles while the frozen b=1 rule had one observed cycle through seeds 1..1,000,000. Of 18 one-coordinate perturbations c(d) -> c(d)+/-2, 11 had multiple observed cycles through 100,000; all 7 one-cycle survivors remained one-cycle through 1,000,000.

**FINITE ADVERSARIAL TESTING.** All 9,000 boundary seeds d*10^k +/- 1 for d=1..9 and k=1..500 entered the distinguished cycle within the stated cap. Explicit residue-lifted examples with at least 30, 50, and 100 consecutive initial v2=1 accelerated steps also entered the distinguished cycle within the stated cap.

**LITERATURE STATUS.** The 5x+1 cycle is prior art; standard finite-modulus generalized-Collatz/RCWA frameworks are close analogues but do not contain this leading-decimal-sector map as a finite-modulus instance; active leading-digit integer dynamics exists elsewhere. No exact or mathematically equivalent full-map construction has yet been identified in the current audit. This is negative search evidence, not a novelty claim.

## Active mathematical programme

Stage 1 develops several approaches in parallel:

- accelerated odd dynamics and deterministic descent;
- cycle exclusion from exact valuation/digit constraints;
- inverse-tree structure;
- decimal-sector geometry;
- targeted computation for theorem discovery and falsification.

The theorem on arbitrarily long v2=1 runs means no proof may assume a global bound on consecutive weak divisions.

See ROADMAP.md and notes/PROOF_ATTACK_MAP.md for the current research plan.

### First Stage-1 progress

**ELEMENTARY FACTS.** For any accelerated odd cycle,
2^R/3^q = product_i(1+c_i/(3x_i)). If M is the minimum odd state, this gives
1 < 2^R/3^q <= (1+19/(3M))^q. Also, above 19 an accelerated step rises exactly when its valuation is 1 and falls whenever its valuation is at least 2. After s consecutive valuation-1 steps, a single next step returning to or below the pre-run height must satisfy 2^(r+s)>3^(s+1).

**FINITE EXACT CONSEQUENCE.** Combining the general product window with the exhaustive 5,000,000-seed cycle exclusion yields an exact-integer certificate excluding q<=970 for any different positive accelerated cycle. Thus any such cycle must contain at least 971 odd states.

**STRUCTURED-CYCLE THEOREM + FINITE EXACT CONSEQUENCE.** For the narrower class with one contiguous r=1 rise block followed by one contiguous r>=2 fall block, geometric state bounds on both sides of the unique local minimum/maximum pair sharpen the product window to
1 < 2^R/3^q <= M(M-19)/(M^2-57M+361).
Under M>=5,000,001, exact integer arithmetic excludes q<=79,334. The first q not excluded by this necessary window is 79,335 with R=125,743, and any surviving structured cycle must contain at least 32,927 consecutive rise steps. This does not exclude arbitrary cycles or even the full structured class.

**MECHANISM-TARGETED COMPUTATION.** The explicit long weak-run examples do not exhibit immediate giant compensation: the observed 32-, 50-, and 100-step runs first exit with valuations 2, 3, and 2 and return below their starting seeds after 51, 128, and 304 accelerated steps. This makes multi-step block compensation a higher-value target than a one-step reset hypothesis.


## Reproducibility

Python reference and verification implementations live under src/leading_digit_hailstone. Key scripts and machine-readable summaries live under scripts/ and data/.

## Lean

A Lean 4 layer under LeadingDigitHailstone/ specifies the map and central conjecture and proves stable elementary facts. The universal conjecture remains an unproved Prop; no sorry placeholder is used. Formalisation is now expanded alongside Stage-1 mathematics while CI is kept green.

See RESEARCH_RULES.md, PROJECT_STATUS.json, notes/CANDIDATE_ASSESSMENT.md, notes/cycle_constraints.md, and literature/DEEP_AUDIT_2026-09-26.md before making stronger claims.
