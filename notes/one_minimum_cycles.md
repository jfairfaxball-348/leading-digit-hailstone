# Structured One-Minimum Accelerated Cycles

This note studies the structured cycle class targeted by Issue #10. It does **not** exclude arbitrary accelerated cycles.

Write the accelerated odd recurrence as

x_(i+1) = (3 x_i + c_i) / 2^(r_i),

where c_i = 2 L(x_i)+1 is in {3,5,...,19} and r_i = v2(3x_i+c_i).

Assume throughout this note that the cycle is written with its minimal period q, all odd states exceed 19, and the cycle has been rotated to x_0=M.

## Precise structured class

A **one-rise/one-fall cycle** is a cycle for which there are integers a,b >= 1, q=a+b, such that

- r_0=...=r_(a-1)=1;
- r_a,...,r_(q-1) >= 2.

Because every accelerated step above 19 is strictly increasing when r=1 and strictly decreasing when r>=2, this valuation-word condition is equivalent to the cyclic trajectory having exactly one strict local minimum and exactly one strict local maximum per period. Then

M=x_0 < x_1 < ... < x_a=H > x_(a+1) > ... > x_(q-1) > x_q=M.

The phrase "one minimum" by itself is **not** equivalent: a minimal-period cycle automatically has a unique global minimum unless two states repeat, but it can still have several intermediate local minima and maxima. The structured class is therefore defined by the one-rise/one-fall valuation word, or equivalently by exactly one local minimum and one local maximum.

## Exact rise block

For 0 <= i <= a, define

A_i = sum_(j=0)^(i-1) 3^(i-1-j) c_j 2^j,

with A_0=0. Then

2^i x_i = 3^i M + A_i.                                    (1)

Since 3 <= c_j <= 19 and

sum_(j=0)^(i-1) 3^(i-1-j)2^j = 3^i-2^i,

we obtain

3^i(M+3)-3*2^i <= 2^i x_i <= 3^i(M+19)-19*2^i.            (2)

Equivalently,

(3/2)^i(M+3)-3 <= x_i <= (3/2)^i(M+19)-19.

In particular H>(3/2)^a M.

## Exact fall block and backward envelope

Let

S = sum_(i=a)^(q-1) r_i

and, for 0 <= j <= b,

S_j = sum_(t=0)^(j-1) r_(a+t),

with S_0=0. Iterating the falling affine steps gives

2^S M
=
3^b H
+
sum_(j=0)^(b-1) 3^(b-1-j)c_(a+j) 2^(S_j).                (3)

Every term in the additive correction is positive.

More importantly, each falling step obeys a useful reverse inequality. If x_i -> x_(i+1) is falling, then r_i>=2, so

4 x_(i+1) <= 2^(r_i)x_(i+1)=3x_i+c_i <= 3x_i+19.

Hence

x_i-19 >= (4/3)(x_(i+1)-19).                              (4)

Iterating backward from M gives, for t=1,...,b,

x_(q-t) >= 19 + (4/3)^t (M-19).                          (5)

Thus states are forced away from the minimum geometrically on both sides of the unique turning pair.

## Fall-excess identity

Define the nonnegative fall excess

E = sum_(i=a)^(q-1) (r_i-2) >= 0.

Then

R = sum_i r_i = a + 2b + E = 2q-a+E.                    (6)

Equivalently,

a-E = 2q-R.                                               (7)

This is an exact combinatorial identity for the structured valuation word.

## Uniform product window — ELEMENTARY FACT

The exact cycle product identity is

2^R/3^q = product_i (1 + c_i/(3x_i)).                    (8)

For the rise-source states x_0,...,x_(a-1), positivity of the corrections gives

x_i > (3/2)^i M,

so

sum_(i=0)^(a-1) c_i/(3x_i)
<
(19/(3M)) sum_(i>=0) (2/3)^i
=
19/M.                                                      (9)

For the fall-source states, use (5). If t=q-i, then t>=1 and

x_i > (4/3)^t(M-19),

so

sum_(i=a)^(q-1) c_i/(3x_i)
<
(19/(3(M-19))) sum_(t>=1) (3/4)^t
=
19/(M-19).                                                 (10)

Put

sigma = 19/M + 19/(M-19).

When sigma<1, the elementary inequality

product_j (1+u_j) <= 1/(1-sum_j u_j)

