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

x_i >= (3/2)^i M, with strict inequality for i>0,

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

## Exact bounded consequences from the 5M census

The script

scripts/structured_one_minimum_bound.py

first checks (11) using integer arithmetic only.

At M=5,000,001, the product-window survivors through q=400,000 are exactly:

| q | R | required a >= 2q-R |
|---:|---:|---:|
| 79,335 | 125,743 | 32,927 |
| 158,670 | 251,486 | 65,854 |
| 190,537 | 301,994 | 79,080 |
| 269,872 | 427,737 | 112,007 |
| 349,207 | 553,480 | 144,934 |
| 381,074 | 603,988 | 158,160 |

This enumeration is exact. A safe 17-bit integer prefilter is used only to skip values that cannot possibly meet the rational window; every retained possibility is decided by the full cross-multiplied integer inequality.

### Each surviving q forces a finite minimum range

For fixed q and R, inequality (11) becomes an upper bound on M because

B(M)=M(M-19)/(M^2-57M+361)

is strictly decreasing on the relevant range. An exact discrete check is

N(M+1)D(M)-N(M)D(M+1)
=
-38(M^2-18M+171)
<
0,

where N(M)=M(M-19) and D(M)=M^2-57M+361.

Therefore each product-window survivor has a largest possible minimum M_max. Exact binary search gives:

| q | M_max |
|---:|---:|
| 79,335 | 10,369,168 |
| 158,670 | 5,184,598 |
| 190,537 | 589,078,792 |
| 269,872 | 10,189,804 |
| 349,207 | 5,139,366 |
| 381,074 | 294,539,410 |

These are theorem-driven finite ranges, not arbitrary search cutoffs.

### Exact decimal-sector / 2-adic symbolic exclusion

The script then checks whether any odd M in

5,000,001 <= M <= M_max

can sustain the required initial r=1 rise block.

It does **not** enumerate every seed. It maintains cells of initial M values for which:

- the current rise digit word is fixed;
- the exact affine formula
  2^i x_i = 3^i M + A_i
  is fixed;
- M lies in one exact residue class modulo 2^(i+1).

At each step, every cell is split across every decimal leading-digit sector intersecting the affine image interval. For each resulting sector, the two lifts modulo 2^(i+2) are tested, and only the unique lift giving exact valuation r=1 is retained.

Thus the symbolic procedure is exactly the intersection described in (12): decimal interval consistency plus exact binary lifting. If the cell set becomes empty after s steps, no seed in the complete stated M range has s consecutive r=1 accelerated steps.

For the six product-window survivors above, the first impossible rise lengths are:

| q | required rise length | first impossible rise length |
|---:|---:|---:|
| 79,335 | 32,927 | 21 |
| 158,670 | 65,854 | 17 |
| 190,537 | 79,080 | 29 |
| 269,872 | 112,007 | 21 |
| 349,207 | 144,934 | 17 |
| 381,074 | 158,160 | 28 |

Every product-window survivor through q=400,000 is therefore excluded.

> **Finite structured-cycle corollary.** Any different positive one-rise/one-fall accelerated cycle consistent with the exhaustive 5,000,000-seed census must have q>=400,001.

This is an explicitly bounded structured-class exclusion, not a global no-cycle theorem.

There is also a uniform rise-length consequence. Because the structured product bound is <2, any surviving q has the unique possible total valuation

R = bit_length(3^q).

Multiplying 3^q by 3 changes this bit length by either 1 or 2, so

k(q)=2q-R

is nondecreasing. At q=400,001,

k(400,001)=166,015.

Hence every remaining structured cycle under the same census premise must have at least

a>=166,015

consecutive exact-r=1 rise steps.

The machine-readable certificate is

data/structured_one_minimum_bound.json.

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

## Prior-art status of this structured theorem

The general strategy of forcing close powers-of-two / powers-of-three approximation from a hypothetical Collatz-type cycle is classical; the project already records Eliahou and Simons–de Weger as methodological prior art.

The theorem-specific historical question is narrower: whether the state-dependent leading-digit corrections have previously been combined with one-rise/one-fall geometry to obtain the period-independent envelope (11), or with exact decimal-sector / 2-adic symbolic lifting to obtain a bounded structured-cycle exclusion of this form.

That theorem-specific question has **not** received a final prior-art determination. No claim of novelty, originality, uniqueness, or priority is made here. It should be included explicitly in the final theorem-level prior-art audit.

## Research status

The one-rise/one-fall class is **excluded through q=400,000 under the existing 5M minimum premise, but not globally excluded**.

The strongest theorem-level ingredient is the period-independent product envelope (11). The strongest finite exact consequence combines that theorem with exact product-window enumeration and exact symbolic decimal/2-adic rise-word coverage to give q>=400,001 and a>=166,015.

The next high-value target is to extend the exact structured exclusion beyond q=400,000 without turning the period scan into an undirected computation. The preferred route is to enumerate the next Diophantine product-window survivors and use their theorem-derived M_max ranges with the same exact symbolic digit/residue checker; if a survivor ceases to be eliminated quickly, analyze that specific word family mathematically.
