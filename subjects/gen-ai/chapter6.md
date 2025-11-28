---
title: "第六章：生成式 AI 專案管理與評估 (Project Planning & Eval)"
order: 6
label: sec-gen-chapter6
---

<!-- # 第六章：生成式 AI 專案管理與評估 (Project Planning & Eval) {#sec-project-planning} -->

> **考點摘要**：涵蓋從 POC 到上線的完整流程，以及如何量化評估生成模型的好壞。

## 導入流程與策略 {#sec-implementation-strategy}

### 1. 階段規劃 {.unnumbered}
導入 GenAI 專案通常遵循以下步驟：
1.  **目標設定 (Goal Setting)**：明確定義要解決什麼問題（如：減少客服 30% 工作量）。設定 KPI。
2.  **資料準備 (Data Preparation)**：清洗企業內部資料，去個資，轉換格式。這是最耗時但也最重要的步驟。
3.  **技術選型 (Model Selection)**：決定用雲端 API (GPT-4) 還是自建模型 (Llama 3)？決定用 RAG 還是 Fine-tuning？
4.  **POC (概念驗證)**：快速做出原型，驗證可行性。
5.  **部署與監控 (Deployment & Monitoring)**：上線後持續監控幻覺率與使用者滿意度。

### 2. 部署策略：雲端 vs. 本地 {.unnumbered}
*   **雲端 API (Cloud API)**：
    *   *優點*：建置快、無需維護硬體、模型能力最強 (SOTA)。
    *   *缺點*：資料需傳出企業、長期成本高（按 Token 計費）、受限於 API 速率限制 (Rate Limit)。
    *   *適用*：POC 階段、非核心業務、對資安要求較低的場景。
*   **本地部署 (Local Deployment / On-Premise)**：
    *   *優點*：**資料隱私最高**（資料不出門）、可完全掌控模型行為、無傳輸延遲。
    *   *缺點*：初期硬體投資大 (GPU Server)、需專業團隊維護 MLOps。
    *   *適用*：金融/醫療等高監管行業、處理機密資料。

<!-- Image Prompt: Title: "Cloud vs. Local Deployment". Style: Stick figures with color. Content: A split scene. Left (Cloud): A stick figure relaxing on a cloud, throwing data packets into the sky. It's fast and easy, but the data is flying away. Label: "Cloud API (Easy but Data Leaves)". Right (Local): A stick figure sweating while guarding a huge, heavy server rack inside a fortress. It's secure, but hard work. Label: "Local Deployment (Secure but Heavy Ops)". Note: dialogs and all texts/labels should be in Traditional Chinese. -->

### 3. 硬體資源優化 {.unnumbered}
*   **GPU 利用率低**：常見原因包括 Batch Size 設太小（GPU 沒吃飽）或 I/O 瓶頸（硬碟讀取太慢，GPU 在等資料）。
*   **VRAM 估算**：跑一個 7B 的模型 (FP16) 大約需要 14GB VRAM。若使用量化 (INT4)，則只需約 5-6GB。

## 效能評估指標 {#sec-performance-metrics}

評估生成式 AI 比評估傳統 AI 難，因為「好文筆」很難量化。

### 1. 基準測試 (Benchmarks) {.unnumbered}
學術界常用的標準考卷：
*   **MMLU (Massive Multitask Language Understanding)**：包含數學、歷史、法律、醫學等 57 個學科，測試模型的**廣度知識**與推理能力。
*   **GSM8K**：小學數學應用題。測試模型的**多步驟推理**能力。
*   **HumanEval / MBPP**：測試**寫程式**的能力。
*   **TTQA (Taiwan Truthful QA)**：針對**台灣本土文化與知識**的測試集（避免模型只懂美國文化）。

### 2. 服務指標 (Service Metrics) {.unnumbered}
上線後要看的指標：
*   **TTFT (Time to First Token)**：從使用者送出請求，到看到第一個字跳出來的時間。這直接影響**使用者體驗 (感知延遲)**。
*   **TPS (Tokens Per Second)**：生成速度。越快越好。
*   **Latency (總延遲)**：生成完整回應所需的時間。
*   **Throughput (吞吐量)**：系統單位時間內能處理多少請求。

<!-- Image Prompt: Title: "AI Service Metrics". Style: Stick figures with color. Content: A race track scene. One stick figure (TTFT) sprints off the starting line instantly but runs slowly. Another stick figure (Throughput) starts slowly but carries a huge pile of boxes (Tokens) and moves a massive amount of cargo by the end. Label: "Responsiveness (TTFT) vs. Efficiency (Throughput)". Note: dialogs and all texts/labels should be in Traditional Chinese. -->

### 3. 準確性與安全性評估 {.unnumbered}
*   **LLM-as-a-Judge**：用更強的模型 (如 GPT-4) 來幫小模型 (如 Llama-7B) 的回答評分。
*   **紅隊演練 (Red Teaming)**：聘請專家扮演攻擊者，故意誘導模型說出有害內容，以找出安全漏洞。
*   **對抗性測試 (Adversarial Testing)**：輸入微擾動的樣本，看模型是否會崩潰或輸出錯誤。
