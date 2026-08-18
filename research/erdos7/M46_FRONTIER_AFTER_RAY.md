# Milestone 46 — the minimal exponent frontier drops to four directions

M42 left five minimal sorted six-prime exponent profiles.  M45 removes not just
`(6,2,1,1,1,1)` but the entire ray

\[
(A,2,1,1,1,1),\qquad A\ge6.
\]

The smaller members of the same branch were already inside the known
noncovering down-set.  Hence the whole `a_2=2,a_3=1` branch disappears from the
frontier.

The exact remaining componentwise-minimal antichain is

\[
\boxed{
(5,3,1,1,1,1),
(4,2,2,1,1,1),
(3,3,2,1,1,1),
(3,2,2,2,1,1).
}
\]

Completeness follows by sorting

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1.
\]

If `a_3=1`, the entire `a_2=2` branch is now closed, so any remaining profile
has `a_2>=3`.  Failure of the already closed `(4,4,1,1,1,1)` down-set forces
`a_1>=5`, giving domination of `(5,3,1,1,1,1)`.

If `a_3>=2`, then:

- `a_4>=2` gives `(3,2,2,2,1,1)`;
- `a_4=1` and `a_2>=3` gives `(3,3,2,1,1,1)`;
- `a_4=1` and `a_2=2` forces `a_1>=4` outside the closed P322 down-set, giving
  `(4,2,2,1,1,1)`.

The four profiles are pairwise incomparable, so the list is exact.

The verifier is `solver/m46_frontier_after_ray.py`.
