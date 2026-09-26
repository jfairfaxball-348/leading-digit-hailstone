# Post-Lock Scaled Tube and Phase/Residue Separation

**Issue:** #10 — one-rise/one-fall structured accelerated cycles  
**Claim discipline:** theorem-level statements are separated from finite exact certificates. No novelty claim is made.

This note continues `notes/post_lock_tail_control.md`. The post-lock tail is already known to be deterministic. The new point is that its decimal geometry has a fixed-width normalized coordinate.

## 1. Exact scaled-tube coordinate

Let `X=x_B` be the odd accelerated state at lock depth, and suppose the next `t` accelerated steps all have exact valuation one. Write

`d_j=L(x_j)`, `c_j=2d_j+1`, so `3 <= c_j <= 19`, and

`x_(j+1)=(3x_j+c_j)/2`.

Define the normalized state

`Y_t=(2/3)^t x_t`.

Then

`Y_(t+1)=Y_t+(c_t/3)(2/3)^t`.

Therefore `Y_t` is strictly increasing, and

`X <= Y_t < X+19`.

More sharply,

`X+3(1-(2/3)^t) <= Y_t <= X+19(1-(2/3)^t)`.

Equivalently,

`(3/2)^t X <= x_t < (3/2)^t (X+19)`.

Thus the whole compatible post-lock valuation-one tail is trapped in the multiplicative image of one fixed interval of absolute width 19. The width does **not** grow with `t` in normalized coordinates.

A convenient one-step form is

`3(x+3) <= 2(y+3)`

and

`2(y+19) <= 3(x+19)`

whenever `2y=3x+c` and `3<=c<=19`. These inequalities iterate immediately.

## 2. Exact local decimal-sector escape

Suppose `x` lies in the decimal sector

`d 10^k <= x < (d+1)10^k`

and one exact valuation-one step is taken.

If `d>=2`, then

`x_(next) >= (d+1)10^k`.

So a valuation-one trajectory cannot remain for two source states in the same sector with leading digit `d>=2`.

For digit `1`, two consecutive valuation-one steps with correction 3 give

`4x_2 = 9x_0+15`,

hence `x_2>2*10^k` whenever `x_0>=10^k`. Thus digit 1 can persist for at most two source states in one sector.

Independently of the digit, each exact valuation-one step satisfies

`3x_j < 2x_(j+1)`.

After six such steps,

`x_6 > (3/2)^6 x_0 = (729/64)x_0 > 10x_0`.

Hence one decimal decade can contain at most six source states from a consecutive valuation-one run.

These are local theorems. They do not by themselves bound the number of decades crossed.

## 3. Boundary localization after lock

A decimal leading-digit boundary has the form

`C=d 10^k`, with `d in {1,...,9}`.

At post-lock time `t`, the conservative tube is

`[(3/2)^t X, (3/2)^t(X+19))`.

If this tube contains no decimal boundary, then the leading digit of the true state `x_t` is forced by the homogeneous phase `(3/2)^t X`.

A possible ambiguity therefore requires

`X <= C(2/3)^t < X+19`.

The post-lock decimal problem has become a near-hit problem for scaled decimal boundaries against one fixed width-19 interval.

## 4. Exact separation theorem for boundary hits

Assume `X>38`. Suppose scaled boundaries

`z_s=C_s(2/3)^s`

and

`z_t=C_t(2/3)^t`

both lie in `[X,X+19]`, with `s<t`, and put `n=t-s`.

Because

`z_t/z_s >= X/(X+19) > 2/3`,

we have

`C_t/C_s = (z_t/z_s)(3/2)^n > 1`.

So the later decimal boundary is larger and its decimal exponent does not decrease. Write

`C_s=d 10^k`, `C_t=e 10^(k+m)`, with `m>=0`.

Then

`z_t/z_s = e 10^m 2^n / (d 3^n)`.

If `z_t != z_s`, the numerator and denominator on the right are distinct positive integers. Therefore

`|z_t/z_s - 1| >= 1/(d3^n) >= 1/(9*3^n)`.

But both scaled boundaries lie in an interval of width 19, so

`|z_t/z_s - 1| <= 19/X`.

Hence

`X <= 171*3^n`.

