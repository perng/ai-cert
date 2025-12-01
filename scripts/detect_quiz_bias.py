import os
import yaml
import re
import statistics
from pathlib import Path

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def has_english(text):
    # Check for latin characters inside parentheses, typical for "Term (English)"
    # or just English words.
    return bool(re.search(r'[a-zA-Z]', str(text)))

def detect_bias(subjects_dir):
    report = {}
    
    subjects_dir = Path(subjects_dir)
    yaml_files = sorted(list(subjects_dir.glob("**/*.yaml")))
    
    for yaml_file in yaml_files:
        if yaml_file.name == "subject.yaml":
            continue
            
        try:
            data = load_yaml(yaml_file)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")
            continue
            
        if not data or 'questions' not in data:
            continue
            
        questions = data['questions']
        file_issues = []
        
        for q in questions:
            if 'options' not in q or 'correct_index' not in q:
                continue
                
            options = q['options']
            correct_idx = q['correct_index']
            
            # Check indices
            if correct_idx < 0 or correct_idx >= len(options):
                continue
                
            correct_opt = options[correct_idx]
            other_opts = [o for i, o in enumerate(options) if i != correct_idx]
            
            if not other_opts:
                continue
                
            # 1. Length Bias
            len_correct = len(str(correct_opt))
            len_others = [len(str(o)) for o in other_opts]
            avg_len_others = statistics.mean(len_others) if len_others else 0
            
            # Threshold: Correct is significantly longer (e.g., > 1.5x average of others, and absolute difference is noticeable > 5 chars)
            is_length_biased = False
            if avg_len_others > 0 and len_correct > 1.5 * avg_len_others and (len_correct - avg_len_others) > 5:
                is_length_biased = True
            
            # 2. Translation Bias
            # Check if correct option has English but others don't
            has_eng_correct = has_english(correct_opt)
            has_eng_others = [has_english(o) for o in other_opts]
            
            is_translation_biased = False
            if has_eng_correct and not any(has_eng_others):
                is_translation_biased = True
                
            if is_length_biased or is_translation_biased:
                issue = {
                    "id": q.get('id'),
                    "text": q.get('text'),
                    "issues": []
                }
                if is_length_biased:
                    issue['issues'].append(f"Length Bias: Correct({len_correct}) vs Others({len_others})")
                if is_translation_biased:
                    issue['issues'].append("Translation Bias: Only correct option has English")
                
                file_issues.append(issue)
        
        if file_issues:
            report[str(yaml_file)] = file_issues

    return report

if __name__ == "__main__":
    import json
    report = detect_bias("subjects")
    print(json.dumps(report, indent=2, ensure_ascii=False))
