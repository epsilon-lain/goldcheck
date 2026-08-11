# goldcheck

A minimal Rust CLI that validates JSONL files of AI dataset gold cases. It reads
a file line by line, reports per-line validation errors with their 1-based line
number, and prints a final count of valid and invalid records.

## Why this topic

AI dataset curation relies on gold-standard annotations being both well-formed
and internally consistent. A lightweight checker that catches malformed records,
schema violations, and duplicate case identifiers helps keep datasets correct
before they are used to train or evaluate models. Rust was chosen for a safe,
dependency-light, fast single-binary tool with no runtime interpreter to ship.

## Supported JSONL input format

One JSON value per line. Blank (whitespace-only) lines are ignored. Each
non-empty line should be a JSON **object** with at least two fields:

```json
{"case_id": "case-001", "gold_label": "pass"}
```

- `case_id` — a non-empty string uniquely identifying the case.
- `gold_label` — the expected outcome for the case.

Other top-level fields, if present, are accepted but not inspected yet.

## Current validation rules

For each non-empty line, evaluated in order:

1. The line must be valid JSON.
2. The parsed value must be a JSON **object**.
3. The object must contain a `case_id` field that is a **non-empty string**
   (`case_id` is trimmed before the emptiness check).
4. The object must contain a `gold_label` field that is a **string**.
5. `gold_label` must be exactly `"pass"` or `"fail"`.
6. `case_id` values are compared **case-sensitively**. A `case_id` already seen
   in a *valid* record is reported as a duplicate.

Key semantics:

- Processing never stops on an error; every non-empty line is counted as
  either valid or invalid.
- `case_id` duplicate detection is **case-sensitive** and uses the value as-is
  (no normalization beyond the non-empty trim check).
- A record that fails JSON parsing or any schema/gold-label rule does **not**
  register its `case_id`. A later valid record sharing that same `case_id`
  is therefore accepted.

### Example valid input

```jsonl
{"case_id": "case-001", "gold_label": "pass"}
{"case_id": "case-002", "gold_label": "fail"}
```

### Example invalid input

```jsonl
{bad json}
{"case_id": "  ", "gold_label": "pass"}
{"case_id": "case-003"}
{"case_id": "case-004", "gold_label": "maybe"}
{"case_id": "case-001", "gold_label": "pass"}
```

## Build instructions

```sh
cargo build --release
```

The binary is emitted at `target/release/goldcheck`. Build artifacts under
`target/` are excluded from version control via `.gitignore`.

## Usage

```sh
goldcheck <file.jsonl>
```

If no argument is given, or the file cannot be opened, the program prints a
usage/error message to stderr and exits with status 1.

### Example

```sh
goldcheck data.jsonl
```

### Example output

For an input file containing valid records plus a bad label and a duplicate:

```
line 3: gold_label must be 'pass' or 'fail', got 'maybe'
line 4: duplicate case_id 'rec1'
3 valid record(s)
2 invalid record(s)
```

## Test instructions

```sh
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt --check
```

The test suite (`#[cfg(test)] mod tests` in `src/main.rs`) covers:

- valid `"pass"` and `"fail"` records
- malformed JSON
- non-object JSON (e.g. an array)
- missing `case_id`
- empty (whitespace-only) `case_id`
- non-string `case_id`
- missing `gold_label`
- non-string `gold_label`
- `gold_label` not in `{"pass", "fail"}`
- blank-line skipping
- duplicate `case_id` detection
- an invalid record not suppressing a later valid record that shares its `case_id`

## Development process

The project was developed incrementally with Kilo Code across small iterations,
each scoped to a narrow, explicit set of changes and verified before moving on.

### How the prompts were produced

The requirements were decomposed into small, incremental iterations, each with
explicit scope constraints, followed by build/test verification and a code
review before moving to the next iteration. Each prompt referenced the current
state of the code (e.g. "inspect the existing implementation before editing"),
asked for a minimal implementation, then verified it with `cargo build`,
`cargo clippy --all-targets -- -D warnings`, and a functional check, and finally
summarized the changed files — so each step built on a known-good state rather
than a large speculative edit.

### How the JSONL development record was generated

Each Kilo Code interaction was paired with its actual Git diff, the
corresponding Git commit hash, a timestamp, the agent type (Kilo Code), and the
development language (Rust), serialized as one JSON object per line to form an
auditable JSONL process record. No commits were created during this work, so the
diffs remain in the working tree for the user to review and commit.

### Problems encountered and solutions

1. **Unsafe duplicate detection.** Duplicate detection initially used unchecked
   `value["case_id"].as_str().unwrap()` access. Code review identified the
   implicit coupling between that access and the internal guarantees of
   `check_record` (and the latent panic risk if validation logic changed), and
   the implementation was refactored so the validated `case_id` is returned
   safely from validation, eliminating the `unwrap()` and the unchecked
   indexing.

2. **Network interruption during test preparation.** A network interruption
   occurred while automated tests were being prepared. After reconnection, the
   working tree was inspected (`git status`, `git diff`, file reads) to confirm
   no partial changes had been applied, and the same iteration was resumed
   without duplicating changes.

3. **Docker unavailable locally.** Docker was unavailable in the local
   environment, so the multi-stage `Dockerfile` was prepared but could not be
   locally built. The Rust build, tests, and Clippy checks were still
   verified locally.

### Commands used for verification

```sh
cargo build            # compiles the project
cargo test             # runs the unit test suite
cargo clippy --all-targets -- -D warnings   # lint with warnings as errors
cargo fmt --check       # enforces formatting
```

## Docker

A minimal multi-stage `Dockerfile` is included for building and running the CLI
without a local Rust toolchain. Build artifacts (`target/`) are excluded from
version control and from the Docker build context.

```sh
docker build -t goldcheck .
docker run --rm -v "$PWD/data.jsonl:/data.jsonl" goldcheck /data.jsonl
```
