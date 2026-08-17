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

*Update (Milestone 3 pivot).*  The "missing" multi-prime-power ingredient is
supplied by McNew–Setty equation (10) itself, evaluated on the **full** divisor
set `D_{>1}(n)`; see Section 8.  It directly kills `51975` and, in fact, every
odd `n` with `ω(n) ≤ 4` (Section 9), so the specific `51975` bottleneck is
retired.  The remaining frontier is `ω(n) ≥ 5` (and, from the published
literature, `ω(n) ≥ 6`), see Sections 10–11.

No finite search is claimed to resolve the open problem.

## 6. The power-lifting criterion

### Statement

Let `p` be prime and `gcd(p, M) = 1`.  If

    (p − 1) · δ(pM) ≥ σ(M),

then for **every** integer `a ≥ 1`,

    δ(p^a M) ≥ σ(M)/(p − 1) ≥ 1,

and consequently `p^a M` is **not** a covering number for every `a ≥ 1`.

### Proof

Iterate the deficiency recurrence (Section 2).  Induction on `a` gives

    δ(p^a M) ≥ p^{a−1} δ(pM) − σ(M) · (p^{a−1} − 1)/(p − 1).       (†)

The base case `a = 1` is trivial.  For `a ≥ 2`,

    δ(p^a M) ≥ p · δ(p^{a−1}M) − σ(M)
              ≥ p · [ p^{a−2} δ(pM) − σ(M)(p^{a−2}−1)/(p−1) ] − σ(M)
              = p^{a−1} δ(pM) − σ(M) · (p^{a−1}−1)/(p−1).

Combining (†) with `(p−1)δ(pM) ≥ σ(M)`:

    δ(p^a M) ≥ p^{a−1} · σ(M)/(p−1) − σ(M) · (p^{a−1}−1)/(p−1)
              = σ(M)/(p−1) ≥ 1,

because `σ(M) ≥ 1` and `p − 1 ≥ 1`.  ∎

### Classification

The criterion is an immediate corollary of the (elementary) deficiency
recurrence.  It does not appear to be stated in the literature we checked
(McNew–Setty, Mian–Siddique, Hough–Nielsen, BBMST); we record it as a
straightforward, apparently unpublished observation.

## 7. Infinite families and the exponent-cone miner

Combining McNew–Setty Lemma 4.10 with Section 6 gives proved infinite families;
the full catalogue and derivations are in `INFINITE_FAMILIES.md`.  Two headline
families:

### Family B

For every prime `q ≥ 11` and every integer `a ≥ 1`,

    N = 3^a · 5 · 7 · q   is not a covering number.

Derivation: `δ(3·5·7·q) ≥ 35q − 89` (Lemma 4.10); with `p = 3`, `M = 5·7·q`,
`σ(M) = 48(q+1)`, and

    2·(35q−89) − 48(q+1) = 22q − 226 ≥ 0   for q ≥ 11.

### Family C

For every prime `q ≥ 11` and every integer `b ≥ 1`,

    N = 3^2 · 5^b · 7 · q   is not a covering number.

Derivation: `δ(3^2·5·7·q) ≥ 57q − 315` (one recurrence step); with `p = 5`,
`M = 3^2·7·q`, `σ(M) = 104(q+1)`, and

    4·(57q−315) − 104(q+1) = 124q − 1364 ≥ 0   for q ≥ 11,

with equality at `q = 11`.

The `solver/symbolic.py` miner turns this into exact machinery: it evaluates
Lemma 4.10 symbolically as an affine form in a free prime `q`, applies the
recurrence one prime-power step at a time, and checks the Section 6 criterion to
mark an exponent as free.  See `INFINITE_FAMILIES.md` for the clustered output.

### Smallest surviving primitive-candidate pattern (Task E — corrected)

The previous claim that `51975 = 3^3 · 5^2 · 7 · 11` is the smallest survivor
is **obsolete**.  The full divisor-set bound (Section 8) certifies
`δ(51975) ≥ 4295`, so `51975` is not a covering number.  The corrected frontier
is recorded in Section 11: the smallest odd `ω = 5` candidate that passes the
necessary filters and is not excluded by the direct Lemma 4.10 bound is

    70945875 = 3^4 · 5^3 · 7^2 · 11 · 13.

## 8. The full prime-power form of Lemma 4.10

### Source and statement

McNew–Setty equation (10) applies Lemma 4.10 to the **full** set `D_{>1}(n)`
of divisors of `n` larger than 1.  For

    n = ∏_{i=1}^{k} p_i^{a_i},
    x_i = Σ_{j=1}^{a_i} p_i^{-j} = (1 − p_i^{-a_i})/(p_i − 1),
    C_m = Σ_{t=1}^{m} (−1)^{t+1} S2(m, t),

the bound is

    r(n)/n ≤ R(n) := Σ_{∅≠U⊆[k]} C_|U| ∏_{i∈U} x_i.

### Derivation

A pairwise-coprime subfamily of `D_{>1}(n)` has pairwise disjoint prime
supports, so it is exactly a set partition of a nonempty support `U ⊆ [k]` into
nonempty blocks, one divisor per block.  For a fixed block `B`, summing `1/d`
over all exponent choices on that block factorises as `∏_{i∈B} x_i`, while
`lcm` of a coprime family is the product of its moduli.  Grouping by `U` and by
the number `t` of blocks gives the coefficient
`C_|U| = Σ_t (−1)^{t+1} S2(|U|,t)`; the sign is the inclusion–exclusion sign of
Lemma 4.10.  Hence

    δ(n) = n − r(n) ≥ n·(1 − R(n)),

and `n·R(n)` is always an integer (Lemma 4.10 gives an integer coverage bound).

The first coefficients are `C_1 = 1, C_2 = 0, C_3 = −1, C_4 = −1, C_5 = 2,
C_6 = 9, C_7 = 9, C_8 = −50, …`.  In particular, for `k = 4`,

    R = e_1 − e_3 − e_4,

where `e_j` is the `j`-th elementary symmetric polynomial in `x_1,…,x_k`.
Implementation: `solver/full_bound.py::support_R`, cross-checked against the
independent divisor-sum form `solver/full_bound.py::divisor_R`.

### The `51975` certificate

