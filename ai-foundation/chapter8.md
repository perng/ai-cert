# 生成式 AI 與大型語言模型 (LLM)

生成式 AI (Generative AI) 不再只是分析既有資料，而是能創造出全新的內容。從寫詩、繪畫到寫程式，它正在重塑創意產業。

## 8.1 生成式模型原理 {#sec-generative-models}

### 變分自編碼器 (VAE, Variational Autoencoder) {#sec-vae}

*   **概念**：將資料壓縮到一個機率分佈（潛在空間），然後從這個分佈中隨機採樣，解碼出新的資料。
*   **特點**：生成的圖像較模糊，但數學理論紮實。

### 生成對抗網路 (GAN, Generative Adversarial Network) {#sec-gan}

*   **概念**：兩個神經網路在打架。
    *   **生成器 (Generator)**：負責偽造假鈔（生成假圖片）。
    *   **判別器 (Discriminator)**：負責分辨真鈔與假鈔（分辨真圖與假圖）。
    *   兩者互相競爭，最後生成器強到連判別器都分不出來。
*   **特點**：生成的圖像極度逼真，但訓練不穩定（容易模式崩潰）。

### 擴散模型 (Diffusion Models) {#sec-diffusion}

*   **概念**：學習如何「破壞」一張圖（加雜訊），然後反過來學習如何「修復」它（去雜訊）。
*   **流程**：從一張全是雜訊的圖開始，一步步去除雜訊，最後浮現出清晰的影像。
*   **代表作**：Stable Diffusion, Midjourney, DALL-E。
*   **特點**：生成品質極高，多樣性好，是目前 AI 繪圖的主流技術。

## 8.2 大型語言模型 (LLM) 技術 {#sec-llm-tech}

LLM (Large Language Model) 如 GPT 系列，本質上是一個超巨大的「文字接龍」機器。

### 預訓練與微調 (Pre-training & Fine-tuning) {#sec-pretrain-finetune}

*   **預訓練 (Pre-training)**：讓模型閱讀網際網路上數兆字的文本，學習語言的文法、知識和邏輯。這階段耗資巨大（數百萬美金）。
    *   **目標**：預測下一個字。
*   **微調 (Fine-tuning)**：使用高品質的問答資料，教導模型如何聽懂指令並給出有用的回答（Instruction Tuning）。

### Scaling Laws (擴展定律) {#sec-scaling-laws}

*   **觀察**：模型的參數越多、訓練資料越多、計算量越大，模型的性能就會**可預測地**提升。
*   **啟示**：這給了科技巨頭信心，只要砸錢堆算力，AI 就會變強。

### 災難性遺忘 (Catastrophic Forgetting) {#sec-catastrophic-forgetting}

*   **問題**：當模型學習新知識時，很容易忘記舊知識。
*   **解法**：重播舊資料、參數凍結等技術。

### 提示工程 (Prompt Engineering) {#sec-prompt-engineering}

*   **概念**：既然我們無法輕易重新訓練模型，那就改變我們問問題的方式。透過設計精確的提示詞 (Prompt)，引導模型輸出我們想要的結果。
*   **技巧**：
    *   **Few-shot Prompting**：給幾個範例。
    *   **Chain-of-Thought (CoT)**：要求模型「一步步思考」。

## 8.3 LLM 優化與應用架構 {#sec-llm-optimization}

### 檢索增強生成 (RAG, Retrieval-Augmented Generation) {#sec-rag}

*   **問題**：LLM 會有**幻覺 (Hallucination)**（一本正經胡說八道），且知識截止於訓練時間。
*   **解法**：考試時允許「開書考」。
    1.  **檢索 (Retrieve)**：先去外部知識庫（如公司文件、Google 搜尋）找相關資料。
    2.  **增強 (Augment)**：將找到的資料連同使用者的問題一起餵給 LLM。
    3.  **生成 (Generate)**：LLM 根據參考資料回答問題。
*   **優勢**：資料即時更新，回答有憑有據。

### 模型壓縮與推論優化 {#sec-model-compression}

為了讓 LLM 能在手機或較小的伺服器上跑：

*   **模型剪枝 (Pruning)**：剪掉神經網路中不重要的連接（權重接近 0 的）。
*   **量化 (Quantization)**：降低數值精度。從 32-bit 浮點數 (FP32) 降到 8-bit 整數 (INT8) 甚至 4-bit。雖然精度下降，但速度變快，記憶體需求大減，且對性能影響有限。
*   **知識蒸餾 (Knowledge Distillation)**：讓一個大模型（老師）教導一個小模型（學生），讓小模型學會大模型的行為。
