# Residue-Position Locking and Binary Lift Coordinates

**Issue:** #10 — one-rise/one-fall structured accelerated cycles  
**Claim discipline:** theorem-level statements are separated from finite exact symbolic/direct diagnostics. No novelty claim is made.

## 1. Fixed rise word and decimal cell

Fix a prescribed leading-digit word

\[
w=(d_0,\ldots,d_{s-1}),\qquad d_i\in\{1,\ldots,9\},
\]

write \(c_i=2d_i+1\), and set \(A_0=0\),

\[
A_{i+1}=3A_i+c_i2^i.
\]

Along prescribed exact-\(r=1\) rises,

\[
2^i x_i=3^iM+A_i.
\]

The established fixed-word congruence is

\[
M\equiv \rho_s(w)
:=3^{-s}(2^s-A_s)\pmod{2^{s+1}},
\]

with canonical representative \(0\le\rho_s<2^{s+1}\).

If the digit word is augmented with decade exponents \(k_i\), so that

\[
d_i10^{k_i}\le x_i\le(d_i+1)10^{k_i}-1,
\]

then the exact **pure decimal-consistency interval** is

\[
I_s(w)=[L_s(w),U_s(w)],
\]

where

\[
L_s(w)=
\max_{0\le i<s}
\left\lceil
\frac{2^i d_i10^{k_i}-A_i}{3^i}
\right\rceil,
\]

and

\[
U_s(w)=
\min_{0\le i<s}
\left\lfloor
\frac{2^i((d_i+1)10^{k_i}-1)-A_i}{3^i}
\right\rfloor.
\]

The repository's implementation cells can be slightly narrower because they preserve an already selected binary residue while splitting endpoint sectors. They should not be identified with the pure decimal interval.

Also,

\[
\frac{A_i}{3^i}
=
\frac13\sum_{j=0}^{i-1}c_j\left(\frac23\right)^j.
\]

Since \(3\le c_j\le19\),

\[
3\left(1-\left(\frac23\right)^i\right)
\le
\frac{A_i}{3^i}
\le
19\left(1-\left(\frac23\right)^i\right).
\]

Thus every decimal endpoint is a homogeneous scaled boundary plus an explicitly bounded additive displacement smaller than 19.

## 2. Exact one-bit lift recurrence

Define

\[
H_s=
\frac{3^s\rho_s+A_s-2^s}{2^{s+1}}.
\]

This is integral by the residue congruence.

### Proposition 1 — exact lift bit

When digit \(d_s\) is appended, there is a unique \(b_s\in\{0,1\}\) such that

\[
\boxed{\rho_{s+1}=\rho_s+b_s2^{s+1}},
\]

and it is determined by

\[
\boxed{b_s\equiv1+H_s+d_s\pmod2}.
\]

The carry coordinate satisfies

\[
\boxed{
H_{s+1}
=
\frac{1+3H_s+d_s+b_s3^{s+1}}2
}.
\]

### Proof

The defining equation gives

\[
3^s\rho_s+A_s=2^s+H_s2^{s+1},
\]

so the depth-\(s\) state for the lower lift is \(x_s=1+2H_s\). Its next odd numerator is

\[
3x_s+(2d_s+1)=2(2+3H_s+d_s).
\]

Exact valuation 1 requires the quotient in parentheses to be odd. The other possible start lift, \(\rho_s+2^{s+1}\), changes \(x_s\) by \(2\cdot3^s\), hence changes that quotient by the odd number \(3^{s+1}\). Exactly one lift works. Its parity is the displayed condition for \(b_s\), and substitution gives the carry recurrence. \(\square\)

## 3. Lift bits are binary digits

Starting from \(\rho_0=1\), Proposition 1 gives

\[
\boxed{
\rho_s
=
1+\sum_{j=0}^{s-1}b_j2^{j+1}
}.
\]

The lift choices are therefore exactly the successive binary digits of the required start residue above its forced least-significant bit.

For

\[
\theta_s=\frac{\rho_s}{2^{s+1}},
\]

the recurrence becomes

\[
\boxed{\theta_{s+1}=\frac{\theta_s+b_s}{2}}.
\]

The dyadic coordinate itself is simple; the difficulty is the correlation between decimal-sector choices and the selected lift bits.

## 4. Exact residue-cell discrepancy

For a decimal cell \([L,U]\), modulus \(m=2^{s+1}\), and residue \(\rho_s\), the first representative at or above \(L\) is

\[
R_s=
\rho_s+
m\left\lceil\frac{L-\rho_s}{m}\right\rceil.
\]

Compatibility is exactly \(R_s\le U\). If \(U-L<m\), the representative is unique. Defining

\[
\Delta_s=R_s-L,
\]

compatibility is equivalent to

\[
0\le\Delta_s\le U-L.
\]

This restates the PR #13 obstruction precisely: sub-modulus cell width gives uniqueness, not exclusion.

## 5. Bit-length locking theorem

Let

\[
B(U)=\lfloor\log_2U\rfloor,
\]

so

\[
2^{B(U)}\le U<2^{B(U)+1}.
\]

### Theorem 2 — bounded-range residue locking

Suppose \(1\le M\le U\) realizes \(B=B(U)\) prescribed exact-\(r=1\) rises. Then

\[
\boxed{M=\rho_B}.
\]

If that same start extends through further exact-\(r=1\) rises, then every later lift bit is zero:

