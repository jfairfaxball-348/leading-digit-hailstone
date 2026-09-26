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
