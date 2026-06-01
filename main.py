from pypdf import PdfReader

reader = PdfReader(
    "Summary Notes - Topic 6 Magnetism and Electromagnetism - Edexcel Physics IGCSE.pdf"
)

for page in reader.pages:
    print(page.extract_text())