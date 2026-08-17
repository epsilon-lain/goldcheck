# Milestone 25 — cross-support second moments close the last M24 seed

Milestone 24 reduced the complete six-prime exponent profile

\[
(4,3,1,1,1,1)
\]

to the single unresolved number

\[
N_0=3^4\cdot5^3\cdot7\cdot11\cdot13\cdot17=172297125.
\]

M25 closes that seed by using the part of the M15 moment theorem that had not
previously been exploited: **cross-support** second moments.

## Theorem candidate

\[
\boxed{172297125\text{ is noncovering}.}
\]

Together with M24, this excludes the entire odd six-prime exponent profile

\[
\boxed{(4,3,1,1,1,1).}
\]

As throughout this project, this is an internal rigorous theorem candidate
pending independent audit and literature/novelty review; it is not a solution
of the full odd distinct covering-system problem.

## 1. Fibre data

Stage modulo `81`.  Select 41 fibres surviving the pure `3,9,27,81`
classes.  On the remaining five prime coordinates `(5,7,11,13,17)`, define
square-free support charges `q_S(r)` as in M14–M16 and

\[
b_S=\prod_{p\in S}x_p,
\qquad
(x_5,x_7,x_{11},x_{13},x_{17})
=\left(\frac{31}{125},\frac17,\frac1{11},\frac1{13},\frac1{17}\right).
\]

For each selected fibre,

\[
b_S\le q_S(r)\le5b_S.
\]

M15 gives simultaneously for every pair of supports

\[
\sum_r q_S(r)\le81b_S,
\qquad
\sum_r q_S(r)q_T(r)\le197b_Sb_T.
\]

The second inequality includes the diagonal case `S=T`.

## 2. Pointwise certificate

M25 uses nonnegative rational coefficients of three types:

* `lambda_S` on all supports;
* diagonal coefficients `nu_S` for all 16 supports containing prime `5`;
* 46 cross coefficients `mu_{S,T}` between selected pairs of the 15 supports
  not containing `5`.

They are stored explicitly in `solver/m25_cross_support_seed.py` and satisfy on
the complete factor-5 box

\[
\rho(q)
+\sum_S\lambda_S q_S
+\sum_{5\in S}\nu_S q_S^2
+\sum_{\substack{5\notin S,T\\S<T}}\mu_{S,T}q_Sq_T
\ge C,
\]

where the exact global minimum is

\[
\boxed{
C=\frac{8062944017330066479969}
{19768351476874000000000}.
}
\]

No floating-point value is used by the verifier.

### Why `2^15` corners still suffice

Fix the 15 non-5 support variables.  Because all five-containing supports
share the prime `5`, the Clique–Shearer polynomial is linear in each of those
16 variables once the non-5 vector is fixed.  M25 adds only a separate
nonnegative square `nu_S q_S^2` to each such variable, so each minimizes as a
one-dimensional clipped convex quadratic.

After those 16 exact minimizations, fix any one non-5 coordinate.  The
Clique–Shearer terms are affine in that coordinate, every cross penalty
`mu_{S,T}q_Sq_T` is affine in it when the other coordinate is fixed, and each
eliminated quadratic contributes the infimum of affine functions of that
coordinate.  Hence the reduced objective is separately concave in all 15
non-5 variables.

Therefore its box minimum is attained at a corner.  The verifier enumerates
exactly

\[
2^{15}=32768
\]

non-5 corners and performs 16 rational clipped-quadratic minimizations at each
corner.

## 3. Summed moment margin

Summing the pointwise certificate over the 41 selected fibres and applying the
M15 first- and second-moment budgets gives

\[
\sum_r\rho(q(r))
\ge
41C
-81\sum_S\lambda_Sb_S
-197\sum_{5\in S}\nu_Sb_S^2
-197\sum_{S<T}\mu_{S,T}b_Sb_T.
\]

The exact verifier obtains

\[
\boxed{
\frac{148743273991746196533}
{3953670295374800000000}
>0.
}
\]

Thus at least one selected fibre has `rho(q(r))>0`.

## 4. Factor-5 completion audit

As in M16, the full four-coordinate non-5 polynomial can be negative, so the
implication from positive full `rho` to an uncovered point must be checked.
The exact M25 audit gives

\[
\min_{C\subsetneq J}\rho_C=\frac1{91}>0,
\qquad
\min\rho_J=-\frac{258}{17017}.
\]

If `rho_J<=0`, then `q_{\{5\}}<=5(31/125)=31/25`.  Using the baseline lower
bounds for the other five-containing supports in the prime-5 split recurrence
gives a multi-affine upper bound whose exact maximum over the same `2^15`
corners is

\[
\boxed{-\frac{3629}{425425}<0.}
\]

Therefore `rho(q)>0` forces `rho_J>0`; all proper coordinate polynomials are
already positive, so the non-5 subsystem lies in the Clique–Shearer region and
the M14/M16 one-coordinate completion argument yields a genuinely uncovered
point.

Hence `172297125` is noncovering.

## 5. Consequence for the exponent frontier

M24 had already excluded every other member of `(4,3,1,1,1,1)`.  Combining
M24 and M25 therefore gives

\[
\boxed{
\{a_1,\ldots,a_6\}=\{4,3,1,1,1,1\}
\Longrightarrow
\prod_{i=1}^6p_i^{a_i}\text{ is noncovering}
}
\]

for arbitrary six distinct odd primes and arbitrary placement of the exponents.

The natural next frontier is no longer this seed.  It is the first exponent
profiles not dominated by the regions already closed in M20–M25, such as
`(4,4,1,1,1,1)`, `(5,3,1,1,1,1)`, and profiles with a third repeated prime.
