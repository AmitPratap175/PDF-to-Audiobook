"""Tests for PDF text extraction."""

import pytest
from pathlib import Path

from src.pdf_parser import extract_text_from_pdf

def test_pdf_extraction_success(tmp_path):
    """Test successful PDF text extraction."""
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_text("Sample PDF content")
    
    text = extract_text_from_pdf(test_pdf)
    assert "Sample PDF content" in text

def test_pdf_extraction_failure(tmp_path):
    """Test handling of invalid PDF."""
    test_file = tmp_path / "not_pdf.txt"
    test_file.touch()
    
    with pytest.raises(ValueError):
        extract_text_from_pdf(test_file)