> **Scaled-boundary separation theorem.** Two distinct scaled decimal-boundary hits `n` post-lock steps apart force `X<=171*3^n`.

This is an exact rational inequality; no equidistribution heuristic is used.

### Exact coincident hits

The only way the separation lower bound can fail is `z_t=z_s`, equivalently

`e 2^n 10^m = d 3^n`.

The complete positive solutions with decimal digits `d,e in {1,...,9}`, `n>=1`, `m>=0` are

- `n=1,m=0: 2 -> 3`;
- `n=1,m=0: 4 -> 6`;
- `n=1,m=0: 6 -> 9`;
- `n=2,m=0: 4 -> 9`.

For `n>=3`, divisibility by `2^n` forces `d=8` already at `n=3), and then the remaining equality would require a decimal digit outside `1,...,9`; larger `n` are still more impossible. The `n=1,2` cases reduce immediately to the list above.

Thus exact coincident ambiguities form only the short chains `2->3` and `4->6->9`.

Define `g(X)` as the least positive integer `n` with

`X <= 171*3^n`.

Distinct ambiguity hits are separated by at least `g(X)`; only the short exact-coincidence clusters above can occur at smaller gaps. This is the first explicit scale-aware sparsity result for the post-lock decimal phase.

## 5. Phase/residue termination certificate

Suppose the width-19 tube is boundary-free for times `0,...,h-1`. Then the entire candidate digit word

`d_0,...,d_(h-1)`

is forced by the homogeneous phase.

For that fixed word, the already proved terminal congruence says that all `h` exact valuation-one conditions are equivalent to one residue condition modulo `2^(h+1)`.

Therefore a candidate can be terminated without following its true post-lock orbit:

1. certify the width-19 phase tube is boundary-free;
2. read the forced homogeneous digit word;
3. compute its exact required start residue;
4. compare that residue with `X mod 2^(h+1)`.

The first prefix mismatch proves that the exact-r=1 tail ends before that prefix.

This is a candidate-specific exact certificate, not a uniform tail bound.

## 6. Finite exact certificates for current lock states

The reproducible script `scripts/post_lock_phase.py` records three checks in `data/post_lock_phase.json`.

For the two locked states used in the current Farey certificate:

- `X=2,225,217,764,551,392,093,807`: forced word `2357`; the first three prefixes match and the fourth residue fails, certifying post-lock tail 3. Its distinct-boundary gap threshold is 41.
- `X=3,337,826,646,827,088,140,713`: forced word `357`; the first two prefixes match and the third fails, certifying post-lock tail 2. Its threshold is also 41.

For the tail-6 counterexample lock state

`X=12,166,406,006,866,046,930,622,304,922,581`,

the tube forces the word `1124691`. The first six residue prefixes match, while the seventh requires residue 85 modulo 256 but the lock state is 213 modulo 256. This certifies post-lock tail 6. The noncoincident boundary-gap threshold is 61.

Direct deterministic iteration is retained only as an independent finite cross-check; the phase/residue certificate itself does not use post-lock orbit following.

## 7. What this changes, and what remains open

The post-lock problem now has two complementary exact reductions:

- **state/carry reduction:** zero lift is exactly deterministic valuation-one continuation;
- **scaled-phase reduction:** normalized states remain in one fixed width-19 interval, so decimal ambiguity is sparse at a scale controlled by the lock state.

The new separation theorem is genuinely scale-aware, but it is **not** an `F(B)` or `F(M)` bound on total tail length. Between sparse ambiguity clusters there may be long intervals whose digit word is completely forced by the homogeneous phase, and the current mathematics does not yet prove that the associated 2-adic residue conditions must fail within a uniform number of such forced steps.

The next target is therefore sharper:

> bound the length of a boundary-free forced homogeneous digit block that can continue satisfying the exact terminal 2-adic residue conditions.

A proof of that statement with polynomial or otherwise useful dependence on lock scale would combine directly with the present ambiguity sparsity theorem.

The structured one-rise/one-fall frontier remains

`q >= 1,643,749,725,074`

and

`a >= 682,217,775,335`

under the existing 5,000,000 minimum premise. The arbitrary-cycle bound remains separately `q>=971`.
