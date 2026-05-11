import os
import json
import yaml
import argparse
import subprocess
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Defaults
DEFAULT_SUBJECTS_DIR = "subjects"
DEFAULT_OUTPUT_FILE = "assets/content.json"
CONTENT_SCHEMA_VERSION = 3
REMOTE_IMAGE_PREFIXES = ('http://', 'https://', 'data:')
ASSET_IMAGE_PREFIX = "assets/images/"

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def is_remote_image(src):
    return src.startswith(REMOTE_IMAGE_PREFIXES)

def block_context(yaml_path, question_id):
    return f"{yaml_path} question {question_id}"

def safe_filename_part(value):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', str(value)).strip('_') or "unknown"

def resolve_question_image(src, yaml_path, image_output_dir, question_id):
    """
    Copy rich question images into the app image asset directory and return the
    Flutter asset path. Existing asset paths and remote/data images pass through.
    """
    if not src:
        raise ValueError(f"{block_context(yaml_path, question_id)} image block missing src")

    if is_remote_image(src) or src.startswith(ASSET_IMAGE_PREFIX):
        return src

    source_path = (yaml_path.parent / src).resolve()
    if not source_path.exists():
        raise FileNotFoundError(
            f"{block_context(yaml_path, question_id)} image not found: {source_path}"
        )

    image_out_path = Path(image_output_dir)
    image_out_path.mkdir(parents=True, exist_ok=True)

    subject_name = yaml_path.parent.name
    chapter_name = yaml_path.stem
    unique_filename = (
        f"{safe_filename_part(subject_name)}_"
        f"{safe_filename_part(chapter_name)}_"
        f"{safe_filename_part(question_id)}_"
        f"{safe_filename_part(source_path.name)}"
    )
    dest_path = image_out_path / unique_filename
    shutil.copy2(source_path, dest_path)
    return f"{ASSET_IMAGE_PREFIX}{unique_filename}"

def normalize_blocks(blocks, yaml_path, image_output_dir, question_id):
    """
    Normalize YAML rich content blocks into JSON-safe block dictionaries.
    Supported types are text, code, and image.
    """
    if blocks is None:
        return []

    if not isinstance(blocks, list):
        raise TypeError(f"{block_context(yaml_path, question_id)} content must be a list")

    normalized = []
    for index, block in enumerate(blocks):
        if isinstance(block, str):
            normalized.append({"type": "text", "text": block})
            continue

        if not isinstance(block, dict):
            raise TypeError(
                f"{block_context(yaml_path, question_id)} content block {index} must be a mapping"
            )

        block_type = block.get("type")
        if block_type == "text":
            text = block.get("text")
            if text is None:
                raise ValueError(
                    f"{block_context(yaml_path, question_id)} text block {index} missing text"
                )
            normalized.append({"type": "text", "text": str(text)})
        elif block_type == "code":
            code = block.get("code")
            if code is None:
                raise ValueError(
                    f"{block_context(yaml_path, question_id)} code block {index} missing code"
                )
            normalized_block = {"type": "code", "code": str(code)}
            language = block.get("language")
            if language:
                normalized_block["language"] = str(language)
            normalized.append(normalized_block)
        elif block_type == "image":
            src = resolve_question_image(
                str(block.get("src", "")), yaml_path, image_output_dir, question_id
            )
            alt = block.get("alt")
            if not alt:
                raise ValueError(
                    f"{block_context(yaml_path, question_id)} image block {index} missing alt"
                )
            normalized_block = {"type": "image", "src": src, "alt": str(alt)}
            caption = block.get("caption")
            if caption:
                normalized_block["caption"] = str(caption)
            normalized.append(normalized_block)
        else:
            raise ValueError(
                f"{block_context(yaml_path, question_id)} unsupported content block type: {block_type}"
            )

    return normalized

def blocks_to_markdown(blocks):
    parts = []
    for block in blocks:
        block_type = block.get("type")
        if block_type == "text":
            parts.append(block.get("text", ""))
        elif block_type == "code":
            language = block.get("language", "")
            code = block.get("code", "")
            parts.append(f"```{language}\n{code.rstrip()}\n```")
        elif block_type == "image":
            alt = block.get("alt", "")
            src = block.get("src", "")
            image_markdown = f"![{alt}]({src})"
            caption = block.get("caption")
            if caption:
                image_markdown = f"{image_markdown}\n\n{caption}"
            parts.append(image_markdown)
    return "\n\n".join(part for part in parts if part).strip()

def scalar_to_text_block(value):
    return [{"type": "text", "text": "" if value is None else str(value)}]

