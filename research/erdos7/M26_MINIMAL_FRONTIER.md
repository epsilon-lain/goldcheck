# Milestone 26 — the exact minimal exponent frontier after M25

M25 closes the complete six-prime profile

\[
(4,3,1,1,1,1).
\]

Together with the profile-level regions already supplied by M22, this lets us
identify the **exact componentwise-minimal exponent profiles still outside the
current six-prime exclusion region**.

The answer is

\[
\boxed{
(5,2,1,1,1,1),\qquad
(4,4,1,1,1,1),\qquad
(3,2,2,1,1,1).
}
\]

This corrects the earlier informal frontier description: the first profile with
a third repeated prime is `(3,2,2,1,1,1)`, not `(3,3,2,1,1,1)`.

M26 then applies the universal McNew–Setty coordinate monotonicity from M22 to
reduce these three infinite profile families to **30 explicit direct-bound
seeds in total**.

This is a frontier census, not a proof that any of the 30 seeds covers.

## 1. Why exactly these three profiles are minimal

Write a sorted exponent profile as

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1.
\]

Before M26 we already know, at the profile level:

1. if `a_1<=2`, M22 directly excludes the number;
2. if `a_2=1`, M22 excludes the entire one-repeated-prime ray, with `a_1`
   arbitrary;
3. if
   \[
   (a_1,\ldots,a_6)\le(4,3,1,1,1,1)
   \]
   componentwise, M25 plus divisibility excludes the number.

Now take a profile outside all three regions.  Then `a_2>=2`.  Failure of the
M25 down-set means at least one of

\[
a_1\ge5,\qquad a_2\ge4,\qquad a_3\ge2
\]

holds.  In the first case the profile dominates `(5,2,1,1,1,1)`; in the
second it dominates `(4,4,1,1,1,1)`; in the third, since the profile is not in
the all-`<=2` region, `a_1>=3`, so it dominates `(3,2,2,1,1,1)`.

The three displayed profiles are pairwise incomparable, hence they are exactly
the minimal antichain.

## 2. Universal direct monotonicity

M22 proves that for six odd prime coordinates

\[
R=e_1-e_3-e_4+2e_5+9e_6
\]

has

\[
\frac{\partial R}{\partial x_i}\ge\frac{719}{1440}>0
\]

throughout the full positive-exponent domain.  Since

\[
x(p,a)=\sum_{j=1}^a p^{-j}
\]

decreases as the prime `p` increases, every fixed exponent placement is worst
at the coordinatewise-smallest allowed ordered prime tuple.

This turns each infinite prime family below into a finite exact placement scan
plus a handful of monotone `R<1` anchors.

## 3. Profile `(5,2,1,1,1,1)` — only 7 seeds

There are 30 placements of exponents `5` and `2`.  At
`(3,5,7,11,13,17)`, only

\[
(5,2,1,1,1,1),\qquad(5,1,2,1,1,1)
\]

have `R>=1`.  The largest of the other 28 is

\[
(5,1,1,2,1,1),\qquad
R=\frac{2655728}{2675673}<1.
\]

The canonical placement reduces to exactly

\[
\begin{aligned}
&(3,5,7,11,13,P),\quad P=17,19,23,29,31,\\
&(3,5,7,11,17,19),
\end{aligned}
\]

with exponent placement `(5,2,1,1,1,1)`.  The second exceptional placement
leaves only `(3,5,7,11,13,17)` with exponents `(5,1,2,1,1,1)`.

Thus this whole profile is reduced to

\[
\boxed{7\text{ seeds}.}
\]

For example, on the canonical branch the tail anchors

\[
(3,5,7,11,13,37),\quad
(3,5,7,11,17,23),\quad
(3,5,7,11,19,23)
\]

already have `R<1`, and earlier-coordinate deviations are killed by their
corresponding minimal anchors.

## 4. Profile `(4,4,1,1,1,1)` — only 11 seeds

Of the 15 placements of the two fourth powers, only

\[
(4,4,1,1,1,1),\qquad(4,1,4,1,1,1)
\]

survive the minimal-prime direct scan.  The largest killed placement is

\[
(4,1,1,4,1,1),\qquad
R=\frac{1815414127}{1834619787}<1.
\]

The canonical branch reduces to

\[
(3,5,7,11,13,P),\quad
P=17,19,23,29,31,37,41,43,
\]

and

\[
(3,5,7,11,17,P),\quad P=19,23.
\]

The noncanonical exceptional placement leaves only the minimal prime tuple.
Hence

\[
\boxed{11\text{ seeds}.}
\]

The first missing tail values are certified by the exact anchors
`(3,5,7,11,13,47)`, `(3,5,7,11,17,29)`, and
`(3,5,7,11,19,23)`, all with `R<1`.

## 5. Profile `(3,2,2,1,1,1)` — only 12 seeds

This is the genuinely new third-repeated-prime frontier.  There are 60 labelled
placements.  Only four survive at the six smallest odd primes:

\[
\begin{aligned}
&(3,2,2,1,1,1),\\
&(3,2,1,2,1,1),\\
&(3,2,1,1,2,1),\\
&(3,2,1,1,1,2).
\end{aligned}
\]

The largest of the other 56 placements is

\[
(3,1,2,2,1,1),\qquad
R=\frac{1300549}{1310309}<1.
\]

The first exceptional placement leaves six prime tuples:

\[
(3,5,7,11,13,P),\quad P=17,19,23,29,31,
\]

plus `(3,5,7,11,17,19)`.  Each of the other three exceptional placements
leaves only the two tuples

\[
(3,5,7,11,13,17),\qquad(3,5,7,11,13,19).
\]

Therefore

\[
\boxed{12\text{ seeds}.}
\]

## 6. New frontier size

Combining the three minimal profiles:

\[
\boxed{7+11+12=30}
\]

explicit seeds remain after the universal direct-bound reduction.

The exact verifier is `solver/m26_minimal_frontier.py`, with regression tests in
`solver/test_m26_minimal_frontier.py`.  The key next mathematical task is now
sharper than the earlier vague list of profiles: adapt the M25 cross-support
second-moment machinery to these 30 seeds, beginning with the seven-seed
`(5,2,1,1,1,1)` branch or the eleven-seed `(4,4,1,1,1,1)` branch.

As usual, this is an internal rigorous frontier reduction pending independent
full-suite execution and literature/novelty review; it does not solve the odd
distinct covering-system problem.
