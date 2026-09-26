# Accelerated Cycle Constraints

This note records elementary constraints for Task 4. They do **not** exclude all nontrivial cycles.

For an odd state `x_i`, define `c_i=2L(x_i)+1 ∈ {3,5,7,9,11,13,15,17,19}` and `r_i=v2(3x_i+c_i)≥1`. The accelerated recurrence is

`x_(i+1)=(3x_i+c_i)/2^(r_i)`.

Suppose `x_0,…,x_(q-1)` form a cycle of odd states, with `x_q=x_0`. Put `R=r_0+...+r_(q-1)` and `R_j=r_0+...+r_(j-1)` for `j≥1`, with `R_0=0`. Iterating gives the exact cycle equation

`(2^R-3^q)x_0 = Σ_(j=0)^(q-1) 3^(q-1-j) c_j 2^(R_j)`.

The right-hand side is positive. Therefore every positive accelerated cycle must satisfy

`2^R > 3^q`,

equivalently `R/q > log_2(3)`.

This is only a necessary condition. The correction word is state-dependent: each `c_j` must equal `2L(x_j)+1`, and each `r_j` must be the exact 2-adic valuation at that state.

## Bounded-search consequence

A rigorous bounded cycle search should enforce:

1. `2^R>3^q`;
2. integrality and positivity from the cycle equation;
3. exact valuation at every state;
4. leading-digit consistency at every state;
5. canonical rotation to avoid duplicate cycle words.

Any exclusion must state its bounds on `q`, `R`, and/or state size. It is not a global proof unless those bounds are separately proved universal.

## Finite cycle exclusion from the 5M census

The exact exhaustive census in `data/task2_census_5m.json` followed every positive starting value `1 <= n <= 5,000,000` into the distinguished cycle and observed no other cycle.

Therefore, as a **FINITE COMPUTATION** consequence, any different positive cycle (if one exists) must have minimum element strictly greater than `5,000,000`. This is a bounded exclusion only.
