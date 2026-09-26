# Farey Record Scaling and Finite-Range Symbolic Complexity

**Status:** theorem-level elementary analysis plus finite exact rational arithmetic and finite exact symbolic computation.

This note continues Issue #10. It does not prove the Leading-Digit Hailstone Conjecture and does not globally exclude one-rise/one-fall cycles.

## 1. Exact logarithmic certification without giant powers

Put

\[
\alpha=\log_2 3.
\]

For \(x>1\), set \(z=(x-1)/(x+1)\). Then

\[
\log x
=
2\sum_{k\ge0}\frac{z^{2k+1}}{2k+1}.
\]

After \(N\) terms, positivity gives the exact tail bound

\[
0<
\log x-
2\sum_{k=0}^{N-1}\frac{z^{2k+1}}{2k+1}
\le
\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

For rational \(x\), both endpoints are rational. Exact rational enclosures for
\(\log 2\) and \(\log 3\) therefore give an exact rational enclosure for
\(\alpha\). This certifies whether a candidate \(R/q\) lies above or below
\(\alpha\), and it certifies product-window inequalities after taking logs,
without materializing \(3^q\) for the very large later records.

As an independent regression, the first new record
\[
(q,R)=(64,497,107,102,225,496)
\]
is also checked directly with integer arithmetic: \(3^q\) has bit length
\(R\), hence
\[
2^{R-1}\le 3^q<2^R.
\]
Thus
\[
R=\lceil q\alpha\rceil
\quad\text{and}\quad
2^R>3^q.
\]

The exact product-window maximum at this record is

\[
M_{\max}=4,350,616,725.
\]

## 2. Record-to-record growth bound

Let \(R/q>\alpha\) be an upper Farey neighbour, and let \(r/s<\alpha\)
be the final lower neighbour immediately before the next upper record. Thus

\[
Rs-rq=1.
\]

Write

\[
\delta=R-q\alpha>0,
\qquad
\eta=s\alpha-r>0.
\]

Then the determinant identity is exactly

\[
s\delta+q\eta=1.
\]

The next mediant upper record is

\[
\frac{R+r}{q+s}>\alpha,
\]

so \(\delta-\eta>0\). Hence

\[
1=s\delta+q\eta
<
(s+q)\delta.
\]

If \(q_{\rm next}=q+s\), then

\[
\boxed{\delta>\frac1{q_{\rm next}}.}
\]

Now the structured product envelope gives

\[
2^\delta
\le
B(M)
=
\frac{M(M-19)}{M^2-57M+361}.
\]

For \(M>57\),

\[
B(M)-1
=
\frac{38M-361}{M^2-57M+361}
<
\frac{38}{M-57}.
\]

Also \(2^\delta-1>\delta\log 2\). Therefore

\[
\frac{\log 2}{q_{\rm next}}
<
\delta\log 2
<
\frac{38}{M-57},
\]

and so every structured-cycle minimum at this record satisfies

\[
\boxed{
M<57+\frac{38q_{\rm next}}{\log 2}.
}
\]

This is a theorem-level record-to-record growth bound. It does not by itself
control \(q_{\rm next}/q\), so it is not yet an asymptotic exclusion.

## 3. Normalized weak-run strip

Suppose

\[
x_{i+1}=\frac{3x_i+c_i}{2},
\qquad
3\le c_i\le19,
\]

for \(s\) consecutive exact-\(r=1\) rises, with \(x_0=M\). The exact affine
formula gives

\[
\left(\frac23\right)^i x_i
=
M+
\frac13\sum_{j=0}^{i-1}
c_j\left(\frac23\right)^j.
\]

Define

\[
\beta_i=
\left(\frac23\right)^i x_i-M.
\]

Since \(3\le c_j\le19\),

\[
3\left(1-\left(\frac23\right)^i\right)
\le
\beta_i
\le
19\left(1-\left(\frac23\right)^i\right).
\]

Therefore the uncertainty width in normalized coordinates is

\[
\boxed{
\operatorname{width}(\beta_i)
\le
16\left(1-\left(\frac23\right)^i\right)
<16.
}
\]

This is finite-range symbolic structure, not a global bound on the length of
weak runs.

## 4. Linear bound on decimal-sector words and symbolic cells

Fix a finite starting interval

\[
L\le M\le U.
\]

A decimal leading-digit boundary has the form \(b=d10^k\), with
\(d\in\{1,\ldots,9\}\). At depth \(i\), its normalized location is

\[
t=b\left(\frac23\right)^i.
\]

Because the possible \(\beta_i\)-values occupy an interval of width less
than 16, the digit at depth \(i\) can depend on the correction history only
when \(M\) lies in a boundary-preimage strip of width less than 16.

Only boundaries whose normalized locations meet \([L,U+19]\) can matter.
Let

\[
D=
9\left(
\left\lceil\log_{10}\frac{U+19}{L}\right\rceil+2
\right).
\]

This is a safe upper bound for the number of relevant decimal boundaries at
each depth. Across \(s\) rise steps there are at most \(N=sD\) ambiguity
strips.

The union of \(N\) intervals of width less than 16 contains at most \(16N\)
integer seeds when counted strip-by-strip. Its complement has at most
\(N+1\) connected components, and on each such component every one of the
first \(s\) decimal sectors is forced and constant. Hence the number of
possible complete decimal-sector words is at most

\[
\boxed{17sD+1.}
\]

For a fixed complete sector word, the affine formulas are fixed; intersecting
the sector constraints gives at most one interval in \(M\), and the exact
\(r=1\) conditions give one residue class modulo \(2^{s+1}\). Therefore the
same bound applies to the number of symbolic decimal-sector / binary-lift
cells:

\[
\boxed{
\#\text{cells after }s\text{ rises}\le17sD+1.
}
\]

This proves linear growth in \(s\) for every fixed finite multiplicative
range \([L,U]\).

A second consequence is residue sparsification. If

\[
2^{s+1}>U-L,
\]

then each surviving cell contains at most one admissible seed. At such a
depth the entire surviving set has at most \(17sD+1\) seeds. Taking
\(s=O(\log U)\) therefore reduces a fixed finite range to only
\(O((\log U)^2)\) terminal candidates.

What is *not* proved is that those candidates must miss the next binary lift.
That residue-position problem is the remaining asymptotic obstruction.

## 5. Exact record chain and finite exclusion

Starting from the PR #12 bracket

\[
\frac{17,087,915}{10,781,274}
>
\alpha
>
\frac{85,137,581}{53,715,833},
\]

exact Stern-Brocot/Farey iteration gives the following upper records. Each
listed \(M_{\max}\) is exact. The symbolic extinction depth means that no
odd \(M\) in the complete interval
\([5,000,001,M_{\max}]\) sustains that many consecutive exact-\(r=1\)
rises.

| upper \(q\) | \(R\) | next upper \(q\) | \(M_{\max}\) | required \(a\ge2q-R\) | first impossible rise | peak cells |
|---:|---:|---:|---:|---:|---:|---:|
| 64,497,107 | 102,225,496 | 118,212,940 | 4,350,616,725 | 26,768,718 | 31 | 276 |
| 118,212,940 | 187,363,077 | 171,928,773 | 7,221,856,344 | 49,062,803 | 31 | 301 |
| 171,928,773 | 272,500,658 | 397,573,379 | 21,238,350,355 | 71,356,888 | 35 | 350 |
| 397,573,379 | 630,138,897 | 6,586,818,670 | 359,020,668,782 | 165,007,861 | 38 | 485 |
| 6,586,818,670 | 10,439,860,591 | 72,057,431,991 | 3,753,781,445,604 | 2,733,776,749 | 41 | 603 |
| 72,057,431,991 | 114,208,327,604 | 137,528,045,312 | 6,895,437,822,163 | 29,906,536,378 | 41 | 636 |
| 137,528,045,312 | 217,976,794,617 | 890,638,885,193 | 42,285,421,502,900 | 57,079,296,007 | 49 | 727 |

The lower-neighbour updates between successive upper records are also exact.
In particular, the record at \(q=397,573,379\) survives fifteen successive
lower mediants before the next upper record appears; no period-by-period scan
is used.

Combining the exact record blocks with their complete symbolic extinction
certificates gives:

> **Finite structured-cycle corollary.** Under the existing
> \(M\ge5,000,001\) premise, any different positive one-rise/one-fall
> accelerated cycle has
>
> \[
> \boxed{q\ge890,638,885,193}.
> \]
>
> At the first uncovered upper record,
> \[
> R=1,411,629,234,715,
> \]
> so every remaining structured cycle has
> \[
> \boxed{a\ge369,648,535,671}.
> \]

The arbitrary-cycle bound remains \(q\ge971\). These statements must not be
combined.

## 6. Mechanism diagnosis

The decimal/binary squeeze continues rather than failing. Across the seven
new certified record ranges:

- \(M_{\max}\) grows from about \(4.35\times10^9\) to
  \(4.23\times10^{13}\);
- the required rise length grows from \(2.68\times10^7\) to
  \(5.71\times10^{10}\);
- exact symbolic extinction depth grows only from 31 to 49;
- the peak exact cell count grows only from 276 to 727.

The new theorem explains why exponential branching is not occurring: for a
fixed finite range, normalized weak-run uncertainty is confined to
width-\(<16\) boundary strips, giving a linear cell-count bound.

However, this does **not** prove a maximum weak-run length
\(C\log M+O(1)\). Once the residue modulus dominates the finite interval,
a polynomially small set of isolated representatives can still survive in
principle. The current certificates eliminate those representatives by exact
calculation, but no theorem yet forces the miss uniformly from record to
record.

Therefore the Farey/continued-fraction method is now a genuine
record-to-record framework, but the global structured-class result remains a
sequence of finite certificates rather than an asymptotic proof.

## 7. Highest-value next target

Prove a uniform **residue-position obstruction** for the sparse terminal
representatives after \(2^{s+1}>U-L\): use the decimal-sector word, affine
formula, and lifted residue to show that beyond an explicit logarithmic depth,
the required next lift cannot remain inside its permitted boundary component.

That is more valuable than extending the finite Farey chain again.
