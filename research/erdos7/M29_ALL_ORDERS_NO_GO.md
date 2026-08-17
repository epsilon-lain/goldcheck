# Milestone 29 — exact all-orders barrier for the fixed-five M25/M28 cone

The hardest M27 seed is

\[
N_0=3^4\cdot5^4\cdot7\cdot11\cdot13\cdot17=861485625.
\]

M28 supplies exact moment bounds of every order, so the first natural question is whether one can keep the successful M25 treatment of the sixteen supports containing prime `5` and simply add arbitrary higher-order nonnegative multilinear penalties among the fifteen supports not containing `5`.

M29 answers that precise question **no**, with an exact rational dual certificate.

This is a method-level obstruction only. It does **not** prove that `N_0` covers, and it does not resolve Erdős Problem #7.

## 1. The certificate class ruled out

Stage modulo `81` and select 41 surviving 3-adic fibres as in M15–M28. Put

\[
(x_5,x_7,x_{11},x_{13},x_{17})
=
\left(\frac{156}{625},\frac17,\frac1{11},\frac1{13},\frac1{17}\right).
\]

Keep exactly the M25 linear coefficients `lambda_S` and the positive diagonal coefficients `nu_S q_S^2` on the sixteen supports containing prime `5`.

On the fifteen non-5 supports, allow an **arbitrary** finite penalty

\[
\sum_{\varnothing\ne A\subseteq\mathcal N}
 c_A\prod_{S\in A}q_S,
\qquad c_A\ge0,
\]

where `mathcal N` is the set of fifteen non-5 support variables. Thus every multilinear order `1,...,15` is available; only repeated use of the same support variable inside one monomial is excluded.

M28 charges an order-`t` monomial by

\[
H(4,t)\prod_{S\in A}b_S.
\]

For a non-5 box corner write `q_S=b_S z_S`, with `z_S in {1,5}`. After the sixteen five-containing variables are minimized exactly as independent clipped convex quadratics, denote the remaining exact pointwise value by `B(z)`.

Writing

\[
w_A=c_A\prod_{S\in A}b_S,
\]

a positive-margin proof in this class would require some `C` and `w_A>=0` such that

\[
B(z)+\sum_A w_A\prod_{S\in A}z_S\ge C
\]

for every non-5 corner, while

\[
41C-K_5-\sum_A H(4,|A|)w_A>0,
\]

where `K_5` is the exact first/second-moment cost of the frozen M25 five-containing terms.

## 2. Exact dual distribution

`solver/m29_all_orders_no_go.py` stores nonnegative rational weights

\[
\alpha_z=\frac{w_z}{100000}
\]

on 103 of the `2^15` non-5 corners. They satisfy exactly

\[
\sum_z\alpha_z=41.
\]

For every nonempty subset `A` of the fifteen non-5 variables — all

\[
2^{15}-1=32767
\]

multilinear monomials — the verifier checks

\[
\boxed{
\sum_z\alpha_z\prod_{S\in A}z_S
\le H(4,|A|).
}
\]

The tightest integer slack after multiplying by the common denominator `100000` is still positive:

\[
\boxed{60}.
\]

Thus the dual distribution respects the complete M28 hierarchy for every multilinear order `1,...,15` simultaneously.

## 3. Negative dual gap

The frozen five-containing global cost is

\[
K_5=\frac{807151395889143}{83666064453125}.
\]

The same exact weights give

\[
\sum_z\alpha_z B(z)-K_5
=
\boxed{
-\frac{3441114552627898016887069582655901956931361}
{86697898630058196083796127935000000000000000}
}<0.
\]

Now multiply any purported pointwise certificate by `alpha_z` and sum over the corners. The dual moment inequalities imply

\[
41C
\le
\sum_z\alpha_zB(z)
+
\sum_A H(4,|A|)w_A.
\]

Therefore its summed margin must satisfy

\[
41C-K_5-\sum_AH(4,|A|)w_A
\le
\sum_z\alpha_zB(z)-K_5
<0.
\]

So **no certificate in this entire all-orders multilinear non-5 cone can close `861485625` while the five-containing side is frozen to M25.**

## 4. What this rules out — and what it does not

This is substantially stronger than the M28 numerical observation that a few cubic terms did not help. M29 permits every nonnegative multilinear penalty among the non-5 variables, through order 15, and excludes the whole class exactly.

It does **not** rule out stronger uses of M28. In particular, the dual does not satisfy the repeated-support moment constraints strongly enough to exclude penalties such as

\[
q_S^2,\qquad q_S^3,\qquad q_S^2q_T,
\]

on the non-5 side. Nor does M29 allow the sixteen five-containing linear/diagonal coefficients to be re-optimized jointly, cross terms involving five-containing supports, or exact 3-adic transport information beyond the moment hierarchy.

Those are now the justified next directions. A useful next attack should therefore change the mechanism, not merely add more distinct-variable multilinear terms to the frozen M25 certificate.

## 5. Verification

Exact arithmetic only:

```text
cd research/erdos7/solver
python -m pytest -q test_m29_all_orders_no_go.py
```

The verifier checks all 32767 dual moment inequalities, the 103-point rational mass certificate, the exact frozen cost, and the exact negative dual gap.
