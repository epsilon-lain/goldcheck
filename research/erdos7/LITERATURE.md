# Literature check: Erdős #7 (odd distinct covering systems)

Status of the core problem, and the exact provenance of every statement we rely
on.  Everything below was checked against the primary sources (arXiv pages,
published journals, and the Lean sources of the cited repository) on 2026-08-16.

## 1. The open problem

**Erdős problem #7** asks whether there is a covering system of the integers by
congruence classes with pairwise distinct moduli, all odd and greater than 1.
The problem remains **open**; see <https://www.erdosproblems.com/7>.

Two landmark partial results are cited throughout the literature:

* **Hough–Nielsen**, *Covering systems with restricted divisibility*, Duke
  Math. J. **168** (2019), 3261–3295.  In particular, any distinct covering
  system has a modulus divisible by 2 or by 3.  Hence an **odd** distinct
  covering system, if it existed, would have lcm divisible by 3.

* **Balister–Bollobás–Morris–Sahasrabudhe–Tiba**, *The Erdős–Selfridge
  problem with square-free moduli* (and the related *The Erdős covering
  problem: the density of the uncovered set*, Invent. Math. **228** (2022)).
  There is **no** distinct covering system whose moduli are all odd and
  square-free.  Combining the two results, any odd covering lcm would have to
  be divisible by 9 or 15.

* **Berger–Felzenbaum–Fraenkel**, *Necessary condition for the existence of an
  incongruent covering system with odd moduli*, Acta Arith. **45** (1986)
  375–379 (Zbl 0533.10001): an odd distinct covering system has at least
  **five** distinct prime factors.  The sequel *… II*, Acta Arith. **48**
  (1987) 73–79 (Zbl 0623.10004), proves at least **six** distinct prime
  factors.  These are the current published frontier facts for the
  non-square-free odd case.

* **Bispels–Cohen–Harrington–Lowrance–Pontes–Schaumann–Wong**, *A further
  investigation on covering systems with odd moduli*, Discrete Math. **349**
  (2026) 115013 (arXiv:2507.16135).  This treats repeated-modulus variants and
  does **not** resolve Erdős #7.

## 2. The covering-number model

Following **McNew–Setty**, *On the densities of covering numbers and abundant
numbers*, arXiv:2507.23041 (v2, 10 Feb 2026; Math. Comp. 2026):

* an integer `n` is a **covering number** if there is a distinct covering
  system in which every modulus divides `n`;
* `r(n)` is the maximum number of residue classes modulo `n` coverable by
  congruence classes with distinct moduli `d > 1`, `d | n`;
* `c(n) := 1 + r(n)/n`, so `n` is a covering number iff `c(n) = 2`.

This is exactly the model used by the solver in `solver/`.

## 3. Exact published statements we use

### 3.1 McNew–Setty Lemma 3.1 (largest prime)

If `n` is a primitive covering number then

    P⁺(n) ≤ τ(n / P⁺(n)).

This is Lemma 3.1 of McNew–Setty (arXiv:2507.23041).  We verified the statement
and its proof directly in the published PDF.  It is the *largest*-prime form of
the inequality.

### 3.2 McNew–Setty Lemma 4.10 (CRT / inclusion–exclusion capacity)

For any multiset `M = {m_1, …, m_k}` of moduli, the proportion of integers
covered by any residue system whose moduli are the elements of `M` is at most

    ∑_{S ⊆ M, S ≠ ∅, S pairwise coprime} (−1)^{|S|+1} / lcm(S).

This is Lemma 4.10 of McNew–Setty, proved by the Chinese remainder theorem and
inclusion–exclusion.  It is the **key CRT/Hall inequality** used below.

### 3.3 Mian–Siddique capacity certificate

**Mian–Siddique**, *Kernel-Checked Exclusions for the Erdős–Selfridge Odd
Covering Problem: Any Odd Covering of ℤ Has lcm Exceeding 10000*,
arXiv:2607.25628 (cs.LO), with Lean 4 sources in
`github.com/ibrahimmian36/centurion`.

Their formalized capacity certificate (`Erdos7/Capacity.lean`,
`capacity_exclusion`) states: if `T` is a set of pairwise-coprime divisors of
`N` (each `> 1`) and

    ∑_{d ∈ D(N) \ {1}, d ∉ T} N/d  <  (N / ∏_{d∈T} d) · ∏_{d∈T} (d − 1),

