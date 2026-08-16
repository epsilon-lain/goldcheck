# AGENTS.md

You are working in `epsilon-lain/goldcheck` on the Erdős–Selfridge odd distinct covering-system problem.

Your primary task is defined in:

- `research/erdos7/CODEX_TASK.md`
- GitHub issue #1: `[Codex] Erdős #7 — attack odd distinct covering systems`

## Immediate execution order

1. Read `research/erdos7/CODEX_TASK.md` completely.
2. Perform a literature check for the proposed all-primes primitive-covering lemma
   `p <= tau(N / p^v_p(N))` for every prime `p | N`.
3. Write the result to `research/erdos7/LITERATURE.md`, distinguishing:
   - exact published theorem;
   - straightforward consequence;
   - apparently unpublished observation.
   Do not call anything novel unless verified.
4. Prove or refute the all-primes lemma carefully. If valid, write a polished proof in `research/erdos7/NOTES.md` and add tests checking the arithmetic condition on candidate `N`.
5. Implement an exact CRT-aware solver/certificate miner under `research/erdos7/solver/`.
6. First targets: `N = 10395`, `12285`, `17325`.
7. For each target, obtain an exact UNSAT/non-covering certificate and attempt to compress it into a human-readable CRT/Hall inequality under `research/erdos7/certificates/`.
8. Try to generalize certificate patterns to infinite families. Falsify each generalization computationally before writing it as a theorem candidate.
9. If a theorem candidate survives, formalize it in Lean 4. Final theorem path must contain no `sorry`, no new `axiom`, and no `native_decide`.
10. Run all relevant tests and record exact commands, runtimes, and outcomes.

## Working discipline

- Work autonomously; do not stop after planning.
- Prefer producing code, proofs, tests, and certificates over discussion.
- Do not claim the full open problem is solved from any finite computation.
- Never silently assume a covering uses every divisor of `N`; each divisor modulus may be unused, but no modulus may be repeated.
- Keep counterexamples to failed lemmas.
- Use exact integer/rational arithmetic for certificates.
- When an external solver is used, also provide a small independent verifier for emitted certificates when practical.
- Commit coherent milestones with descriptive commit messages.

## First milestone definition of done

The first milestone is complete only when all of the following exist:

- `research/erdos7/LITERATURE.md` with verified citations/statements;
- `research/erdos7/NOTES.md` with the audited all-primes lemma proof or a concrete counterexample;
- executable solver code with tests;
- at least one exact certificate or independently checked UNSAT result for one of `10395`, `12285`, `17325`;
- a concise status summary identifying the next mathematical bottleneck.

Begin immediately. Do not merely restate this file.