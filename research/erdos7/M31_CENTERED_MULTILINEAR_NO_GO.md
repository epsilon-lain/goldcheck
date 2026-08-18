# Milestone 31 — exact barrier for the centered distinct-variable cone

For

\[
N_0=3^4\cdot5^4\cdot7\cdot11\cdot13\cdot17,
\]

freeze the sixteen prime-5 supports to the M25 treatment.  On the fifteen
non-5 supports, allow every nonnegative centered multilinear penalty

\[
c_A\prod_{S\in A}(q_S-b_S),
\qquad c_A\ge0,
\]

for every nonempty set `A` of distinct support variables, through order 15.
Charge an order-`t` monomial by the M30 centered budget

\[
M(4,t)\prod_{S\in A}b_S.
\]

M31 gives an exact rational dual distribution on 124 non-5 box corners with
common denominator `5120`.  It has total mass `41`, satisfies all
`2^15-1=32767` centered moment constraints, and yields the strictly negative
dual gap

\[
\boxed{
-\frac{459546958093873554501492643621474782569}
{12137705808208147451731457910900000000000}<0.
}
\]

Hence this entire centered **distinct-variable** multilinear cone is
insufficient.

The dual simultaneously pinpoints the escape direction.  For every one of the
fifteen variables its repeated centered square moment equals

\[
160,
\]

while the valid M30 repeated-support cap is only

\[
M(4,2)=76.
\]

Thus every repeated-square constraint is violated by the dual by

\[
\boxed{84}.
\]

This is why M32 changes mechanism and uses repeated-support/factorial powers
rather than adding still more distinct-variable cross terms.

Exact implementation: `solver/m31_centered_multilinear_no_go.py`.
