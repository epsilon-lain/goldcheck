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
    let mut count = 0usize;

    for (i, line) in reader.lines().enumerate() {
        let line_no = i + 1;
        let line = match line {
            Ok(l) => l,
            Err(e) => {
                eprintln!("line {line_no}: I/O error: {e}");
                continue;
            }
        };

        if line.trim().is_empty() {
            continue;
        }

        match serde_json::from_str::<Value>(&line) {
            Ok(_) => count += 1,
            Err(e) => eprintln!("line {line_no}: {e}"),
        }
    }

    println!("{count} record(s) parsed successfully");
}
