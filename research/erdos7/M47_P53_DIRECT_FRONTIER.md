# Milestone 47 — `(5,3,1,1,1,1)` reduces to sixteen exact seeds

M46 leaves `(5,3,1,1,1,1)` as one of four minimal exponent directions.  At
the minimal odd primes `(3,5,7,11,13,17)`, only three of the 30 exponent
placements survive the monotone McNew--Setty direct bound:

\[
(3,5,1,1,1,1),\qquad
(5,1,3,1,1,1),\qquad
(5,3,1,1,1,1).
\]

Their exact direct-bound values are respectively

\[
\frac{28445708}{28153125},\qquad
\frac{338863268}{337702365},\qquad
\frac{3455656}{3378375},
\]

all greater than one.  The other 27 placements are uniformly below one.

Coordinate monotonicity then leaves exactly sixteen prime tuples:

- 3 seeds for placement `(3,5,1,1,1,1)`, with final prime `17,19,23`;
- 1 seed for placement `(5,1,3,1,1,1)`, at the minimal prime tuple;
- 12 seeds for canonical placement `(5,3,1,1,1,1)`: final prime
  `17,19,23,29,31,37,41,43,47,53` and the two off-family simple tuples
  `(7,11,17,19)` and `(7,11,17,23)`.

A small exact antichain of `R<1` boundary anchors covers every coordinatewise
larger prime tuple.  Hence the entire infinite profile is reduced to

\[
\boxed{16}
\]

explicit seeds.

The verifier is `solver/m47_p53_direct_frontier.py`.