For `51975 = 3^3 · 5^2 · 7 · 11`:

    x_3 = 13/27,  x_5 = 6/25,  x_7 = 1/7,  x_11 = 1/11,
    R(51975) = e_1 − e_3 − e_4 = 9536/10395 < 1,
    δ(51975) ≥ 51975 · (1 − 9536/10395) = 4295.

See `certificates/51975.md`.

## 9. Every odd `n` with `ω(n) ≤ 4` is non-covering

### Statement

If `n` is odd and `ω(n) ≤ 4`, then `R(n) < 1`, hence `δ(n) > 0` and `n` is not
a covering number.  Equivalently, any odd covering number has at least five
distinct prime factors.

### Proof (monotonicity)

Write `k = ω(n)`.  For `k ≤ 4`, `R = e_1` (`k = 1,2`), `e_1 − e_3` (`k = 3`),
or `e_1 − e_3 − e_4` (`k = 4`).

**Coordinatewise monotonicity.**  Each `x_i` lies in `(0, 1/(p_i−1)]`; for four
distinct odd primes the three largest possible `x`-values are at most
`1/2, 1/4, 1/6`.  For `k = 4`,

    ∂R/∂x_i = 1 − e_2(rest) − e_3(rest),

where `rest` is the other three variables.  Since
`e_2 ≤ 1/2·1/4 + 1/2·1/6 + 1/4·1/6 = 1/4` and `e_3 ≤ 1/2·1/4·1/6 = 1/48`,

    ∂R/∂x_i ≥ 1 − 1/4 − 1/48 = 35/48 > 0.

So `R` is nondecreasing in every variable (the `k ≤ 3` cases are similar), and
its maximum is attained at infinite exponents with the smallest odd primes.

**Exact limits.**  For the smallest odd primes and infinite exponents:

| ω | primes | R limit |
|---|--------|---------|
| 1 | 3 | 1/2 |
| 2 | 3,5 | 3/4 |
| 3 | 3,5,7 | 43/48 |
| 4 | 3,5,7,11 | 31/32 |

All are `< 1`, so `R(n) < 1` for every odd `n` with `ω(n) ≤ 4`.  ∎

### Provenance

This exact consequence is **already published**: Berger–Felzenbaum–Fraenkel,
*Necessary condition for the existence of an incongruent covering system with
odd moduli*, Acta Arith. **45** (1986) 375–379 (Zbl 0533.10001), proves at least
**five** distinct prime factors.  We record our derivation only as a
self-contained route through McNew–Setty Lemma 4.10; we do **not** claim
novelty.

## 10. Five-prime large-prime family (direct-bound monotonicity)

### Statement

Let `p_1,…,p_4` be four distinct odd primes, let `q ≥ 23` be a prime distinct
from them, and let `a_1,…,a_4, b ≥ 1` be arbitrary.  Then

    n = p_1^{a_1} ⋯ p_4^{a_4} · q^b

is **not** a covering number.

### Proof

For `k = 5`, `R = e_1 − e_3 − e_4 + 2 e_5`.  Write the fifth variable as `y`
and the other four as `x_1,…,x_4`, with elementary symmetric polynomials
`E_j` in the four `x`'s.  Then

    R(x_1,…,x_4, y) = (E_1 − E_3 − E_4) + y·(1 − E_2 − E_3 + 2 E_4).

Set `m = (1/2, 1/4, 1/6, 1/10)` and `B = [0,1/2]×[0,1/4]×[0,1/6]×[0,1/10]`.
For four distinct odd primes and `q ≥ 23`, the sorted values
`x_1,…,x_4, y` fit in `B × [0,1/22]`, because the four largest possible
`1/(p−1)` values are `1/2,1/4,1/6,1/10` and `y < 1/(q−1) ≤ 1/22`.

**Monotonicity.**  For any coordinate `x_i`, with `g` defined on the "other
four" variables by `g = 1 − E_2 − E_3 + 2E_4`,

    ∂R/∂x_i = g(other four),  ∂R/∂y = g(x_1,…,x_4).

It suffices to show `g ≥ 0` on `B`.  For a variable `z_1` of `g`,

    ∂g/∂z_1 = −(z_2+z_3+z_4) − (z_2z_3+z_2z_4+z_3z_4) + 2 z_2 z_3 z_4 ≤ 0,

since `z_2,z_3,z_4 ≥ 0` and each is `≤ 1/2`, so `2 z_2 z_3 z_4 ≤ z_2 z_3`.
Thus `g` is nonincreasing in each coordinate and its minimum on `B` is at the
corner `m`.  There

    g(m) = 1 − E_2(m) − E_3(m) + 2E_4(m)
         = 1 − 41/120 − 11/240 + 1/240 = 37/60 > 0.

Therefore `R` is nondecreasing in each of its five coordinates on
`B × [0,1/22]`, and its maximum there is

    R(1/2, 1/4, 1/6, 1/10, 1/22) = 5263/5280 < 1.

Consequently `R(n) ≤ 5263/5280 < 1`, so `δ(n) ≥ n·17/5280 ≥ 1`.  ∎

### Provenance

This is a straightforward consequence of McNew–Setty Lemma 4.10/equation (10)
plus an elementary monotonicity estimate.  It is **subsumed** by the published
result of Berger–Felzenbaum–Fraenkel, *…II*, Acta Arith. **48** (1987) 73–79
(Zbl 0623.10004), which proves at least **six** distinct prime factors; we
include it as a self-contained illustration of the direct-bound method, not as
a new fact.

## 11. Corrected survivor frontier and next bottleneck

Intersecting the necessary filters — all-primes primitive condition
`p_i ≤ τ(N/p_i^{v_p(N)})` and abundance `σ(N) > 2N` — with the direct bound
`R(N) ≥ 1` (i.e. the bound does **not** certify positive deficiency) gives:

* every odd `N` with `ω(N) ≤ 4` is excluded (Section 9);
* every odd `N` with `ω(N) = 5` whose largest prime is `≥ 23` is excluded
  (Section 10), so a surviving five-prime support must be drawn from
  `{3,5,7,11,13,17,19}`.

An exact search over those 21 supports (exponents enumerated up to the running
minimum, so the result is a genuine minimum) finds

    70945875 = 3^4 · 5^3 · 7^2 · 11 · 13,
    R(70945875) = 876698/875875 ≈ 1.00094,

as the smallest odd `ω = 5` candidate that passes all three filters.
`solver/full_bound.py::smallest_omega5_survivor` computes it.

