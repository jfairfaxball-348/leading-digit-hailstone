# Accelerated Cycle Constraints

This note records rigorous constraints for positive accelerated cycles. They do **not** exclude all nontrivial cycles.

For an odd state x_i, define

c_i = 2L(x_i)+1 in {3,5,7,9,11,13,15,17,19}

and

r_i = v2(3x_i+c_i) >= 1.

The accelerated recurrence is

x_(i+1) = (3x_i+c_i)/2^(r_i).

Suppose x_0,...,x_(q-1) form a cycle of odd states, with x_q=x_0. Put

R = r_0+...+r_(q-1)

and

R_j = r_0+...+r_(j-1)

for j>=1, with R_0=0.

## Additive cycle equation — ELEMENTARY FACT

Iterating the affine recurrence gives

(2^R-3^q)x_0 = sum_(j=0)^(q-1) 3^(q-1-j)c_j 2^(R_j).

The right-hand side is positive. Therefore every positive accelerated cycle satisfies

2^R > 3^q,

equivalently

R/q > log_2(3).

This is necessary only. Every c_j must be the correction selected by the actual leading digit of x_j, and every r_j must be the exact 2-adic valuation at x_j.

## Multiplicative cycle identity — ELEMENTARY FACT

Rewrite each accelerated step as

2^(r_i) x_(i+1) / (3x_i) = 1 + c_i/(3x_i).

Multiplying over i=0,...,q-1 makes the state factors telescope around the cycle:

product_i x_(i+1)/x_i = 1.

Hence

2^R / 3^q = product_(i=0)^(q-1) (1 + c_i/(3x_i)).

This identity is exact.

If

M = min_i x_i,

then x_i>=M and 3<=c_i<=19, so

1 < 2^R/3^q <= (1 + 19/(3M))^q.                 (1)

Thus a cycle with large minimum forces 2^R/3^q to lie in a very narrow interval immediately above 1. Equivalently,

0 < R log 2 - q log 3 <= q log(1 + 19/(3M)),

but the rational inequality (1) is preferable for exact finite certificates because it can be checked using integer arithmetic only.

## Local direction is determined by the valuation above 19 — ELEMENTARY FACT

Let x>19 be odd and let

x'=(3x+c)/2^r,

where c=2L(x)+1<=19.

If r=1, then

x'=(3x+c)/2 > x

because x+c>0.

If r>=2, then

x' <= (3x+19)/4 < x

because x>19.

Therefore for every odd x>19:

- r=1 implies a strict accelerated increase;
- r>=2 implies a strict accelerated decrease.

This does **not** give a global descent theorem, because arbitrarily long consecutive r=1 runs exist.

## Minimum anchor for a large cycle — ELEMENTARY FACT

Consider a positive accelerated cycle all of whose odd states exceed 19, and let x_i=M be a minimum state.

Its successor cannot be smaller than M. By the previous lemma, the outgoing valuation at the minimum must therefore satisfy

r_i=1.

Likewise the state immediately preceding M cannot enter M by an r=1 step, because every r=1 step above 19 strictly increases. Hence the incoming valuation satisfies

r_(i-1)>=2.

So every large cycle has, after rotation to a minimum state, the anchored valuation pattern

..., r_(q-1)>=2, r_0=1, ...

This is a local necessary condition, not a sufficient word description.

## Exact 5M consequence: at least 971 odd states — FINITE EXACT ARITHMETIC CONSEQUENCE

The exhaustive census through 5,000,000 proves only the bounded statement that any different positive cycle, if one exists, has minimum element >5,000,000. In particular its minimum odd state satisfies

M>=5,000,001.

Combine this with (1). For a fixed q, let R_min(q) be the least integer R with

2^R>3^q.

If even R_min(q) violates the upper bound in (1), then every larger R violates it as well. The necessary condition is therefore

2^(R_min(q)) / 3^q <= ((3M+19)/(3M))^q.

For M=5,000,001 this can be checked without floating point by cross-multiplying:

2^(R_min(q)) (3M)^q <= 3^q (3M+19)^q.          (2)

The exact-integer certificate in

scripts/cycle_minimum_length_bound.py

checks (2) for consecutive q and records its result in

data/cycle_minimum_length_bound.json.

It verifies:

- every q=1,...,970 is excluded by this necessary inequality;
- q=971 is the first value not excluded by this coarse product window;
- R_min(971)=1539.

Therefore:

> **Bounded corollary.** Any different positive accelerated cycle consistent with the exhaustive 5,000,000-seed census must contain at least 971 odd states.

This is stronger than the minimum-element exclusion alone, but it is still not a global no-cycle theorem. In particular q=971 is **not** claimed to be realizable.

## Structured one-rise/one-fall cycles — ELEMENTARY FACTS + FINITE EXACT SYMBOLIC EXCLUSION

Issue #10 studies the narrower class whose valuation word, after rotation to the minimum, has one nonempty block of r=1 steps followed by one nonempty block of r>=2 steps. Above 19 this is equivalent to exactly one strict local minimum and one strict local maximum, not merely a unique global minimum.

The block geometry yields the period-independent product estimate

1 < 2^R/3^q <= M(M-19)/(M^2-57M+361).             (3)

Under M>=5,000,001 the right side is less than 2, so the only possible total valuation at fixed q is R=ceil(q log_2 3). Farey-neighbour control transfers the product-ratio lower bound across complete denominator blocks.

The first certificate scanned q<=400,000 exactly and eliminated its six product-window survivors. PR #12 then transferred two Farey blocks through q=64,497,106. The current record-chain certificate iterates the same exact mechanism through seven further upper records, using rigorous rational logarithm bounds with explicit remainder estimates for the power-side and M_max decisions, together with complete decimal-sector / 2-adic symbolic rise coverage.

Therefore:

> **Bounded structured corollary.** Any different positive one-rise/one-fall accelerated cycle consistent with the exhaustive 5,000,000-seed census must have q>=890,638,885,193 and at least 369,648,535,671 consecutive exact-r=1 rise steps.

The largest processed M range is 5,000,001<=M<=42,285,421,502,900 and becomes symbolically empty at rise 49. The next unprocessed upper record is (q,R)=(890,638,885,193,1,411,629,234,715).

A new finite-range boundary-localization lemma bounds the number of possible decimal-sector words through s rises by 20J_s(L,U)+1, where J_s counts relevant scaled decimal boundaries. For fixed [L,U], J_s=O(s). This proves low symbolic complexity but not eventual extinction: after the residue modulus exceeds the interval width, each word can still carry one residue representative. Controlling those representative positions is the remaining structured-class obstruction.

See notes/one_minimum_cycles.md, scripts/structured_record_chain.py, and data/structured_record_chain.json. This does **not** change the arbitrary-cycle bound q>=971.

## Why this matters for the next cycle search

A rigorous bounded cycle search should now enforce at least:

1. 2^R>3^q;
2. the product window (1);
3. the additive cycle equation;
4. the minimum anchor r_out=1 and r_in>=2 when M>19;
5. exact valuation at every state;
6. leading-digit consistency at every state;
7. canonical rotation to the minimum state to avoid duplicate cycle words.

The product window is useful because it restricts (q,R) before digit-word enumeration. The next goal is to add enough valuation-word and decimal-sector consistency to turn the coarse q>=971 consequence into much stronger bounded exclusions.

## Status discipline

- The additive and multiplicative identities are **ELEMENTARY FACTS**.
- The direction lemma and minimum anchor are **ELEMENTARY FACTS**.
- The 971 statement depends on the 5M census plus a finite exact arithmetic certificate.
- No statement here excludes all competing positive cycles.
