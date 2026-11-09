---
name: pdf
description: Read, create, transform, and inspect local PDF files, including text extraction, page previews, and filling interactive forms.
---

# PDF files

Use the workspace's Python environment and file tools. Use an image viewer for
page checks. Resolve resource paths relative to this skill's actual location,
including a task-local package copy when supplied. No account, host connector,
or Node runtime is needed.

## Dependencies

Install only the libraries required by the task in the selected virtual
environment, subject to its installation permissions:

```sh
python -m pip install 'pypdf>=6,<8' 'pdfplumber>=0.11,<1' 'reportlab>=4,<5'
```

- `pypdf`: page manipulation, document metadata, and AcroForm fields.
- `pdfplumber`: text positions and table extraction from text-bearing pages.
- `reportlab`: creating new PDFs with text, tables, images, and forms.
- Poppler's `pdftoppm`: page images; `pdfinfo`: page metadata. Install Poppler
  through the operating system's package manager, or pass an existing binary.

On macOS, Poppler is available through `brew install poppler`; on Debian or
Ubuntu, use `poppler-utils`. On Windows, add installed Poppler executables to
`PATH` or supply an explicit path. Use fonts covering the document's language.

## Read and transform

Inspect page count, encryption, and the content type before choosing a method.
Use text extraction for text-bearing PDFs; scanned pages require OCR or visual
reading. Empty extracted text is not evidence of an empty page. For tables,
compare extracted rows and headers against the page image before calculations.

Use `PdfReader` and `PdfWriter` for page selection, merging, rotation, and
metadata edits. Preserve the original and save to a new path unless overwriting
was requested. Form-bearing PDFs require form-aware copying, not merely a loop
that adds pages. Read [form workflows](references/forms.md) for form tasks.

Editing may invalidate existing digital signatures. Detect signed documents
before changing them and clarify the desired signed-document outcome. Do not
claim that an edited PDF preserves a signature without verification.

## Create

Use ReportLab's document layout objects for flowing text and multi-page tables;
use its canvas for fixed-position layouts. Keep text inside page margins and
repeat table headers where useful. Embed appropriate fonts. Choose page size
from the user's requirements or reference and keep text selectable where
possible. See [creation and extraction examples](references/examples.md).

## Inspect the result

Reopen outputs with `PdfReader` and verify the requested page count, content,
and fields. Generate page images into a new or empty directory:

```sh
python /path/to/skill/scripts/render_pdf.py report.pdf --output-dir previews
```

The helper accepts `--pdftoppm /path/to/pdftoppm`, `--dpi`, and a per-command
`--timeout`. Inspect all changed pages and the final document's layout as
appropriate to the scope. Check clipping, missing glyphs, unexpected blank
pages, image quality, and table alignment. Regenerate previews after changes.
If visual inspection is unavailable, disclose that limitation explicitly.

Covering text with a rectangle does not remove it. A redaction request requires
a redaction-capable tool plus extraction and object checks; do not use a visual
overlay as proof that sensitive content was removed.

## Deliver

Save to the user's requested destination or the workspace's artifact directory.
Keep previews and temporary files outside the installed skill. Return normal
file links or attachments supported by the host, and report material validation
limits. For PDF questions, identify source filenames and verified page numbers;
distinguish printed page labels from physical PDF page indices.
