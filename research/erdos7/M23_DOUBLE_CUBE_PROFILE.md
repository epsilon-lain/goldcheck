# Milestone 23 — complete exclusion of the `(3,3,1,1,1,1)` six-prime profile

M22 exposes the next minimal profile outside the previously certified regions:

\[
(3,3,1,1,1,1).
\]

The McNew–Setty direct bound fails at exactly one exponent placement on the six smallest odd primes.  That remaining canonical family can be closed by re-optimizing the M14 `3`-adic Clique–Shearer affine certificate.

## Theorem

Let

\[
N=\prod_{i=1}^6 p_i^{a_i}
\]

be odd with six distinct prime factors, and suppose

\[
\boxed{\{a_1,\ldots,a_6\}=\{3,3,1,1,1,1\}.}
\]

Then `N` is not a covering number for a distinct covering system.

## 1. The only direct-bound exceptional exponent placement

The six-coordinate direct bound is coordinatewise increasing by the universal M22 derivative gap `719/1440`.  Hence every fixed exponent placement is worst at

\[
(3,5,7,11,13,17).
\]

There are 15 placements of the two exponent-3 coordinates.  Exact enumeration shows that only

\[
(3,3,1,1,1,1)
\]

on the two smallest primes has `R>=1`, namely

\[
R=\frac{378736}{375375}>1.
\]

The largest of the other 14 placements is `(3,1,3,1,1,1)` and already satisfies

\[
R=\frac{37123796}{37522485}
=1-\frac{398689}{37522485}<1.
\]

Thus only the canonical family with cubes on `3` and `5` remains.

## 2. The canonical small-prime family

Consider

\[
N_P=3^3\cdot5^3\cdot7\cdot11\cdot13\cdot P.
\]

Stage modulo `27`.  As in M14, at least 14 pure-3 fibres survive, the support box is

\[
b_S\le q_S(r)\le4b_S,
\]

and the cross-fibre budget is

\[
\sum_r q_S(r)\le27b_S.
\]

The only change from M14 is the 5-coordinate baseline

\[
x_5=\frac15+\frac1{25}+\frac1{125}=\frac{31}{125}.
\]

A new exact affine certificate uses nonnegative rational weights `lambda_S` stored in `solver/m23_double_cube_profile.py` and verifies

\[
\rho(q)+\sum_S\lambda_S q_S\ge C_P
\]

on the full 31-variable factor-4 box by the same exact `2^15` corner reduction as M14.

For `P=17,19,23`, the summed 14-fibre margins are respectively

\[
\boxed{
\frac{795361761}{21271250000},\qquad
\frac{58151681}{679250000},\qquad
\frac{410035473}{2616250000}
}>0.
\]

The non-5 Clique coordinate polynomials remain strictly positive, so the M14 one-coordinate completion argument turns `rho(q)>0` into an uncovered point.

Hence the three direct-bound exceptions `P=17,19,23` are noncovering.

## 3. Direct bridge for every `P>=29`

For the same one-parameter family, exact simplification gives

\[
R(P)=\frac{3294908}{3378375}+\frac{1933172}{3378375P}.
\]

The real threshold is

\[
P>\frac{1933172}{83467}\approx23.1609.
\]

Therefore every prime `P>=29` is directly excluded.  Together with the three affine certificates,

\[
3^3 5^3 7\cdot11\cdot13\cdot P
\]

is noncovering for every prime `P>=17`.

## 4. Close the four simple-prime coordinates

For a canonical ordered tuple with cubes on the two smallest primes:

* if the two smallest primes are not `(3,5)`, the minimal off-base anchor `(3,7,11,13,17,19)` already has `R<1`;
* if they are `(3,5)` but the four simple primes are not of the form `(7,11,13,P)`, the minimal remaining off-family anchor is `(7,11,17,19)`, for which
  \[
  R=\frac{3091888}{3108875}<1.
  \]

Coordinatewise monotonicity closes all larger tuples.

Combining the 14 noncanonical placements, the three exact affine certificates, and the two direct monotone bridges proves the complete exponent-profile theorem above.

All arithmetic is checked using `Fraction` in `solver/m23_double_cube_profile.py` and its tests.  This is an internal rigorous theorem candidate pending independent literature/novelty review; it does not solve the general odd distinct covering-system problem.
