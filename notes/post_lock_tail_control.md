# Post-Lock Deterministic Tail Reduction

**Issue:** #10 — one-rise/one-fall structured accelerated cycles  
**Claim discipline:** theorem-level statements are separated from finite exact symbolic/direct certificates. No novelty claim is made.

## 1. Exact elimination of the residue variable

For a prescribed exact-r=1 rise word, retain the established identities

`2^s x_s = 3^s M + A_s`

and

`H_s = (3^s rho_s + A_s - 2^s) / 2^(s+1)`.

After bounded-range locking, `rho_s = M`. Therefore

`3^s M + A_s = 2^s + H_s 2^(s+1)`.

Comparing the two identities and dividing by `2^s` gives

`x_s = 1 + 2 H_s`.

Thus after locking the carry is not an independent symbolic coordinate:

`H_s = (x_s - 1) / 2`.

This is the simplest post-lock coordinate.

## 2. Zero lift is exactly one deterministic r=1 step

Write `d_s = L(x_s)`. The established lift rule is

`b_s = 1 + H_s + d_s (mod 2)`.

Hence `b_s = 0` exactly when `H_s + d_s` is odd.

Using `x_s = 1 + 2 H_s`,

`3 x_s + (2 d_s + 1) = 2(3 H_s + d_s + 2)`.

Therefore

`v2(3 x_s + 2 d_s + 1) = 1`

exactly when `3 H_s + d_s + 2` is odd, equivalently when `H_s + d_s` is odd. Consequently

`b_s = 0  iff  v2(3 x_s + 2 L(x_s) + 1) = 1`.

When this holds,

`x_(s+1) = 3 H_s + d_s + 2`

and

`H_(s+1) = (1 + 3 H_s + d_s)/2 = (x_(s+1)-1)/2`.

So the carry recurrence and the actual accelerated orbit recurrence are the same dynamics in two coordinates.

## 3. Deterministic-tail theorem

Let `1 <= M <= U` and `B = floor(log_2 U)`. Suppose `M` survives `B` exact-r=1 rises.

The established bit-length locking theorem gives `M = rho_B`, and every compatible later lift bit is zero. By the equivalence above, each later zero lift is exactly one valuation-1 accelerated step of the concrete state reached by the fixed integer `M`.

> **Post-lock deterministic-tail theorem.** Once a bounded start reaches lock depth, there is no remaining symbolic lift or decimal-sector choice. Its entire compatible zero-lift tail is exactly its deterministic accelerated orbit until the first valuation different from 1.

For a finite interval `[L,U]`, exact symbolic coverage is therefore required only through `B`. If `C_B(L,U)` is the finite set of starts surviving to lock and `ell(M)` denotes the total initial exact-r=1 rise length of `M`, then, whenever `C_B` is nonempty,

`first impossible rise length = 1 + max { ell(M) : M in C_B(L,U) }`.

This is an exact finite-range reduction. It is not a general bound on the maximum tail length.

## 4. A false route: no universal tail bound <= 5

A deliberate exact search for long locked tails finds

`M = 43,574,304,770,317,398,119`.

Its own bit-length lock depth is

`B = floor(log_2 M) = 65`.

Direct exact accelerated iteration gives 71 consecutive initial valuation-1 rises, followed by valuation 7. Hence its post-lock zero-lift tail is

`71 - 65 = 6`.

This is a **finite exact computation**. It rigorously falsifies every proposed universal constant bound of the form

`post-lock tail <= 5`.

It does **not** show that post-lock tails are unbounded, and it does not rule out a quantitative `F(B)` or `F(M)` theorem.

## 5. Lock-and-follow certificate for the next Farey record

The first upper record beyond the PR #15 frontier is

`(q,R) = (890,638,885,193, 1,411,629,234,715)`.

Its determinant-one lower neighbour remains

`(753,110,839,881, 1,193,652,440,098)`.

Exact rational-log product-window certification gives

`M <= 48,737,068,628,469`.

The lock depth remains `B = 45`. Exact symbolic coverage through depth 45 leaves exactly the same two locked starts already seen in the preceding range:

