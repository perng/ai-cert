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
from collections import defaultdict

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
  .options {{ list-style: none; padding: 0; }}
  .options li {{
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.35rem;
    border-radius: 6px;
    border: 1px solid var(--border);
    font-size: 0.92rem;
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
  }}
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


def build_html(questions: list[dict], module_dir: str) -> str:
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

                parts.append('<div class="question-card">')
                parts.append('<div class="q-header">')
                parts.append(f'<div class="q-text">{escape(text)}</div>')
                parts.append(f'<span class="q-id">#{qid}</span>')
                parts.append("</div>")

                parts.append('<ol class="options">')
                for i, opt in enumerate(options):
                    cls = ' class="correct"' if i == correct else ""
                    label = labels[i] if i < len(labels) else str(i)
                    parts.append(
                        f"<li{cls} data-label=\"{label}.\">{escape(opt)}</li>"
                    )
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
    html = build_html(questions, module_dir)

    output_path = args.output or os.path.join(module_dir, "quiz_review.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Generated {output_path} ({len(questions)} questions)")


if __name__ == "__main__":
    main()
