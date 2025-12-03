import os
import re
import random
import glob

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into blocks. Assuming top-level list items start with "- " at the beginning of a line
    # or indented if under a key. In the viewed file, they are indented by 0 or 2 spaces depending on context?
    # In 'subjects/m1/chapter1.yaml':
    # questions:
    # - id: ...
    # So they are indented by 0 spaces? No, usually YAML lists under a key are indented.
    # Let's check the file content again carefully.
    # Line 1: questions:
    # Line 2: - id: 3101
    # It seems there is NO indentation for the dash? Or maybe 2 spaces?
    # The view_file output shows:
    # 1: questions:
    # 2: - id: 3101
    # If I assume standard YAML, it could be indented.
    # Let's detect the indentation of the first "- id:" or just "- ".
    
    # Actually, splitting by "\n- " (newline, dash, space) is risky if indentation varies.
    # But looking at the file, it seems consistent.
    
    # Let's try to parse line by line to be safer.
    
    lines = content.splitlines()
    new_lines = []
    
    in_options = False
    options_buffer = []
    current_options = []
    correct_index_line_idx = -1
    current_question_start_idx = -1
    
    # We need to process question by question.
    # A question starts with "- " (possibly indented).
    # But we only care about the "options:" and "correct_index:" fields within a block.
    
    # Strategy:
    # Iterate through lines.
    # When we see "options:", we start capturing options.
    # We stop capturing when we see a line that has the same indentation as "options:" or less, OR "correct_index:".
    # Actually "correct_index" usually follows options.
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detect "options:"
        # Regex to match "  options:" or "options:"
        match_options = re.match(r'^(\s*)options:\s*$', line)
        if match_options:
            indent = match_options.group(1)
            # Start collecting options
            new_lines.append(line) # Keep "options:" line
            i += 1
            
            opts = []
            current_opt_lines = []
            
            while i < len(lines):
                opt_line = lines[i]
                # Check if it's a new option
                # It should start with indent + "  - " ? 
                # Usually options are indented by 2 spaces relative to "options:" key?
                # Or same level if it's a list?
                # In the file:
                #   options:
                #   - ...
                # So same indentation as "options:" key?
                # Wait, line 7: "  options:" (2 spaces indent?)
                # Line 8: "  - ..." (2 spaces indent)
                # So the dash is aligned with the start of "options"?
                # Let's assume the dash is at the same indentation level as the "options" key or +2 spaces.
                # Actually, standard YAML:
                # key:
                # - item
                # OR
                # key:
                #   - item
                
                # In the file view:
                # 7:   options:
                # 8:   - ...
                # So they are aligned.
                
                # Check for end of options block
                # End is reached if we see a line with same indentation as "options:" but NOT starting with "- "
                # OR dedented line.
                
                # Regex for option start: ^(indent)- 
                match_opt_start = re.match(f'^{indent}- (.*)', opt_line)
                
                if match_opt_start:
                    if current_opt_lines:
                        opts.append(current_opt_lines)
                    current_opt_lines = [opt_line]
                elif re.match(f'^{indent}\s+', opt_line):
                    # Continuation line (more indented)
                    if current_opt_lines:
                        current_opt_lines.append(opt_line)
                    else:
                        # Should not happen if valid yaml, but maybe comments?
                        # If it's a comment line inside options?
                        pass
                else:
                    # End of options block
                    if current_opt_lines:
                        opts.append(current_opt_lines)
                    break
                
                i += 1
            
            # Now we have the options in `opts`.
            # We expect `correct_index:` to follow or be somewhere.
            # But wait, we need to find `correct_index` to know which one is correct.
            # It might be the line we just stopped at, or further down.
            # Usually it is the next line.
            
            # Let's look for correct_index in the subsequent lines until the next question starts or block ends.
            # A new block starts with "- ".
            
            # We need to buffer the lines after options until we find correct_index.
            post_options_lines = []
            correct_index_found = False
            correct_idx_val = -1
            
            # We are currently at line `i` (which triggered the break).
            # We need to scan forward to find correct_index, BUT we must be careful not to go into the next question.
            # The next question starts with a line starting with "- " at the parent level (indentation of "options" - 2 usually).
            
            # Let's assume "correct_index:" is at the same indentation level as "options:".
            
            j = i
            while j < len(lines):
                curr = lines[j]
                match_correct = re.match(f'^{indent}correct_index:\s*(\d+)', curr)
                if match_correct:
                    correct_idx_val = int(match_correct.group(1))
                    correct_index_found = True
                    # We found it.
                    break
                
                # If we see a new top-level item or dedent, we abort (shouldn't happen in valid quiz file)
                # If indentation is less than `indent`, we stop.
                if len(curr) - len(curr.lstrip()) < len(indent) and curr.strip() != "":
                     break
                
                # If we see another "- " at the parent level (question level), stop.
                # Question level indent is likely `indent` minus 2.
                # But `options` is usually indented.
                
                j += 1
            
            if correct_index_found and opts:
                # Logic to shuffle
                # 1. Get correct option content
                if 0 <= correct_idx_val < len(opts):
                    correct_opt_lines = opts[correct_idx_val]
                    
                    # 2. Shuffle indices
                    indices = list(range(len(opts)))
                    random.shuffle(indices)
                    
                    # 3. Build new options list
                    new_opts = [opts[k] for k in indices]
                    
                    # 4. Find new correct index
                    # The correct option was at `correct_idx_val`.
                    # Now it is at `new_index` such that `indices[new_index] == correct_idx_val`.
                    new_correct_idx = indices.index(correct_idx_val)
                    
                    # 5. Append shuffled options to new_lines
                    for opt in new_opts:
                        new_lines.extend(opt)
                    
                    # 6. Append lines between options and correct_index (if any)
                    # usually none, but maybe comments.
                    # `lines[i:j]` are the lines between end of options and correct_index line.
                    new_lines.extend(lines[i:j])
                    
                    # 7. Append updated correct_index line
                    # Preserve indentation
                    new_lines.append(f"{indent}correct_index: {new_correct_idx}")
                    
                    # 8. Advance main loop index `i` to `j + 1`
                    i = j + 1
                    continue
                else:
                    print(f"Warning: Invalid correct_index {correct_idx_val} for options length {len(opts)} in {filepath}")
                    # Just append the original options and continue
                    for opt in opts:
                        new_lines.extend(opt)
            else:
                # Could not find correct_index or no options, just append what we read
                for opt in opts:
                    new_lines.extend(opt)
                # We are at line `i` which is the line after options.
                # Continue loop from `i`
                continue

        else:
            new_lines.append(line)
            i += 1

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

# Main execution
base_dir = r"c:\Users\charl\Documents\ai-cert\subjects"
target_dirs = ["m1", "m2", "m3", "m4"]

for d in target_dirs:
    pattern = os.path.join(base_dir, d, "chapter*.yaml")
    files = glob.glob(pattern)
    for f in files:
        process_file(f)

print("Done shuffling options.")
