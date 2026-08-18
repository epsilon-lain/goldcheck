# Milestone 53 — every six-prime profile with exactly two repeated coordinates is excluded

This milestone replaces a growing list of individual exponent profiles by one
structural theorem candidate.

Let

\[
N=\prod_{i=1}^6 p_i^{a_i},
\qquad 3\le p_1<\cdots<p_6
\]

with exactly four exponents equal to one and the other two exponents arbitrary
finite integers at least two.  Then the project now proves

\[
\boxed{N\text{ is noncovering}.}
\]

Equivalently, every sorted exponent profile

\[
\boxed{(A,B,1,1,1,1),\qquad A\ge B\ge2}
\]

is excluded.

The proof has two reductions: first send both repeated-coordinate charges to
infinity in the McNew--Setty bound; then use the special-coordinate limit
certificates M48/M52 and the deficiency recurrence.

## 1. Double-infinity direct reduction

If a prime `p` is repeated to any finite exponent,

\[
x_p(a)=\sum_{j=1}^a p^{-j}<\frac1{p-1}.
\]

M22 proves that the six-prime direct bound is strictly increasing in every
charge coordinate.  Therefore replacing **both** repeated coordinates by

\[
x_p(\infty)=\frac1{p-1}
\]

gives a uniform upper bound for every choice of the two finite exponents.

At the minimal odd primes `(3,5,7,11,13,17)`, there are only 15 unordered
choices of the two repeated positions.  Exact evaluation leaves only

\[
\{3,5\},\qquad \{3,7\}.
\]

The corresponding double-limit bounds are

\[
R_{3,5}^{\infty,\infty}=\frac{747}{728}>1,
\qquad
R_{3,7}^{\infty,\infty}=\frac{48889}{48620}>1.
\]

The largest of the other thirteen position pairs is repeated primes `{3,11}`:

\[
\boxed{R^{\infty,\infty}=\frac{153903}{154700}<1.}
\]

Hence any possible survivor must repeat prime 3 together with prime 5 or prime
7.

## 2. The universal prime templates are finite

For repeated primes `(3,5)`, exact coordinatewise `R<1` boundary anchors reduce
all increasing prime tuples to 22 survivors:

```text
(3,5,7,11,13,17)  (3,5,7,11,13,19)  (3,5,7,11,13,23)
(3,5,7,11,13,29)  (3,5,7,11,13,31)  (3,5,7,11,13,37)
(3,5,7,11,13,41)  (3,5,7,11,13,43)  (3,5,7,11,13,47)
(3,5,7,11,13,53)  (3,5,7,11,13,59)  (3,5,7,11,13,61)
(3,5,7,11,13,67)  (3,5,7,11,13,71)  (3,5,7,11,13,73)
(3,5,7,11,13,79)  (3,5,7,11,17,19)  (3,5,7,11,17,23)
(3,5,7,11,17,29)  (3,5,7,11,17,31)  (3,5,7,11,19,23)
(3,5,7,13,17,19)
```

The exact boundary values include

\[
R(3,5,7,11,13,83)=\frac{60423}{60424}<1,
\]

\[
R(3,5,7,11,17,37)=\frac{386361}{387464}<1,
\]

\[
R(3,5,7,11,19,29)=\frac{17823}{17864}<1,
\]

and analogous off-base anchors recorded in the verifier.

For repeated primes `(3,7)`, only two prime tuples survive:

```text
(3,5,7,11,13,17)
(3,5,7,11,13,19)
```

with the next canonical boundary already below one:

\[
R(3,5,7,11,13,23)=\frac{65557}{65780}<1.
\]

Thus every exactly-two-repeated problem reduces to 24 prime templates, with the
two exponents still completely arbitrary.

## 3. Arbitrary exponent on prime 3

Fix one of the 24 templates.  Let `u>=2` be the exponent on prime 3 and let
`v>=2` be the arbitrary finite exponent on the other repeated prime.

For `u<=3`, the earlier complete `(A,2,1,1,1,1)` and
`(A,3,1,1,1,1)` ray closures already cover every possible `v`.

For `u=4`:

- repeated `(3,5)` uses M52's `a=4`, prime-5 infinite special-coordinate
  certificate, with
  \[
  \eta_{4,5^\infty}
  =\frac{204805547139351}{289578289000000}>0;
  \]
- repeated `(3,7)` uses M52's prime-7 limit, with
  \[
  \eta_{4,7^\infty}
  =\frac{31948860183767}{26593924500000}>0.
  \]

Because those certificates are already proved at the geometric-series limit,
they apply to every finite `v`.

For `u=5`, M48 gives the corresponding limit certificates

\[
\eta_{5,5^\infty}
=\frac{376679506003531}{289578289000000}>0,
\]

\[
\eta_{5,7^\infty}
=\frac{92070538867211}{53187849000000}>0.
\]

## 4. Every exponent `u>=6` follows by one uniform recurrence

For repeated primes `(3,5)`, charge the divisor-sum factor of the arbitrary
finite power `5^v` by its infinite limit.  At the worst reference simple primes
`7,11,13,17`,

\[
\frac{\sigma(M)}M
<
\frac54\frac87\frac{12}{11}\frac{14}{13}\frac{18}{17}
=
\boxed{\frac{4320}{2431}}.
\]

Starting from the M48 `a=5` margin, the first lifted normalized deficiency gap
is

\[
\boxed{
g_6=
3\eta_{5,5^\infty}-\frac{4320}{2431}
=
\frac{615444438010593}{289578289000000}>0.
}
\]

Moreover

\[
g_6>\frac12\frac{4320}{2431}.
\]

Therefore, if `s=4320/2431`,

\[
g_{u+1}\ge3g_u-s
\]

stays positive and in fact increases forever.  Explicitly

\[
g_u\ge
3^{u-6}g_6-rac{s}{2}(3^{u-6}-1)>0.
\]

Exactly the same argument works for repeated primes `(3,7)`, with

\[
s=\frac76\frac65\frac{12}{11}\frac{14}{13}\frac{18}{17}
=rac{21168}{12155}
\]

and

\[
\boxed{
g_6=
\frac{61194894067211}{17729283000000}>0>
\frac{s}{2}-g_6.}
\]

All coordinatewise larger simple-prime tuples only improve these bounds.

Hence every one of the 24 universal prime templates is noncovering for every
finite pair `(u,v)`, and every other prime tuple or repeated-position pair was
already eliminated by the double-infinity direct bound.

This proves the project theorem candidate

\[
\boxed{
(A,B,1,1,1,1)\text{ is noncovering for all finite }A\ge B\ge2.
}
\]

The exact structural verifier is
`solver/m53_two_repeated_coordinates.py`.  The heavy finite certificates it
uses are independently recorded in M48 and M52.
