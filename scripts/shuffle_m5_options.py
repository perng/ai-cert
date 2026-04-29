#!/usr/bin/env python3
"""
Shuffle quiz options in m5 YAML files so the correct answer isn't always at index 1.
Uses proper YAML parsing for data manipulation + line-based I/O to preserve formatting.
"""
import os
import re
import random
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M5_DIR = os.path.join(BASE_DIR, "subjects", "m5")

def shuffle_question_options(question):
    """Shuffle the options list and update correct_index."""
    if 'options' not in question:
        return
    
    opts = question['options']
    n = len(opts)
    if n <= 1:
        return
    
    correct_idx = question.get('correct_index', 0)
    if correct_idx < 0 or correct_idx >= n:
        return
    
    # Shuffle indices
    indices = list(range(n))
    random.shuffle(indices)
    
    # Reorder options
    question['options'] = [opts[k] for k in indices]
    
    # Find new position of the correct answer
    new_correct_idx = indices.index(correct_idx)
    question['correct_index'] = new_correct_idx

def process_file(filepath):
    """Process a single YAML file."""
    print(f"Processing {filepath}...")
    
    # Read original content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse YAML to get data
    data = yaml.safe_load(content)
    
    if 'questions' not in data:
        print(f"  No 'questions' key found, skipping.")
        return
    
    # Shuffle each question's options in the parsed data
    for q in data['questions']:
        shuffle_question_options(q)
    
    # Now we need to write back while preserving the original formatting.
    # Instead of using yaml.dump (which may alter formatting), we do line-based
    # find-and-replace for each question.
    
    lines = content.splitlines()
    
    # Find each question block and update it
    # We'll track the index in the questions list
    q_idx = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detect "options:" line
        m = re.match(r'^(\s*)options:\s*$', line)
        if m and q_idx < len(data['questions']):
            indent = m.group(1)
            q = data['questions'][q_idx]
            new_opts = q.get('options', [])
            new_correct = q.get('correct_index', 0)
            
            # Collect current options from file
            opt_start_idx = i + 1
            opt_lines = []
            opt_breaks = []  # indices where each option starts within opt_lines
            
            j = opt_start_idx
            while j < len(lines):
                opt_line = lines[j]
                # Check if this starts a new option (same indent level as options:)
                opt_match = re.match(r'^(' + re.escape(indent) + r'-\s)(.*)', opt_line)
                
                if opt_match:
                    opt_breaks.append(j)
                    opt_lines.append(opt_line)
                    j += 1
                elif opt_lines and re.match(r'^' + re.escape(indent) + r'\s+\S', opt_line):
                    # Continuation of previous option (more indented)
                    opt_lines.append(opt_line)
                    j += 1
                else:
                    break
            
            # We've captured options lines from opt_start_idx to j-1
            # Now we need to find correct_index: line
            correct_line_idx = -1
            for k in range(j, min(j + 5, len(lines))):
                if re.match(r'^' + re.escape(indent) + r'correct_index:\s*\d+', lines[k]):
                    correct_line_idx = k
                    break
            
            if not new_opts or correct_line_idx < 0:
                q_idx += 1
                i = j
                continue
            
            # We need to rebuild the options section with shuffled content
            # Get the old correct answer text to identify it
            old_opts_indices = list(range(len(opt_breaks)))
            
            # Map old options to new order
            # The old options at positions old_opts_indices need to be in the new order
            
            # We'll read the old option texts and find the correct one
            old_option_texts = []
            for idx, break_idx in enumerate(opt_breaks):
                # Get the first line of this option
                first_line = opt_lines[break_idx - opt_start_idx]
                # Get the text after "- "
                m2 = re.match(r'^' + re.escape(indent) + r'- (.*)', first_line)
                opt_text = m2.group(1) if m2 else ""
                # Add continuation lines
                full_text = [opt_text]
                k = break_idx + 1
                while k < (opt_breaks[idx + 1] if idx + 1 < len(opt_breaks) else j):
                    cont_line = lines[k]
                    # Remove the indent prefix for comparison
                    full_text.append(cont_line)
                    k += 1
                old_option_texts.append(full_text)
            
            # Replace the options block with shuffled version
            # We need to construct new option lines from the new_opts list
            new_option_lines = []
            for opt_text in new_opts:
                # The text might be multi-line if it contains \n
                opt_lines_split = opt_text.split('\n')
                new_option_lines.append(f"{indent}- {opt_lines_split[0]}")
                for sub_line in opt_lines_split[1:]:
                    new_option_lines.append(f"{indent}  {sub_line}")
            
            # Replace lines from opt_start_idx to j-1 with new_option_lines
            replacement = new_option_lines
            old_range_len = j - opt_start_idx
            
            # Calculate the difference in line count
            diff = len(replacement) - old_range_len
            
            # Replace the options lines
            lines[opt_start_idx:j] = replacement
            
            # Adjust correct_line_idx if needed
            if correct_line_idx >= j:
                # correct_index line is after the options block, adjust by diff
                pass
            
            # Now update the correct_index: line
            # Since we changed the number of lines, correct_line_idx may have shifted
            # Actually correct_line_idx is relative to the original lines, so we need to recalculate
            # After replacement, positions after opt_start_idx shift
            new_correct_line_idx = correct_line_idx
            if correct_line_idx >= j:
                new_correct_line_idx = correct_line_idx + diff
            elif correct_line_idx > opt_start_idx and correct_line_idx < j:
                # This shouldn't happen normally, correct_index is after options
                pass
            
            lines[new_correct_line_idx] = f"{indent}correct_index: {new_correct}"
            
            # Update i to continue after this question
            if new_correct_line_idx >= opt_start_idx:
                i = new_correct_line_idx + 1
            else:
                i = j + diff
            
            q_idx += 1
        else:
            i += 1
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"  Done. Processed {q_idx} questions.")

def main():
    random.seed()  # Use true randomness
    
    # Process all chapter YAML files in m5
    pattern = os.path.join(M5_DIR, "chapter*.yaml")
    import glob
    files = sorted(glob.glob(pattern))
    
    for filepath in files:
        process_file(filepath)
    
    print("All m5 files processed!")

if __name__ == "__main__":
    main()