for nonnegative u_j with sum_j u_j<1 gives the period-independent bound

1
<
2^R/3^q
<=
1/(1-sigma)
=
M(M-19)/(M^2-57M+361).                                   (11)

This is substantially sharper for the one-rise/one-fall class than the general-cycle bound

2^R/3^q <= (1+19/(3M))^q,

because the right-hand side of (11) does not grow with q.

For M=5,000,001, the exact rational upper bound is

24999914999982 / 24999725000305,

which is strictly less than 2. Therefore, for each fixed q, at most one integer R can satisfy (11): it must be the least integer with 2^R>3^q.

## Exact bounded consequence from the 5M census

The script

scripts/structured_one_minimum_bound.py

checks (11) using integer arithmetic only. Its recorded certificate is

data/structured_one_minimum_bound.json.

It verifies:

- q=1,...,79,334 are excluded by the structured uniform product window;
- q=79,335 is the first period not excluded by this necessary inequality;
- at q=79,335 the unique possible total valuation is R=125,743.

Therefore:

> **Bounded structured-cycle corollary.** Any different positive one-rise/one-fall accelerated cycle consistent with the exhaustive 5,000,000-seed census must contain at least 79,335 odd states.

This is not a global cycle exclusion, and q=79,335 is not asserted to be realizable.

Equation (6) also yields a rise-length consequence. Any such surviving structured cycle must have

a >= 32,927.

The exact certificate proves this uniformly for q>=79,335 by comparing the homogeneous lower ratio 2^(2q-a)/3^q with the rational bound (11). At the first surviving period,

q=79,335,  R=125,743,

so

a-E=32,927,

and therefore

a=32,927+E,
b=46,408-E,

with 0 <= E <= 46,407.

This sharply reduces the first surviving structured period to a family indexed by the distribution of fall excess valuations and the digit word, but it does not enumerate that family.

## Turning-point congruences

Let d=L(M). Since the outgoing minimum step has exact valuation 1,

3M+(2d+1) == 2 (mod 4).

Thus

- if d is odd, M == 1 (mod 4);
- if d is even, M == 3 (mod 4).

At the maximum H=x_a, let D=L(H). Its outgoing step has valuation at least 2, so

3H+(2D+1) == 0 (mod 4),

hence

- if D is odd, H == 3 (mod 4);
- if D is even, H == 1 (mod 4).

The same modulo-4 condition applies to the final falling source x_(q-1). For a prescribed exact valuation r and leading digit d, the existing 2-adic result gives one exact residue class modulo 2^(r+1); the congruences above are only the first local layer.

## Exact decimal consistency for a prescribed rise word

Suppose a proposed rise block has prescribed leading digits d_0,...,d_(a-1), and put c_j=2d_j+1. For each i, formula (1) fixes A_i from the previous digits.

If x_i is also required to have leading digit d_i and decimal exponent k_i, then exact digit consistency is

d_i 10^(k_i) <= x_i < (d_i+1)10^(k_i),

equivalently

2^i d_i 10^(k_i) - A_i
<=
3^i M
<
2^i (d_i+1)10^(k_i) - A_i.                              (12)

Thus each prescribed digit/decade choice cuts M to an explicit integer interval, and the complete rise word is feasible only if the intersection of all such intervals is nonempty.

The exact-r=1 requirements simultaneously impose the previously established unique binary lift for the fixed digit word. Hence a fully fixed rise digit/decade word can be checked by intersecting:

1. the exact decimal intervals (12);
2. the exact 2-adic residue class modulo 2^(a+1);
3. the lower bound M>=5,000,001.

This is an exact finite check **only after** the digit and decade ranges have themselves been proved complete. No unbounded word enumeration is claimed here.

## Research status

The one-rise/one-fall class is **substantially constrained, not globally excluded**.

The strongest new theorem-level ingredient is the period-independent product envelope (11). The strongest finite exact consequence is q>=79,335 under the existing 5M minimum premise, together with a>=32,927.

The next high-value target is to attack the first surviving period q=79,335 using its fixed R=125,743 and relation a-E=32,927, combining exact decimal interval consistency with exact 2-adic valuation lifting. A rigorous exclusion of that period would move the structured lower bound to the next admissible Diophantine period without pretending to cover arbitrary cycles.
