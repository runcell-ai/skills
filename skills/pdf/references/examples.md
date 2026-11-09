# Creation and extraction

## A short report

```python
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table

styles = getSampleStyleSheet()
blocks = [Paragraph("Service schedule", styles["Title"]), Spacer(1, 12)]
blocks.append(Paragraph("The next inspection is scheduled for Monday.", styles["BodyText"]))
blocks.append(Table([["Equipment", "Status"], ["Pump", "Scheduled"]], repeatRows=1))
SimpleDocTemplate("schedule.pdf").build(blocks)
```

Treat user-supplied strings as text: escape XML characters before inserting
them into a ReportLab `Paragraph`. For non-Latin content, register and use a
font with the required glyphs rather than relying on built-in PDF fonts.

## Text and tables

```python
import pdfplumber

with pdfplumber.open("schedule.pdf") as document:
    for number, page in enumerate(document.pages, start=1):
        print(number, page.extract_text())
        tables = page.extract_tables()
        # Compare with page images before relying on cell boundaries.
```

For large documents, inspect only relevant pages initially, then widen the
read as needed. Multi-column layouts, merged cells, and scans need additional
review; do not present extraction output as lossless transcription.
