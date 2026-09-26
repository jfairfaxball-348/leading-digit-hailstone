# Leading-Digit Hailstone Dynamics

A controlled conjecture-discovery project for

T(n) = n/2 when n is even, and T(n) = 3n + 2L(n) + 1 when n is odd,

where L(n) is the leading decimal digit of the positive integer n.

The distinguished observed cycle is

1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1.

## Candidate conjecture

**Leading-Digit Hailstone Conjecture.** Every positive integer eventually enters the distinguished 7-cycle.

This is a conjecture, not a theorem. The current project gate is **CANDIDATE_DISTINCTIVE_CONJECTURE**: the object has survived the present falsification work and has enough structural and comparative content to justify continued study as a named conjecture candidate. This gate is deliberately weaker than a novelty determination.

The map is **not claimed to be new or previously unknown**. Equivalent mathematics under different notation counts as prior art.

The distinguished cycle itself is not novel: on single-digit odd inputs L(n)=n, so the odd rule is 5n+1 and the displayed cycle is the familiar positive 5x+1 cycle.

## Current evidence, kept separate by type

**FINITE COMPUTATION.** Exact exhaustive testing through 5,000,000 found every tested seed entering the distinguished cycle and no competing cycle. The current cycle-entry record in that census is seed 4,625,895 at 713 raw iterations; the current maximum-excursion record is seed 4,449,695 reaching 1,265,270,503,548. Consequently any different positive cycle, if one exists, has minimum element greater than 5,000,000.

**ELEMENTARY FACTS.** The repository records exact 2-adic residue classes, decimal-boundary jumps, strong inverse-image restrictions, an accelerated-cycle equation, and a proof that the full map is not a standard finite-modulus residue-class-wise affine map.

**FINITE COMPARISON.** In the predeclared family c_b(d)=2d+b with b in {-3,-1,1,3,5}, all four nonfrozen shifts had multiple observed cycles among seeds 1..100,000, while the frozen b=1 rule had one observed cycle. In the 18 one-coordinate perturbations c(d) -> c(d)+/-2, 11 had multiple observed cycles and 7 had one. This is evidence that the frozen behaviour is not automatic in a tiny nearby neighbourhood; it is not evidence of uniqueness or a theorem-level phase boundary.

**FINITE ADVERSARIAL TESTING.** Boundary seeds d*10^k +/- 1 for d=1..9 and k=1..18 all entered the distinguished cycle. The longest initial run of accelerated odd steps with exact v2=1 found among odd seeds through 5,000,000 has length 21 at seed 2,826,307. Constructed 50-, 100-, and 200-digit near-boundary starts chosen to sustain low valuation also entered the cycle within the explicit cap.

**LITERATURE STATUS.** The 5x+1 cycle is prior art; standard generalized-Collatz/RCWA frameworks are close analogues but do not contain this leading-decimal-sector rule as a finite-modulus instance; active leading-digit integer dynamics exists in other digit-map literature. The current deeper audit has not identified an exact or equivalent full-map construction. That remains negative search evidence, not a novelty claim.

## Reproducibility

Python reference and verification implementations live under src/leading_digit_hailstone. Key scripts include:

- scripts/reproduce_incoming.py
- scripts/sweep.py
- scripts/compare_nearby_rules.py
- scripts/adversarial_search.py

Machine-readable summaries are under data/.

## Lean specification

A compact Lean 4 layer lives in LeadingDigitHailstone/. It defines the leading digit, frozen map, iteration proposition, and distinguished cycle; states LeadingDigitHailstoneConjecture as a Prop; checks all seven cycle transitions; and proves that odd inputs map to even outputs. It contains no proof of the central conjecture and no sorry placeholder.

See RESEARCH_RULES.md, ROADMAP.md, notes/CANDIDATE_ASSESSMENT.md, and literature/DEEP_AUDIT_2026-09-26.md before making stronger claims.