\[
\boxed{b_B=b_{B+1}=\cdots=0}.
\]

Hence \(\rho_{B+t}=M\) throughout every compatible continuation.

### Proof

The fixed-word theorem gives

\[
M\equiv\rho_B\pmod{2^{B+1}}.
\]

Both numbers lie in \([0,2^{B+1})\): \(M\le U<2^{B+1}\) and \(\rho_B\) is the canonical residue. Therefore \(M=\rho_B\).

The next two lifts are \(M\) and \(M+2^{B+1}\). The second exceeds \(U\), so only the zero lift can retain the same bounded start. The same argument repeats at all later depths. \(\square\)

This is a deterministic residue-position theorem. At the bit-length threshold, modular translation ambiguity disappears completely.

The remaining question is sharper:

> How long can an admissible decimal word continue to select the zero lift after its starting integer has become fully determined?

## 6. Candidate compression at locking depth

The existing boundary-localization theorem gives at most

\[
20J_s(L,U)+1
\]

decimal-sector words through depth \(s\). At \(s=B(U)\), Theorem 2 gives at most one start per word, so

\[
\boxed{N_B(L,U)\le20J_B(L,U)+1}.
\]

There is also an explicit elementary bound on \(J_s\). At any depth, the relevant scaled decimal boundaries lie in an interval whose endpoint ratio is at most

\[
\frac{U+19}{L}.
\]

That interval meets at most

\[
\left\lceil\log_{10}\frac{U+19}{L}\right\rceil+1
\]

decimal decades, each with at most nine leading-digit boundaries. Thus

\[
\boxed{
J_s(L,U)
\le
9s\left(
\left\lceil\log_{10}\frac{U+19}{L}\right\rceil+1
\right).
}
\]

Therefore

\[
\boxed{
N_B(L,U)
\le
180B\left(
\left\lceil\log_{10}\frac{U+19}{L}\right\rceil+1
\right)+1.
}
\]

For fixed \(L\), this is \(O((\log U)^2)\). It is candidate compression, not an extinction law.

## 7. Exact diagnostics on already processed ranges

The companion script "scripts/residue_position_locking.py" applies this theorem to the existing record-chain ranges only. It does not certify another Farey record.

For the largest processed range,

\[
5{,}000{,}001\le M\le42{,}285{,}421{,}502{,}900,
\]

the locking depth is \(B=45\), because

\[
2^{46}=70{,}368{,}744{,}177{,}664>U.
\]

The explicit theorem bound gives at most 64,801 starts at lock depth. Complete exact symbolic coverage leaves exactly two:

\[
26{,}501{,}219{,}601{,}103,\qquad
39{,}751{,}829{,}401{,}657.
\]

Direct exact continuation gives:

- 48 total exact-\(r=1\) rises for the first, a post-lock zero-lift tail of length 3, then valuation 2;
- 47 total exact-\(r=1\) rises for the second, a post-lock zero-lift tail of length 2, then valuation 2.

For the processed range with \(U=21{,}238{,}350{,}355\), lock depth is 34. Exactly one start survives to lock,

\[
16{,}670{,}166{,}793,
\]

and its next valuation is 2.

For the known depth-48 terminal representative, the complete lift-bit word, from low binary positions upward, is

"111001101010011111000111101001001011000000110000".

It reconstructs the exact residue/start \(26{,}501{,}219{,}601{,}103\).

Everything in this section is **FINITE EXACT SYMBOLIC ENUMERATION / FINITE DIRECT COMPUTATION** attached to the proved locking mechanism. These diagnostics do not strengthen the existing structured period lower bound.

## 8. Counter-obstruction to a range-independent finite-state extinction proof

The repository already proves that, for every \(m\), some positive odd start has at least \(m\) initial exact-\(r=1\) rises.

Therefore any finite directed graph that exactly encodes all admissible rise prefixes using only range-independent finite state has paths of arbitrarily large length. Any finite directed graph with arbitrarily long paths contains a directed cycle, equivalently a reachable strongly connected component supporting indefinite graph paths.

So a sound **range-independent finite acyclic transition obstruction** cannot eliminate all sufficiently long rise words.

A finite-state method is not ruled out, but it must retain scale/range information, an unbounded monotone coordinate, or another mechanism preventing a graph cycle from falsely representing indefinite bounded-range continuation.

## 9. Current mathematical status

### Proved in this increment

- exact one-bit residue update and carry recurrence;
- lift bits are the binary digits of the required start residue;
- normalized dyadic update;
- explicit pure decimal-cell endpoint formulas;
- bounded-range bit-length locking;
- explicit polylogarithmic candidate compression at lock depth;
- a counter-obstruction to a purely range-independent finite acyclic transition proof.

### Not proved

No explicit general bound

\[
s_{\max}(X)\le f(X)
\]

has been obtained. In particular, no logarithmic or sublinear finite-range rise bound follows from locking alone.

The unresolved task is to bound the **zero-lift tail after bit-length locking** strongly enough to compare with the required rise length in the structured cycle argument.

Accordingly:

- the one-rise/one-fall class is still only finitely excluded through \(q=890{,}638{,}885{,}192\) under the 5M minimum premise;
- the arbitrary-cycle bound remains separately \(q\ge971\);
- no universal-convergence claim is strengthened;
- the Farey/product side should now be treated as essentially sufficient for this structured attack unless a residue-tail theorem needs another record as a test case.