then no system of congruence classes with distinct moduli `> 1` dividing `N`
covers `[0, N)`.  The repository uses this to exclude all 23 odd abundant
`N < 10 000` and proves the headline `lcm > 10000`; the three stragglers
`10395`, `12285`, `17325` are the first odd abundant numbers **above** 10000 and
are **not** closed by that certificate alone.

### 3.4 Berger–Felzenbaum–Fraenkel odd-moduli necessary conditions

* **Berger, M. A., Felzenbaum, A., Fraenkel, A. S.**, *Necessary condition for
  the existence of an incongruent covering system with odd moduli*, Acta Arith.
  **45** (1986), 375–379 (Zbl 0533.10001).  Proves that an incongruent covering
  system with all moduli odd must have at least **five** distinct prime factors.

* **Berger, M. A., Felzenbaum, A., Fraenkel, A. S.**, *Necessary condition for
  the existence of an incongruent covering system with odd moduli II*, Acta
  Arith. **48** (1987), 73–79 (Zbl 0623.10004).  Proves at least **six**
  distinct prime factors.

These two papers are the current published frontier for the (not necessarily
square-free) odd distinct case.  In particular, our full-bound corollary that
every odd covering number has `ω(n) ≥ 5` is already the 1986 result, and the
1987 result (`ω(n) ≥ 6`) is strictly stronger than anything derivable from the
direct McNew–Setty Lemma 4.10 bound alone.

The 1987 theorem is `g(w, z) ≥ 2` for the `(n+1)`-variate polynomial built from
the direct product-set union bound and a **forest** overlap correction; the
proof uses the forest inequality
`|⋃ S_v| ≤ Σ|S_v| − Σ_{uv∈E}|S_u∩S_v|` on the 2-subsets of the prime
coordinates.  We audited the scanned PDF directly and reconstructed this engine
in `solver/bff1987.py` (see `NOTES.md` Section 13); the reconstruction is
validated by reproducing the published `ω ≥ 6`, not claimed as new.
The higher-order overlap optimizations of Sections 14–15 (`ω = 6` pair/triple
and pair/triple/quadruple coefficient certificates) are exact computational
consequences of the audited BFF product-set structure; they likewise are not new
theorems, and their insufficiency certificates are recorded with exact rational
dual witnesses in `solver/higher_overlap.py`.

## 4. Classification of the facts used in this repository

### 4.1 Exact published theorem

* McNew–Setty Lemma 3.1 (largest-prime bound `P⁺(n) ≤ τ(n/P⁺(n))`).
* McNew–Setty Lemma 4.10 (inclusion–exclusion CRT bound).
* Mian–Siddique capacity certificate (`capacity_exclusion`).
* Hough–Nielsen restricted-divisibility theorem.
* Balister–Bollobás–Morris–Sahasrabudhe–Tiba square-free exclusion.
* Berger–Felzenbaum–Fraenkel 1986 (`ω ≥ 5` for odd distinct coverings).
* Berger–Felzenbaum–Fraenkel 1987 (`ω ≥ 6` for odd distinct coverings).

### 4.2 Straightforward consequence

* **All-primes lemma**: for a primitive covering number `N`, every prime
  `p | N` satisfies `p ≤ τ(N / p^{v_p(N)})`.  This is the statement obtained by
  rerunning the McNew–Setty Lemma 3.1 proof for an arbitrary prime factor `p`
  and counting the `p`-saturated divisors `p^{v_p(N)} · e` (`e | M`) exactly:
  their count is `τ(M)`.  We do **not** claim this as a new theorem; it is a
  direct sharpening of the published argument.

* **Square-free CRT/Hall bound**: for odd square-free `n = ∏ p_i`,

      r(n) ≤ ∑_{∅≠U⊆[k]} C_|U| ∏_{i∉U} p_i,
      C_j = ∑_{t=1..j} (−1)^{t+1} S2(j,t),

  where `S2` is the Stirling number of the second kind.  This is Lemma 4.10
  evaluated on the full divisor set `D_{>1}(n)`; see `NOTES.md`.

* **Full prime-power form of Lemma 4.10** (`R(n) = Σ_U C_|U| ∏_{i∈U} x_i`):
  a direct grouping of McNew–Setty equation (10) by prime support; see
  `NOTES.md` Section 8.  It is a reformulation, not a new theorem.

