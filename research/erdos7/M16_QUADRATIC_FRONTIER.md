# Milestone 16 — quadratic second-moment exclusion of the first `a=4` frontier

This milestone turns the M15 second-moment constraint into an exact finite
Clique-Shearer certificate.

It excludes all three previously listed first `a=4` six-prime survivors

\[
\begin{aligned}
34459425 &= 3^4\cdot5^2\cdot7\cdot11\cdot13\cdot17,\\
38513475 &= 3^4\cdot5^2\cdot7\cdot11\cdot13\cdot19,\\
46621575 &= 3^4\cdot5^2\cdot7\cdot11\cdot13\cdot23.
\end{aligned}
\]

This is still a finite frontier exclusion, not a solution of the odd distinct
covering-system problem.

## 1. Input from the `3^4` fibre geometry

Saturate a hypothetical divisor-modulus covering and select 41 fibres modulo
81 that survive the pure moduli `3,9,27,81`.

For square-free support `S` on the five non-3 prime coordinates, let `q_S(r)`
be the grouped union-bound charge in fibre `r`, and let

\[
b_S=\prod_{p\in S}x_p,\qquad
x_5=\frac6{25},\ x_7=\frac17,\ x_{11}=\frac1{11},
\ x_{13}=\frac1{13},\ x_P=\frac1P.
\]

M14/M15 give, for every selected fibre,

\[
b_S\le q_S(r)\le5b_S,
\]

and across the 41 selected fibres,

\[
\sum_r q_S(r)\le81b_S,\qquad
\sum_r q_S(r)q_T(r)\le197b_Sb_T.
\]

M16 only needs the diagonal case for the support `{5}`:

\[
\sum_r q_{\{5\}}(r)^2\le197\left(\frac6{25}\right)^2.
\]

## 2. A quadratic pointwise certificate

Let `rho(q)` be the five-coordinate Clique-Shearer independence polynomial.
The exact verifier uses nonnegative rational coefficients `lambda_S` and

\[
\mu=\frac{258}{625}
\]

such that, on the whole factor-5 support box,

\[
\rho(q)+\sum_S\lambda_Sq_S+\mu q_{\{5\}}^2\ge C_P.
\]

The `lambda_S` are stored explicitly in
`solver/m16_quadratic_frontier.py`.

This inequality is verified without floating-point optimization.  Split off the
5-coordinate.  For each of the `2^15=32768` corners of the 15 non-5 support
variables:

* every 5-containing variable except `q_{\{5\}}` occurs linearly and therefore
  minimizes at an endpoint;
* `q_{\{5\}}` is a one-dimensional convex quadratic and its clipped rational
  minimizer is evaluated exactly.

Thus the verifier computes the true global minimum of the quadratic certificate
on the complete 31-variable box.

For `P=17`,

\[
C_{17}=\frac{27401186093}{53178125000}.
\]

The resulting summed lower bound is

\[
41C_{17}
-81\sum_S\lambda_Sb_S
-197\mu b_{\{5\}}^2
=
\boxed{\frac{2804670823}{13294531250}}>0.
\]

Hence at least one selected fibre has `rho(q(r))>0`.

The same exact certificate gives

\[
\boxed{
\begin{aligned}
P=19:\quad&
\frac{704120180922703}{1918675352343750}>0,\\[1mm]
P=23:\quad&
\frac{49732740695329}{83861791406250}>0.
\end{aligned}}
\]

## 3. Closing the factor-5 Shearer subtlety

At factor 5 the four-coordinate non-5 polynomial `rho_J` is not positive on the
entire box, so the M14 implication `rho(q)>0 => uncovered` cannot simply be
reused without an audit.

The exact audit observes that every *proper* non-5 coordinate polynomial stays
positive; for all three primes above the worst proper value is

\[
\frac1{91}>0.
\]

Write `J={7,11,13,P}`.  The prime-5 split recurrence is

\[
\rho(q)
=(1-q_{\{5\}})\rho_J(q^0)
-\sum_{\emptyset\ne T\subseteq J}
q_{\{5\}\cup T}\rho_{J\setminus T}(q^0).
\]

If `rho_J<=0`, then `q_{\{5\}}\le 6/5` and
`q_{\{5\}\cup T}\ge b_{\{5\}\cup T}`, so

\[
\rho(q)\le
-\frac15\rho_J(q^0)
-\sum_{\emptyset\ne T\subseteq J}
b_{\{5\}\cup T}\rho_{J\setminus T}(q^0).
\]

The right side is multi-affine in the 15 non-5 variables, hence its maximum is
at a box corner.  Exact enumeration gives

\[
\begin{array}{c|c}
P & \text{uniform upper bound}\\ \hline
17 & -744/85085\\
19 & -4766/475475\\
23 & -6858/575575
\end{array}
\]

and all are strictly negative.

Therefore `rho(q)>0` forces `rho_J(q^0)>0`.  Since every proper non-5
coordinate polynomial is already positive, the non-5 subsystem is in the
Clique-Shearer region.  The M14 one-coordinate completion lemma then applies,
so `rho(q)>0` leaves an uncovered point in that fibre.

Combining this implication with the positive summed quadratic margins excludes
all three numbers above as covering numbers.

## 4. Verification

Exact arithmetic only:

```text
cd research/erdos7/solver
python -m pytest -q test_m16_quadratic_frontier.py
```

The next target is to determine whether the same quadratic certificate can be
proved uniformly for the symbolic family

\[
3^4\cdot5^2\cdot7\cdot11\cdot13\cdot P,\qquad P\ge17,
\]

rather than checking primes one at a time.
