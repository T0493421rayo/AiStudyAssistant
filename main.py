from pypdf import PdfReader

reader = PdfReader("magnetism.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

print(text)