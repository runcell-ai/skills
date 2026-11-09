# Editing and review

## Ordinary documents

```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_heading("Equipment inspection", level=0)
doc.add_paragraph("The following items require inspection this week.")
table = doc.add_table(rows=1, cols=2)
table.rows[0].cells[0].text = "Item"
table.rows[0].cells[1].text = "Owner"
cells = table.add_row().cells
cells[0].text, cells[1].text = "Pump", "Maintenance"
doc.save("inspection.docx")
assert Document("inspection.docx").tables[0].cell(1, 0).text == "Pump"
```

For edits, load the existing file. Locate the intended paragraph, table, or
run with enough surrounding context to distinguish duplicate text. Preserve
unrelated fields, hyperlinks, section breaks, and drawings. Text may cross
run boundaries; never assume a word or sentence occupies one run.

Use `Document.iter_inner_content()` for body paragraphs/tables in order,
then traverse table cells as needed. Inspect other document parts separately.
Do not reconstruct a complex document solely from extracted text.

## Comments

With python-docx 1.2 or later, anchor a comment to the intended contiguous
runs with `Document.add_comment(runs=..., text=..., author=...)`. Use the
user's specified author, or a neutral label; do not invent their identity.
Reopen the saved file and inspect `Document.comments` and the anchor text.

Comments are separate from body content. Their absence in a PDF preview does
not mean they were lost. Replies and resolved-thread state are not supported
by this API; preserve existing threads rather than rewriting them as plain
comments. See the [python-docx comments documentation](https://python-docx.readthedocs.io/en/latest/user/comments.html).

## Tracked changes and complex XML

Direct text replacement is not a tracked revision. python-docx does not offer
a general track-changes editor. When native redlines are requested, inspect
the relevant OOXML parts in the DOCX ZIP and use a narrowly scoped XML edit,
or an available office application's revision API.

For XML work, use a parser with network access and external entity resolution
disabled. Preserve ZIP members and relationships outside the edit. Inspect
existing revision identifiers and author/date metadata before adding markup.
Text insertions/deletions, paragraph marks, moves, and formatting revisions
have different representations; a blanket removal of revision tags is not
a valid general accept/reject implementation. Do not silently accept existing
changes or discard reviewer comments during an unrelated edit.

Use the [Open XML reference](https://learn.microsoft.com/en-us/office/open-xml/word/how-to-accept-all-revisions-in-a-word-processing-document)
for the specific revision type. After writing, reopen the ZIP/XML, check both
the intended accepted and rejected text, and verify in a revision-aware
viewer when available. Report unsupported revision types before claiming a
complete redline or clean copy. The skill does not ship a universal revision
conversion script.

## Special content

Keep editable equations editable when requested; an image is not an editable
equation. Preserve numbering and reference field codes during edits. Page
previews may show cached field results, so verify field updates separately.
For redaction, replacing visible text or drawing an opaque rectangle is not
proof of removal: inspect comments, revisions, metadata, headers, footers,
and embedded content for the target information before making that claim.
