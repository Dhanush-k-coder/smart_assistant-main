from pdfminer.high_level import extract_text

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text(file)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return "❌ Unsupported file type"
