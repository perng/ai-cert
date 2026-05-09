import json
import os

with open('/Users/charles/ai-cert/assets/content.json', 'r', encoding='utf-8') as f:
    content = json.load(f)

empty_past_exams = []

for subject in content.get('subjects', []):
    for chapter in subject.get('chapters', []):
        for section in chapter.get('sections', []):
            # Check if this is a past exam section by id or title
            if section.get('id') == 'sec-past-exam' or '歷屆考題' in section.get('title', ''):
                if len(section.get('questions', [])) == 0:
                    empty_past_exams.append(f"{subject.get('id')} -> {chapter.get('title')}")

print(f"Total empty '歷屆考題' sections: {len(empty_past_exams)}")
if empty_past_exams:
    print("List of chapters with NO past exam questions attached:")
    for item in empty_past_exams:
        print(f"  - {item}")
