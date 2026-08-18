# Milestone 40 — six exceptional `(3,2,2,1,1,1)` seeds are excluded

M26 leaves twelve direct-bound survivor seeds for the six-prime exponent
profile

\[
(3,2,2,1,1,1).
\]

Six are canonical, with the second square on `7`.  The other six put that
square on `11`, `13`, or the final prime `P`, for `P=17,19`.  M40 excludes all
six exceptional seeds with one quantitative `a=3` reference certificate and
the deficiency recurrence.

## 1. Quantitative precursor

Use the reference precursor

\[
N_0=3^3\cdot5^2\cdot7\cdot11\cdot13\cdot17.
\]

After staging on `3^3`, at least 14 fibres survive.  Distinguish `5^2`; the
other four coordinates `7,11,13,17` are simple.  Hence each nonempty support
has a unique exact divisor and

\[
z_S=q_S/b_S=1+A_S\in\{1,2,3,4\}.
\]

The single-divisor factorial budgets from M30 are

\[
\sum_r A_S\le13,\qquad
\sum_r\binom{A_S}{2}\le5.
\]

Keep the M25 nonnegative linear and diagonal penalties on the sixteen supports
containing `5`.  Add first/second factorial penalties on the six non-special
supports

\[
\{7\},\{11\},\{13\},\{17\},\{7,11\},\{7,13\}.
\]

With denominator `10^6`, the `(alpha,beta)` numerators are

```text
{7}:     (23714,16013)
{11}:    (15815, 3158)
{13}:    (12454, 2217)
{17}:    ( 8914, 1344)
{7,11}:  ( 4451, 1418)
{7,13}:  ( 3593,  988)
```

The selected six variables are checked at all four integral levels; the other
nine are at endpoints by separate concavity.  Thus the exact reduced state
space has

\[
4^6 2^9=2,097,152
\]

states.

Take

\[
C=\frac{3219}{10000}.
\]

All rational lookup entries are multiplied by `Q=10^12` and rounded downward.
The exhaustive integer minimum is

\[
\boxed{321924524492}
\]

against

\[
QC=321900000000,
\]

leaving exact integer slack

\[
\boxed{24524492>0}.
\]

At the minimizing state

```text
(2,2,2,4,3,4,4,3,4,4,4,4,4,4,4)
```

in natural nonempty subset-mask order, the independent exact value is

\[
\frac{27602892902794854989741}{85743367783909735900000}>C.
\]

The distinguished-coordinate first/second-moment cost is

\[
\frac{19049050319373}{6463801093750},
\]

and the factorial cost is

\[
\frac{1021923}{1000000}.
\]

Therefore the quantitative summed-rho margin is

\[
\boxed{
\eta=
\frac{111206677906959}{206841635000000}
}>0.
\]

The non-special four-prime box is the M14 box, whose Clique-Shearer coordinate
polynomials are positive.  Also the special singleton satisfies
`q_5<=4*(6/25)=24/25<1`.  Thus M39 applies quantitatively: the actual uncovered
mass in the selected fibres is at least the summed full-rho margin.

## 2. Scaling from `P=17` to `P=19`

For `P>=17`, replacing the final simple coordinate `1/17` by `1/P` only
shrinks support baselines.  Inflate each grouped charge to the reference
baseline.  The normalized integer activations are unchanged, while first,
second, and factorial budgets scale to the same reference bounds.  Hence the
same exact reference certificate supplies the same `eta` for the `P=19`
precursor.

## 3. Lift one simple prime to a square

Let `q` be the simple prime to be squared and write

\[
N_0=3^3 q B,\qquad N_1=3^3q^2B,
\]

where `B` contains the remaining post-stage factors.  Since the precursor
certificate gives

\[
\delta(N_0)\ge qB\eta,
\]

the deficiency recurrence gives

\[
\delta(N_1)
\ge q\delta(N_0)-\sigma(3^3B)
\ge q^2B\left(\eta-\frac{40}{q^2}\frac{\sigma(B)}B\right).
\]

For all six exceptional seeds the normalized gap is strictly positive:

\[
\begin{array}{c|c|c}
P&q&\eta-40\sigma(B)/(q^2B)\\ \hline
17&11&713749906959/206841635000000\\
17&13&31068949906959/206841635000000\\
17&17&63543061906959/206841635000000\\
19&11&25838240232221/3929991065000000\\
19&13&599214240232221/3929991065000000\\
19&19&26370825700412199/74669830235000000
\end{array}
\]

Hence all six noncanonical M26 seeds in profile `(3,2,2,1,1,1)` are
noncovering.  The exact verifier is
`solver/m40_p322_exceptional_lifts.py`.
