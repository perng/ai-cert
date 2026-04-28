import yaml, glob
import os

for f in sorted(glob.glob("subjects/m5/*.yaml")):
    with open(f, "r") as fh:
        data = yaml.safe_load(fh)
    
    changed = False
    for i, q in enumerate(data.get("questions", [])):
        options = q.get("options", [])
        correct_idx = q.get("correct_index", -1)
        if not options or correct_idx == -1: continue
        
        correct_opt = options[correct_idx]
        correct_len = len(str(correct_opt))
        
        other_lens = [len(str(opt)) for j, opt in enumerate(options) if j != correct_idx]
        if not other_lens: continue
        
        avg_other_len = sum(other_lens) / len(other_lens)
        
        if correct_len > 1.5 * avg_other_len and correct_len - avg_other_len > 10:
            print(f"{os.path.basename(f)}: Question {i} (id: {q.get('id')})")
            print(f"  Correct len: {correct_len}, Avg other len: {avg_other_len:.1f}")
            for j, opt in enumerate(options):
                print(f"  {'*' if j==correct_idx else ' '} {j}: {opt}")
            print("-" * 40)
