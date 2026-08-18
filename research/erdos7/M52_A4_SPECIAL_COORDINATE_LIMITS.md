# Milestone 52 — the missing `a=4` special-coordinate limits

M48 certifies infinite distinguished-prime baselines at stages `a=3` and
`a=5`.  M52 fills the remaining `a=4` layer needed to treat two repeated prime
coordinates with arbitrary exponents.

## Prime 5 sent to infinity

Stage on `3^4` and use non-special primes `(7,11,13,17)`.  Inflate every finite
power of the distinguished prime 5 to

\[
x_5(\infty)=1/4.
\]

Use the stronger M44 goodness penalties, but now with five activation levels.
The exact reduced state count is

\[
5^6 2^9=8,000,000.
\]

With `C=32999/100000`, the rigorous downward-rounded minimum is

\[
\boxed{330004947384}>329990000000.
\]

After the exact `a=4` first/second-moment and factorial costs are subtracted,

\[
\boxed{
\eta_{4,5^\infty}
=
\frac{204805547139351}{289578289000000}>0.
}
\]

Thus at stage `3^4` the distinguished prime 5 may have **any finite exponent**.

## Prime 7 sent to infinity

Now use non-special primes `(5,11,13,17)` and inflate the distinguished prime 7
to

\[
x_7(\infty)=1/6.
\]

The M33 asymmetric-goodness factorial coefficients remain valid at this limit.
The exact 8,000,000-state minimum is

\[
\boxed{303811982434}>300000000000,
\]

and the exact value at the minimizing state is

\[
\frac{811658073226246909231891}
{2671580188169160840000000}>3/10.
\]

The summed-goodness margin is

\[
\boxed{
\eta_{4,7^\infty}
=
\frac{31948860183767}{26593924500000}>0.
}
\]

Thus the distinguished prime 7 may likewise have arbitrary finite exponent.

Together with M48, we now possess prime-5 and prime-7 infinite special-coordinate
certificates at stages `a=4` and `a=5`, plus the prime-5 limit at `a=3`.  M53
uses exactly this package to eliminate **every six-prime profile with only two
repeated prime coordinates**.

The verifier is `solver/m52_a4_special_coordinate_limits.py`.
