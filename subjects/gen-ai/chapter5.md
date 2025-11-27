---
title: "第五章：No Code / Low Code 平台與 AI 開發工具"
order: 5
label: sec-gen-chapter5
---

<!-- # 第五章：No Code / Low Code 平台與 AI 開發工具 {#sec-no-code-low-code} -->

> **考點摘要**：結合傳統 Low Code 概念與新一代 AI Native 開發工具，強調非技術人員的賦能與開發效率。

## 5.1 平台特性與選擇 (理論基礎)

### 1. No Code vs. Low Code
這兩者都是為了加速開發，但目標客群與適用場景不同。

*   **No Code (無程式碼)**：
    *   **核心**：完全圖形化介面 (GUI)，拖拉元件 (Drag-and-Drop) 即可完成。
    *   **目標客群**：非技術人員 (Citizen Developers)、行銷、PM。
    *   **適用場景**：標準化應用、簡單的表單流程、個人網站、內部儀表板。
    *   **限制**：靈活性低，只能做平台允許的功能，很難客製化複雜邏輯。
*   **Low Code (低程式碼)**：
    *   **核心**：大部分功能用拖拉，但關鍵邏輯允許（或需要）寫少量程式碼。
    *   **目標客群**：專業開發者 (加速開發)、具有基本程式概念的 IT 人員。
    *   **適用場景**：企業級應用 (ERP/CRM)、需串接多個舊系統、需高度客製化的邏輯。
    *   **優勢**：兼具開發速度與擴展性 (Scalability)。

### 2. 模型 (Model) 的定義
在 Low Code 平台的語境中，「Model」通常**不是**指 AI 模型，而是指**資料模型 (Data Model)**。
*   它抽象地描述了資料結構（如客戶資料表包含姓名、電話）、業務流程（訂單審核流程）與介面邏輯。
*   這讓開發者可以專注於業務邏輯，而不用管底層的資料庫語法。

## 5.2 熱門 AI 開發與 No/Low Code 工具 (實務趨勢)

新一代的開發工具深度整合了生成式 AI，模糊了 Coding 與 No Code 的界線。

### 1. AI 原生編輯器 (AI-Native IDEs)
這些編輯器從底層就整合了 AI，而不僅僅是外掛。

*   **Cursor**：
    *   基於 VS Code 修改。
    *   **Codebase RAG**：它會索引你整個專案的程式碼。當你問「如何新增一個 API？」時，它會參考你現有的程式碼風格與架構來回答，而不是給出通用的範例。
    *   **Composer**：可以同時編輯多個檔案，一次完成跨檔案的修改。
*   **Windsurf**：
    *   強調 "Flow" 範式。Agent 能持續監控你的開發行為，預測你下一步想做什麼，並主動提供協助。
*   **Google Antigravity**：
    *   **核心**：Google 推出的 "Agent-first" IDE，基於 VS Code 修改。
    *   **特色**：內建 Gemini 3 Pro 模型。採用雙視圖設計 (Editor & Manager)，允許使用者同時指揮多個 AI Agent 進行自主規劃、寫程式、執行終端機指令甚至瀏覽網頁。
    *   **優勢**：強調「可驗證性 (Verifiability)」，Agent 會產出實作計畫、螢幕截圖等 Artifacts，適合處理高度複雜的系統級任務。

### 2. 雲端與 Agentic 平台
*   **Replit**：
    *   雲端 IDE。其 **Replit Agent** 允許使用者用自然語言描述需求（如「做一個貪食蛇遊戲」），Agent 會自動規劃、寫程式、除錯並部署，使用者完全不用看程式碼。
*   **Lovable / v0**：
    *   專注於 UI 生成。使用者上傳一張手繪草圖或截圖，AI 直接生成可用的前端程式碼 (React/Tailwind)。

### 3. 模型引擎與 CLI
*   **GitHub Copilot**：
    *   最普及的 AI 助手。提供即時的程式碼補全 (Autocomplete) 和單元測試建議。
*   **Claude Code**：
    *   Anthropic 推出的 CLI 工具，具備強大的邏輯推理能力，能在終端機中直接操作檔案系統、執行指令並修改程式碼。
