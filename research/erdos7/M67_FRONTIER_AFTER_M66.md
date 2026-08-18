# Milestone 67 — exact frontier after closing `(4,2,2,1,1,1)`

M66 closes the former frontier branch

\[
(4,2,2,1,1,1).
\]

The closure does **not** simply reduce the M65 three-branch frontier to two:
three immediate successor directions become visible above the newly closed
P422 down-set.  Combining M22, M53, M55, M58, M61, M64 and M66, the exact
componentwise-minimal sorted six-prime exponent profiles still outside the
current exclusion region are

\[
\boxed{
(5,2,2,1,1,1),\quad
(4,3,2,1,1,1),\quad
(4,2,2,2,1,1),\quad
(3,3,3,1,1,1),\quad
(3,3,2,2,1,1).
}
\]

These five profiles are pairwise incomparable.

Completeness follows directly from sorting.  Any still-open profile has at
least three repeated coordinates and leading exponent at least 3.  If the
leading exponent is at least 5 it dominates `(5,2,2,1,1,1)`.  If it equals 4,
then either the second exponent is at least 3, giving `(4,3,2,1,1,1)`, or the
second is 2; failure of the M66 P422 down-set then forces a fourth repeated
coordinate, giving `(4,2,2,2,1,1)`.  Finally, if the leading exponent is 3,
M64 has already closed the entire `(3,2,2,2,2,2)` box, so the second exponent
must be at least 3.  A third exponent at least 3 gives `(3,3,3,1,1,1)`;
otherwise failure of the M58 `(3,3,2,1,1,1)` down-set forces a fourth repeated
coordinate, giving `(3,3,2,2,1,1)`.

The structural verifier is `solver/m67_frontier_after_m66.py`, with regression
checks in `solver/test_m67_frontier_after_m66.py`.
