import json

with open('assets/content.json', 'r', encoding='utf-8') as f:
    content = json.load(f)

prompts = []

for subject in content.get('subjects', []):
    subject_title = subject.get('title', subject.get('id', 'Unknown Subject'))
    
    for chapter in subject.get('chapters', []):
        chapter_title = chapter.get('title', 'Unknown Chapter')
        
        for section in chapter.get('sections', []):
            section_title = section.get('title', '')
            
            if '歷屆考題' in section_title:
                continue
                
            sec_content = section.get('content', '')
            questions = section.get('questions', [])
            
            content_len = len(sec_content)
            q_count = len(questions)
            
            issues = []
            if content_len < 200:
                issues.append(f"- The content length is only {content_len} characters (needs at least 200).")
            if q_count < 3:
                issues.append(f"- The section only has {q_count} questions (needs at least 3).")
                
            if issues:
                prompt = f"Please improve the following section in the AI certification curriculum:\n\n"
                prompt += f"**Subject:** {subject_title}\n"
                prompt += f"**Chapter:** {chapter_title}\n"
                prompt += f"**Section:** {section_title}\n\n"
                prompt += "**Identified Issues:**\n"
                prompt += "\n".join(issues) + "\n\n"
                
                if content_len < 200:
                    prompt += "**Current Content Snippet:**\n"
                    snippet = sec_content.strip()
                    if not snippet:
                        snippet = "(Empty)"
                    prompt += f"```markdown\n{snippet}\n```\n\n"
                    prompt += "Task 1: Please write detailed, educational textbook content for this section to reach at least 200 characters. Cover the core concepts, technical details, and real-world examples related to this topic.\n"
                    
                if q_count < 3:
                    prompt += f"Task 2: Please generate {3 - q_count} additional high-quality, multiple-choice questions for this section in YAML format. Ensure the questions have clear explanations and plausible distractors.\n"
                    
                prompt += "---\n"
                prompts.append(prompt)

output_file = 'scripts/health_check_prompts.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(prompts))

print(f"Health check completed. Found {len(prompts)} sections that need improvement.")
print(f"Generated LLM prompts have been saved to {output_file}")
