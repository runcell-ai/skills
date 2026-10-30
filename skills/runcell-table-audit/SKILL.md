---
name: runcell-table-audit
description: Audit CSV data quality for missing values and duplicate rows, and save a reproducible JSON report using the project's reporting convention.
---

Read `references/reporting.md` before auditing. Use `scripts/audit.py` from
this package to compute the report. It uses Python's standard library.

Run the script with the input CSV and output JSON paths:

```sh
python /path/to/this/skill/scripts/audit.py input.csv report.json
```

Use the Python interpreter selected by the workspace. Quote paths that contain
spaces. When a runtime provides a task copy of this package, use that copy.
Inspect the saved report before reporting completion. Do not modify the input.
