import glob
import re
import os

def fix_lists_in_file(f_path):
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    # regex for list starts: *, -, +, or 1.
    list_pattern = re.compile(r'^(\s*)(\*|\-|\+|\d+\.)\s')
    
    for i in range(len(lines)):
        line = lines[i]
        if i > 0:
            prev_line = lines[i-1]
            
            # If current line is a list item
            if list_pattern.match(line):
                # If previous line is NOT empty, NOT a header, and NOT a list item itself
                if prev_line.strip() != '' and not prev_line.strip().startswith('#') and not list_pattern.match(prev_line):
                    # Add an empty line
                    new_lines.append('')
        
        new_lines.append(line)
        
    new_content = '\n'.join(new_lines)
    if new_content != content:
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

all_files = glob.glob('subjects/**/*.md', recursive=True) + glob.glob('subjects/**/*.qmd', recursive=True)
fixed_count = 0

for f_path in all_files:
    if fix_lists_in_file(f_path):
        print(f"Fixed list formatting in {f_path}")
        fixed_count += 1

print(f"Total files fixed: {fixed_count}")
