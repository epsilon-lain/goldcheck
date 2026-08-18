# Milestone 41 — exponent frontier after closing `(3,2,2,1,1,1)`

M40 closes the full six-prime profile

\[
(3,2,2,1,1,1).
\]

Adding its divisibility down-set to the regions already closed by M22, M33 and
M37 changes the minimal sorted exponent frontier.  The new antichain is

\[
\boxed{
(6,2,1,1,1,1),\quad
(5,3,1,1,1,1),\quad
(4,2,2,1,1,1),\quad
(3,3,2,1,1,1),\quad
(3,2,2,2,1,1).
}
\]

These five profiles are pairwise incomparable.

## Completeness of the five directions

Let

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1
\]

be outside the current exclusion down-set.  The M22 one-repeat region forces
`a_2>=2`.

If `a_3=1`, the old M38 argument remains unchanged:

- `a_2=2` forces `a_1>=6`, hence the profile dominates `(6,2,1,1,1,1)`;
- `a_2>=3` forces `a_1>=5`, hence it dominates `(5,3,1,1,1,1)`.

Now suppose `a_3>=2`.  Failure of M22's all-exponents-at-most-two region gives
`a_1>=3`.

- If `a_4>=2`, the profile dominates `(3,2,2,2,1,1)`.
- If `a_4=1` and `a_2>=3`, it dominates `(3,3,2,1,1,1)`.
- If `a_4=1` and `a_2=2`, then `a_3=2`; failure of the newly closed
  `(3,2,2,1,1,1)` down-set forces `a_1>=4`, so the profile dominates
  `(4,2,2,1,1,1)`.

Thus every still-open sorted six-prime exponent profile dominates one of the
five displayed profiles, and none of those five lies below another.

This is a structural frontier statement only.  It does not assert that any of
the five profiles is coverable, and it does not resolve Erdős Problem #7.

The verifier is `solver/m41_frontier_after_p322.py`, with regression checks in
`solver/test_m41_frontier_after_p322.py`.
