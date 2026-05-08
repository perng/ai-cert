import yaml
import glob
import json

questions = []
for file in glob.glob('/Users/charles/ai-cert/subjects/gen-ai/chapter*.yaml'):
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    items = data.get('questions', []) if isinstance(data, dict) else data
    if not isinstance(items, list):
        items = [items]
        
    for item in items:
        if isinstance(item, dict) and item.get('explanation') == '（115年第一梯次）公告試題':
            questions.append({
                'file': file,
                'id': item['id'],
                'text': item['text'],
                'options': item['options'],
                'correct_index': item['correct_index']
            })

with open('/tmp/questions_to_explain.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(questions)} questions.")
