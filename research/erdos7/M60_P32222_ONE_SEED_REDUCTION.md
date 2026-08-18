# Milestone 60 — `(3,2,2,2,2,1)` reduces to one explicit seed

For the M59 frontier profile

\[
(3,2,2,2,2,1),
\]

M60 proves that every member is noncovering except possibly

\[
\boxed{
3^3\cdot5^2\cdot7^2\cdot11^2\cdot13^2\cdot17
=11497961475.
}
\]

At the minimal odd primes, only five of the 30 exponent placements survive the
direct McNew–Setty bound.  Three noncanonical placements with exponent `3` on
prime `3` have positive exact `a=3` M25-tensor certificates at the minimal
reference and therefore scale to their full prime families.  The placement
with exponent `3` on prime `5` is already excluded at the absolute minimal
tuple by an exact `a=2` certificate; its nonminimal prime tail has direct
`R<1`.  Finally, the canonical placement `(3,2,2,2,2,1)` has a positive exact
reference certificate at `(3,5,7,11,13,19)`, so its entire tail scales from
that point.

The only canonical tuple below that tail reference is the absolute minimal one,
which is the displayed hard seed.

The exact verifier is `solver/m60_p32222_one_seed_reduction.py`; regression
checks are in `solver/test_m60_p32222_one_seed_reduction.py`.
