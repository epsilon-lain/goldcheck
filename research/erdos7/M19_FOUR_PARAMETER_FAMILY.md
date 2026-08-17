# Milestone 19 — four-parameter six-prime exclusion family

Milestone 18 excludes

\[
3^4\cdot5^2\cdot7\cdot p\cdot q\cdot r
\]

for every three distinct primes `11 <= p < q < r`.  One more monotonicity step
removes the fixed prime `7` as well.

## Theorem

Let `p<q<r<s` be distinct primes with `p>=7`. Then

\[
\boxed{3^4\cdot5^2\cdot p\cdot q\cdot r\cdot s}
\]

is not a covering number for a distinct covering system.

Thus the four primes beyond `3,5` are completely free, subject only to being
distinct primes at least `7`.

## Proof split

If `p=7`, then `q,r,s` are distinct primes at least `11`, so this is exactly
Milestone 18.

It remains to treat `p>=11`.  The McNew–Setty six-coordinate bound is

\[
R=e_1-e_3-e_4+2e_5+9e_6
\]

at

\[
x=\left(\frac{40}{81},\frac6{25},\frac1p,\frac1q,\frac1r,\frac1s\right).
\]

As in M18,

\[
\frac{\partial R}{\partial x_i}
\ge1-e_2(y)-e_3(y).
\]

On the larger box where all four variable prime reciprocals are at most `1/7`,
any five-coordinate remainder is bounded after sorting by

\[
U=\left(\frac{40}{81},\frac6{25},\frac17,\frac17,\frac17\right),
\]

and

\[
e_2(U)+e_3(U)=\frac{137266}{231525}.
\]

Hence

\[
\boxed{\frac{\partial R}{\partial x_i}\ge
\frac{94259}{231525}>0.}
\]

So increasing any prime decreases `R`.

For `p>=11`, distinctness gives

\[
p\ge11,\quad q\ge13,\quad r\ge17,\quad s\ge19.
\]

The minimal anchor already satisfies

\[
R(11,13,17,19)=\frac{276127}{289575}
=1-\frac{13448}{289575}<1.
\]

Therefore every `p>=11` case is killed by the direct bound, while `p=7` is M18.
This proves the theorem.

Exact Fraction verification is in `solver/m19_four_parameter_family.py`.
As before, this is an internal theorem candidate until literature/novelty review;
it is not a solution of the full odd distinct covering-system problem.
