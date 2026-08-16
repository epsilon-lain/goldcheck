# AGENTS.md

You are working in `epsilon-lain/goldcheck` on the Erdős–Selfridge odd distinct covering-system problem.

Your primary task is defined in:

- `research/erdos7/CODEX_TASK.md`
- GitHub issue #1: `[Codex] Erdős #7 — attack odd distinct covering systems`

## Immediate execution order

1. Read `research/erdos7/CODEX_TASK.md` completely.
2. Read the latest comments on GitHub issue #1 and treat the newest actionable milestone brief as the current priority.
3. Perform the requested mathematical/computational work autonomously; do not stop at a plan.
4. Maintain `research/erdos7/LITERATURE.md`, `NOTES.md`, solver code, tests, and certificates as appropriate.
5. Falsify theorem candidates computationally before presenting them as valid.
6. If a theorem candidate survives, formalize it in Lean 4 when requested. Final theorem paths must contain no `sorry`, no new `axiom`, and no `native_decide`.
7. Run all relevant tests and record exact commands, runtimes, and outcomes.
8. Commit every coherent milestone with a descriptive commit message.
9. Push the milestone to `origin/master` yourself and verify that the remote contains the commit.
10. Report the commit SHA, exact mathematical status, verification results, and next bottleneck.

## Working discipline

- Work autonomously; do not ask the user to run routine shell, Git, test, solver, file-management, or push commands that you can run yourself.
- Prefer producing code, proofs, tests, certificates, and committed artifacts over discussion.
- Do not claim the full open problem is solved from any finite computation.
- Never silently assume a covering uses every divisor of `N`; each divisor modulus may be unused, but no modulus may be repeated.
- Keep counterexamples to failed lemmas.
- Use exact integer/rational arithmetic for certificates.
- When an external solver is used, also provide a small independent verifier for emitted certificates when practical.
- Preserve the distinction between published theorems, straightforward consequences, apparently unpublished observations, computational evidence, and genuinely new proved statements.

## Autonomous Git / repository operations

You are responsible for the repository lifecycle during a work session. In particular:

1. Before work, run `git status` and inspect the current branch/history.
2. Work from the repository root; if the shell starts elsewhere, locate and `cd` to the `goldcheck` repository yourself.
3. Stage only intended files and review the diff before committing.
4. Commit coherent milestones with descriptive messages.
5. Run `git push origin master` after every completed milestone unless a different branch is explicitly requested.
6. If push fails with a transient network error such as connection reset, timeout, TLS/HTTP transport failure, or temporary DNS failure, retry with reasonable backoff. Do not hand this routine retry back to the user.
7. If authentication or permissions genuinely prevent pushing, preserve the local commit and report the exact blocker; do not discard work.
8. After pushing, verify with `git status` plus a remote-aware command (`git fetch`, `git log origin/master -1`, or equivalent) that the milestone is present remotely.
9. Never force-push, rewrite published history, delete branches, or discard user work unless explicitly instructed.
10. Keep the working tree clean at milestone boundaries when practical.

## Continuous milestone workflow

After completing one milestone:

1. Push and verify it remotely.
2. Re-read the latest GitHub issue #1 comments.
3. If a newer actionable milestone exists, execute it immediately in the same autonomous style.
4. If no newer brief exists, continue the mathematically natural next step already designated in the current brief rather than stopping merely because one subtask completed.
5. Stop only at a genuine mathematical/computational bottleneck, an external dependency that cannot be resolved locally, or a completed milestone that explicitly requires review before further work.

## Current research direction

Milestones 1 and 2 established the all-primes primitive condition, the deficiency recurrence, exact certificates for the first targets, the power-lifting criterion, and infinite excluded exponent families. The present bottleneck is to sharpen the raw top-layer `sigma(M)` charge using conditioned CRT/Hall information, with `N = 51975 = 3^3 * 5^2 * 7 * 11` as the first concrete survivor to attack. Read the newest issue #1 comment for the exact current task.

Begin immediately. Do not merely restate this file.