"""Real local file and renderer checks; no service or library mocks."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


def run_script(skill, source, output, *extra):
    script = "render_docx.py" if skill == "word-documents" else "render_pdf.py"
    result = subprocess.run(
        [sys.executable, str(ROOT / "skills" / skill / "scripts" / script),
         str(source), "--output-dir", str(output), *extra],
        capture_output=True, text=True, timeout=180, check=True,
    )
    return json.loads(result.stdout)


@pytest.mark.parametrize("skill", ["word-documents", "pdf"])
def test_portable_bundle_roundtrip(skill, tmp_path):
    spec = importlib.util.spec_from_file_location("document_release", ROOT / "scripts/official_skill_release.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    first = module.build_release(repo_root=ROOT, skill_id=skill, version="1.0.0", output_dir=tmp_path / "one")
    second = module.build_release(repo_root=ROOT, skill_id=skill, version="1.0.0", output_dir=tmp_path / "two")
    assert first[0].read_bytes() == second[0].read_bytes()
    manifest = module.verify_release(bundle_path=first[0], release_path=first[1])
    assert any(item["path"].startswith("scripts/") for item in manifest["files"])
    for path in (ROOT / "skills" / skill).rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" not in target:
                assert (path.parent / target.split("#")[0]).is_file(), target


def test_word_comment_edit_and_render(tmp_path):
    docx = pytest.importorskip("docx")
    pypdf = pytest.importorskip("pypdf")
    office = os.environ.get("DOCUMENT_TEST_SOFFICE") or shutil.which("soffice")
    if not office or not shutil.which("pdftoppm"):
        pytest.skip("Install LibreOffice and Poppler to run actual Word rendering")
    source = tmp_path / "source with spaces.docx"
    doc = docx.Document()
    doc.add_heading("Inspection record", 0)
    paragraph = doc.add_paragraph()
    paragraph.add_run("Keep this formatting. ").bold = True
    changed = paragraph.add_run("Draft")
    changed.text = "Approved"
    doc.add_comment(runs=[changed], text="Status checked", author="Reviewer")
    table = doc.add_table(rows=1, cols=2)
    table.cell(0, 0).text, table.cell(0, 1).text = "Pump", "Ready"
    doc.add_page_break()
    doc.add_paragraph("Second page retained.")
    doc.save(source)
    reopened = docx.Document(source)
    assert reopened.paragraphs[1].runs[0].bold
    assert reopened.comments.get(0).text == "Status checked"
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    rendered = run_script("word-documents", source, tmp_path / "word previews", "--soffice", office)
    assert len(rendered["pages"]) == 2
    assert "Approved" in pypdf.PdfReader(rendered["pdf"]).pages[0].extract_text()
    assert all(Path(page).read_bytes().startswith(b"\x89PNG") for page in rendered["pages"])
    assert hashlib.sha256(source.read_bytes()).hexdigest() == before


def test_pdf_form_fill_extract_and_render(tmp_path):
    canvas_module = pytest.importorskip("reportlab.pdfgen.canvas")
    pypdf = pytest.importorskip("pypdf")
    plumber = pytest.importorskip("pdfplumber")
    if not shutil.which("pdftoppm"):
        pytest.skip("Install Poppler to run actual PDF rendering")
    source = tmp_path / "form source.pdf"
    canvas = canvas_module.Canvas(str(source))
    canvas.drawString(50, 760, "Contact form")
    canvas.acroForm.textfield(name="contact_name", x=50, y=700, width=200, height=25)
    canvas.showPage()
    canvas.drawString(50, 760, "Instructions on page two")
    canvas.save()
    original = source.read_bytes()
    reader = pypdf.PdfReader(source)
    writer = pypdf.PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, {"contact_name": "Taylor"}, auto_regenerate=False)
    filled = tmp_path / "filled form.pdf"
    writer.write(filled)
    saved = pypdf.PdfReader(filled)
    assert saved.get_fields()["contact_name"]["/V"] == "Taylor"
    widgets = [ref.get_object() for page in saved.pages for ref in page.get("/Annots", [])
               if ref.get_object().get("/Subtype") == "/Widget"]
    assert len(widgets) == 1 and widgets[0]["/AP"]["/N"].get_data()
    with plumber.open(filled) as extracted:
        assert "Contact form" in extracted.pages[0].extract_text()
    rendered = run_script("pdf", filled, tmp_path / "pdf previews")
    assert len(rendered["pages"]) == 2
    assert all(Path(page).read_bytes().startswith(b"\x89PNG") for page in rendered["pages"])
    assert source.read_bytes() == original
    # Reusing the preview directory must fail instead of mixing stale pages.
    with pytest.raises(subprocess.CalledProcessError):
        run_script("pdf", filled, tmp_path / "pdf previews")


def test_pdf_renderer_reports_corrupt_input(tmp_path):
    if not shutil.which("pdftoppm"):
        pytest.skip("Install Poppler")
    damaged = tmp_path / "damaged.pdf"
    damaged.write_bytes(b"%PDF-1.7\ntruncated")
    with pytest.raises(subprocess.CalledProcessError) as error:
        run_script("pdf", damaged, tmp_path / "previews")
    assert "PDF rendering failed" in error.value.stderr
    assert not list((tmp_path / "previews").glob("*.png"))
