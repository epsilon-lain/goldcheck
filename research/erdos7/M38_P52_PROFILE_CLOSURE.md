# Milestone 38 — the complete `(5,2,1,1,1,1)` profile is excluded

M26 reduced the six-prime exponent profile

\[
(5,2,1,1,1,1)
\]

to seven explicit McNew–Setty survivor seeds.

The last three milestones account for all seven:

- M35 lifts five canonical seeds using quantitative `a=4` Clique–Shearer
  margins and the deficiency recurrence;
- M36 directly excludes the exceptional placement
  \(3^5\cdot5\cdot7^2\cdot11\cdot13\cdot17\);
- M37 strengthens the last canonical `p=17` precursor with factorial penalties
  and then lifts it to exponent five.

Therefore

\[
\boxed{
\{a_1,\ldots,a_6\}=\{5,2,1,1,1,1\}
\Longrightarrow
\prod_{i=1}^6p_i^{a_i}\text{ is noncovering}.
}
\]

This is a new profile-level exclusion inside the project.  It is not a complete
solution of the odd distinct covering-system problem.

## 1. Exact seed accounting

The M26 P52 seed list contains seven integers.  M35 returns five distinct
canonical lifted integers.  Its sole unresolved canonical value is exactly

\[
3^5\cdot5^2\cdot7\cdot11\cdot13\cdot17,
\]

which is M37's target.  The unique exceptional M26 exponent placement is
exactly M36's target.  The verifier checks set equality between these seven
certified values and the seven M26 seeds; there is no unaccounted seed.

Since M26's universal coordinate monotonicity sends every other member of the
profile either directly below `R<1` or above one of its exact kill anchors,
closing all seven seeds closes the whole infinite prime family.

## 2. Important frontier correction

Closing a minimal profile does **not** mean all profiles above it are closed:
noncoverage is downward under divisibility, not upward.  Therefore after P52 is
removed from the old M34 antichain, two immediate successor directions become
visible.

Combining the M22 regions, the closed `(4,4,1,1,1,1)` profile, and the newly
closed P52 down-set, the exact componentwise-minimal sorted six-prime exponent
profiles still outside the current exclusion region are

\[
\boxed{
(6,2,1,1,1,1),\qquad
(5,3,1,1,1,1),\qquad
(3,2,2,1,1,1).
}
\]

The three are pairwise incomparable.

To see completeness, let

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1
\]

be outside the closed region.  Then `a_2>=2`.

- If `a_3>=2`, failure of the all-`<=2` M22 region forces `a_1>=3`, so the
  profile dominates `(3,2,2,1,1,1)`.
- If `a_3=1` and `a_2>=3`, failure of the closed `(4,4,1,1,1,1)` down-set
  forces `a_1>=5`, so it dominates `(5,3,1,1,1,1)`.
- If `a_3=1` and `a_2=2`, failure of the newly closed P52 down-set forces
  `a_1>=6`, so it dominates `(6,2,1,1,1,1)`.

Thus these are exactly the new minimal exponent directions.

The structural verifier is `solver/m38_p52_profile_closure.py`, with regression
checks in `solver/test_m38_p52_profile_closure.py`.
