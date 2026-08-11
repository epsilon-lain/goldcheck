# goldcheck

A small Rust CLI that validates JSONL files of AI dataset gold cases.

## Purpose

`goldcheck` reads a `.jsonl` file and verifies that each non-empty line is a
well-formed gold-case record. It reports per-line validation errors while
processing, then prints a final summary of valid and invalid record counts.

## Supported JSONL format

One JSON record per line. Blank lines are ignored. Example:

```jsonl
{"case_id": "case-001", "gold_label": "pass"}
{"case_id": "case-002", "gold_label": "fail"}
```

## Validation rules

For each non-empty line, in order:

1. The line must be valid JSON.
2. The parsed value must be a JSON **object**.
3. The object must contain a `case_id` field that is a **non-empty string**
   (whitespace is trimmed before the emptiness check).
4. The object must contain a `gold_label` field that is a string.
5. `gold_label` must be exactly `"pass"` or `"fail"`.
6. `case_id` values are compared **case-sensitively**. A `case_id` that has
   already appeared in a *valid* record is a duplicate.

Additional behavior:

- `case_id` duplicate detection is **case-sensitive** and uses the `case_id`
  value as-is (no normalization beyond the non-empty trim check).
- A record that fails JSON parsing or schema validation does **not** register
  its `case_id`, so a later valid record with the same `case_id` is accepted.
- Processing continues after errors; every non-empty line is counted as either
  valid or invalid.

## Build

```sh
cargo build --release
```

The binary is placed at `target/release/goldcheck`.

## Usage

```sh
goldcheck <file.jsonl>
```

Example:

```sh
goldcheck data.jsonl
```

## Example output

```
line 3: gold_label must be 'pass' or 'fail', got 'maybe'
line 4: duplicate case_id 'rec1'
3 valid record(s)
2 invalid record(s)
```

- `valid` records passed all checks (and are the first valid occurrence of
  their `case_id`).
- `invalid` records are any of: malformed JSON, schema violation, disallowed
  `gold_label` value, or a duplicate `case_id`.

## Tests

```sh
cargo test
cargo clippy --all-targets -- -D warnings
```

The test suite covers valid `pass`/`fail` records, malformed JSON, missing and
empty `case_id`, non-string fields, missing/invalid `gold_label`, duplicate
detection, and the case where an invalid record does not suppress a later valid
record sharing its `case_id`.

## Development process

This project was developed incrementally with Kilo Code across several review
iterations (argument parsing, schema validation, `gold_label` value checking,
case_id duplicate detection, `unwrap()` removal and testability extraction, and
a final review). Each iteration was built, tested, and linted with
`cargo clippy -- -D warnings` before proceeding to the next.
