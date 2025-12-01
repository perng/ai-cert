
import re

source_path = r"c:\Users\charl\Documents\ai-cert\temp_pdf_content.txt"
dest_path = r"c:\Users\charl\Documents\ai-cert\subjects\m2\chapter1.qmd"

with open(source_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract Chapter 4 (approx lines 2906 to 4215, 0-indexed is 2905 to 4214)
# Note: The line numbers from view_file are 1-indexed.
start_line = 2906 - 1
end_line = 4215 - 1
chapter_lines = lines[start_line:end_line]

# Filter out headers and footers
cleaned_lines = []
skip_next = False

for line in chapter_lines:
    # Remove page headers
    if " 第四章" in line:
        continue
    # Remove page numbers like 4-1, 4-2
    if re.match(r"^\s*4-\d+\s*$", line):
        continue
    # Remove isolated "AI" lines that appear in headers
    if line.strip() == "AI":
        continue
    
    cleaned_lines.append(line)

# Read destination file header
with open(dest_path, "r", encoding="utf-8") as f:
    dest_lines = f.readlines()

# Keep the first few lines (Title and Intro)
# Assuming the first 4 lines are header and intro.
# Let's check the file content again to be sure.
# 1: # AI 專案生命週期 {#sec-m2-ch1}
# 2: 
# 3: 成功的 AI 專案需要嚴謹的生命週期管理。本章將介紹 AI 專案從評估、規劃到風險管理的完整流程。
# 4: 
# 5: ## AI 導入評估與可行性研究 {#sec-feasibility}
# So keep lines 0-3 (0-indexed).

header_content = dest_lines[:4]

# Combine
new_content = "".join(header_content) + "\n" + "".join(cleaned_lines)

with open(dest_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done")
