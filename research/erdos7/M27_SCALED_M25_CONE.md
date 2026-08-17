# Milestone 27 — one scaled M25 certificate removes 9 of the 11 `(4,4,1,1,1,1)` seeds

M26 reduced the complete six-prime exponent profile

\[
(4,4,1,1,1,1)
\]

to eleven direct-bound seeds.  M27 reuses the M25 cross-support second-moment
certificate, but adds a supportwise scaling observation that turns one exact
reference computation into a whole monotone cone of exclusions.

The result is that nine of those eleven seeds are noncovering.  Only

\[
\boxed{861485625=3^4\cdot5^4\cdot7\cdot11\cdot13\cdot17}
\]

and

\[
\boxed{2363916555=3^4\cdot5\cdot7^4\cdot11\cdot13\cdot17}
\]

remain from this profile.

This is an internal rigorous frontier reduction pending independent full-suite
execution and literature review; it does not assert that either remaining seed
covers.

## 1. Exact reference certificate

Stage modulo `81` as in M15–M25.  For the post-3 coordinates take the reference
charge vector

\[
\bar x=
\left(\frac{156}{625},\frac17,\frac1{11},\frac1{13},\frac1{19}\right).
\]

The first coordinate is the full `5^4` charge

\[
\frac15+\frac1{25}+\frac1{125}+\frac1{625}=\frac{156}{625}.
\]

For every nonempty support `S`, put

\[
\bar b_S=\prod_{i\in S}\bar x_i.
\]

Use exactly the nonnegative M25 coefficients `lambda_S`, the 16 diagonal
coefficients `nu_S` on supports containing the first coordinate, and the 46
cross-support coefficients `mu_{S,T}` among the other 15 supports.  On the
factor-5 box

\[
\bar b_S\le q_S\le5\bar b_S
\]

the exact `2^15` corner / clipped-quadratic verifier gives

\[
C=
\frac{46195504828341741529478638060857243}
{113607824903921989436397505904000000}.
\]

After the M15 budgets

\[
\sum_rq_S(r)\le81\bar b_S,
\qquad
\sum_rq_S(r)q_T(r)\le197\bar b_S\bar b_T,
\]

the summed margin is

\[
\boxed{
\frac{41149879073842994613795978360877402927}
{355024452824756216988742205950000000000}>0.
}
\]

The completion audit is also strict:

\[
\min_{C\subsetneq J}\rho_C=\frac1{91}>0,
\qquad
\max(\text{bad completion branch})
=-\frac{118016}{11886875}<0.
\]

So the reference baseline is noncovering by exactly the same M25 logic.

## 2. Supportwise scaling lemma

Now let an actual post-stage coordinate vector be

\[
x=(x_1,\ldots,x_5)
\]

with

\[
x_i\le\bar x_i\quad\text{for every }i.
\]

Write

\[
b_S=\prod_{i\in S}x_i,
\qquad
\gamma_S=\frac{\bar b_S}{b_S}\ge1.
\]

For the actual grouped fibre charges define

\[
\bar q_S(r)=\gamma_S q_S(r).
\]

Because `b_S <= q_S <= 5b_S`, we get exactly

\[
\bar b_S\le\bar q_S(r)\le5\bar b_S.
\]

The M15 budgets scale without loss:

\[
\sum_r\bar q_S(r)
=\gamma_S\sum_rq_S(r)
\le81\bar b_S,
\]

and for every pair

\[
\sum_r\bar q_S(r)\bar q_T(r)
=\gamma_S\gamma_T\sum_rq_S(r)q_T(r)
\le197\bar b_S\bar b_T.
\]

Finally `gamma_S>=1`, so

\[
q_S(r)\le\bar q_S(r).
\]

Thus the reference Clique-Shearer certificate proves noncoverage for a vector
that upper-bounds the actual event probabilities supportwise.  Hence every
coordinatewise smaller baseline is also noncovering.

This scaling step is useful because it transports both the first and the full
pair-moment data exactly; no fresh optimization is needed for each larger prime
tuple.

## 3. Nine M26 seeds disappear at once

The reference vector corresponds to the canonical simple-prime tuple

\[
(7,11,13,19).
\]

Therefore it dominates all seven canonical M26 seeds

\[
(7,11,13,P),
\qquad P\in\{19,23,29,31,37,41,43\},
\]

and also the two off-family seeds

\[
(7,11,17,19),\qquad(7,11,17,23).
\]

All nine are noncovering.

The canonical `P=17` baseline is not coordinatewise dominated because
`1/17>1/19`.  The exceptional placement with the fourth power on `7` is also
not dominated by the reference vector.  M27 therefore deliberately leaves
exactly the two numbers displayed at the start.

## 4. New frontier

M26 had 11 seeds for `(4,4,1,1,1,1)`.  M27 reduces this to

\[
\boxed{11\longrightarrow2}.
\]

The exact verifier is `solver/m27_scaled_m25_cone.py`; regression tests are in
`solver/test_m27_scaled_m25_cone.py`.

The next useful attacks are now sharply separated:

* the symmetric hard seed `3^4 5^4 7 11 13 17`, where the old M25 coefficients
  miss a positive summed margin;
* the exceptional placement `3^4 5 7^4 11 13 17`, where a different staging
  prime or a permuted/heavier-coordinate certificate is likely required.
