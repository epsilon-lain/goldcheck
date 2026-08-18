# Milestone 35 — quantitative Clique–Shearer margins lift five `3^5 5^2` seeds

M34 leaves two minimal six-prime exponent profiles.  This milestone attacks the
seven-seed branch

\[
(5,2,1,1,1,1).
\]

The key observation is that the older `a=4` Clique–Shearer certificates contain
strictly more information than was previously used.  They do not merely prove
that some fibre is uncovered: their **summed rho margin is a quantitative lower
bound for the uncovered mass**.  Feeding that bound into the deficiency
recurrence lifts five canonical `a=4` certificates to `a=5`.

This milestone reduces the six canonical seeds in this profile to one.  The
seventh M26 seed has the square on prime `7` rather than prime `5` and is left
for a separate direct `a=5` factorial-goodness certificate.

## 1. Quantitative form of the staged certificate

Let

\[
N_4=3^4M,
\]

and select 41 fibres modulo `81` surviving the pure `3,9,27,81` classes.  In
M16/M25 the pointwise proof supplies the support-intersection polynomial
`rho(q(r))` and an exact completion audit with the following property:

- if `rho(q(r))>0`, the actual uncovered proportion inside that fibre is at
  least `rho(q(r))`;
- if `rho(q(r))<=0`, the uncovered proportion is of course at least zero and
  hence still at least `rho(q(r))`.

Consequently, if the global certificate proves

\[
\sum_r \rho(q(r))\ge \eta>0,
\]

then the number of uncovered residues modulo `N_4` satisfies

\[
\boxed{\delta(N_4)\ge M\eta.}
\]

This is the quantitative information that the earlier qualitative use of M16
and M25 discarded.

## 2. Lift from `3^4` to `3^5`

For `N_5=3^5M`, the deficiency recurrence gives

\[
\delta(N_5)\ge 3\delta(N_4)-\sigma(M).
\]

Hence the staged margin proves `N_5` noncovering whenever

\[
\boxed{
3\eta>\frac{\sigma(M)}M.
}
\]

For the canonical profile branch

\[
M=5^2pqrs
\]

with four simple odd primes `p,q,r,s`,

\[
\frac{\sigma(M)}M
=\frac{31}{25}\prod_{u\in\{p,q,r,s\}}\frac{u+1}{u}.
\]

Everything below is checked with exact rational arithmetic.

## 3. Four lifts from the M16 diagonal certificate

The M16 coefficient vector was originally recorded only for tails
`17,19,23`.  The same exact `2^15` endpoint verifier remains valid for two
further direct-bound frontier tails and for the off-tail simple-prime tuple.

The four quantitative margins used here are

\[
\begin{array}{c|c}
(p,q,r,s)&\eta\\ \hline
(7,11,13,23)&49732740695329/83861791406250\\
(7,11,13,29)&34454129718207371/42463315034765625\\
(7,11,13,31)&83924772650351557/97044579663281250\\
(7,11,17,19)&63881523541951/76303450781250.
\end{array}
\]

The corresponding normalized lift gaps

\[
3\eta-\sigma(M)/M
\]

are respectively

\[
\frac{89914207333}{2150302343750},
\quad
\frac{10075865808207371}{14154438344921875},
\quad
\frac{28331122538351557}{32348193221093750},
\quad
\frac{20056203541951}{25434483593750},
\]

all strictly positive.

Thus the canonical seeds with last prime `23,29,31`, and the tuple
`(7,11,17,19)`, lift immediately to noncoverage at exponent `3^5`.

## 4. The p=19 seed needs the stronger M25 certificate

The older M16 margin at tail `19` is not large enough for this recurrence.
However, the M25 cross-support second-moment certificate, evaluated at

\[
(7,11,13,19),
\]

has the exact summed margin

\[
\eta_{19}
=
\frac{3231212534728550154455103}
{4930518875613871540000000}.
\]

Its normalized lift gap is

\[
\boxed{
\frac{1052798929867280671365309}
{4930518875613871540000000}>0.
}
\]

So this fifth canonical seed is also noncovering at exponent `3^5`.

## 5. What remains in the `(5,2,1,1,1,1)` branch

M26 had six canonical seeds with the fifth power on `3` and the square on `5`.
M35 eliminates five of them.  The only canonical survivor is

\[
\boxed{
3^5\cdot5^2\cdot7\cdot11\cdot13\cdot17.
}
\]

There is also the exceptional M26 placement

\[
3^5\cdot5\cdot7^2\cdot11\cdot13\cdot17,
\]

which is not covered by this lifting argument because its repeated post-stage
coordinate is different.  It is the natural target for an `a=5` analogue of
the M33 factorial-goodness certificate.

Thus M35 reduces the seven direct-bound seeds of the profile to **two** before
that separate attack.

## 6. Verification

The exact verifier is

`solver/m35_quantitative_lifting.py`

with regression tests in

`solver/test_m35_quantitative_lifting.py`.

It recomputes every `2^15` pointwise minimum with `Fraction`, rechecks the
Shearer-completion sign conditions, recomputes all global penalty costs, and
then verifies each recurrence gap exactly.

As usual this is a six-prime partial theorem, not a resolution of the full odd
distinct covering-system problem.
