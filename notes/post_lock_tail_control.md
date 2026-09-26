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

## 7. A normalized corridor of width less than 19

There is a useful exact coordinate once the lock state itself is taken as the
origin.  Let

`X_0=X`

be a concrete post-lock odd state, and suppose the next `t` accelerated steps
all have exact valuation one.  Write

`c_j=2L(X_j)+1`,

so `3 <= c_j <= 19`, and

`2 X_(j+1) = 3 X_j + c_j`.

Define

`Z_j = (2/3)^j X_j`.

Then direct substitution gives the exact recurrence

`Z_(j+1)-Z_j = (c_j/3)(2/3)^j`.

Hence

`Z_t-X = (1/3) sum_(j=0)^(t-1) c_j (2/3)^j`,

and therefore

`3(1-(2/3)^t) <= Z_t-X <= 19(1-(2/3)^t) < 19.`

Equivalently, every exact-r=1 post-lock state has the form

`X_t = (3/2)^t (X + delta_t)`

with

`3(1-(2/3)^t) <= delta_t < 19.`

This is an **elementary exact theorem**.  The striking point is that the
normalized uncertainty does not grow with the length of the tail: the whole
future exact-r=1 segment stays in one interval of width less than 19 above the
single locked state `X`.

In the original unscaled coordinate this gives

`3((3/2)^t-1) <= X_t-(3/2)^t X <= 19((3/2)^t-1)`.

The absolute error grows, but only because the common homogeneous scale grows.

## 8. Exact decimal-boundary corridor

Let

`Y_t=(3/2)^t X`

be the homogeneous state.  The preceding theorem gives `X_t>Y_t`.  If the
actual leading digit of `X_t` differs from the leading digit of `Y_t), then
some decimal leading-digit boundary

`C=d 10^k`

must lie strictly between them.  Scaling back by `(2/3)^t` gives

`X < C(2/3)^t < X+19`.

After clearing denominators this is the exact integer inequality

`X 3^t < C 2^t < (X+19)3^t.`

Thus:

> **Decimal-boundary corridor lemma.**  A post-lock leading-digit disagreement
> with the homogeneous `(3/2)^t X` itinerary is possible only if a scaled
> decimal boundary lies in the fixed length-19 interval `(X,X+19)`.

No logarithm or floating-point approximation is needed to certify the
condition for a concrete locked candidate.  Conversely, absence of such a
boundary hit forces the actual and homogeneous leading digits to agree at
that time.

This is useful phase control, but it is not a tail bound: valuation one also
requires the exact 2-adic parity condition, and that parity may continue even
when the digit itinerary is completely frozen.

## 9. Exact same-sector exit bounds

The local affine geometry is even more rigid than the boundary corridor first
suggests.

Suppose a valuation-one source lies in the decimal sector

`d 10^k <= x < (d+1)10^k`.

Because

`x'=(3x+2d+1)/2 > (3/2)x`,

the following hold.

- If `d>=2`, one valuation-one step already exits that sector upward.
- If `d=1`, at most two consecutive source states can remain in the
  digit-one sector.  Indeed two digit-one steps give
  `4x_2=9x_0+15>8*10^k`.
- Six consecutive valuation-one steps increase the state by more than
  `(3/2)^6=729/64>10`.  Therefore every six-step valuation-one segment
  crosses at least one power-of-ten boundary.

These are **elementary theorems**.  Their algebraic cores are formalized in
`LeadingDigitHailstone/Basic.lean`.

They do not supply a global post-lock bound: a long tail can keep traversing
new sectors and new decades.

## 10. Complete own-bit lock scan through 220 bits

The new exact diagnostic in

`scripts/post_lock_scale_geometry.py`

partitions starts by their own bit-length depth `B`:

`2^B < M < 2^(B+1)`.

For each complete interval it performs exact decimal/2-adic symbolic coverage
through depth `B`.  Since the depth-`B` residue modulus is `2^(B+1)`,
every surviving cell contains at most one concrete start, equal to its
canonical residue.  The script then follows that concrete orbit directly.

The machine-readable certificate is

`data/post_lock_scale_geometry.json`.

For every `1 <= B <= 220`, equivalently for every start in the complete
own-bit bins below `2^221` that survives to its own lock depth, the exact
scan finds:

- 96 locked candidates in total;
- 41 with a positive post-lock valuation-one tail;
- tail histogram
  `{0:55, 1:16, 2:13, 3:7, 4:1, 5:3, 6:1}`;
- maximum observed post-lock tail 6.

The successive positive records are

- `B=33`, `M=16,670,166,793`, tail 1;
- `B=44`, `M=26,501,219,601,103`, tail 4;
- `B=65`, `M=43,574,304,770,317,398,119`, tail 6.

There are three further tail-5 starts through the scan, at bit depths 65,
103, and 216.

This is **finite exact symbolic/direct computation**, not a theorem that the
tail is universally at most 6.

A more informative negative diagnostic is that all 41 positive-tail
candidates have:

- zero scaled decimal-boundary corridor hits during their post-lock tail; and
- zero disagreement between the actual leading digits and the exact
  homogeneous `(3/2)^t X` leading digits.

Thus the observed post-lock tails do not require repeated decimal-boundary
near-hits.  In this complete finite scan, their decimal itinerary is already
phase-frozen.

## 11. Sharpened obstruction and next target

The width-19 corridor makes the decimal geometry much cleaner, but the exact
scan shows why decimal separation alone is insufficient.  Once the
homogeneous itinerary is safely away from every boundary, the remaining
condition is the post-lock parity rule

`(X_t-1)/2 + L(X_t) == 1 (mod 2)`

at every step.

Accordingly, the highest-value next theorem is now a **scale-aware
parity/congruence obstruction along a phase-frozen homogeneous digit
itinerary**.  Useful forms would combine the exact `(3/2)^t` digit word with
the carry parity, mixed `2^m5^n` congruences, or another monotone scale
coordinate.

A separate high-value falsification route is to extend the exact own-bit scan
and deliberately search for a tail longer than 6 or for a recursively
extendable family.  Until such a theorem or family is established, no
universal `F(B)` or `F(M)` bound is claimed.

The structured one-rise/one-fall frontier remains
`q>=1,643,749,725,074` with
`a>=682,217,775,335` under the existing 5M premise.  The arbitrary-cycle
bound remains separately `q>=971`.

