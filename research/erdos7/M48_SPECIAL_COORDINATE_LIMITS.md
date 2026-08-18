# Milestone 48 — three repeated-coordinate exponents can be sent to infinity

Several staged Clique--Shearer certificates treat one post-stage prime as a
special repeated coordinate and the other four primes as the non-special
system.  The special coordinate itself never needs an integral activation
law: it is minimized continuously over its support box and charged only through
raw moment bounds.

This makes a useful strengthening possible.  Instead of certifying a fixed
finite exponent `b`, inflate its baseline

\[
x_p(b)=\sum_{j=1}^b p^{-j}
\]

to the geometric-series limit

\[
\boxed{x_p(\infty)=\frac1{p-1}.}
\]

Every actual grouped charge may be multiplied by
`x_p(infinity)/x_p(b)`.  The result remains a valid upper-probability vector;
normalized support loads are unchanged and the first/second moment budgets
become exactly the limit-baseline budgets.  Therefore a certificate at the
limit automatically covers **every finite exponent** on that distinguished
prime.

M48 verifies three such limits exactly.

## 1. `a=3`, special prime 5 at `x_5=1/4`

Take non-special primes `(7,11,13,17)` and use the M40 first/second factorial
penalties.  The six selected normalized variables run over four levels and the
other nine are at endpoints:

\[
4^6 2^9=2,097,152
\]

states.

With

\[
C=3219/10000,
\]

the exact downward-rounded integer minimum is

\[
\boxed{321972889801}>321900000000,
\]

leaving slack `72,889,801`.  The exact value at the minimizing state is

\[
\frac{2237914997425511686938229122037}
{6950631771340631703208880000000}>C.
\]

The resulting quantitative summed-rho margin is

\[
\boxed{
\eta_{3,5^\infty}
=
\frac{7030993631127}{20684163500000}>0.
}
\]

The complete non-special factor-4 box is in the Clique--Shearer region; its
previously audited endpoint minimum is `941/17017>0`.  Hence M39 converts this
rho margin into genuine uncovered mass.

Consequently the same certificate works for

\[
3^3\cdot5^b\cdot7\cdot11\cdot13\cdot P
\]

for every finite `b`, at the reference simple baseline and all coordinatewise
smaller simple baselines.

## 2. `a=5`, special prime 5 at `x_5=1/4`

Use the M44 goodness certificate with non-special primes `(7,11,13,17)`.
The exact reduced state count is

\[
6^6 2^9=23,887,872.
\]

At the infinite special baseline the rigorous integer minimum is

\[
\boxed{330004947384}>329990000000,
\]

and the exact minimizing value is

\[
\frac{3204402373366585023349981183247200703}
{9710164646566517961385166328720000000}>32999/100000.
\]

After subtracting the exact special and factorial budgets,

\[
\boxed{
\eta_{5,5^\infty}
=
\frac{376679506003531}{289578289000000}>0.
}
\]

Thus the staged `a=5` certificate survives **arbitrarily large powers of 5** on
the special coordinate.

## 3. `a=5`, special prime 7 at `x_7=1/6`

Now use M36's non-special system `(5,11,13,17)` and send the distinguished
prime-7 exponent to infinity.  The same 23,887,872-state exact verification
gives

\[
\boxed{293118223450}>292900000000.
\]

The exact minimizing value is

\[
\frac{4197539859160637669}{14320296464760000000}>2929/10000,
\]

and the summed-goodness margin is

\[
\boxed{
\eta_{5,7^\infty}
=
\frac{92070538867211}{53187849000000}>0.
}
\]

Therefore the same staged geometry works for every finite power of the
special prime 7.

The exact verifier is `solver/m48_special_coordinate_limits.py`.  These limit
certificates are used immediately in M49 to close the full
`(5,3,1,1,1,1)` exponent profile.
