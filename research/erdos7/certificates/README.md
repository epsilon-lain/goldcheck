# Exact non-covering certificates

Each file below records an exact lower bound on the deficiency
`δ(N) = N − r(N)`, obtained by chaining the proved lemmas in `../NOTES.md`:

* the square-free CRT/Hall bound (McNew–Setty Lemma 4.10), and
* the deficiency recurrence `δ(p^a M) ≥ p·δ(N/p) − σ(M)`;

and, for `51975`, the **full** prime-power form of Lemma 4.10
(`../NOTES.md` Section 8).

A positive lower bound proves the integer is **not** a covering number, hence
not a counterexample to the Erdős–Selfridge odd covering problem.

| N     | factorisation          | `δ(N) ≥` |
|-------|------------------------|----------|
| 945   | 3³ · 5 · 7             | 123      |
| 10395 | 3³ · 5 · 7 · 11        | 360      |
| 12285 | 3³ · 5 · 7 · 13        | 606      |
| 17325 | 3² · 5² · 7 · 11       | 312      |
| 51975 | 3³ · 5² · 7 · 11       | 4295     |

Independent verification:

```bash
cd solver
python -c "from certificate import verify_certificates; print(verify_certificates())"
pytest test_full_bound.py::test_51975_is_excluded_by_full_bound -q
pytest test_certificate.py -q
```

The square-free base values are pure integer arithmetic (no external solver);
the recurrence is likewise exact integer arithmetic.  The `covering.py` and
`milp.py` modules provide an independent SAT/MILP cross-check for small `N`.

## Higher-order insufficiency certificate

`omega6_overlap.json` is a different kind of artifact: an exact **dual**
certificate (171 rational weights) proving that the pair+triple overlap basis
cannot exclude the six-prime corner `{3,5,7,11,13,17}`.  Its optimal correction
is `F* = 9997/161280`, giving `g = g1 − F* = 349343/161280 > 2`; see
`../NOTES.md` Section 14.  It is verified with exact rational arithmetic by
`../solver/higher_overlap.py::verify_certificate` and
`../solver/test_higher_overlap.py` (no floating point, no external solver in the
trusted path).

`omega6_order4_overlap.json` extends the same insufficiency to the full
`|J| ≤ 4` basis (pairs + triples + quadruples).  Its `235`-weight dual certificate
proves the order-4 optimum is `F* = 24457/394240`, hence
`g = g1 − F* = 2561789/1182720 > 2`, with residual gap `196349/1182720`.  It is
verified by `../solver/higher_overlap.py::verify_order4_certificate` (exact
`Fraction` arithmetic).  See `../NOTES.md` Section 15.

`omega6_star.json` is the one-coordinate star-collision certificate: for each
prime coordinate `i` it stores an exactly feasible atom distribution (primal) and
an exactly feasible star-LP dual, both with `Fraction` values, proving the exact
star lower envelope `1/105, 307/6720, 1/560, 0, 0, 0`.  These give the rigorous
insufficiency bound `F_star* ≤ 347/2688`, hence `g_star ≥ 2821/1344 > 2`
(residual gap `≥ 133/1344`).  Verified by
`../solver/star_collision.py::verify_star`.  See `../NOTES.md` Section 16.
