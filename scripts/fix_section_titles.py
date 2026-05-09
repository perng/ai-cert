import os
import glob
import yaml
import re

def parse_markdown_headers(md_path):
    header_map = {}
    past_exam_title = None
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'^(#+)\s+(.+?)\s*(?:\{#(sec-[^}]+|chap-[^}]+)\})?$', line.strip())
                if match:
                    title = match.group(2).strip()
                    tag_id = match.group(3)
                    if tag_id:
                        header_map[tag_id] = title
                    
                    if "考題" in title or "考點" in title or "past-exam" in line.lower() or "summary" in str(tag_id):
                        past_exam_title = title
    except Exception as e:
        print(f"Error reading {md_path}: {e}")
    return header_map, past_exam_title

base_dir = '/Users/charles/ai-cert/subjects'
yaml_files = glob.glob(os.path.join(base_dir, '**', '*.yaml'), recursive=True)

for yml_file in yaml_files:
    if os.path.basename(yml_file) in ['_quarto.yml', 'subject.yaml']:
        continue
        
    md_file = yml_file.replace('.yaml', '.md')
    if not os.path.exists(md_file):
        md_file = yml_file.replace('.yaml', '.qmd')
        
    if not os.path.exists(md_file):
        continue
        
    header_map, past_exam_title = parse_markdown_headers(md_file)
    if not header_map and not past_exam_title:
        continue
        
    with open(yml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    if not data: continue
    
    items = data.get('questions', data) if isinstance(data, dict) else data
    if not isinstance(items, list): continue
    
    changed = False
    for item in items:
        if not isinstance(item, dict): continue
        
        tags = item.get('tags', [])
        
        found_title = None
        
        for tag in tags:
            if tag in header_map:
                found_title = header_map[tag]
                break
                
        if not found_title and ('past-exam' in tags or any('114' in t or '115' in t for t in tags)) and past_exam_title:
            found_title = past_exam_title
            
        if found_title and item.get('section_title') != found_title:
            item['section_title'] = found_title
            changed = True
            
    if changed:
        with open(yml_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float("inf"))
        print(f"Updated section_titles in {yml_file}")

print("Done")
