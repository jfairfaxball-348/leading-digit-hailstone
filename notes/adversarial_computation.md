# Adversarial Computation — 2026-09-26

**Claim type: FINITE COMPUTATION.**

The goal is to break the conjecture, not to inflate the count of confirming random samples.

## Decimal boundaries

All odd seeds

d*10^k - 1 and d*10^k + 1

were tested for d=1..9 and k=1..18, giving 324 boundary-adjacent starts.

All 324 entered the distinguished cycle within the 200,000-step cap.

The largest cycle-entry time in this boundary set was 646 raw steps for

9,000,000,000,001 = 9*10^12 + 1.

The largest excursion ratio in this boundary set occurred at

900,000,000,000,001 = 9*10^14 + 1,

which reached 8,089,497,811,387,627,412 before entering the cycle.

## Repeated minimal 2-adic contraction

For an odd state n, the accelerated odd step divides 3n+2L(n)+1 by its exact power of two. The growth-favoring case is v2=1.

Among odd seeds 1..5,000,000, the longest initial run found with v2=1 at every accelerated step has length 21, beginning at seed 2,826,307.

The accelerated states begin

2,826,307 -> 4,239,463 -> 6,359,199 -> 9,538,805 -> 14,308,217 -> ... -> 14,097,337,415,

with v2=1 for 21 consecutive accelerated transitions; the next valuation is 3.

This is an adversarial growth mechanism, not evidence of divergence.

## Large constructed starts

For decimal lengths 50, 100, and 200, the search examined odd offsets in [-9999,9999] around every leading boundary d*10^(m-1), d=1..9, and chose starts maximizing the initial v2=1 run.

For all three lengths the best offset found was +1133 above the leading-5 boundary, giving a 17-step initial v2=1 run.

- 50-digit start: entered the distinguished cycle in 1,192 raw steps; peak has 54 digits.
- 100-digit start: entered in 2,340 raw steps; peak has 104 digits.
- 200-digit start: entered in 4,937 raw steps; peak has 204 digits.

These examples are deliberately constructed rather than uniformly random.

## Interpretation

No tested adversarial family produced a competing cycle or cap hit. The evidence is stronger than another uniform sample because it directly targets two exact structural hazards: decimal discontinuities and repeated weak division by two.

It remains finite evidence only. Reproduce with scripts/adversarial_search.py; summary data is in data/adversarial_2026-09-26.json.
