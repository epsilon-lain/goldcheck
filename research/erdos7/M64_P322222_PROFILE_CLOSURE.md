# Milestone 64 — the complete `(3,2,2,2,2,2)` profile is excluded

M63 reduces the profile to the single hard integer

\[
N_*=3^3\cdot5^2\cdot7^2\cdot11^2\cdot13^2\cdot17^2
=195465345075.
\]

M64 closes that seed by retaining the exact two-level activations of all four non-special repeated singleton coordinates after staging on `3^3` and distinguishing `5^2`:

\[
\frac{q_{\{p\}}}{b_{\{p\}}}
=1+\frac{pA_p+B_p}{p+1},
\qquad p\in\{7,11,13,17\},\quad A_p,B_p\in\{0,1,2,3\}.
\]

The M61 sparse linear/pair feature family is reused.  First/second factorial penalties are retained on all eight exact-divisor activation variables; the new `17^2` coefficient quadruple is

```text
(6,1,4,1)/1000.
```

The remaining eleven non-special support charges are reduced to endpoints by separate concavity.  The exact finite state space is

\[
16^4\,2^{11}=\boxed{134217728}.
\]

The standalone `__int128` verifier at scale `Q=10^7` returns

```text
3359197 2 1 1 3 1 2 1 0 335
```

so with

\[
C=\frac{3359}{10000}
\]

we have the rigorous floor bound

\[
\boxed{3359197>3359000=QC},
\]

with integer slack `197`.  At the minimizing recorded state the independent exact value is

\[
\frac{3521116425483227803279}
{10481948182520940125000}>C.
\]

The special-coordinate global cost is

\[
\frac{1188734751673549101999}
{374355292232890718750},
\]

and the complete non-special linear/pair/factorial cost is

\[
\frac{3536143347274623257}
{2395873870290500600}.
\]

Hence the summed quantitative rho margin is

\[
\boxed{
\frac{5481727876909402311}
{106958654923683062500}>0.
}
\]

The full non-special factor-4 box remains inside the Clique–Shearer region: the proper and full coordinate minima are respectively

\[
\frac{47337}{1002001}>0,
\qquad
\frac{2099121}{289578289}>0.
\]

Also `q_5<=4(6/25)=24/25<1`, so the M39 quantitative completion argument converts the positive summed rho margin into actual uncovered mass.

Therefore

\[
\boxed{
\{a_1,\ldots,a_6\}=\{3,2,2,2,2,2\}
\Longrightarrow
\prod_i p_i^{a_i}\text{ is noncovering}.
}
\]

Files:

- `solver/m64_p322222_hard_seed.py` — exact theorem constants and audit;
- `solver/m64_p322222_hard_seed_fast.cpp` — reproducible 134,217,728-state exact integer verifier;
- `solver/test_m64_p322222_hard_seed.py` — regression checks.
