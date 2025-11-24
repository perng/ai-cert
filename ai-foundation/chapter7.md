# 神經網路架構演進 (Neural Network Architecture Evolution)

深度學習 (Deep Learning) 是機器學習的一個分支，靈感來自人類大腦的神經元運作方式。從簡單的感知機到如今強大的 Transformer，神經網路架構經歷了數十年的演進，每一次的突破都帶來了 AI 能力的飛躍。

## 7.1 基礎神經網路 {#sec-basic-nn}

### 多層感知機 (MLP, Multi-Layer Perceptron) {#sec-mlp}

這是最基礎的深度學習架構，也稱為全連接網路 (Fully Connected Network)。

*   **結構**：
    1.  **輸入層 (Input Layer)**：接收原始資料（如圖片的像素值）。
    2.  **隱藏層 (Hidden Layers)**：中間的黑盒子，負責提取特徵。層數越多，能學到的特徵越抽象、越複雜。
    3.  **輸出層 (Output Layer)**：給出最終預測（如分類機率）。
*   **運作原理**：每個神經元接收上一層的訊號，乘上**權重 (Weight)**，加上**偏差 (Bias)**，最後通過**啟動函數**輸出給下一層。
    *   **公式**：$$ y = \sigma(\sum_{i=1}^{n} w_i x_i + b) $$
        *   $x_i$: 輸入訊號
        *   $w_i$: 權重 (Weight)，代表該輸入的重要性
        *   $b$: 偏差 (Bias)，調整啟動門檻
        *   $\sigma$: 啟動函數 (Activation Function)

### 啟動函數 (Activation Functions) {#sec-activation-functions}

如果沒有啟動函數，神經網路不管有幾層，本質上都只是線性變換（矩陣相乘），無法解決複雜的非線性問題（如分類貓和狗）。啟動函數引入了**非線性**。

*   **Sigmoid**：
    *   **公式**：$$ f(x) = \frac{1}{1 + e^{-x}} $$
    *   **特性**：將數值壓縮到 $(0, 1)$ 之間。
    *   **缺點**：容易導致**梯度消失 (Vanishing Gradient)**，即在深層網路中，誤差訊號傳不回去，導致前面的層學不到東西。
*   **ReLU (Rectified Linear Unit)**：
    *   **公式**：$$ f(x) = \max(0, x) $$
    *   **特性**：負數變 0，正數不變。
    *   **優點**：計算極快，且有效解決了梯度消失問題。是目前最常用的啟動函數。
*   **Softmax**：
    *   **公式**：$$ P(y=j) = \frac{e^{z_j}}{\sum_{k=1}^{K} e^{z_k}} $$
    *   **特性**：通常用於**輸出層**。將一組數值轉換為**機率分佈**（總和為 1）。例如：[貓: 0.8, 狗: 0.1, 鳥: 0.1]。

### 反向傳播 (Backpropagation) 與優化器 {#sec-backpropagation}

神經網路是如何「學習」的？

1.  **前向傳播 (Forward)**：資料從輸入算到輸出，得到預測值。
2.  **計算損失 (Loss)**：比較預測值與真實答案的差距（誤差）。
3.  **反向傳播 (Backward)**：利用**連鎖律 (Chain Rule)**，將誤差**從後往前**傳遞，計算每個權重對誤差的貢獻（梯度）。
4.  **更新權重 (Update)**：利用**優化器 (Optimizer)** 調整權重，讓誤差變小。

**常見優化器**：
*   **SGD (Stochastic Gradient Descent)**：隨機梯度下降。像下山一樣，每次走一步，方向是目前最陡的下坡。
*   **Adam**：結合了動量 (Momentum) 的概念。像滾動的球，會有慣性，能更快收斂且不易卡在局部最佳解。

## 7.2 經典深度架構 {#sec-deep-architectures}

### 卷積神經網路 (CNN, Convolutional Neural Networks) {#sec-cnn}

*   **專長**：**影像辨識**、電腦視覺 (CV)。
*   **靈感**：人類視覺皮層對邊緣、形狀的反應。我們看東西不是一個像素一個像素看，而是看特徵（線條、圓圈、眼睛、鼻子）。
*   **關鍵元件**：
    *   **卷積層 (Convolution Layer)**：使用**濾鏡 (Filter)** 在圖片上滑動，提取局部特徵（如垂直線、水平線）。
    *   **池化層 (Pooling Layer)**：將圖片縮小（如 Max Pooling 取 2x2 區域的最大值）。
        *   *目的*：減少運算量，並保留最顯著的特徵（就像瞇著眼睛看東西，只看大輪廓）。
*   **應用**：人臉辨識、醫療影像分析 (X光/MRI)、自駕車視覺系統。

### 循環神經網路 (RNN, Recurrent Neural Networks) {#sec-rnn}

