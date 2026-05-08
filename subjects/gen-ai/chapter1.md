---
title: "生成式 AI 模型架構與機制 (Generative Models & Mechanisms)"
order: 1
label: chap-gen-chapter1
---

<!-- # 生成式 AI 模型架構與機制 (Generative Models & Mechanisms) {#sec-gen-ai-models} -->

> **考點摘要**：不同於基礎 AI 概論，本科聚焦於「生成」技術的特點、Transformer 變體應用以及推論參數的控制。

## Transformer 核心機制 {#sec-transformer-core}

Transformer 的強大來自於其獨特的設計，摒棄了傳統 RNN 的循環處理方式，改用並行運算。

### 1. 自注意力機制 (Self-Attention) {.unnumbered}
這是 Transformer 的靈魂。它讓模型在處理一個字時，能同時「關注」句子中的其他字，從而理解上下文關係。

*   **例子**：「**蘋果**因為太貴了，所以我沒買**它**。」
    *   當模型處理「它」這個字時，Self-Attention 機制會告訴模型，「它」指代的是前面的「蘋果」，而不是「我」。
*   **優勢**：解決了長距離依賴問題 (Long-term Dependency)，即使句子很長，開頭和結尾的關係也能被捕捉。



### 2. 位置編碼 (Positional Encoding) {.unnumbered}
由於 Transformer 是並行處理所有字（不像 RNN 一個字一個字讀），它本身不知道「順序」。

*   **功能**：給每個字加上一個「位置標籤」，讓模型知道哪個字在前面，哪個字在後面。
*   **意義**：確保「貓追狗」和「狗追貓」能被區分為不同的語意。


## Transformer 架構變體 {#sec-transformer-variants}

Transformer 模型自 2017 年問世以來，已成為自然語言處理 (NLP) 的基石。根據其架構的不同部分，主要可以分為三大類：

![Transformer 架構變體](images/transformer_architectures.webp)

### 1. Encoder-only (編碼器模型) {.unnumbered}
這類模型只使用了 Transformer 的編碼器部分。它們透過**雙向注意力機制 (Bidirectional Attention)** 同時關注上下文，因此非常擅長理解語意。

*   **代表模型**：BERT (Bidirectional Encoder Representations from Transformers), RoBERTa。
*   **核心能力**：**理解與分類**。
    *   情感分析 (Sentiment Analysis)：判斷這句話是正評還是負評。
    *   命名實體識別 (NER)：找出句子中的人名、地名、機構名。
    *   文本分類 (Text Classification)：將新聞歸類為體育、財經或政治。
*   **運作原理**：像是一個閱讀測驗的高手，讀完文章後能精準回答關於文章內容的問題，但不太會自己寫作文。

### 2. Decoder-only (解碼器模型) {.unnumbered}
這類模型只使用了 Transformer 的解碼器部分。它們採用**遮罩注意力機制 (Masked Self-Attention)**，只能看到前面的字，無法看到後面的字（單向），因此非常適合預測下一個字。

*   **代表模型**：GPT (Generative Pre-trained Transformer) 系列, LLaMA, Claude。
*   **核心能力**：**生成與續寫**。
    *   文本生成 (Text Generation)：寫故事、寫信、寫程式碼。
    *   對話系統 (Chatbot)：與使用者進行流暢的對話。
*   **運作原理**：像是一個即興演講者或小說家，根據已經講過的內容，不斷構思並說出下一個字，創造出流暢的篇章。

### 3. Encoder-Decoder (編碼器-解碼器模型) {.unnumbered}
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

## LLM 訓練生命週期 (The Lifecycle of LLM Training) {#sec-llm-lifecycle}

一個成熟的生成式 AI 模型（如 ChatGPT）通常經歷三個階段的訓練：

### 1. 預訓練 (Pre-training) {.unnumbered}
*   **目標**：讓模型學會「說人話」並具備廣泛的世界知識。
*   **資料**：海量的網際網路文本 (Wikipedia, 書籍, 網頁)。
*   **方法**：**自監督學習 (Self-Supervised Learning)**。遮住下一個字，讓模型去猜。
*   **產出**：基底模型 (Base Model)。它懂很多知識，但不懂如何遵循指令（你問它問題，它可能會反問你）。

### 2. 監督式微調 (Supervised Fine-Tuning, SFT) {.unnumbered}
*   **目標**：教會模型「聽懂指令」並以對話方式回應。
*   **資料**：人類精心撰寫的「指令-回答」對 (Instruction-Response Pairs)。
*   **產出**：指令微調模型 (Instruction Tuned Model)。此時模型已經可以當 Chatbot 用了。

