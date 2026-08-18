# Milestone 49 — the complete `(5,3,1,1,1,1)` profile is excluded

M47 reduces the six-prime exponent profile

\[
(5,3,1,1,1,1)
\]

to sixteen exact direct-bound survivor seeds in three exponent placements.
M48 was built precisely to remove those three placements.

Therefore

\[
\boxed{
\{a_1,\ldots,a_6\}=\{5,3,1,1,1,1\}
\Longrightarrow
\prod_{i=1}^6p_i^{a_i}\text{ is noncovering}.
}
\]

This is another project-internal six-prime profile theorem candidate.  It is
not a complete resolution of Erdős Problem #7.

## 1. The three M47 branches

M47 leaves:

- three seeds with placement `(3,5,1,1,1,1)`;
- one seed with placement `(5,1,3,1,1,1)`;
- twelve seeds with placement `(5,3,1,1,1,1)`.

For the first branch, stage on `3^3` and distinguish the finite power `5^5`.
M48 certifies the stronger reference baseline

\[
x_5(\infty)=1/4,
\]

with positive quantitative margin

\[
\frac{7030993631127}{20684163500000}>0.
\]

All three simple-prime tuples are coordinatewise no smaller than the M48
reference `(7,11,13,17)`, so baseline inflation applies.

For the unique `(5,1,3,1,1,1)` seed, stage on `3^5` and distinguish `7^3`.
M48 proves the stronger infinite-prime-7 reference

\[
x_7(\infty)=1/6
\]

with summed-goodness margin

\[
\frac{92070538867211}{53187849000000}>0.
\]

The non-special tuple is exactly `(5,11,13,17)`.

For the twelve canonical `(5,3,1,1,1,1)` seeds, stage on `3^5`, distinguish
`5^3`, and use M48's infinite prime-5 reference.  Its exact summed-goodness
margin is

\[
\frac{376679506003531}{289578289000000}>0.
\]

All twelve non-special simple tuples are coordinatewise no smaller than
`(7,11,13,17)`, including the two off-family tuples `(7,11,17,19)` and
`(7,11,17,23)`.

Thus every one of M47's sixteen seeds is noncovering.  M47's monotone direct
reduction then closes the complete infinite prime family.

## 2. New minimal exponent frontier

Before M49, the minimal antichain was

\[
(5,3,1,1,1,1),
(4,2,2,1,1,1),
(3,3,2,1,1,1),
(3,2,2,2,1,1).
\]

Closing the first profile exposes two successor directions.  The exact new
frontier is

\[
\boxed{
(6,3,1,1,1,1),
(5,4,1,1,1,1),
(4,2,2,1,1,1),
(3,3,2,1,1,1),
(3,2,2,2,1,1).
}
\]

Indeed, in the `a_3=1` branch, M45 already removes `a_2=2`.  If `a_2=3`,
failure of the newly closed P53 down-set forces `a_1>=6`, giving `(6,3,...)`.
If `a_2>=4`, failure of the old P44 down-set forces `a_1>=5`, giving
`(5,4,...)`.  The three directions with `a_3>=2` are unchanged.

The verifier is `solver/m49_p53_profile_closure.py`.