*   **專長**：**序列數據**（文字、語音、股票走勢）。
*   **特點**：具有**記憶**功能。神經元會把上一步的輸出 ($h_{t-1}$)，跟這一步的輸入 ($x_t$) 一起處理。
*   **致命傷**：**短期記憶**。對於太長的序列（如長篇文章），前面的資訊傳到後面早就忘光了（梯度消失）。
*   **救星：LSTM (Long Short-Term Memory)**：
    *   設計了精巧的「門控」機制（遺忘門、輸入門、輸出門），像水庫的閘門一樣，主動決定什麼該記、什麼該忘。
    *   *應用*：Google 翻譯（早期版本）、語音辨識 (Siri)。

## 7.3 Transformer 與注意力機制 {#sec-transformer}

2017 年 Google 發表論文《Attention Is All You Need》，徹底改變了 NLP 領域，也開啟了大型語言模型 (LLM) 的時代。

### 自注意力機制 (Self-Attention) {#sec-self-attention}

*   **核心概念**：在處理一個句子時，模型會計算每個字與其他所有字的**關聯強度 (Attention Score)**。
*   **數學公式**：
    $$ Attention(Q, K, V) = softmax(\frac{QK^T}{\sqrt{d_k}})V $$
    *   **Q (Query)**：查詢向量（我想找什麼？）
    *   **K (Key)**：鍵值向量（你是什麼？）
    *   **V (Value)**：數值向量（你的內容是什麼？）
    *   *類比*：你在圖書館找書。Q 是你的關鍵字，K 是書背上的標籤，V 是書的內容。算出 Q 和 K 的相似度，決定要拿出哪些 V。

*   **例子**："The animal didn't cross the street because **it** was too tired."
    *   當模型讀到 "**it**" 時，Attention 機制會告訴它，這個 "it" 與 "**animal**" 的關聯性最強（Attention Score 最高），而不是 "street"。這讓模型真正「讀懂」了代名詞的指涉。

### Transformer 架構優勢 {#sec-transformer-arch}

1.  **並行計算 (Parallelization)**：
    *   RNN 必須一個字一個字讀（讀完第一個字才能讀第二個），無法平行化。
    *   Transformer 可以**一次讀入整篇文章**，利用 GPU 的強大平行運算能力，訓練速度大幅提升。這使得訓練像 GPT-4 這種超巨大模型成為可能。
2.  **長距離依賴 (Long-range Dependency)**：
    *   透過 Attention，無論兩個字距離多遠，都能直接建立關聯，不再有 LSTM 的記憶長度限制。

### Encoder 與 Decoder 家族

Transformer 由 Encoder（編碼器）和 Decoder（解碼器）組成，後來衍生出三大流派：

1.  **Encoder-only (如 BERT)**：
    *   擅長「理解」文本。
    *   *應用*：情感分析、分類、問答系統。
2.  **Decoder-only (如 GPT 系列)**：
    *   擅長「生成」文本。像接龍一樣，預測下一個字。
    *   *應用*：聊天機器人、文章寫作、程式碼生成。
3.  **Encoder-Decoder (如 T5, Bart)**：
    *   同時具備理解與生成能力。
    *   *應用*：機器翻譯（英文入 $\to$ 理解 $\to$ 生成 $\to$ 中文出）、摘要生成。

## 本章總結與考點提示 {#sec-chapter7-summary}

### 核心概念回顧

深度學習是 AI 的核心引擎。

*   **基礎元件**：
    *   **MLP**：全連接，基礎結構。
    *   **Activation**：ReLU (防梯度消失)、Sigmoid (二元分類)、Softmax (多類別)。
    *   **Backpropagation**：誤差反向傳播，更新權重。
*   **三大架構**：
    *   **CNN**：影像霸主。卷積 (特徵) + 池化 (降維)。
    *   **RNN/LSTM**：序列專家。有記憶，但怕長序列 (梯度消失)。
    *   **Transformer**：NLP 新皇。Self-Attention (平行運算、長距離依賴)。

### AI 應用規劃師認證考點

**常考題型與解題策略**：

1.  **架構對應題**：
    *   *例題*：「人臉辨識系統通常使用哪種架構？」
    *   **解答**：CNN。
    *   *例題*：「股價預測或語音辨識通常使用哪種架構？」
    *   **解答**：RNN 或 LSTM。
    *   *例題*：「ChatGPT 是基於哪種架構？」
    *   **解答**：Transformer。

2.  **功能題**：
    *   *例題*：「CNN 中池化層 (Pooling) 的主要功能是什麼？」
    *   **解答**：降低維度（減少運算量）並保留重要特徵。
    *   *例題*：「為什麼 LSTM 比傳統 RNN 好？」
    *   **解答**：解決了梯度消失問題，能記住更長的序列。

3.  **啟動函數題**：
    *   *例題*：「目前最常用的隱藏層啟動函數是什麼？」
    *   **解答**：ReLU。因為計算快且無梯度消失問題。

### 記憶口訣

*   **CNN**：「看圖」（卷積）。
*   **RNN**：「讀書」（序列）。
*   **Transformer**：「劃重點」（Attention）。

### 延伸思考

*   為什麼 Transformer 可以取代 RNN？（因為它可以平行運算，速度快很多，且 Attention 機制解決了長距離記憶問題）。

