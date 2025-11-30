import yaml
import glob
import os

base_dir = r'c:\Users\charl\Documents\ai-cert\subjects\ai-foundation'
files = glob.glob(os.path.join(base_dir, 'chapter*.yaml'))

questions = []

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            if not data: continue
            
            # Handle both list and dict wrapper
            qs = data if isinstance(data, list) else data.get('questions', [])
            
            for q in qs:
                if 'tags' in q and 'past-exam' in q['tags'] and '114-4' in q['tags']:
                    questions.append({
                        'filepath': filepath,
                        'id': q['id'],
                        'text': q['text'],
                        'options': q['options'],
                        'correct_index': q['correct_index']
                    })
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

import json
print(json.dumps(questions, indent=2, ensure_ascii=False))