- `26,501,219,601,103`;
- `39,751,829,401,657`.

Direct deterministic continuation gives total exact-r=1 rise lengths 48 and 47, respectively, and both then have valuation 2. Hence no start in the complete product-window range can realize 49 rises.

The record itself requires

`a >= 2q - R = 369,648,535,671`,

so it is excluded.

The following upper record is

`(q',R') = (1,643,749,725,074, 2,605,281,674,813)`,

with no intervening lower-neighbour update. The established Farey-neighbour transfer therefore excludes the one-rise/one-fall structured class through

`q <= 1,643,749,725,073`

under the existing `M > 5,000,000` premise.

Thus any remaining one-rise/one-fall cycle must satisfy

`q >= 1,643,749,725,074`

and, by monotonicity of `2q - ceil(q log_2 3)`,

`a >= 682,217,775,335`.

This is a structured-class theorem plus finite exact rational/symbolic/direct certificate. The arbitrary-cycle bound remains separately `q >= 971`.

## 6. What this does and does not solve

The important gain is conceptual and algorithmic: **branching stops at lock depth**. The difficult tail question is now a question about ordinary deterministic orbit segments of a small exact candidate set, not about continued symbolic lift choices.

What is still missing is a theorem bounding those deterministic tails as a function of scale. The explicit tail-6 example shows that very small universal constants are already false. A viable next attack should therefore seek a scale-aware quantity, for example:

- a bound in terms of bit length or decimal scale;
- Diophantine control of the post-lock decimal itinerary;
- a discrepancy coordinate comparing the fixed locked start with scaled decimal boundaries;
- a congruence/scale state whose nonrecurrence is provable.

No universal-convergence claim follows from this increment.


## 7. Terminally anchored homogeneous guide — theorem-level

The fixed lock-depth comparison

`x_s=(3/2)^s(M+D_s)`

is useful for relative error, but its absolute discrepancy from the fixed
`D_B` guide grows like `(3/2)^(s-B)`.  For a **finite** exact-r=1 run
there is a sharper coordinate.

Let

`x_0,x_1,...,x_N`

be any finite run with exact valuation one at sources `x_0,...,x_(N-1)`.
Write

`c_j=2L(x_j)+1`.

Define the terminally anchored homogeneous guide

`g_s = x_N (2/3)^(N-s)`, for `0<=s<=N`.

Because exact valuation one gives

`x_(j+1)=(3x_j+c_j)/2`,

one backward step gives

`(2/3)x_(j+1)=x_j+c_j/3`.

Iterating from `N` down to `s` yields the exact identity

`g_s-x_s = sum_(j=s)^(N-1) (c_j/3)(2/3)^(j-s)`.

Since `3<=c_j<=19`,

`0 <= g_s-x_s < (19/3) sum_(m>=0) (2/3)^m = 19`.

Therefore:

> **Finite-horizon homogeneous-guide theorem.** Every state in any finite exact-r=1 run lies less than 19 below one terminally anchored homogeneous `(3/2))-orbit.  The bound is uniform in the run length and in the scale of the starting value.

This is stronger in absolute error than using a fixed `D_B` guide over a long
post-lock tail.  It is finite-horizon: the guide depends on the terminal state
`x_N`, so it does not presuppose or construct an infinite valuation-one orbit.

### Decimal-boundary consequence

If `x_s` and `g_s` lie in different leading-digit sectors, monotonicity and
`0<=g_s-x_s<19` imply that some decimal boundary

`C=d 10^k`

lies in `(x_s,g_s]`.  Hence necessarily

`0 <= g_s-C < 19`.

Thus every disagreement between the true digit itinerary and the terminally
anchored homogeneous itinerary is localized to an absolute window of width 19
immediately above a decimal boundary.

This is an exact boundary-separation lemma.  It is not yet a bound on the number
of such near-boundary events.

## 8. Same-sector valuation-one runs are uniformly short — theorem-level

Let `S=10^k` and suppose the current leading digit is `d`.

For `d>=2`, if `x>=dS`, then one valuation-one affine step satisfies

`x'=(3x+2d+1)/2 >= (d+1)S`.

