# Saved notebook health convention

Use `runcell-notebook-health-v1` as the report method. Cell indexes are zero
based. Count all cells, code cells, markdown cells and saved output records.
List code cells with a null execution count as `unexecuted_code_cells`.
For each saved error output, report the cell index, error name and message.
Inspect the on-disk notebook without running or changing it.
