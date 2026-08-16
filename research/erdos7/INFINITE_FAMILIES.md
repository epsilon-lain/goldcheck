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

## 5. Corrected primitive frontier (full Lemma 4.10 bound)

The all-primes necessary condition for a primitive covering number
`N = ∏ p_i^{a_i}` is

    p_i ≤ τ(N / p_i^{a_i}) = ∏_{j ≠ i} (a_j + 1).

Milestone 2 intersected this filter with the *chained* recurrence bounds and
reported `51975 = 3^3·5^2·7·11` as the smallest survivor.  That conclusion is
**obsolete**.  The Milestone 3 pivot evaluates McNew–Setty Lemma 4.10/equation
(10) on the **full** divisor set `D_{>1}(n)`, giving the bound

    r(n)/n ≤ R(n) = Σ_{∅≠U⊆[k]} C_|U| ∏_{i∈U} x_i,
    x_i = (1 − p_i^{-a_i})/(p_i − 1),   C_m = Σ_{t=1..m} (−1)^{t+1} S2(m,t).

This full bound (a) excludes every odd `n` with `ω(n) ≤ 4`, and (b) certifies
`δ(51975) ≥ 4295` and `δ(496125) ≥ 57006`, `δ(61425) ≥ 5733`,
`δ(135135) ≥ 8557`, so all four former "smallest survivors" are non-covering.

### 5.1 The true smallest `ω = 5` survivor of the direct bound

After intersecting the necessary filters (all-primes condition and abundance
`σ(N) > 2N`) with the full bound `R(N) ≥ 1`, the smallest surviving odd
candidate is

    70945875 = 3^4 · 5^3 · 7^2 · 11 · 13,   R = 876698/875875 ≈ 1.00094.

This is a **genuine minimum** over all five-prime supports, by two proved facts
(see `NOTES.md` Sections 10–11 and `solver/full_bound.py`):

1. any odd `n` with `ω(n) ≤ 4` is excluded by the full bound;
2. any odd `n` with `ω(n) = 5` whose largest prime is `≥ 23` is excluded by the
   full bound, so only the 21 five-prime supports inside
   `{3,5,7,11,13,17,19}` can survive, and they are searched exhaustively with
   exponent pruning by the running minimum.

This is a statement about the **direct union bound**, not about covering: it
only means the direct Lemma 4.10 bound does not exclude `70945875`.

## 5.5 Five-prime large-prime family (full bound, monotonicity)

**Theorem.**  Let `p_1,…,p_4` be four distinct odd primes, let `q ≥ 23` be a
prime distinct from them, and let `a_1,…,a_4, b ≥ 1`.  Then

    n = p_1^{a_1} ⋯ p_4^{a_4} · q^b   is not a covering number.

*Proof sketch.*  For five variables `R = e_1 − e_3 − e_4 + 2e_5`.  Writing the
fifth variable as `y` and `E_j` for the elementary symmetric polynomials of the
other four,

    R = (E_1 − E_3 − E_4) + y·(1 − E_2 − E_3 + 2E_4).

`R` is coordinatewise nondecreasing on `[0,1/2]×[0,1/4]×[0,1/6]×[0,1/10]×[0,1/22]`
because `g = 1 − E_2 − E_3 + 2E_4 ≥ 37/60 > 0` on the four-variable box.  Its
maximum there is

    R(1/2, 1/4, 1/6, 1/10, 1/22) = 5263/5280 < 1,

so `δ(n) ≥ n·17/5280 ≥ 1`.  Full proof: `NOTES.md` Section 10.  This family is
a straightforward consequence of McNew–Setty Lemma 4.10 and is **subsumed** by
Berger–Felzenbaum–Fraenkel 1987 (`ω ≥ 6`); it is included as an independent,
self-contained derivation, not as a new fact.

## 6. Classification

| item | status |
|---|---|
| McNew–Setty Lemma 4.10 | exact published theorem (arXiv:2507.23041) |
| deficiency recurrence `δ(p^a M) ≥ p δ(p^{a−1}M) − σ(M)` | elementary; folklore-adjacent, proved in `NOTES.md` |
| power-lifting criterion | straightforward consequence of the recurrence; apparently unpublished |
| Families B, C and the miner families | straightforward consequences of Lemma 4.10 + the recurrence; apparently unpublished |
| full prime-power form `R(n) = Σ C_|U| ∏ x_i` | reformulation of McNew–Setty equation (10); `NOTES.md` Section 8 |
| every odd `n` with `ω(n) ≤ 4` is non-covering | straightforward consequence of Lemma 4.10; subsumed by Berger–Felzenbaum–Fraenkel 1986 (`ω ≥ 5`) |
| five-prime large-prime family (`q ≥ 23`) | straightforward consequence of Lemma 4.10; subsumed by Berger–Felzenbaum–Fraenkel 1987 (`ω ≥ 6`) |

No family here is claimed to be new without that qualification: the heavy
capacity result is McNew–Setty's, and our contribution is the explicit
exponent-lifting extraction.  The full-bound consequences are likewise recorded
as consequences of the published bound, not as new theorems; the published
`ω ≥ 5` (1986) and `ω ≥ 6` (1987) results are strictly stronger.

## 7. Counterexample / falsification search

* The symbolic square-free base `δ(3·5·7·q) = 35q − 89` was checked against the
  numeric `squarefree_coverage_bound` for every prime `q ∈ {11,13,…,97}`.
* Families B and C were checked with `delta_lower_fixed` for
  `a,b ∈ {1,…,6}` and `q ∈ {11,13,17,19,23,29,31,37}`; all lower bounds are
  `≥ 1` (see `solver/test_symbolic.py`).
* The five-prime corner bound `R(1/2,1/4,1/6,1/10,1/22) = 5263/5280` and the
  monotonicity assertions are checked in `solver/test_full_bound.py`.
* The `ω = 5` survivor search is exhaustive over the 21 supports in
  `{3,5,7,11,13,17,19}` with exponent pruning; it returns `70945875`.

## 8. Exact commands and runtimes

From `goldcheck/research/erdos7/solver`:

```bash
python -m pytest -q -p no:cacheprovider
# 145 passed in 2.33s

python -c "from symbolic import mine_families; mine_families([3,5,7], max_exponent=4)"
python -c "from full_bound import smallest_omega5_survivor; print(smallest_omega5_survivor())"
```
