# Milestone 42 — the complete `(3,2,2,1,1,1)` profile is excluded

M26 reduced the six-prime exponent profile

\[
(3,2,2,1,1,1)
\]

to twelve explicit McNew-Setty survivor seeds.

M40 excludes the six exceptional placements by a quantitative `a=3`
precursor plus the deficiency recurrence.  M41 excludes the six canonical
placements with the weighted two-level law

\[
q_S/b_S=1+(7A_S+B_S)/8
\]

for the repeated coordinate `7^2`.  The two six-element seed sets are disjoint
and their union is exactly the M26 twelve-seed list.

Therefore

\[
\boxed{
\{a_1,\ldots,a_6\}=\{3,2,2,1,1,1\}
\Longrightarrow
\prod_{i=1}^6p_i^{a_i}\text{ is noncovering}.
}
\]

This is a profile-level theorem candidate internal to the project, not a
complete solution of the odd distinct covering-system problem.

## New minimal exponent frontier

Before M42, the exact minimal sorted exponent directions outside the known
noncovering down-set were

\[
(6,2,1,1,1,1),\qquad
(5,3,1,1,1,1),\qquad
(3,2,2,1,1,1).
\]

Closing the third direction exposes three immediate successors.  The exact new
minimal antichain is

\[
\boxed{
(6,2,1,1,1,1),
(5,3,1,1,1,1),
(4,2,2,1,1,1),
(3,3,2,1,1,1),
(3,2,2,2,1,1).
}
\]

To see completeness, let

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1
\]

lie outside the closed region.

If `a_3=1`, the old M38 classification remains: either `a_2>=3`, forcing the
profile to dominate `(5,3,1,1,1,1)`, or `a_2=2`, forcing it to dominate
`(6,2,1,1,1,1)`.

Now suppose `a_3>=2`.  Failure of the all-`<=2` M22 region gives `a_1>=3`.

- If `a_4>=2`, the profile dominates `(3,2,2,2,1,1)`.
- If `a_4=1` and `a_2>=3`, it dominates `(3,3,2,1,1,1)`.
- If `a_4=1` and `a_2=2`, failure of the newly closed P322 down-set forces
  `a_1>=4`, so it dominates `(4,2,2,1,1,1)`.

These five profiles are pairwise incomparable, so the list is exact.

The structural verifier is `solver/m42_p322_profile_closure.py`.
