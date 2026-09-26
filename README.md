# Leading-Digit Hailstone Dynamics

A controlled object-discovery and conjecture-testing pilot for the map

\[
T(n)=\begin{cases}
n/2,&n\text{ even},\\
3n+2L(n)+1,&n\text{ odd},
\end{cases}
\]

where `L(n)` is the leading decimal digit of the positive integer `n`.

The distinguished observed cycle is

`1 → 6 → 3 → 16 → 8 → 4 → 2 → 1`.

## Epistemic status

The central statement

> Every positive integer eventually enters the distinguished 7-cycle.

is a **conjecture**, not a theorem. The map is **not claimed to be novel**. Finite computation is evidence only. Equivalent mathematics under different notation counts as prior art.

The frozen pilot object is exactly the map above. Changes of multiplier, base, digit convention, or correction term belong in a separate comparison layer.

## Exact conventions

For this repository:

- `L(n)` means the first digit of the ordinary base-10 expansion of positive integer `n`, so `L(n) ∈ {1,…,9}`.
- `stopping_time(n)` means the first raw iteration `k ≥ 1` for which `T^k(n) < n`.
- `cycle_entry_time(n)` means the first raw iteration `k ≥ 0` for which `T^k(n)` is in `{1,2,3,4,6,8,16}`.
- `max_excursion(n)` is the maximum value seen through first distinguished-cycle entry (or over the examined prefix if a cap/other cycle intervenes).
- `excursion_ratio(n) = max_excursion(n)/n`, stored exactly as a rational pair where results are machine-readable.

## Reproducibility

The reference implementation is `src/leading_digit_hailstone/core.py`. An independently written checker with a different leading-digit implementation is in `src/leading_digit_hailstone/verify.py`.

```bash
python -m pip install -e .
python -m unittest discover -s tests
python scripts/verify_implementations.py
python scripts/reproduce_incoming.py
```

For a resumable batch sweep:

```bash
python scripts/sweep.py --stop 10000000 --checkpoint data/sweep_checkpoint.json
```

The incoming observations are preserved separately in `data/incoming_observations.json`. Reproduction output is written to `data/task1_reproduction.json`. The original 1,000-sample random claim did not include its RNG seed or sample list, so exact replay is impossible; the reproduction script runs a clearly labelled deterministic replacement sample instead.

## Pilot tasks

0. Scaffold — repository structure, rules, status, reference/verification implementations and reproducibility conventions.
1. Independent reproduction — reproduce incoming numerical claims without treating them as universal.
2. Dynamical census — extend exhaustive testing and catalogue records.
3. Structural decomposition — leading-digit intervals, parity, 2-adic valuation, transitions and inverse structure.
4. Cycle search — forward/inverse methods for bounded nontrivial cycles.
5. Prior-art audit — exact and mathematically equivalent constructions.
6. Pilot decision — choose one of the explicit STOP/CONTINUE gate outcomes in `ROADMAP.md`.

See `RESEARCH_RULES.md` before adding claims.
