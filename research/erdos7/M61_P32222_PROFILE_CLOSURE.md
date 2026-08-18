# Milestone 61 — the complete `(3,2,2,2,2,1)` profile is excluded

M60 reduced this profile to the single integer

\[
N_*=3^3\cdot5^2\cdot7^2\cdot11^2\cdot13^2\cdot17
=11497961475.
\]

M61 gives an exact finite certificate for that last seed, so

\[
\boxed{
\{a_1,\ldots,a_6\}=\{3,2,2,2,2,1\}
\Longrightarrow
\prod_i p_i^{a_i}\text{ is noncovering}.
}
\]

Stage on `3^3`, distinguish `5^2`, and retain exact two-level activations for
the repeated singleton supports `{7}`, `{11}`, `{13}`:

\[
\frac{q_{\{p\}}}{b_{\{p\}}}
=1+\frac{pA+B}{p+1},
\qquad A,B\in\{0,1,2,3\}.
\]

The simple singleton `{17}` is kept at its exact integral activation level.
A sparse nonnegative family of linear and pair-moment penalties on the other
non-special charges is added, together with first/second factorial penalties on
the retained activation variables.  M28 gives the `27/63` first/pair budgets;
M30 gives `13/5` factorial caps for each exact-divisor activation.

After clipped-quadratic minimization of the sixteen `5`-containing variables,
the remaining eleven unpenalized support charges are reduced to box endpoints
by separate concavity.  The exact finite state space is

\[
16^3\cdot4\cdot2^{11}
=\boxed{33,554,432}.
\]

With coefficient denominator `1000` and

\[
C=\frac{3367}{10000}=0.3367,
\]

the standalone C++ verifier uses exact `__int128` rational floor arithmetic at
scale `Q=10^7` and returns

```text
3367573 3 2 1 3 0 1 1 843
```

so the rigorous lower minimum is

\[
\boxed{3367573}>3367000=QC,
\]

with integer slack `573>0`.  The minimizing reduced state is

```text
(3,2,1,3,0,1,1,843)
```

and an independent exact Fraction evaluation there is

\[
\frac{232313797012832336720879}
{689850015334077097500000}
>C.
\]

The special-coordinate global cost is

\[
\frac{4089100538208632211}{1295347031947718750},
\]

while all added non-special linear/pair/factorial penalties cost

\[
\frac{4660298627896907}{3188546540179000}.
\]

Therefore the summed quantitative margin is

\[
\boxed{
\frac{61829991701702982}{647673515973859375}>0.
}
\]

The non-special factor-4 box remains in the Clique–Shearer region, with proper
and full coordinate minima `47337/1002001` and `161325/17034017`, and the
special singleton obeys `q_5<=24/25<1`.  M39 therefore converts the positive
summed rho margin into actual uncovered mass.

Files:

- `solver/m61_p32222_hard_seed.py` — exact theorem constants and audit;
- `solver/m61_p32222_hard_seed_fast.cpp` — reproducible 33,554,432-state integer verifier;
- `solver/test_m61_p32222_hard_seed.py` — regression checks.
