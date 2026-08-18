# Milestone 51 — the `a_2=3,a_3=1` branch disappears

M50 closes every

\[
(A,3,1,1,1,1),\qquad A\ge6.
\]

The smaller first exponents on the same branch were already closed by M23,
M25, and M49 together with downward closure.  Thus there is no remaining
minimal direction with `a_2=3,a_3=1`.

The exact componentwise-minimal six-prime exponent frontier is now

\[
\boxed{
(5,4,1,1,1,1),
(4,2,2,1,1,1),
(3,3,2,1,1,1),
(3,2,2,2,1,1).
}
\]

If `a_3=1`, the `a_2=2` and `a_2=3` branches are both closed, so any outside
profile has `a_2>=4`.  The old P44 down-set closes `a_1<=4`, forcing
`a_1>=5` and hence domination of `(5,4,1,1,1,1)`.

If `a_3>=2`, the same three-way split from M46 remains:

- `a_4>=2` gives `(3,2,2,2,1,1)`;
- `a_4=1,a_2>=3` gives `(3,3,2,1,1,1)`;
- `a_4=1,a_2=2` forces `a_1>=4`, giving `(4,2,2,1,1,1)`.

The verifier is `solver/m51_frontier_after_A3_ray.py`.
