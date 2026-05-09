import yaml
import glob
import sys
import os

REQUIRED_FIELDS = {
    'id', 
    'text', 
    'type', 
    'options', 
    'correct_index', 
    'explanation', 
    'tags', 
    'usage'
}

def check_and_format_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return 0

    if not data:
        print(f"Skipping empty file: {filepath}")
        return 0
        
    items = data.get('questions', data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        print(f"Warning: Unexpected data structure in {filepath}. Expected a list of questions.")
        return 0

    has_errors = False
    
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            print(f"[{filepath}] Item {i} is not a dictionary.")
            has_errors = True
            continue
            
        item_keys = set(item.keys())
        missing_fields = REQUIRED_FIELDS - item_keys
        
        # We can also check for extra fields, but usually missing fields are the main issue.
        if missing_fields:
            item_id = item.get('id', f'index {i}')
            print(f"[{filepath}] Question ID {item_id} is missing fields: {', '.join(missing_fields)}")
            has_errors = True

    with open(filepath, 'w', encoding='utf-8') as f:
        # width=float("inf") prevents PyYAML from wrapping long lines
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float("inf"))
        
    if has_errors:
        print(f"Reformatted {filepath}, but found missing fields as listed above.")
        
    return len(items)

if __name__ == "__main__":
    # Scan all yaml files in subjects directory to cover gen-ai, m1, etc.
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/Users/charles/ai-cert/subjects'
    yaml_files = glob.glob(os.path.join(base_dir, '**', '*.yaml'), recursive=True)
    
    total_questions = 0
    files_processed = 0
    
    for filepath in yaml_files:
        # Skip quarto config files or subject.yaml
        if os.path.basename(filepath) in ['_quarto.yml', 'subject.yaml']:
            continue
        total_questions += check_and_format_yaml(filepath)
        files_processed += 1
        
    print(f"Scan complete! Scanned {total_questions} questions across {files_processed} files.")
