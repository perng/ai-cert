import yaml
import glob
import math

for filepath in glob.glob('/Users/charles/ai-cert/subjects/gen-ai/chapter*.yaml'):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue
            
    with open(filepath, 'w', encoding='utf-8') as f:
        # width=float("inf") prevents PyYAML from wrapping long lines
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float("inf"))
        
    print(f"Reformatted {filepath} successfully.")
