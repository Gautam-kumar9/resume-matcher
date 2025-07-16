import fitz  # PyMuPDF
import re
import spacy

nlp_name = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_name(text):
    # Try NER using spaCy (filtering likely headers)
    doc = nlp_name(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) <= 3 and ent.start_char < 100:
            return ent.text.strip()

    # Fallback 1: Check first few lines
    lines = text.strip().split('\n')[:5]
    for line in lines:
        name_match = re.match(r'^([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)$', line.strip())
        if name_match:
            return name_match.group(1).strip()

    # Fallback 2: Regex for "Name: John Doe"
    match = re.search(r"(?i)(name|full name)[\s:]*([A-Z][a-z]+\s[A-Z][a-z]+)", text)
    return match.group(2).strip() if match else "Unknown"
