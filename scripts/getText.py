import pdfplumber

pdf = pdfplumber.open('scripts/data.pdf')
page = pdf.pages[5]
text = page.extract_text()
print(text)
pdf.close()
