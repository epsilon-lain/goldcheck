# Milestone 32 — repeated-support factorial moments close the symmetric `(4,4)` seed

The hardest symmetric M27 seed is

\[
N_0=3^4\cdot5^4\cdot7\cdot11\cdot13\cdot17=861485625.
\]

M29 and M31 showed that very large **distinct-variable** moment cones do not
close this seed while the prime-5 side is frozen to the M25 treatment.  M30
identified the missing structure: for every non-5 square-free support there is
only one exact divisor of

\[
M=5^4\cdot7\cdot11\cdot13\cdot17
\]
with that support after the prime-5 coordinate is separated.  Hence its
normalized 3-adic fibre charge is an integer activation count rather than an
arbitrary point of the factor-5 box.

M32 exploits precisely that repeated-support information and gives an exact
finite certificate that

\[
\boxed{861485625\text{ is noncovering}.}
\]

As throughout the project, this is an internal rigorous theorem candidate
pending independent full-suite and literature/novelty review.  It is not a
solution of the complete odd distinct covering-system problem.

## 1. Integer activation variables

Stage modulo `81` and choose 41 fibres surviving the pure
`3,9,27,81` classes.  For a non-5 support `S`, there is one exact divisor
`m` with `sqf(m)=S`, and

\[
q_S(r)=b_S(1+A_S(r)),\qquad A_S(r)\in\{0,1,2,3,4\}.
\]

Equivalently

\[
z_S(r):=q_S(r)/b_S\in\{1,2,3,4,5\}.
\]

M30 gives the exact factorial caps

\[
\sum_r A_S(r)\le40,
\qquad
\sum_r {A_S(r)\choose2}\le18.
\]

M32 uses these two constraints for the six supports

\[
\boxed{
\{7\},\{11\},\{13\},\{17\},\{7,11\},\{7,13\}.
}
\]

## 2. Pointwise factorial certificate

Keep the sixteen supports containing prime `5` exactly as in the frozen M25
quadratic completion used by M29.  For each of the six displayed non-5
supports add

\[
\alpha_S A_S+\beta_S{A_S\choose2},
\qquad \alpha_S,\beta_S\ge0.
\]

In the support order above, with common denominator `10^6`, the coefficient
numerator pairs `(alpha,beta)` are

```text
{7}:     (27687,14172)
{11}:    (14737, 4884)
{13}:    (12743, 2484)
{17}:    ( 9775, 1333)
{7,11}:  ( 3191, 2315)
{7,13}:  ( 3924,  838)
```

The other nine non-5 variables receive no new penalty.  After minimizing the
sixteen prime-5 variables as clipped convex quadratics, the resulting base
function is separately concave in every non-5 coordinate.  Thus the nine
unpenalized coordinates attain their minimum at endpoints `1` or `5`, while
the six penalized coordinates must be checked at their five genuine integer
values.  The complete state space therefore has

\[
5^6 2^9=\boxed{8,000,000}
\]

states.

Take

\[
C=\frac{79437}{250000}=0.317748.
\]

The verifier uses no floating-point acceptance test.  It first evaluates every
clipped quadratic lookup exactly with `Fraction`, multiplies by
`Q=10^{12}`, and rounds **down**.  The exhaustive state loop then uses only
integer arithmetic, so the reported minimum is a rigorous lower bound for the
true pointwise expression.  Its exact scaled minimum is

\[
\boxed{317748994349},
\]

whereas

\[
QC=317748000000.
\]

Hence the integer certificate has positive slack

\[
\boxed{994349}.
\]

The minimizing state is also reevaluated directly with rational arithmetic;
its exact value is

\[
\frac{3274623664211662201315187}
{10305693243258381718750000}>C.
\]

## 3. Summed margin

The six factorial penalties cost at most

\[
40\sum_S\alpha_S+18\sum_S\beta_S
=\frac{837687}{250000}.
\]

The frozen prime-5 first/second-moment cost is

\[
K_5=\frac{807151395889143}{83666064453125}.
\]

Summing the pointwise inequality over 41 fibres therefore gives

\[
\sum_r\rho(q(r))
\ge
41C-K_5-rac{837687}{250000}
=
\boxed{
\frac{19827332308731}{669328515625000}
}>0.
\]

Thus at least one selected fibre has positive full Clique-Shearer polynomial.

## 4. Completion audit

The non-5 coordinate polynomials have exact box extrema

\[
\min_{C\subsetneq J}\rho_C=\frac1{91}>0,
\qquad
\min\rho_J=-\frac{258}{17017}.
\]

The same factor-5 bad-branch argument used in M25 is rechecked for the new
`5^4` baseline.  Its exact box maximum is

\[
\boxed{-\frac{1062}{125125}<0.}
\]

so positive full `rho` forces the non-5 subsystem into the Clique-Shearer
region, and the relative one-coordinate completion argument leaves a genuinely
uncovered point in that fibre.

Therefore `N_0` cannot be the LCM of a saturated distinct divisor-modulus
cover, and hence cannot support any distinct covering system.

## 5. Frontier consequence

M27 had reduced the entire six-prime profile `(4,4,1,1,1,1)` to two seeds.
M32 removes the symmetric one.  The only M27 seed still open in this profile is

\[
\boxed{
2363916555=3^4\cdot5\cdot7^4\cdot11\cdot13\cdot17.
}
\]

The next attack should exploit the asymmetry of that seed rather than treating
it as another `5^4` instance.

Exact verifier:

```text
cd research/erdos7/solver
python -m pytest -q test_m32_factorial_seed.py
```
