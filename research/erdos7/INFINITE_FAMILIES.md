# Infinite excluded families (Milestone 2)

Milestone 2 turns the finite certificates of Milestone 1 into proved infinite
families of non-covering numbers.  Every family below is a formal consequence of

* **McNew–Setty Lemma 4.10** (the CRT inclusion–exclusion capacity bound), and
* the **deficiency recurrence** `δ(p^a M) ≥ p·δ(p^{a−1}M) − σ(M)`,

so every inequality is exact integer arithmetic and no external solver is in the
trusted base.  The symbolic machinery lives in
`solver/symbolic.py`; the tests are in `solver/test_symbolic.py`.

## 1. The power-lifting criterion (Task A)

**Theorem.** Let `p` be prime and `gcd(p, M) = 1`.  If

    (p − 1) · δ(pM) ≥ σ(M),

then `p^a M` is not a covering number for **every** `a ≥ 1`.

*Proof.* Iterating the recurrence (induction on `a`) gives

    δ(p^a M) ≥ p^{a−1} δ(pM) − σ(M)·(p^{a−1}−1)/(p−1).

Under the hypothesis this is at least
`σ(M)/(p−1) ≥ 1`, so `δ(p^a M) > 0`.  ∎

The proof is in `NOTES.md` (Section 6).  It is a straightforward consequence of
the elementary recurrence and is recorded as **apparently unpublished**.

## 2. Family B — `3^a · 5 · 7 · q` (Task B)

For every prime `q ≥ 11` and every integer `a ≥ 1`,

    N = 3^a · 5 · 7 · q   is not a covering number.

Derivation:

```
δ(3·5·7·q) >= 35q - 89                 [McNew–Setty Lemma 4.10, symbolic]
M = 5·7·q,  σ(M) = 48(q+1)
2·δ(3M) - σ(M) = 2(35q-89) - 48(q+1) = 22q - 226
22q - 226 >= 0  for  q >= 11
=> (3-1)·δ(3M) >= σ(M), so 3^a·5·7·q is not covering for every a >= 1.
```

Numerically, `q = 11` gives `δ(3·5·7·11) ≥ 296` and the criterion is uniform in
`q`; the `a`-direction is free by Section 1.

## 3. Family C — `3^2 · 5^b · 7 · q` (Task C)

For every prime `q ≥ 11` and every integer `b ≥ 1`,

    N = 3^2 · 5^b · 7 · q   is not a covering number.

Derivation:

```
δ(3·5·7·q) >= 35q - 89                 [McNew–Setty Lemma 4.10, symbolic]
δ(3^2·5·7·q) >= 3·δ(3·5·7·q) - σ(5·7·q)
                = 3(35q-89) - 48(q+1) = 57q - 315
M = 3^2·7·q,  σ(M) = 104(q+1)
4·δ(5M) - σ(M) = 4(57q-315) - 104(q+1) = 124q - 1364
124q - 1364 >= 0  for  q >= 11   (equality at q = 11)
=> (5-1)·δ(5M) >= σ(M), so 3^2·5^b·7·q is not covering for every b >= 1.
```

## 4. Exponent-cone miner (Task D)

`solver/symbolic.py::mine_families([3,5,7], max_exponent=4)` searches all
exponent-raising orders.  For the square-free kernel `3·5·7` with a free prime
`q`, the base bound is

    δ(3·5·7·q) ≥ 35q − 89.

The search finds 34 exponent-lifting families (a free prime direction from some
fixed exponent state) and 25 fixed-exponent exclusions (also infinite in `q`,
with every exponent fixed).  The strongest exponent-lifting families,
**uniform in `q ≥ 11`**, are:

