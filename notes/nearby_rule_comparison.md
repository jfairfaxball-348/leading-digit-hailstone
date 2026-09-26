# Nearby-Rule Comparison

**Claim type: FINITE COMPUTATION.**

The comparison family was fixed before running it. The frozen correction vector is

c(d)=2d+1 = (3,5,7,9,11,13,15,17,19).

The purpose is not to optimize over rules. It is to test whether the frozen behavior looks automatic in a tiny, principled neighborhood.

## Family A — global shifts

Define c_b(d)=2d+b for b in {-3,-1,1,3,5}. The frozen map is b=1.

Exact cycle census for seeds 1..100,000 with a 100,000-step cap:

| b | observed cycles | unresolved |
|---:|---:|---:|
| -3 | 2 | 0 |
| -1 | 4 | 0 |
| 1 | 1 | 0 |
| 3 | 4 | 0 |
| 5 | 3 | 0 |

For the frozen b=1 rule, all 100,000 seeds entered the distinguished 7-cycle. Each of the four nonfrozen global shifts had more than one observed attracting cycle.

On seeds 1..10,000, the frozen rule also had the largest mean preperiod to first cycle entry among these five rules (72.3741 raw steps), the largest maximum preperiod (342 at seed 8403), and the largest observed excursion ratio in this metric sample (seed 3569 reaching 661,617,320). These are descriptive finite comparisons, not asymptotic statements.

## Family B — one-coordinate perturbations

For each digit d=1..9, change only c(d) by -2 or +2, leaving the other eight corrections frozen. This gives 18 rules.

Results through 100,000:

- 11 of 18 perturbations had multiple observed cycles.
- 7 of 18 had exactly one observed cycle.
- Several of the one-cycle perturbations preserve the distinguished 7-cycle; the d=3,+2 perturbation instead has a different observed 15-cycle.

Thus the frozen behavior is not generic in this immediate coordinate neighborhood, but it is not uniquely isolated either.

## Interpretation

This experiment supports **distinctiveness**, not uniqueness.

The strongest finite contrast is the global-shift family: b=1 is the only tested member with one observed cycle through 100,000. The one-coordinate family is more nuanced and is important precisely because it prevents over-selling that observation: convergence-like behavior survives in a substantial minority of nearby rules.

There is not enough evidence to call the frozen rule a phase-boundary point in any formal or asymptotic sense. A defensible statement is only that the tested neighborhood contains a mixture of single-attractor and multi-attractor behavior, with the frozen rule lying next to both kinds.

Reproduce with scripts/compare_nearby_rules.py. Machine-readable output is data/nearby_rule_comparison.json.
