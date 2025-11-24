# 神經網路架構演進

深度學習 (Deep Learning) 是機器學習的一個分支，靈感來自人類大腦的神經元運作方式。從簡單的感知機到如今強大的 Transformer，神經網路架構經歷了數十年的演進。

## 7.1 基礎神經網路 {#sec-basic-nn}

### 多層感知機 (MLP, Multi-Layer Perceptron) {#sec-mlp}

*   **結構**：由輸入層、隱藏層（可以多層）和輸出層組成。每一層的神經元都與下一層的所有神經元相連（全連接）。
*   **運作**：輸入訊號經過權重 (Weight) 加權求和，再加上偏差 (Bias)，最後通過啟動函數輸出。

### 啟動函數 (Activation Functions) {#sec-activation-functions}

如果沒有啟動函數，神經網路不管有幾層，本質上都只是線性變換，無法解決複雜問題。啟動函數引入了**非線性**。

*   **Sigmoid / Tanh**：早期的啟動函數，將數值壓縮到 (0, 1) 或 (-1, 1)。缺點是容易導致**梯度消失 (Vanishing Gradient)**，讓深層網路無法訓練。
*   **ReLU (Rectified Linear Unit)**：$f(x) = \max(0, x)$。負數變 0，正數不變。計算簡單且有效解決了梯度消失問題，是目前最常用的啟動函數。

### 前向傳播與反向傳播 (Backpropagation) {#sec-backpropagation}

*   **前向傳播 (Forward Propagation)**：資料從輸入層一路算到輸出層，得到預測結果。
*   **反向傳播 (Backpropagation)**：比較預測結果與真實答案的誤差，將誤差**從後往前**傳遞，告訴每一層的權重該如何調整，以減少誤差。這是神經網路學習的核心機制。

### 優化器 (Optimizer) {#sec-optimizer}

決定如何更新權重的演算法。
*   **SGD (Stochastic Gradient Descent)**：隨機梯度下降。像下山一樣，每次走一步，方向是目前最陡的下坡。
*   **Adam**：結合了動量 (Momentum) 的概念。像滾動的球，會有慣性，能更快收斂且不易卡在局部最佳解。

## 7.2 經典深度架構 {#sec-deep-architectures}

### 卷積神經網路 (CNN, Convolutional Neural Networks) {#sec-cnn}

*   **專長**：影像辨識、電腦視覺。
*   **靈感**：人類視覺皮層對邊緣、形狀的反應。
*   **關鍵元件**：
    *   **卷積層 (Convolution Layer)**：使用**濾鏡 (Filter)** 在圖片上滑動，提取特徵（如線條、邊緣）。
    *   **池化層 (Pooling Layer)**：將圖片縮小（如取 2x2 區域的最大值），減少運算量並保留重要特徵（就像瞇著眼睛看東西）。
*   **應用**：人臉辨識、醫療影像分析、自駕車視覺。

### 循環神經網路 (RNN, Recurrent Neural Networks) {#sec-rnn}

*   **專長**：序列數據（文字、語音、股票）。
*   **特點**：具有**記憶**功能。上一步的輸出會變成這一步的輸入。
*   **問題**：對於太長的序列，記憶會淡忘（梯度消失）。
*   **改進版**：
    *   **LSTM (Long Short-Term Memory)**：設計了精巧的「門控」機制（遺忘門、輸入門、輸出門），決定什麼該記、什麼該忘。
    *   **GRU**：LSTM 的簡化版，效能接近但計算更快。

## 7.3 Transformer 與注意力機制 {#sec-transformer}

2017 年 Google 發表論文《Attention Is All You Need》，徹底改變了 NLP 領域。

### 自注意力機制 (Self-Attention) {#sec-self-attention}

*   **概念**：在處理一個句子時，模型會計算每個字與其他所有字的關聯性。
*   **例子**："The animal didn't cross the street because **it** was too tired."
    *   當模型看到 "it" 時，Attention 機制會告訴它，這個 "it" 與 "animal" 的關聯性最強，而不是 "street"。

### Transformer 架構優勢 {#sec-transformer-arch}

*   **並行計算**：不像 RNN 必須一個字一個字讀，Transformer 可以一次讀入整篇文章，利用 GPU 平行運算，訓練速度大幅提升。
*   **編碼器-解碼器 (Encoder-Decoder)**：
    *   **Encoder**：理解輸入（如閱讀英文句子）。
    *   **Decoder**：生成輸出（如翻譯成中文）。
    *   BERT 使用 Encoder，GPT 使用 Decoder。
*   **代價**：計算複雜度隨著序列長度平方成長 ($O(N^2)$)，處理超長文本極耗資源。
