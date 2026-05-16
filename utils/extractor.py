"""
Text extraction from PDF and DOCX files.
"""

import io


def extract_text_from_pdf(file_obj) -> str:
    """Extract text from an uploaded PDF file."""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_obj.read()))
        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
        return text.strip()
    except Exception as e:
        return f"[PDF extraction error: {e}]"


def extract_text_from_docx(file_obj) -> str:
    """Extract text from an uploaded DOCX file."""
    try:
        import docx
        document = docx.Document(io.BytesIO(file_obj.read()))
        text = "\n".join(para.text for para in document.paragraphs)
        return text.strip()
    except Exception as e:
        return f"[DOCX extraction error: {e}]"
