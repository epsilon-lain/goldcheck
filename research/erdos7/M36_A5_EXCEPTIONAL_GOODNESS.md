# Milestone 36 — the exceptional `(5,2,1,1,1,1)` seed is noncovering

M35 reduces the six canonical M26 seeds in profile

\[
(5,2,1,1,1,1)
\]

to one.  The seventh M26 seed has a different exponent placement:

\[
\boxed{
N_*=3^5\cdot5\cdot7^2\cdot11\cdot13\cdot17.
}
\]

M36 excludes this exceptional seed by a direct `a=5` factorial-goodness
certificate.  Thus after M35–M36 the entire seven-seed P52 frontier is reduced
to the single canonical integer

\[
\boxed{3^5\cdot5^2\cdot7\cdot11\cdot13\cdot17.}
\]

This is still a partial six-prime theorem, not a resolution of Erdős Problem #7.

## 1. Stage on `3^5`

The pure classes modulo

\[
3,9,27,81,243
\]

cover at most

\[
81+27+9+3+1=121
\]

residues modulo `243`.  Hence at least

\[
\boxed{122}
\]

3-adic fibres survive.

Use the repeated post-stage coordinate `7^2` as the distinguished
Clique–Shearer completion coordinate.  The other four coordinates are the
simple primes

\[
5,11,13,17.
\]

Therefore every nonempty support among these four primes corresponds to a
single exact divisor.  Its normalized charge has the integral form

\[
z_S=\frac{q_S}{b_S}=1+A_S,
\qquad A_S\in\{0,1,2,3,4,5\}.
\]

## 2. Exact a=5 factorial budgets

M30 gives, for a single exact divisor,

\[
\sum_r {A_S(r)\choose t}
\le
F(5,t).
\]

The complete a=5 list is

\[
\boxed{F(5,1),\ldots,F(5,5)=(121,58,24,7,1).}
\]

M36 uses only the first two:

\[
\sum_r A_S\le121,
\qquad
\sum_r {A_S\choose2}\le58.
\]

## 3. Goodness functional

As in M33, define

\[
g(q)=\min\left(
\rho_{\rm full}(q),
\{\rho_C(q^0):\varnothing\ne C\subseteq\{5,11,13,17\}\}
\right).
\]

If `g(q)>0`, all non-special coordinate polynomials are positive and the full
five-coordinate polynomial is positive.  Hence the non-special subsystem lies
in the Clique–Shearer region and the relative one-coordinate completion
argument gives a genuinely uncovered point.

The distinguished-coordinate baseline is

\[
x_7=\frac17+\frac1{49}=\frac8{49}.
\]

Keep the nonnegative M25 linear and diagonal penalties on the sixteen supports
containing the distinguished coordinate.  At `a=5` their global first/second
moment cost is

\[
\boxed{
K_7=
\frac{767161507789382}{44341675503125}.
}
\]

Their pointwise minimum at lower endpoints is

\[
P_0=
\frac{2324089726722}{44341675503125}.
\]

## 4. Six factorial penalties

Use the six non-special supports

\[
\{5\},\{11\},\{13\},\{17\},\{5,11\},\{5,13\}.
\]

For each selected support add

\[
\alpha_S A_S+\beta_S{A_S\choose2}.
\]

With common denominator `10^6`, the numerator pairs `(alpha,beta)` are

```text
{5}:     (55520,32504)
{11}:    (16007, 4671)
{13}:    (13335, 2716)
{17}:    (10803, 1636)
{5,11}:  ( 8762, 2963)
{5,13}:  ( 7194, 1580)
```

Their exact global factorial cost is

\[
121\sum\alpha_S+58\sum\beta_S
=
\boxed{\frac{16178201}{1000000}}.
\]

The six selected variables are checked at every integer level `1,...,6`.
The other nine variables carry no new penalty, and the reduced goodness base is
separately concave in each of them, so their minima occur at endpoints `1` or
`6`.  The complete finite state space is therefore

\[
6^6 2^9=\boxed{23,887,872}.
\]

## 5. Exact pointwise verification

Take

\[
C=\frac{2929}{10000}=0.2929.
\]

The verifier constructs all clipped-quadratic and coordinate-branch lookup
entries using exact `Fraction` arithmetic.  It multiplies each by

\[
Q=10^{12}
\]

and rounds **down**, so the subsequent integer loop computes a rigorous lower
bound.

The exhaustive minimum is

\[
\boxed{292944712245}
\]

against

\[
QC=292900000000,
\]

leaving integer slack

\[
\boxed{44712245>0}.
\]

The minimizing normalized state is

```text
(1,6,2,1,1,6,6,1,6,6,6,6,6,6,6)
```

in subset order

`1,2,12,3,13,23,123,4,14,24,124,34,134,234,1234`.

An independent exact evaluation at this state gives

\[
\frac{47181019651823844673970073}
{161057761680622927120000000}
>\frac{2929}{10000}.
\]

## 6. Positive summed goodness

Finally,

\[
\sum_{r=1}^{122}g(q(r))
\ge
122C-K_7-\frac{16178201}{1000000}.
\]

The exact margin is

\[
\boxed{
\frac{31989285548113199}
{14189336161000000}
}>0.
\]

Therefore at least one surviving fibre has `g(q)>0`, and on that fibre the
relative Clique–Shearer completion leaves an uncovered residue.  Hence

\[
\boxed{
3^5\cdot5\cdot7^2\cdot11\cdot13\cdot17
\text{ is noncovering}.}
\]

The verifier is `solver/m36_a5_exceptional_goodness.py`; its regression test is
`solver/test_m36_a5_exceptional_goodness.py`.
