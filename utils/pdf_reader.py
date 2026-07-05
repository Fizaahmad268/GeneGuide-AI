import fitz

def extract_text(pdf_file):
    text = ""

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf:
        page_text = page.get_text()
        text += page_text

    pdf.close()

    if text.strip() == "":
        return "⚠️ This PDF appears to be scanned or contains no selectable text."

    return text