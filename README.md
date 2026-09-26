# Leading-Digit Hailstone Dynamics

A mathematical research programme studying the frozen map

T(n) = n/2 when n is even, and T(n) = 3n + 2L(n) + 1 when n is odd,

where L(n) is the leading decimal digit of the positive integer n.

The distinguished observed cycle is

1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1.

## Central conjecture

**Leading-Digit Hailstone Conjecture.** Every positive integer eventually enters the distinguished 7-cycle.

This is a conjecture, not a theorem.

The completed discovery pilot reached the gate **CANDIDATE_DISTINCTIVE_CONJECTURE**. The declared Stage-1 red-team/mathematical exploration programme is frozen with status **COMPLETE_CONJECTURE_SURVIVES_DECLARED_STRESS_TEST**. The conjecture remains unproved. **Stage 2: Lean formalisation** has completed its audit exit gate. **Stage 3B: Palomar editorial remediation** is active. The first Palomar snapshot passed full mechanical verification but was rejected editorially because its sole selected valuation-burst theorem was too elementary to establish research interest. That immutable snapshot remains preserved. The remediation selects the substantially stronger conditional accelerated-cycle theorem: every positive accelerated cycle with all odd states at least 5,000,001 has at least 971 odd states. Universal convergence remains unproved.

The map is **not claimed to be new or previously unknown**. Historical novelty remains unresolved, and mathematically equivalent prior art under different notation counts.

The distinguished cycle itself is not novel: on single-digit odd inputs L(n)=n, so the odd rule is 5n+1 and the displayed cycle is the familiar positive 5x+1 cycle.

## Current evidence, kept separate by type

**FINITE COMPUTATION.** Exact exhaustive testing through 5,000,000 found every tested seed entering the distinguished cycle and no competing positive cycle. The cycle-entry record is seed 4,625,895 at 713 raw iterations; the maximum-excursion record is seed 4,449,695 reaching 1,265,270,503,548. Consequently any different positive cycle, if one exists, has minimum element greater than 5,000,000.

**ELEMENTARY FACTS.** The repository records exact 2-adic residue classes, decimal-sector affine structure and boundary jumps, strong inverse-image restrictions, an accelerated-cycle equation, a proof that the full map is not a finite-modulus residue-class-wise affine map, and a constructive proof that arbitrarily long initial runs with exact accelerated valuation v2=1 exist.

**FINITE COMPARISON.** In the predeclared family c_b(d)=2d+b with b in {-3,-1,1,3,5}, all four nonfrozen shifts had multiple observed cycles while the frozen b=1 rule had one observed cycle through seeds 1..1,000,000. Of 18 one-coordinate perturbations c(d) -> c(d)+/-2, 11 had multiple observed cycles through 100,000; all 7 one-cycle survivors remained one-cycle through 1,000,000.

**FINITE ADVERSARIAL TESTING.** All 9,000 boundary seeds d*10^k +/- 1 for d=1..9 and k=1..500 entered the distinguished cycle within the stated cap. The final declared Stage-1 campaign additionally tests 756 multi-offset decimal-boundary starts at exponents 600..2000, 350 deterministic random odd starts at 20..2000 decimal digits, 1,476 inverse-tree-derived hostile starts, and exact residue-engineered starts requesting 150, 300, 500, 750 and 1000 initial v2=1 accelerated steps. Every tested seed in these declared campaigns entered the distinguished cycle within the stated raw-step cap. This is finite computation, not a proof.

**LITERATURE STATUS.** The 5x+1 cycle is prior art; standard finite-modulus generalized-Collatz/RCWA frameworks are close analogues but do not contain this leading-decimal-sector map as a finite-modulus instance; active leading-digit integer dynamics exists elsewhere. No exact or mathematically equivalent full-map construction has yet been identified in the current audit. This is negative search evidence, not a novelty claim.

## Stage 1 outcome and next stage

Stage 1 is intentionally complete as a declared falsification programme, not because universal convergence has been proved.

The conjecture survived the agreed stress-test gate: no competing positive cycle, apparent escape within the declared caps, structural contradiction, or statement defect was found. The project retains the strong partial mathematics developed during Stage 1, including the arbitrary-cycle q>=971 consequence, the structured one-rise/one-fall frontier, residue locking, deterministic post-lock reduction, and width-19 phase guides.

A new elementary red-team family is also recorded: for n=2*10^k-1, the odd-branch numerator is exactly 6*10^k, so its 2-adic valuation is k+1. Thus arbitrarily large single valuation bursts occur.

The Lean formalisation audit now certifies the positive-domain convention, decimal leading-digit semantics and 1..9 bound, positivity preservation of the frozen map, the exact distinguished cycle and its invariance, iterates, and the central conjecture as an unproved proposition. A proof of universal convergence remains outside the pipeline requirement. See notes/STAGE_2_LEAN_FORMALISATION.md for the exact formalisation audit.

See ROADMAP.md and notes/STAGE_1_FINAL_STRESS_TEST.md.

### First Stage-1 progress

