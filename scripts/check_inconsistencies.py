import yaml
import glob
import os
import re

files = glob.glob('subjects/**/*.yaml', recursive=True)

inconsistencies = []

for f_path in files:
    if os.path.basename(f_path) == 'subject.yaml': continue
    try:
        with open(f_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or 'questions' not in data: continue
            
            for q in data['questions']:
                text = q.get('text', '')
                if "114年第四梯次" in text or "115年第一梯次" in text:
                    options = q.get('options', [])
                    correct_index = q.get('correct_index')
                    explanation = q.get('explanation', '')
                    
                    if correct_index is None:
                        inconsistencies.append({
                            'file': f_path, 'id': q.get('id'), 'issue': 'Missing correct_index'
                        })
                        continue
                    
                    if not (0 <= correct_index < len(options)):
                        inconsistencies.append({
                            'file': f_path, 'id': q.get('id'), 'issue': f'correct_index {correct_index} out of range (len={len(options)})'
                        })
                        continue
                    
                    # Heuristic: Check if explanation contains a different answer
                    # Many explanations follow the format: 正確答案為「...」
                    match = re.search(r'正確答案為[「「](.*?)[」」]', explanation)
                    if match:
                        expected_text = match.group(1).strip()
                        actual_text = options[correct_index].strip()
                        # Remove some common punctuation/suffixes for comparison
                        def clean(s):
                            return re.sub(r'[；。； ]', '', s).strip()
                        
                        if clean(expected_text) not in clean(actual_text) and clean(actual_text) not in clean(expected_text):
                            inconsistencies.append({
                                'file': f_path,
                                'id': q.get('id'),
                                'issue': 'Mismatch between explanation and correct_index',
                                'explanation_says': expected_text,
                                'correct_index_points_to': actual_text
                            })
    except Exception as e:
        print(f"Error processing {f_path}: {e}")

output_path = 'scripts/historical_inconsistencies.yaml'
with open(output_path, 'w', encoding='utf-8') as f:
    yaml.dump(inconsistencies, f, allow_unicode=True, sort_keys=False)

print(f"Found {len(inconsistencies)} potential inconsistencies.")
