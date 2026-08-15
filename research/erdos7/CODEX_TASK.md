# Codex task: Erdős #7 — odd distinct covering systems

## Mission
Work on Erdős problem #7: determine whether there exists a covering system of the integers by congruence classes with pairwise distinct odd moduli greater than 1.

Do not claim a solution from finite search. The target is either an explicit valid odd distinct cover, or a rigorous obstruction that applies to an infinite class and can plausibly be iterated to all odd LCMs.

## Literature baseline to verify first
- Erdős Problems #7 (current public status: open).
- Hough–Nielsen, *Covering systems with restricted divisibility*.
- Balister–Bollobás–Morris–Sahasrabudhe–Tiba, *The Erdős–Selfridge problem with square-free moduli* and related density paper.
- McNew–Setty, *On the densities of covering numbers and abundant numbers* (arXiv:2507.23041; Math. Comp. 2026).
- Mian–Siddique, *Kernel-Checked Exclusions for the Erdős-Selfridge Odd Covering Problem* (arXiv:2607.25628), and `ibrahimmian36/centurion`.
- Bispels et al., *A further investigation on covering systems with odd moduli*, Discrete Math. 349 (2026), 115013.

## Model
A positive integer `N` is a covering number if there is a distinct covering system whose moduli all divide `N`. If an odd covering exists, take an odd primitive covering number `N` (no proper divisor is a covering number). Work in `Z/NZ` using the CRT decomposition.

## Lemma candidate 1 — check literature, then prove/formalize
For every prime `p | N`, let `a = v_p(N)` and `M = N / p^a`. Conjectured necessary condition for primitive covering `N`:

`p <= tau(M)`.

Proof sketch to audit:
1. `N/p` is not a covering number by primitivity.
2. In a fixed covering of `N`, the subfamily of moduli dividing `N/p` therefore misses some residue `y (mod N/p)`.
3. `y` has exactly `p` lifts modulo `N`.
4. Any modulus that can cover one of these lifts but is not in the lower subfamily must have full p-adic exponent `a`, hence is `p^a e` for some `e | M`.
5. One congruence class modulo `p^a e` meets at most one of those `p` lifts: the difference of two lifts is `(k-k') p^(a-1) M`, which is not divisible by `p^a e` for distinct `k,k' mod p` because `gcd(p,M)=1`.
6. Distinct moduli give distinct `e`, so at least `p` divisors `e | M` are needed. Thus `p <= tau(M)`.

McNew–Setty explicitly use the analogous inequality for the largest prime divisor; determine whether the all-primes version is already known. If it is known, cite it. If not, preserve a clean proof but do not call it novel until checked.

## Lemma candidate 2 — deficiency recurrence
Let `r(n)` be the maximum number of residues modulo `n` coverable by congruence classes with pairwise distinct moduli `d>1` dividing `n`, and let `delta(n)=n-r(n)`.

For `N=p^a M` with `gcd(p,M)=1`, audit/prove the raw inequality

`delta(p^a M) >= p*delta(p^(a-1) M) - sigma(M)`.

Reason: lower p-adic layers cover at most `p*r(N/p)` lifts; top-layer moduli `p^a e` (`e|M`) have raw total capacity `sum_{e|M} M/e = sigma(M)`.

This bound is expected to be too weak alone. The main goal is to replace the raw `sigma(M)` capacity by a sharper CRT/Hall capacity term that accounts for forced overlaps and the fact that each top-layer congruence selects only one lift in each p-fiber it meets.

## Main research direction — multi-fiber Hall/CRT obstruction
For the uncovered set `U` modulo `N/p` left by the lower layer, model the `p|U|` lifted points as a bipartite/fiber-cover problem. Each top modulus `p^a e` induces a structured partial matching/diagonal across p-fibers, not an arbitrary subset.

Derive Hall-type necessary inequalities for subsets of fibers and/or CRT boxes. Seek an inequality depending only on the divisor lattice / prime-power exponents. It should specialize to the Mian–Siddique capacity certificate but be stronger on their first simple-bound failures `10395`, `12285`, `17325`.

## Exact computational discovery
Implement a reproducible exact solver, but use it to mine symbolic certificates rather than to claim the open problem solved.

Requirements:
- variables: for each divisor `d|N, d>1`, choose one residue `a_d mod d` or mark unused;
- all chosen residue classes must cover `Z/NZ`;
- exploit CRT product structure; avoid naively materializing all `N` residues for large `N`;
- use CP-SAT / SAT / MILP if available, otherwise emit DIMACS and provide an independent verifier;
- generate odd primitive candidates using known necessary filters: abundant, non-squarefree, LCM divisible by 9 or 15, and Lemma candidate 1 if validated;
- first reproduce known exclusions and produce compact certificates for `945`, `10395`, `12285`, `17325`;
- then scan odd candidates below `10^6` and compare with McNew–Setty's classification.

For every UNSAT instance, try to extract one of:
- a small CRT capacity certificate;
- a Hall deficit on a small family of fibers;
- a dual LP/Farkas certificate;
- an unsat core that can be translated into a human inequality.

Cluster certificates by prime exponent pattern and attempt to generalize each cluster into an infinite-family theorem.

## Secondary structural experiment
Investigate the empirical statement that known almost-covering numbers are even. Test:

> There is no odd `n>1` with `r(n)=n-1`.

Also test whether every primitive covering number has a proper divisor with deficiency 1, or more weakly deficiency bounded in terms of a prime factor. Search for counterexamples before attempting proof.

## Formal verification
If a lemma survives literature review and computational falsification, formalize it in Lean 4. Reuse ideas/code from `ibrahimmian36/centurion` where appropriate, especially the bridge between integer coverings and finite `Z/NZ` checks.

Final theorem path: no `sorry`, no new `axiom`, no `native_decide`.

## Deliverables
- `research/erdos7/LITERATURE.md`
- `research/erdos7/NOTES.md`
- `research/erdos7/solver/`
- `research/erdos7/certificates/`
- Lean files for any theorem candidate that survives

At every milestone record: exact claim, proof status, counterexamples tried, command, runtime, and whether the result is mathematical or merely computational.

Start now with Lemma candidate 1, then implement the first exact solver/certificate miner for 10395, 12285, and 17325.