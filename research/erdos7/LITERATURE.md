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

## 5. What this repository does *not* claim

No finite computation is used to claim the open problem is solved.  The three
certificates only show that `10395`, `12285`, `17325`, and (via the full bound)
`51975` are not covering numbers.  The direct Lemma 4.10 bound proves the
published `ω ≥ 5` consequence (`ω ≤ 4` is impossible) but does **not** reach the
published `ω ≥ 6` result; the current frontier and next bottleneck are the
`ω = 5` survivors of the direct bound, beginning with
`70945875 = 3^4 · 5^3 · 7^2 · 11 · 13` (see `NOTES.md` Section 11).
