import os
import yaml

def update_usage(file_path):
    print(f"Processing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'questions' not in data:
            print(f"Skipping {file_path} (no questions)")
            return

        questions = data['questions']
        
        mock_questions = []
        quiz_candidates = []
        
        # First pass: Identify mock vs quiz candidates
        for q in questions:
            text = q.get('text', '')
            # Heuristic: "情境" in text or length > 150
            if '情境' in text or len(text) > 150:
                q['usage'] = 'mock'
                mock_questions.append(q)
            else:
                quiz_candidates.append(q)
                
        # Second pass: Assign quiz vs both
        # Max 10 for quiz
        count_quiz = 0
        for q in quiz_candidates:
            if count_quiz < 10:
                q['usage'] = 'quiz'
                count_quiz += 1
            else:
                q['usage'] = 'both'
                
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            # default_flow_style=False ensures block format for lists/dicts
            # allow_unicode=True ensures Chinese characters are not escaped
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"Updated {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root_dir = 'subjects'
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.yaml') and file != 'subject.yaml':
                update_usage(os.path.join(root, file))

if __name__ == '__main__':
    main()
