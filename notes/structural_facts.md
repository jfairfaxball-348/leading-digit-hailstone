# Elementary Structural Facts

Unless explicitly labelled otherwise, statements in the proved sections are **ELEMENTARY FACTS** for the frozen map

`T(n)=n/2` for even `n`, and `T(n)=3n+2L(n)+1` for odd `n`, where `L(n)` is the leading decimal digit.

## Parity and accelerated dynamics

1. **Odd steps are even.** If `n` is odd, then `3n` is odd, `2L(n)` is even, and therefore `3n+2L(n)+1` is even. Hence the accelerated odd-to-odd map is always defined after removing at least one factor of two.

2. **Fixed-leading-digit 2-adic congruence.** Fix `d ∈ {1,…,9}` and restrict to odd `n` with `L(n)=d`. For every `r ≥ 1`,

   `v2(3n+2d+1) ≥ r`

   iff

   `3n ≡ -(2d+1) (mod 2^r)`.

   Since `3` is invertible modulo `2^r`, this selects exactly one residue class modulo `2^r`, and it is an odd class.

3. **Exact valuation classes.** For fixed `d`, the condition `v2(3n+2d+1)=r` is exactly one residue class modulo `2^(r+1)`: of the two lifts of the class from modulus `2^r`, one has valuation at least `r+1` and the other has valuation exactly `r`.

4. **Every finite valuation occurs infinitely often in every leading-digit sector.** The interval `[d·10^k,(d+1)·10^k)` has length `10^k`. For fixed `r`, sufficiently large `k` makes it longer than `2^(r+1)`, so it contains a representative of the exact-valuation residue class.

5. **Interval density.** For fixed `d` and `r`, among odd integers in increasingly long leading-digit intervals with digit `d`, the proportion having exact valuation `r` tends to `2^(-r)`. Consequently the interval-average valuation tends to `sum_(r>=1) r/2^r = 2`. This is a counting statement about fixed intervals, not a statement that actual trajectories sample those residue classes independently.

## Decimal-sector structure

6. **Piecewise affine form.** On each leading-digit interval `[d·10^k,(d+1)·10^k)`, the odd branch is `n -> 3n+(2d+1)`. Thus the frozen odd rule stitches together the nine corrections `3,5,7,9,11,13,15,17,19` according to decimal magnitude and leading digit.

7. **Single-digit odd inputs coincide with the raw 5x+1 map.** For odd `n ∈ {1,3,5,7,9}`, `L(n)=n`, so `3n+2L(n)+1=5n+1`. In particular, the distinguished cycle uses odd states only `1` and `3`, so `1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1` is also the familiar positive cycle of the raw `5x+1` map. This concerns the cycle only; the full frozen map is not the `5x+1` map once multi-digit odd inputs are reached.

8. **Odd-branch increments away from decimal boundaries.** If odd `n` and `n+2` have the same leading digit, then `T(n+2)-T(n)=6`.

9. **Internal leading-digit boundary jump.** Let `B=d·10^k` with `k≥1` and `d∈{2,…,9}`. Then `T(B+1)-T(B-1)=8`.

10. **Power-of-ten downward jump.** Let `B=10^k` with `k≥1`. Then `L(B-1)=9`, `L(B+1)=1`, and `T(B+1)-T(B-1)=-10`. Therefore the odd branch is not globally monotone.

## Relation to finite-modulus generalized Collatz maps

11. **No finite-modulus residue-class-wise affine representation on the positive integers.** There is no positive integer modulus `m` for which the frozen map is affine on every residue class modulo `m`.

    Proof sketch: if `m` is odd, any residue class contains infinitely many even and odd positive integers, forcing one affine formula to agree with both slope `1/2` on the even subsequence and slope `3` on suitable odd subsequences. If `m` is even, take an odd residue class. For every leading digit `d`, sufficiently large intervals `[d·10^k,(d+1)·10^k)` contain at least two integers in that residue class. Agreement there forces slope `3` and intercept `2d+1`; a different leading digit forces a different intercept, contradiction.

    This separates the frozen map from the standard finite-modulus residue-class-wise affine (RCWA) class. It does not establish novelty relative to broader state-dependent or digit-dependent classes.

## Inverse structure

12. **One-step inverse candidates.** Every positive target `m` has the even predecessor `2m`. An odd predecessor with leading digit `d` must satisfy `n=(m-2d-1)/3`, and is valid exactly when this is a positive odd integer with leading digit `d`.

13. **At most three arithmetic odd-predecessor candidates.** Divisibility by `3` restricts `d` to one residue class modulo `3`, so among `d=1,…,9` there are at most three values to test before the leading-digit condition is applied.

14. **Odd-predecessor multiplicity is essentially unique.** If two valid odd predecessors have leading digits `d1<d2`, then `d2-d1` is `3` or `6`, and the predecessors differ by `2` or `4`. For predecessors at least `10`, two integers this close can only have equal leading digits, adjacent leading digits across an internal decimal boundary, or leading digits `9` and `1` across a power of ten; none has digit difference `3` or `6`. Checking the remaining small case leaves one exception: `T(7)=T(11)=36`. Hence every positive target other than `36` has at most one odd predecessor, while `36` has exactly odd predecessors `7` and `11` (plus even predecessor `72`).

## Heuristic direction, not theorem

The exact interval-density result in item 5 gives the same geometric valuation profile as the usual accelerated Collatz heuristic. If actual large odd trajectory states behaved as though they sampled these classes without strong bias, then `E[v2]≈2` and the dominant multiplicative log drift would be `log 3 - 2 log 2 = log(3/4) < 0`, with additive correction `(2L(n)+1)/n` small at large `n`.

This is **HEURISTIC** when applied to trajectories. Decimal-leading-digit correlations, boundary crossings, and state dependence could invalidate an independence model.
