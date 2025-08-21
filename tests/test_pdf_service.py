import pytest
from pathlib import Path
import sys

# Add project root to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.pdf_service import md_to_pdf, txt_to_pdf

def test_md_to_pdf(tmp_path: Path):
    """Tests that a PDF is created from a markdown string."""
    output_file = tmp_path / "test_md.pdf"
    md_content = "# Hello World\n\nThis is a test of the markdown to PDF conversion."

    md_to_pdf(md_content, output_file)

    assert output_file.exists()
    assert output_file.stat().st_size > 0, "PDF file should not be empty"

def test_txt_to_pdf(tmp_path: Path):
    """Tests that a PDF is created from a plain text string."""
    output_file = tmp_path / "test_txt.pdf"
    txt_content = "Hello World\n\nThis is a test of plain text to PDF conversion.\nIt includes special characters: <>\"'&"

    txt_to_pdf(txt_content, output_file)

    assert output_file.exists()
    assert output_file.stat().st_size > 0, "PDF file should not be empty"

def test_md_to_pdf_empty_input(tmp_path: Path):
    """Tests markdown to PDF with empty input."""
    output_file = tmp_path / "test_empty_md.pdf"
    md_to_pdf("", output_file)
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_txt_to_pdf_empty_input(tmp_path: Path):
    """Tests text to PDF with empty input."""
    output_file = tmp_path / "test_empty_txt.pdf"
    txt_to_pdf("", output_file)
    assert output_file.exists()
    assert output_file.stat().st_size > 0
