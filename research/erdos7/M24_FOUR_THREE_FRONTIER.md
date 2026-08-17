# Milestone 24 — reduce `(4,3,1,1,1,1)` to one remaining seed

This milestone attacks the next exponent profile after M23:

\[
\{4,3,1,1,1,1\}.
\]

It does **not** yet exclude the whole profile.  It proves that every odd six-prime member of this profile is noncovering except possibly

\[
\boxed{3^4\cdot5^3\cdot7\cdot11\cdot13\cdot17=172297125.}
\]

## 1. Only two exponent placements survive the direct bound

At the six smallest odd primes `(3,5,7,11,13,17)`, exact enumeration of all 30 placements of exponents `4` and `3` leaves only

\[
(4,3,1,1,1,1),\qquad(3,4,1,1,1,1)
\]

with direct bound at least one.  The largest of the other 28 placements is

\[
(4,1,3,1,1,1),
\]

with

\[
R=\frac{112558664}{112567455}
=1-\frac{8791}{112567455}<1.
\]

M22 gives the uniform derivative gap `719/1440>0`, so every larger prime tuple with one of those 28 placements is also directly excluded.

## 2. The swapped placement `3^3 5^4`

For

\[
3^3\cdot5^4\cdot7\cdot11\cdot13\cdot P,
\]

stage modulo `27` as in M14.  The only changed baseline is

\[
x_5=\frac15+\frac1{25}+\frac1{125}+\frac1{625}=\frac{156}{625}.
\]

A new exact factor-4 affine Clique–Shearer certificate gives positive 14-fibre margins

\[
P=17:\ \frac{12690063}{3038750000},\qquad
P=19:\ \frac{274867563}{6256250000},\qquad
P=23:\ \frac{227052153}{2213750000}.
\]

The direct tail is

\[
R(P)=\frac{5498761}{5630625}+\frac{1377221}{2413125P},
\]

whose real threshold is

\[
\frac{9640547}{395592}\approx24.37,
\]

so every prime `P>=29` is directly excluded.  Monotonicity also closes the off-family and off-base prime tuples.  Hence the entire swapped exponent placement is noncovering.

## 3. The hard placement `3^4 5^3`

For the canonical placement

\[
3^4\cdot5^3\cdot p q r s,
\]

direct monotonicity reduces the four simple primes to exactly seven direct-bound survivors:

\[
\begin{aligned}
&(7,11,13,17),(7,11,13,19),(7,11,13,23),\\
&(7,11,13,29),(7,11,13,31),(7,11,13,37),\\
&(7,11,17,19).
\end{aligned}
\]

The old M16 quadratic certificate, re-evaluated exactly with the new `5^3` baseline `31/125`, excludes

\[
(7,11,13,P),\quad P=23,29,31,37,
\]

and also `(7,11,17,19)`.  In every case the factor-5 completion audit remains strict.

The `P=19` case needs a stronger pointwise certificate.  M24 uses nonnegative diagonal quadratic penalties on all sixteen supports containing prime `5`:

\[
\rho(q)+\sum_S\lambda_S q_S+\sum_{5\in S}\mu_S q_S^2\ge C.
\]

Because the five-containing variables separate once the 15 non-5 support variables are fixed, the global box minimum is still checked exactly by `2^15` non-5 corners and one rational clipped quadratic minimizer per five-containing support.  The summed margin is

\[
\boxed{
\frac{1098589626561579134109123}
{39422315130808610000000000}>0.
}
\]

The proper non-5 coordinate minimum is `1/91>0`, and the completion upper bound is

\[
-\frac{23641}{2377375}<0.
\]

Thus `P=19` is also noncovering.

## 4. Remaining frontier

After the direct placement scan, the swapped affine campaign, the generalized M16 quadratic certificates, and the new `P=19` diagonal certificate, only

\[
\boxed{172297125=3^4\cdot5^3\cdot7\cdot11\cdot13\cdot17}
\]

remains from the entire `(4,3,1,1,1,1)` profile.

The exact verifier is `solver/m24_four_three_frontier.py`.  This is an internal rigorous frontier reduction pending independent audit and literature review; the remaining seed is not asserted to cover, and the general odd distinct covering-system problem remains open.
