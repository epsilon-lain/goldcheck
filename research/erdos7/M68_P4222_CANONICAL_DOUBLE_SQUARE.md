# Milestone 68 — exact double-weighted-square certificate for the canonical `(4,2,2,2,1,1)` seed

The next six-prime frontier branch is

\[
(4,2,2,2,1,1).
\]

At the minimal odd primes `(3,5,7,11,13,17)`, exact McNew--Setty evaluation
leaves nine of the sixty exponent placements.  The canonical placement is the
hard integer

\[
N_*=3^4\cdot5^2\cdot7^2\cdot11^2\cdot13\cdot17
=\boxed{2653375725}.
\]

M68 gives an exact finite certificate that this integer is noncovering.  This
does **not** yet close the entire `(4,2,2,2,1,1)` profile, and it is not a
complete solution of Erdős Problem #7.

## 1. Two repeated non-special coordinates are retained exactly

Stage on `3^4`, giving 41 selected surviving fibres, and distinguish the
coordinate `5^2`.  For the two repeated non-special singleton supports retain
their two exact-divisor activation counts:

\[
\frac{q_{\{7\}}}{b_{\{7\}}}
 =1+\frac{7A_7+B_7}{8},
\qquad
\frac{q_{\{11\}}}{b_{\{11\}}}
 =1+\frac{11A_{11}+B_{11}}{12},
\]

with

\[
A_7,B_7,A_{11},B_{11}\in\{0,1,2,3,4\}.
\]

The simple singleton coordinates `13` and `17` retain exact activation levels
`1,...,5`.  The other eleven non-special support charges occur separately
concavely after the special-coordinate quadratic minimization, so their minima
are attained at box endpoints.

The resulting exact finite state space is

\[
25^2\cdot5^2\cdot2^{11}
=\boxed{32,000,000}.
\]

## 2. Penalty family

The pointwise certificate is the M66 goodness lower bound plus a nonnegative
family of:

* 11 linear support penalties;
* 32 distinct-support pair penalties;
* first and second factorial penalties on
  `A7,B7,A11,B11,A13,A17`.

All coefficients have denominator `10^6`.

M28 supplies the support budgets

\[
\sum_r q_S(r)\le81b_S,
\qquad
\sum_r q_S(r)q_T(r)\le197b_Sb_T,
\]

and M30 supplies, separately for every retained exact-divisor activation,

\[
\sum_r A(r)\le40,
\qquad
\sum_r {A(r)\choose2}\le18.
\]

## 3. Exact exhaustive verifier

Take

\[
C=\frac{34795}{100000}=0.34795,
\qquad
Q=10^9.
\]

The standalone C++ verifier uses `__int128` rational arithmetic and floors every
rational contribution downward before summation.  It exhausts all 32,000,000
reduced states and returns

```text
347959679 0 0 0 0 1 1 0
```

Therefore the rigorous pointwise lower minimum satisfies

\[
\boxed{347959679>347950000=QC},
\]

with integer floor slack

\[
\boxed{9679>0}.
\]

At the recorded minimizing state, an independent exact `Fraction` evaluation is

\[
\frac{
140088010630411032032228450809957711087
}{
402598364961488706245123434706160000000
}
>C.
\]

## 4. Positive summed quantitative margin

The exact special-coordinate global cost is

\[
\frac{5146853782690471671}{536534273587812500},
\]

and the exact added linear/pair/factorial feature cost is

\[
\frac{7945074076619350717}{1716909675481000000}.
\]

Hence the summed goodness margin is

\[
\boxed{
41C-\mathrm{special\ cost}-\mathrm{feature\ cost}
=
\frac{391707018496559429}{8584548377405000000}
>0.
}
\]

By the same quantitative goodness/completion mechanism audited in M39 and used
in M66, this positive margin gives genuine uncovered mass.  Thus

\[
\boxed{
3^4\cdot5^2\cdot7^2\cdot11^2\cdot13\cdot17
\text{ is noncovering}.
}
\]

Files:

* `solver/m68_p4222_canonical_double_square.py` — exact constants and theorem audit;
* `solver/m68_p4222_canonical_double_square_fast.cpp` — independent 32,000,000-state integer verifier;
* `solver/test_m68_p4222_canonical_double_square.py` — regression checks.

The remaining goal is to transport or reproduce the double-weighted-square
certificate across the other hard `(4,2,2,2,1,1)` placements and their prime
tails.
