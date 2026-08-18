# Milestone 71 — close exponent placement `(4,2,2,1,2,1)`

Inside the sorted six-prime frontier profile `(4,2,2,2,1,1)`, the fixed
placement

\[
(a_1,\ldots,a_6)=(4,2,2,1,2,1)
\]

is now completely excluded for all increasing six-tuples of distinct odd
primes.

At the minimal tuple this is

\[
N_*=3^4\cdot5^2\cdot7^2\cdot11\cdot13^2\cdot17.
\]

Stage on `3^4` and distinguish the `13^2` coordinate.  Retain the exact
two-level activations of the fixed non-special squares `5^2` and `7^2`:

\[
\frac{q_{\{5\}}}{b_{\{5\}}}=1+\frac{5A_5+B_5}{6},
\qquad
\frac{q_{\{7\}}}{b_{\{7\}}}=1+\frac{7A_7+B_7}{8},
\]

with all four activation variables in `{0,1,2,3,4}`.  The simple singleton
levels for 11 and 17 are kept exactly in `{1,...,5}`; the other eleven
non-special support charges reduce to endpoints by separate concavity.

A sparse nonnegative family of linear, pair, and first/second factorial
penalties is used.  The final coefficients are rational with common
denominator `100000`; the optimization that discovered them is not part of the
proof.

The exact reduced state space has

\[
25^2\cdot5^2\cdot2^{11}=\boxed{32,000,000}
\]

states.  With

\[
Q=10^9,
\qquad
C=\frac{16929}{50000}=0.33858,
\]

the standalone `__int128` verifier returns

```text
338583246 2 2 0 0 1 1 1112
```

and hence

\[
\boxed{338583246>338580000=QC}
\]

with exact floor slack `3246`.

Independent exact evaluation at the recorded minimizing state is

\[
\frac{4269567609502557002629}
{12610096302537327343750}>C.
\]

The exact special-coordinate and added-feature costs are

\[
\frac{9105881382571301}{3058670677562500},
\qquad
\frac{57057870182650423}{5247535562500000},
\]

so the summed-goodness margin is

\[
\boxed{
\frac{428350949784729177}{13624987563687500000}>0.
}
\]

For the fixed placement, direct McNew--Setty anchors with the first, second, or
third prime displaced from `(3,5,7)` are all below one.  Thus every remaining
prime tuple has prefix `(3,5,7)`.  On that family the two exact weighted
non-special squares stay literally `5^2` and `7^2`, while the continuously
treated special square and the two simple coordinates only decrease their
support baselines as primes increase.  M27 supportwise scaling therefore
transports the exact reference certificate to the whole family.

Consequently

\[
\boxed{
(a_1,\ldots,a_6)=(4,2,2,1,2,1)
\Longrightarrow
\prod_i p_i^{a_i}\text{ is noncovering}.
}
\]

This is one exponent-placement theorem inside the sorted P4222 profile; it is
not yet a closure of all nine surviving placements and not a complete solution
of Erdős Problem #7.

Files:

- `solver/m71_p4222_special13_placement.py`
- `solver/m71_p4222_special13_fast.cpp`
- `solver/test_m71_p4222_special13_placement.py`
