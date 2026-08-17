# M16 audit — why the `2^15` corner reduction is globally valid

Milestone 16 proves exact quadratic Clique–Shearer certificates for

\[
N_P=3^4\cdot5^2\cdot7\cdot11\cdot13\cdot P,
\qquad P\in\{17,19,23\}.
\]

This note closes a subtle optimization point in that proof: after the
5-containing support variables are minimized, why is it sufficient to enumerate
only the `2^15` corners of the 15 non-5 support variables?

## 1. Split the prime-5 coordinate

Write `J={7,11,13,P}` and denote the non-5 charge vector by `q^0`.  The
five-coordinate independence polynomial has the exact recurrence

\[
\rho(q)=\rho_J(q^0)-
\sum_{T\subseteq J}q_{\{5\}\cup T}\,\rho_{J\setminus T}(q^0).
\]

M16 minimizes the pointwise certificate

\[
F(q)=\rho(q)+\sum_S\lambda_Sq_S+\mu q_{\{5\}}^2,
\qquad \mu>0,
\]

over the box `b_S <= q_S <= 5 b_S`.

For fixed `q^0`, every 5-containing variable except `q_{\{5\}}` occurs
linearly.  Hence its exact minimum is attained at one of its two endpoints.
The remaining variable `q_{\{5\}}` minimizes the one-dimensional convex
quadratic

\[
(\lambda_{\{5\}}-\rho_J(q^0))x+\mu x^2
\]
clipped to `[b_{\{5\}},5b_{\{5\}}]`.

## 2. Separate concavity after eliminating the 5-containing variables

Let `Phi(q^0)` be the exact value after those 16 minimizations.
Fix any one of the 15 non-5 support coordinates and hold the other 14 fixed.
Every `rho_C(q^0)` is affine in that coordinate because the independence
polynomial is multi-affine.

For a 5-containing support `{5} union T`, `T != empty`, the eliminated term is

\[
\min_{x\in\{b_{5T},5b_{5T}\}}
(\lambda_{5T}-\rho_{J\setminus T}(q^0))x.
\]

It is the minimum of two affine functions of the chosen non-5 coordinate, hence
is concave in that coordinate.

For the singleton support `{5}`, define

\[
\psi(c)=\min_{x\in[b_5,5b_5]}(cx+\mu x^2).
\]

As a function of `c`, `psi` is an infimum of affine functions and is therefore
concave.  Since

\[
c=\lambda_5-\rho_J(q^0)
\]
is affine in each individual non-5 coordinate, `psi(c)` is concave in that
coordinate as well.

The terms left before elimination are affine in each individual coordinate.
Therefore `Phi` is **separately concave** in all 15 non-5 variables.

## 3. A separately concave function reaches its box minimum at a corner

On an interval, a concave function has a minimum at an endpoint.  Starting from
any point of the 15-dimensional box, move the first coordinate to an endpoint
without increasing `Phi`, then the second, and so on.  After 15 moves one reaches
a box corner with value no larger than the starting value.

Consequently

\[
\min_{q^0\text{ in the box}}\Phi(q^0)
=
\min_{q^0\text{ at a box corner}}\Phi(q^0).
\]

Thus the exact `2^15=32768` enumeration in
`solver/m16_quadratic_frontier.py` really computes the global pointwise minimum;
it is not merely a corner heuristic.

This audit is purely structural and independent of the numerical values of the
M16 certificate weights.
