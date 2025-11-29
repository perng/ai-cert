import pypdf
import os

pdf_path = r"docs/iPAS-level1/AI應用規劃師(初級)-學習指引-科目2生成式AI應用與規劃.pdf"
output_path = "pdf_content.txt"

try:
    reader = pypdf.PdfReader(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for page in reader.pages:
            text = page.extract_text()
            f.write(text)
            f.write("\n\n")
    print(f"Successfully extracted text to {output_path}")
except Exception as e:
    print(f"Error extracting text: {e}")
