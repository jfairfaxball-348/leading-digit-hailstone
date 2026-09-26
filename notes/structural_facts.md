# Elementary Structural Facts

All items in the first section are **ELEMENTARY FACTS** for the frozen map.

## Proved directly

1. **Odd steps are even.** If `n` is odd, then `3n` is odd, `2L(n)` is even, and therefore `3n+2L(n)+1` is even. Hence the accelerated odd-to-odd map is always defined after removing at least one factor of two.

2. **2-adic congruence for fixed leading digit.** Fix `d ∈ {1,…,9}` and restrict to odd `n` with `L(n)=d`. For every `r ≥ 1`,

   `v2(3n+2d+1) ≥ r`

   iff

   `3n ≡ -(2d+1) (mod 2^r)`.

   Since `3` is invertible modulo `2^r`, this selects exactly one residue class modulo `2^r`, and that class is odd because the right-hand side is odd.

3. **Exact valuation classes.** For fixed `d`, the condition `v2(3n+2d+1)=r` is the unique class satisfying the congruence modulo `2^r` but not its unique lift satisfying the congruence modulo `2^(r+1)`.

4. **Piecewise affine form.** On every decimal leading-digit interval `[d·10^k,(d+1)·10^k)` (with the usual interpretation for `d=9`), the odd branch is the affine rule `3n+(2d+1)`.

5. **One-step inverse images.** Every positive target `m` has the even predecessor `2m`. An odd predecessor must have some leading digit `d` and satisfy `n=(m-2d-1)/3`; it is valid exactly when this value is a positive odd integer with leading digit `d`. Thus there are at most nine odd-predecessor candidates to test.

## Heuristic direction, not theorem

If odd residues were sampled uniformly modulo powers of two inside a fixed-leading-digit region, the valuation classes above would give the same geometric 2-adic pattern familiar from accelerated Collatz-type maps. Whether decimal-leading-digit correlations materially disturb that heuristic along actual trajectories is an experimental question, not an established fact.
