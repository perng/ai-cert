import yaml
import glob
import os

patterns = ["114年第四梯次", "115年第一梯次"]
files = glob.glob('subjects/**/*.yaml', recursive=True)

results = []

for f_path in files:
    if os.path.basename(f_path) == 'subject.yaml': continue
    try:
        with open(f_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or 'questions' not in data: continue
            
            for q in data['questions']:
                text = q.get('text', '')
                if any(p in text for p in patterns):
                    results.append({
                        'file': f_path,
                        'id': q.get('id'),
                        'text': text,
                        'options': q.get('options', []),
                        'correct_index': q.get('correct_index'),
                        'explanation': q.get('explanation', '')
                    })
    except Exception as e:
        print(f"Error processing {f_path}: {e}")

output_path = 'scripts/historical_questions_review.yaml'
with open(output_path, 'w', encoding='utf-8') as f:
    yaml.dump(results, f, allow_unicode=True, sort_keys=False)

print(f"Extracted {len(results)} historical questions to {output_path}")