def normalize_option(option, yaml_path, image_output_dir, question_id):
    if isinstance(option, dict):
        option_blocks = normalize_blocks(
            option.get("content"), yaml_path, image_output_dir, question_id
        )
        fallback = option.get("text")
        if not option_blocks:
            option_blocks = scalar_to_text_block(fallback)
        if fallback is None:
            fallback = blocks_to_markdown(option_blocks)
        return str(fallback), option_blocks

    option_blocks = scalar_to_text_block(option)
    return str(option), option_blocks

def normalize_question(question, yaml_path, image_output_dir):
    q = dict(question)
    question_id = q.get("id", "unknown")

    raw_content = q.pop("content", None)
    if "text" in q:
        raw_text = q.pop("text")
        q.pop("textContent", None)
    else:
        raw_text = q.pop("textContent", None)
    content_blocks = normalize_blocks(raw_content, yaml_path, image_output_dir, question_id)
    if not content_blocks:
        content_blocks = scalar_to_text_block(raw_text)

    q["textContent"] = blocks_to_markdown(content_blocks)
    q["content"] = content_blocks

    options = q.get("options", [])
    if not isinstance(options, list):
        raise TypeError(f"{block_context(yaml_path, question_id)} options must be a list")

    fallback_options = []
    option_content = []
    for option in options:
        option_text, option_blocks = normalize_option(
            option, yaml_path, image_output_dir, question_id
        )
        fallback_options.append(option_text)
        option_content.append(option_blocks)

    q["options"] = fallback_options
    q["optionContent"] = option_content

    if "correct_index" in q:
        q["correctIndex"] = q.pop("correct_index")
    if "correctIndex" in q:
        correct_index = int(q["correctIndex"])
        if correct_index < 0 or correct_index >= len(fallback_options):
            raise ValueError(
                f"{block_context(yaml_path, question_id)} correctIndex {correct_index} "
                f"outside options length {len(fallback_options)}"
            )
        q["correctIndex"] = correct_index

    explanation_content = q.pop("explanationContent", None)
    if explanation_content is not None:
        explanation_blocks = normalize_blocks(
            explanation_content, yaml_path, image_output_dir, question_id
        )
        q["explanationContent"] = explanation_blocks
        if not q.get("explanation"):
            q["explanation"] = blocks_to_markdown(explanation_blocks)

    return q

