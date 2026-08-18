# Milestone 62 — frontier after closing `(3,2,2,2,2,1)`

M61 closes the complete six-prime exponent profile

\[
(3,2,2,2,2,1).
\]

Combining that new down-set with the exact M59 frontier leaves the componentwise-minimal sorted profiles

\[
\boxed{
(4,2,2,1,1,1),\quad
(3,3,3,1,1,1),\quad
(3,3,2,2,1,1),\quad
(3,2,2,2,2,2).
}
\]

Only the last M59 branch changes.  If a still-open sorted profile begins with `3,2,2`, then M61 rules out every case whose sixth exponent is `1`; hence all five remaining coordinates must have exponent at least two, giving the new minimal direction `(3,2,2,2,2,2)`.

The structural verifier is `solver/m62_frontier_after_m61.py`, with regression checks in `solver/test_m62_frontier_after_m61.py`.