**ELEMENTARY FACTS.** For any accelerated odd cycle,
2^R/3^q = product_i(1+c_i/(3x_i)). If M is the minimum odd state, this gives
1 < 2^R/3^q <= (1+19/(3M))^q. Also, above 19 an accelerated step rises exactly when its valuation is 1 and falls whenever its valuation is at least 2. After s consecutive valuation-1 steps, a single next step returning to or below the pre-run height must satisfy 2^(r+s)>3^(s+1).

**FINITE EXACT CONSEQUENCE.** Combining the general product window with the exhaustive 5,000,000-seed cycle exclusion yields an exact-integer certificate excluding q<=970 for any different positive accelerated cycle. Thus any such cycle must contain at least 971 odd states.

**STRUCTURED-CYCLE THEOREM + FINITE EXACT SYMBOLIC/DIRECT CONSEQUENCE.** For the narrower class with one contiguous r=1 rise block followed by one contiguous r>=2 fall block, geometric state bounds sharpen the product window to
1 < 2^R/3^q <= M(M-19)/(M^2-57M+361).
Exact Farey-neighbour transfer avoids period-by-period scanning. Seven further upper records beyond PR #12 were eliminated by complete decimal-sector / 2-adic symbolic coverage. The next upper record is now eliminated by a lock-and-follow certificate: symbolic coverage is needed only to the bit-length lock depth, after which the surviving concrete starts are followed directly. Consequently any remaining one-rise/one-fall cycle consistent with the 5M minimum premise must have q>=1,643,749,725,074 and at least 682,217,775,335 consecutive rise steps. The new certified product-window range has M_max=48,737,068,628,469 and is empty at rise 49.

The residue-position theorem now collapses the post-lock dynamics exactly. For a fixed rise word, rho_(s+1)=rho_s+b_s*2^(s+1); at B=floor(log_2 U), a bounded surviving start satisfies M=rho_B and all later compatible lift bits are zero. Moreover x_s=1+2H_s after lock, and b_s=0 is equivalent to the concrete accelerated numerator at x_s having valuation one. Thus there is no symbolic branching after B: the remaining tail is deterministic orbit following. This still is not a scale-aware extinction theorem. In fact a finite exact example has lock depth 65 and total rise length 71, so universal constant post-lock tail bounds <=5 are false. The structured class is therefore not globally excluded, and arbitrary cycles retain the separate q>=971 bound.

**MECHANISM-TARGETED COMPUTATION.** The explicit long weak-run examples do not exhibit immediate giant compensation: the observed 32-, 50-, and 100-step runs first exit with valuations 2, 3, and 2 and return below their starting seeds after 51, 128, and 304 accelerated steps. This makes multi-step block compensation a higher-value target than a one-step reset hypothesis.


## Reproducibility

Python reference and verification implementations live under src/leading_digit_hailstone. Key scripts and machine-readable summaries live under scripts/ and data/.

## Lean

The Lean 4 layer under LeadingDigitHailstone/ specifies the frozen map and central conjecture, proves the decimal leading-digit specification on positive naturals, and now formally proves the conditional 971-state accelerated-cycle restriction. The selected theorem derives a cyclic product identity, a product window from the correction bound 3..19 and minimum floor 5,000,001, and an exact Farey-neighbour exclusion. The finite 5M census is not imported into Lean; the minimum floor is an explicit theorem hypothesis. The universal conjecture remains an unproved Prop, and no sorry placeholder is used in the substantive development or Solution. Challenge.lean contains only the deliberate Comparator proof hole.

See RESEARCH_RULES.md, PROJECT_STATUS.json, notes/CANDIDATE_ASSESSMENT.md, notes/cycle_constraints.md, and literature/DEEP_AUDIT_2026-09-26.md before making stronger claims.


## Palomar Stage-3B editorial remediation

The historical Stage-3 snapshot `f3309bd7d47da7cc3f1a12119aea8022b8f6c98a`
passed the official full mechanical verifier but was later rejected by
Palomar's automated editorial review because the sole selected
`valuationBurstFamily` result was an elementary substitution whose research
interest had not been established. That commit is preserved unchanged.

The replacement Palomar result is
`LeadingDigitHailstonePalomar.leadingDigitCyclePeriodLowerBound`: any positive
accelerated periodic orbit satisfying the actual leading-decimal-digit
numerators and having every odd state at least 5,000,001 has at least 971 odd
states. The proof is entirely Lean/kernel checked and uses no Python
certificate. It does **not** formalize the external 5M census, the much larger
structured one-rise/one-fall finite certificate, or universal convergence.

The targeted Stage-3B literature check records classical product-window and
continued-fraction/Farey cycle-length methods as prior methodology, especially
Eliahou (1993) and Simons--de Weger (2005). A current Lean formalization of
Eliahou's ordinary-Collatz theorem is also recorded as related formal prior
art. No exact decimal-leading-digit analogue was identified in the targeted
search; novelty therefore remains `UNRESOLVED_DO_NOT_CLAIM`.

The project remains pinned to Lean/Mathlib `v4.35.0-rc2`. The current official
PalomarSubmission full-preflight revision remains
`a59f25bd8a66bf6faf3a4f4260d412989c0185ea`. Registration is not performed
by repository CI; final resubmission remains an owner action.