### 3. 人類回饋強化學習 (RLHF) {.unnumbered}
*   **目標**：讓模型的回答更符合人類的價值觀（有用、誠實、無害）。
*   **方法**：
    *   讓模型生成多個回答。
    *   人類標註員對回答進行排名 (Ranking)。
    *   訓練一個獎勵模型 (Reward Model) 來模擬人類喜好。
    *   用強化學習 (PPO) 優化模型。
*   **產出**：對齊模型 (Aligned Model)。這是我們最終使用的版本 (如 GPT-4)。

<!-- Image Prompt: Title: "LLM Training Lifecycle". Style: Stick figures with color. Content: Three stages. Stage 1 (Pre-training): A robot reading a mountain of books (Base Model). Stage 2 (SFT): A teacher showing the robot Q&A flashcards (Instruction Tuned). Stage 3 (RLHF): A human giving a thumbs up/down to the robot's answers (Aligned Model). Label: "From Reading to Chatting". Note: dialogs and all texts/labels should be in Traditional Chinese. -->

## 模型參數與控制 {#sec-model-params}

在使用生成式 AI (特別是 LLM) 進行推論 (Inference) 時，我們可以透過調整參數來控制輸出的風格與品質。

### 1. 溫度 (Temperature) {.unnumbered}
溫度參數控制了模型在選擇下一個 Token 時的**隨機性 (Randomness)**。

![AI 溫度](images/ai_temperature.webp)

*   **低溫 (0.1 - 0.3)**：
    *   **效果**：模型會傾向選擇機率最高的 Token。輸出非常穩定、確定性高，幾乎每次跑結果都一樣。
    *   **適用場景**：事實問答、程式碼生成、數學解題、資料萃取。
    *   *例子*：問「中華民國的首都是哪？」，我們希望它回答「台北」，而不是發揮創意說「可能是高雄」。
*   **高溫 (0.7 - 1.0+)**：
    *   **效果**：模型有機會選擇機率較低（但仍合理）的 Token。輸出變化多端，充滿創造力，但有時會胡言亂語。
    *   **適用場景**：創意寫作、腦力激盪、寫詩、聊天。
    *   *例子*：請它「寫一首關於秋天的詩」，高溫可以讓用詞更豐富、意境更獨特。

### 2. Top-K Sampling {.unnumbered}
*   **原理**：限制模型只能從機率最高的 **K** 個 Token 中選擇 (例如 K=50)。
*   **效果**：強迫模型忽略那些機率極低的冷門字，避免生成離題或不通順的內容。

### 3. Top-P (Nucleus Sampling) {.unnumbered}
這是另一種控制隨機性的方法，通常與 Temperature 二擇一使用。

*   **原理**：模型只從累積機率達到 P (例如 0.9) 的前幾個候選 Token 中進行抽樣。
*   **效果**：截斷了機率極低的尾端選項（那些完全不通順的字），確保生成的內容在「有創意」的同時，依然保持「通順合理」。

### 4. Token (詞元) 與 Context (上下文) {.unnumbered}

![Token](images/token.webp)

*   **Token (詞元)**：
    *   LLM 看不懂中文字或英文字母，它看的是 Token。
    *   **計算方式**：
        *   英文：通常 1 個單字約等於 1.3 個 Token (或是 1000 Tokens 約等於 750 單字)。
        *   中文：通常 1 個中文字約等於 1.5 ~ 2 個 Token (取決於分詞器)。
    *   *考點*：API 計費通常是以 Token 數計算，包含輸入 (Prompt) 和輸出 (Completion)。
    *   **注意**：新型的「推論模型」(Reasoning Models, 如 OpenAI o1)，其內部的「思考過程」(Reasoning Tokens) 雖不可見，但**通常會被計入輸出 Token (Output Tokens)** 收費。

![Context Window](images/context_window.webp)

*   **Context Window (上下文窗口)**：
    *   **定義**：模型一次能「記住」的最大 Token 數量 (包含輸入 + 輸出)。
    *   **限制**：
        *   早期模型 (如 GPT-3) 只有 4k Tokens。
        *   現代模型 (如 GPT-4, Claude 3) 可達 128k 甚至 1M Tokens。
    *   **影響**：如果對話長度超過 Context Window，最早的訊息就會被「擠出」記憶，模型會忘記你一開始說過的話。
    *   **解決策略**：使用 RAG (檢索增強生成) 或摘要技術來管理上下文。

