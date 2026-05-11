# Rich Question Content Design

## Goal

Allow quiz questions in chapter YAML files, such as `backup-modules/m6/chapter1.yaml`, to include images and code snippets in either the question prompt or answer options. The generated content must still be usable by `scripts/build_content.py` and eventually consumed by the app in `~/ai-planner`.

## Current State

The current YAML shape is intentionally simple:

```yaml
questions:
  - id: 8001
    chapter_title: Basic Python Language
    section_title: Python 的定位與執行方式
    text: Python 被稱為動態型別語言，主要代表什麼意思？
    type: multiple_choice
    options:
      - Python 程式一定會自動使用 GPU 執行
      - 變數宣告時必須明確指定資料型別
      - 變數本身不固定型別，型別會跟著當前指派的值而定
      - Python 只能在 Jupyter Notebook 中執行
    correct_index: 2
    explanation: 動態型別表示變數名稱不綁定固定型別，執行時的值決定其型別。
```

`scripts/build_content.py` currently transforms this into app JSON by:

- renaming `text` to `textContent`
- renaming `correct_index` to `correctIndex`
- forcing each option to a string with `str(opt)`

The Flutter app in `~/ai-planner` currently expects:

- `QuestionDto.textContent: String`
- `QuestionDto.options: List<String>`
- `questions.options_json` in Drift as a JSON-encoded list of strings

This means rich option objects cannot be introduced directly without changing both the builder and the app model.

## Recommendation

Add a backward-compatible rich content schema using a new `content` field for prompts and a new object form for options. Keep existing scalar `text` and scalar options valid.

The builder should normalize both old and new YAML into a consistent app-facing JSON shape:

```json
{
  "textContent": "fallback markdown string",
  "content": [{ "type": "text", "text": "..." }],
  "options": ["fallback A", "fallback B"],
  "optionContent": [
    [{ "type": "text", "text": "fallback A" }],
    [{ "type": "text", "text": "fallback B" }]
  ]
}
```

This gives the app a gradual path:

1. Existing screens keep rendering `textContent` and `options`.
2. New screens can prefer `content` and `optionContent` when present.
3. Legacy YAML files do not need to be rewritten immediately.

## Proposed YAML Format

### Text-Only Questions Stay Valid

Existing questions should keep working unchanged:

```yaml
questions:
  - id: 8001
    text: Python 被稱為動態型別語言，主要代表什麼意思？
    options:
      - Python 程式一定會自動使用 GPU 執行
      - 變數宣告時必須明確指定資料型別
      - 變數本身不固定型別，型別會跟著當前指派的值而定
      - Python 只能在 Jupyter Notebook 中執行
    correct_index: 2
```

### Rich Prompt Content

Use `content` when the question prompt needs multiple blocks:

```yaml
questions:
  - id: 8101
    chapter_title: Basic Python Language
    section_title: 變數、型別與資料結構
    text: 下列程式碼執行後，輸出結果為何？
    content:
      - type: text
        text: 下列程式碼執行後，輸出結果為何？
      - type: code
        language: python
        code: |
          labels = {"cat": 0, "dog": 1}
          print(labels["dog"])
    type: multiple_choice
    options:
      - "0"
      - "1"
      - "cat"
      - "KeyError"
    correct_index: 1
```

`text` remains the fallback plain or Markdown representation for older app versions.

### Rich Answer Options

Use option objects when an answer option needs code or an image:

```yaml
questions:
  - id: 8102
    text: 哪一個選項正確建立 Python dictionary？
    type: multiple_choice
    options:
      - content:
          - type: code
            language: python
            code: |
              scores = {"A": 90, "B": 80}
        text: 'scores = {"A": 90, "B": 80}'
      - content:
          - type: code
            language: python
            code: |
              scores = ["A": 90, "B": 80]
        text: 'scores = ["A": 90, "B": 80]'
      - content:
          - type: code
            language: python
            code: |
              scores = ("A": 90, "B": 80)
        text: 'scores = ("A": 90, "B": 80)'
      - content:
          - type: code
            language: python
            code: |
              scores = set("A": 90, "B": 80)
        text: 'scores = set("A": 90, "B": 80)'
    correct_index: 0
```

