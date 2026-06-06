import io

import pytest
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.engines.pdf_parser import PDFParser
from app.utils.exceptions import FileTooLargeError, InvalidFileError


@pytest.fixture
def parser():
    return PDFParser()


def _make_pdf(lines: list[str]) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    y = 750
    for line in lines:
        c.drawString(72, y, line)
        y -= 20
    c.save()
    return buf.getvalue()


def _make_docx(paragraphs: list[str]) -> bytes:
    buf = io.BytesIO()
    doc = Document()
    for p in paragraphs:
        doc.add_paragraph(p)
    doc.save(buf)
    return buf.getvalue()


def test_extract_pdf_text(parser):
    pdf = _make_pdf(["John Doe", "Software Engineer", "Python and FastAPI"])
    result = parser.extract(pdf, "resume.pdf")
    assert "John Doe" in result.text
    assert result.page_count == 1
    assert result.word_count > 0


def test_extract_pdf_by_magic_bytes_without_filename(parser):
    pdf = _make_pdf(["Magic bytes test content here"])
    result = parser.extract(pdf)
    assert "Magic bytes" in result.text


def test_extract_docx_text(parser):
    docx = _make_docx(["Jane Smith", "Data Engineer with SQL skills"])
    result = parser.extract(docx, "resume.docx")
    assert "Jane Smith" in result.text
    assert result.word_count > 0


def test_unsupported_file_raises(parser):
    with pytest.raises(InvalidFileError):
        parser.extract(b"plain old text, not a document", "resume.txt")


def test_garbage_bytes_raise(parser):
    with pytest.raises(InvalidFileError):
        parser.extract(b"\x00\x01\x02\x03 garbage")


def test_oversized_file_raises(parser):
    with pytest.raises(FileTooLargeError):
        parser.extract(b"x" * (11 * 1024 * 1024), "huge.pdf")


def test_corrupt_pdf_raises_invalid(parser):
    with pytest.raises(InvalidFileError):
        parser.extract(b"%PDF-1.4 then it all goes wrong", "broken.pdf")
