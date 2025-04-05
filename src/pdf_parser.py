"""PDF text extraction functions."""

from pathlib import Path
from typing import Union

import pdfplumber
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """
    Extract text from a PDF file using pdfplumber or PyPDF2.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Extracted text as a single string
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If PDF cannot be parsed
    """
    path = Path(pdf_path) if isinstance(pdf_path, str) else pdf_path
    
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
        
    try:
        # First try pdfplumber for better text extraction
        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)
    except Exception as e:
        try:
            # Fall back to PyPDF2 if pdfplumber fails
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() for page in reader.pages)
        except Exception:
            raise ValueError(f"Failed to parse PDF: {e}")
    
    if not text.strip():
        raise ValueError("PDF appears to have no extractable text")
        
    return text

