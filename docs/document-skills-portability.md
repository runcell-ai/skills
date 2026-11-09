# Portable Word and PDF skills

Added 2026-11-09 as source-only skills:

- `skills/word-documents/`: DOCX creation, reading, editing, comments, review
  guidance, and a standalone page renderer.
- `skills/pdf/`: PDF creation, extraction, transformations, AcroForm guidance,
  and a standalone page renderer.

## Origin and scope

These files are newly authored for this repository. The locally inspected
bundled Word package's license restricts extraction, copying, and distribution,
so its instructions and helper scripts were not imported. The new skills use
public Python libraries and ordinary command-line tools. The root MIT license
applies to this new material; see `NOTICE` for the explicit exception to the
older imported-path notice.

This is not a feature-for-feature copy of the bundled Word utility collection.
Advanced revisions, content controls, equation conversion, metadata scrubbing,
and destructive redaction do not have dedicated automation helpers here.
The review reference identifies limitations and directs the agent to a
supported library or document-format workflow for those tasks.

## Host contract

The host supplies a workspace, a Python interpreter, process/file access, and
an image viewer for visual verification. Each skill resolves its own resources
relative to its installed location. No host-specific APIs, event markers,
authentication, citation syntax, cache paths, or workspace loaders are needed.
The executable helpers use Python's standard library and command-line tools.

Word authoring uses `python-docx`; rendering uses LibreOffice plus Poppler.
PDF tasks use `pypdf`, `pdfplumber`, or `reportlab` as needed, with Poppler for
previews. Dependencies are described inside each skill and are not embedded
in distribution ZIPs. Installing a skill does not automatically install its
libraries, native tools, or fonts.

## Validation

Validation ran in this repository's isolated `.venv` with Python 3.10,
python-docx 1.2.0, pypdf 7.0.0, pdfplumber 0.11.10, reportlab 4.5.1,
PyYAML 6.0.3, and pytest 9.2.0.

```sh
DOCUMENT_TEST_SOFFICE=/absolute/path/to/soffice \
  .venv/bin/python -m pytest tests/test_document_skills.py tests/test_official_skill_release.py -q
```

Result: **8 passed**, with no skips or mocks in the recorded run.

- Generated a real two-page DOCX, edited a run, retained bold formatting,
  added/reopened a comment, converted it to PDF and PNG, and checked the
  source-file digest remained unchanged.
- Generated a real two-page PDF with an AcroForm, filled a text field, reopened
  it to inspect the stored value and appearance stream, extracted text, and
  rendered both pages. Confirmed the source remained unchanged.
- Verified that nonempty preview destinations are rejected and damaged PDFs
  report renderer failure rather than producing successful-looking output.
- Built both skill bundles twice at candidate version 1.0.0 in temporary
  directories; bytes matched and the repository verifier accepted their
  archive paths, manifests, sizes, and hashes. Checked local Markdown links.
- Inspected all four resulting page images. Text, table content, page breaks,
  and the completed field were visible without clipping.
- Both skill entrypoints passed the skill frontmatter validator. A source scan
  found no host-specific tool names or machine-specific paths in either skill.

The Word rendering run used an existing LibreOffice binary from this machine's
bundled installation, passed explicitly through `--soffice`; it did not use its
host wrapper or runtime discovery API. Poppler came from the system installation.
This validates executable-path injection, but is not a separate acceptance run
on a freshly installed office suite, Windows, Linux, or a RunCell agent session.
Native Word revision behavior, complex form flattening, OCR, and cloud uploads
were not tested. Tests skip renderer checks when native tools are absent; such
skips are not rendering acceptance.

## Distribution status

No existing immutable package, release version, or automatic delivery catalog
was changed. No deployment was performed. The README lists these as available
sources. A later distribution release should build and verify new immutable
packages, then update the appropriate catalog through the existing workflow.
