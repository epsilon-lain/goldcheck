use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};

use serde_json::Value;

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

        if line.trim().is_empty() {
            continue;
        }

        let value = match serde_json::from_str::<Value>(&line) {
            Ok(v) => v,
            Err(e) => {
                eprintln!("line {line_no}: {e}");
                invalid += 1;
                continue;
            }
        };

        if let Err(e) = check_record(&value) {
            eprintln!("line {line_no}: {e}");
            invalid += 1;
            continue;
        }

        valid += 1;
    }

    println!("{valid} valid record(s)");
    println!("{invalid} invalid record(s)");
}

fn check_record(value: &Value) -> Result<(), String> {
    let obj = value
        .as_object()
        .ok_or_else(|| "must be a JSON object".to_string())?;

    match obj.get("case_id") {
        Some(Value::String(s)) if !s.trim().is_empty() => {}
        Some(Value::String(_)) => return Err("case_id must not be empty".to_string()),
        Some(_) => return Err("case_id must be a string".to_string()),
        None => return Err("missing field: case_id".to_string()),
    }

    match obj.get("gold_label") {
        Some(Value::String(_)) => {}
        Some(_) => return Err("gold_label must be a string".to_string()),
        None => return Err("missing field: gold_label".to_string()),
    }

    Ok(())
}
