# Milestone 50 — every `(A,3,1,1,1,1)` profile with `A>=6` is excluded

M49 closes `(5,3,1,1,1,1)`.  M50 goes further and removes the entire next
large-exponent ray

\[
\boxed{(A,3,1,1,1,1),\qquad A\ge6.}
\]

The proof combines an infinite-exponent McNew--Setty reduction with the three
special-coordinate limit certificates from M48.

## 1. Only three placements survive when `A` is sent to infinity

Replace the large-coordinate charge by

\[
x_p(\infty)=\frac1{p-1}.
\]

At the minimal odd primes `(3,5,7,11,13,17)`, all 30 placements of the large
exponent and the cube can be checked exactly.  Only

\[
(A,3,1,1,1,1),\qquad
(A,1,3,1,1,1),\qquad
(3,A,1,1,1,1)
\]

survive.  In coordinate-position notation these are `(0,1)`, `(0,2)`, and
`(1,0)`, with exact limit bounds

\[
\frac{333}{325},\qquad
\frac{4190826}{4169165},\qquad
\frac{54619}{54054}.
\]

The largest of the other 27 placements is

\[
\boxed{931068/935935<1}.
\]

Exact monotone boundary anchors reduce the three surviving placements to 22
prime-tuple templates in total: 17 for `(0,1)`, two for `(0,2)`, and three for
`(1,0)`.

## 2. Cube on 3, large exponent on 5

For placement `(1,0)`, stage directly on `3^3`.  M48's `a=3` prime-5 limit
certificate already allows **any finite exponent** on the distinguished prime
5 and gives

\[
\eta=\frac{7030993631127}{20684163500000}>0.
\]

Thus all three direct-survivor templates in this placement are excluded
without any lifting step.

## 3. Large exponent on 3, cube on 5

M48's `a=5` infinite-prime-5 certificate gives the precursor margin

\[
\eta_{5,5^\infty}
=\frac{376679506003531}{289578289000000}.
\]

For the actual cube `5^3` and reference simple tuple `(7,11,13,17)`,

\[
\frac{\sigma(M)}M=\frac{41472}{23375}.
\]

The first lift to exponent six has normalized gap

\[
\boxed{
g_6=
\frac{616267788538593}{289578289000000}>0.
}
\]

Moreover `g_6 > (sigma(M)/M)/2`.  Therefore the recurrence

\[
g_{a+1}\ge3g_a-\frac{\sigma(M)}M
\]

is increasing, and every exponent `A>=6` remains positive.  The same reference
bound applies to all 17 prime-tuple templates by coordinatewise baseline
inflation.

## 4. Large exponent on 3, cube on 7

Use M48's `a=5` prime-7 limit certificate.  With the actual cube `7^3`,

\[
\frac{\sigma(M)}M=\frac{207360}{119119},
\]

and the first lifted normalized gap is

\[
\boxed{
g_6=
\frac{2999179924493339}{868734867000000}>0.
}
\]

Again `g_6>s/2`, so recurrence propagates forever.  This removes the two
remaining direct-survivor templates.

Hence every direct-survivor template is noncovering for every finite `A>=6`,
while every other prime tuple or exponent placement is already excluded by the
infinite-exponent direct bound.

The verifier is `solver/m50_infinite_pA3_ray.py`.
