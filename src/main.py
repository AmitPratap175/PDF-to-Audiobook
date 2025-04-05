"""Main entry point for PDF to Speech conversion."""

import argparse
import logging
import sys
from pathlib import Path

from .pdf_parser import extract_text_from_pdf
from .speech_synth import text_to_speech

def setup_logging() -> None:
    """Configure basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def main() -> None:
    """Handle command line interface and coordinate PDF to speech conversion."""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="Convert PDF files to speech using Google Text-to-Speech."
    )
    parser.add_argument("input_pdf", help="Path to input PDF file")
    parser.add_argument("output_mp3", help="Path to output MP3 file")
    
    args = parser.parse_args()
    
    try:
        logging.info(f"Processing PDF: {args.input_pdf}")
        text = extract_text_from_pdf(Path(args.input_pdf))
        text_to_speech(text, Path(args.output_mp3))
        logging.info(f"Successfully saved speech to {args.output_mp3}")
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

