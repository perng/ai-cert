import yaml
import random
import glob
import os
import sys

def shuffle_file(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return
            data = yaml.safe_load(content)
            
        questions = []
        if isinstance(data, list):
            questions = data
        elif isinstance(data, dict) and 'questions' in data:
            questions = data['questions']
        else:
            print(f"Skipping {filepath}: Unknown structure")
            return

        changed = False
        for question in questions:
            if 'options' in question and 'correct_index' in question:
                options = question['options']
                try:
                    correct_idx = int(question['correct_index'])
                except ValueError:
                    print(f"Warning: Invalid correct_index format in question {question.get('id')}")
                    continue
                
                if correct_idx < 0 or correct_idx >= len(options):
                    print(f"Warning: Invalid correct_index {correct_idx} in question {question.get('id')}")
                    continue
                
                correct_option = options[correct_idx]
                
                # Shuffle options
                random.shuffle(options)
                
                # Find new index
                new_idx = options.index(correct_option)
                
                question['options'] = options
                question['correct_index'] = new_idx
                changed = True
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                try:
                    yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
                except TypeError:
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, width=1000)
            print(f"Updated {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        import traceback
        traceback.print_exc()

def main():
    base_dir = r'c:\Users\charl\Documents\ai-cert\subjects'
    patterns = [
        os.path.join(base_dir, 'gen-ai', 'chapter*.yaml'),
        os.path.join(base_dir, 'ai-foundation', 'chapter*.yaml')
    ]
    
    files = []
    for p in patterns:
        files.extend(glob.glob(p))
        
    print(f"Found {len(files)} files.")
    
    for f in files:
        if 'extra' in f: continue
        shuffle_file(f)

if __name__ == "__main__":
    main()