This is **not** a claim that `70945875` is a covering number: it only means the
direct Lemma 4.10 bound does not exclude it, and no finite search resolves the
open problem.

### The genuine mathematical bottleneck

The published literature already gives `ω(n) ≥ 6` for an odd distinct covering
system (Berger–Felzenbaum–Fraenkel 1987).  The direct Lemma 4.10 bound is
exhausted at `ω ≤ 4`: its infinite-exponent limits are `1469/1440` (`ω = 5`)
and `32323/30720` (`ω = 6`), both `> 1`, so it can never exclude a general
five- or six-prime support by itself.  The next bottleneck is therefore to
**replace or sharpen the direct union bound** for the `ω = 5` survivors (and
then `ω = 6`) with the conditioned top-layer CRT/Hall profile machinery of the
Milestone 3 brief (Task F1–F4), or another method, in order to reproduce or go
beyond the published `ω ≥ 6` result.

## 12. Conditioned top-layer profile inequality (Task F1)

The first concrete tool for sharpening the raw recurrence is the following
conditioned capacity inequality, which is where the next proof effort resumes.

### Statement

Let `N = p^a M` with `p` prime, `gcd(p, M) = 1`, and write `L = N/p =
p^{a−1} M`.  Fix the *lower layer*: one residue class for each chosen divisor
`d | L, d > 1` (at most one per divisor).  Let `U ⊆ Z/LZ` be the set of
residues left uncovered by the lower layer, and define, for `d | L`,

    μ_d(U) = max_b |{ u ∈ U : u ≡ b (mod d) }|.

Then the full-`p`-adic top layer (`p^a e`, `e | M`) can cover at most

    C(U) = Σ_{e | M} μ_{p^{a−1} e}(U)

of the `p · |U|` lifts of `U` to `Z/NZ`.  Consequently any full cover requires

    p · |U| ≤ Σ_{e | M} μ_{p^{a−1} e}(U).

### Proof

A class `r mod p^a e` meets a lift `u + tL` only if `u ≡ r (mod p^{a−1} e)`,
because `L` is divisible by `p^{a−1} e`.  Hence its base points `u ∈ U` lie in
one residue class modulo `p^{a−1} e`, at most `μ_{p^{a−1} e}(U)` of them.  For
fixed `u`, two distinct lifts `u + tL`, `u + t′L` differ by
`(t−t′)·p^{a−1} M`, which is divisible by `p^a` only when `t ≡ t′ (mod p)`;
so the class meets at most one lift of each such `u`.  Therefore the class meets
at most `μ_{p^{a−1} e}(U)` lifts in total, and summing over the distinct top
moduli gives `C(U)`.  ∎

### Relation to the raw recurrence

Each residue class modulo `p^{a−1} e` has size `L/(p^{a−1} e) = M/e`, so
`μ_{p^{a−1} e}(U) ≤ M/e`, and replacing every profile term by `M/e` recovers
the raw `σ(M)` charge.  The profile inequality is therefore a strict refinement
whenever `U` is concentrated in some residue classes.  Brute-force verification
on small instances is in `solver/test_profile.py`; the implementation is
`solver/profile.py`.

### Provenance

This is an elementary counting lemma.  We prove it and verify it exhaustively;
we do **not** claim novelty, and we have not yet located an exact published
statement.  It is the intended entry point to the conditioned CRT/Hall profile
state needed to attack the `ω = 5` survivors.

## 13. BFF 1987: the forest method (Milestone 4)

### 13.1 The forest lemma

If `G` is a forest and `{S_v : v ∈ V(G)}` is any family of finite sets, then

    |⋃_{v∈V} S_v| ≤ Σ_{v∈V} |S_v| − Σ_{uv∈E(G)} |S_u ∩ S_v|.        (F)

*Proof.*  For a point `x` in the union let `k` be the number of sets containing
it.  Its contribution to the right-hand side is `k − e`, where `e` is the number
of edges both of whose endpoints contain `x`.  Those `k` vertices induce a
subforest of `G`, so `e ≤ k − 1`, giving contribution `≥ 1` when `k ≥ 1`, and
`0` otherwise.  ∎  This is the overlap-subtraction step at the heart of the
paper; implementation and brute-force checks are in `solver/bff1987.py`.

### 13.2 The audited engine (tasks H2/H3)

The BFF proof applies (F) to the building blocks indexed by **2-subsets** of the
`n` prime coordinates.  The audited correspondence is:

* vertices: the 2-subsets of `{1, …, n}`;
* an edge is allowed exactly when the two 2-subsets are disjoint (the Kneser
  graph `KG(n,2)`);
* the certified pairwise-overlap weight of an edge `{I, J}` is
  `∏_{i ∈ I ∪ J} z_i`.

For fixed parameters any forest is admissible, so the strongest correction is a
maximum-weight spanning tree of `KG(n,2)` (all weights positive, hence a
spanning tree).  `solver/bff1987.py` implements Kruskal's algorithm in exact
rational arithmetic together with an independent acyclicity/weight verifier.
For `n = 5` the maximum tree has `9` edges and weight `13/384`, which exceeds
the four-term lower bound
`z_1z_2z_3z_4 + z_1z_2z_3z_5 + z_1z_2z_4z_5 + z_1z_3z_4z_5 = 1/80` extracted in
the paper's equation (25); the optimized tree is therefore strictly stronger.

### 13.3 The reconstructed necessary polynomial

The paper's theorem is `g(w,z) ≥ 2`, with

    g1(w,z) = (1+w)∏_{i=2}^{n}(1+z_i) − w − (1+w−z_1)Σ_{i=2}^{n} z_i,
    g = g1 − (forest overlap sum).

Here `N = ∏ p_i^{s_i}` and the variables (and their monotonicity bounds, paper
(13)/(14)) are

    w < 1/(p_1−2),   z_1 < 1/(p_1(p_1−2)),   z_i < 1/(p_i−3)  (2 ≤ i ≤ n).

