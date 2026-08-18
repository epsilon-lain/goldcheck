# Milestone 45 — every `(A,2,1,1,1,1)` profile with `A>=6` is excluded

M44 closes exponent profile `(6,2,1,1,1,1)`, but its quantitative deficiency
margins are much stronger than positivity.  M45 combines those margins with an
infinite-exponent McNew--Setty audit and closes the entire ray

\[
\boxed{(A,2,1,1,1,1),\qquad A\ge6.}
\]

Thus no new successor `(7,2,1,1,1,1)`, `(8,2,1,1,1,1)`, and so on needs to be
added to the exponent frontier.

## 1. Direct bound uniformly in the large exponent

For a prime coordinate `p`,

\[
x_p(A)=\sum_{j=1}^A p^{-j}<\frac1{p-1}.
\]

M22 proves that the six-prime direct bound is strictly increasing in every
`x` coordinate.  Hence replacing the large exponent `A` by infinity gives a
valid uniform upper bound for every finite `A`.

At the minimal odd primes `(3,5,7,11,13,17)`, all 30 placements of the large
exponent and the square can therefore be audited once in the limit.  Only two
survive:

\[
\begin{array}{c|c}
\text{positions}&R_\infty\\ \hline
A\text{ on }3,\ 2\text{ on }5&927/910\\
A\text{ on }3,\ 2\text{ on }7&1194969/1191190
\end{array}
\]

The largest of the remaining 28 limit placements is the square-on-11 case,
with

\[
\boxed{R_\infty=169203/170170<1.}
\]

Thus no new exponent placement can appear at any larger `A`.

For the two surviving placements, exact `R_infinity<1` kill anchors show that
exactly the same eight prime tuples found by M43 are the only direct survivors
for every `A>=6`: seven canonical square-on-5 tuples and one square-on-7 tuple.

## 2. Quantitative recurrence propagates forever

For fixed post-stage part `M`, if

\[
\delta(3^aM)\ge M g_a,
\]

the deficiency recurrence gives

\[
g_{a+1}\ge3g_a-\frac{\sigma(M)}M.
\]

M44 supplies the uniform canonical base gap

\[
g_6=
\frac{1396444066114191}{180986430625000},
\qquad
s=\frac{\sigma(M)}M\le\frac{107136}{60775}.
\]

Since

\[
g_6>s/2,
\]

the lower-bound recurrence is increasing.  Explicitly, for `A>=6`,

\[
\boxed{
g_A\ge
3^{A-6}g_6-rac{s}{2}(3^{A-6}-1)>0.
}
\]

The seven canonical direct-survivor tuples are all covered by this same
reference lower bound because increasing the four simple primes only decreases
`sigma(M)/M`.

For the exceptional square-on-7 tuple, M44 supplies

\[
g_6^*=\frac{71329092093939597}{14189336161000000},
\qquad
s^*=\frac{147744}{85085},
\]

and again `g_6^*>s^*/2`, so the identical recurrence propagates positivity to
all higher exponents.

Consequently every one of the eight universal direct-survivor templates is
noncovering for every finite `A>=6`.  Together with the infinite-exponent
direct reduction, this proves the complete ray exclusion.

The exact verifier is `solver/m45_infinite_pA2_ray.py`.