* **Every odd `n` with `ω(n) ≤ 4` is non-covering**: proved from the full
  form by a monotonicity argument.  This is a straightforward consequence of
  Lemma 4.10, and it is **subsumed** by Berger–Felzenbaum–Fraenkel 1986
  (`ω ≥ 5`); we do not claim novelty.

* **Five-prime large-prime family** (`q ≥ 23`): proved from the full form by
  the same monotonicity machinery.  A straightforward consequence of Lemma
  4.10, and **subsumed** by Berger–Felzenbaum–Fraenkel 1987 (`ω ≥ 6`).

* **Forest reformulation of BFF 1987**: the Kneser-graph / maximum-weight
  spanning-tree overlap engine in `solver/bff1987.py`.  This is an equivalent
  reformulation (with an exact rational verifier) of the forest step in the
  published paper, **not** a new theorem.

### 4.3 Apparently unpublished / folklore-adjacent observation

* **Deficiency recurrence**: for `N = p^a M`, `gcd(p, M) = 1`,

      δ(N) ≥ p · δ(N/p) − σ(M),   δ(n) := n − r(n).

  This "raw top-layer capacity" argument is the same counting that drives
  McNew–Setty Lemma 4.1 (`c(n) ≤ σ(n)/n`), split one `p`-adic step at a time.
  It is elementary and we prove it in full; we do not claim novelty.

* **The chained certificates** `945 → 123`, `10395 → 360`, `12285 → 606`,
  `17325 → 312` (positive lower bounds on `δ`), obtained by combining the
  proved recurrence with the square-free CRT/Hall bound.  These are concrete
  computational instantiations of the two proved lemmas, not a new theorem.

* **Conditioned top-layer profile inequality** (Section 12 of `NOTES.md`): for
  `N = p^a M`, the full-`p`-adic top layer covers at most
  `Σ_{e|M} μ_{p^{a−1}e}(U)` of the `p|U|` lifts of a lower-uncovered set `U`.
  This is an elementary counting lemma; we prove and exhaustively test it but do
  not claim novelty, and we have not located an exact published statement.

* **Lcm-histogram transition lemma** (Section 17 of `NOTES.md`): the family
  `h_d(b;U)` is Markovian under removing one lower-layer class when the divisor
  family is lcm-closed.  This is an elementary CRT consequence proved and
  brute-force-validated in this repository; we do not claim it as a published
  theorem.

* **Exact insufficiency certificates for the one-coordinate star-pair, K3
  32-atom, pair+triple, and pair+triple+quadruple coefficient bases** (Sections
  14–18 of `NOTES.md`).  These are exact computational consequences of the
  audited BFF product-set structure, not new theorems; their rational dual
  witnesses are independently verified in `solver/`.

## 5. What this repository does *not* claim

No finite computation is used to claim the open problem is solved.  The three
certificates only show that `10395`, `12285`, `17325`, and (via the full bound)
`51975` are not covering numbers.  The direct Lemma 4.10 bound proves the
published `ω ≥ 5` consequence (`ω ≤ 4` is impossible) but does **not** reach the
published `ω ≥ 6` result.  The audited BFF 1987 forest method reproduces
`ω ≥ 6`, and the repository currently has no proof of `ω ≥ 7`; the six-prime
corner `{3,5,7,11,13,17}` remains open at the level of the K3/profile states.

## 6. Milestone 9 literature sanity check (M9.0)

On 2026-08-17 we searched primary sources and recent literature for any
post-1987 strengthening of the BFF `ω ≥ 6` theorem, any `ω ≥ 7` claim, and any
prior use of conditioned CRT/profile/histogram states for odd incongruent
covering systems.

### 6.1 No post-1987 general `ω ≥ 7` found

We did **not** find a published theorem asserting that an odd distinct covering
system must have at least seven distinct prime factors.  The 1987 result

* **Berger–Felzenbaum–Fraenkel**, *Necessary condition for the existence of an
  incongruent covering system with odd moduli. II*, Acta Arith. **48** (1987)
  73–79 (Zbl 0623.10004),

