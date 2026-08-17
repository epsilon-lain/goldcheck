# Milestone 21 — downward closure from M20

Milestone 20 excludes the six-prime exponent profile `(4,2,1,1,1,1)` for
**every** assignment of those exponents to six distinct odd primes.
Divisibility immediately turns that single boundary profile into a whole
exponent-profile down-set.

## Theorem

Let

\[
N=\prod_{i=1}^6 p_i^{a_i}
\]

have six distinct odd prime factors.  Sort the six exponents decreasingly as

\[
b_1\ge b_2\ge\cdots\ge b_6\ge1.
\]

If

\[
\boxed{b_1\le4,\qquad b_2\le2,\qquad b_3=\cdots=b_6=1,}
\]

then `N` is not a covering number.

Equivalently, the following seven sorted exponent profiles are all excluded:

`(1,1,1,1,1,1)`, `(2,1,1,1,1,1)`, `(2,2,1,1,1,1)`,
`(3,1,1,1,1,1)`, `(3,2,1,1,1,1)`, `(4,1,1,1,1,1)`,
`(4,2,1,1,1,1)`.

## Proof

Choose primes carrying the two largest exponents (arbitrarily if there are
ties).  On the same six-prime support define `N_tilde` by raising those two
exponents to `4` and `2`, respectively, and setting all other exponents to `1`.
The displayed hypotheses give

\[
N\mid \widetilde N.
\]

Milestone 20 applies to `N_tilde`, regardless of which two primes carry the
exponents `4` and `2`, so `N_tilde` is noncovering.

If `N` admitted a distinct divisor-modulus covering, every modulus in that
cover would also divide `N_tilde`; the same residue classes would therefore
cover modulo `N_tilde`.  This contradicts M20.  Hence `N` is noncovering.

The divisibility construction and the seven-profile enumeration are checked in
`solver/m21_profile_downset.py`.  This is a consequence of the internal M20
theorem candidate, not a claim of publication novelty and not a solution of the
full odd distinct covering-system problem.
