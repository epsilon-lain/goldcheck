# Notes: audited lemmas and the three certificates

## 0. Model and notation

Throughout, `N ≥ 2` is an integer.  A family
`{ a_d mod d : d ∈ D, d > 1 }` is **valid for `N`** if every modulus `d`
divides `N` and the moduli are pairwise distinct (each `d` is used at most
once, with one residue class).

* `r(N)` = maximum size of a subset of `Z/NZ` coverable by a valid family;
* `δ(N) = N − r(N)` (the *deficiency*);
* `N` is a **covering number** iff `δ(N) = 0`;
* `N` is **primitive** if it is a covering number and no proper divisor of it
  is a covering number.

Every statement below uses exact integer arithmetic.

## 1. The all-primes lemma

### Statement

If `N` is a primitive covering number, then for **every** prime `p | N`,

    p ≤ τ( M ),        M := N / p^{v_p(N)}.

Here `τ` is the divisor-count function.

### Proof

Let `a = v_p(N)` and `M = N/p^a`, so `gcd(p, M) = 1`.  Because `N` is
primitive, `N/p` is **not** a covering number.  Fix a valid family for `N`
that covers all of `Z/NZ`, and let `F_0` be the subfamily of classes whose
modulus divides `N/p`.

The classes in `F_0`, regarded modulo `N/p`, form a valid family for `N/p`.
Since `N/p` is not a covering number, `F_0` does **not** cover all of
`Z/(N/p)`: choose a residue `y mod N/p` missed by `F_0`.

The residue `y mod N/p` has exactly `p` lifts to `Z/NZ`, namely

    y,  y + N/p,  y + 2(N/p),  …,  y + (p−1)(N/p)    (mod N).

Each of these `p` lifts must be covered by some class of the full family.

**Claim 1.** A class with modulus dividing `N/p` that covers one of these lifts
already covers `y mod N/p`.

If `d | N/p` and `x ≡ y (mod N/p)`, then `d | N/p` gives `x ≡ y (mod d)`, so
membership of `x` in `a mod d` depends only on the residue of `y` modulo `N/p`.
This contradicts the choice of `y`.  Hence the `p` lifts are covered only by
classes whose modulus does **not** divide `N/p`.

**Claim 2.** Such a modulus has full `p`-adic exponent: it is `p^a · e` with
`e | M`.

Any divisor `d | N` has `v_p(d) ≤ a`.  The condition `d ∤ N/p` forces
`v_p(d) > a − 1`, hence `v_p(d) = a`, i.e. `d = p^a e` with `e | M`.

**Claim 3.** One congruence class modulo `p^a e` meets at most one of the `p`
lifts.

Two distinct lifts differ by `(k − k′)·(N/p) = (k − k′)·p^{a−1}·M`.  For
`k ≢ k′ (mod p)` this difference is not divisible by `p^a`, so it is not
divisible by `p^a e`.  Hence a single class `mod p^a e` cannot contain two of
the lifts.

Therefore, to cover all `p` lifts we need at least `p` classes of the form
`p^a e`.  Their moduli are distinct, so the divisors `e` are distinct divisors
of `M`, giving `p ≤ τ(M)`.  ∎

### Remarks

* McNew–Setty Lemma 3.1 states the special case `P⁺(N) ≤ τ(N/P⁺(N))`; the
  argument above is verbatim their proof, specialised to an arbitrary prime
  and with the sharper count `τ(M)` in place of `τ(N/p)`.
* The condition is only necessary: it holds for `10395`, `12285`, `17325`, yet
  all three are excluded below.  See `solver/certificate.py::all_primes_lemma_holds`.

## 2. The deficiency recurrence

### Statement

For `N = p^a M` with `p` prime and `gcd(p, M) = 1`,

    δ(N) ≥ p · δ(N/p) − σ(M),

where `σ` is the sum-of-divisors function.

### Proof

Split the moduli of any valid family for `N` into

* the **lower layer**: moduli `d` with `d | N/p` (equivalently
  `v_p(d) ≤ a − 1`);
* the **top layer**: moduli `d` with `v_p(d) = a`, i.e. `d = p^a e`, `e | M`.

**Lower layer.**  The lower classes are classes modulo `d | N/p`.  Regarded
modulo `N/p`, they form a valid family for `N/p`, so they cover at most
`r(N/p)` residues of `Z/(N/p)`.  Each covered residue lifts to exactly `p`
residues of `Z/NZ`; hence the lower layer covers at most `p · r(N/p)` residues
of `Z/NZ`.

**Top layer.**  A class modulo `p^a e` contains exactly `N/(p^a e) = M/e`
residues of `Z/NZ`.  The union of the top classes has size at most the sum of
their sizes:

    ∑_{e | M} M/e = σ(M).

Therefore `r(N) ≤ p · r(N/p) + σ(M)`, and rearranging with
`δ(n) = n − r(n)` gives

    δ(N) = N − r(N) ≥ N − p·r(N/p) − σ(M)
                        = p·δ(N/p) − σ(M).  ∎

## 3. The square-free CRT/Hall bound

### Source

This is McNew–Setty **Lemma 4.10**, evaluated on the full divisor set of an odd
square-free integer.

### Lemma 4.10 (McNew–Setty, restated)

For any multiset `M` of moduli, the proportion of integers covered by a residue
system whose moduli are the elements of `M` is at most

    ∑_{S ⊆ M, S ≠ ∅, S pairwise coprime} (−1)^{|S|+1} / lcm(S).

### Specialisation to odd square-free `n`

Let `n = p_1 ⋯ p_k` with distinct odd primes.  Take `M` to be the set of all
nonempty divisors of `n`.  A pairwise-coprime subfamily `S ⊆ M` is a collection
of divisors whose prime-factor sets are pairwise disjoint; writing each divisor
as the product of its primes, `S` is the same data as a set partition of a
nonempty subset `U ⊆ {1,…,k}` into nonempty blocks, and `lcm(S) = ∏_{i∈U} p_i`.

