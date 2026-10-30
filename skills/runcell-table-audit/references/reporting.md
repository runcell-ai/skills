# CSV audit convention

The report's `method` is `runcell-table-audit-v1`.

- The first CSV record is the header. `rows` counts subsequent records, ignoring
  empty lines. A row with empty fields still counts.
- A value is missing when empty or entirely whitespace. Report counts by column.
- `duplicate_rows` counts repeated complete rows after their first occurrence.
  Compare original strings, including whitespace, without normalization.
- Reject a missing header, duplicate column names, and records whose width
  differs from the header. Never silently discard extra fields.
- Report `columns` in input order. Save UTF-8 JSON with sorted object keys.
