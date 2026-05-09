import glob
import os
import re
import yaml

base_dir = '/Users/charles/ai-cert/subjects'
yaml_files = glob.glob(os.path.join(base_dir, '**', '*.yaml'), recursive=True)

headers_injected = 0
headers_appended = 0

for yml_file in yaml_files:
    if os.path.basename(yml_file) in ['_quarto.yml', 'subject.yaml']:
        continue
        
    md_file = yml_file.replace('.yaml', '.md')
    if not os.path.exists(md_file):
        md_file = yml_file.replace('.yaml', '.qmd')
        
    if not os.path.exists(md_file):
        continue
        
    # Get existing tags and content
    existing_tags = set()
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            tags_in_md = re.findall(r'\{#(sec-[^}]+|chap-[^}]+)\}', line)
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
        
        missing_sections = {}
        
        for item in items:
            if not isinstance(item, dict): continue
            
            tags = item.get('tags', [])
            q_title = item.get('section_title', '').strip()
            
            if not q_title:
                continue
            
            sec_tag = None
            for t in tags:
                if t.startswith('sec-'):
                    sec_tag = t
                    break
                    
            if sec_tag and sec_tag not in existing_tags:
                if sec_tag not in missing_sections:
                    missing_sections[sec_tag] = q_title
                    
        if not missing_sections:
            continue
            
        # Process missing sections
        new_lines = []
        appended_sections = {}
        
        for i, line in enumerate(lines):
            matched_injection = False
            
            # Check if this line is a header that matches a missing section title
            header_match = re.search(r'^(#+)\s+(.+?)\s*$', line.strip())
            if header_match:
                # Make sure it doesn't already have a tag
                if '{#' not in line:
                    title = header_match.group(2).strip()
                    
                    # Try to find a missing section with this title
                    for tag, missing_title in list(missing_sections.items()):
                        # Fuzzy match: clean numbering and parens from markdown title
                        cand_clean = re.sub(r'^\d+(\.\d+)*\s+', '', title)
                        cand_clean = re.sub(r'\s*\([^)]*\)', '', cand_clean).strip()
                        
                        if missing_title == cand_clean or missing_title in title:
                            # Inject tag!
                            lines[i] = line.rstrip() + f" {{#{tag}}}\n"
                            existing_tags.add(tag)
                            del missing_sections[tag]
                            headers_injected += 1
                            matched_injection = True
                            break

        # Any remaining missing_sections must be completely missing, append them
        with open(md_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
            if missing_sections:
                f.write("\n\n")
                for tag, title in missing_sections.items():
                    f.write(f"## {title} {{#{tag}}}\n\n")
                    headers_appended += 1
                    
        if missing_sections:
            print(f"Appended {len(missing_sections)} headers to {md_file}")
            
    except Exception as e:
        print(f"Error processing {yml_file}: {e}")

print(f"Injected {headers_injected} tags into existing headers.")
print(f"Appended {headers_appended} new headers across all files.")
