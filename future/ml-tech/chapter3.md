# 第 3 章：深度學習架構

本章探討現代深度學習的核心架構：CNN, RNN 與 Transformer。

## 3.1 卷積神經網路 (CNN)

### 3.1.1 卷積層 (Convolutional Layer)

*   **功能**：自動提取輸入影像中的**局部特徵** (A)。
*   **優勢**：相較於全連接網路 (FCNN)，CNN 透過**區域感知 (Local Receptive Field)** 與**參數共享 (Parameter Sharing)**，大幅降低參數量與運算複雜度 (C)。

### 3.1.2 VGG16 架構分析

*   **參數量 (Parameters)**：
    *   **全連接層 (Linear)** 參數量最多 (B)。例如 VGG16 第一個 FC 層連接 7x7x512 的特徵圖到 4096 個神經元，參數極大。
*   **運算量 (FLOPs)**：
    *   **卷積層 (Conv2d)** 運算量最多 (A)。因為要在整張圖上滑動視窗進行乘加運算。
*   **架構細節**：
    *   VGG16 包含 13 層 Conv 與 3 層 FC，總參數約 138M (D)。
    *   池化層輸出通常會被 Flatten，VGG最後一層池化輸出為 7x7 (非 4x4)，輸入 FC 層維度為 512x7x7 = 25088。

### 3.1.3 遷移學習 (Transfer Learning)

*   **實作**：凍結特徵提取層，僅訓練分類器。
*   **程式碼**：
    *   遍歷 `model.features.parameters()` 並設 `requires_grad = False`。
    *   重新定義 `model.classifier` (B)。

## 3.2 循環神經網路 (RNN) & LSTM

*   **LSTM (Long Short-Term Memory)**：
    *   **適用情境**：處理序列資料，如預測未來七天的電力需求趨勢 (A)。
    *   解決傳統 RNN 的梯度消失問題。

## 3.3 Transformer

### 3.3.1 多頭注意力 (Multi-head Attention)

*   **優點**：能從**不同表示子空間 (Representation Subspaces)** 同時捕捉多樣化的關聯資訊 (C)。
*   讓模型能同時關注語音/文字的不同特徵 (如語速、語意)。

## 3.4 激活函數 (Activation Function)

*   **ReLU (Rectified Linear Unit)**：
    *   解決梯度消失，加速收斂。
    *   若使用線性激活函數導致準確率停滯，應改用 **ReLU** 以引入非線性 (D)。
*   **Sigmoid**：$\frac{1}{1+e^{-x}}$，用於二元分類輸出。
*   **Keras 實作**：
    *   `Dense(10)`：Param = (Input+1)*10。若 Input=9，Param=100。
    *   `Dense(1)`：Param = (10+1)*1 = 11。
    *   題目圖表：Input=9 -> Dense(10) Param=100; Dense(10) Param=110 (C)。
