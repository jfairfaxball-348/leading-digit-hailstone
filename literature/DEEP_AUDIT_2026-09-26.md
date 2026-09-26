# Deep Prior-Art Audit — 2026-09-26

**Status:** literature/search evidence only. This is not a novelty determination.

The audit asks for exact or essentially equivalent mathematics, not a literal formula match. A broad class counts as prior art only if the frozen object is naturally contained in it in a mathematically informative way; a universal programming formalism that can encode arbitrary computable maps is not by itself a meaningful identification of this object.

## Search target

The frozen odd branch can be restated as follows:

For odd n with leading decimal digit d, choose the correction c_d from

3, 5, 7, 9, 11, 13, 15, 17, 19

and apply 3n+c_d; for even n apply n/2.

Searches therefore included generalized Collatz / an+b maps, periodically linear and residue-class-wise affine maps, 3x+k systems, radix-dependent and digit maps, leading-digit-controlled iterations, automata/transducer descriptions, OEIS, repositories, and MathOverflow/Math StackExchange queries.

## Candidate classes and sources

### 1. Classical generalized Collatz / periodically linear / RCWA frameworks

Jeffrey Lagarias, “The 3x+1 problem and its generalizations,” American Mathematical Monthly 92 (1985), 3–23, DOI 10.2307/2322189, gives a taxonomy in which generalized Collatz functions are affine on residue classes modulo a fixed finite modulus.

R. N. Buttsworth and K. R. Matthews, “On some Markov matrices arising from the generalized Collatz mapping,” Acta Arithmetica 55 (1990), 43–57, DOI 10.4064/aa-55-1-43-57, studies this finite-residue generalized-Collatz setting.

Stefan Kohl, “Wildness of iteration of certain residue-class-wise affine mappings,” Advances in Applied Mathematics 39 (2007), 322–328, DOI 10.1016/j.aam.2006.08.003, and “Algorithms for a class of infinite permutation groups,” Journal of Symbolic Computation 43 (2008), 545–581, DOI 10.1016/j.jsc.2007.12.001, develop the RCWA framework.

Pascal Michel, “Problems in number theory from busy beaver competition,” Logical Methods in Computer Science 11 (2015), surveys the overlapping terminology: Collatz-type iteration functions, generalized Collatz mappings, one-state linear operator algorithms, periodically linear functions, Collatz-like functions, and RCWA mappings.

**Classification: close superclass, but not containing this object as a finite-modulus instance.**

The repository’s elementary non-RCWA argument shows that no fixed finite modulus makes the frozen map affine on every congruence class. Decimal leading-digit sectors cross every fixed congruence partition. Therefore these standard generalized-Collatz definitions do not contain the full frozen map merely by a change of notation.

This does not exclude broader state-dependent piecewise-affine classes.

### 2. Fixed 3x+k systems

Franz Wegner, “The Collatz Problem generalized to 3x+k,” arXiv:2101.08060 (2021), studies fixed odd corrections k.

Alex V. Kontorovich and Jeffrey C. Lagarias, “Stochastic Models for the 3x+1 and 5x+1 Problems,” arXiv:0910.1944, treats 3x+1 and 5x+1 stochastic behavior.

**Classification: close analogue.**

Within each leading-digit sector the frozen odd branch is a fixed 3x+k rule, but k changes when the decimal leading digit changes. No fixed-k paper located in this audit gives the full state-dependent rule.

### 3. The distinguished 7-cycle

OEIS A328011 records the 5x+1 sequence beginning at 1:

1, 6, 3, 16, 8, 4, 2, 1, ...

OEIS A393125 and the Kontorovich–Lagarias 5x+1 literature likewise record this positive cycle.

**Classification: exact prior art for the cycle itself.**

For single-digit odd n, L(n)=n, hence the frozen odd rule is 5n+1. The cycle must not be used as evidence of novelty of the full map.

### 4. Digit maps and active leading-digit dynamics

Zachary Chase, “On the Iterates of Digit Maps,” Integers 18 (2018), A86, arXiv:1609.03263, studies maps built from digit contributions.

N. Bradley Fox, Nathan H. Fox, Helen G. Grundman, Rachel Lynn, Changningphaabi Namoijam, and Mary Vanderschoot, “Elated Numbers,” arXiv:2409.09863, later published in La Matematica, defines a radix-dependent iteration in which the leading digit actively multiplies a digit-square sum. OEIS A376270/A377087/A377088 record associated elated-number dynamics.

**Classification: close thematic/structural analogue, not an equivalent formulation.**

These sources establish that using the leading digit as an active state variable in integer dynamics is not itself novel. They do not supply the frozen parity/affine map.

