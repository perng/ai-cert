import glob
import os
import re

base_dir = '/Users/charles/ai-cert/subjects'
md_files = glob.glob(os.path.join(base_dir, '**', 'chapter*.md'), recursive=True)
qmd_files = glob.glob(os.path.join(base_dir, '**', 'chapter*.qmd'), recursive=True)
all_files = md_files + qmd_files

count = 0

for file_path in all_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if the section already exists
        if '## 歷屆考題' not in content:
            # Append it to the end of the file
            # Ensure there's a blank line before adding the new section
            if not content.endswith('\n\n'):
                if content.endswith('\n'):
                    append_text = '\n## 歷屆考題 {#sec-past-exam}\n\n請做測驗看歷屆考題。\n\n'
                else:
                    append_text = '\n\n## 歷屆考題 {#sec-past-exam}\n\n請做測驗看歷屆考題。\n\n'
            else:
                append_text = '## 歷屆考題 {#sec-past-exam}\n\n請做測驗看歷屆考題。\n\n'
                
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(append_text)
            count += 1
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

print(f"Successfully added '歷屆考題' section to {count} files.")
