# 生成式 AI 與大型語言模型 (Generative AI & LLM)

生成式 AI (Generative AI) 不再只是分析既有資料（如分類貓狗），而是能**創造**出全新的內容。從寫詩、繪畫到寫程式，它正在重塑創意產業。

## 8.1 生成式模型原理 {#sec-generative-models}

### 變分自編碼器 (VAE, Variational Autoencoder) {#sec-vae}

*   **核心概念**：將資料壓縮到一個機率分佈（潛在空間 Latent Space），然後從這個分佈中隨機採樣，解碼出新的資料。
*   **運作**：
    1.  **Encoder**：將圖片壓縮成兩個向量：平均值 $\mu$ 和標準差 $\sigma$。
    2.  **Sampling**：從常態分佈 $N(\mu, \sigma)$ 中抽樣出一個點 $z$。
    3.  **Decoder**：將 $z$ 還原成圖片。
*   **特點**：生成的圖像較模糊，但數學理論紮實，且潛在空間連續（可以做平滑的漸變效果）。

### 生成對抗網路 (GAN, Generative Adversarial Network) {#sec-gan}

*   **核心概念**：兩個神經網路在打架（零和賽局）。
    *   **生成器 (Generator, G)**：負責偽造假鈔（生成假圖片）。目標是騙過判別器。
    *   **判別器 (Discriminator, D)**：負責分辨真鈔與假鈔（分辨真圖與假圖）。目標是抓出生成器。
*   **訓練過程**：
    1.  G 生成假圖。
    2.  D 判斷這張圖是真的還是假的。
    3.  如果 D 抓到了，G 就修正自己變得更強；如果 D 被騙了，D 就修正自己變得更嚴格。
    4.  最終達到**納許均衡 (Nash Equilibrium)**：G 生成的圖逼真到 D 只能瞎猜（機率 0.5）。
*   **特點**：生成的圖像極度逼真，但訓練不穩定（容易模式崩潰 Mode Collapse，即 G 只會生成同一種圖）。

### 擴散模型 (Diffusion Models) {#sec-diffusion}

*   **核心概念**：學習如何「破壞」一張圖，然後反過來學習如何「修復」它。
*   **流程**：
    1.  **前向擴散 (Forward Diffusion)**：在一張清晰的圖片上，一步步加入高斯雜訊，直到它變成完全的雜訊圖。
    2.  **逆向擴散 (Reverse Diffusion)**：訓練一個神經網路（通常是 U-Net），學習如何預測並**減去**雜訊，從雜訊中還原出清晰的影像。
*   **代表作**：Stable Diffusion, Midjourney, DALL-E。
*   **特點**：生成品質極高，多樣性好，是目前 AI 繪圖的主流技術。

## 8.2 大型語言模型 (LLM) 技術 {#sec-llm-tech}

LLM (Large Language Model) 如 GPT 系列，本質上是一個超巨大的「文字接龍」機器。

### 預訓練與微調 (Pre-training & Fine-tuning) {#sec-pretrain-finetune}

1.  **預訓練 (Pre-training)**：**通識教育**。
    *   讓模型閱讀網際網路上數兆字的文本（Wikipedia, 書籍, 程式碼）。
    *   **目標**：預測下一個字 (Next Token Prediction)。
    *   *成果*：模型學會了文法、世界知識、邏輯推理，但還不懂得如何當個好助手（可能會講髒話或續寫小說）。
    *   *成本*：耗資巨大（數百萬美金，數千張 GPU）。
2.  **微調 (Fine-tuning)**：**職前訓練**。
    *   **指令微調 (Instruction Tuning)**：使用高品質的「問題-答案」對，教導模型如何聽懂指令並給出有用的回答。
    *   **RLHF (Reinforcement Learning from Human Feedback)**：讓人類對模型的回答評分（按讚/按倒讚），用強化學習來調整模型，使其更符合人類價值觀（有用、誠實、無害）。

### Scaling Laws (擴展定律) {#sec-scaling-laws}

*   **觀察**：OpenAI 發現，模型的性能與三個因素呈**冪律 (Power Law)** 關係：
    1.  **參數量 (Parameters)**：模型腦容量。
    2.  **資料量 (Data Size)**：讀了多少書。
    3.  **計算量 (Compute)**：訓練用了多少 GPU 時間。
*   **啟示**：只要持續擴大這三者，AI 就會變強。這引發了科技巨頭的軍備競賽。

### 提示工程 (Prompt Engineering) {#sec-prompt-engineering}

既然我們無法輕易重新訓練模型，那就改變我們問問題的方式。

*   **Zero-shot**：直接問，不給範例。「將這句話翻譯成法文：...」
*   **Few-shot Prompting**：給幾個範例 (Example)，讓模型模仿。「將這句話翻譯成法文。例如：Hello -> Bonjour。Good morning -> Bonjour。現在翻譯：Good night ->」
*   **Chain-of-Thought (CoT)**：要求模型「一步步思考 (Let's think step by step)」。這能顯著提升模型解決數學或邏輯問題的能力。

## 8.3 LLM 優化與應用架構 {#sec-llm-optimization}

### 檢索增強生成 (RAG, Retrieval-Augmented Generation) {#sec-rag}

*   **痛點**：LLM 有**幻覺 (Hallucination)**（一本正經胡說八道），且知識截止於訓練時間（不知道昨天發生的新聞）。
*   **解法**：考試時允許「開書考」。
    1.  **檢索 (Retrieve)**：當使用者問問題時，系統先去外部知識庫（如公司文件、Google 搜尋）找相關資料。
    2.  **增強 (Augment)**：將找到的資料連同使用者的問題，組合成一個 Prompt：「請根據以下資料回答問題...」。
    3.  **生成 (Generate)**：LLM 根據參考資料回答問題。
*   **優勢**：資料即時更新，回答有憑有據，且不需要重新訓練模型。

### 模型壓縮 (Model Compression) {#sec-model-compression}

為了讓 LLM 能在手機或較小的伺服器上跑：

*   **量化 (Quantization)**：
    *   降低數值的精確度。
    *   從 32-bit 浮點數 (FP32) 降到 8-bit 整數 (INT8) 甚至 4-bit。
    *   *效果*：模型體積縮小 4-8 倍，速度變快，記憶體需求大減，且對準確率影響微乎其微。
*   **知識蒸餾 (Knowledge Distillation)**：
    *   讓一個大模型（老師）教導一個小模型（學生）。
    *   學生不僅學習正確答案，還學習老師的「機率分佈」（老師對每個選項的信心）。
    *   *效果*：小模型能達到接近大模型的效能，但速度快得多。
