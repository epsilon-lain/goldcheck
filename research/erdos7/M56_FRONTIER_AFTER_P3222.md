# Milestone 56 — frontier after closing `(3,2,2,2,1,1)`

M55 removes the M54 direction

\[
(3,2,2,2,1,1).
\]

The exact minimal sorted six-prime exponent frontier becomes

\[
\boxed{
(4,2,2,1,1,1),\qquad
(3,3,2,1,1,1),\qquad
(3,2,2,2,2,1).
}
\]

The first two directions survive unchanged.  The old four-repeated-coordinate
direction moves one step deeper, from three twos after the leading `3` to four.

To see completeness, use M53 first: every still-open profile has at least three
repeated coordinates.  If there are exactly three, the M54 argument gives
`(4,2,2,1,1,1)` or `(3,3,2,1,1,1)`.  If there are at least four and either the
largest exponent is at least `4` or the second largest is at least `3`, one of
those same two profiles already lies below it.  The only remaining case begins
`(3,2,2,2,...)`; failure of the newly closed M55 down-set forces the fifth
exponent to be at least `2`, producing `(3,2,2,2,2,1)`.

The structural verifier is `solver/m56_frontier_after_p3222.py` with regression
checks in `solver/test_m56_frontier_after_p3222.py`.
