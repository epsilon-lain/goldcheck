# Milestone 40 — the complete `(3,2,2,1,1,1)` profile is excluded

M26 reduced the six-prime exponent profile

\[
(3,2,2,1,1,1)
\]

to twelve explicit McNew–Setty survivor seeds.  M40 excludes all twelve by a
single exact `a=3` Clique–Shearer certificate template.  Therefore

\[
\boxed{
\{a_1,\ldots,a_6\}=\{3,2,2,1,1,1\}
\Longrightarrow
\prod_{i=1}^6 p_i^{a_i}\text{ is noncovering}.
}
\]

This is a six-prime profile theorem inside the project, not a complete solution
of Erdős Problem #7.

## 1. Why the old M25 tensor unexpectedly works

Every M26 P322 seed has exponent `3` on prime `3`, exponent `2` on prime `5`,
and one further squared prime among the four post-stage coordinates.  Stage on
`3^3`.  The pure moduli `3,9,27` cover at most `13` residues modulo `27`, so we
may select

\[
\boxed{14}
\]

surviving 3-adic fibres.

For each square-free support `S`, let `b_S` be its exact divisor baseline and
`q_S(r)` its grouped charge in fibre `r`.  M28 gives the universal `a=3`
budgets

\[
\sum_r q_S(r)\le 27b_S,
\qquad
\sum_r q_S(r)q_T(r)\le63b_Sb_T.
\]

These bounds already allow repeated prime powers inside a support; no
squarefree-modulus assumption is being made.

Reuse the nonnegative M25 penalty tensor:

- linear terms on the support charges;
- diagonal quadratic terms on the sixteen supports containing the distinguished
  coordinate `5^2`;
- cross quadratic terms among selected non-5 supports.

Only the baseline and the moment constants change from M25.

## 2. Exact pointwise minimization

The distinguished coordinate has

\[
x_5=\frac15+\frac1{25}=\frac6{25}.
\]

Since `a=3`, every support charge lies in

\[
b_S\le q_S\le4b_S.
\]

Fix the fifteen non-5 variables.  The sixteen 5-containing variables then
occur as independent convex quadratics and are minimized exactly by clipping
the rational stationary point to `[b_S,4b_S]`.

After this elimination, the remaining function is separately concave in each
of the fifteen non-5 variables: the Clique–Shearer part is multi-affine, the
M25 cross terms are bilinear, and an infimum of affine functions of one
coordinate is concave.  Hence the global minimum is attained at a corner of the
non-5 box.  M40 checks all

\[
\boxed{2^{15}=32768}
\]

corners for each seed using exact `Fraction` arithmetic.

## 3. Quantitative margins

The summed lower bound for each seed is

\[
14C
-27\sum_S\lambda_Sb_S
-63\sum_S\mu_Sb_S^2
-63\sum_{S,T}\nu_{S,T}b_Sb_T.
\]

All twelve margins are strictly positive.  The smallest occurs at the minimal
canonical seed

\[
3^3\cdot5^2\cdot7^2\cdot11\cdot13\cdot17
\]

and equals

\[
\boxed{
\frac{435379245946298325768261464374075213}
{3089597842089346624077098377320000000}
}>0.
\]

Thus even the worst seed has substantial exact slack.

## 4. Completion audit is simpler than M25

The non-special four-coordinate Clique–Shearer vector stays inside the Shearer
region throughout every one of the twelve factor-4 boxes.  In the worst
canonical seed the exact minima are

\[
\min_{C\subsetneq J}\rho_C=\frac{459}{7007}>0,
\qquad
\min\rho_J=\frac{155}{7007}>0.
\]

Moreover the distinguished singleton satisfies

\[
q_{\{5\}}\le4\frac6{25}=\frac{24}{25}<1.
\]

Therefore the quantitative completion lemma audited in M39 applies directly:
for every selected fibre,

\[
\Pr(\text{uncovered})\ge\rho_{\rm full}(q).
\]

Summing over the fourteen fibres converts the positive exact certificate margin
into positive deficiency.

## 5. Profile closure

M26 proved that every member of the full `(3,2,2,1,1,1)` prime family is either
excluded by the direct McNew–Setty bound/monotone kill anchors or is one of its
twelve explicit seeds.  M40 verifies all twelve seeds, so the whole infinite
profile is excluded.

The exact verifier is `solver/m40_p322_profile_closure.py`, with regression
checks in `solver/test_m40_p322_profile_closure.py`.