*   **[OpenAI Codex](https://openai.com/codex/)**：
    *   **核心**：最初是 GitHub Copilot 背後的模型，現已演化為全方位的雲端軟體工程 Agent。
    *   **特色**：可透過 CLI 或 IDE 擴充功能使用。具備在隔離沙箱 (Sandbox) 中導航程式碼庫、執行測試與修復 Bug 的能力。
    *   **模型**：由 `codex-1` (基於 o3 微調) 等專用模型驅動，擅長精確的程式碼生成與除錯。

### 4. 工作流自動化與視覺化編排 (Workflow Automation & Visual Orchestration)
這類工具專注於將 AI 模型與其他應用程式串接，或是提供視覺化的介面來設計複雜的 AI 處理流程。

*   **n8n**：
    *   **定位**：強大的工作流自動化工具 (Workflow Automation Tool)，強調可自託管與高度客製化。
    *   **AI 整合**：內建 AI Agent 節點，可以輕鬆將 LLM (如 GPT-4, Claude) 與超過 400 種外部服務 (如 Google Sheets, Slack, Email) 串接。
    *   **應用場景**：自動化辦公流程，例如「收到客戶 Email -> 用 AI 分析情緒與摘要 -> 寫入 Notion 資料庫 -> 自動草擬回信」。
*   **ComfyUI**：
    *   **定位**：專為 [Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion) 設計的節點式圖形介面 (Node-based GUI)。
    *   **核心**：將圖像生成的各個步驟 (如 Checkpoint 載入、CLIP 編碼、採樣器 Sampler、VAE 解碼) 拆解成獨立的節點，讓使用者能精細控制生成流程。
    *   **應用場景**：進階圖像生成、影片製作、建立複雜的圖像處理工作流 (Workflow)。
*   **LangFlow / Flowise**：
    *   **定位**：專為構建 LLM 應用設計的視覺化平台，通常基於 [LangChain](https://www.langchain.com/) 框架。
    *   **核心**：提供拖拉介面來組裝 RAG (檢索增強生成) 系統、聊天機器人 (Chatbot) 或 Agent。
    *   **應用場景**：快速原型開發 (Prototyping)，無需寫程式即可測試不同的 Prompt 策略或知識庫檢索效果。

### 5. 工具比較總結 (Summary Table)

| 工具名稱 (Tool) | 類別 (Category) | 核心特色 (Key Features) | 適用場景 (Use Case) |
| :--- | :--- | :--- | :--- |
| **Cursor** | AI-Native IDE | Codebase RAG, Composer (跨檔案編輯) | 專業開發者日常 Coding |
| **Windsurf** | AI-Native IDE | Flow 範式, 主動預測開發行為 | 追求流暢開發體驗的工程師 |
| **Google Antigravity** | AI-Native IDE | Agent-first, 雙視圖, 可驗證 Artifacts | 複雜系統開發, 需高度自主 Agent |
| **Replit** | Cloud / Agentic | 雲端 IDE, 自然語言生成 App (Replit Agent) | 快速構建 MVP, 非專業開發者 |
| **Lovable / v0** | UI Generation | 圖像/草圖轉前端程式碼 (React/Tailwind) | 前端介面設計, 快速 UI 原型 |
| **GitHub Copilot** | CLI / Extension | 程式碼補全, 單元測試建議 | 輔助 Coding, 提升寫碼速度 |
| **Claude Code** | CLI | 終端機操作, 邏輯推理, 檔案系統控制 | 腳本自動化, 複雜重構任務 |
| **OpenAI Codex** | Model / Agent | 雲端軟體工程 Agent, 沙箱執行 | 程式碼生成, Bug 修復, 測試 |
| **n8n** | Workflow Automation | 串接 LLM 與 400+ 外部服務, 辦公自動化 | 企業流程自動化, 資料串接 |
| **ComfyUI** | Visual Orchestration | 節點式 Stable Diffusion 工作流 | 進階 AI 圖像/影片生成 |
| **LangFlow / Flowise** | Visual Orchestration | 視覺化 LLM/RAG 應用構建 (LangChain) | 快速打造 Chatbot, RAG 原型 |

## 5.3 整合策略與風險

### 1. 影子 IT (Shadow IT)
*   **定義**：員工在未經 IT 部門核准的情況下，擅自使用外部的 No Code/AI 工具來處理公務。
*   **風險**：
    *   **資安漏洞**：資料可能被上傳到不安全的雲端。
    *   **缺乏維護**：員工離職後，他用 No Code 做的系統沒人會維護，變成孤兒系統。
    *   **資料孤島**：數據散落在各個小應用中，無法整合。

### 2. 開發輔助策略
*   利用 AI 生成 boilerplate code (樣板程式碼)、API 呼叫範例、測試數據，讓開發者專注於核心邏輯。
*   **Review 是關鍵**：AI 生成的程式碼可能有 Bug 或安全漏洞，人類必須進行 Code Review。
