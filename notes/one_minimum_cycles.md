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

## Farey-neighbour block transfer — ELEMENTARY FACT + FINITE EXACT CERTIFICATE

Put alpha=log_2(3). Because the structured product bound is strictly less than 2, a product-window survivor at period q has the unique possible total valuation

R(q)=ceil(q alpha),

and its multiplicative excess is

2^R/3^q = 2^(R-q alpha).

Thus the relevant Diophantine quantity is the **upper absolute error**

delta(q)=R-q alpha,

not merely the slope error R/q-alpha.

A useful transfer lemma avoids scanning every q.

> **Farey-neighbour transfer lemma.** Suppose R_u/q_u>alpha>R_l/q_l and
>
> R_u q_l - R_l q_u = 1.
>
> Then every rational strictly between R_l/q_l and R_u/q_u has denominator at least q_u+q_l. Consequently, if q_u<=q<q_u+q_l and R/q>alpha, then
>
> R-q alpha >= R_u-q_u alpha.
>
> Indeed, an upper rational with smaller absolute error would, because q>=q_u, also have slope strictly between alpha and R_u/q_u, contradicting the Farey denominator bound.

The power-side hypotheses are certified by exact integer comparisons 2^R versus 3^q. This is the local continued-fraction/Farey structure behind the survivor pattern; the use of such Diophantine approximation is classical Collatz methodology.

### First transferred block

The exact pair

301994/190537 > alpha > 16785921/10590737

has determinant 1. Their mediant is

17087915/10781274.

The already-certified upper approximation q=190537 has M_max=589,078,792, and exact symbolic coverage shows that no M in

5,000,001 <= M <= 589,078,792

sustains 29 consecutive exact-r=1 rises.

Therefore every q with

400,001 <= q <= 10,781,273

is excluded without enumerating the individual periods: any upper approximation in this block has product ratio at least that of q=190537, hence M<=589,078,792, while the required rise length is at least 166,015.

### Second transferred block

The mediant above is itself an exact upper approximation:

2^17087915 > 3^10781274.

It gives the theorem-derived finite range

M <= 3,112,972,388.

Exact decimal-sector / 2-adic symbolic coverage on the complete interval

5,000,001 <= M <= 3,112,972,388

becomes empty at rise depth 31.

The exact lower neighbour

85137581/53715833 < alpha

has determinant 1 with 17087915/10781274. Hence the same Farey transfer excludes every q with

10,781,274 <= q <= 64,497,106.

At the block start,

2q-R = 4,474,633,

so the required rise length is enormously larger than the 31-step symbolic extinction depth.

Combining the two transferred blocks with the previous q<=400,000 certificate gives

> **Finite structured-cycle corollary.** Any different positive one-rise/one-fall accelerated cycle consistent with the exhaustive 5,000,000-seed census must satisfy
>
> q >= 64,497,107.

A conservative exact rise consequence can also be obtained without evaluating 3^64497107. The mediant numerator at the first uncovered denominator is

17087915+85137581 = 102225496.

The two exact bit-length checks place the summed approximation within one integer of q alpha, so

ceil(q alpha) <= 102225497

at q=64,497,107. Since k(q)=2q-ceil(q alpha) is nondecreasing,

> every remaining structured cycle has at least 26,768,717 consecutive exact-r=1 rise steps.

### Why the new symbolic range dies

The new symbolic range does not die because long r=1 runs are globally impossible; arbitrarily long such runs still exist at sufficiently large seeds.

For M<=3,112,972,388, the exact symbolic cell count rises to 263 cells at depths 16 and 17, then contracts:

177, 132, 107, 72, 38, 26, 15, 11, 6, 3, 0

at depths 21 through 31.

At depth 30 only three residue-compatible representatives remain:

- 1,229,721,173;
- 1,380,119,257;
- 1,637,781,257.

Their 31st accelerated valuations are respectively 5, 3, and 2, so none extends the weak run. At this depth the residue modulus is already 2^31 and each surviving decimal-consistent cell is narrower than that modulus. The mechanism is therefore a finite-range **decimal-sector narrowing plus binary-lift squeeze**: digit consistency fragments the allowed M interval until each cell contains at most one admissible residue representative, and the next required lift misses the permitted cell/range.

This diagnosis is exact for the stated finite M range. It is not a uniform bound on weak-run length.

The machine-readable extension certificate is

data/structured_farey_extension.json,

generated by

scripts/structured_farey_extension.py.

## Iterated Farey record chain — ELEMENTARY FACTS + FINITE EXACT CERTIFICATE

The first denominator not covered by the previous transfer is not merely a boundary point. The exact mediant

102225496 / 64497107
=
(17087915+85137581)/(10781274+53715833)

lies above alpha=log_2(3), so

R(64,497,107)=102,225,496

and

2^102225496 > 3^64497107.

Thus q=64,497,107 is the next upper Farey/Stern-Brocot record generated from the previous neighbour pair.

Direct construction of 3^q is no longer a sensible certificate as the denominators grow. The script

scripts/structured_record_chain.py

instead uses the exact positive series

