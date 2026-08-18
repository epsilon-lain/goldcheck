# Milestones 68–70 — the canonical `(4,2,2,2,1,1)` placement is excluded

This checkpoint treats the canonical exponent placement

\[
(p_1,p_2,p_3,p_4,p_5,p_6)^{(4,2,2,2,1,1)}.
\]

It does **not** yet close all nine exponent placements in the sorted profile
`(4,2,2,2,1,1)`.

## M68: the `(3,5,7,11,13,17)` reference

Stage on `3^4`, distinguish `5^2`, and keep the exact two-level activations of
`7^2` and `11^2`:

\[
\frac{q_{\{7\}}}{b_{\{7\}}}=1+\frac{7A_7+B_7}{8},
\qquad
\frac{q_{\{11\}}}{b_{\{11\}}}=1+\frac{11A_{11}+B_{11}}{12}.
\]

The simple singleton levels for 13 and 17 are kept exactly.  The eleven other
non-special support charges reduce to factor-5 endpoints by separate
concavity.  A cutting-plane LP was used only to discover sparse nonnegative
coefficients; the final certificate is rational and does not rely on the LP.

The exact state space is

\[
25^2\,5^2\,2^{11}=\boxed{32,000,000}.
\]

With coefficient denominator `100000`, scale `Q=10^9`, and

\[
C=\frac{69699}{200000}=0.348495,
\]

the exact `__int128` verifier returns

```text
348498368 0 0 0 0 1 1 1024
```

so

\[
\boxed{348498368>348495000=QC}
\]

with floor slack `3368`.  Independent exact evaluation at the recorded state is

\[
\frac{140304882616225190852074066798016594047}
{402598364961488706245123434706160000000}>C.
\]

The exact global special and added-feature costs are

\[
\frac{5146853782690471671}{536534273587812500},
\qquad
\frac{11425137346771651}{2452728107830000},
\]

hence the summed-goodness margin is

\[
\boxed{
\frac{320918421385649239}{8584548377405000000}>0.
}
\]

## M69: the `(3,5,7,13,17,19)` reference

The same coefficient family is reused with weighted singleton coordinates
`7^2,13^2` and simple coordinates `17,19`.  Again there are exactly
`32,000,000` reduced states.

Take

\[
C=\frac{17017}{50000}=0.34034.
\]

The exact verifier returns

```text
340352099 4 4 0 0 1 1 1371
```

so the floor slack is `12099`.  The exact value at the recorded state is

\[
\frac{97400023463548344087}{286174284246760000000}>C,
\]

and the summed-goodness margin is

\[
\boxed{
\frac{1757511727763981557}{2235736595677812500}>0.
}
\]

## M70: close the whole canonical placement

The direct McNew–Setty bound is already below one at the four monotone anchors

\[
(5,7,11,13,17,19),\quad
(3,7,11,13,17,19),\quad
(3,5,11,13,17,19),\quad
(3,5,7,17,19,23),
\]

for the exponent placement `(4,2,2,2,1,1)`.

Therefore every surviving prime tuple begins with `(3,5,7)` and has fourth
prime either 11 or 13.  If it is 11, M68 supportwise scaling changes only the
two simple coordinates; the weighted `7^2/11^2` activation laws remain exact.
If it is 13, the analogous M69 scaling applies.  If the fourth prime is at
least 17, the last direct anchor already excludes the tuple.

Consequently

\[
\boxed{
3<p_1<\cdots<p_6\text{ odd primes},\quad
(a_1,\ldots,a_6)=(4,2,2,2,1,1)
\Longrightarrow
\prod_i p_i^{a_i}\text{ is noncovering}.
}
\]

This is a single exponent-placement theorem inside the six-prime frontier, not
a complete solution of Erdős Problem #7 and not yet a closure of the full
sorted profile `(4,2,2,2,1,1)`.

Files:

- `solver/m68_p4222_canonical_seed.py`
- `solver/m68_p4222_canonical_fast.cpp`
- `solver/m69_p4222_canonical_tail.py`
- `solver/m69_p4222_canonical_tail_fast.cpp`
- `solver/m70_p4222_canonical_placement.py`
- `solver/test_m68_p4222_canonical_seed.py`
- `solver/test_m70_p4222_canonical_placement.py`
