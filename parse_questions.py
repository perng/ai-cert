import re
import os
import yaml

with open('/Users/charles/.gemini/antigravity/brain/ee715722-dec9-4991-b720-f2272b5ca067/scratch/pdf_text.txt', 'r') as f:
    text = f.read()

pattern = re.compile(r'([A-D])\s+(\d+)\.\s+(.*?)(?=\(A\))(.*?)(?=\(B\))(.*?)(?=\(C\))(.*?)(?=\(D\))(.*?)(?=[A-D]\s+\d+\.\s+|$)', re.DOTALL)
matches = pattern.findall(text)

chapter_keywords = {
    'chapter1.yaml': ['弱人工智慧', '強人工智慧', '專家系統', '符號邏輯', '達特茅斯', '圖靈測試', '人機協作', '定義', '歷史'],
    'chapter3.yaml': ['資料清理', '缺失值', '標準化', '特徵', '探索性資料分析', 'EDA', '轉換', '型態', 'V', '大數據'],
    'chapter5.yaml': ['監督式', '分類', '迴歸', '決策樹', '隨機森林', 'SVM', 'KNN', '邏輯迴歸', '線性迴歸'],
    'chapter6.yaml': ['非監督式', '分群', 'K-Means', '降維', 'PCA', '關聯規則', '強化學習', 'Q-learning'],
    'chapter7.yaml': ['深度學習', '神經網路', 'CNN', 'RNN', '梯度消失', '啟動函數', '卷積', '池化', 'LSTM'],
    'chapter8.yaml': ['生成式', 'LLM', '變分自編碼', 'GAN', 'RAG', '提示', '微調', 'Transformer', 'Attention'],
    'chapter9.yaml': ['評估指標', '準確率', '召回率', 'F1', '均方誤差', '過度擬合', '欠擬合', '交叉驗證', 'MSE', 'ROC', 'AUC', '梯度下降', '學習率'],
    'chapter10.yaml': ['邊緣運算', '雲端', 'MLOps', '容器化', '推論', '部署', '專案管理', '敏捷'],
    'chapter11.yaml': ['隱私', '偏見', '智財權', '歐盟', '聯邦學習', '差分隱私', '可解釋', '公平性', '法規', '倫理'],
    'chapter12.yaml': ['Sora', 'SynthID', 'AgentKit', 'Realtime', '多模態', '浮水印', 'Copilot']
}

def guess_chapter(question_text):
    scores = {ch: 0 for ch in chapter_keywords}
    for ch, kws in chapter_keywords.items():
        for kw in kws:
            if kw.lower() in question_text.lower():
                scores[ch] += 1
    best_ch = max(scores, key=scores.get)
    if scores[best_ch] == 0:
        return 'chapter1.yaml' # default
    return best_ch

ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

results = {ch: [] for ch in chapter_keywords}
results['chapter1.yaml'] = []
results['chapter2.yaml'] = []
results['chapter4.yaml'] = []

for m in matches:
    ans, num, q_text, opt_a, opt_b, opt_c, opt_d = m
    q_text = q_text.strip().replace('\n', '')
    
    # Clean options
    opt_a = opt_a.strip().replace('(A)', '').strip()
    opt_b = opt_b.strip().replace('(B)', '').strip()
    opt_c = opt_c.strip().replace('(C)', '').strip()
    opt_d = opt_d.strip().replace('(D)', '').strip()
    
    # Format option text removing trailing semicolons
    opts = [opt_a, opt_b, opt_c, opt_d]
    for i in range(4):
        if opts[i].endswith('；'): opts[i] = opts[i][:-1]
        
    full_text = q_text + " " + " ".join(opts)
    ch = guess_chapter(full_text)
    
    q_obj = {
        'id': f"115-1-{num}",
        'text': f"{q_text} （115年第一梯次）",
        'type': 'multiple_choice',
        'options': opts,
        'correct_index': ans_map[ans.strip()],
        'explanation': '（115年第一梯次公告試題）',
        'tags': ['past-exam', '115-1'],
        'usage': 'mock'
    }
    
    if ch not in results: results[ch] = []
    results[ch].append(q_obj)

base_dir = '/Users/charles/ai-cert/subjects/ai-foundation'

for ch, qs in results.items():
    if not qs: continue
    filepath = os.path.join(base_dir, ch)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f) or {}
        
    if 'questions' not in data:
        data['questions'] = []
        
    # Append
    for q in qs:
        # Give numeric ID based on chapter if possible, or just string ID
        # Looking at chapter1.yaml it uses numeric like 11401. I'll just use string for safe.
        data['questions'].append(q)
        
    # write back
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

print("Done appending to YAML files.")