| family (free exponent `a,b,c ≥ 1`) | free prime |
|---|---|
| `3^a · 5 · 7 · q` | 3 |
| `3 · 5^b · 7 · q` | 5 |
| `3 · 5 · 7^c · q` | 7 |
| `3^2 · 5^b · 7 · q` | 5 |
| `3^2 · 5 · 7^c · q` | 7 |
| `3 · 5^2 · 7^c · q` | 7 |
| `3 · 5^b · 7^2 · q` | 5 |
| `3 · 5^3 · 7^c · q` | 7 |
| `3 · 5^b · 7^3 · q` | 5 |
| `3 · 5^4 · 7^c · q` | 7 |
| `3 · 5^b · 7^4 · q` | 5 |

Additional families hold with a larger `q` threshold; for example the miner
also proves `3^3 · 5^b · 7 · q` for primes `q ≥ 29` and `3^a · 5^2 · 7 · q` for
primes `q ≥ 37`.  Each family is emitted together with an exact derivation
(base inequality, prime-lifting order, `σ(M)` values, and the iterated
recurrence) via `InfiniteFamily.derivation`.

The miner is not limited to `{3,5,7}`: any square-free kernel can be passed in,
and the base Lemma 4.10 bound is recomputed symbolically.

## 5. Connection to primitive constraints (Task E)

The all-primes necessary condition for a primitive covering number
`N = ∏ p_i^{a_i}` is

    p_i ≤ τ(N / p_i^{a_i}) = ∏_{j ≠ i} (a_j + 1).

Intersecting this filter with the certified deficiency lower bounds
(`δ_lower`) gives the surviving primitive-candidate patterns — those that pass
the necessary condition but are **not** yet killed by our inequalities.  For
the small odd kernels:

| kernel | exponent bound | # survivors | smallest survivor |
|---|---|---|---|
| `3,5,7` | 5 | 27 | `3^4·5^3·7^2 = 496125` |
| `3,5,7,11` | 5 | 463 | `3^3·5^2·7·11 = 51975` |
| `3,5,7,13` | 5 | 436 | `3^3·5^2·7·13 = 61425` |
| `3,5,7,11,13` | 3 | 158 | `3^3·5·7·11·13 = 135135` |

The **smallest** surviving odd primitive candidate is

    51975 = 3^3 · 5^2 · 7 · 11.

It is odd, abundant, divisible by 9 and 15, satisfies the all-primes condition,
and has `δ_lower = 0` under the current recurrence + Lemma 4.10 bounds.  This is
the next mathematical bottleneck: the raw `σ(M)` top-layer capacity is exactly
what still has to be sharpened (Task F).

## 6. Classification

| item | status |
|---|---|
| McNew–Setty Lemma 4.10 | exact published theorem (arXiv:2507.23041) |
| deficiency recurrence `δ(p^a M) ≥ p δ(p^{a−1}M) − σ(M)` | elementary; folklore-adjacent, proved in `NOTES.md` |
| power-lifting criterion | straightforward consequence of the recurrence; apparently unpublished |
| Families B, C and the miner families | straightforward consequences of Lemma 4.10 + the recurrence; apparently unpublished |

No family here is claimed to be new without that qualification: the heavy
capacity result is McNew–Setty's, and our contribution is the explicit
exponent-lifting extraction.

## 7. Counterexample / falsification search

* The symbolic square-free base `δ(3·5·7·q) = 35q − 89` was checked against the
  numeric `squarefree_coverage_bound` for every prime `q ∈ {11,13,…,97}`.
* Families B and C were checked with `delta_lower_fixed` for
  `a,b ∈ {1,…,6}` and `q ∈ {11,13,17,19,23,29,31,37}`; all lower bounds are
  `≥ 1` (see `solver/test_symbolic.py`).
* The surviving-candidate search covered the small odd kernels listed in
  Section 5 with the stated exponent bounds.

## 8. Exact commands and runtimes

From `goldcheck/research/erdos7/solver`:

```bash
python -m pytest -q -p no:cacheprovider
# 119 passed in 1.15s

python -c "from symbolic import mine_families; mine_families([3,5,7], max_exponent=4)"
python -c "from symbolic import surviving_candidates; print(surviving_candidates([3,5,7,11], 5)[0])"
```
