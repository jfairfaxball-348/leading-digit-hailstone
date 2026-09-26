# Stage 3B Palomar Editorial Remediation

Date: 2026-09-26

Status: **STAGE_3B_PALOMAR_EDITORIAL_REMEDIATION**

Novelty status: **UNRESOLVED_DO_NOT_CLAIM**

## Immutable historical attempt

The exact historical Palomar snapshot is:

`f3309bd7d47da7cc3f1a12119aea8022b8f6c98a`

PR #24: **Stage 3: prepare and preflight Palomar registration snapshot**

That commit passed the official full mechanical Palomar verification, including
the default Lean kernel, NanoDa, con-ron, Comparator, and metadata checks. The
subsequent automated editorial review did **not** offer registration. Its core
finding was that the sole selected theorem, `valuationBurstFamily`, was an
elementary substitution and that research interest had not been established
for the selected result itself.

The historical commit is intentionally preserved. Stage 3B does not amend,
force-push, rewrite, or conceal that failed attempt.

## Candidate decision

### Candidate A: structured one-rise/one-fall frontier

Stage 1 establishes the much larger conditional frontier
`q >= 1,643,749,725,074` and at least `682,217,775,335` consecutive
exact-`v2=1` rises for the structured one-rise/one-fall class.

This is mathematically the strongest candidate, but the present headline
depends on an extensive exact Python certificate chain: rational logarithm
enclosures and Farey record generation, decimal-sector/2-adic symbolic cells,
bit-length locking, and deterministic post-lock continuation. Formalising only
the general lemmas would not kernel-check the advertised numerical conclusion.
Candidate A is therefore **not selected for this Palomar remediation** unless
that full certificate is later ported to a Lean-checkable representation.

### Candidate B: arbitrary accelerated-cycle 971 bound — SELECTED

The selected theorem is:

`LeadingDigitHailstonePalomar.leadingDigitCyclePeriodLowerBound`

Plain language:

> Every minimal positive accelerated Leading-Digit Hailstone periodic orbit whose odd
> states are all at least 5,000,001 contains at least 971 distinct odd states.

The minimum threshold is an explicit theorem hypothesis. The selected theorem
does **not** formalize the separate exhaustive census through 5,000,000.
Consequently the Lean theorem is not phrased as an unconditional statement
about every hypothetical competing cycle.

The Stage-1 source obtained the 971 frontier by exact scanning of the necessary
product inequality for `q=1,...,970`. The Stage-3B Lean proof replaces that
scan with a compact Farey gap:

[
  1054/665 < R/q < 485/306,
]

where

[
  485cdot665-1054cdot306=1
  quad	ext{and}quad
  665+306=971.
]

The lower side follows from the cycle product identity and the exact power
comparison `2^1054 < 3^665`. The upper side follows from the minimum floor,
the correction ceiling 19, the product window, and the exact integer
comparison

\[
  (3\cdot5{,}000{,}001+19)^{306}
  < 2^{485}5{,}000{,}001^{306}.
\]

Lean checks these finite arithmetic facts directly with `norm_num`; no Python
certificate is trusted by the selected theorem.

### Candidate C: arbitrarily long weak-division runs

Candidate C remains a genuine theorem and a possible fallback, but is not
needed because Candidate B now has a compact, complete kernel-checked proof
chain and is more directly tied to the cycle problem.

## Formal dependency structure

The selected theorem depends on:

1. positivity and the ordinary decimal leading-digit specification from
   `LeadingDigitHailstone.Basic`;
2. explicit oddness, positive valuation exponents, injective state indexing, and ordinary cyclic successor so q denotes distinct odd states of one minimal cycle;
3. the exact bound `1 <= L(n) <= 9`, hence `3 <= 2L(n)+1 <= 19`;
4. cyclic reindexing of a finite product by the successor permutation;
5. the exact product identity obtained by multiplying
   `2^r_i x_(i+1) = 3x_i+c_i`;
6. the strict lower inequality `3^q < 2^R` from positive corrections;
7. the upper product window induced by `x_i >= 5,000,001` and `c_i <= 19`;
8. the two exact integer power certificates above;
9. the determinant-one Farey denominator lemma.

This is the complete logical chain for the selected theorem. The 5M census and
the larger structured-cycle Python certificates are outside it.

## Targeted theorem-specific prior-art audit

This audit is deliberately narrower than the later Stage-4 comprehensive
novelty audit.

### Sources checked

- Shalom Eliahou, *The 3x+1 problem: new lower bounds on nontrivial cycle
  lengths*, Discrete Mathematics 118 (1993), 45–56,
  DOI 10.1016/0012-365X(93)90052-U.
- John Simons and Benne de Weger, *Theoretical and computational bounds for
  m-cycles of the 3n+1-problem*, Acta Arithmetica 117 (2005), 51–70,
  DOI 10.4064/aa117-1-3.
- Franz Wegner, *The Collatz Problem generalized to 3x+k*, arXiv:2101.08060
  (2021).
- Jeffrey C. Lagarias, *The 3x+1 Problem: An Overview*, in *The Ultimate
  Challenge: The 3x+1 Problem* (AMS, 2010), arXiv:2111.02635.
- `tangentproofs/eliahou-collatz-bounds`, a current public Lean
  formalization of Eliahou's ordinary-Collatz cycle bounds.
- Targeted web searches for leading-digit, decimal-digit, radix-dependent,
  digit-dependent, and generalized-Collatz formulations.

### Findings

The use of a cycle product identity together with continued fractions/Farey or
Diophantine approximation is **classical Collatz methodology**, not a novelty
claim of this project. Eliahou's 1993 result is especially close methodologically:
it combines a verified lower bound on a hypothetical cycle's minimum with
one-sided Diophantine approximation of `log_2 3` to force a large cycle
length. Simons--de Weger develops related cycle restrictions further.

Generalized `3x+k` systems with constant `k` are also established prior
art. They do not by themselves match the present state-dependent correction
`2L(n)+1`, where `L(n)` is the leading decimal digit.

The targeted search did not identify a published or formal theorem matching
the selected decimal-leading-digit recurrence and its conditional 971-state
bound. That is **negative search evidence only**. It does not establish
novelty, priority, or publication-worthiness by itself.

### Research audience and interest assessment

A plausible audience exists in generalized Collatz/Syracuse dynamics,
arithmetic dynamics, Diophantine cycle restrictions, and formalized
computational number theory. The selected result is a genuine restriction on
hypothetical cycles of a state-dependent digit-sensitive map; unlike the
rejected valuation-burst substitution, its content is the interaction between
a cyclic product identity, decimal leading-digit correction bounds, an explicit
minimum-scale hypothesis motivated by the separate census, and a Farey gap.

Whether this clears Palomar's editorial floor is ultimately Palomar's decision.
This repository records the positive mathematical case without claiming
novelty or treating formal verification alone as evidence of research
interest.

## Palomar tooling check

On 2026-09-26, the current `PalomarRegistry/PalomarSubmission` main commit is
still `a59f25bd8a66bf6faf3a4f4260d412989c0185ea`, the revision used by the
historical preflight. The current policy requires full mechanical replay with
Comparator, Lean's kernel, and the toolchain's independent NanoDa and con-ron
kernels. Predictive preflight does not itself run the editorial AI review.

The Stage-3B branch workflow is configured to run that current full predictive
preflight. Final owner resubmission must use the exact immutable commit that
passes it.
