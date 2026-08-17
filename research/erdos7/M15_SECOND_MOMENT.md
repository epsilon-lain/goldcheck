# Milestone 15 seed: exact second-moment 3-adic compatibility

The M14 `a=4` affine no-go used only the pointwise support box
`b_S <= q_S(r) <= 5 b_S` and the first-moment budget
`sum_r q_S(r) <= 81 b_S` across 41 selected surviving fibres.
That abstraction is too coarse.  The next exact constraint is already much
stronger and follows directly from the 3-adic cylinder geometry.

Let `N=3^a M`, select `s_a=(3^a+1)/2` surviving fibres, and for an exact
`M`-divisor `m` write

`k_m(r) <= 1 + sum_{j=1}^a I_{m,j}(r)`,

where `I_{m,j}` is the indicator of one residue class modulo `3^j`.
For any two divisors `m,n`,

`sum_r I_{m,j}(r) <= 3^(a-j)`,

and an intersection of a `3^j` cylinder with a `3^ell` cylinder is either
empty or one residue class modulo `3^max(j,ell)`, hence

`sum_r I_{m,j}(r) I_{n,ell}(r) <= 3^(a-max(j,ell))`.

Expanding the product gives

`sum_r k_m(r) k_n(r) <= H_a`,

where

`H_a = s_a + 2 sum_j 3^(a-j) + sum_{j,ell} 3^(a-max(j,ell))`.

The double sum has the exact closed form

`sum_{j,ell} 3^(a-max(j,ell)) = sum_{t=1}^a (2t-1)3^(a-t) = 3^a-a-1`,

so

`H_a = (5*3^a - 2a - 3)/2`.

After grouping exact `M`-moduli by square-free support as in M14,

`q_S(r)=sum_{sqf(m)=S} k_m(r)/m`,  `b_S=sum_{sqf(m)=S}1/m`,

we therefore obtain for every pair of supports `S,T`

`sum_r q_S(r) q_T(r) <= H_a b_S b_T`.

For the next frontier `a=4`,

`H_4 = 197`.

This immediately cuts the old 32-corner affine dual obstruction.  That dual
has total weight 41 and first moment exactly `81 b_S` on every support.  Since
its corners use only endpoint multipliers `z_S in {1,5}`, the first moment
forces upper-endpoint weight 10 and hence

`sum_i alpha_i z_S^2 = 41 + 24*10 = 281`

for every support `S`.  Thus the dual has diagonal second moment

`281 b_S^2`,

while every realizable 3-adic fibre configuration satisfies

`sum_r q_S(r)^2 <= 197 b_S^2`.

So the M14 affine dual is not merely suboptimal: it is non-realizable once the
first genuine second-order 3-adic compatibility constraint is retained.

This does **not** yet prove `34459425` noncovering.  It identifies a concrete
strictly stronger feasible region for the next certificate search: keep the
41/81 first moments together with all pair constraints

`sum_r q_S q_T <= 197 b_S b_T`,

then seek a nonlinear / quadratic / transport Clique-Shearer certificate.

Exact verification is in `solver/m15_second_moment.py` and
`solver/test_m15_second_moment.py`.
