# Milestone 33 — the asymmetric seed closes the full `(4,4,1,1,1,1)` profile

M27 reduced the complete six-prime exponent profile

\[
(4,4,1,1,1,1)
\]

to two explicit seeds.  M32 excludes the symmetric one

\[
3^4\cdot5^4\cdot7\cdot11\cdot13\cdot17.
\]

M33 excludes the remaining asymmetric seed

\[
\boxed{
N_1=3^4\cdot5\cdot7^4\cdot11\cdot13\cdot17
=2363916555.
}
\]

Consequently, subject to the standing independent-audit caveat, the entire
profile is now excluded:

\[
\boxed{
\{a_1,\ldots,a_6\}=\{4,4,1,1,1,1\}
\Longrightarrow
\prod_{i=1}^6 p_i^{a_i}\text{ is noncovering}.
}
\]

This is still a partial theorem toward Erdős Problem #7, not a resolution of
the full odd distinct covering-system problem.

## 1. Why the asymmetric seed needs a different completion coordinate

Continue to stage on the `3^4=81` coordinate, so 41 3-adic fibres survive.
For M32 the prime `5` was the distinguished Clique-Shearer completion
coordinate.  That is poorly matched to `N_1`, because now the repeated
post-stage coordinate is `7^4`.

M33 instead distinguishes the prime `7`.  The other four coordinates are then
exactly

\[
5,11,13,17,
\]

all to exponent one.  Hence every nonempty square-free support among those four
coordinates corresponds to a unique exact divisor, and its normalized charge
is an integer

\[
z_S=1+A_S\in\{1,2,3,4,5\}.
\]

The M30 factorial budgets

\[
\sum_r A_S\le40,
\qquad
\sum_r {A_S\choose2}\le18
\]

are therefore available on all fifteen non-special supports.

## 2. A goodness functional instead of a fragile implication audit

The non-special factor-5 box for `(5,11,13,17)` is not uniformly inside the
Clique-Shearer region, so merely proving the full five-coordinate polynomial
positive is not by itself the right target.

M33 uses the stronger pointwise quantity

\[
g(q)=\min\left(
\rho_{\mathrm{full}}(q),
\{\rho_C(q^0):\varnothing\ne C\subseteq\{5,11,13,17\}\}
\right),
\]

where `q^0` denotes the fifteen non-special support charges.

If `g(q)>0`, then every non-special coordinate polynomial is positive and the
full five-coordinate polynomial is positive.  Thus the non-special subsystem
lies in the Clique-Shearer region and the M14 relative one-coordinate
completion argument with distinguished prime `7` yields a genuinely uncovered
point.

This avoids having to infer Shearer-region membership from positivity of only
one polynomial.

## 3. Exact reduction after the frozen special penalties

Use the same nonnegative M25 linear/diagonal penalties on the sixteen supports
containing the distinguished coordinate.  For fixed `q^0`, minimizing

\[
g(q)+P_{\mathrm{special}}(q)
\]

over the sixteen special charges is exact.

- On the `rho_full` branch, the sixteen variables minimize independently as the
  usual clipped convex quadratics, giving `B(q^0)`.
- On a coordinate branch `rho_C(q^0)`, the coordinate polynomial is independent
  of the special variables and the nonnegative special penalty is minimized at
  all lower endpoints.  Its exact minimum is

\[
P_0=
\frac{45778312503188}{851714903064025}.
\]

Hence the reduced base is

\[
G(q^0)=\min\left(
B(q^0),
P_0+\rho_C(q^0)\ (\varnothing\ne C\subseteq J)
\right).
\]

Each branch is separately concave in every non-special variable, so `G`, as a
minimum of separately concave functions, is separately concave as well.

## 4. Six repeated-support factorial penalties

M33 uses the six supports

\[
\boxed{
\{5\},\{11\},\{13\},\{17\},\{5,11\},\{5,13\}.
}
\]

For each selected support it adds

\[
\alpha_S A_S+\beta_S{A_S\choose2}.
\]

With common denominator `10^6`, the coefficient numerator pairs are

```text
{5}:     (54506,31667)
{11}:    (15997, 4353)
{13}:    (13268, 2571)
{17}:    (10495, 1509)
{5,11}:  ( 8673, 1858)
{5,13}:  ( 6719, 3325)
```

The selected six variables are checked at all five integer values; the other
nine have no new penalty and therefore minimize at endpoints by separate
concavity.  Again the complete finite state space is

\[
5^6 2^9=\boxed{8,000,000}.
\]

Take

\[
C=\frac3{10}.
\]

The verifier builds every clipped-quadratic and coordinate-branch lookup with
exact `Fraction` arithmetic, scales by `Q=10^{12}`, rounds downward, and then
runs the eight-million-state check with integers only.  It obtains the rigorous
scaled lower bound

\[
\boxed{303809359581}
\]

against

\[
QC=300000000000,
\]

leaving pointwise integer slack

\[
\boxed{3809359581}.
\]

The reported minimizing state is independently evaluated exactly; the true
value there is

\[
\frac{2639033771723344936606712407}
{8686479492576292487080000000}
>\frac3{10}.
\]

## 5. Positive summed goodness

The special first/second-moment penalty costs

\[
K_7=
\frac{5019735697491668}{851714903064025},
\]

and the six factorial penalties cost

\[
40\sum\alpha_S+18\sum\beta_S
=\frac{2600707}{500000}.
\]

Therefore

\[
\sum_{r=1}^{41}g(q(r))
\ge
41\frac3{10}-K_7-\frac{2600707}{500000}
\]

and the exact margin is

\[
\boxed{
\frac{20524715787799539373}
{17034298061280500000}
}>0.
\]

Thus some surviving 3-adic fibre has `g(q(r))>0`.  On that same fibre the
non-special subsystem is in the Clique-Shearer region and the full polynomial
is positive, so the relative completion argument produces an uncovered
integer.  Hence `N_1` is noncovering.

## 6. Consequence

M27 killed nine of the eleven minimal `(4,4,1,1,1,1)` seeds.  M32 kills the
symmetric tenth and M33 kills the asymmetric eleventh.  Therefore no member of
this exponent profile can be a covering LCM.

The minimal six-prime frontier after M33 is now pushed away from `(4,4,1,1,1,1)`;
the remaining M26 antichain directions are `(5,2,1,1,1,1)` and
`(3,2,2,1,1,1)` (subject to recomputing the down-set frontier after incorporating
this new closed profile).

Exact verifier:

```text
cd research/erdos7/solver
python -m pytest -q test_m33_goodness_factorial_seed.py
```
