# Milestone 58 — the complete `(3,3,2,1,1,1)` profile is excluded

M57 reduced the six-prime exponent profile `(3,3,2,1,1,1)` to one integer:

\[
N_*=3^3\cdot5^3\cdot7^2\cdot11\cdot13\cdot17
=402026625.
\]

M58 gives an exact weighted-activation certificate for this final seed.  Hence

\[
\boxed{
\{a_1,\ldots,a_6\}=\{3,3,2,1,1,1\}
\Longrightarrow
\prod_i p_i^{a_i}\text{ is noncovering}.
}
\]

This remains a six-prime partial theorem, not a complete solution of Erdős
Problem #7.

## 1. Keep two repeated-7 supports exactly

Stage on `3^3`, leaving 14 selected fibres, and distinguish the repeated
`5^3` coordinate.  On the non-special coordinates `(7^2,11,13,17)`, retain the
weighted activation structure of the two supports `{7}` and `{7,11}`.

For either support, let `A` count the extra 3-adic activations of the exact
divisor containing `7` and let `B` count those of the exact divisor containing
`49`.  Because

\[
\frac1{7m}+\frac1{49m}=\frac8{49m},
\]

the normalized grouped charge is

\[
\boxed{
\frac{q_S}{b_S}=1+\frac{7A+B}{8},
\qquad A,B\in\{0,1,2,3\}.
}
\]

M30 gives separate exact-divisor factorial budgets

\[
\sum A\le13,
\qquad
\sum {A\choose2}\le5,
\]

and the same for every `B` activation.

Five simple supports

\[
\{11\},\{13\},\{17\},\{11,13\},\{11,17\}
\]

are also kept at their exact integral levels `1+A in {1,2,3,4}` and charged by
first/second factorial penalties.

## 2. Rational certificate

With denominator `100000`, the eighteen nonnegative coefficient numerators are

```text
3682, 268, 1370, 391,
437, 70, 202, 32,
1100, 762,
1287, 342,
887, 166,
176, 49,
101, 68
```

in the order

```text
{7}:       A, B, C(A,2), C(B,2)
{7,11}:    A, B, C(A,2), C(B,2)
{11}:      A, C(A,2)
{13}:      A, C(A,2)
{17}:      A, C(A,2)
{11,13}:   A, C(A,2)
{11,17}:   A, C(A,2).
```

The sixteen supports containing the distinguished `5^3` coordinate keep the
M25 nonnegative linear and diagonal quadratic penalties.  M28 supplies their
`a=3` first/second budgets `27` and `63`.

After fixing the non-special charges, each distinguished-coordinate variable
is minimized exactly as a clipped convex rational quadratic.  The eight
remaining unpenalized non-special support variables occur in a separately
concave reduced function, so their minima occur at box endpoints.  The exact
finite state space is therefore

\[
4^4\cdot4^5\cdot2^8
=\boxed{67,108,864}.
\]

## 3. Exact exhaustive lower bound

Take

\[
C=\frac{1591}{5000}=0.3182.
\]

The fast verifier first generates every clipped-quadratic lookup value with
`Fraction` arithmetic.  Each value is multiplied by

\[
Q=10^{12}
\]

and rounded downward.  The exhaustive loop then uses only signed integer
addition and comparison, so its minimum is a rigorous lower bound.

The result is

\[
\boxed{318224090677}
>
318200000000=QC,
\]

with integer slack

\[
\boxed{24090677>0}.
\]

The minimizing reduced state is

```text
(1,1,1,1,2,2,3,2,2,255).
```

An independent exact evaluation at that state is

\[
\frac{334248664255027713025529067}
{1050356255352894264775000000}
>C.
\]

## 4. Positive summed uncovered mass

The exact global charge of the distinguished-coordinate linear/diagonal
penalties is

\[
K_5=
\frac{102569429391470073}
{31672625359375000},
\]

and the factorial penalties cost

\[
K_F=\frac{60507}{50000}.
\]

Hence

\[
14C-K_5-K_F
=
\boxed{
\frac{394942414159229}
{63345250718750000}
}>0.
\]

The non-special factor-4 box is already inside the Clique–Shearer region; its
proper-coordinate and full-coordinate minima are respectively

\[
\frac{459}{7007}>0,
\qquad
\frac{155}{7007}>0.
\]

Also

\[
q_{\{5\}}\le4\left(\frac15+\frac1{25}+\frac1{125}\right)
=\frac{124}{125}<1.
\]

Thus the quantitative completion argument audited in M39 converts the positive
summed `rho` margin into genuine uncovered mass, proving `N_*` noncovering.
Together with M57, this closes the complete `(3,3,2,1,1,1)` profile.

Files:

- `solver/m58_p332_hard_seed.py` — exact constants and theorem audit;
- `solver/m58_p332_hard_seed_fast.py` — reproducible 67,108,864-state integer verifier (`numpy` + `numba`);
- `solver/test_m58_p332_hard_seed.py` — regression checks.
