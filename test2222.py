import pdfplumber

pdf_path = "C:\\Users\\Lenovo\\Downloads\\2017 Crop.pdf"  # Use your actual PDF file

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages[:5]):  # Check first 5 pages
        text = page.extract_text()
        print(f"--- Page {i+1} ---\n{text}\n")
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages[:5]):  # Check first 5 pages
        tables = page.extract_tables()
        print(f"--- Page {i+1} ---\n{tables}\n")