log x
=
2 sum_(k>=0) z^(2k+1)/(2k+1),
qquad
z=(x-1)/(x+1),

with the rigorous tail estimate

tail_N
<=
2 z^(2N+1) / ((2N+1)(1-z^2)).

All endpoints are represented by Python Fraction objects. Hence every sign test for

R log 2-q log 3

and every comparison with log B(M), where

B(M)=M(M-19)/(M^2-57M+361),

is an exact rational certificate with an explicit remainder bound, not a floating-point decision. As a regression, this method reproduces the previous exact M_max=3,112,972,388 at q=10,781,274.

Iterating the Farey-neighbour step gives the following seven further certified upper records. For each row, exact symbolic coverage of the complete interval 5,000,001<=M<=M_max becomes empty at the listed rise depth.

| q | R | M_max | required a>=2q-R | first impossible rise | peak cells | next upper q |
|---:|---:|---:|---:|---:|---:|---:|
| 64,497,107 | 102,225,496 | 4,350,616,725 | 26,768,718 | 31 | 276 | 118,212,940 |
| 118,212,940 | 187,363,077 | 7,221,856,344 | 49,062,803 | 31 | 301 | 171,928,773 |
| 171,928,773 | 272,500,658 | 21,238,350,355 | 71,356,888 | 35 | 350 | 397,573,379 |
| 397,573,379 | 630,138,897 | 359,020,668,782 | 165,007,861 | 38 | 485 | 6,586,818,670 |
| 6,586,818,670 | 10,439,860,591 | 3,753,781,445,604 | 2,733,776,749 | 41 | 603 | 72,057,431,991 |
| 72,057,431,991 | 114,208,327,604 | 6,895,437,822,163 | 29,906,536,378 | 41 | 636 | 137,528,045,312 |
| 137,528,045,312 | 217,976,794,617 | 42,285,421,502,900 | 57,079,296,007 | 49 | 727 | 890,638,885,193 |

The lower neighbour immediately before the next unprocessed upper record is

1193652440098 / 753110839881
<
alpha,

and its determinant with

1411629234715 / 890638885193
>
alpha

is exactly 1.

Therefore the seven record blocks exclude every structured period through

q=890,638,885,192.

The first period not covered by this finite certificate is

q=890,638,885,193,

where the exact upper record has R=1,411,629,234,715. Since k(q)=2q-ceil(q alpha) is nondecreasing, every remaining one-rise/one-fall cycle under the 5M minimum premise must satisfy

q>=890,638,885,193

and

a>=369,648,535,671.

This remains a bounded structured-class consequence. It says nothing stronger about arbitrary cycles, whose separate current lower bound remains q>=971.

## Product-window scale at Farey records — ELEMENTARY FACT

Write

t
=
log(2^R/3^q)
=
(R-q alpha) log 2
>
0.

For M>=5,000,001,

B(M)-1
=
(38M-361)/(M^2-57M+361)

satisfies the explicit elementary bounds

37/M
<
B(M)-1
<
39/M.

The left inequality is equivalent to

M^2+1748M-13357>0,

and the right inequality is equivalent to

M^2-1862M+14079>0,

so both hold throughout the range in use.

If the product window exp(t)<=B(M) holds, then exp(t)-1>=t gives

M<39/t.                                                     (13)

Conversely, for 0<t<1, exp(t)<=1/(1-t). Therefore every M satisfying

M<=37(1-t)/t

also satisfies the product window. Thus the product-derived minimum scale is quantitatively Theta(1/t), with explicit constants, for the record errors relevant here.

There is also an exact record-to-record relation. Suppose R/q is the current upper Farey neighbour and S/p the lower neighbour, and put

delta=R-q alpha>0,
epsilon=p alpha-S>0.

The determinant-one identity gives

p delta+q epsilon=1.                                      (14)

After updating lower mediants until the next mediant is upper, that next upper has denominator q_next=p+q and upperness means delta>epsilon. Hence

delta>1/q_next.

Combining this with (13) gives the explicit record-to-record estimate

M_max
<
39 q_next / log 2.                                       (15)

This is a genuine asymptotic framework for the product-window scale: M_max is controlled by Diophantine approximation error, and every certified record gives a bound in terms of the next upper denominator. It is not by itself a global cycle exclusion, because unrestricted continued-fraction partial quotients do not give the missing symbolic-residue conclusion.

The required rise length is independently linear in q. The exact inequality

alpha<8/5

follows from 3^5=243<256=2^8. Since R=ceil(q alpha),

2q-R
>
2q/5-1.                                                   (16)

Thus the structural rise requirement grows linearly in the period while the product window is governed by the reciprocal Diophantine error.

## Finite-range decimal boundary localization — ELEMENTARY FACT

The exact rise formula gives, for lambda_i=(3/2)^i,

lambda_i M + 3(lambda_i-1)
<=
x_i
<=
lambda_i M + 19(lambda_i-1).                              (17)

In particular x_i is always above the homogeneous point lambda_i M.

Suppose the actual decimal sector of x_i differs from the sector containing lambda_i M. Then some decimal-sector boundary B=d*10^k is crossed between them. By (17),