def parse_frontmatter(file_path):
    """
    Simple frontmatter parser to avoid extra dependencies if possible,
    or use python-frontmatter if available.
    Here we implement a simple one since we already need to read the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip leading whitespace/newlines so we can detect ---
    content = content.lstrip()
    
    if content.startswith('---'):
        try:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                return frontmatter
        except Exception as e:
            print(f"Error parsing frontmatter for {file_path}: {e}")
    return {}

def render_quarto(file_path):
    """
    Renders a single .md file to HTML fragment using Quarto.
    Returns the path to the generated HTML file.
    """
    # We render to a temporary file or just let quarto render alongside
    # quarto render <file> --to html --no-full-html --output <temp_name>
    # Note: --output changes the filename, but quarto might still put it in the same dir.
    
    # Resolve to absolute path to avoid issues with relative paths (e.g. ..)
    file_path = file_path.resolve()
    output_filename = file_path.stem + ".html"
    output_path = file_path.parent / output_filename
    
    # Check for _quarto.yml in the same directory to find custom output-dir
    quarto_config_path = file_path.parent / "_quarto.yml"
    custom_output_dir = None
    if quarto_config_path.exists():
        try:
            config = load_yaml(quarto_config_path)
            project_config = config.get('project', {})
            output_dir_str = project_config.get('output-dir')
            if output_dir_str:
                # Resolve relative to the config file location
                custom_output_dir = (file_path.parent / output_dir_str).resolve()
        except Exception as e:
            print(f"Warning: Failed to parse _quarto.yml: {e}")

    # Check if quarto is installed
    if shutil.which("quarto") is None:
        raise RuntimeError("Quarto CLI is not found in PATH.")

    cmd = [
        "quarto", "render", str(file_path),
        "--to", "html",
        "-M", "mermaid-format:png",
        "-M", "html-math-method:plain"
        # Removed --embed-resources to allow image copying (src will be paths, not base64)
    ]
    
    print(f"Rendering {file_path}...")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        print(f"Error rendering {file_path}:")
        print(result.stderr)
        raise RuntimeError("Quarto render failed")
        
    # Check for output in _book (Quarto project default) or same dir
    possible_paths = [
        file_path.parent / "_book" / output_filename,
        file_path.parent / output_filename
    ]
    
    if custom_output_dir:
        possible_paths.insert(0, custom_output_dir / output_filename)
    
    for p in possible_paths:
        if p.exists():
            return p
            
    raise FileNotFoundError(f"Could not find generated HTML for {file_path}. Checked: {[str(p) for p in possible_paths]}")

def process_chapter(md_file, questions_map, image_output_dir=None, 
                    current_chapter_id=0, current_section_id=0):
    """
    Process a single chapter: render, parse HTML, split sections, attach questions.
    """
    frontmatter = parse_frontmatter(md_file)
    chapter_title = frontmatter.get('title', md_file.stem)
    section_order = 1
    
    # Priority: id -> global counter
    # Do NOT use order as ID, as it is not globally unique
    chapter_id = frontmatter.get('id')
        
    if chapter_id is None:
        # If no explicit ID, use the global counter
        chapter_id = current_chapter_id
        current_chapter_id += 1
    
    # Render
    html_path = render_quarto(md_file)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Remove warning lines containing python filenames and line numbers
    # which can leak host information. e.g. "base_conv.py:113"
    html_content = re.sub(r'(?m)^.*\.py:\d+.*$\n?', '', html_content)

        
    # Clean up the generated HTML file
    # os.remove(html_path) # Uncomment to clean up
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # If full HTML, extract body content
    if soup.body:
        # Create a new soup with just the body content to avoid processing head/scripts
        # But we need to keep the soup structure for find_all to work correctly on the subset
        # So we just narrow our focus or replace soup
        soup = BeautifulSoup(str(soup.body), 'html.parser')
    
    # Process Images
    if image_output_dir:
        image_out_path = Path(image_output_dir)
        image_out_path.mkdir(parents=True, exist_ok=True)
        
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and not src.startswith(('http', 'https', 'data:')):
                # Resolve source path (relative to the generated HTML file)
                # Quarto places generated images relative to the output HTML.
                img_source_path = (html_path.parent / src).resolve()
                
                # Fallback: Check relative to source markdown if not found in output
                if not img_source_path.exists():
                    img_source_path_md = (md_file.parent / src).resolve()
                    if img_source_path_md.exists():
                        img_source_path = img_source_path_md
                        
                if img_source_path.exists():
                    # Destination: flat structure in assets/images/
                    # To avoid collisions, we use subject and chapter as prefix.
                    subject_name = md_file.parent.name
                    chapter_name = md_file.stem
                    unique_filename = f"{subject_name}_{chapter_name}_{img_source_path.name}"
                    
                    dest_path = image_out_path / unique_filename
                    
                    try:
                        shutil.copy2(img_source_path, dest_path)
                        # Update src to be relative to Flutter assets root
                        # Assuming the app loads from 'assets/images/'
                        img['src'] = f"assets/images/{unique_filename}"
                    except Exception as e:
                        print(f"Warning: Failed to copy image {img_source_path}: {e}")
                else:
                    print(f"Warning: Image not found: {img_source_path}")

    sections = []
    
    # 1. Identify Intro Content (before first section)
    # Quarto usually wraps sections in <section class="level2"> if using ## headers
    # Or just flat content if no headers.
    
    # Strategy: Find all level2 sections
    level2_sections = soup.find_all('section', class_='level2')
    
    # If no sections found, treat whole body as one section or intro
    if not level2_sections:
        # Check if there is content
        body_content = str(soup)
        sections.append({
            "id": current_section_id,
            "order": section_order,
            "title": "Introduction",
            "content": body_content,
            "questions": [] # We'll attach questions later
        })
        current_section_id += 1
        section_order += 1
    else:
        # Handle Intro (content before first section)
        # This is tricky with BS4 flat parsing, but if Quarto wraps everything in sections, 
        # the intro might be in a section class="level1" or just loose elements.
        # Often Quarto puts the title in a header, we might want to skip that if we use app navigation.
        
        # Let's iterate and build
        for sec in level2_sections:
            sec_title_tag = sec.find(['h2'])
            sec_title = sec_title_tag.get_text() if sec_title_tag else "Untitled Section"
            sec_id = sec.get('id', '')
            
            # Get content of the section
            # We might want to remove the h2 tag from the content if the app displays the title separately
            if sec_title_tag:
                sec_title_tag.decompose() 
            
            sec_content = str(sec)
            
            # Find questions for this section
            # We filter by section_title matching (fuzzy) or tag matching
            
            # 1. Get all header texts in this section for title matching
            headers = sec.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])
            candidate_titles = [h.get_text() for h in headers]
            if sec_title not in candidate_titles:
                candidate_titles.append(sec_title)
                
            sec_questions = []
            for q in questions_map:
                is_match = False
                q_title = q.get('section_title', '').strip()
                q_tags = q.get('tags', [])
                
                # A. Tag Matching
                if sec_id and sec_id in q_tags:
                    is_match = True
                
                # B. Title Matching
                if not is_match and q_title:
                    for cand in candidate_titles:
                        # Clean candidate: remove numbering "1.1 " and parens "(English)"
                        # 1. Remove numbering
                        cand_clean = re.sub(r'^\d+(\.\d+)*\s+', '', cand)
                        # 2. Remove parens content
                        cand_clean = re.sub(r'\s*\([^)]*\)', '', cand_clean).strip()
                        
                        # Check exact match of cleaned title
                        if q_title == cand_clean:
                            is_match = True
                            break
                        
                        # Check if q_title is in cand (fallback)
                        if q_title in cand:
                            is_match = True
                            break
                            
                        # Special case for "A vs B" where parens might break simple substring
                        cand_no_parens = re.sub(r'\([^)]*\)', '', cand)
                        if q_title.replace(" ", "") == cand_no_parens.replace(" ", ""):
                            is_match = True
                            break
                
                if is_match:
                    sec_questions.append(q)
            
            sections.append({
                "id": current_section_id,
                "order": section_order,
                "title": sec_title,
                "link_id": sec_id,
                "content": sec_content,
                "questions": sec_questions
            })
            current_section_id += 1
            section_order += 1
            
    return {
        "id": chapter_id,
        "order": frontmatter.get('order', chapter_id),
        "title": chapter_title,
        "sections": sections
    }, current_chapter_id, current_section_id

def main():
    parser = argparse.ArgumentParser(description="Build content.json from Quarto source.")
    parser.add_argument("--subjects_dir", default=DEFAULT_SUBJECTS_DIR, help="Path to subjects directory")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_FILE, help="Path to output json file")
    parser.add_argument("--image_output_dir", default="assets/images", help="Path to copy images to")
    args = parser.parse_args()
    
    subjects_dir = Path(args.subjects_dir)
    output_file = Path(args.output)
    image_output_dir = Path(args.image_output_dir)
    
    if not subjects_dir.exists():
        print(f"Error: Subjects directory '{subjects_dir}' does not exist.")
        return

    final_json = {
        "version": CONTENT_SCHEMA_VERSION,
        "subjects": []
    }
    
    # Global counters to ensure uniqueness if IDs are missing
    # Start high to avoid conflicts with manual IDs if any
    global_subject_id = 1
    global_chapter_id = 1000 
    global_section_id = 10000
    
    # Iterate Subjects
    # We assume directories starting with a number or just all directories containing subject.yaml
    subject_dirs = sorted([d for d in subjects_dir.iterdir() if d.is_dir()])
    
    for sub_dir in subject_dirs:

        subject_yaml_path = sub_dir / "subject.yaml"
        if not subject_yaml_path.exists():
            continue
            
        print(f"Processing Subject: {sub_dir.name}")
        subject_meta = load_yaml(subject_yaml_path)
        
        s_id = subject_meta.get('id')
        if s_id is None:
            s_id = global_subject_id
            global_subject_id += 1

        subject_obj = {
            "id": s_id,
            "order": subject_meta.get('order', s_id),
            "isLocked": subject_meta.get('is_locked', False),
            "title": subject_meta.get('title'),
            "description": subject_meta.get('description'),
            "chapters": []
        }
        
        # Process Chapters
        # Find .md and .qmd files
        md_files = sorted(list(sub_dir.glob("*.md")) + list(sub_dir.glob("*.qmd")))
        print(f"    Found {len(md_files)} files in {sub_dir.name}: {[f.name for f in md_files]}")
        
        for md_file in md_files:
            if md_file.name == "index.md" or md_file.name == "index.qmd":
                continue
            print(f"  Processing Chapter: {md_file.name}")
            
            # Load corresponding questions yaml
            # e.g. 01_intro.md -> 01_intro.yaml
            yaml_name = md_file.stem + ".yaml"
            yaml_path = sub_dir / yaml_name
            questions = []
            if yaml_path.exists():
                print(f"    Found questions file: {yaml_name}")
                q_data = load_yaml(yaml_path)
                questions = q_data.get('questions', [])
                questions = [
                    normalize_question(q, yaml_path, image_output_dir)
                    for q in questions
                ]
                print(f"    Loaded {len(questions)} questions")
            else:
                print(f"    No questions file found (looked for {yaml_name})")
            
            # Pass counters
            try:
                chapter_obj, global_chapter_id, global_section_id = process_chapter(
                    md_file, questions, image_output_dir, 
                    global_chapter_id, global_section_id
                )
                subject_obj['chapters'].append(chapter_obj)
            except Exception as e:
                print(f"    Error processing chapter {md_file.name}: {e}")
                continue
            
        final_json['subjects'].append(subject_obj)
        
    # Output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    main()
