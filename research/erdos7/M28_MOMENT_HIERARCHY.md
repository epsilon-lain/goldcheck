# Milestone 28 — an all-orders 3-adic moment hierarchy

M25 succeeded because M15 retained genuine cross-support second moments.  The
hardest remaining M27 seed

\[
3^4\cdot5^4\cdot7\cdot11\cdot13\cdot17
\]

is already beyond the fixed M25 second-order certificate.  M28 therefore
extracts the complete higher-moment information hidden in the same 3-adic
fibre geometry instead of deriving moments ad hoc one order at a time.

This milestone is a structural theorem/tool, not yet an exclusion of the two
remaining M27 seeds.

## 1. Exact divisor-load moments

Let `N=3^a M`, with `(3,M)=1`, and select

\[
s_a=\frac{3^a+1}{2}
\]

fibres modulo `3^a` surviving the pure classes.  For an exact divisor `m|M`,
write

\[
k_m(r)\le 1+\sum_{j=1}^a
\mathbf 1_{r\equiv c_{j,m}\pmod{3^j}}.
\]

For `t>=1` exact divisors `m_1,...,m_t`, expand

\[
\prod_{h=1}^t k_{m_h}(r).
\]

A term using `u` indicator factors at levels `j_1,...,j_u` has intersection
size at most

\[
3^{a-\max(j_1,\ldots,j_u)}
\]

on the full `3^a` residue space; incompatibility only makes the intersection
smaller.  Grouping level tuples by `J=max(j_h)` gives

\[
M(a,u)=\sum_{J=1}^a
\bigl(J^u-(J-1)^u\bigr)3^{a-J}.
\]

Hence

\[
\boxed{
H(a,t)=s_a+\sum_{u=1}^t\binom tu M(a,u)
}
\]

satisfies

\[
\boxed{
\sum_r\prod_{h=1}^t k_{m_h}(r)\le H(a,t).
}
\]

The proof does not require the `m_h` to be distinct.

## 2. Grouped support charges

For the M14/M25 square-free support charge

\[
q_S(r)=\sum_{\operatorname{sqf}(m)=S}\frac{k_m(r)}m,
\qquad
b_S=\sum_{\operatorname{sqf}(m)=S}\frac1m,
\]

expand a product of arbitrary, possibly repeated supports.  Applying the exact
divisor-load inequality term by term yields

\[
\boxed{
\sum_r\prod_{h=1}^t q_{S_h}(r)
\le
H(a,t)\prod_{h=1}^t b_{S_h}.
}
\]

Thus the first-moment and pair-moment budgets used before are simply the first
two levels of one hierarchy.

## 3. The `a=4` constants

For the current 81-fibre geometry,

\[
\boxed{
H(4,1)=81,\quad
H(4,2)=197,\quad
H(4,3)=573,\quad
H(4,4)=1925,\quad
H(4,5)=7221.
}
\]

In particular, M15's constant `197` is recovered exactly and the new cubic
budget is

\[
\boxed{
\sum_r q_S(r)q_T(r)q_U(r)
\le573\,b_Sb_Tb_U.
}
\]

Repeated supports are allowed, for example

\[
\sum_r q_S(r)^2q_T(r)\le573\,b_S^2b_T.
\]

The first three level sums also simplify to

\[
M(a,1)=\frac{3^a-1}{2},
\qquad
M(a,2)=3^a-a-1,
\]

\[
4M(a,3)=11\cdot3^a-6a^2-12a-11,
\]

and therefore

\[
\boxed{
4H(a,3)=31\cdot3^a-6a^2-24a-27.
}
\]

## 4. Why this matters for the M27 boss

The factor-5 pointwise box at `a=4` allows an endpoint multiplier as large as
`5`.  Relative to 41 selected fibres, the normalized moment caps become much
stronger as the order rises:

\[
81,\ 197,\ 573,\ 1925,\ 7221
\]

versus endpoint growth

\[
5,\ 25,\ 125,\ 625,\ 3125.
\]

So highly spiky configurations that can survive all first- and second-moment
relaxations are increasingly expensive at third and higher order.  This gives
a principled next certificate hierarchy: augment the M25 polynomial minorant
with nonnegative multilinear moment penalties and charge every monomial by the
corresponding exact `H(4,t)` budget.

A numerical reconnaissance during this milestone found that merely appending
cubic terms to the **fixed** M25 lower-order coefficients does not immediately
close the symmetric `3^4 5^4` seed.  This is deliberately not recorded as a
rigorous no-go: it only says the next certificate should re-optimize the lower
orders jointly with the new hierarchy, or retain still more compatibility.

The exact implementation is `solver/m28_moment_hierarchy.py`, with regression
checks in `solver/test_m28_moment_hierarchy.py`.
