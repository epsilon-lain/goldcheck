# Milestone 17 — an infinite six-prime exclusion family

Milestone 16 gives exact quadratic Clique–Shearer certificates for

\[
3^4\cdot5^2\cdot7\cdot11\cdot13\cdot P
\]

at `P=17,19,23`.  The remaining primes in the same one-parameter support can
be disposed of by the older McNew–Setty full-divisor bound, so the finite M16
frontier closes into an infinite family.

## Theorem

For every prime `P >= 17`,

\[
\boxed{3^4\cdot5^2\cdot7\cdot11\cdot13\cdot P}
\]

is not a covering number for a distinct covering system.

This is an infinite six-prime exclusion family.  It is **not** a solution of
the general odd distinct covering-system problem and no publication-level
novelty claim is made here without an external literature audit.

## 1. Small primes `17,19,23`

These are exactly the three first `a=4` frontier values already certified in
Milestone 16 by the quadratic second-moment argument.  The corresponding
numbers are

\[
34459425,\qquad38513475,\qquad46621575.
\]

The optimization corner reduction used there is separately audited in
`M16_AUDIT.md`.

## 2. Direct bound for every `P >= 29`

For

\[
N_P=3^4\cdot5^2\cdot7\cdot11\cdot13\cdot P,
\]

the McNew–Setty full-divisor variables are

\[
x_3=\frac{40}{81},\quad
x_5=\frac6{25},\quad
x_7=\frac17,\quad
x_{11}=\frac1{11},\quad
x_{13}=\frac1{13},\quad
x_P=\frac1P.
\]

For six prime coordinates the direct covering-density bound is

\[
R=e_1-e_3-e_4+2e_5+9e_6.
\]

Because the elementary symmetric polynomials are affine in the last coordinate
`x_P`, exact simplification gives

\[
\boxed{
R(P)=\frac{220676}{225225}+\frac{17833}{31185P}.
}
\]

The coefficient of `1/P` is positive, so `R(P)` is strictly decreasing in
`P`.  Moreover

\[
R(29)=\frac{58755581}{58783725}
=1-\frac{28144}{58783725}<1.
\]

Equivalently the real threshold is

\[
P>\frac{1159145}{40941}\approx28.31257.
\]

Hence every integer `P >= 29`, in particular every prime `P >= 29`, is
noncovering by the direct bound alone.

## 3. Close the prime range

The primes at least 17 are

`17,19,23`, or at least `29`.

Milestone 16 handles the first three and the direct bound handles the rest.
Therefore

\[
\boxed{
3^4\cdot5^2\cdot7\cdot11\cdot13\cdot P
\text{ is noncovering for every prime }P\ge17.
}
\]

Exact arithmetic for the bridge is independently checked in
`solver/m17_infinite_family.py`; no floating-point threshold is used by the
verifier.
