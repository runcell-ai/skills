#!/usr/bin/env python3
"""Audit a CSV without changing it; requires only the Python standard library."""

import argparse
import csv
import json
from pathlib import Path

METHOD = "runcell-table-audit-v1"


def audit(source: Path) -> dict:
    with source.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        columns = next(reader, [])
        if not columns or any(not name.strip() for name in columns):
            raise ValueError("CSV needs a nonempty header")
        if len(set(columns)) != len(columns):
            raise ValueError("CSV column names must be unique")
        missing = dict.fromkeys(columns, 0)
        seen = set()
        count = duplicates = 0
        for number, row in enumerate(reader, 2):
            if not row:
                continue
            if len(row) != len(columns):
                raise ValueError(f"CSV record {number} has {len(row)} fields; expected {len(columns)}")
            count += 1
            key = tuple(row)
            duplicates += key in seen
            seen.add(key)
            for name, value in zip(columns, row):
                missing[name] += not value.strip()
    return {"method": METHOD, "rows": count, "columns": columns,
            "missing_values": missing, "duplicate_rows": duplicates}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("input and output must be different files")
    report = audit(args.input)
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
