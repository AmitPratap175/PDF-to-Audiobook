import sys
from pathlib import Path
from gtts import gTTS
import PyPDF2
from googletrans import Translator

def extract_text(file_path: Path) -> str:
    if file_path.suffix.lower() == '.pdf':
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    elif file_path.suffix.lower() == '.txt':
        return file_path.read_text(encoding='utf-8')
    else:
        raise ValueError("Unsupported file type. Only .pdf and .txt are supported.")

def translate_to_hindi(text: str) -> str:
    translator = Translator()
    print("Translating to Hindi...")
    translated = translator.translate(text, dest='hi')
    return translated.text

def text_to_hindi_speech(text: str, output_path: Path):
    tts = gTTS(text=text, lang='hi', tld='co.in')
    tts.save(str(output_path))

def main():
    if len(sys.argv) < 2:
        print("Usage: python doc_to_hindi_translated_speech.py <input_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = input_path.with_suffix('.mp3')

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    try:
        print("Extracting text...")
        english_text = extract_text(input_path)

        print("Translating to Hindi...")
        hindi_text = translate_to_hindi(english_text)

        print("Converting Hindi text to speech...")
        text_to_hindi_speech(hindi_text, output_path)

        print(f"✅ Hindi audiobook saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