M
<
B/lambda_i
<=
M+19(1-1/lambda_i)
<
M+19.                                                      (18)

So, at each depth, disagreement with the homogeneous decimal itinerary is confined to integer starting values lying in a window of width less than 19 immediately below a scaled decimal boundary B/lambda_i.

This gives an explicit finite-range symbolic-complexity bound. For a fixed interval [L,U] and rise depth s, let J_s(L,U) be the total number, over i=0,...,s-1, of decimal boundaries B=d*10^k for which

B/lambda_i
lies in
[L,U+19].

The union of those J scaled boundary points partitions [L,U] into at most J+1 homogeneous decimal-sector words. Each exceptional boundary window in (18) contains at most 19 integer starts. Therefore the number of exact decimal-sector words realized by integer starts in [L,U] through s rises is at most

20 J_s(L,U)+1.                                            (19)

For fixed L,U, the number of relevant decimal boundaries at each depth is bounded independently of i because the multiplicative width of

[lambda_i L, lambda_i(U+19)]

is constant. Hence J_s(L,U)=O(s), and (19) gives a linear, rather than exponential, finite-range word-complexity bound.

For any one fixed decimal-sector word d_0,...,d_(s-1), let A_s be the rise-word additive term from (1). The s exact-r=1 parity conditions collapse to the single terminal congruence

3^s M + A_s
==
2^s
(mod 2^(s+1)).                                            (20)

Indeed, writing Y_i=3^i M+A_i, the recurrence gives

Y_(i+1)=3Y_i+(2d_i+1)2^i.

If Y_(i+1)==2^(i+1) (mod 2^(i+2)), then the oddness of 2d_i+1 forces Y_i==2^i (mod 2^(i+1)); backward induction recovers every earlier exact-r=1 condition. Conversely an exact rise word plainly gives (20). Since 3 is invertible modulo powers of two, the unique starting residue is explicitly

M
==
3^(-s)(2^s-A_s)
(mod 2^(s+1)).                                            (21)

Consequently the number of starts in [L,U] realizing s exact rises is bounded by

(20 J_s(L,U)+1)
(
floor((U-L)/2^(s+1))+1
).                                                         (22)

This is substantially stronger than treating all leading-digit words as independent branches.

It is still explicitly finite-range. It does not contradict the proved existence of arbitrarily long r=1 runs at sufficiently large seeds.

## Why the symbolic theorem does not yet close the class

Equation (20) isolates the remaining obstruction precisely. Once

2^(s+1)>U-L,

each fixed word contributes at most one residue representative, but the bound still permits one representative for each surviving word. Width and cell count alone cannot prove that those representatives miss their decimal cells.

The largest processed range makes this visible. For

5,000,001
<=
M
<=
42,285,421,502,900,

the cell count peaks at 727 at rise depth 19 and then collapses to one cell at depth 48 and zero cells at depth 49. At depth 48 the sole cell is

[26,465,544,205,035, 26,666,666,666,617],

with exact residue representative

M=26,501,219,601,103

and digit word

235812346112357112358112461123571123581124691235.

After 48 exact r=1 rises, its state is

7,510,109,955,360,948,316,615,

whose next accelerated valuation is 2. Hence the range becomes empty at rise 49.

For this same finite range and depth, the boundary count in (19) is J=2,997, giving the proved coarse word bound 59,941. The residue modulus already exceeds the full initial interval, so the residue capacity per fixed word is one. The actual checker has only one surviving word and representative, showing that the theorem explains low symbolic entropy but not the final miss.

The three terminal representatives from the previous PR #12 range also do not collapse to one common prefix obstruction. Their 30-digit words are

- 112469123471123581124691234611;
- 123461123571124691234611235711;
- 123581124691234711235811246912.

They diverge near the start, and their next valuations are 5, 3, and 2. Thus no reusable common-prefix terminal lemma has been identified from those three examples.

The missing global step is therefore sharper than “prove cells get narrow.” A global one-rise/one-fall exclusion would need control of the positions of the word-dependent 2-adic residue representatives relative to the narrow decimal cells, or another obstruction of comparable strength. The present Farey mechanism plus (13)–(20) is an asymptotic framework, but the repository still contains only finite record certificates, not an all-record theorem.

The machine-readable certificate for this increment is

data/structured_record_chain.json,

generated by

scripts/structured_record_chain.py.

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

The one-rise/one-fall class is **excluded through q=64,497,106 under the existing 5M minimum premise, but not globally excluded**.

The theorem-level ingredients are the period-independent product envelope (11), the fall-excess identity, and the Farey-neighbour transfer lemma for upper powers-of-two / powers-of-three approximations. The finite exact certificates combine those facts with exact power comparisons, theorem-derived M_max ranges, and exact symbolic decimal/2-adic rise coverage.

The current structured consequence is

q>=64,497,107

and, conservatively,

a>=26,768,717.

The first period not covered by the current Farey transfer is 64,497,107. The highest-value next target is to analyze that next approximation record and determine whether the same finite-range modulus squeeze can be made into a general record-to-record theorem, or where it first fails.
