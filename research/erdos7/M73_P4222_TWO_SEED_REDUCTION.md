# Milestone 73 — placement `(4,2,1,2,2,1)` reduces to two hard seeds

One of the four placements left open by M72 is

\[
(a_1,\ldots,a_6)=(4,2,1,2,2,1).
\]

M73 reduces its entire increasing-prime family to only two explicit tuples:

\[
\boxed{
(3,5,7,11,13,17),\qquad(3,5,7,11,13,19).
}
\]

Equivalently, only

\[
3^4 5^2 7\,11^2 13^2 17
\quad\text{and}\quad
3^4 5^2 7\,11^2 13^2 19
\]

remain unresolved for this fixed exponent placement.

This is a finite reduction, not a noncovering proof for those two integers and
not a solution of Erdős Problem #7.

## Direct anchors

For this placement the McNew–Setty bound is already below one at

```text
(5,7,11,13,17,19)
(3,7,11,13,17,19)
(3,5,11,13,17,19)
(3,5,7,13,17,19)
(3,5,7,11,19,23)
```

so every unresolved tuple must have prefix `(3,5,7,11)`, and the fifth prime
is either 13 or 17.

## Two exact goodness tail references

For fifth prime 13, the reference

\[
(3,5,7,11,13,23)
\]

has exact M66-style summed-goodness margin

\[
\boxed{
\frac{3572573911745719375023766982387}
{39000910457186880649887440000000}>0.
}
\]

Therefore M27 supportwise scaling closes every tuple with fifth prime 13 and
sixth prime at least 23.

For fifth prime 17, the minimal possible tuple

\[
(3,5,7,11,17,19)
\]

already has exact positive margin

\[
\boxed{
\frac{8641667081450002389773953401647099}
{14896714180047996733231794384000000}>0.
}
\]

and its reference certificate scales to the whole `p5=17` tail.

Thus only sixth primes 17 and 19 in the `p5=13` branch remain.

Files:

- `solver/m73_p4222_open3_two_seed_reduction.py`
- `solver/test_m73_p4222_open3_two_seed_reduction.py`
