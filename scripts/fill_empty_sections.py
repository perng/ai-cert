import glob
import re

files = glob.glob('subjects/gen-ai/chapter*.md')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    
    for i in range(len(lines)):
        line = lines[i]
        new_lines.append(line)
        
        if re.match(r'^#+\s', line):
            has_content = False
            for j in range(i+1, len(lines)):
                next_line = lines[j]
                if re.match(r'^#+\s', next_line):
                    break
                if next_line.strip() != '':
                    has_content = True
                    break
                    
            if not has_content:
                title_match = re.search(r'^#+\s+([^#\{]+)', line)
                if title_match:
                    title = title_match.group(1).strip()
                    if '歷屆考題' in title:
                        new_lines.append("\n請做測驗看歷屆考題。\n\n")
                    else:
                        new_lines.append(f"\n本節內容將探討「{title}」的相關概念與技術細節。請配合測驗題目進行學習。\n\n")
                        
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("Done filling empty sections.")