remains, to our knowledge, the published frontier for the unrestricted
non-square-free odd distinct case: it proves `ω ≥ 6`.  Our repository
reproduces this (Section 13 of `NOTES.md`) but does **not** extend it to
`ω ≥ 7`.

### 6.2 Square-free results do not give a general `ω ≥ 7`

The square-free case is much stronger but does **not** transfer to the
non-square-free setting:

* **Song Guo and Zhi-Wei Sun**, *On odd covering systems with distinct moduli*,
  Adv. Appl. Math. **35** (2005) 182–187 (arXiv:math/0412217): a square-free
  odd distinct covering system, if it existed, would have lcm with at least
  **22** distinct prime divisors.

* **Balister–Bollobás–Morris–Sahasrabudhe–Tiba**, *The Erdős–Selfridge problem
  with square-free moduli*, Algebra Number Theory **15** (2021) 609–626
  (arXiv:1901.11465): such a square-free odd distinct covering does **not**
  exist at all.  This supersedes the Guo–Sun `22`-prime necessary condition.

Neither result constrains a hypothetical odd covering whose lcm has a squared
prime divisor; in particular, neither implies `ω ≥ 7` in the unrestricted case.

### 6.3 Provenance of the repository's higher-order/profile statements

The one-coordinate star-collision lower envelopes, the K3 32-atom relaxation,
the pair/triple and order-4 coefficient certificates, the conditioned top-layer
profile inequality, and the lcm-histogram transition lemma are all formulated
and machine-checked in this repository.  They are exact computational or
elementary counting consequences of the published BFF product-set structure and
the CRT; we classify them as **straightforward consequences / apparently
unpublished observations**, and we do **not** claim any of them as a published
theorem or as a solution of Erdős #7.

## 7. Milestone 12 — the distortion method (primary sources)

### 7.1 Hough–Nielsen Theorem 4 (the general LLL/weights layer)

From **Hough–Nielsen**, *Covering systems with restricted divisibility*,
arXiv:1703.02133, Theorem 4.  For a finite modulus collection `N`, with a
residue set `a_n mod n` for each `n ∈ N`, if there are weights `x_p ≥ 0`
satisfying

    x_p ≥ Σ_{n ∈ N, p | n} (|a_n mod n| ∏_{p' | n}(1 + x_{p'})) / n

for every prime `p`, then the uncovered set `R` satisfies

    |R mod Q|/Q ≥ exp( −Σ_{n ∈ N} (|a_n| ∏_{p|n}(1+x_p)) / n ) > 0

and, for every `n ∈ N`,

    max_b |R ∩ (b mod n)| / |R| ≤ exp( Σ_{p|n} x_p ) / n.

This theorem makes **no square-freeness assumption** on the moduli `n`.  It is
implemented exactly in `solver/distortion.py` (`hn_weights`,
`hn_uncovered_density`, `hn_concentration`).

### 7.2 BBMST square-free geometric sieve

From **Balister–Bollobás–Morris–Sahasrabudhe–Tiba**, *The Erdős–Selfridge
problem with square-free moduli*, arXiv:1901.11465, Theorem 1.2.  With
`S_k = [p_{k+1}]` and hyperplanes
`A = A_1 × … × A_n` where each `A_k` is either full or a singleton, a cover of
the box by hyperplanes forces two parallel hyperplanes.  The translation from a
square-free modulus `d = ∏_{i∈I} p_i` to a hyperplane with fixed-coordinate set
`I` uses square-freeness **essentially**: distinct square-free moduli correspond
to distinct fixed-coordinate sets.  For a non-square-free modulus this
correspondence fails, because the moduli `p^1, p^2, …` all have the same
square-free part `p`.

### 7.3 Classification for the prime-power transfer

* **Hough–Nielsen Theorem 4**: remains literally valid for repeated prime
  powers; brute-force-validated here on `N=9` and `N=27`.
* **BBMST/Hough–Nielsen Shearer geometric sieve (Theorem 1.2 / Theorem 2)**:
  the hyperplane/fixed-coordinate translation does **not** survive repeated
  prime powers, because distinct moduli can share the same square-free part.
* **Replacement quantity**: group moduli by square-free part and bound their
  union by the McNew–Setty prime-power factor
  `x_p = Σ_{j=1}^{v_p(N)} p^{-j}`; the missing joint/conditional structure is
  the diagonal `p×p` lift law of `NOTES.md` Section 20.
