# Milestone 41 — weighted two-level activation closes the six canonical P322 seeds

After M40, the only M26 seeds left in exponent profile

\[
(3,2,2,1,1,1)
\]

are the six canonical seeds

\[
3^3\cdot5^2\cdot7^2\cdot p\cdot q\cdot r.
\]

M41 excludes all six with one exact reference certificate.  The new ingredient
is to retain the two different exact divisors behind the repeated coordinate
`7^2`, instead of replacing their grouped charge by a continuous box variable.

## 1. Weighted activation law

Stage on `3^3` and distinguish `5^2`.  For a support `S` containing the
repeated coordinate `7`, write `m` for the product of its other simple primes.
Its two exact divisors with this square-free support are `7m` and `49m`.
Let their 3-adic activation counts in a selected fibre be `A_S` and `B_S`.
Then

\[
 b_S=\frac1{7m}+\frac1{49m}=\frac8{49m}
\]

and therefore

\[
\boxed{
\frac{q_S}{b_S}=1+\frac{7A_S+B_S}{8}.
}
\]

Here

\[
A_S,B_S\in\{0,1,2,3\}.
\]

This is much smaller than the fake continuous box `[1,4]`: the normalized
levels are the sixteen weighted values obtained from `(A,B)`, and the two
activation variables separately obey M30's exact factorial budgets

\[
\sum A\le13,\quad \sum\binom A2\le5,
\qquad
\sum B\le13,\quad \sum\binom B2\le5.
\]

M41 uses this discrete structure for the singleton support `{7}`.

## 2. Reference pointwise certificate

Use the smallest canonical simple tuple

\[
(11,13,17).
\]

Keep M25's nonnegative linear/diagonal penalties on the sixteen supports
containing the distinguished coordinate `5`.  On the repeated singleton `{7}`
use the coefficient numerators, with denominator `10^6`,

```text
A_7:        37094
A_49:        5952
C(A_7,2):   17949
C(A_49,2):    602
```

and on five simple supports use

```text
{11}:     (15816,3723)
{13}:     (13298,2026)
{17}:     ( 9089,1187)
{11,13}:  ( 1866, 491)
{11,17}:  ( 1330, 382)
```

for first/second factorial penalties.

The repeated singleton runs over all `4*4=16` pairs `(A_7,A_49)`.  The five
selected simple variables run over four integer levels, and the remaining nine
variables are checked at endpoints by separate concavity.  Hence the exact
reduced state count is

\[
16\cdot4^5\cdot2^9=\boxed{8,388,608}.
\]

Take

\[
C=\frac{15473}{50000}=0.30946.
\]

Every rational lookup value is multiplied by `Q=10^12` and rounded downward.
The exhaustive integer minimum is

\[
\boxed{309465375243}
\]

against

\[
QC=309460000000,
\]

so the rigorous integer slack is

\[
\boxed{5375243>0}.
\]

At the minimizing weighted state `(A_7,A_49)=(1,1)`, the normalized support
vector in natural mask order is

```text
(2,2,4,2,4,2,4,4,4,3,4,4,4,4,4)
```

and the independent exact value is

\[
\frac{41353979144540955436}{133630391156527890625}>C.
\]

## 3. Completion and global margin

The whole non-special four-coordinate box is inside the Clique-Shearer region.
Exact endpoint enumeration gives

\[
\boxed{
\min_{\emptyset\ne C\subseteq J}\rho_C=\frac{155}{7007}>0.
}
\]

Thus no conditional completion loophole is needed: the M39 quantitative
relative bound is valid throughout the reference box.

The distinguished-coordinate first/second-moment cost is

\[
\frac{487174848269706}{158363126796875},
\]

and the weighted/simple factorial cost is

\[
\frac{245917}{200000}.
\]

Therefore

\[
\sum_{r=1}^{14}\rho(q(r))
\ge
14C-	ext{costs}
=
\boxed{
\frac{268990177767141}{10135240115000000}
}>0.
\]

Hence the reference canonical seed is noncovering.

## 4. One reference kills all six canonical seeds

For every other canonical M26 seed, after keeping `7^2` fixed the three simple
primes are coordinatewise at least `(11,13,17)`.  Thus their reciprocal support
baselines are coordinatewise no larger than the reference baselines.

Inflate each actual grouped charge to the reference baseline.  The normalized
simple activations and the weighted `(A_7,A_49)` pair are unchanged; all M28/M30
budgets become exactly the reference budgets.  These inflated charges remain
valid upper bounds on the actual events.  Therefore the same reference
certificate applies.

This includes the five tuples `(11,13,P)` for

\[
P=17,19,23,29,31
\]

and the off-family tuple `(11,17,19)`.

Consequently all six canonical P322 seeds are noncovering.  Together with M40,
all twelve M26 seeds for `(3,2,2,1,1,1)` are now excluded.

The exact verifier is `solver/m41_p322_canonical_weighted.py`.