### 5. 頻率懲罰 (Frequency Penalty) 與 存在懲罰 (Presence Penalty) {.unnumbered}
*   **Frequency Penalty**：根據一個字**已經出現的次數**來懲罰它。出現越多次，懲罰越重。
    *   *用途*：減少「跳針」、重複同一句話的情況。
*   **Presence Penalty**：只要一個字**出現過**（不管幾次），就給予懲罰。
    *   *用途*：鼓勵模型談論新的話題，增加多樣性。

### 6. 生成策略 (Generation Strategies) {.unnumbered}
除了上述參數，模型在生成時的搜尋策略也很重要：

*   **Greedy Search (貪婪搜尋)**：
    *   每次都只選機率最高的那個字。
    *   *優點*：速度快、穩定。
    *   *缺點*：容易陷入局部最佳解，生成的句子可能缺乏創意或重複。
*   **Beam Search (束搜尋)**：
    *   每次保留前 N 個 (Beam Width) 可能性最高的「路徑」，走到最後再選總分最高的。
    *   *優點*：生成的句子通常比 Greedy Search 更通順、品質更好。
    *   *缺點*：運算量大，速度較慢。
    *   *注意*：在現代 LLM (如 GPT-4) 中，通常預設使用 Sampling (Temperature/Top-P) 而非 Beam Search，因為 Sampling 更能產生多樣化的內容。


## 官方學習指引補充：生成式 AI 應用領域與工具使用

生成式 AI 是人工智慧的一個重要分支，其核心特徵在於透過模型的學習能力生成新內容，而非僅僅分析或辨識現有數據。這種能力不僅在技術層面帶來突破，也為多領域應用和市場價值創造了豐富的可能性。

隨著 ChatGPT 於 2022 年 11 月正式向公眾推出後，生成式 AI 掀起了一波重大的科技革命浪潮，不僅徹底改變了人類與機器互動的方式，更廣泛應用在不同領域，為各行各業帶來前所未有的創新契機。

### 1. 生成式 AI 的技術架構與關鍵特徵

