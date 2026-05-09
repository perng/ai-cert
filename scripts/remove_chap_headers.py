import glob
import os
import re

base_dir = '/Users/charles/ai-cert/subjects'
md_files = glob.glob(os.path.join(base_dir, '**', '*.md'), recursive=True)
qmd_files = glob.glob(os.path.join(base_dir, '**', '*.qmd'), recursive=True)
all_files = md_files + qmd_files

removed_count = 0

for file_path in all_files:
    if os.path.basename(file_path) == 'index.md' or os.path.basename(file_path) == 'index.qmd':
        continue
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        changed = False
        
        for line in lines:
            # Check if this line is an appended chap header like: ## Title {#chap-xxx}
            # Note: We only want to remove ones we appended, which are level 2 ## headers with {#chap-}
            if re.match(r'^## .*?\{#chap-[^}]+\}\s*$', line):
                changed = True
                removed_count += 1
            else:
                new_lines.append(line)
                
        if changed:
            # remove trailing newlines that we might have added before the header
            while new_lines and new_lines[-1].strip() == '':
                new_lines.pop()
            new_lines.append('\n')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"Removed {removed_count} erroneously appended chapter headers.")
