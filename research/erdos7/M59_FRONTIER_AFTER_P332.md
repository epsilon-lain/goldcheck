# Milestone 59 — corrected frontier after closing `(3,3,2,1,1,1)`

M58 closes `(3,3,2,1,1,1)`.  Combining this with M53, M55 and the original
M22 all-exponents-at-most-two theorem gives the exact minimal sorted six-prime
exponent frontier

\[
\boxed{
(4,2,2,1,1,1),\quad
(3,3,3,1,1,1),\quad
(3,3,2,2,1,1),\quad
(3,2,2,2,2,1).
}
\]

M59 also repairs a bookkeeping issue in an older frontier helper: the helper's
predicate did not explicitly include M22's region where **all six exponents are
at most two**, even though that theorem had already been proved.  The current
frontier predicate checks the case `(2,2,2,2,2,2)` explicitly.

Completeness is short.  A still-open profile has at least three repeated
coordinates and largest exponent at least `3`.  If the largest exponent is at
least `4`, it dominates `(4,2,2,1,1,1)`.  Otherwise it begins with `3`.  If the
next two exponents are at least `3`, it dominates `(3,3,3,1,1,1)`.  If only the
second is at least `3`, failure of the newly closed `(3,3,2,1,1,1)` down-set
forces a fourth repeated coordinate, giving `(3,3,2,2,1,1)`.  Finally, if the
second exponent is `2`, failure of the M55 `(3,2,2,2,1,1)` down-set forces a
fifth repeated coordinate, giving `(3,2,2,2,2,1)`.

The verifier is `solver/m59_frontier_after_p332.py`; regression checks are in
`solver/test_m59_frontier_after_p332.py`.
