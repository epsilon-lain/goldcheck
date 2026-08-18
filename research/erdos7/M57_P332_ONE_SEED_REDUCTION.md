# Milestone 57 — `(3,3,2,1,1,1)` reduces to one explicit seed

M56 leaves the profile

\[
(3,3,2,1,1,1)
\]

as one of the three minimal six-prime exponent directions.  M57 proves that
every member of this profile is noncovering **except possibly one integer**:

\[
\boxed{
N_*=3^3\cdot5^3\cdot7^2\cdot11\cdot13\cdot17.
}
\]

This is a reduction, not yet a closure of the profile.

## 1. Placement reduction

At the minimal odd primes `(3,5,7,11,13,17)` there are 60 exponent placements.
The direct McNew–Setty bound leaves only eight:

```text
(3,2,1,1,1,3)
(3,2,1,1,3,1)
(3,2,1,3,1,1)
(3,2,3,1,1,1)
(3,3,1,1,1,2)
(3,3,1,1,2,1)
(3,3,1,2,1,1)
(3,3,2,1,1,1)
```

The other 52 placements are universally excluded by M22 monotonicity.  If the
smallest prime is greater than `3`, the common anchor
`(5,7,11,13,17,19)` has `R<1` for all eight survivors.

## 2. Seven noncanonical placements disappear by scaled certificates

For each of the first seven placements, stage on `3^3` at the minimal prime
tuple and reuse the nonnegative M25 linear/diagonal/cross penalty tensor with
M28's `a=3` budgets

\[
\sum q_S\le27b_S,
\qquad
\sum q_Sq_T\le63b_Sb_T.
\]

The exact `2^15` endpoint certificate has positive summed-rho margin in every
case, and the non-special Clique–Shearer coordinate polynomials stay strictly
positive.  M27 supportwise scaling therefore propagates each reference
certificate to every coordinatewise larger prime tuple with the same exponent
placement.

## 3. The canonical placement has a positive tail reference

For

\[
(3,3,2,1,1,1)
\]

the minimal reference `(3,5,7,11,13,17)` is the unique obstruction to this
particular M25-tensor argument: its summed margin is negative.  But moving only
the final prime from `17` to `19` makes the same exact certificate positive.
At

\[
(3,5,7,11,13,19)
\]

the exact margin is

\[
\boxed{
\frac{217161974733034408394686802579413972423}
{6014114230851370315789292968793000000000}>0.
}
\]

Its non-special coordinate minima are

\[
\min_{C\subsetneq J}\rho_C=\frac{459}{7007}>0,
\qquad
\min\rho_J=\frac{17}{637}>0.
\]

Every increasing odd-prime tuple beginning with `3` other than the absolute
minimal tuple is coordinatewise at least `(3,5,7,11,13,19)`.  Hence M27 scaling
kills the entire canonical tail.

What remains is exactly

\[
\boxed{3^3\cdot5^3\cdot7^2\cdot11\cdot13\cdot17}.
\]

The exact verifier is `solver/m57_p332_one_seed_reduction.py`; regression checks
are in `solver/test_m57_p332_one_seed_reduction.py`.
