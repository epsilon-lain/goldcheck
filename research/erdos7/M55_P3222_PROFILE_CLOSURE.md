# Milestone 55 — the complete `(3,2,2,2,1,1)` profile is excluded

M54 left three minimal six-prime exponent directions.  M55 removes one of
them completely:

\[
\boxed{
\{a_1,\ldots,a_6\}=\{3,2,2,2,1,1\}
\Longrightarrow
\prod_{i=1}^6p_i^{a_i}\text{ is noncovering}.
}
\]

This remains a six-prime partial theorem, not a complete resolution of Erdős
Problem #7.

## 1. Only six exponent placements survive the direct bound

At the minimal odd primes

\[
(3,5,7,11,13,17),
\]

the profile has 60 distinct exponent placements.  Exact McNew–Setty evaluation
leaves only

```text
(3,2,1,1,2,2)
(3,2,1,2,1,2)
(3,2,1,2,2,1)
(3,2,2,1,1,2)
(3,2,2,1,2,1)
(3,2,2,2,1,1)
```

with `R>=1`.  The other 54 placements are universally excluded by the M22
coordinate monotonicity.

Every survivor has exponent `3` on prime `3` and exponent `2` on prime `5`.
If the smallest prime is not `3`, the common anchor

\[
(5,7,11,13,17,19)
\]

already has `R<1` for all six placements.  It therefore remains only to treat
prime tuples beginning with `3`.

## 2. Six exact `a=3` reference certificates

For each surviving placement, stage on `3^3`.  There are 14 selected surviving
fibres and M28 gives

\[
\sum_rq_S(r)\le27b_S,
\qquad
\sum_rq_S(r)q_T(r)\le63b_Sb_T.
\]

Reuse the nonnegative M25 penalty tensor: linear support penalties, diagonal
quadratics on the distinguished-coordinate supports, and selected non-special
cross terms.  The distinguished coordinate is the prime carrying exponent 2
in position two; at the reference tuple it is `5^2`, so

\[
x_5=\frac6{25},\qquad 4x_5=\frac{24}{25}<1.
\]

For fixed non-special charges, the sixteen distinguished-coordinate variables
minimize as clipped rational quadratics.  The remaining function is separately
concave, so each reference minimum is checked at exactly

\[
2^{15}=32768
\]

non-special corners using exact rational arithmetic.

All six summed-rho margins are positive.  The smallest is for the canonical
placement

\[
(3,2,2,2,1,1)
\]

and equals

\[
\boxed{
\frac{261660093197770847845124451200472947}
{5751405213735552946358906210088000000}
}>0.
\]

For that worst reference, the non-special Shearer-coordinate minima are also
strictly positive:

\[
\min_{C\subsetneq J}\rho_C=\frac{4177}{77077}>0,
\qquad
\min\rho_J=\frac{2655}{187187}>0.
\]

Thus M39 converts the positive rho margin into genuine uncovered mass.

## 3. One reference certificate covers every larger prime tuple

Let `x` be the five post-stage charge coordinates for an arbitrary increasing
prime tuple beginning with `3`, and let `xbar` be the corresponding minimal
reference coordinates.  Coordinate monotonicity gives `x<=xbar`.  For each
support set `S`, write the baseline products as `b_S` and `bbar_S`, and rescale

\[
\bar q_S=\frac{\bar b_S}{b_S}q_S.
\]

Then

\[
\bar b_S\le\bar q_S\le4\bar b_S,
\]

and the moment budgets transport exactly:

\[
\sum_r\bar q_S(r)\le27\bar b_S,
\qquad
\sum_r\bar q_S(r)\bar q_T(r)\le63\bar b_S\bar b_T.
\]

This is the same scaling mechanism isolated in M27.  The rescaled vector is a
valid larger upper-probability vector for the actual grouped events, so the
reference Clique–Shearer certificate applies unchanged.  Hence each of the six
reference certificates covers the entire coordinatewise larger prime family.

Combining the 54 direct-bound placements, the off-3 anchor, and the six scaled
certificates proves the complete profile theorem.

The exact verifier is `solver/m55_p3222_profile_closure.py`; regression checks
are in `solver/test_m55_p3222_profile_closure.py`.
