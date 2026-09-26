# Arbitrarily Long Weak-Division Runs

**Claim type: ELEMENTARY FACT.**

Write the accelerated odd map as

[
A(n)=rac{3n+2L(n)+1}{2^{v_2(3n+2L(n)+1)}}.
]

A growth-favouring accelerated step has exact valuation (v_2=1), so it is locally

[
nmapsto rac{3n+2L(n)+1}{2}approx rac32n.
]

## Proposition

For every integer (mge 1), there exists a positive odd starting value whose first (m) accelerated steps all have exact valuation (v_2=1).

Equivalently, there is no uniform finite bound on the number of consecutive initial weak-division steps.

## Proof

Fix (m).

First choose a positive real number (a) such that none of

[
(3/2)^i a,qquad 0le ile m,
]

lies on a decimal leading-digit boundary (d10^j), with (din{1,ldots,9}). Only finitely many boundary preimages matter for fixed (m), so such an (a) exists. Shrinking to a small open interval (I) around (a), the leading digit of ((3/2)^i x) is constant on (I) for every (0le i<m). Call these digits (d_0,ldots,d_{m-1}).

Now temporarily prescribe those digits and suppose every accelerated valuation is (1). Define

[
x_{i+1}=rac{3x_i+(2d_i+1)}2.
]

There is exactly one odd residue class modulo (2^{m+1}) for (x_0) that makes (x_1,ldots,x_m) all odd.

This follows inductively. For (m=0), (x_0) is simply odd modulo (2). Suppose the first (j) weak-division conditions determine one class modulo (2^{j+1}). Its two lifts modulo (2^{j+2}) differ by (2^{j+1}). After (j) forced weak-division steps, the corresponding (x_j) values differ by (2cdot 3^j), hence by (2pmod 4). Since (2d_j+1) is odd, exactly one of those two lifts satisfies

[
3x_j+(2d_j+1)equiv2pmod4,
]

which is exactly (v_2(3x_j+2d_j+1)=1). Thus one lift survives at each stage.

Finally scale the interval by (10^k). Its length tends to infinity, so for sufficiently large (k), the interval (10^k I) contains an integer from the required residue class modulo (2^{m+1}). The forced affine orbit differs from the homogeneous orbit ((3/2)^i x_0) only by an additive quantity depending on (m), while the scale is (10^k). For sufficiently large (k), all first (m) states therefore stay in the prescribed leading-digit sectors (d_i). The prescribed corrections are consequently the actual corrections of the frozen map, and all first (m) accelerated valuations are exactly (1).

Hence arbitrarily long initial runs of exact valuation (1) exist. (square)

## Consequence for the conjecture

This does **not** imply divergence. It shows that one obvious proof strategy cannot work: there is no global constant (B) such that every trajectory is forced to receive a valuation (v_2ge2) within (B) accelerated steps.

Any successful descent argument has to tolerate arbitrarily long local stretches whose dominant multiplier is (3/2>1).

## Constructive examples

The accompanying script `scripts/construct_low_v2_runs.py` implements the one-bit-at-a-time residue lift for a fixed safe mantissa (a=7/3). It constructs explicit starts with at least 30, 50, and 100 initial exact-(v_2=1) accelerated steps and then follows those finite examples under the frozen map.

Those trajectory outcomes are **FINITE COMPUTATION** and are separate from the elementary existence proof above.
