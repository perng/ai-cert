import pypdf
import sys

def extract_section(pdf_path, keyword, output_file):
    try:
        reader = pypdf.PdfReader(pdf_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Searching for '{keyword}' in {pdf_path}...\n")
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                lines = text.split('\n')
                found_header = False
                for line in lines:
                    # Check for "3.3" at the start of a line (ignoring leading whitespace)
                    if line.strip().startswith(keyword):
                        found_header = True
                        f.write(f"\n--- Found Header '{keyword}' on page {i+1} ---\n")
                        f.write(f"Header Line: {line.strip()}\n")
                        break
                
                if found_header:
                    f.write(f"\n--- Page {i+1} Content ---\n")
                    f.write(text)
                    f.write("\n------------------------\n")
                    
                    # Extract next page too
                    if i + 1 < len(reader.pages):
                        f.write(f"\n--- Page {i+2} Content (Continuation) ---\n")
                        f.write(reader.pages[i+1].extract_text())
                        f.write("\n------------------------\n")

    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    pdf_file = r"c:\Users\charl\Documents\ai-cert\docs\iPAS-level2\AI應用規劃師(中級)-學習指引-科目1人工智慧技術應用規劃.pdf"
    output_path = r"c:\Users\charl\Documents\ai-cert\scripts\extracted_5_2.txt"
    # Search for "5.2"
    extract_section(pdf_file, "5.2", output_path)
