# Milestone 65 — the minimal six-prime exponent frontier collapses to three branches

M64 closes

\[
(3,2,2,2,2,2).
\]

Unlike earlier closures, this branch does not reveal a new incomparable successor.  Any larger sorted profile either raises the leading exponent to at least `4`, hence dominates `(4,2,2,1,1,1)`, or raises a later exponent to `3`, hence enters one of the existing `(3,3,3,1,1,1)` or `(3,3,2,2,1,1)` branches.

Therefore the exact componentwise-minimal sorted six-prime exponent frontier is now

\[
\boxed{
(4,2,2,1,1,1),\qquad
(3,3,3,1,1,1),\qquad
(3,3,2,2,1,1).
}
\]

Equivalently, any still-open six-prime exponent profile dominates at least one of these three.

The structural verifier is `solver/m65_frontier_after_m64.py`, with regression checks in `solver/test_m65_frontier_after_m64.py`.
