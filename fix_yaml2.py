import yaml, os, glob

replacements = {
    7101: [
        "聊天機器人只能單輪問答，無法理解上下文",
        "代理人能自主規劃並執行工具，機器人僅問答",
        "代理人不需語言模型即可自主執行複雜任務",
        "代理人只能執行特定腳本，機器人可自由對話"
    ],
    7104: [
        "先完整生成整個任務計劃，再一次性執行所有步驟",
        "透過事後檢討記錄失敗原因，以改進下一次的嘗試",
        "交替進行推理與行動，並根據環境觀察來動態調整",
        "使用多個不同代理人並行處理，最終投票決定結果"
    ],
    7105: [
        "Reflexion 專門用於數學計算，且不呼叫任何外部工具",
        "Reflexion 引入反思機制，將失敗經驗轉化為文字記憶",
        "Reflexion 透過多個模型協同工作來解決複雜邏輯問題",
        "Reflexion 預先載入大量成功案例以提高任務成功機率"
    ],
    7107: [
        "評估代理人每秒內能夠成功處理的最高併發請求數量",
        "評估代理人完成任務所需最少步驟，步驟越少效率越高",
        "評估代理人在複雜情境下正確選擇並呼叫工具的比例",
        "評估代理人在嚴格限制的時間內成功完成任務的比例"
    ],
    7108: [
        "大幅加速大型語言模型在處理複雜長文本時的推理速度",
        "讓代理人意識自身決策過程，並根據經驗進行自我修正",
        "強制代理人嚴格按照預先設定的固定腳本逐步執行任務",
        "根據當前環境與任務需求，自動為代理人生成新工具函數"
    ],
    7201: [
        "提升大型語言模型處理海量資料時的執行與推理速度",
        "解決 AI 模型與工具整合的碎片化問題，提供標準協議",
        "改善大型語言模型的訓練效率並顯著降低硬體資源消耗",
        "大幅降低 AI 模型在回答專業問題時產生的幻覺現象"
    ],
    7202: [
        "負責在本地環境中直接儲存與管理所有工具的程式碼邏輯",
        "管理客戶端生命週期、協調通訊，並負責執行核心授權決策",
        "主要功能是負責將使用者的自然語言輸入轉換為 JSON 格式",
        "作為語言模型與使用者之間單純負責語言翻譯的中介層服務"
    ],
    7204: [
        "資源是提供 LLM 讀取的靜態資料，工具是可執行的操作",
        "資源比工具更安全且不需授權，工具則需要經過嚴格審核",
        "工具只能回傳純文字結果，而資源則專門用來回傳二進位資料",
        "資源和工具在功能與本質上完全相同，純粹只是不同命名習慣"
    ],
    7205: [
        "stdio 適合遠端叢集伺服器，HTTP + SSE 適合本地應用程式",
        "stdio 適合本地端直接部署，HTTP + SSE 適合遠端與雲端部署",
        "stdio 的執行速度極快但不安全，HTTP + SSE 速度較慢但安全",
        "兩者在部署架構與使用情境上完全相同，純粹只是連線語法不同"
    ],
    7207: [
        "基於安全考量，系統預設禁止語言模型呼叫任何外部操作工具",
        "伺服器應對來自 LLM 的輸入進行驗證，不信任未經驗證內容",
        "為了確保相容性與安全性，建議只使用官方所提供的標準伺服器",
        "為了防止資料外洩，必須將所有工具呼叫結果加密後再回傳給模型"
    ]
}

class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

for f in sorted(glob.glob("subjects/m5/*.yaml")):
    with open(f, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    
    changed = False
    for q in data.get("questions", []):
        qid = q.get("id")
        if qid in replacements:
            q["options"] = replacements[qid]
            changed = True
            
    if changed:
        with open(f, "w", encoding="utf-8") as fh:
            yaml.dump(data, fh, Dumper=MyDumper, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"Updated {f}")
