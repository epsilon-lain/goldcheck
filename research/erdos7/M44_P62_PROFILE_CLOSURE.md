# Milestone 44 — the complete `(6,2,1,1,1,1)` profile is excluded

M43 reduces the six-prime exponent profile

\[
(6,2,1,1,1,1)
\]

to eight exact McNew--Setty survivor seeds: seven canonical seeds with the
square on prime `5`, and one exceptional seed with the square on prime `7`.
M44 excludes all eight.

Therefore

\[
\boxed{
\{a_1,\ldots,a_6\}=\{6,2,1,1,1,1\}
\Longrightarrow
\prod_{i=1}^6 p_i^{a_i}\text{ is noncovering}.
}
\]

This is a project-internal profile theorem candidate, not a complete solution
of Erdős Problem #7.

## 1. Canonical branch: a quantitative `a=5` precursor

Use the reference precursor

\[
N_5=3^5\cdot5^2\cdot7\cdot11\cdot13\cdot17.
\]

Stage on `3^5`; at least

\[
\frac{3^5+1}{2}=122
\]

fibres survive.  Distinguish the repeated post-stage coordinate `5^2`.  The
remaining coordinates `7,11,13,17` are simple, so every nonempty support has
an integral normalized activation

\[
z_S=q_S/b_S=1+A_S\in\{1,2,3,4,5,6\}.
\]

M30 gives

\[
\sum A_S\le121,
\qquad
\sum\binom{A_S}{2}\le58.
\]

The certificate keeps the M25 nonnegative linear/diagonal penalties on the
sixteen supports containing `5`.  Six non-special supports are checked at all
six activation levels with first/second factorial penalties:

\[
\{7\},\{11\},\{13\},\{17\},\{7,11\},\{7,13\}.
\]

The remaining nine supports receive only nonnegative first-factorial penalties.
The reduced goodness base is separately concave in each such variable, so their
minima occur at endpoints.  Hence the exact reduced state count is

\[
6^6 2^9=\boxed{23,887,872}.
\]

With coefficient denominator `10^6`, the six selected `(alpha,beta)` numerator
pairs are

```text
{7}:     (18860,18054)
{11}:    (11896, 5465)
{13}:    ( 9760, 3740)
{17}:    ( 6345, 2463)
{7,11}:  ( 4095, 1428)
{7,13}:  ( 3068, 1217)
```

and the linear numerators on the remaining masks
`6,7,9,10,11,12,13,14,15` are

```text
2278, 611, 3458, 1591, 423, 1254, 343, 165, 43.
```

Take

\[
C=\frac{32999}{100000}=0.32999.
\]

Every rational lookup entry is computed exactly, multiplied by `Q=10^12`, and
rounded downward.  The exhaustive integer lower minimum is

\[
\boxed{329998003891}
\]

against

\[
QC=329990000000,
\]

so the rigorous integer slack is

\[
\boxed{8003891>0}.
\]

The minimizing normalized state is

```text
(3,2,2,3,3,1,1,3,6,1,1,6,6,1,6)
```

in natural nonempty subset order.  Its independent exact value is

\[
\frac{90509692970019047913}{274273455901445000000}>C.
\]

## 2. Quantitative goodness margin and lift to exponent six

As in M36, use

\[
g(q)=\min\bigl(\rho_{\rm full}(q),\{\rho_C(q^0):\emptyset\ne C\subseteq J\}\bigr).
\]

If `g>0`, all non-special coordinate polynomials are positive and the relative
Clique--Shearer completion gives a genuinely uncovered proportion at least
`rho_full>=g`.  If `g<=0`, uncovered probability is trivially at least
`0>=g`.  Thus the summed goodness margin is a quantitative lower bound on real
uncovered mass, not merely a positivity witness.

The distinguished-coordinate first/second-moment cost is

\[
\frac{1242244751435847}{45246607656250},
\]

and the total factorial/linear penalty cost is

\[
\frac{2411069}{250000}.
\]

Hence

\[
\sum_{r=1}^{122}g(q(r))
\ge
122C-	ext{costs}
=
\boxed{
\eta=
\frac{571830798571397}{180986430625000}
}>0.
\]

Let

\[
M=5^2\cdot7\cdot11\cdot13\cdot17.
\]

Then

\[
\frac{\sigma(M)}M=\frac{107136}{60775}.
\]

Therefore

\[
\delta(3^6M)
\ge3\delta(3^5M)-\sigma(M)
\ge M\left(3\eta-\frac{\sigma(M)}M\right),
\]

and the exact normalized lift gap is

\[
\boxed{
\frac{1396444066114191}{180986430625000}>0.
}
\]

Thus the minimal canonical M43 seed is noncovering.

For every other canonical seed, the four simple primes are coordinatewise no
smaller than `(7,11,13,17)`.  Inflate their grouped charges to the reference
baselines.  Normalized activations and the reference factorial/moment budgets
are preserved, while `sigma(M)/M` only decreases.  Hence the same reference
certificate and lift exclude all seven canonical seeds.

## 3. Exceptional seed

The unique exceptional M43 seed is

\[
3^6\cdot5\cdot7^2\cdot11\cdot13\cdot17.
\]

M36 already supplies the quantitative `a=5` goodness margin for its precursor

\[
3^5\cdot5\cdot7^2\cdot11\cdot13\cdot17:
\qquad
\eta_*=\frac{31989285548113199}{14189336161000000}.
\]

For

\[
M_*=5\cdot7^2\cdot11\cdot13\cdot17,
\]

\[
\frac{\sigma(M_*)}{M_*}=\frac{147744}{85085}.
\]

The lift gap is

\[
3\eta_*-rac{\sigma(M_*)}{M_*}
=
\boxed{
\frac{71329092093939597}{14189336161000000}>0.
}
\]

so the exceptional seed is also noncovering.

All eight M43 seeds are therefore excluded, and M43's universal direct-bound
reduction closes the entire `(6,2,1,1,1,1)` prime family.

The exact verifier is `solver/m44_p62_profile_closure.py`, with regression
checks in `solver/test_m44_p62_profile_closure.py`.
