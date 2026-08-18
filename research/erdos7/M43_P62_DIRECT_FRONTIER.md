# Milestone 43 — `(6,2,1,1,1,1)` reduces to eight exact seeds

M42 exposes

\[
(6,2,1,1,1,1)
\]

as one of the new minimal exponent directions.  The universal positive
coordinate derivatives of the McNew-Setty bound from M22 make the direct bound
monotone under increasing any prime coordinate.

At the minimal odd primes `(3,5,7,11,13,17)`, the 30 exponent placements have
only two survivors:

\[
(6,2,1,1,1,1),\qquad (6,1,2,1,1,1).
\]

Their exact direct-bound values are

\[
\frac{18573409}{18243225}>1,
\qquad
\frac{8535517}{8513505}>1.
\]

The largest of the other 28 placements is

\[
(6,1,1,2,1,1),\qquad
R=\frac{678016499}{682296615}<1,
\]

so all nonexceptional placements are eliminated uniformly.

For the canonical placement, monotonicity leaves exactly seven prime tuples:

```text
(3,5,7,11,13,17)
(3,5,7,11,13,19)
(3,5,7,11,13,23)
(3,5,7,11,13,29)
(3,5,7,11,13,31)
(3,5,7,11,13,37)
(3,5,7,11,17,19)
```

For the exceptional placement `(6,1,2,1,1,1)`, only the minimal tuple

```text
(3,5,7,11,13,17)
```

survives.  Exact `R<1` kill anchors cover every coordinatewise larger tuple.
Therefore the entire infinite profile is reduced to

\[
\boxed{8}
\]

explicit seeds.

The verifier is `solver/m43_p62_direct_frontier.py`.