Each rich option should include `text` as a fallback. The builder can generate a fallback if omitted, but requiring it keeps review and search easier.

### Images

Images should use paths relative to the YAML file or chapter directory. The builder should copy local image assets into the app asset folder, similar to how chapter images are copied today.

```yaml
questions:
  - id: 8103
    text: 觀察下圖，哪一個敘述最合理？
    content:
      - type: text
        text: 觀察下圖，哪一個敘述最合理？
      - type: image
        src: images/confusion_matrix.png
        alt: 混淆矩陣範例
        caption: 模型在四個類別上的預測結果
    options:
      - A 類別完全沒有預測錯誤
      - B 類別常被誤判為 C 類別
      - C 類別沒有任何樣本
      - D 類別召回率為 100%
    correct_index: 1
```

Recommended output path:

```text
assets/images/questions/{subject}_{chapter}_{question_id}_{filename}
```

The generated JSON should use Flutter asset paths:

```json
{
  "type": "image",
  "src": "assets/images/questions/m6_chapter1_8103_confusion_matrix.png",
  "alt": "混淆矩陣範例",
  "caption": "模型在四個類別上的預測結果"
}
```

## Content Block Types

Start with three block types:

```yaml
- type: text
  text: Markdown text is allowed.

- type: code
  language: python
  code: |
    print("hello")

- type: image
  src: images/example.png
  alt: 圖片替代文字
  caption: Optional caption
```

Do not add more block types until the app needs them. These three cover normal prompts, code snippets, screenshots, diagrams, charts, and image-based exam questions.

## Generated JSON Contract

Update `build_content.py` to emit both fallback string fields and rich fields:

