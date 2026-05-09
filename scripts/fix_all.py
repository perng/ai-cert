import yaml
import glob
import os
import re

base_dir = '/Users/charles/ai-cert/subjects'
yaml_files = glob.glob(os.path.join(base_dir, '**', '*.yaml'), recursive=True)

# 1. Fix Duplicates
seen_ids = set()
duplicates_fixed = 0

for yml_file in yaml_files:
    if os.path.basename(yml_file) in ['_quarto.yml', 'subject.yaml']:
        continue
        
    try:
        with open(yml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data: continue
        
        items = data.get('questions', data) if isinstance(data, dict) else data
        if not isinstance(items, list): continue
        
        changed = False
        for item in items:
            if not isinstance(item, dict): continue
            
            q_id = str(item.get('id', ''))
            original_id = q_id
            
            if not q_id:
                q_id = f"missing_{duplicates_fixed}"
                item['id'] = q_id
                changed = True
                
            if q_id in seen_ids:
                # Find a unique id
                counter = 1
                while f"{original_id}_{counter}" in seen_ids:
                    counter += 1
                new_id = f"{original_id}_{counter}"
                item['id'] = new_id
                seen_ids.add(new_id)
                changed = True
                duplicates_fixed += 1
            else:
                seen_ids.add(q_id)
                
        if changed:
            with open(yml_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float("inf"))
                
    except Exception as e:
        print(f"Error processing duplicates in {yml_file}: {e}")

print(f"Fixed {duplicates_fixed} duplicate IDs.")

# 2. Fix Missing Headers
headers_added = 0

for yml_file in yaml_files:
    if os.path.basename(yml_file) in ['_quarto.yml', 'subject.yaml']:
        continue
        
    md_file = yml_file.replace('.yaml', '.md')
    if not os.path.exists(md_file):
        md_file = yml_file.replace('.yaml', '.qmd')
        
    if not os.path.exists(md_file):
        continue
        
    # Get existing headers
    existing_tags = set()
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match {#sec-...} or {#chap-...}
            tags_in_md = re.findall(r'\{#(sec-[^}]+|chap-[^}]+)\}', content)
            existing_tags.update(tags_in_md)
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        continue

    # Find missing headers required by YAML
    try:
        with open(yml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data: continue
        
        items = data.get('questions', data) if isinstance(data, dict) else data
        if not isinstance(items, list): continue
        
        # We need a map of missing tag to its title
        missing_sections = {}
        
        for item in items:
            if not isinstance(item, dict): continue
            
            tags = item.get('tags', [])
            q_title = item.get('section_title', 'Unknown Section')
            
            # Find the primary section tag (sec- only)
            sec_tag = None
            for t in tags:
                if t.startswith('sec-'):
                    sec_tag = t
                    break
                    
            if sec_tag and sec_tag not in existing_tags:
                if sec_tag not in missing_sections:
                    missing_sections[sec_tag] = q_title
                    
        # Append missing sections to md_file
        if missing_sections:
            with open(md_file, 'a', encoding='utf-8') as f:
                f.write("\n\n")
                for tag, title in missing_sections.items():
                    f.write(f"## {title} {{#{tag}}}\n\n")
                    headers_added += 1
                    existing_tags.add(tag) # prevent adding twice just in case
            print(f"Appended {len(missing_sections)} missing headers to {md_file}")
            
    except Exception as e:
        print(f"Error processing missing headers in {yml_file}: {e}")

print(f"Appended {headers_added} missing headers across all markdown files.")
