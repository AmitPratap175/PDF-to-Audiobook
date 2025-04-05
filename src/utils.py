"""Utility functions for PDF to Speech conversion."""

from pathlib import Path
from typing import Optional

def validate_input_path(path: Path) -> bool:
    """Check if input path exists and has valid PDF extension."""
    if not path.exists():
        return False
    if path.suffix.lower() != ".pdf":
        return False
    return True

def validate_output_path(path: Path) -> bool:
    """Check if output directory exists and file has MP3 extension."""
    if not path.parent.exists():
        return False
    if path.suffix.lower() != ".mp3":
        return False
    return True

