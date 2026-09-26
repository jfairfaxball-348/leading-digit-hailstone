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

## Long weak-division stretches

15. **Arbitrarily long initial runs with exact valuation 1 exist.** For every m >= 1 there is a positive odd seed whose first m accelerated odd steps all satisfy v2(3n+2L(n)+1)=1.

    Proof idea: choose a real mantissa whose first m homogeneous multiplications by 3/2 avoid all decimal leading-digit boundaries, so the corresponding digit word is stable on an open interval. For that fixed digit word, the requirement that each accelerated state remain odd selects exactly one lift at each binary digit, hence one residue class modulo 2^(m+1). A sufficiently large decimal scaling of the stable interval is longer than this modulus and contains a representative of that class. The additive digit corrections are bounded at fixed m, so at sufficiently large scale they do not change the prescribed leading-digit word. The full proof is in notes/arbitrarily_long_weak_division.md.

    Consequently there is no uniform finite bound on consecutive growth-favouring v2=1 accelerated steps. This is an elementary existence fact, not a divergence result.

## Additional accelerated block facts

16. **Direction above 19 is determined by the exact valuation.** For odd x>19, write the accelerated successor as x'=(3x+c)/2^r with c=2L(x)+1<=19. If r=1 then x'>x. If r>=2 then x'<x. Therefore every large accelerated-cycle minimum leaves with r=1 and is entered with r>=2.

17. **Exact multiplicative cycle identity.** For an accelerated odd cycle x_0,...,x_(q-1),

   2^R/3^q = product_i (1+c_i/(3x_i)).

   Hence if M=min_i x_i,

   1 < 2^R/3^q <= (1+19/(3M))^q.

   This is the map-specific cycle window used in notes/cycle_constraints.md. The general powers-of-2/powers-of-3 approximation strategy has classical Collatz-cycle prior art.

18. **Weak-run growth and one-step compensation.** If s consecutive accelerated steps have exact valuation 1, then

   2^s x_s = 3^s x_0 + sum_(j=0)^(s-1) 3^(s-1-j)c_j 2^j,

   and therefore x_s>(3/2)^s x_0. If the next accelerated step has valuation r and already returns to x_(s+1)<=x_0, then necessarily

   2^(r+s)>3^(s+1).

   Thus arbitrarily long weak runs cannot in general be neutralized by a valuation bound independent of the run length. See notes/weak_run_compensation.md.

19. **One-rise/one-fall cycles have a period-independent product envelope and Farey block transfer.** Consider an accelerated cycle entirely above 19 whose valuation word, after rotation to its minimum M, consists of a nonempty r=1 rise block followed by a nonempty r>=2 fall block. This is equivalent to exactly one strict local minimum and one strict local maximum per period. Rise states satisfy x_i>=(3/2)^i M, with strict inequality away from the minimum. Reading the fall block backward from M gives x_(q-t)>=19+(4/3)^t(M-19). Inserting these geometric state bounds into the exact product identity yields

   1 < 2^R/3^q <= M(M-19)/(M^2-57M+361).

   Because this bound is <2 at M>=5,000,001, the possible R is ceil(q log_2 3). If R_u/q_u is an exact upper approximation to log_2 3, R_l/q_l is an exact lower approximation, and R_u q_l-R_l q_u=1, then the Farey denominator theorem shows that no closer upper slope occurs before denominator q_u+q_l. For q>=q_u this also makes the upper absolute error R-q log_2 3 at least the error of R_u/q_u, so the same product-derived M_max applies throughout that whole denominator block.

   Iterating the exact Farey/Stern-Brocot neighbour mechanism with rigorous rational-log sign certificates and the same complete symbolic checker now excludes every structured period q<=890,638,885,192 under the 5M premise. Hence any remaining structured cycle has q>=890,638,885,193 and at least 369,648,535,671 consecutive exact-r=1 rise steps. The largest processed product range is M<=42,285,421,502,900 and becomes empty at rise depth 49. This is a bounded structured-class consequence, not a global cycle exclusion. See notes/one_minimum_cycles.md.

20. **Finite-range rise words have linear boundary-controlled symbolic complexity.** During s exact r=1 rises, the exact state x_i differs from the homogeneous point (3/2)^i M by a positive additive displacement less than 19((3/2)^i-1). Therefore the actual decimal sector can differ from the homogeneous sector only when M lies within a width-<19 window below a scaled decimal boundary. If J_s(L,U) counts all such scaled boundaries relevant to M in [L,U] through depth s, then at most 20 J_s(L,U)+1 exact decimal-sector words can occur. For fixed finite [L,U], J_s(L,U)=O(s). For each fixed word, the r=1 constraints impose one residue class modulo 2^(s+1). This proves low finite-range symbolic entropy, but does not force the final residue representative to miss its cell once cells are sub-modulus; residue position is the remaining obstruction.


## Heuristic direction, not theorem

The exact interval-density result in item 5 gives the same geometric valuation profile as the usual accelerated Collatz heuristic. If actual large odd trajectory states behaved as though they sampled these classes without strong bias, then `E[v2]≈2` and the dominant multiplicative log drift would be `log 3 - 2 log 2 = log(3/4) < 0`, with additive correction `(2L(n)+1)/n` small at large `n`.

This is **HEURISTIC** when applied to trajectories. Decimal-leading-digit correlations, boundary crossings, and state dependence could invalidate an independence model.
