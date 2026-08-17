# Milestone 20 — complete exclusion of the `(4,2,1,1,1,1)` six-prime exponent profile

Milestone 19 removes the remaining freedom in the four simple-prime coordinates
when the two repeated prime powers are `3^4` and `5^2`.  A finite exact
rearrangement audit now removes the assumption that the exponents `4` and `2`
are attached to the two smallest primes at all.

## Theorem

Let

\[
N=\prod_{i=1}^6 p_i^{a_i}
\]

be odd with six distinct prime factors, and suppose the exponent multiset is

\[
\boxed{\{a_1,\ldots,a_6\}=\{4,2,1,1,1,1\}.}
\]

Then `N` is not a covering number for a distinct covering system.

Thus an entire six-prime exponent profile is excluded, independently of the
actual odd primes and independently of which primes carry the exponents `4`
and `2`.

## 1. Uniform monotonicity of the McNew–Setty six-coordinate bound

For a prime power `p^a`, write

\[
x(p,a)=\sum_{j=1}^a p^{-j}.
\]

The six-coordinate direct bound is

\[
R=e_1-e_3-e_4+2e_5+9e_6.
\]

As before,

\[
\frac{\partial R}{\partial x_i}
\ge1-e_2(y)-e_3(y).
\]

For six distinct odd primes and exponents at most `4`, sort the six `x`
coordinates decreasingly.  Their first five coordinates satisfy the simple
rank bounds

\[
x_{(1)}<\frac12,\quad
x_{(2)}<\frac14,\quad
x_{(3)}<\frac16,\quad
x_{(4)}<\frac1{10},\quad
x_{(5)}<\frac1{12}.
\]

Indeed

\[
x(3,4)=\frac{40}{81}<\frac12,
\]
\[
x(5,4)=\frac{156}{625}<\frac14,
\]
\[
x(7,4)=\frac{400}{2401}<\frac16,
\]
\[
x(11,4)=\frac{1464}{14641}<\frac1{10},
\]
\[
x(13,4)=\frac{2380}{28561}<\frac1{12}.
\]

Therefore every five-coordinate remainder is bounded by

\[
U=\left(\frac12,\frac14,\frac16,\frac1{10},\frac1{12}\right),
\]

for which

\[
e_2(U)+e_3(U)=\frac{721}{1440}.
\]

Hence throughout the complete exponent-profile domain

\[
\boxed{\frac{\partial R}{\partial x_i}\ge\frac{719}{1440}>0.}
\]

So, for any fixed assignment of exponents to the ordered prime positions, the
direct bound is maximized at the six smallest odd primes

\[
(3,5,7,11,13,17).
\]

## 2. Exact audit of all 30 exponent placements

There are exactly

\[
6\cdot5=30
\]

placements of the exponents `4` and `2` among six ordered prime positions.
Evaluate all 30 exactly at `(3,5,7,11,13,17)`.

Only the canonical placement

\[
(4,2,1,1,1,1)
\]

has `R>=1`, with

\[
R=\frac{293467}{289575}>1.
\]

Among the other 29 placements the maximum is attained at

\[
(4,1,2,1,1,1),
\]

and equals

\[
\boxed{
\frac{16047137}{16081065}
=1-\frac{33928}{16081065}<1.
}
\]

By the monotonicity above, every noncanonical exponent placement is therefore
excluded by the direct bound for every choice of six distinct odd primes.

## 3. Canonical placement

It remains to take the ordered primes `p_1<...<p_6` with exponent placement

\[
(4,2,1,1,1,1).
\]

If `(p_1,p_2)=(3,5)`, Milestone 19 applies to the four remaining distinct
primes `p_3,...,p_6>=7` and excludes the number.

If `(p_1,p_2)!=(3,5)`, the ordered prime tuple is coordinatewise at least

\[
(3,7,11,13,17,19),
\]

and the direct bound at that minimal off-base anchor is already

\[
R=\frac{54428893}{61108047}
=1-\frac{6679154}{61108047}<1.
\]

Monotonicity closes all larger canonical tuples.

This proves the theorem.

The 30-placement scan, the monotonicity margin, and both direct-bound anchors
are verified exactly with `Fraction` arithmetic in
`solver/m20_exponent_profile.py` and its tests.  This remains an internal
rigorous theorem candidate pending independent literature/novelty review; it
does not solve the general odd distinct covering-system problem.
