"""Text to speech conversion using Google Text-to-Speech, with optional translation."""

from pathlib import Path
from typing import Union
from gtts import gTTS
from gtts.tokenizer import pre_processors, Tokenizer, tokenizer_cases

# Add translator import
from googletrans import Translator

def preprocess_text(text: str) -> str:
    """Clean and prepare text for speech synthesis."""
    return " ".join(text.split())

def translate_text(text: str, target_lang: str) -> str:
    """Translate the input text to the target language using Google Translate."""
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")

def text_to_speech(
    text: str,
    output_path: Union[str, Path],
    lang: str = 'en',
    translate: bool = False
) -> None:
    """
    Convert text to speech and save as MP3, with optional translation.

    Args:
        text: Input text to convert
        output_path: Path to save MP3 file
        lang: Language code for speech (e.g., 'en', 'hi')
        translate: If True, translates text to the target lang before speech

    Raises:
        ValueError: If text is empty or output path is invalid
        RuntimeError: If translation or speech synthesis fails
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")

    path = Path(output_path) if isinstance(output_path, str) else output_path

    if not path.parent.exists():
        raise ValueError(f"Output directory does not exist: {path.parent}")

    try:
        processed_text = preprocess_text(text)

        if lang != 'en':
            translate = True

        # Translate if requested
        if translate:
            processed_text = translate_text(processed_text, lang)

        # Choose appropriate TLD
        tld = 'co.in' if lang == 'hi' else 'com'

        tts = gTTS(processed_text, lang=lang, slow=False, tld=tld)
        tts.save(str(path))
    except Exception as e:
        raise RuntimeError(f"Speech synthesis failed: {e}")
