# Milestone 54 — every remaining six-prime profile has at least three repeated primes

M53 closes every exponent profile with exactly two repeated prime coordinates;
M22 and its down-set already cover zero or one repeated coordinate.  Therefore
the six-prime problem has crossed a structural threshold:

\[
\boxed{\text{any still-unexcluded six-prime profile has at least three exponents }\ge2.}
\]

Combining that fact with the complete P322 profile closure from M42 leaves the
exact minimal componentwise frontier

\[
\boxed{
(4,2,2,1,1,1),
(3,3,2,1,1,1),
(3,2,2,2,1,1).
}
\]

Indeed, write

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1.
\]

An outside profile has `a_3>=2`, and `a_1>=3` because all exponents at most two
are already excluded by M22.

- If `a_4>=2`, it dominates `(3,2,2,2,1,1)`.
- If `a_4=1` and `a_2>=3`, it dominates `(3,3,2,1,1,1)`.
- If `a_4=1` and `a_2=2`, then failure of the closed
  `(3,2,2,1,1,1)` down-set forces `a_1>=4`, so it dominates
  `(4,2,2,1,1,1)`.

The three profiles are pairwise incomparable, so this antichain is exact.

This is still not a complete solution of Erdős Problem #7, nor even yet a
complete exclusion of all six-prime possibilities.  It does, however, remove
the entire two-repeated-coordinate universe and concentrates the remaining
six-prime campaign on genuinely multi-repeated CRT geometry.

The verifier is `solver/m54_three_repeated_frontier.py`.
