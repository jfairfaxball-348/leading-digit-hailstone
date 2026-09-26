# Initial Prior-Art Audit

**Status:** preliminary search layer for Task 5, dated 2026-09-26. This is not a novelty determination.

The audit is equivalence-focused: absence of the literal formula is weak evidence only. Equivalent mathematics under different notation counts as prior art.

## 1. Finite-modulus generalized Collatz / RCWA maps

Stefan Kohl's residue-class-wise affine framework uses a finite modulus whose residue-class restrictions are affine.

Sources:

- Stefan Kohl, *Algorithms for a class of infinite permutation groups*, Journal of Symbolic Computation 43 (2008), 545–581. DOI: https://doi.org/10.1016/j.jsc.2007.12.001
- RCWA definitions: https://stefan-kohl.github.io/rcwa/doc/chap2.html

**Classification:** related general Collatz framework, but not an exact containment of the frozen object. `notes/structural_facts.md` proves that the leading-digit rule has no finite-modulus residue-class-wise affine representation on the positive integers. Decimal leading-digit sectors cut across every fixed finite congruence partition.

This is narrower than a novelty claim: broader state-dependent piecewise-affine frameworks may still subsume the map.

## 2. Fixed `3x+k` maps

Bell and Lagarias study maps with odd branch `(3n+k)/2` and even branch `n/2` under their stated congruence restrictions on `k`.

Source:

- Jason P. Bell and Jeffrey C. Lagarias, *3x+1 inverse orbit generating functions almost always have natural boundaries*, Acta Arithmetica 170 (2015), 101–120: https://arxiv.org/abs/1408.6884

**Classification:** close local analogue, not the frozen system. In a fixed leading-digit sector the frozen odd branch is `3n+k` with `k=2d+1`; after its compulsory first division by two it locally resembles a `3x+k` step. Globally, `k` changes with the decimal leading digit.

## 3. Distinguished cycle and the `5x+1` problem

For a single-digit odd integer, `L(n)=n`, so the frozen odd rule becomes `5n+1`. Consequently

`1 -> 6 -> 3 -> 16 -> 8 -> 4 -> 2 -> 1`

is exactly the standard positive cycle of the raw `5x+1` map.

Sources:

- Alex V. Kontorovich and Jeffrey C. Lagarias, *Stochastic Models for the 3x+1 and 5x+1 Problems*: https://arxiv.org/abs/0910.1944
- OEIS A328011: https://oeis.org/A328011
- OEIS A393125: https://oeis.org/A393125

**Classification:** direct prior art for the cycle itself, not for the full frozen leading-digit map. The observed 7-cycle must not be presented as a distinctive new cycle.

## 4. Digit maps

Chase studies digit maps of the form `f(Σ a_i b^i)=Σ f_*(a_i)`, a sum of per-digit contributions.

Source:

- Zachary Chase, *On the Iterates of Digit Maps*, Integers 18 (2018), A86: https://arxiv.org/abs/1609.03263

**Classification:** digit-dependent dynamics, but not an immediate containment. The frozen map uses only the most significant decimal digit to choose an additive correction to an affine map of the whole integer.

## 5. Leading digits in ordinary Collatz trajectories

Leading-digit/Benford behavior for ordinary `3x+1` has established literature.

Source:

- Alex V. Kontorovich and Steven J. Miller, *Benford's Law, Values of L-functions and the 3x+1 Problem*, Acta Arithmetica 120 (2005), 269–297: https://arxiv.org/abs/math/0412003

**Classification:** observational/statistical leading-digit literature, not a rule in which the leading digit controls the next iterate.

## 6. Literal and repository search snapshot

Initial web searches covered literal variants of `3n+2L(n)+1`, `3x+2L(x)+1`, leading-digit Collatz rules, and combinations of `3n`, leading digit, and additive correction. Initial GitHub code searches included `3n+2L(n)+1`, `3*x 2*leading_digit`, and leading-digit/Collatz combinations.

No exact implementation or paper matching the frozen formula surfaced in this first pass. The connected GitHub code search for the exact query `3n+2L(n)+1` returned zero results on 2026-09-26.

**Epistemic status:** negative search evidence only. This does **not** justify `new`, `original`, `unique`, or `previously unknown`. Search coverage is incomplete and a broader class may contain the construction without displaying this formula literally.

## Provisional audit position

- the **cycle itself has clear prior art** via `5x+1`;
- the map has **close local `3x+k` analogues**;
- the map is **not** a standard finite-modulus RCWA map, by an elementary structural argument;
- common sum-of-digits-style digit-map frameworks do not immediately identify it;
- leading-digit studies of ordinary Collatz are mainly observational rather than state-controlling;
- **no conclusion on novelty of the full frozen map is yet warranted**.

Task 5 remains open. The next layer should target broader state-dependent/piecewise affine integer dynamics, automata/transducer-defined maps, radix-dependent arithmetic maps, OEIS/sequence signatures, and older generalized-Collatz bibliographies.

## 7. Other leading-digit-controlled integer iterations

The leading digit has been used as an active part of other integer dynamical rules. One recent example is the `b`-elated function, which multiplies the leading base-`b` digit by the sum of the squares of all digits.

Source:

- N. Bradley Fox, Nathan H. Fox, Helen G. Grundman, Rachel Lynn, Changningphaabi Namoijam, Mary Vanderschoot, *Elated Numbers*: https://arxiv.org/abs/2409.09863 (later published in *La Matematica*).

**Classification:** meaningful adjacent prior art for the general idea of a leading digit actively controlling an integer iteration, but not an algebraic containment of the frozen map. It reinforces that any eventual distinctiveness claim must be about the specific leading-digit-dependent Collatz-style affine mechanism, not about the use of a leading digit in dynamics per se.