`g` is increasing on the paper's domain `w,z_i > 0, w ≥ 3z_1, z_2,z_3 < 1,
z_4,z_5 < 1/3`, so the worst case is approached at those bounds.  Evaluating
`g = g1 − F_max` (the optimized forest) at the bound values gives:

| ω | smallest primes | g |
|---|-----------------|---|
| 2 | 3,5 | 7/6 |
| 3 | 3,5,7 | 3/2 |
| 4 | 3,5,7,11 | 335/192 |
| 5 | 3,5,7,11,13 | 761/384 < 2 |
| 6 | 3,5,7,11,13,17 | 4889/2240 > 2 |
| 7 | 3,5,7,11,13,17,19 | 34095/14336 > 2 |

Hence `g < 2` for every odd support with at most five primes, reproducing the
published `ω(N) ≥ 6`; and `g > 2` for the smallest six-prime support, so the
optimized forest condition does **not** exclude `ω = 6`.

### 13.4 Status and confidence

The forest lemma, the Kneser-graph engine, the maximum-weight spanning tree, and
the independent verifier are exact and fully tested.  The polynomial `g1`, the
parameter bounds, and the worst-case values above were reconstructed by OCR from
the scanned PDF and then **validated by reproducing the published `ω ≥ 6`
result**; the exact closed-form equations (9)/(15) and the precise edge set of
the paper's Figure 1 should still be re-audited against a clean typeset copy
before they are quoted as verbatim transcription.  No novelty is claimed: this
is a reformulation/reproduction of Berger–Felzenbaum–Fraenkel 1987.

### 13.5 The next bottleneck (tasks H4/H5)

Because `g(3,5,7,11,13,17) = 4889/2240 > 2`, the pairwise forest correction is
exhausted at `ω = 6`; it cannot force `ω ≥ 7`.  The next step is a higher-order
acyclic-overlap correction (junction-tree / hypertree inclusion–exclusion, or a
dual certificate weighting triple intersections), using the `k = 6` corner
`{3,5,7,11,13,17}` as the discovery instance.

## 14. Higher-order overlap certificate (Milestone 5)

### 14.1 The coefficient-certificate lemma (task I1)

Let `{A_v : v ∈ V}` be finite sets and `{α_J : ∅≠J⊆V}` rational coefficients.
If, for every nonempty membership pattern `T ⊆ V`,

    Σ_{∅≠J⊆T} α_J ≥ 1,                                          (C)

then

    |⋃_{v∈V} A_v| ≤ Σ_{∅≠J⊆V} α_J · |⋂_{j∈J} A_j|.

*Proof.*  Fix a point `x`; put `T = {v : x ∈ A_v}`.  If `T = ∅` then `x`
contributes to neither side.  Otherwise `x` contributes `1` to the left side and
exactly `Σ_{∅≠J⊆T} α_J` to the right side, which is `≥ 1` by (C).  Summing over
`x` gives the bound.  ∎  The forest lemma is the special case `α_v = 1`,
`α_{uv} = −1` on forest edges, all other `α_J = 0`: for `T` the induced subgraph
has `≤ |T|−1` edges, so `|T| − (#edges) ≥ 1`.

### 14.2 The six-prime intersection semantics (task I2)

At `n = 6`, the BFF building blocks are indexed by the `15` two-subsets `I` of
`{1,…,6}`; each is a product set whose normalized size is `∏_{i∈I} z_i`, with
the worst-case `z` values

    z_1 = 1/3, z_2 = 1/2, z_3 = 1/4, z_4 = 1/8, z_5 = 1/10, z_6 = 1/14.

Because the sets are products over disjoint coordinate sets:

* a **disjoint** pair `{I,J}` has exact intersection `∏_{i∈I∪J} z_i` (a lower
  bound and also exact);
* an **overlapping** pair shares a coordinate, so its intersection can be `0`
  (the safe lower bound; such pairs are never useful and are omitted);
* a **triple** `{I,J,K}` has intersection at most `∏_{i∈I∪J∪K} z_i` (the safe
  upper bound used with the positive triple coefficient).

These are the only intersection bounds entering the certificate; none is
heuristic.

### 14.3 The pair+triple LP and its exact dual (tasks I3/I4)

The certificate is

    |⋃ A_v| ≤ Σ_v |A_v| − Σ_e λ_e |A_u∩A_v| + Σ_h μ_h |A_i∩A_j∩A_k|,

with `λ_e, μ_h ≥ 0` and pointwise validity (from (C))

    |T| − Σ_{e⊆T} λ_e + Σ_{h⊆T} μ_h ≥ 1   for all ∅≠T⊆V.

Maximizing the correction `F = Σ_e λ_e L_e − Σ_h μ_h U_h` over the `2^15−1`
patterns gives, by LP duality, an exact optimum `F* = 9997/161280`.  The dual
certificate (171 nonzero rational dual weights, stored in
`certificates/omega6_overlap.json`) independently proves this value: it is
nonnegative, covers every disjoint pair weight, and its objective is exactly
`9997/161280`.

Consequently, with `g1 = 5989/2688`,

    g = g1 − F* = 349343/161280 = 2.16606… > 2,

and the residual gap above `2` is

    g − 2 = 26783/161280 ≈ 0.166.

### 14.4 Verdict and the next missing term (tasks I5/I6)

The pair+triple basis is therefore **rigorously certified insufficient**: even
its exact optimum leaves `g > 2`, so it cannot exclude the six-prime corner and
cannot yield `ω(N) ≥ 7`.  The sharply isolated missing ingredient is the next
acyclic-overlap layer — selected **quadruple** intersections (or an equivalent
junction-tree/hypertree correction) — to close the residual gap `26783/161280`.
`solver/higher_overlap.py` provides the lemma and the pure-`Fraction` verifier;
`solver/test_higher_overlap.py` checks the pointwise constraints, the forest
special case, and the exact certificate.

## 15. Order-4 (quadruple) basis is also insufficient (Milestone 6)

### 15.1 The audited intersection oracle (task J1)

With the BFF building block `A_I` a product set whose coordinate `i ∈ I` is a
single residue class (normalized factor `z_i`) and whose other coordinates are
full, the certified intersection bounds for a family `J` of two-subsets are:

* `U_J = ∏_{i∈∪_{v∈J} I_v} z_i` is a certified upper bound (and tight), for
  every `J`;
* `L_J = U_J` is certified **exactly** when the index sets `I_v` are pairwise
  disjoint (no coordinate is shared, so no coordinate can be split);
* otherwise only the trivial `L_J = 0` is certified.

For `n = 6` there are `15` two-subsets; a quadruple of two-subsets always shares
a coordinate (`4·2 > 6`), so **every quadruple has only `L = 0`**.  This is the
key structural fact: the unconditioned basis has no positive lower bound for any
overlapping pair, any non-matching triple, or any quadruple.

### 15.2 The sign-aware order-4 LP (task J2)

Using the Milestone-5 coefficient certificate with signs split as
`α_J = α_J⁺ − α_J⁻`, the objective maximizes the certified correction

    F = Σ_e λ_e L_e − Σ_h μ_h U_h − Σ_q ν_q U_q

over `λ, μ, ν ≥ 0`, subject to the `2^15 − 1 = 32767` pointwise constraints

    |T| − Σ_{e⊆T} λ_e + Σ_{h⊆T} μ_h + Σ_{q⊆T} ν_q ≥ 1.

Here `e` ranges over the `45` disjoint pairs (`L_e` exact), `h` over the `455`
triples (`U_h`), and `q` over the `1365` quadruples (`U_q`).  A positive
coefficient is charged its upper bound; a negative coefficient is credited its
lower bound.

### 15.3 Exact optimum and insufficiency certificate (tasks J4/J5)

The exact optimum (HiGHS for discovery, then rationalized and independently
verified with `Fraction`) is

    F* = 24457/394240,
    g  = g1 − F* = 5989/2688 − 24457/394240 = 2561789/1182720 = 2.16601… > 2,
    g − 2 = 196349/1182720 ≈ 0.166.

The `235`-weight rational dual certificate is stored in
`certificates/omega6_order4_overlap.json`; `verify_order4_certificate` re-checks
nonnegativity, the pair lower-bound constraints, the triple upper-bound
constraints, the quadruple upper-bound constraints, and the exact dual objective.

The order-3 value was `9997/161280 ≈ 0.061985`; adding quadruples only moves the
optimum to `24457/394240 ≈ 0.062036`, an improvement of about `5 × 10⁻⁵`.
Quadruple terms therefore provide essentially no additional certified correction.

### 15.4 Structural conclusion and the next step (tasks J5/J6)

The complete unconditioned `|J| ≤ 4` coefficient basis is **insufficient** and
its residual gap is `196349/1182720`.  The obstruction is not "need fifth-order
terms": it is the absence of any nonzero certified **lower** bound for the
overlapping intersections (`L = 0` for every non-matching family).  The
unconditioned product-set structure cannot certify that two blocks sharing a
coordinate actually overlap.

The precise next ingredient is therefore **conditioned** lower-bound
information: the Task-F1 profile state `μ_d(U)` (concentration of the lower
layer's uncovered set in residue classes) can certify, for a realizable lower
layer, that certain overlapping intersections are nonempty, turning some
`L = 0` entries into positive certified lower bounds.  That is the concrete
multi-intersection inequality invisible to the unconditional BFF basis, and the
natural entry point for a profile-state recurrence rather than a finite
computation.

## 16. One-coordinate star-collision relaxation (Milestone 7)

### 16.1 The star-collision lemma (task K1)

For a fixed prime coordinate `i`, the five blocks `B_{ij}` (`j ≠ i`) all have
measure `z_i` in the same coordinate.  Writing the `2^5 = 32` membership-pattern
atom masses

    y_{i,T} = measure{x : x ∈ B_{ij} ⟺ j ∈ T},   T ⊆ [6]∖{i},

the constraints are `y ≥ 0`, `Σ_T y_{i,T} = 1`, and `Σ_{T∋j} y_{i,T} = z_i` for
every `j ≠ i`.  For any nonnegative pair weights `c_{jk}`,

    Σ_{j<k, j,k≠i} c_{jk} · measure(B_{ij} ∩ B_{ik})
      = Σ_T y_{i,T} · Σ_{{j,k}⊆T} c_{jk}
      ≥ min over feasible ``y`` of that same linear form.

That minimum is the *star lower envelope*.  Its LP dual is
`max v_0 + z_i Σ_j v_j` subject to `v_0 + Σ_{j∈T} v_j ≤ Σ_{{j,k}⊆T} c_{jk}`.
For the benchmark `c_{jk} = z_j z_k` the exact optima (primal+dual certified in
`certificates/omega6_star.json`) are:

| coordinate i | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `LP_i(z_j z_k)` | 1/105 | 307/6720 | 1/560 | 0 | 0 | 0 |

The first three stars are nontrivial (`5 z_i > 1` for `i = 1,2,3`), as expected.
Implementation and independent verification: `solver/star_collision.py`.

### 16.2 The star-pair relaxation is insufficient (tasks K2/K3)

Embedding each star dual into the coefficient certificate gives the star-pair
aggregate relaxation.  A direct rigorous upper bound on its optimum is:

* each pair multiplier is `≤ 1` (the two-vertex pointwise constraint), so the
  disjoint-pair credit is at most `Σ L_e = 3 e_4(z) = 323/4480`;
* by monotonicity of each star LP in the weights, the overlapping-pair credit is
  at most `Σ_i LP_i(z_j z_k) = 383/6720`;
* positive triple/quadruple coefficients only reduce the credit.

Therefore

    F_star* ≤ 323/4480 + 383/6720 = 347/2688,
    g_star = g1 − F_star* ≥ 5989/2688 − 347/2688 = 2821/1344 = 2.09896… > 2,
    g_star − 2 ≥ 133/1344 ≈ 0.099.

So the one-coordinate star-pair aggregate relaxation cannot close the six-prime
corner; the residual gap is certified at least `133/1344`.

### 16.3 The next profile state: lcm-bin histograms (task K5)

The obstruction remains exactly as diagnosed in Section 15.4: overlapping
intersections have no individual positive lower bound.  The richer exact state
is the lcm-bin histogram

    h_d(b; U) = |{ u ∈ U : u ≡ b (mod d) }|.

For projected top classes `b_j mod d_j`, the joint base count is
`h_lcm(d_j)(b; U)` when the congruences are CRT-compatible, and `0` otherwise;
this is proved and brute-force-validated in `solver/profile_histogram.py`.  For
full-`p`-adic top classes `mod p^a e_j`, a compatible base contributes exactly
one of its `p` lifts (two lifts of the same base are distinct `mod p^a e_j`), so
the joint lift count equals the same compatible-base count.  This is the exact
finite-dimensional state from which a conditioned profile recurrence should be
built, replacing the scalar `μ_d(U)` of Task F1.

### 16.4 Status

Milestone 7 outcome is the *sharp obstruction* at the one-coordinate level: the
star-pair membership-pattern relaxation is certified insufficient, and the
joint lcm-bin histogram is the exact next state.  The full K3 atom-state LP
(pricing triples/quadruples through `y_{i,T}`) remains a larger exact
computation; the star-pair bound above already dominates its pair-level
contribution.

## 17. The lcm-histogram transition lemma (Milestone 8, L2)

The scalar profile `μ_d(U)` of Task F1 loses information because it forgets
which bins are CRT-compatible with an added lower-layer class.  The exact
Markovian state is the lcm-closed histogram family.

### Statement

Let `D` be an lcm-closed set of divisors of a period `L`, let `U ⊆ Z/LZ`, and
store `h_d(b; U) = |{u∈U : u ≡ b (mod d)}|` for every `d ∈ D`.  Suppose the
lower-layer class `r mod m` is added and `U' = U \ {x : x ≡ r (mod m)}`.  Then,
for every `d ∈ D` and `b mod d`:

* if `b` and `r` are CRT-incompatible (i.e. `b ≢ r (mod gcd(d, m))`), then
  `h'_d(b) = h_d(b)`;
* if compatible, let `c mod lcm(d, m)` be their unique CRT class; then
  `h'_d(b) = h_d(b) − h_{lcm(d,m)}(c)`.

### Proof

The elements removed from the bin `b mod d` are exactly those `x ∈ U` with
`x ≡ b (mod d)` **and** `x ≡ r (mod m)`.  This pair of congruences has a
solution only in the compatible case, and then its solutions are exactly one
residue class `c mod lcm(d, m)`.  The count of such elements is therefore
`h_{lcm(d,m)}(c)`.  ∎

The point of retaining `lcm(d, m)` (hence the lcm-closure of `D`) is exactly
that this single number is what the transition needs; with it the histogram
state is updated exactly, without enumerating the points of `U`.
Implementation and brute-force validation: `solver/profile_histogram.py`
(`histograms`, `transition_step`, `brute_transition`).

### Milestone 8 status

The L2 transition lemma above is proved and tested.  The full L1 K3 atom-state
LP (pricing every pair/triple/quadruple overlap at coordinate `i` through the
same `32`-atom distribution) is formulated in Section 16.1 but remains a large
exact computation; the star-pair bound of Section 16.2 is a rigorous lower
bound on its correction.  The next concrete steps are: solve/dualize the full
K3 LP, then use the L2 transition to build the first histogram-state profile
optimizer (L3) on the smallest surviving six-prime seed.

## 18. Full K3 32-atom relaxation is certified insufficient (Milestone 9, M9.1)

### 18.1 The local K3 atom LP

For a fixed prime coordinate `i ∈ {1,…,6}`, the five blocks
`B_{ij}` (`j ≠ i`) all have measure `z_i` in the `i`-th coordinate.  Write the
`2^5 = 32` membership-pattern atom masses

    y_{i,T} = measure{ x : x ∈ B_{ij} ⟺ j ∈ T },   T ⊆ [6]∖{i},

with the exact atom constraints

    y_{i,T} ≥ 0,   Σ_T y_{i,T} = 1,
    Σ_{T ∋ j} y_{i,T} = z_i   for every j ≠ i.

For a family `S ⊆ [6]∖{i}` of neighbours, the intersection of the blocks
`B_{ij}` (`j ∈ S`) has mass

    Σ_{T ⊇ S} y_{i,T}.

The full K3 model prices every such family simultaneously through the same atom
distribution.  If `β_S ≥ 0` are the global coefficients and

    p_S := ∏_{j∈S} z_j,

then the *worst-case* (most spread-out) weighted intersection mass allowed by
the atom constraints is the optimum of

    min_y  Σ_T y_{i,T} · Σ_{S⊆T} β_S p_S
    s.t.   the atom constraints above.                                   (L)

By strong LP duality this equals its dual

    max  v_0 + z_i Σ_{j≠i} v_j
    s.t. v_0 + Σ_{j∈T} v_j ≤ Σ_{S⊆T} β_S p_S   for every T.            (D)

The common optimum `LC_i` is the largest certified lower bound on the weighted
star-intersection mass, hence the largest credit that the single coordinate `i`
can contribute to the global correction; the `Σ_i LC_i` term below is therefore
an exact upper bound on the star-family part of that correction.

For the six-prime corner `{3,5,7,11,13,17}` and parameters

    z = (1/3, 1/2, 1/4, 1/8, 1/10, 1/14),

the exact local optima, each certified by a primal/dual pair stored in
`certificates/omega6_k3_atom.json` and independently re-checked by
`solver/k3_atom.py::verify_local`, are:

| coordinate i | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `LC_i` | 1/168 | 59/2380 | 1/664 | 0 | 0 | 0 |

The first three stars are the only nontrivial ones, as in the pair-level
Section 16 bound.  The exact primal and dual vectors are part of the certificate
and are verified with `Fraction` arithmetic only.

### 18.2 Decoupling the global coefficient certificate

The global BFF correction at `n = 6` splits into three disjoint sources:

* **Disjoint pairs.**  A pair of blocks `{I,J}` with `I∩J=∅` has exact
  intersection `∏_{i∈I∪J} z_i` and each pair multiplier is at most `1` (the
  two-vertex pointwise constraint).  The total disjoint-pair credit is therefore
  at most

      Σ_{I∩J=∅} ∏_{i∈I∪J} z_i = 3 e_4(z) = 323/4480.

* **Perfect matchings.**  A triple of pairwise-disjoint blocks (a perfect
  matching of the six coordinates) has exact intersection `∏_i z_i`.  Each such
  triple can carry a coefficient of size at most `2` under the pointwise
  constraint, and there are `15` perfect matchings, so their total credit is at
  most

      15 · 2 · ∏_{i=1}^{6} z_i = 1/896.

* **All remaining families.**  Every remaining pair/triple/quadruple family
  shares at least one prime coordinate, so its contribution is covered by one of
  the six local star LPs; their total is at most

      Σ_{i=1}^{6} LC_i = 19111/592620.

Hence the complete one-coordinate K3 star-atom relaxation satisfies

    F_K3 ≤ 323/4480 + 1/896 + 19111/592620 = 249997/2370480.

With `g1 = 5989/2688`,

    g_K3 = g1 − F_K3 ≥ 5989/2688 − 249997/2370480
                    = 13417473/6321280 = 2.122587… > 2,

and the residual gap above `2` is at least

    g_K3 − 2 ≥ 774913/6321280 = 0.122587….

### 18.3 Conclusion (M9.1)

The full one-coordinate `32`-atom K3 relaxation is therefore **rigorously
certified insufficient** at the six-prime corner: even its exact decoupling
bound leaves `g > 2`, so it cannot close the corner and cannot yield
`ω(N) ≥ 7`.  The obstruction is unchanged in character: no single-coordinate
atom state certifies enough positive overlap among the `B_{ij}`.  The next
state must couple at least two coordinates — the exact lcm-bin histogram state
of Section 17 and the profile optimizer of M9.3.

## 19. The first six-prime profile seed (Milestone 9, M9.2)

### 19.1 The surviving support pool is finite

The BFF 1987 necessary polynomial `g` is increasing in its parameters `w,z` on
the paper's domain, and the parameters are bounded above by their
infinite-exponent values.  Hence a six-prime support is excluded by BFF for
**all** exponent patterns exactly when the infinite-exponent value

    bff_bound(p_1, …, p_6) < 2.

Because `g` is monotone in each prime (larger primes shrink `w,z`), the
completion of a fixed prefix with the smallest available remaining primes
maximises `g`.  A complete DFS with that pruning proves that exactly **37**
six-prime supports can survive the BFF bound:

    {3,5,7,11,13,17}, {3,5,7,11,13,19}, {3,5,7,11,13,23}, …, 
    {3,5,7,11,17,31}, {3,5,7,11,19,23}, {3,5,7,13,17,19}.

Every other six-prime support is excluded by BFF 1987 (this is a rephrasing of
the published `ω ≥ 6` engine, **not** a new theorem).

### 19.2 The exact smallest surviving candidate

Over the 37 surviving supports, intersecting

* the all-primes primitive condition `p_i ≤ ∏_{j≠i}(a_j+1)`,
* abundance `σ(N) > 2N`, and
* the direct Lemma 4.10 bound `R(N) ≥ 1`,

and enumerating every exponent vector below the running minimum gives the
genuine smallest six-prime survivor:

    N* = 11486475 = 3^3 · 5^2 · 7 · 11 · 13 · 17,
    R(N*) = 677674/675675 = 1.0029585…,

with exponents `(3,2,1,1,1,1)`.  The first few survivors below `5 × 10^7` are:

| N | support | exponents | R(N) |
|---|---------|-----------|-------|
| 11486475 | 3,5,7,11,13,17 | 3,2,1,1,1,1 | 677674/675675 |
| 34459425 | 3,5,7,11,13,17 | 4,2,1,1,1,1 | 293467/289575 |
| 38513475 | 3,5,7,11,13,19 | 4,2,1,1,1,1 | 38894741/38513475 |
| 46621575 | 3,5,7,11,13,23 | 4,2,1,1,1,1 | 46839077/46621575 |

Implementation: `solver/omega6_seed.py` (`omega6_support_pool`,
`omega6_survivors`, `smallest_omega6_survivor`); tests in
`solver/test_omega6_seed.py`.  This is a finite discovery seed only; it is
**not** a claim that `N*` is a covering number.

### 19.3 The next step (M9.3)

`N*` is the smallest instance where the current filters stop: it is abundant,
satisfies the all-primes condition, has `R(N*) > 1`, and its support survives
the BFF forest bound.  The profile optimizer must now show either a strict
Hall/profile deficit for every realizable lower-uncovered set, or a precise
obstruction showing what extra state is missing.

## 20. The diagonal top-layer law and the insufficiency of scalar profiles (M9.3/M9.6)

### 20.1 Exact lift-coverage law

Let `N = p^a M`, `gcd(p,M)=1`, `L = N/p = p^{a−1}M`, and let `U ⊆ Z/LZ` be the
lower-uncovered set.  A top modulus is `p^a e` for `e | M`.  Fix a top class
`r mod p^a e`; write `d = p^{a−1}e`, `b = r mod d`, `c = (r−b)/d`, and
`m = M/e`.  For a base `u ≡ b (mod d)`, put `t = (u−b)/d`.  Then the unique
lift `u + sL` that meets the top class is given by the **diagonal law**

    t + s·m ≡ c  (mod p),        s ≡ m^{−1}(c − t)  (mod p).

*Proof.*  `u + sL ≡ r (mod p^a e)` is
`b + t p^{a−1}e + s p^{a−1}M ≡ b + c p^{a−1}e (mod p^a e)`.  Cancelling
`p^{a−1}e` gives `t + s(M/e) ≡ c (mod p)`.  Since `gcd(p,M)=1`,
`m = M/e` is invertible modulo `p`, giving the formula.  ∎

Thus, inside one `p × p` CRT fiber, a top class is a **diagonal**, not a
horizontal row of constant lift color.  This is the exact primitive implemented
and brute-force-validated in `solver/profile_optimizer.py`
(`lift_color`, `top_class_lifts`, `brute_top_class_lifts`).

### 20.2 The scalar profile is an insufficient state

The Task-F1 scalar profile

    μ_{p^{a−1}e}(U) = max_b |{ u ∈ U : u ≡ b (mod p^{a−1}e) }|

records only a cardinality for each top projection modulus.  It is **not** a
sufficient statistic for top-layer coverability.  The machine-checkable witness
in `solver/profile_optimizer.py::scalar_profile_insufficient_witness` is

    p = 3,  a = 2,  M = 4,  L = 12,
    U1 = {0},  U2 = {0,1}.

Both have identical scalar profile

    (μ_3, μ_6, μ_12) = (1, 1, 1),

but the top layer (`moduli 9, 18, 36`) covers all `p|U1| = 3` lifts of `U1` and
cannot cover all `p|U2| = 6` lifts of `U2`.  This is exact, not heuristic: the
coverability decision for each set is by exhaustive top-layer residue choice and
is independently re-checked by the brute-force lift enumerator.

### 20.3 Minimal augmentation

The lcm-bin histogram `h_d(b;U)` distinguishes the two witnesses because
`h_12(0;U1)=1, h_12(1;U1)=0` while `h_12(0;U2)=h_12(1;U2)=1`.  Thus the
minimal information missing from the scalar profile is the **joint lcm-bin
occupancy**, i.e. the histogram state of Section 17.  In the presence of the
full top-layer query family `{p^{a−1}e : e | M}`, that family is lcm-closed
only if it includes `L` (take `e = M`); hence the exact histogram state contains
`h_L`, which is precisely the indicator of `U`.  The diagonal law shows this
degeneration is unavoidable for *exact* top-layer feasibility: a top class
couples the base index `t` and the lift color `s`, so no cardinality-only state
shorter than `U` itself can decide coverability in general.

### 20.4 Status

Milestone 9 has reached the following exact, machine-checked facts:

* M9.1: the full one-coordinate K3 32-atom relaxation is certified
  insufficient (Section 18).
* M9.2: the first six-prime profile seed is `11486475` (Section 19).
* M9.3/M9.6 primitive: the top-layer lift-coverage law is diagonal, and the
  scalar Task-F1 profile is insufficient; the lcm-bin histogram is the minimal
  augmentation, and exactness forces the state to retain `h_L`, i.e. `U`.

The remaining bottleneck is therefore **not** a missing primitive law but the
exponential lower-layer optimization over realizable `U`.  A compressed exact
profile optimizer would have to solve the diagonal `p×p` fiber-cover problem
without enumerating `U`; no such compression is available from cardinality data
alone.

## 21. Lossy profile machinery and the compression barrier (Milestone 10)

### 21.1 The first-order dual is exactly abundance (N0)

For the covering problem on `Z/NZ` with distinct moduli `d | N`, the first-order
Farkas/weighted-set-cover dual is:

    y_x ≥ 0,  z_d ≥ 0,
    Σ_{x ≡ a (mod d)} y_x ≤ z_d    for every d | N, d > 1, and every a mod d.

Any valid distinct-modulus cover then gives `Σ_x y_x ≤ Σ_{d used} z_d`.

**Theorem.**  The translation-invariant first-order dual can prove `N` is not
covering exactly when `σ(N) < 2N`; for abundant `N` its optimum is `0`, and for
deficient `N` it is unbounded.

*Proof.*  The constraint system and the objective `Σ_x y_x` are invariant under
translating the point weights `y`, so the optimum may be taken with
`y_x = c` for all `x`.  The constraints become `c N/d ≤ z_d`.  Minimising
`Σ z_d` subject to those constraints gives

    Σ_x y_x − Σ_d z_d
      = cN − Σ_{d|N,d>1} cN/d
      = cN (2 − σ(N)/N)
      = c (2N − σ(N)).

This is positive for some `c > 0` iff `σ(N) < 2N`, and is otherwise maximised at
`c = 0`.  ∎  Hence no generic point-weight certificate can exceed the raw
abundance obstruction; in particular it cannot touch the abundant seed
`N* = 11486475`.  Implementation: `solver/m10_profile.py::first_order_dual_status`.

### 21.2 Safe head/tail truncation (N1)

For `N = p^a M`, partition the top divisors `e | M` into a head `H` and tail
`T`.  Let `C_H(U)` be the maximum number of lifts coverable by top moduli
`p^a e` with `e ∈ H`, and let `C_top(U)` use all `e`.  Then

    C_top(U) ≤ C_H(U) + Σ_{e∈T} min(M/e, |U|).                    (T)

*Proof.*  The union over all top classes is contained in the union over the
head classes together with the union over the tail classes; the tail union has
size at most the sum of the sizes of its classes.  A tail class `mod p^a e`
contains `M/e` points of `Z/NZ` and meets at most one lift of each base, hence
at most `min(M/e, |U|)` of the `p|U|` lifted points.  ∎  The point of (T) is
that the expensive `e = M` modulus has capacity only `1`; we may pay it as a
tail budget rather than retain `h_L`.

### 21.3 The exact head signature (N3)

For a head `H ⊆ {e : e | M}`, every retained top class `r mod p^a e` depends on
the base `u` only through `u mod p^a e` (Section 20.1).  Therefore the coarsest
equivalence relation on bases that preserves all retained top-class incidences
is

    u ∼ v  ⟺  u ≡ v  (mod p^a · lcm(H)).

The counts of `U` in the residue classes modulo `Q = p^a · lcm(H)` are thus a
lossless state for the head evaluation: `C_H(U)` can be computed from

    h_Q(c; U) = |{u ∈ U : u ≡ c (mod Q)}|,

without knowing the individual points of `U`.  This is implemented and
brute-force-validated in `solver/m10_profile.py` (`head_signature_counts`,
`max_top_coverage`).

### 21.4 The compression barrier (C)

For `N = 36 = 3^2 · 4` (`p=3,a=2,M=4,L=12`) and the lossy head `H = {1}`
(`Q = 9 < L`), the following two states are both **realizable** by valid
distinct lower-layer classes and have identical head-signature counts:

    U1 = {5,10,11}  (lower classes mod 3,4,6,12: 0,0,1,2),
    U2 = {2,5,10}   (lower classes mod 3,4,6,12: 0,0,1,11),

with `h_9(U1) = h_9(U2) = {1:1, 2:1, 5:1}`, yet

    C_top(U1) = 5,   C_top(U2) = 4.

This is a machine-checkable sharp compression barrier for the N3 head-signature
feature: the single head modulus `e=1` cannot distinguish states with different
full top capacity.  The minimal next correlation is the **next head modulus**
(here `e=2`, signature `u mod 18`), which strictly separates the two states.
Implementation and verifier:
`solver/m10_profile.py::head_signature_barrier_witness`.

### 21.5 Status

Milestone 10 has established:

* N0: the generic first-order dual is exactly the abundance obstruction.
* N1: a safe head/tail truncation with tail budget `Σ min(M/e, |U|)`.
* N2: `solver/m10_profile.py::head_candidates` enumerates divisor-closed heads
  by signature modulus and tail budget (48 heads for the seed `p=3` direction).
* N3: the exact head signature `u mod p^a lcm(H)` and its sufficiency for
  `C_H(U)`.
* C: a realizable compression barrier for the lossy head-signature feature,
  with the next head modulus identified as the minimal missing correlation.

The full CEGAR/Bellman seed verdict (N4–N6) remains open; the barrier above is
the precise reason a nontrivial lossy head cannot be evaluated without deciding
which tail/coarser correlations to retain.
