# Milestone 30 — centered and factorial 3-adic moment hierarchies

M28 bounds the raw support charges `q_S`.  Saturation supplies a deterministic
baseline `b_S` in every selected fibre, so write

\[
u_S(r)=q_S(r)-b_S\ge0.
\]

For `N=3^aM`, after choosing `s_a=(3^a+1)/2` surviving 3-adic fibres, the exact
centered hierarchy is

\[
\boxed{
\sum_r\prod_{h=1}^t u_{S_h}(r)
\le M(a,t)\prod_{h=1}^tb_{S_h}
}
\]

for arbitrary, possibly repeated supports, where

\[
M(a,t)=\sum_{J=1}^a\bigl(J^t-(J-1)^t\bigr)3^{a-J}.
\]

At `a=4`,

\[
\boxed{M(4,1..5)=(40,76,184,532,1720).}
\]

The M28 raw constants are recovered exactly by the binomial transform

\[
H(a,t)=s_a+\sum_{u=1}^t{t\choose u}M(a,u).
\]

There is additional discrete information when a support contains only one exact
`M`-divisor.  Writing

\[
q_S/b_S=1+A_S,
\qquad A_S\in\{0,\ldots,a\},
\]

one has the falling-factorial bounds

\[
\boxed{
\sum_r{A_S(r)\choose t}
\le F(a,t),
\qquad
F(a,t)=\sum_{J=t}^a{J-1\choose t-1}3^{a-J}.
}
\]

At `a=4`,

\[
\boxed{F(4,1..4)=(40,18,6,1).}
\]

These factorial constraints are strictly stronger than retaining only
multilinear moments in distinct support variables and are the mechanism used by
M32 and M33.

Exact implementation: `solver/m30_centered_moments.py`.
