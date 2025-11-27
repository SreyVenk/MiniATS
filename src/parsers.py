from io import BytesIO
from typing import Optional

import pdfplumber
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file given raw bytes.
    """
    text_chunks = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_chunks.append(page_text)
    return "\n".join(text_chunks)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text from .docx given raw bytes.
    """
    document = Document(BytesIO(file_bytes))
    lines = [p.text for p in document.paragraphs if p.text]
    return "\n".join(lines)


def extract_resume_text(uploaded_file) -> Optional[str]:
    """
    Streamlit's UploadedFile -> raw text string.
    Supports PDF and DOCX.
    """
    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        # Unsupported type – caller can handle this case
        return None
