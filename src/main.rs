use std::collections::HashSet;
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

use serde_json::Value;

#[derive(Debug)]
enum Outcome {
    Valid,
    Invalid(String),
    Skipped,
}

fn main() {
    let mut args = env::args();
    let program = args.next().unwrap_or_else(|| "goldcheck".into());
    let path = match args.next() {
        Some(p) => p,
        None => {
            eprintln!("Usage: {program} <file.jsonl>");
            std::process::exit(1);
        }
    };

    let file = match File::open(&path) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("Error: cannot open file '{path}': {e}");
            std::process::exit(1);
        }
    };

    let reader = BufReader::new(file);
    let mut valid = 0usize;
    let mut invalid = 0usize;
    let mut seen = HashSet::new();

    for (i, line) in reader.lines().enumerate() {
        let line_no = i + 1;
        let line = match line {
            Ok(l) => l,
            Err(e) => {
                eprintln!("line {line_no}: I/O error: {e}");
                invalid += 1;
                continue;
            }
        };

        match process_line(&line, line_no, &mut seen) {
            Outcome::Valid => valid += 1,
            Outcome::Invalid(msg) => {
                eprintln!("{msg}");
                invalid += 1;
            }
            Outcome::Skipped => {}
        }
    }

    println!("{valid} valid record(s)");
    println!("{invalid} invalid record(s)");
}

fn process_line(line: &str, line_no: usize, seen: &mut HashSet<String>) -> Outcome {
    if line.trim().is_empty() {
        return Outcome::Skipped;
    }

    let value = match serde_json::from_str::<Value>(line) {
        Ok(v) => v,
        Err(e) => {
            return Outcome::Invalid(format!("line {line_no}: {e}"));
        }
    };

    let case_id = match check_record(&value) {
        Ok(id) => id,
        Err(e) => {
            return Outcome::Invalid(format!("line {line_no}: {e}"));
        }
    };

    if seen.contains(&case_id) {
        return Outcome::Invalid(format!("line {line_no}: duplicate case_id '{case_id}'"));
    }
    seen.insert(case_id);

    Outcome::Valid
}

fn check_record(value: &Value) -> Result<String, String> {
    let obj = value
        .as_object()
        .ok_or_else(|| "must be a JSON object".to_string())?;

    let case_id = match obj.get("case_id") {
        Some(Value::String(s)) if !s.trim().is_empty() => s.clone(),
        Some(Value::String(_)) => return Err("case_id must not be empty".to_string()),
        Some(_) => return Err("case_id must be a string".to_string()),
        None => return Err("missing field: case_id".to_string()),
    };

    match obj.get("gold_label") {
        Some(Value::String(s)) if matches!(s.as_str(), "pass" | "fail") => {}
        Some(Value::String(s)) => {
            return Err(format!("gold_label must be 'pass' or 'fail', got '{s}'"));
        }
        Some(_) => return Err("gold_label must be a string".to_string()),
        None => return Err("missing field: gold_label".to_string()),
    }

    Ok(case_id)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn parse(json: &str) -> Value {
        serde_json::from_str(json).unwrap()
    }

    #[test]
    fn valid_pass_label() {
        let v = parse(r#"{"case_id":"a","gold_label":"pass"}"#);
        assert_eq!(check_record(&v), Ok("a".to_string()));
    }

    #[test]
    fn valid_fail_label() {
        let v = parse(r#"{"case_id":"b","gold_label":"fail"}"#);
        assert_eq!(check_record(&v), Ok("b".to_string()));
    }

    #[test]
    fn not_an_object() {
        let v = parse("[1,2,3]");
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("JSON object"));
    }

    #[test]
    fn missing_case_id() {
        let v = parse(r#"{"gold_label":"pass"}"#);
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("missing field: case_id"));
    }

    #[test]
    fn empty_case_id() {
        let v = parse(r#"{"case_id":"  ","gold_label":"pass"}"#);
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("case_id must not be empty"));
    }

    #[test]
    fn non_string_case_id() {
        let v = parse(r#"{"case_id":5,"gold_label":"pass"}"#);
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("case_id must be a string"));
    }

    #[test]
    fn missing_gold_label() {
        let v = parse(r#"{"case_id":"a"}"#);
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("missing field: gold_label"));
    }

    #[test]
    fn non_string_gold_label() {
        let v = parse(r#"{"case_id":"a","gold_label":5}"#);
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("gold_label must be a string"));
    }

    #[test]
    fn invalid_gold_label_value() {
        let v = parse(r#"{"case_id":"a","gold_label":"yes"}"#);
        let err = check_record(&v).unwrap_err();
        assert!(err.contains("'yes'") && err.contains("pass") && err.contains("fail"));
    }

    #[test]
    fn empty_line_is_skipped() {
        let mut seen = HashSet::new();
        assert!(matches!(process_line("", 1, &mut seen), Outcome::Skipped));
        assert!(matches!(
            process_line("   ", 1, &mut seen),
            Outcome::Skipped
        ));
        assert!(seen.is_empty());
    }

    #[test]
    fn malformed_json_is_invalid() {
        let mut seen = HashSet::new();
        let outcome = process_line("{bad json}", 7, &mut seen);
        match outcome {
            Outcome::Invalid(msg) => {
                assert!(msg.contains("line 7"));
            }
            other => panic!("expected Invalid, got {other:?}"),
        }
        assert!(seen.is_empty());
    }

    #[test]
    fn process_line_valid_pass() {
        let mut seen = HashSet::new();
        assert!(matches!(
            process_line(r#"{"case_id":"z","gold_label":"pass"}"#, 1, &mut seen),
            Outcome::Valid
        ));
        assert_eq!(seen.len(), 1);
    }

    #[test]
    fn duplicate_case_id_is_invalid() {
        let mut seen = HashSet::new();
        assert!(matches!(
            process_line(r#"{"case_id":"r1","gold_label":"pass"}"#, 1, &mut seen),
            Outcome::Valid
        ));
        let outcome = process_line(r#"{"case_id":"r1","gold_label":"pass"}"#, 2, &mut seen);
        match outcome {
            Outcome::Invalid(msg) => {
                assert!(msg.contains("duplicate case_id 'r1'"));
            }
            other => panic!("expected Invalid, got {other:?}"),
        }
    }

    #[test]
    fn invalid_record_does_not_register_id() {
        let mut seen = HashSet::new();
        let first = process_line(r#"{"case_id":"x","gold_label":"yes"}"#, 1, &mut seen);
        assert!(matches!(first, Outcome::Invalid(_)));
        assert!(seen.is_empty());
        let second = process_line(r#"{"case_id":"x","gold_label":"pass"}"#, 2, &mut seen);
        assert!(matches!(second, Outcome::Valid));
        assert_eq!(seen.len(), 1);
    }
}
