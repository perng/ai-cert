#!/usr/bin/env python3
"""
Convert YAML quiz files in a module directory to a reviewable HTML page.

Usage:
    python yaml_to_html.py subjects/m5
    python yaml_to_html.py subjects/m5 -o review.html
"""

import argparse
import glob
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import Optional

import yaml


def load_questions(module_dir: str) -> list[dict]:
    """Load all questions from chapter*.yaml files in the given directory."""
    pattern = os.path.join(module_dir, "chapter*.yaml")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"Error: No chapter*.yaml files found in {module_dir}", file=sys.stderr)
        sys.exit(1)

    all_questions = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
            if data and "questions" in data:
                for q in data["questions"]:
                    q["_source_file"] = os.path.basename(f)
                    q["_source_path"] = f
                all_questions.extend(data["questions"])
    return all_questions


def group_questions(questions: list[dict]) -> dict:
    """Group questions by chapter_title then section_title."""
    grouped = defaultdict(lambda: defaultdict(list))
    for q in questions:
        chapter = q.get("chapter_title", "未分類")
        section = q.get("section_title", "未分類")
        grouped[chapter][section].append(q)
    return grouped


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 題庫審閱</title>
<style>
  :root {{
    --bg: #f8f9fa;
    --card-bg: #ffffff;
    --correct: #d4edda;
    --correct-border: #28a745;
    --wrong: #ffffff;
    --accent: #2563eb;
    --text: #1a1a2e;
    --muted: #6c757d;
    --border: #dee2e6;
    --section-bg: #e9ecef;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 2rem 1rem;
  }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  h1 {{
    font-size: 1.8rem;
    margin-bottom: 0.25rem;
    color: var(--accent);
  }}
  .subtitle {{
    color: var(--muted);
    font-size: 0.95rem;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--border);
  }}
  .stats {{
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
  }}
  .stat-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }}
  .stat-card strong {{ color: var(--accent); font-size: 1.3rem; }}
  .toc {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 2rem;
  }}
  .toc h2 {{ font-size: 1.1rem; margin-bottom: 0.75rem; }}
  .toc ul {{ list-style: none; padding-left: 0; }}
  .toc li {{ margin-bottom: 0.3rem; }}
  .toc a {{
    color: var(--accent);
    text-decoration: none;
    font-size: 0.9rem;
  }}
  .toc a:hover {{ text-decoration: underline; }}
  .toc .toc-section {{ padding-left: 1.25rem; color: var(--muted); font-size: 0.85rem; }}

  .chapter-heading {{
    font-size: 1.4rem;
    margin-top: 2.5rem;
    margin-bottom: 0.25rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accent);
    color: var(--accent);
  }}
  .section-heading {{
    font-size: 1.1rem;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    padding: 0.5rem 0.75rem;
    background: var(--section-bg);
    border-radius: 6px;
    color: var(--text);
  }}

  .question-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.15s;
  }}
  .question-card:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
  .q-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.6rem;
  }}
  .q-id {{
    font-size: 0.8rem;
    color: var(--muted);
    font-family: monospace;
    background: var(--bg);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
  }}
  .q-text {{
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
  }}
  .q-content {{
    margin-bottom: 0.85rem;
  }}
  .content-block {{
    margin-bottom: 0.75rem;
  }}
  .content-block:last-child {{ margin-bottom: 0; }}
  .content-text {{
    white-space: pre-wrap;
  }}
  .content-code {{
    background: #0f172a;
    color: #e2e8f0;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    overflow-x: auto;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
    font-size: 0.86rem;
    line-height: 1.5;
    border: 1px solid #1e293b;
  }}
  .code-language {{
    display: inline-block;
    margin-bottom: 0.25rem;
    color: var(--muted);
    font-size: 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  }}
  .content-image {{
    margin: 0.75rem 0;
  }}
  .content-image img {{
    display: block;
    max-width: 100%;
    height: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: #fff;
  }}
  .content-image figcaption {{
    margin-top: 0.35rem;
    color: var(--muted);
    font-size: 0.82rem;
  }}
  .missing-image {{
    color: #842029;
    background: #f8d7da;
    border: 1px solid #f5c2c7;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }}
  .options {{ list-style: none; padding: 0; }}
  .options li {{
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.35rem;
    border-radius: 6px;
    border: 1px solid var(--border);
    font-size: 0.92rem;
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
  }}
  .option-body {{ flex: 1; min-width: 0; }}
  .option-body .content-code {{ margin-top: 0.25rem; }}
  .options li.correct {{
    background: var(--correct);
    border-color: var(--correct-border);
    font-weight: 600;
  }}
  .options li.correct::before {{ content: "✅"; }}
  .options li:not(.correct)::before {{
    content: attr(data-label);
    color: var(--muted);
    font-weight: 600;
    min-width: 1.5em;
  }}
  .explanation {{
    margin-top: 0.6rem;
    padding: 0.6rem 0.75rem;
    font-size: 0.88rem;
    color: #155724;
    background: #f0fff4;
    border-left: 3px solid var(--correct-border);
    border-radius: 0 6px 6px 0;
  }}
  .tags {{
    margin-top: 0.5rem;
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }}
  .tag {{
    font-size: 0.75rem;
    background: var(--bg);
    color: var(--muted);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    border: 1px solid var(--border);
  }}

  /* Correct-answer index distribution warning */
  .warning {{
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
  }}
  .warning strong {{ color: #856404; }}

  @media print {{
    body {{ padding: 0.5rem; }}
    .question-card {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="container">
{content}
</div>
</body>
</html>
"""


def escape(text: str) -> str:
    """Escape HTML special characters."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


REMOTE_IMAGE_PREFIXES = ("http://", "https://", "data:")


def normalize_blocks(blocks, fallback_text=None) -> list[dict]:
    """Normalize rich content blocks while keeping legacy scalar text valid."""
    if blocks is None:
        return [{"type": "text", "text": "" if fallback_text is None else str(fallback_text)}]

    if isinstance(blocks, str):
        return [{"type": "text", "text": blocks}]

    if not isinstance(blocks, list):
        return [{"type": "text", "text": str(blocks)}]

    normalized = []
    for block in blocks:
        if isinstance(block, str):
            normalized.append({"type": "text", "text": block})
            continue
        if not isinstance(block, dict):
            normalized.append({"type": "text", "text": str(block)})
            continue

        block_type = block.get("type", "text")
        if block_type == "text":
            normalized.append({"type": "text", "text": "" if block.get("text") is None else str(block.get("text"))})
        elif block_type == "code":
            item = {"type": "code", "code": "" if block.get("code") is None else str(block.get("code"))}
            if block.get("language"):
                item["language"] = str(block.get("language"))
            normalized.append(item)
        elif block_type == "image":
            item = {
                "type": "image",
                "src": "" if block.get("src") is None else str(block.get("src")),
                "alt": "" if block.get("alt") is None else str(block.get("alt")),
            }
            if block.get("caption"):
                item["caption"] = str(block.get("caption"))
            normalized.append(item)
        else:
            normalized.append({"type": "text", "text": f"[Unsupported content block: {block_type}]"})
    return normalized


def normalize_option(option) -> tuple[str, list[dict]]:
    """Return fallback text plus rich blocks for a scalar or rich option object."""
    if isinstance(option, dict):
        fallback = option.get("text")
        blocks = normalize_blocks(option.get("content"), fallback)
        if fallback is None:
            fallback = blocks_to_plain_text(blocks)
        return str(fallback), blocks
    return str(option), normalize_blocks(None, option)


def blocks_to_plain_text(blocks: list[dict]) -> str:
    parts = []
    for block in blocks:
        block_type = block.get("type")
        if block_type == "text":
            parts.append(block.get("text", ""))
        elif block_type == "code":
            language = block.get("language", "")
            parts.append(f"```{language}\n{block.get('code', '').rstrip()}\n```")
        elif block_type == "image":
            alt = block.get("alt", "")
            src = block.get("src", "")
            caption = block.get("caption")
            text = f"![{alt}]({src})"
            if caption:
                text += f"\n\n{caption}"
            parts.append(text)
    return "\n\n".join(part for part in parts if part).strip()


def resolve_image_src(src: str, yaml_path: str, output_dir: str) -> tuple[str, bool]:
    """Resolve local image src relative to the YAML file and return HTML-relative path."""
    if not src:
        return "", False
    if src.startswith(REMOTE_IMAGE_PREFIXES) or os.path.isabs(src):
        return src, os.path.exists(src) if os.path.isabs(src) else True

    yaml_dir = Path(yaml_path).resolve().parent
    output = Path(output_dir).resolve()
    asset_candidate = (Path.cwd() / src).resolve()
    if src.startswith("assets/") and asset_candidate.exists():
        return os.path.relpath(asset_candidate, output), True

    candidate = (yaml_dir / src).resolve()
    if candidate.exists():
        return os.path.relpath(candidate, output), True
    return src, False


def render_blocks(blocks: list[dict], yaml_path: str, output_dir: str) -> str:
    html = []
    for block in blocks:
        block_type = block.get("type")
        if block_type == "text":
            html.append(f'<div class="content-block content-text">{escape(block.get("text", ""))}</div>')
        elif block_type == "code":
            language = block.get("language", "")
            if language:
                html.append(f'<div class="code-language">{escape(language)}</div>')
            html.append(
                '<pre class="content-block content-code"><code>'
                f'{escape(block.get("code", ""))}'
                '</code></pre>'
            )
        elif block_type == "image":
            src, exists = resolve_image_src(block.get("src", ""), yaml_path, output_dir)
            alt = block.get("alt", "")
            caption = block.get("caption", "")
            if exists:
                figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
                html.append(
                    '<figure class="content-block content-image">'
                    f'<img src="{escape(src)}" alt="{escape(alt)}">'
                    f"{figcaption}</figure>"
                )
            else:
                html.append(
                    '<div class="content-block missing-image">'
                    f'Image not found: {escape(block.get("src", ""))}'
                    '</div>'
                )
        else:
            html.append(f'<div class="content-block content-text">{escape(blocks_to_plain_text([block]))}</div>')
    return "\n".join(html)


def build_html(questions: list[dict], module_dir: str, output_path: Optional[str] = None) -> str:
    """Build the full HTML content."""
    grouped = group_questions(questions)
    total = len(questions)
    chapter_count = len(grouped)
    files = sorted({q["_source_file"] for q in questions})

    # Analyse correct_index distribution
    index_counts = defaultdict(int)
    for q in questions:
        index_counts[q.get("correct_index", -1)] += 1

    parts = []
    output_dir = os.path.dirname(os.path.abspath(output_path)) if output_path else os.path.abspath(module_dir)

    # Header
    module_name = os.path.basename(os.path.normpath(module_dir))
    first_chapter = next(iter(grouped), module_name)
    parts.append(f'<h1>📋 {escape(first_chapter)} — 題庫審閱</h1>')
    parts.append(
        f'<div class="subtitle">模組：{escape(module_name)} ｜ 來源：{", ".join(files)}</div>'
    )

    # Stats
    parts.append('<div class="stats">')
    parts.append(f'<div class="stat-card">題目總數 <strong>{total}</strong></div>')
    parts.append(
        f'<div class="stat-card">章節數 <strong>{chapter_count}</strong></div>'
    )
    parts.append(
        f'<div class="stat-card">檔案數 <strong>{len(files)}</strong></div>'
    )
    parts.append("</div>")

    # Correct-index distribution warning
    if total > 0:
        dominant_idx = max(index_counts, key=index_counts.get)
        dominant_pct = index_counts[dominant_idx] / total * 100
        if dominant_pct > 60:
            labels = "ABCDEFGH"
            dist_str = " ｜ ".join(
                f"{labels[k]}：{v} 題 ({v/total*100:.0f}%)"
                for k, v in sorted(index_counts.items())
                if k >= 0
            )
            parts.append(
                f'<div class="warning"><strong>⚠️ 答案分佈不均：</strong>'
                f"正確答案集中在選項 {labels[dominant_idx]}（{dominant_pct:.0f}%）。"
                f"<br/>分佈：{dist_str}</div>"
            )

    # Table of contents
    parts.append('<div class="toc"><h2>目錄</h2><ul>')
    chap_idx = 0
    for chapter, sections in grouped.items():
        chap_idx += 1
        anchor = f"ch-{chap_idx}"
        sec_count = sum(len(qs) for qs in sections.values())
        parts.append(
            f'<li><a href="#{anchor}">{escape(chapter)}</a> ({sec_count} 題)</li>'
        )
        for section in sections:
            parts.append(f'<li class="toc-section">— {escape(section)}</li>')
    parts.append("</ul></div>")

    # Questions
    labels = "ABCDEFGH"
    chap_idx = 0
    for chapter, sections in grouped.items():
        chap_idx += 1
        anchor = f"ch-{chap_idx}"
        parts.append(f'<h2 class="chapter-heading" id="{anchor}">{escape(chapter)}</h2>')

        for section, qs in sections.items():
            parts.append(f'<h3 class="section-heading">{escape(section)}</h3>')

            for q in qs:
                qid = q.get("id", "?")
                text = q.get("text", "")
                options = q.get("options", [])
                correct = q.get("correct_index", -1)
                explanation = q.get("explanation", "")
                tags = q.get("tags", [])
                yaml_path = q.get("_source_path", module_dir)
                prompt_blocks = normalize_blocks(q.get("content"), text)
                normalized_options = [normalize_option(opt) for opt in options]

                parts.append('<div class="question-card">')
                parts.append('<div class="q-header">')
                if not q.get("content"):
                    parts.append(f'<div class="q-text">{escape(text)}</div>')
                else:
                    parts.append("<div></div>")
                parts.append(f'<span class="q-id">#{qid}</span>')
                parts.append("</div>")
                if q.get("content"):
                    parts.append('<div class="q-content">')
                    parts.append(render_blocks(prompt_blocks, yaml_path, output_dir))
                    parts.append("</div>")

                parts.append('<ol class="options">')
                for i, (fallback, option_blocks) in enumerate(normalized_options):
                    cls = ' class="correct"' if i == correct else ""
                    label = labels[i] if i < len(labels) else str(i)
                    if isinstance(options[i], dict):
                        option_html = render_blocks(option_blocks, yaml_path, output_dir)
                    else:
                        option_html = escape(fallback)
                    parts.append(f'<li{cls} data-label="{label}."><div class="option-body">{option_html}</div></li>')
                parts.append("</ol>")

                if explanation:
                    parts.append(
                        f'<div class="explanation">💡 {escape(explanation)}</div>'
                    )

                if tags:
                    parts.append('<div class="tags">')
                    for tag in tags:
                        parts.append(f'<span class="tag">{escape(tag)}</span>')
                    parts.append("</div>")

                parts.append("</div>")

    title = f"{first_chapter} — 題庫審閱"
    return HTML_TEMPLATE.format(title=escape(title), content="\n".join(parts))


def main():
    parser = argparse.ArgumentParser(
        description="Convert YAML quiz files to a reviewable HTML page."
    )
    parser.add_argument(
        "module_dir",
        help="Path to the module directory containing chapter*.yaml files (e.g. subjects/m5)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output HTML file path (default: <module_dir>/quiz_review.html)",
    )
    args = parser.parse_args()

    module_dir = args.module_dir.rstrip("/")
    if not os.path.isdir(module_dir):
        print(f"Error: {module_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    questions = load_questions(module_dir)
    output_path = args.output or os.path.join(module_dir, "quiz_review.html")
    html = build_html(questions, module_dir, output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Generated {output_path} ({len(questions)} questions)")


if __name__ == "__main__":
    main()
