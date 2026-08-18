# Milestone 34 — the minimal six-prime frontier collapses to two profiles

M33 closes the complete profile

\[
(4,4,1,1,1,1).
\]

Combining this with the broad M22 exclusion regions, the exact
componentwise-minimal sorted six-prime exponent profiles still outside the
current down-set are now only

\[
\boxed{
(5,2,1,1,1,1),\qquad
(3,2,2,1,1,1).
}
\]

The former M26 frontier `(4,4,1,1,1,1)` has disappeared completely.

## Why these two are exact

Let

\[
a_1\ge a_2\ge\cdots\ge a_6\ge1.
\]

The current profile-level results already exclude:

1. every profile with `a_1<=2`;
2. every profile with `a_2=1`, with `a_1` arbitrary;
3. every profile componentwise dominated by `(4,4,1,1,1,1)`.

Take a profile outside all three regions.  Then `a_2>=2`.

- If `a_1>=5`, it dominates `(5,2,1,1,1,1)`.
- Otherwise `a_1<=4`.  Since it is not dominated by `(4,4,1,1,1,1)`, one
  must have `a_3>=2`.  Since the all-`<=2` region is already excluded, one also
  has `a_1>=3`.  Therefore it dominates `(3,2,2,1,1,1)`.

These two profiles are incomparable, so they form the exact minimal antichain.

M26 already reduced them by universal McNew--Setty monotonicity to

\[
7\quad\text{and}\quad12
\]

explicit seeds.  Hence the finite direct-bound frontier after M33 is

\[
\boxed{19\text{ seeds in total}.}
\]

This is a frontier reduction only, not a proof that any of those 19 seeds
covers.  The next natural target is the seven-seed `(5,2,1,1,1,1)` branch,
where staging on `3^5` gives integer activation variables on the four simple
post-stage coordinates and invites an `a=5` version of the M32/M33 factorial
goodness certificate.
