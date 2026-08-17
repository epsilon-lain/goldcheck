# Milestone 18 — three-parameter six-prime exclusion family

Milestone 16 handled the three exceptional triples `(11,13,17)`,
`(11,13,19)`, `(11,13,23)` with exact quadratic Clique–Shearer certificates.
Milestone 17 then observed that, with the first two variable primes fixed at
`11,13`, the McNew–Setty full-divisor bound closes the tail from `29` onward.

The same monotonicity gives a substantially larger family.

## Theorem

Let `p<q<r` be distinct primes with `p>=11`. Then

\[
\boxed{3^4\cdot5^2\cdot7\cdot p\cdot q\cdot r}
\]

is not a covering number for a distinct covering system.

Equivalently, every exponent pattern

\[
3^4\,5^2\,7\,p\,q\,r
\]

with three further distinct prime factors at least `11` is excluded.
This is a three-parameter infinite six-prime family. It is not a solution of
the general odd distinct covering-system problem, and no publication-level
novelty claim is made here without a separate literature audit.

## 1. The direct six-coordinate bound is coordinatewise increasing

For six full-divisor variables `x_1,...,x_6`, the McNew–Setty bound used in
M9/M17 is

\[
R=e_1-e_3-e_4+2e_5+9e_6.
\]

For one coordinate `x_i`, with the other five coordinates denoted by `y`,

\[
\frac{\partial R}{\partial x_i}
=1-e_2(y)-e_3(y)+2e_4(y)+9e_5(y)
\ge 1-e_2(y)-e_3(y).
\]

In the present family the six coordinates are

\[
\frac{40}{81},\quad\frac6{25},\quad\frac17,
\quad\frac1p,\quad\frac1q,\quad\frac1r,
\]

and every variable prime is at least `11`. After sorting, any five coordinates
remaining after deletion are coordinatewise bounded by

\[
U=\left(\frac{40}{81},\frac6{25},\frac17,\frac1{11},\frac1{11}\right).
\]

Since elementary symmetric polynomials are increasing in nonnegative
coordinates,

\[
e_2(y)+e_3(y)\le e_2(U)+e_3(U)
=\frac{111682}{245025}.
\]

Therefore throughout the whole relevant box

\[
\boxed{
\frac{\partial R}{\partial x_i}
\ge\frac{133343}{245025}>0.
}
\]

Thus `R` increases with every reciprocal prime coordinate, and hence decreases
whenever any of `p,q,r` is increased.

## 2. Only three ordered triples escape the direct bound

Sort the three variable primes as `p<q<r`.

If `(p,q)=(11,13)` and `r>=29`, monotonicity reduces everything to

\[
R(11,13,29)=\frac{58755581}{58783725}
=1-\frac{28144}{58783725}<1.
\]

If `(p,q)!=(11,13)`, distinctness and primality imply

\[
p\ge11,\qquad q\ge17,\qquad r\ge19.
\]

Hence monotonicity reduces this entire region to

\[
R(11,17,19)=\frac{7187843}{7194825}
=1-\frac{6982}{7194825}<1.
\]

So the only ordered prime triples with `p>=11` not already killed by the direct
bound are

\[
(11,13,17),\quad(11,13,19),\quad(11,13,23).
\]

## 3. The three exceptions are exactly M16

Those three triples correspond to

\[
\begin{aligned}
3^4 5^2 7\cdot11\cdot13\cdot17&=34459425,\\
3^4 5^2 7\cdot11\cdot13\cdot19&=38513475,\\
3^4 5^2 7\cdot11\cdot13\cdot23&=46621575,
\end{aligned}
\]

all excluded in Milestone 16 by exact quadratic second-moment
Clique–Shearer certificates.

Combining M16 with the two monotone direct-bound regions proves the theorem.
Exact Fraction arithmetic for the bridge and monotonicity margin is checked in
`solver/m18_three_parameter_family.py` and
`solver/test_m18_three_parameter_family.py`.
