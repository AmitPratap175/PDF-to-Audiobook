import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile
from src.pdf_parser import extract_text_from_pdf
from src.speech_synth import text_to_speech
import os
import hashlib

def get_file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()

def main():
    st.title("PDF to Audiobook Converter")
    st.write("Upload a PDF file and convert its content into audiobook.")

    # Initialize session state
    if "mp3_data" not in st.session_state:
        st.session_state["mp3_data"] = None
        st.session_state["mp3_filename"] = None
        st.session_state["pdf_hash"] = None
        st.session_state["word_count"] = None

    # File upload
    st.subheader("1. Upload PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        accept_multiple_files=False,
        help="Only PDF files are supported"
    )

    if uploaded_file is not None:
        current_pdf_hash = get_file_hash(uploaded_file.getvalue())

        # If file is new, reset MP3 state
        if st.session_state["pdf_hash"] != current_pdf_hash:
            st.session_state["mp3_data"] = None
            st.session_state["mp3_filename"] = None
            st.session_state["word_count"] = None
            st.session_state["pdf_hash"] = current_pdf_hash

        # Step 2: Generate MP3 button
        if st.button("🔊 Generate audiobook"):
            try:
                with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(uploaded_file.getvalue())
                    pdf_path = tmp_pdf.name

                # Extract text
                with st.spinner("Extracting text from PDF..."):
                    text = extract_text_from_pdf(Path(pdf_path))
                    word_count = len(text.split())
                    st.session_state["word_count"] = word_count
                    st.success(f"Extracted {word_count} words from the PDF.")

                # Convert to speech
                with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
                    mp3_path = tmp_mp3.name

                with st.spinner("Converting text to speech..."):
                    text_to_speech(text, Path(mp3_path))
                    st.success("Speech generation complete!")

                with open(mp3_path, "rb") as f:
                    st.session_state["mp3_data"] = f.read()
                    st.session_state["mp3_filename"] = f"{Path(uploaded_file.name).stem}.mp3"

                # Clean up
                os.unlink(pdf_path)
                os.unlink(mp3_path)

            except Exception as e:
                st.error(f"Error: {e}")
                st.error("Please try again with a different PDF file.")

    # Step 3: Playback and download
    if st.session_state["mp3_data"]:
        st.subheader("2. Listen to the Result")
        st.audio(st.session_state["mp3_data"], format="audio/mp3")

        st.subheader("3. Download audiobook")
        st.download_button(
            label="Download",
            data=st.session_state["mp3_data"],
            file_name=st.session_state["mp3_filename"],
            mime="audio/mpeg"
        )

if __name__ == "__main__":
    main()
