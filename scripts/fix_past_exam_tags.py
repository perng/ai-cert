import glob
import os
import re

base_dir = '/Users/charles/ai-cert/subjects'
yaml_files = glob.glob(os.path.join(base_dir, '**', '*.yaml'), recursive=True)

updated_questions = 0
updated_files = 0

for file_path in yaml_files:
    if os.path.basename(file_path) == 'subject.yaml': continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    in_tags = False
    question_is_past_exam = False
    changed_file = False
    
    for i in range(len(lines)):
        line = lines[i]
        
        # Detect new question
        if line.startswith('- id:') or line.startswith('- chapter_title:'):
            question_is_past_exam = False
            
        if '梯次' in line or '歷屆考題' in line or 'past-exam' in line:
            question_is_past_exam = True
            
        if line.startswith('  tags:'):
            new_lines.append(line)
            # Find all tags
            j = i + 1
            has_sec_past_exam = False
            tags_to_add = []
            
            while j < len(lines) and lines[j].startswith('  - '):
                if 'sec-past-exam' in lines[j]:
                    has_sec_past_exam = True
                tags_to_add.append(lines[j])
                j += 1
                
            if question_is_past_exam and not has_sec_past_exam:
                tags_to_add.append('  - sec-past-exam\n')
                changed_file = True
                updated_questions += 1
                
            new_lines.extend(tags_to_add)
            
            # fast forward i to j-1
            continue
            
        # If we are in the middle of a tag list and handled it, we just skip because we handled it above
        if line.startswith('  - ') and i > 0 and lines[i-1].startswith('  tags:'):
            continue
        if line.startswith('  - ') and i > 1 and lines[i-2].startswith('  tags:'):
            continue
            
        # Simplified: The above approach is too complex. 
        # Let's do a block-by-block text replacement.
        pass

# Safe block-by-block approach
updated_files = 0
updated_questions = 0

for file_path in yaml_files:
    if os.path.basename(file_path) == 'subject.yaml': continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    blocks = content.split('\n- ')
    new_blocks = []
    changed_file = False
    
    for i, block in enumerate(blocks):
        if i == 0 and not block.startswith('- '):
            new_blocks.append(block)
            continue
            
        full_block = block if i == 0 else '- ' + block
        
        is_past_exam = False
        if '梯次' in full_block or '歷屆考題' in full_block or 'past-exam' in full_block:
            is_past_exam = True
            
        if is_past_exam and 'sec-past-exam' not in full_block:
            # Add sec-past-exam to tags
            # Replace '  tags:\n' with '  tags:\n  - sec-past-exam\n'
            # Also replace section_title if exists
            
            if '  tags:' in full_block:
                full_block = full_block.replace('  tags:\n', '  tags:\n  - sec-past-exam\n')
            else:
                full_block += '  tags:\n  - sec-past-exam\n'
                
            # Optionally replace section_title with 歷屆考題
            full_block = re.sub(r'  section_title:.*\n', '  section_title: 歷屆考題\n', full_block)
                
            changed_file = True
            updated_questions += 1
            
        new_blocks.append(full_block if i == 0 else full_block[2:])
        
    if changed_file:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n- '.join(new_blocks) if len(new_blocks) > 1 else new_blocks[0])
        updated_files += 1

print(f"Added 'sec-past-exam' tag to {updated_questions} questions across {updated_files} files.")
