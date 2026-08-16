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