生成式 AI 的基本概念為人工智慧的一個核心領域，專注於透過深度學習和大數據集的訓練來生成新的內容，而非僅僅分析或辨識現有數據。它通常基於生成對抗網路 (Generative Adversarial Network, GAN) {#sec-gan}、變分自編碼器 (Variational Autoencoder, VAE) {#sec-vae} 以及基於變換器 (Transformer) 架構的模型來執行其任務。以下是生成式 AI 的技術架構及其關鍵特徵：

#### （1） 深度學習網路 (Deep Learning Networks)
*   **多層神經網路 (Multi-layer Neural Network)**：使用多層神經網路進行特徵提取與表示學習，有助於從數據中提取深層特徵。
*   **注意力機制 (Attention Mechanism)**：尤其是自注意力 (Self-Attention)，有助於處理長距離依賴關係，並有效學習序列數據的內在結構。

#### （2） 訓練數據處理 (Training Data Processing)
*   **數據清洗 (Data Cleaning)**：移除雜訊 (Noise) 或錯誤的數據，並填補遺缺值 (Missing Value)，以保證數據的品質與一致性。
*   **標記化處理 (Tokenization)**：將文本數據拆分為基本單元（例如詞或子詞），以便深度學習模型進行處理。
*   **向量化表示 (Vectorization)**：將文本或其他數據轉換為數值形式，從而適應深度學習模型的需求。

#### （3） 推理機制 (Inference Mechanism)
*   **溫度參數 (Temperature Parameter)**：控制生成內容的隨機性，低溫度值會生成較保守的內容，高溫度值則生成更具創意的內容。
*   **頂部採樣 (Top-k Sampling)**：選擇生成機率最高的前 k 個選項來生成內容，保證品質與多樣性。
*   **核採樣 (Nucleus Sampling)**：選擇累積機率達到某一閾值（如 0.9）的選項進行採樣，以更靈活地平衡內容品質與隨機性。

生成式 AI 具備多項關鍵特點，包括強大的上下文理解能力、遷移學習特性、多模態處理支持，以及透過提示詞進行可控生成。然而，在實際應用中也面臨諸多挑戰，如大量計算資源需求、模型訓練和部署的硬體限制、輸出內容的準確性保證、 AI 幻覺 (AI Hallucinations) {#sec-ai-hallucinations} 問題的防範，以及偏見與安全性等考量。為應對這些挑戰，技術持續朝著多個方向演進：在模型效率方面，致力於模型壓縮、量化和推理加速；在架構創新上，發展混合注意力機制和模塊化設計；在應用擴展上，探索領域特定微調和多模態融合。

### 2. 生成式 AI 的市場價值與影響力

生成式 AI 的市場價值與影響力正以驚人的速度增長，並在全球各行各業中發揮出極大的潛力。其市場發展可分為以下幾個關鍵層面：

*   **市場規模與增長趨勢**：市場規模預計將在 2030 年達到數百億美元，涉及領域包括娛樂、醫療、教育、廣告、遊戲設計等。
*   **創業與投資熱潮**：驅動著垂直領域應用開發、工具平台建設以及安全隱私解決方案的創新。
*   **市場發展趨勢**：市場整合加速、商業模式創新（如訂閱制、客製化解決方案）、永續發展考量。
*   **挑戰與風險**：
    *   技術層面：資料安全、模型可靠性和系統穩定性。
    *   商業層面：投資回報的不確定性、市場競爭加劇及法規要求增高。
    *   社會層面：就業結構變動、數位落差及倫理道德問題。
*   **產業轉型影響**：推動生產力的大幅提升，顯著提高自動化程度。
*   **就業市場變革**：部分重複性工作被 AI 取代，同時湧現新興職務（如 AI 訓練師、提示工程師）。
*   **經濟效益分析**：降低營運成本、促進創新、帶動 AI 硬體和雲端服務發展。
*   **社會影響層面**：
    *   教育領域：個人化學習、優化學習評估。
    *   醫療健康：輔助診斷、加速藥物研發。
    *   創意產業：內容創作革新、設計流程優化。

### 3. 生成式 AI 工具的發展方向

生成式 AI 工具的技術進化不僅呈現了過去幾年來關鍵技術的突破，還在應用層面帶來了巨大的變革。

#### （1） 生成式 AI 技術突破
*   **生成對抗網路 (GAN)**：引領了高品質圖像生成的潮流。
*   **變分自編碼器 (VAE) 和流式模型 (Flow-based Generative Model)**：提供穩定性和機率生成方法。
*   **Transformer 架構與自注意力機制**：徹底改變了語言生成的方式，並支持大規模的多模態生成。
*   **預訓練與模型微調技術**：如少樣本學習 (Few-shot Learning) 和提示工程 (Prompt Engineering) 提升適應性。加上人類回饋強化學習 (Reinforcement Learning from Human Feedback, RLHF)，使生成結果更貼近用戶需求。
*   **高效推理與模型壓縮**：如 vLLM 架構，適用於邊緣計算和移動設備。

#### （2） 生成式 AI 工具的發展方向
*   **模型規模與能力提升**：大型語言模型 (LLM) 提升準確度，多模態生成結合文本、圖像、音訊（如 Midjourney、DALL-E）。
*   **輕量化與個人化發展**：模型壓縮與量化 (Model Compression and Quantization)，開發資源需求較低且可客製化的工具。
*   **深層學習架構的改進**：GAN 與擴散模型 (Diffusion Models) 的融合技術，提升品質和精度。
*   **開放原始碼與社群合作**：如 Hugging Face 提供了開源資源，加速整合與創新。

### 4. 生成式 AI 的應用趨勢

生成式 AI 工具逐步滲透至各行各業，並在應用層面與技術層面展現出明顯趨勢：

*   **專業化與垂直整合**：針對特定產業（法律、醫療、金融、教育）深度優化。
*   **多模態整合與協同生成**：文字、圖像、語音、影片等多模態內容協同生成（如 Whisper 語音轉文字）。
*   **AI 即服務 (AI as a Service, AIaaS)**：透過雲端平台 (如 OpenAI API) 存取高效能 AI 工具，降低使用門檻。
*   **個人化生成與可控性提升**：透過模型微調 (Fine-tuning) 與提示工程 (Prompt Engineering) 增強控制權。
*   **協作與即時回饋機制**：即時回饋與迭代式內容優化，增強團隊協作效率。
*   **安全性與隱私保護**：本地部署、資料加密與隱私保護模式。
*   **效能優化與資源效率**：模型壓縮 (Model Compression) 與量化 (Quantization) 技術。
*   **道德與法律規範**：內容版權管理、防範濫用（如深偽影像 Deepfake）、法規遵循。

### 5. 生成式 AI 在各產業的應用實例

*   **藝術與設計 / 內容創作**：協助激發靈感、自動生成背景音樂與旋律。
*   **醫療與生物科技**：生成潛在藥物分子結構、醫學影像分析、個人化醫療。
*   **教育與培訓**：自動生成教學內容、個人化學習路徑、互動式教材。
*   **娛樂與媒體**：遊戲地圖生成、劇本構思、驅動虛擬角色。
*   **產品設計與製造**：生成式設計優化外觀與結構、快速原型製作、供應鏈管理預測。
