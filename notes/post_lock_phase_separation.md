# Post-Lock Boundary Separation and Phase/Residue Certificates

**Issue:** #10 — one-rise/one-fall structured accelerated cycles  
**Claim discipline:** theorem-level statements are separated from finite exact certificates. No novelty claim is made.

This note starts from PR #17. That increment proved the normalized post-lock corridor

`X < (2/3)^t x_t < X+19`

for positive post-lock times and showed that any disagreement with the homogeneous leading digit of `(3/2)^tX` requires a decimal boundary inside that fixed width-19 corridor. It also found, by complete exact computation through own-bit lock depth `B=220`, that every observed positive tail is already phase-frozen.

The new result here quantifies how sparse those exceptional boundary hits must be and then uses phase freezing to replace direct post-lock orbit following by a single 2-adic residue certificate.

## 1. Scaled boundary hits

Let

`C=d 10^k`, `d in {1,...,9}`

be a decimal leading-digit boundary. At post-lock time `t`, call `C` a scaled corridor hit if

`X 3^t < C 2^t < (X+19)3^t`.

Equivalently,

`X < C(2/3)^t < X+19`.

PR #17 already proves that a mismatch between the actual and homogeneous leading digit can occur only at such a hit.

## 2. Exact separation theorem

Assume `X>38`. Suppose hits occur at times `s<t`, with boundaries

`C_s=d10^k`,
`C_t=e10^l`.

Put `n=t-s` and

`z_s=C_s(2/3)^s`,
`z_t=C_t(2/3)^t`.

Both lie in `(X,X+19)`. Since

`z_t/z_s > X/(X+19) > 2/3`,

we have

`C_t/C_s=(z_t/z_s)(3/2)^n>1`.

Hence `C_t>C_s`, so `l>=k`. Write `m=l-k>=0`. Then

`z_t/z_s = e 10^m 2^n / (d 3^n)`.

If `z_t != z_s`, the numerator and denominator on the right are distinct positive integers. Therefore

`|z_t/z_s-1| >= 1/(d3^n) >= 1/(9*3^n)`.

But the two scaled hits lie in one interval of width 19, so

`|z_t/z_s-1| < 19/X`.

Combining the inequalities gives

`X < 171*3^n`.

Using a non-strict outer version gives the convenient statement

> **Scaled-boundary separation theorem.** If two distinct scaled decimal-boundary hits occur `n` steps apart, then `X<=171*3^n`.

No equidistribution statement is used; this is exact rational separation.

Define

`g(X)=min{n>=1 : X<=171*3^n}`.

Then distinct hit values cannot recur at a smaller positive gap.

## 3. Exact coincident hits

The only exception is equality `z_t=z_s`, which is equivalent to

`e 2^n 10^m = d3^n`.

The complete solutions with `d,e in {1,...,9}`, `n>=1`, `m>=0` are

- gap 1: `2->3`;
- gap 1: `4->6`;
- gap 1: `6->9`;
- gap 2: `4->9`.

Thus exact coincidences form only the short chains `2->3` and `4->6->9`.

For `n>=3`, divisibility by `2^n` forces the one-digit factor `d` to absorb too many powers of two; the only borderline case `n=3,d=8` would require `e=27`, impossible for a decimal leading digit. The cases `n=1,2` give the list above directly.

## 4. Phase-frozen digit words reduce to one residue

Suppose the corridor has no scaled decimal-boundary hit at times `1,...,h-1`. Then PR #17 forces the actual leading digits, conditional on exact-r=1 survival, to equal the homogeneous digits of

`X,(3/2)X,...,(3/2)^(h-1)X`.

For that fixed word `d_0,...,d_(h-1)`, the already established terminal congruence says that all `h` exact-r=1 parity conditions are equivalent to one starting residue modulo `2^(h+1)`.

Therefore a phase-frozen candidate can be certified without following its true post-lock orbit:

1. verify there is no scaled boundary hit;
2. read the exact homogeneous digit word;
3. compute the unique required residue for that word;
4. compare with `X mod 2^(h+1)`.

The first mismatch proves the tail cannot reach length `h`.

This is a finite candidate-specific certificate. It is not a uniform bound on all post-lock tails.

## 5. Exact certificates for the current lock states

The script `scripts/post_lock_phase_separation.py` reproduces three current examples.

For

`X=2,225,217,764,551,392,093,807`,

the forced word through failure is `2357`. The first three prefix residues match; the fourth fails. Thus the post-lock tail is exactly 3. The noncoincident boundary-gap threshold is `g(X)=41`.

For

`X=3,337,826,646,827,088,140,713`,

the forced word is `357`; the third prefix fails, giving exact tail 2. Again `g(X)=41`.

For the tail-6 lock state

`X=12,166,406,006,866,046,930,622,304,922,581`,

the forced word through failure is `1124691`. The first six prefixes match. At length 7 the required residue is 85 modulo 256, while

`X mod 256 = 213`.

Hence the exact-r=1 post-lock tail is 6. Here `g(X)=61`.

Direct deterministic iteration is retained in the machine-readable certificate only as an independent cross-check.

## 6. What this proves and what remains open

This increment adds a genuine scale-aware theorem:

- exceptional decimal-phase ambiguity values are separated by a gap growing like `log X`, apart from explicitly classified short exact coincidences.

It also gives a reusable finite termination method:

- phase-frozen blocks reduce to one exact terminal 2-adic congruence.

It does **not** prove an explicit `F(B)` or `F(M)` bound on total post-lock tail length. PR #17 already showed that the observed positive tails through `B=220` need no boundary hit at all, so the main obstruction has moved to parity/congruence along long homogeneous digit words.

The next theorem target is therefore:

> prove a scale-aware upper bound on the length of a homogeneous `(3/2)^t` leading-digit word that can keep matching the required 2-adic residue prefixes.

The structured frontier remains unchanged:

`q>=1,643,749,725,074`,
`a>=682,217,775,335`

under the existing 5,000,000 minimum premise. The arbitrary-cycle bound remains separately `q>=971`.