```json
{
  "id": 8101,
  "textContent": "下列程式碼執行後，輸出結果為何？\n\n```python\nlabels = {\"cat\": 0, \"dog\": 1}\nprint(labels[\"dog\"])\n```",
  "content": [
    { "type": "text", "text": "下列程式碼執行後，輸出結果為何？" },
    {
      "type": "code",
      "language": "python",
      "code": "labels = {\"cat\": 0, \"dog\": 1}\nprint(labels[\"dog\"])\n"
    }
  ],
  "options": ["0", "1", "cat", "KeyError"],
  "optionContent": [
    [{ "type": "text", "text": "0" }],
    [{ "type": "text", "text": "1" }],
    [{ "type": "text", "text": "cat" }],
    [{ "type": "text", "text": "KeyError" }]
  ],
  "correctIndex": 1,
  "explanation": "dict 使用 key 查詢 value。"
}
```

Rules:

- `textContent` is always present.
- `options` is always present as `List<String>`.
- `content` is optional but should be emitted whenever YAML provides it.
- `optionContent` is optional but should be emitted whenever any option is rich.
- If `content` is absent, generate it from scalar `text`.
- If an option is a scalar, generate one text block for that option.
- If an option is an object, use `option.text` as the fallback string and `option.content` as the rich representation.

## `content.json` Schema Change

The top-level `content.json` structure should stay the same so subject, chapter, and section navigation do not change:

```json
{
  "version": 3,
  "subjects": [
    {
      "id": 6,
      "order": 6,
      "isLocked": false,
      "title": "Basic Python Language",
      "description": "...",
      "chapters": [
        {
          "id": 1006,
          "order": 1,
          "title": "Basic Python Language",
          "sections": [
            {
              "id": 10001,
              "order": 1,
              "title": "變數、型別與資料結構",
              "link_id": "sec-python-data-structures",
              "content": "<section>...</section>",
              "questions": []
            }
          ]
        }
      ]
    }
  ]
}
```

Only the objects inside each section's `questions` array need to change.

### Question Object

Recommended question object schema:

```json
{
  "id": 8101,
  "chapter_title": "Basic Python Language",
  "section_title": "變數、型別與資料結構",
  "type": "multiple_choice",
  "textContent": "Fallback Markdown prompt",
  "content": [],
  "options": [],
  "optionContent": [],
  "correctIndex": 1,
  "explanation": "Fallback Markdown explanation",
  "explanationContent": [],
  "tags": ["chap-m6-ch1", "sec-python-data-structures"],
  "usage": "both"
}
```

Field rules:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | number | yes | Existing question id. |
| `chapter_title` | string | no | Preserved metadata from YAML. |
| `section_title` | string | no | Used by `build_content.py` to attach questions to sections. |
| `type` | string | yes | Existing value, currently `multiple_choice`. |
| `textContent` | string | yes | Fallback Markdown prompt for the current app. |
| `content` | `ContentBlock[]` | no | Rich prompt blocks. Prefer this when rendering in the updated app. |
| `options` | `string[]` | yes | Fallback Markdown/plain option labels for the current app. |
| `optionContent` | `ContentBlock[][]` | no | Rich blocks per answer option. Indexes must match `options`. |
| `correctIndex` | number | yes | Existing zero-based correct option index. |
| `explanation` | string | no | Existing fallback explanation. |
| `explanationContent` | `ContentBlock[]` | no | Optional future extension; use the same block model if explanations need code or images. |
| `tags` | `string[]` | no | Existing tags. |
| `usage` | string | no | Existing usage field. Default remains `both`. |

Use `version: 3` for generated files that include rich question fields. The app can use this version to decide whether to parse `content`, `optionContent`, and future `explanationContent`. If a short-term rollout needs to keep `version: 2`, the app must explicitly ignore unknown fields and rely on `textContent` and `options`.

### Content Block Object

`content`, each item in `optionContent`, and future `explanationContent` all use the same block schema.

Text block:

```json
{
  "type": "text",
  "text": "Markdown text is allowed."
}
```

Code block:

```json
{
  "type": "code",
  "language": "python",
  "code": "def predict(x):\n    if x > 0:\n        return \"positive\"\n    return \"zero_or_negative\"\n"
}
```

Image block:

```json
{
  "type": "image",
  "src": "assets/images/questions/m6_chapter1_8103_confusion_matrix.png",
  "alt": "混淆矩陣範例",
  "caption": "模型在四個類別上的預測結果"
}
```

Block field rules:

| Block type | Required fields | Optional fields | Notes |
| --- | --- | --- | --- |
| `text` | `type`, `text` | none | `text` may contain Markdown. |
| `code` | `type`, `code` | `language` | Preserve code exactly after YAML parsing, including Python indentation. |
| `image` | `type`, `src`, `alt` | `caption` | `src` should be rewritten to a Flutter asset path by `build_content.py`. |

### Full Rich Question Example

```json
{
  "id": 8104,
  "chapter_title": "Basic Python Language",
  "section_title": "流程控制與函式",
  "type": "multiple_choice",
  "textContent": "觀察程式碼與圖片，哪個選項描述正確？\n\n```python\nfor i in range(3):\n    print(i)\n```\n\n![迴圈輸出示意圖](assets/images/questions/m6_chapter1_8104_loop-output.png)",
  "content": [
    {
      "type": "text",
      "text": "觀察程式碼與圖片，哪個選項描述正確？"
    },
    {
      "type": "code",
      "language": "python",
      "code": "for i in range(3):\n    print(i)\n"
    },
    {
      "type": "image",
      "src": "assets/images/questions/m6_chapter1_8104_loop-output.png",
      "alt": "迴圈輸出示意圖"
    }
  ],
  "options": [
    "程式會輸出 0、1、2",
    "程式會輸出 1、2、3",
    "程式只會輸出圖片中的最後一列",
    "程式會因為縮排錯誤而失敗"
  ],
  "optionContent": [
    [
      {
        "type": "text",
        "text": "程式會輸出 0、1、2"
      },
      {
        "type": "code",
        "language": "text",
        "code": "0\n1\n2\n"
      }
    ],
    [
      {
        "type": "text",
        "text": "程式會輸出 1、2、3"
      }
    ],
    [
      {
        "type": "text",
        "text": "程式只會輸出圖片中的最後一列"
      },
      {
        "type": "image",
        "src": "assets/images/questions/m6_chapter1_8104_option-c.png",
        "alt": "選項 C 示意圖"
      }
    ],
    [
      {
        "type": "text",
        "text": "程式會因為縮排錯誤而失敗"
      }
    ]
  ],
  "correctIndex": 0,
  "explanation": "`range(3)` 會產生 0、1、2，且 `print(i)` 的縮排位於 for 區塊內。",
  "tags": ["chap-m6-ch1", "sec-python-control-functions"],
  "usage": "both"
}
```

### Backward Compatibility

For every rich question, `build_content.py` must still generate valid fallback fields:

- `textContent` should be a Markdown rendering of `content`.
- `options[index]` should be a Markdown/plain rendering of `optionContent[index]`.
- Existing app code can continue to ignore `content` and `optionContent`.
- Updated app code should prefer rich fields when present.

## Builder Changes

Add helper functions to `scripts/build_content.py`:

```python
def normalize_blocks(blocks, base_dir, image_output_dir, asset_prefix):
    ...

