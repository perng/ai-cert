import json
import os
import re

with open('/Users/charles/ai-cert/assets/content.json', 'r', encoding='utf-8') as f:
    content = json.load(f)

for subject in content.get('subjects', []):
    # Maps subject IDs to directory names
    subj_dir_map = {
        '1': 'ai-foundation',
        '2': 'gen-ai',
        '3': 'm1',
        '4': 'm2',
        '5': 'm3',
        '6': 'm4',
        '7': 'm5'
    }
    
    dir_name = subj_dir_map.get(str(subject.get('id')))
    if not dir_name: continue
    
    for chapter in subject.get('chapters', []):
        chapter_id = chapter.get('id', '')
        if not chapter_id: continue
        
        # Determine the file path
        # In build_content.py, chapter['id'] is something like 'chap-m1-ch1' or 'ai-foundation-chapter1'
        # we can just use the chapter title to search through all md/qmd files in that directory
        # actually, easier: build_content.py adds 'file_path' or something? No.
        # But we know the directory is dir_name, and the file is likely chapterX.md or chapterX.qmd.
        
        has_empty_past_exam = False
        for section in chapter.get('sections', []):
            if section.get('id') == 'sec-past-exam' or '歷屆考題' in section.get('title', ''):
                if len(section.get('questions', [])) == 0:
                    has_empty_past_exam = True
                    
        if has_empty_past_exam:
            # We need to find the markdown file for this chapter.
            # Usually chapter title matches the title in the frontmatter or the first # header.
            # Let's search all md/qmd files in dir_name for this title.
            for ext in ['md', 'qmd']:
                for i in range(1, 20): # chapter1 to chapter15
                    fpath = f"/Users/charles/ai-cert/subjects/{dir_name}/chapter{i}.{ext}"
                    if os.path.exists(fpath):
                        with open(fpath, 'r', encoding='utf-8') as f:
                            text = f.read()
                        if chapter.get('title') in text:
                            # This is likely the file. Remove the past exam section!
                            new_text = re.sub(r'\n*## 歷屆考題 \{#sec-past-exam\}\n+請做測驗看歷屆考題。\n*', '\n\n', text)
                            if new_text != text:
                                with open(fpath, 'w', encoding='utf-8') as f:
                                    f.write(new_text)
                                print(f"Removed empty past exam section from {fpath}")
