# Milestone 66 — the complete `(4,2,2,1,1,1)` profile is excluded

The six-prime frontier branch

\[
(4,2,2,1,1,1)
\]

is now closed:

\[
\boxed{
\{a_1,\ldots,a_6\}=\{4,2,2,1,1,1\}
\Longrightarrow
\prod_{i=1}^6 p_i^{a_i}\text{ is noncovering}.
}
\]

This is still a six-prime partial theorem, not a complete solution of Erdős
Problem #7.

## 1. Direct-bound reduction

At the minimal odd primes `(3,5,7,11,13,17)` there are 60 exponent
placements.  Exact McNew--Setty evaluation leaves only

```text
(4,1,2,1,2,1)
(4,1,2,2,1,1)
(4,2,1,1,1,2)
(4,2,1,1,2,1)
(4,2,1,2,1,1)
(4,2,2,1,1,1)
```

with `R>=1`; the other 54 are excluded universally by M22 monotonicity.
The largest directly killed value is

\[
\frac{273358304}{273378105}<1.
\]

If the smallest prime is not 3, the common anchor
`(5,7,11,13,17,19)` has `R<1` for all six surviving placements.

## 2. Goodness instead of a global Shearer-box hypothesis

For the first four placements, the old M25 tensor already has positive summed
margin at the minimal prime tuple, but two of the coarse non-special boxes
contain corners outside the Shearer region.  Instead of discarding those
certificates, define

\[
g(q)=
\min\left(
\rho_{\rm full}(q),
\{\rho_C(q^0):\varnothing\ne C\subseteq J\}
\right).
\]

If `g(q)>0`, all non-special coordinate polynomials and the full rho polynomial
are positive, so M39 gives

\[
\Pr(\text{uncovered})\ge \rho_{\rm full}(q)\ge g(q).
\]

If `g(q)<=0`, the trivial lower bound `Pr(uncovered)>=0>=g(q)` applies.
Thus `g` is a quantitative lower bound in every selected fibre.

For fixed non-special charges, minimizing
`g + special M25 penalties` splits into two exact branches:

* the old clipped-quadratic full-rho branch;
* the minimum non-special coordinate polynomial plus the special penalties
  minimized at their lower endpoints.

The remaining function is separately concave, so `2^15` non-special corners
suffice.

Five exact goodness references are positive: the first four placements at
`(3,5,7,11,13,17)`, and the placement `(4,2,1,2,1,1)` at the tail reference
`(3,5,7,11,13,19)`.  The smallest of these five margins is the tail value

\[
\boxed{
\frac{
1462871206901910203799485621
}{
94491081811463835401904000000
}>0.
}
\]

M27 supportwise scaling transports each reference certificate to its whole
coordinatewise larger prime family.

For `(4,2,1,2,1,1)` this leaves only the absolute minimal tuple, because every
other increasing six-prime tuple beginning with 3 dominates
`(3,5,7,11,13,19)`.

## 3. Weighted exact activation for the two hard references

The remaining issue is that a repeated non-special singleton should not be
treated as an arbitrary factor-5 box variable.

For a repeated prime `p^2`, retain its two exact-divisor activation counts
`A,B in {0,1,2,3,4}`:

\[
\frac{q_{\{p\}}}{b_{\{p\}}}
=
1+\frac{pA+B}{p+1}.
\]

The three simple non-special singletons retain exact levels `1,...,5`.  The
other eleven non-special support charges are reduced to endpoints by separate
concavity.

M30 supplies, separately for every exact-divisor activation,

\[
\sum A\le40,
\qquad
\sum {A\choose2}\le18,
\]

while M28 supplies the support first/pair budgets `81` and `197`.

### Canonical `7^2` reference

For

\[
3^4 5^2 7^2 11\cdot13\cdot17
\]

use local non-special order `(7^2,11,13,17)`.  Ten sparse linear support
penalties, 21 pair penalties, and first/second factorial penalties on the five
retained activation variables are used; every coefficient has denominator
1000.

The exact state space is

\[
25\cdot5^3\cdot2^{11}
=
\boxed{6,400,000}.
\]

With

\[
C=\frac{1697}{5000}=0.3394,\qquad Q=10^7,
\]

the standalone integer verifier returns

```text
3396094 3 3 1 1 1 1299
```

and therefore

\[
\boxed{3396094>3394000=QC}
\]

with rigorous floor slack `2094`.

The exact value at the recorded minimizing state is

\[
\frac{
51001982532390154600661059
}{
150177322295567550984000000
}>C.
\]

The special-coordinate cost and added-feature cost are

\[
\frac{10474107609241998}{1108541887578125},
\qquad
\frac{61248773103499}{14189336161000},
\]

so the summed-goodness margin is

\[
\boxed{
\frac{666543097807133}{4434167550312500}>0.
}
\]

Any canonical tuple not beginning with `(3,5,7)` is already directly excluded
by the anchors `(3,7,11,13,17,19)` or `(3,5,11,13,17,19)`.  On the remaining
family the repeated prime is literally 7, so supportwise scaling changes only
the three simple coordinates and preserves the normalized weighted activation
`1+(7A+B)/8`.

### Exceptional `11^2` reference

The sole hard tuple for `(4,2,1,2,1,1)` is

\[
3^4 5^2 7\cdot11^2\cdot13\cdot17.
\]

Use local order `(11^2,7,13,17)`.  The exact verifier again checks 6,400,000
states.  With

\[
C=\frac{1701}{5000}=0.3402,
\]

it returns

```text
3404158 1 1 3 3 2 1127
```

so

\[
\boxed{3404158>3402000=QC}
\]

with floor slack `2158`.

The exact pointwise value at that state is

\[
\frac{20420576104903183899}{59986721722928000000}>C,
\]

and the summed-goodness margin is

\[
\boxed{
\frac{17163381759764987}{21899358105625000}>0.
}
\]

## 4. Conclusion

The proof branches now account for every member of the full profile:

* 54 placements: direct McNew--Setty bound;
* four surviving placements: minimal exact goodness reference + M27 scaling;
* `(4,2,1,2,1,1)`: one weighted hard seed plus a positive tail goodness
  reference;
* canonical `(4,2,2,1,1,1)`: direct off-prefix anchors plus the weighted
  `7^2` reference and scaling.

Hence the complete `(4,2,2,1,1,1)` prime family is noncovering.

Files:

* `solver/m66_p422_profile_closure.py` — exact rational theorem audit;
* `solver/m66_p422_canonical_fast.cpp` — exact 6,400,000-state canonical
  verifier;
* `solver/m66_p422_exceptional_fast.cpp` — exact 6,400,000-state exceptional
  verifier;
* `solver/test_m66_p422_profile_closure.py` — regression checks.
