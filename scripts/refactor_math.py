
import os
import re
import argparse
from pathlib import Path

# Mapping of LaTeX symbols to Unicode/HTML
SYMBOL_MAP = {
    # Greek
    r'\alpha': 'α',
    r'\beta': 'β',
    r'\gamma': 'γ',
    r'\delta': 'δ',
    r'\epsilon': 'ε',
    r'\varepsilon': 'ε',
    r'\zeta': 'ζ',
    r'\eta': 'η',
    r'\theta': 'θ',
    r'\vartheta': 'θ',
    r'\iota': 'ι',
    r'\kappa': 'κ',
    r'\lambda': 'λ',
    r'\mu': 'μ',
    r'\nu': 'ν',
    r'\xi': 'ξ',
    r'\pi': 'π',
    r'\rho': 'ρ',
    r'\sigma': 'σ',
    r'\tau': 'τ',
    r'\upsilon': 'υ',
    r'\phi': 'φ',
    r'\varphi': 'φ',
    r'\chi': 'χ',
    r'\psi': 'ψ',
    r'\omega': 'ω',
    
    # Capital Greek
    r'\Gamma': 'Γ',
    r'\Delta': 'Δ',
    r'\Theta': 'Θ',
    r'\Lambda': 'Λ',
    r'\Xi': 'Ξ',
    r'\Pi': 'Π',
    r'\Sigma': 'Σ',
    r'\Upsilon': 'Υ',
    r'\Phi': 'Φ',
    r'\Psi': 'Ψ',
    r'\Omega': 'Ω',

    # Math Symbols
    r'\approx': '≈',
    r'\le': '≤',
    r'\ge': '≥',
    r'\neq': '≠',
    r'\times': '×',
    r'\cdot': '·',
    r'\rightarrow': '→',
    r'\leftrightarrow': '↔',
    r'\leftarrow': '←',
    r'\dots': '...',
    r'\infty': '∞',
    r'\nabla': '∇',
    r'\partial': '∂',
    r'\in': '∈',
    r'\notin': '∉',
    r'\subset': '⊂',
    r'\cup': '∪',
    r'\cap': '∩',
    r'\forall': '∀',
    r'\exists': '∃',
    r'\neg': '¬',
    r'\lor': '∨',
    r'\land': '∧',
    r'\pm': '±',
}

def latex_to_html(match):
    original = match.group(0)
    content = match.group(1).strip()
    
    # Check for unsupported complex LaTeX features
    # If it contains complex commands like \sum, \int, \frac, \mathbb (unless we map it), \mathcal
    # we might want to skip it to ensure we don't produce garbage.
    # We will try to process it, and if we fail to map something meaningful, we might default or be careful.
    
    # Heuristics for skipping complex blocks
    if '\\sum' in content or '\\int' in content or '\\frac' in content or '\\left' in content:
         return original
    
    current = content
    
    # 1. Replace fixed symbols
    for tex, char in SYMBOL_MAP.items():
        # Use word boundary or lookahead to avoid replacing \phi in \phi_0 incorrectly if we had longer matches?
        # Re.sub is better. Escape regex special chars in tex
        pattern = re.escape(tex) + r'(?![a-zA-Z])' 
        current = re.sub(pattern, char, current)
    
    # 2. Handle simple \sqrt{...}
    # This handles simple nested braces case? Regex is bad at nesting.
    # We assume simple \sqrt{...} without nested braces for now.
    current = re.sub(r'\\sqrt\{([^{}]+)\}', r'√\1', current)
    current = re.sub(r'\\sqrt\s+([a-zA-Z0-9])', r'√\1', current) # \sqrt x
    
    # 3. Handle Superscripts and Subscripts
    # We need to handle them carefully. standard markdown/html.
    # pattern: ^... or ^{...}
    
    # Handle ^{...}
    def sup_repl(m):
        return f"<sup>{m.group(1)}</sup>"
    current = re.sub(r'\^\{([^{}]+)\}', sup_repl, current)
    
    # Handle _{...}
    def sub_repl(m):
        return f"<sub>{m.group(1)}</sub>"
    current = re.sub(r'_\{([^{}]+)\}', sub_repl, current)
    
    # Handle single char ^x or _x
    current = re.sub(r'\^([a-zA-Z0-9\+\-\(\)])', r'<sup>\1</sup>', current)
    current = re.sub(r'_([a-zA-Z0-9\+\-\(\)])', r'<sub>\1</sub>', current)
    
    # 4. Remove remaining braces likely from {x}
    current = current.replace('{', '').replace('}', '')
    
    # 5. Handling \text{...} or \mathrm{...}
    # Just remove the command
    current = re.sub(r'\\text\s*', '', current)
    current = re.sub(r'\\mathrm\s*', '', current)
    
    # If after replacements we still have backslashes, it means we failed to handle some latex command.
    # In that case, we should revert to original to avoid showing broken latex like "\unknown char".
    if '\\' in current:
        return original
        
    return current

def process_file(file_path, dry_run=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find inline math $...$
    # We must be careful not to match $$...$$
    # Pattern: (?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)
    # Explanation:
    # (?<!\$)  : Not preceded by $
    # \$       : Match $
    # (?!\$)   : Not followed by $ (excludes $$)
    # (.*?)    : Non-greedy match content
    # (?<!\$)  : Content not ending with $ (to handle empty $$, but we want simple $) 
    #            Wait, simple inline is just $...$.
    #            Standard regex: (?<!\$)\$(?:\\.|[^$])+\$(?!\$) is better to verify escaped $
    
    # Simplified pattern for what likely exists in these files
    pattern = r'(?<!\$)\$(?!\$)([^\n$]+)(?<!\$)\$(?!\$)'
    
    def replacement_func(match):
        return latex_to_html(match)
    
    new_content = re.sub(pattern, replacement_func, content)
    
    if new_content != content:
        print(f"Modifying {file_path}")
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("subjects_dir", help="Directory containing standard markdown/quarto files")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes")
    args = parser.parse_args()
    
    base_dir = Path(args.subjects_dir)
    extensions = ['*.md', '*.qmd']
    
    files = []
    for ext in extensions:
        files.extend(list(base_dir.rglob(ext)))
        
    count = 0
    for file_path in files:
        if file_path.name.startswith("index"): # Skipping index files? user said every chapter.
            # Usually index files are chapters too in quarto context. Let's process them.
            pass
            
        if process_file(file_path, args.dry_run):
            count += 1
            
    print(f"Processed {len(files)} files. Modified {count} files.")

if __name__ == "__main__":
    main()
