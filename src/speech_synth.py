"""Text to speech conversion using Google Text-to-Speech."""

from pathlib import Path
from typing import Union

from gtts import gTTS
from gtts.tokenizer import pre_processors, Tokenizer, tokenizer_cases

def preprocess_text(text: str) -> str:
    """Clean and prepare text for speech synthesis."""
    # Remove excessive whitespace and normalize
    processed = " ".join(text.split())
    return processed

def text_to_speech(text: str, output_path: Union[str, Path], lang = 'en') -> None:
    """
    Convert text to speech and save as MP3.
    
    Args:
        text: Input text to convert
        output_path: Path to save MP3 file
        
    Raises:
        ValueError: If text is empty or output path is invalid
        RuntimeError: If speech synthesis fails
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")
        
    path = Path(output_path) if isinstance(output_path, str) else output_path
    
    if not path.parent.exists():
        raise ValueError(f"Output directory does not exist: {path.parent}")
        
    try:
        processed_text = preprocess_text(text)
        tts = gTTS(processed_text, lang=lang, slow=False, tld='co.in')
        tts.save(str(path))
    except Exception as e:
        raise RuntimeError(f"Speech synthesis failed: {e}")

