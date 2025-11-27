---
title: "生成式 AI 模型架構與機制 (Generative Models & Mechanisms)"
order: 1
label: sec-gen-chapter1
---

<!-- # 生成式 AI 模型架構與機制 (Generative Models & Mechanisms) {#sec-gen-ai-models} -->

> **考點摘要**：不同於基礎 AI 概論，本科聚焦於「生成」技術的特點、Transformer 變體應用以及推論參數的控制。

## 1.1 Transformer 架構變體

Transformer 模型自 2017 年問世以來，已成為自然語言處理 (NLP) 的基石。根據其架構的不同部分，主要可以分為三大類：

### 1. Encoder-only (編碼器模型)
這類模型只使用了 Transformer 的編碼器部分。它們透過**雙向注意力機制 (Bidirectional Attention)** 同時關注上下文，因此非常擅長理解語意。

*   **代表模型**：BERT (Bidirectional Encoder Representations from Transformers), RoBERTa。
*   **核心能力**：**理解與分類**。
    *   情感分析 (Sentiment Analysis)：判斷這句話是正評還是負評。
    *   命名實體識別 (NER)：找出句子中的人名、地名、機構名。
    *   文本分類 (Text Classification)：將新聞歸類為體育、財經或政治。
*   **運作原理**：像是一個閱讀測驗的高手，讀完文章後能精準回答關於文章內容的問題，但不太會自己寫作文。

### 2. Decoder-only (解碼器模型)
這類模型只使用了 Transformer 的解碼器部分。它們採用**遮罩注意力機制 (Masked Self-Attention)**，只能看到前面的字，無法看到後面的字（單向），因此非常適合預測下一個字。

*   **代表模型**：GPT (Generative Pre-trained Transformer) 系列, LLaMA, Claude。
*   **核心能力**：**生成與續寫**。
    *   文本生成 (Text Generation)：寫故事、寫信、寫程式碼。
    *   對話系統 (Chatbot)：與使用者進行流暢的對話。
*   **運作原理**：像是一個即興演講者或小說家，根據已經講過的內容，不斷構思並說出下一個字，創造出流暢的篇章。

### 3. Encoder-Decoder (編碼器-解碼器模型)
這類模型完整保留了 Transformer 的架構。編碼器負責理解輸入，解碼器負責生成輸出。

*   **代表模型**：T5 (Text-to-Text Transfer Transformer), BART。
*   **核心能力**：**序列到序列 (Seq2Seq) 的轉換**。
    *   機器翻譯 (Machine Translation)：將英文句子轉換為中文句子。
    *   文本摘要 (Summarization)：將長篇文章轉換為短摘要。
*   **運作原理**：像是一個專業的翻譯官，先聽懂（Encode）整段話的意思，再用另一種語言或形式表達（Decode）出來。

| 架構類型 | 代表模型 | 核心機制 | 擅長任務 | 類比 |
| :--- | :--- | :--- | :--- | :--- |
| **Encoder-only** | BERT | 雙向注意力 | 理解、分類、標註 | 閱讀測驗高手 |
| **Decoder-only** | GPT | 單向 (遮罩) 注意力 | 生成、創作、續寫 | 小說家 |
| **Encoder-Decoder** | T5 | 完整 Transformer | 翻譯、摘要、轉換 | 翻譯官 |

## 1.2 模型參數與控制

在使用生成式 AI (特別是 LLM) 進行推論 (Inference) 時，我們可以透過調整參數來控制輸出的風格與品質。

### 1. 溫度 (Temperature)
溫度參數控制了模型在選擇下一個 Token 時的**隨機性 (Randomness)**。

*   **低溫 (0.1 - 0.3)**：
    *   **效果**：模型會傾向選擇機率最高的字。輸出非常穩定、確定性高，幾乎每次跑結果都一樣。
    *   **適用場景**：事實問答、程式碼生成、數學解題、資料萃取。
    *   *例子*：問「台灣的首都在哪？」，我們希望它回答「台北」，而不是發揮創意說「可能是高雄」。
*   **高溫 (0.7 - 1.0+)**：
    *   **效果**：模型有機會選擇機率較低（但仍合理）的字。輸出變化多端，充滿創造力，但有時會胡言亂語。
    *   **適用場景**：創意寫作、腦力激盪、寫詩、聊天。
    *   *例子*：請它「寫一首關於秋天的詩」，高溫可以讓用詞更豐富、意境更獨特。

### 2. Top-P (Nucleus Sampling)
這是另一種控制隨機性的方法，通常與 Temperature 二擇一使用。

*   **原理**：模型只從累積機率達到 P (例如 0.9) 的前幾個候選字中進行抽樣。
*   **效果**：截斷了機率極低的尾端選項（那些完全不通順的字），確保生成的內容在「有創意」的同時，依然保持「通順合理」。

### 3. Token (代幣) 與 Context (上下文)

*   **Token (代幣)**：
    *   LLM 看不懂中文字或英文字母，它看的是 Token。
    *   **計算方式**：
        *   英文：通常 1 個單字 $\approx$ 1.3 個 Token (或是 1000 Tokens $\approx$ 750 單字)。
        *   中文：通常 1 個中文字 $\approx$ 1.5 ~ 2 個 Token (取決於分詞器)。
    *   *考點*：API 計費通常是以 Token 數計算，包含輸入 (Prompt) 和輸出 (Completion)。

*   **Context Window (上下文視窗)**：
    *   **定義**：模型一次能「記住」的最大 Token 數量 (包含輸入 + 輸出)。
    *   **限制**：
        *   早期模型 (如 GPT-3) 只有 4k Tokens。
        *   現代模型 (如 GPT-4, Claude 3) 可達 128k 甚至 1M Tokens。
    *   **影響**：如果對話長度超過 Context Window，最早的訊息就會被「擠出」記憶，模型會忘記你一開始說過的話。
    *   **解決策略**：使用 RAG (檢索增強生成) 或摘要技術來管理上下文。

### 4. 頻率懲罰 (Frequency Penalty) 與 存在懲罰 (Presence Penalty)
*   **Frequency Penalty**：根據一個字**已經出現的次數**來懲罰它。出現越多次，懲罰越重。
    *   *用途*：減少「跳針」、重複同一句話的情況。
*   **Presence Penalty**：只要一個字**出現過**（不管幾次），就給予懲罰。
    *   *用途*：鼓勵模型談論新的話題，增加多樣性。
