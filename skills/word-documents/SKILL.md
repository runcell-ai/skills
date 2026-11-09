---
name: word-documents
description: Create, read, edit, and review Word DOCX files, including tables, images, comments, and tracked-change workflows, with rendered page checks.
---

# Word documents

Use this skill for local `.docx` documents. For legacy `.doc` files, convert a
copy with an installed office application first. Preserve the source file.

## Environment

Use the workspace's Python environment, shell/file tools, and image viewer.
Resolve this directory from the loaded skill location; when the host supplies
a task-local copy, use that copy. No host connector, account, or Node runtime
is required. Save outputs to the user's requested directory or the workspace's
normal artifact directory, never inside the installed skill.

Core Python dependency: `python-docx>=1.2,<2`. Its XML support uses `lxml`.
Page previews require LibreOffice and Poppler (`pdftoppm`) on `PATH`; explicit
executable paths are also accepted. Install only missing dependencies in the
selected environment, within the task's installation permissions. Do not
change global Python packages. See [environment setup](references/environment.md).

## Working sequence

1. Inspect the input and requested edit scope. Preserve an existing template's
   styles, page geometry, numbering, and content outside the requested changes.
2. For reading, inspect paragraphs and tables in document order. Check headers,
   footers, comments, and revision XML when they matter; a plain paragraph list
   is not a complete representation of a Word file.
3. Use `python-docx` for ordinary authoring. Use paragraph styles for headings,
   real table cells for tabular content, and explicit image dimensions. Select
   page size and fonts for the user's locale or reference, including fonts with
   the required language coverage.
4. Save a new output path and reopen it to check text, tables, images, and any
   requested comments. Avoid assigning a whole paragraph's `.text` during a
   narrow edit: it replaces runs and can erase formatting and embedded objects.
5. Render the final document and inspect every page for overflow, missing
   glyphs, distorted images, unwanted page breaks, and table/header placement.
   Fix defects and render again after layout changes.

For authoring examples and reviews, read
[editing and review](references/editing-and-review.md). For tracked changes,
read the limitations there before modifying revision markup.

## Page previews

Here `python` means the workspace-selected interpreter, and `/path/to/skill`
means this skill's actual directory:

```sh
python /path/to/skill/scripts/render_docx.py report.docx --output-dir previews
```

The output directory must be new or empty. The helper uses a temporary
LibreOffice profile and produces `document.pdf` and `page-1.png`, etc. The
source remains intact. Executable paths containing spaces work as single
quoted arguments:

```sh
python /path/to/skill/scripts/render_docx.py report.docx --output-dir previews \
  --soffice "/path/to/LibreOffice/soffice" --pdftoppm /path/to/pdftoppm
```

A successful conversion does not prove visual quality. If rendering or image
inspection is unavailable, report the specific check left incomplete; do not
claim visual verification. LibreOffice previews may differ from Microsoft
Word, especially for fields, pagination, or advanced objects. Comments and
revision semantics require structural checks as well as a preview.

## Delivery

Provide the requested final file through the host's normal file links or
attachments, with a brief description of the edits and checks. Keep previews
separate unless requested. Cite source documents with identifiable filenames
and verified locations when answering questions about their contents.

This skill produces local files. If the user requests a cloud document, use
an available authorized upload/import integration and verify its result; do
not assume that a particular connector exists.