Grouping by `|U| = j`, the coefficient of `1/∏_{i∈U} p_i` is the number of
ways to partition a `j`-element set into `t ≥ 1` blocks, signed by
`(−1)^{t+1}`:

    C_j := ∑_{t=1}^{j} (−1)^{t+1} S2(j, t).

Multiplying by `n`, the number of residues of `Z/nZ` coverable by any valid
family is at most

    r(n) ≤ ∑_{j=1}^{k} C_j ∑_{U, |U|=j} ∏_{i∉U} p_i.        (∗)

The first coefficients are `C_1 = 1`, `C_2 = 0`, `C_3 = −1`, `C_4 = −1`,
`C_5 = 2`.  Hence

    δ(n) = n − r(n) ≥ n − (right side of (∗)).

For the bases used by the certificates:

| n            | factors            | coverage bound (∗) | δ(n) ≥  |
|--------------|--------------------|---------------------|---------|
| 105          | 3·5·7              | 70                  | 35      |
| 1155         | 3·5·7·11           | 859                 | 296     |
| 1365         | 3·5·7·13           | 999                 | 366     |

(These values are computed by `solver/certificate.py::squarefree_coverage_bound`;
the computation is pure integer arithmetic and does **not** rely on a solver.)

### A corrected failed generalisation

An earlier working note guessed the square-free bound in the closed form

    δ(n) ≥ φ(n) − ∑_{|S|≥2} ∏_{i∉S} (p_i − 1).

That closed form coincides with (∗) for `k ≤ 3` (`15, 105, 165, 231, 273, 385,
455` all match), but it is **not** the inclusion–exclusion bound for `k ≥ 4`:

| n     | factors       | inclusion–exclusion coverage | φ-form "coverage" | δ(n) ≥ (Lemma 4.10) |
|-------|---------------|------------------------------|--------------------|---------------------|
| 1155  | 3·5·7·11      | 859                          | 862                | 296                 |
| 1365  | 3·5·7·13      | 999                          | 1002               | 366                 |
| 15015 | 3·5·7·11·13   | 12062                        | 12174              | 2953                |

For `1155` the φ-form would only certify `δ(1155) ≥ 293`, whereas the correct
Lemma 4.10 specialisation certifies `δ(1155) ≥ 296`.  The φ-form is therefore
**not** used anywhere in the certificates; it is recorded here only as a
falsified intermediate guess.  Numerically the two quantities agree for every
odd square-free `n` with at most three prime factors and diverge once there are
four; the certificates therefore use the inclusion–exclusion form (∗) directly.

## 4. The certificates

### 4.1 `N = 945 = 3^3 · 5 · 7`

```
δ(105)  ≥ 35                                       [square-free bound]
δ(315)  ≥ 3·δ(105) − σ(35)  = 105 − 48  = 57       [recurrence, p=3]
δ(945)  ≥ 3·δ(315) − σ(35)  = 171 − 48  = 123      [recurrence, p=3]
```

`σ(35) = 48`.  Conclusion: `δ(945) ≥ 123 > 0`, so `945` is **not** a covering
number.

### 4.2 `N = 10395 = 3^3 · 5 · 7 · 11`

```
δ(1155)  ≥ 296                                       [square-free bound]
δ(3465)  ≥ 3·δ(1155) − σ(385)  = 888 − 576 = 312     [recurrence, p=3]
δ(10395) ≥ 3·δ(3465) − σ(385)  = 936 − 576 = 360     [recurrence, p=3]
```

`σ(385) = 576`.  Conclusion: `δ(10395) ≥ 360 > 0`.

### 4.3 `N = 12285 = 3^3 · 5 · 7 · 13`

```
δ(1365)  ≥ 366                                       [square-free bound]
δ(4095)  ≥ 3·δ(1365) − σ(455)  = 1098 − 672 = 426     [recurrence, p=3]
δ(12285) ≥ 3·δ(4095) − σ(455)  = 1278 − 672 = 606     [recurrence, p=3]
```

`σ(455) = 672`.  Conclusion: `δ(12285) ≥ 606 > 0`.

### 4.4 `N = 17325 = 3^2 · 5^2 · 7 · 11`

```
δ(1155)  ≥ 296                                       [square-free bound]
δ(5775)  ≥ 5·δ(1155) − σ(231)  = 1480 − 384 = 1096    [recurrence, p=5]
δ(17325) ≥ 3·δ(5775) − σ(1925) = 3288 − 2976 = 312    [recurrence, p=3]
```

`σ(231) = 384`, `σ(1925) = 2976`.  Conclusion: `δ(17325) ≥ 312 > 0`.

Each chain is printed verbatim by `solver/certificate.py` and asserted by
`verify_certificates`.

## 5. Status and the next bottleneck

The certificates are **proved**, not merely computational: the square-free bases
come from McNew–Setty Lemma 4.10 (an inclusion–exclusion CRT theorem) and the
recurrence is a fully proved counting lemma.  The three targets are therefore
rigorously excluded.

The obvious bottleneck is that the recurrence still charges the top layer its
**raw** capacity `σ(M)`.  For the stragglers `σ(M)` is just small enough for
the chain to remain positive; to push past the next odd abundant candidates and
towards an infinite family, `σ(M)` must be replaced by a sharper CRT/Hall
capacity that accounts for forced overlaps.  The square-free bound (∗) is
exactly such a sharpening for the square-free case; the missing ingredient is a
multi-prime-power version of Lemma 4.10 that also corrects the `σ(M)` term of
the recurrence.

No finite search is claimed to resolve the open problem.
