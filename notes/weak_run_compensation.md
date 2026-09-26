# Weak-Run Growth and One-Step Compensation

**Claim type: ELEMENTARY FACTS.**

This note refines the obstruction created by arbitrarily long accelerated runs with exact v2=1.

Write an accelerated odd step as

x_(i+1) = (3x_i+c_i)/2^(r_i),

where

c_i = 2L(x_i)+1 in {3,5,7,9,11,13,15,17,19}.

## Exact formula for a weak run

Suppose the first s accelerated steps all have exact valuation r_i=1. Then

x_(i+1) = (3x_i+c_i)/2

for i=0,...,s-1.

Iterating gives

2^s x_s
=
3^s x_0
+
sum_(j=0)^(s-1) 3^(s-1-j)c_j 2^j.             (1)

This follows by induction on s.

Since 3<=c_j<=19 and

sum_(j=0)^(s-1) 3^(s-1-j)2^j = 3^s-2^s,

equation (1) gives the exact integer bounds

3^s(x_0+3) - 3*2^s
<=
2^s x_s
<=
3^s(x_0+19) - 19*2^s.                          (2)

In particular,

x_s > (3/2)^s x_0.

Thus a weak run of length s produces at least the homogeneous multiplicative growth (3/2)^s; the bounded digit correction only increases the state further.

## One-step compensation requirement

Now suppose the next accelerated step has valuation r>=2:

x_(s+1) = (3x_s+c_s)/2^r.

Assume this single step returns to or below the height before the weak run:

x_(s+1) <= x_0.

Then

2^r x_0
>=
2^r x_(s+1)
=
3x_s+c_s
>
3x_s
>
(3^(s+1)/2^s)x_0.

Since x_0>0, cancellation gives the necessary condition

2^(r+s) > 3^(s+1).                               (3)

Equivalently,

r > (s+1) log_2(3) - s.

No logarithms are needed to apply the result: the power inequality (3) is exact.

## Examples of the threshold

The smallest integer r satisfying (3) is:

- s=10: r>=8;
- s=30: r>=20;
- s=50: r>=31;
- s=100: r>=61.

These examples do not say that such a compensating step must occur. They state only what its valuation would have to be if one single step is to undo the entire preceding weak run.

## Structured multi-step compensation now available in the cycle setting

For the one-rise/one-fall cycle class of Issue #10, the multi-step fall block can be controlled in reverse. Every falling step satisfies

x_i - 19 >= (4/3)(x_(i+1)-19).

Together with the forward rise bound, this forces states away from the cycle minimum geometrically on both sides of the unique turning pair. Inserting those state lower bounds into the exact cycle product identity yields the period-independent envelope

1 < 2^R/3^q <= M(M-19)/(M^2-57M+361).

This is a genuine block-compensation theorem for the structured cycle problem; it is **not** a theorem that arbitrary forward weak runs must be followed by a comparable monotone fall block. See notes/one_minimum_cycles.md.

## Interpretation

The arbitrary-length weak-run theorem rules out a bounded waiting-time proof for r>=2.

The present lemma shows more: a proof based on "eventual strong division" must quantitatively match the length of the preceding weak run. Long growth stretches require correspondingly large one-step valuations to erase them immediately.

This points toward two more realistic descent strategies:

1. prove that a long weak run forces a later large valuation through digit/residue constraints; or
2. allow several descending accelerated steps and prove a blockwise compensation inequality.

Neither statement is currently proved.