Indeed,

`3dS+2d+1 - 2(d+1)S = (d-2)S+2d+1 > 0`.

So every sector with leading digit `2,...,9` is exited after one exact-r=1
step.

For `d=1`, two repeated digit-1 affine halvings give

`x_2=(9x_0+15)/4 > 2S`

whenever `x_0>=S`.  Thus digit 1 can occur as the source digit of at most two
consecutive valuation-one steps within one decimal decade.

Therefore:

> **Same-sector run theorem.** Along an exact-r=1 run, a fixed leading-digit
> sector contributes at most one rise source for digits 2 through 9, and at
> most two consecutive rise sources for digit 1.

The long-tail obstruction is consequently not persistence inside one decimal
sector.  It is the compatibility of parity with the sequence of sector crossings.

These inequalities are formalized in Lean in
`LeadingDigitHailstone/Basic.lean`.

## 9. Exact bit-length diagnostic through B = 100 — finite exact computation

The script

`scripts/post_lock_geometry.py`

exhausts every bit-length interval

`2^B < M < 2^(B+1)`

for `1<=B<=100` through its exact lock depth `B`, using the existing
complete symbolic decimal/2-adic coverage to lock and then direct deterministic
following.

The finite exact scan has 33 bit lengths with at least one lock-depth survivor.
Its record post-lock tails occur at

- `B=2`: tail 0;
- `B=33`: tail 1;
- `B=44`: tail 4;
- `B=65`: tail 6.

No `B<=100` candidate has post-lock tail greater than 6.  The record remains

`M=43,574,304,770,317,398,119`,

with total exact-r=1 run length 71 and next valuation 7.

For that same 71-step run, the terminally anchored guide has maximum exact
discrepancy

`27745896526529968578632101723473977 / 2503155504993241601315571986085849`

which is approximately 11.084 and is rigorously below 19.  In this particular
finite run there are no leading-digit mismatches between the true states and
the terminally anchored guide.

All of this subsection is **FINITE EXACT SYMBOLIC/DIRECT COMPUTATION**, not a
uniform theorem in `B`.

The machine-readable certificate is

`data/post_lock_geometry.json`.

## 10. What the phase route now reduces to

The guide theorem makes the real-variable target precise.  For a hypothesized
long finite tail, almost every digit is determined by a single geometric
progression unless that progression falls inside a width-19 window above a
decimal boundary.  A successful phase proof therefore needs one of two things:

1. a quantitative bound on how often
   `alpha (3/2)^s` can enter those shrinking relative boundary windows; or
2. a proof that, away from those windows, the forced homogeneous digit word is
   incompatible with the exact 2-adic parity conditions for long enough.

Irrationality of `log_10(3/2)` by itself is not such a theorem.  Problems about
the fractional parts of powers of `3/2` are classically delicate: Mahler's
1968 Z-number problem asks whether a positive real number can keep all
fractional parts of `alpha(3/2)^n` below `1/2`, and remains a standard
reference point for this difficulty.  Flatto, Lagarias and Pollington later
proved quantitative range results for fractional parts of `xi(p/q)^n`.
This project does **not** identify the post-lock problem with the Z-number
problem; the connection is methodological only, and no novelty claim is made.

The present obstruction is more specific: the finite-horizon guide parameter
depends on the terminal state, while the parity constraints are 2-adic and the
decimal coding is archimedean.  A useful next theorem must couple those two
coordinates rather than appeal to heuristic equidistribution.

## 11. Current status after this increment

No explicit general `F(B)` or `F(M)` bound has been proved.

What is now proved is:

1. a uniform absolute finite-horizon discrepancy bound `<19`;
2. exact localization of digit-itinerary disagreements to width-19 decimal
   boundary windows;
3. a scale-independent bound on same-sector valuation-one persistence.

What remains finite computation is the exhaustive bit-length scan through
`B=100`, including the record tail 6.

The structured one-rise/one-fall frontier remains

`q >= 1,643,749,725,074`

with

`a >= 682,217,775,335`

under the existing 5,000,000-seed minimum premise.

The arbitrary-cycle consequence remains separately `q>=971`.
