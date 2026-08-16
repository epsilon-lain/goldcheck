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

## 4. Classification of the facts used in this repository

### 4.1 Exact published theorem

* McNew–Setty Lemma 3.1 (largest-prime bound `P⁺(n) ≤ τ(n/P⁺(n))`).
* McNew–Setty Lemma 4.10 (inclusion–exclusion CRT bound).
* Mian–Siddique capacity certificate (`capacity_exclusion`).
* Hough–Nielsen restricted-divisibility theorem.
* Balister–Bollobás–Morris–Sahasrabudhe–Tiba square-free exclusion.

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
certificates only show that `10395`, `12285`, and `17325` are not covering
numbers; the next bottleneck is turning the raw `σ(M)` term in the recurrence
into a sharper CRT/Hall capacity (see `NOTES.md`).
