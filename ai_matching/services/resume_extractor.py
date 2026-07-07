import os

from pypdf import PdfReader
from docx import Document


def extract_resume_text(file):
    """
    Extract text from PDF or DOCX resumes.
    """

    extension = os.path.splitext(file.name)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file)

    if extension == ".docx":
        return extract_docx_text(file)

    raise ValueError(
        "Only PDF and DOCX files are supported."
    )


def extract_pdf_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_docx_text(file):

    document = Document(file)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    return text.strip()