def blocks_to_markdown(blocks):
    ...

def normalize_question(q, yaml_path, image_output_dir):
    ...

def normalize_option(option, yaml_path, image_output_dir):
    ...
```

Suggested behavior:

- Preserve current key migration from `text` to `textContent`.
- Stop converting all options with `str(opt)` directly; first inspect whether an option is a scalar or mapping.
- Resolve local image paths relative to `yaml_path.parent`.
- Copy question images to `assets/images/questions/`.
- Reject unsupported block types with a clear error message including question id and file path.
- Validate that `correct_index` is within the final option list length.
- Validate that every image has `alt`.
- Keep `version` at `2` only if the app ignores unknown fields safely; otherwise increment to `3`.

## App Changes In `~/ai-planner`

The current app can keep working with fallback fields, but rich rendering requires model and database changes.

Recommended app changes:

- Add Dart models for `ContentBlockDto`.
- Add nullable fields to `QuestionDto`: `List<ContentBlockDto>? content` and `List<List<ContentBlockDto>>? optionContent`.
- Store rich fields in Drift as JSON text columns, for example `content_json` and `option_content_json`.
- In quiz screens, render `content` when available; otherwise render `textContent`.
- Render `optionContent[index]` when available; otherwise render `options[index]`.
- Use the existing Markdown renderer for text blocks.
- Use a syntax-highlighted or monospace code widget for code blocks.
- Use `Image.asset()` for image blocks whose `src` starts with `assets/`.

This avoids a breaking app migration on day one because the existing string fields remain the source of truth until rich rendering is implemented.

## Migration Plan

1. Update `build_content.py` to normalize old and new question shapes.
2. Add validation tests with one scalar question, one code prompt, one image prompt, and one rich option.
3. Generate `content.json` and confirm the existing app still parses fallback fields.
4. Update `~/ai-planner` models and Drift schema to store optional rich fields.
5. Update quiz UI rendering to prefer rich fields.
6. Gradually convert YAML questions that need images or code snippets.

## Example Updated `chapter1.yaml` Entry

```yaml
questions:
  - id: 8101
    chapter_title: Basic Python Language
    section_title: 變數、型別與資料結構
    text: 下列程式碼執行後，輸出結果為何？
    content:
      - type: text
        text: 下列程式碼執行後，輸出結果為何？
      - type: code
        language: python
        code: |
          labels = {"cat": 0, "dog": 1}
          print(labels["dog"])
    type: multiple_choice
    options:
      - "0"
      - "1"
      - "cat"
      - "KeyError"
    correct_index: 1
    explanation: labels["dog"] 會取得 dog 對應的 value，也就是 1。
    tags:
      - chap-m6-ch1
      - sec-python-data-structures
    usage: both
```

## Open Decisions

- Whether rich fields should trigger `content.json` version `3`. (Let's use version 3)
- Whether code blocks need syntax highlighting in the first app implementation or just monospace rendering.  (Let's use monospace rendering first)
- Whether remote image URLs should be allowed. The recommended first version is local assets only. (Let's use local assets only first)
- Whether explanations should also support rich content later. The same block model can be reused as `explanationContent`. (Let's support rich content for explanations later)
