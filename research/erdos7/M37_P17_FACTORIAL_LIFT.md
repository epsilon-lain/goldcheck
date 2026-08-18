# Milestone 37 — factorial mass closes the last canonical `(5,2,1,1,1,1)` seed

M35 quantitatively lifts five of the six canonical seeds in the M26
`(5,2,1,1,1,1)` branch.  The only canonical survivor was

\[
\boxed{
N_5=3^5\cdot5^2\cdot7\cdot11\cdot13\cdot17.
}
\]

The old M16 and M25 `a=4` summed-rho margins are positive but too small to
survive one more application of the deficiency recurrence.  M37 adds the
single-divisor factorial information from M30 to the `a=4` precursor and gets a
large enough **quantitative** margin.

The result is

\[
\boxed{N_5\text{ is noncovering}.}
\]

Together with M35 and M36 this removes all seven M26 seeds of profile
`(5,2,1,1,1,1)`.

## 1. Strengthen the a=4 precursor

Set

\[
N_4=3^4\cdot5^2\cdot7\cdot11\cdot13\cdot17,
\qquad
M=5^2\cdot7\cdot11\cdot13\cdot17.
\]

Stage modulo `81` and select 41 surviving fibres.  Distinguish the prime-5
coordinate.  The remaining four coordinates `7,11,13,17` are simple, so each
of their fifteen nonempty supports has one exact divisor and

\[
z_S=q_S/b_S=1+A_S\in\{1,2,3,4,5\}.
\]

M30 gives

\[
\sum_r A_S\le40,
\qquad
\sum_r{A_S\choose2}\le18.
\]

## 2. Exact factorial pointwise certificate

Keep the nonnegative M25 linear and diagonal penalties on the sixteen supports
containing prime `5`.  Add first/second factorial penalties to

\[
\{7\},\{11\},\{13\},\{17\},\{7,11\},\{7,13\}.
\]

With common denominator `10^6`, the coefficient numerator pairs are

```text
{7}:     (28506,13846)
{11}:    (15147, 4601)
{13}:    (11878, 3468)
{17}:    ( 9885, 1278)
{7,11}:  ( 4026, 1511)
{7,13}:  ( 2880, 1481)
```

The selected variables range over all five integral levels; the other nine are
at endpoints by separate concavity.  Thus the exact reduced state space has

\[
5^6 2^9=8,000,000
\]

states.

Take

\[
C=\frac{3971}{12500}=0.31768.
\]

Every clipped quadratic lookup entry is evaluated as a `Fraction`, multiplied
by `Q=10^12`, and rounded downward before the exhaustive integer loop.  The
rigorous lower minimum is

\[
\boxed{317680825425}
\]

against

\[
QC=317680000000,
\]

so the integer slack is

\[
\boxed{825425>0}.
\]

The minimizing state is

```text
(5,1,4,1,4,5,5,1,5,5,5,5,5,5,5)
```

and its independent exact value is

\[
\frac{268054818379928913}{843786583640000000}
>\frac{3971}{12500}.
\]

## 3. Quantitative rho margin

The special-coordinate first/second-moment cost is

\[
K_5=
\frac{409948781722209}{45246607656250},
\]

while the six factorial penalties cost

\[
40\sum\alpha_S+18\sum\beta_S
=\frac{336421}{100000}.
\]

Therefore the certificate proves

\[
\sum_r\rho(q(r))
\ge
41C-K_5-\frac{336421}{100000}
=
\boxed{
\frac{434620215428731}{723945722500000}
}.
\]

This is about `0.600349`, substantially stronger than the old M25 margin.

The M16 completion audit for the same factor-5 non-special box is reused
unchanged: all proper coordinate polynomials are positive, and the bad branch
has strictly negative completion upper bound.  Hence whenever `rho>0`, the
actual uncovered proportion is at least `rho`.  Thus

\[
\delta(N_4)
\ge
M\frac{434620215428731}{723945722500000}.
\]

## 4. Lift to exponent five

Here

\[
\frac{\sigma(M)}M=\frac{107136}{60775}.
\]

The deficiency recurrence gives

\[
\delta(N_5)
\ge3\delta(N_4)-\sigma(M).
\]

After dividing the lower bound by `M`, the exact gap is

\[
3\frac{434620215428731}{723945722500000}
-
\frac{107136}{60775}
=
\boxed{
\frac{27667327886193}{723945722500000}
}>0.
\]

Therefore

\[
\boxed{
3^5\cdot5^2\cdot7\cdot11\cdot13\cdot17
\text{ is noncovering}.}
\]

The exact verifier is `solver/m37_p17_factorial_lift.py`, with regression tests
in `solver/test_m37_p17_factorial_lift.py`.
