# Milestone 63 — `(3,2,2,2,2,2)` reduces to one hard seed

For the new M62 frontier profile

\[
(3,2,2,2,2,2),
\]

the direct McNew–Setty placement scan at the minimal odd primes leaves only two placements:

- canonical `(3,2,2,2,2,2)`;
- swapped `(2,3,2,2,2,2)`.

The other four placements already have `R<1` at `(3,5,7,11,13,17)`.

The swapped absolute-minimal tuple has a positive exact `a=2` M25-tensor certificate, with summed margin

\[
\frac{10396620060393879335269823900407176231}
{73275880480165539499715127335600000000}>0.
\]

Every nonminimal swapped tuple dominates `(3,5,7,11,13,19)`, where the direct bound is already

\[
\frac{406203011801}{406937656125}<1.
\]

For the canonical placement, the reference tuple `(3,5,7,11,13,19)` has an exact positive `a=3` M25-tensor margin

\[
\frac{66138381986300034053279312820363673862719}
{4821363964703496265315619830881898488000000}>0.
\]

The M27 coordinatewise scaling argument transports that certificate to every larger prime tuple with the same exponent placement.  Therefore the only unresolved member of the complete profile is

\[
\boxed{
3^3\cdot5^2\cdot7^2\cdot11^2\cdot13^2\cdot17^2
=195465345075.
}
\]

The exact verifier is `solver/m63_p322222_one_seed_reduction.py`, with regression checks in `solver/test_m63_p322222_one_seed_reduction.py`.