### 5. Leading digits of ordinary Collatz trajectories

Alex V. Kontorovich and Steven J. Miller, “Benford’s Law, Values of L-functions and the 3x+1 Problem,” Acta Arithmetica 120 (2005), 269–297, arXiv:math/0412003, studies leading-digit statistics in classical Collatz-related sequences.

**Classification: thematic only.**

Here the leading digit is an observed statistic, not the control variable selecting the next arithmetic rule.

### 6. Automata, transducers, and computability frameworks

Conway’s “Unpredictable Iterations” (1972) and later generalized-Collatz undecidability work concern finite-residue affine programs broad enough to encode computation. Recent papers also encode ordinary Collatz digitwise using finite-state symbolic machinery.

**Classification: broad computational framework / thematic.**

A sufficiently general automaton or program can encode the leading-digit map, but that is not an identification of the mathematical construction and does not constitute exact prior art for the conjecture. The standard finite-residue Collatz class remains excluded by the repository’s non-RCWA result.

### 7. OEIS, repository, and forum search

Searches included:

- the literal formula and spacing/notation variants;
- the correction-vector formulation 3n+c with c in 3,5,...,19 selected by first digit;
- “leading digit Collatz,” “most significant digit Collatz,” “digit-dependent Collatz,” and “Collatz leading decimal digit”;
- the initial value sequence of the map on n=1,2,...;
- GitHub code search combinations of leading_digit / most_significant_digit with Collatz and 3*n;
- MathOverflow and Math StackExchange searches for leading-digit-controlled Collatz variants.

The GitHub hits located in this pass were overwhelmingly Benford/diagnostic code or unrelated utilities. The OEIS search recovered the known 5x+1 cycle but did not surface an entry matching the full frozen map. Forum searches did not locate an exact match.

**Classification: negative search evidence only.**

## Current audit conclusion

- **Exact match:** none identified.
- **Equivalent formulation:** none identified.
- **Direct standard superclass containing the object essentially for free:** none identified. The main classical finite-modulus generalized-Collatz/RCWA class is explicitly excluded.
- **Close analogues:** fixed 3x+k maps; digit maps; active leading-digit elated maps.
- **Exact prior art for a component:** the distinguished 7-cycle via 5x+1.
- **Novelty status of the full rule:** unresolved.

The present audit materially reduces the risk that the rule is just a standard finite-modulus generalized Collatz instance or a literal rediscovery of an indexed sequence. It does not justify “new,” “original,” “unique,” “previously unknown,” or historical priority language.

## Remaining risk areas

The next audit should emphasize older recreational mathematics, theses and dissertations, non-English sources, books and problem columns, poorly indexed digit-dependent recurrences, and broader radix/state-dependent affine systems. A human bibliographic search through generalized-Collatz bibliographies remains higher value than adding more literal web queries.

## Addendum: further equivalence controls

### Matthews-Watts finite-residue generalization

K. R. Matthews and A. M. Watts, “A generalization of Hasse's generalization of the Syracuse algorithm,” Acta Arithmetica 43 (1984), 167–175, DOI 10.4064/aa-43-2-167-175, belongs to the older generalized-Collatz literature in which arithmetic branches are selected through finite congruence information.

**Classification: close general framework, not an exact containment.**

It reinforces the distinction already drawn above: the repository's non-RCWA argument separates the frozen leading-decimal-sector rule from fixed finite-residue affine systems.

### Decimal digit operations composed with Collatz

OEIS A129121 records an iteration applying a Collatz operation followed by decimal digit reversal.

**Classification: close analogue.**

This is useful prior art against any broad claim that decimal digit operations have not been combined with Collatz-like iteration. It is not equivalent to choosing the additive correction 3,5,...,19 from the leading digit.

### Automaton implementation of ordinary Collatz

“Automaton implementations of the process of generating a Collatz sequence,” Cybernetics and Systems Analysis (2012), DOI 10.1007/s10559-012-9380-4, studies an iterative-automaton implementation of the Hasse/Collatz process.

**Classification: thematic only.**

It shows that automata/transducer language is established around Collatz computation, but the source identified here implements the ordinary process rather than a leading-digit-controlled affine rule.

### Thesis and recreational search layer

Targeted searches combining generalized Collatz, digit dependence, leading/most-significant digit, thesis/dissertation terminology, and recreational mathematics did not identify an exact or equivalent full-map construction in this pass.

**Classification: negative search evidence only.**

This layer is especially incomplete because older theses, problem columns, books, and non-English sources can be poorly indexed. Its value is to document coverage, not to increase the novelty status.

