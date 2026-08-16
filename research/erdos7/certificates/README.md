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
