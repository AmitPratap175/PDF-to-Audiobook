"""Tests for text to speech conversion."""

import pytest
from pathlib import Path

from src.speech_synth import text_to_speech, preprocess_text

def test_text_preprocessing():
    """Test text preprocessing for speech synthesis."""
    text = "  Hello   \n  World!  "
    processed = preprocess_text(text)
    assert processed == "Hello World!"

def test_speech_conversion(tmp_path):
    """Test successful text to speech conversion."""
    output_path = tmp_path / "test.mp3"
    text = "Test speech synthesis"
    
    text_to_speech(text, output_path)
    assert output_path.exists()

