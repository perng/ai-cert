# 模型評估與效能優化

訓練完模型只是第一步，更重要的是知道它「好不好用」。如果沒有正確的評估，你可能會把一個只會死記硬背的模型誤認為天才。

## 9.1 評估流程與指標 {#sec-evaluation-metrics}

### 資料集劃分 {#sec-data-split}

為了考試公平，我們不能拿「練習題」來當「期末考題」。
*   **訓練集 (Training Set)**：課本。用來訓練模型。
*   **驗證集 (Validation Set)**：模擬考。用來調整參數（如學習率、樹的深度），挑選最佳模型。
*   **測試集 (Test Set)**：期末考。考完就定案了，用來評估最終效能。絕對不能偷看！

### K-fold 交叉驗證 (Cross-Validation) {#sec-cross-validation}

如果資料很少，切成三份太浪費怎麼辦？
*   **做法**：將資料切成 $K$ 等份（例如 5 份）。輪流拿其中 1 份當驗證集，剩下 4 份當訓練集。跑 5 次後取平均分數。
*   **優點**：每一筆資料都被當過驗證集，評估結果更客觀穩健。

### 分類指標 (Classification Metrics) {#sec-classification-metrics}

*   **混淆矩陣 (Confusion Matrix)**：
    *   **TP (True Positive)**：有病，判斷有病 (O)。
    *   **TN (True Negative)**：沒病，判斷沒病 (O)。
    *   **FP (False Positive)**：沒病，判斷有病 (X) -> 誤報 (Type I Error)。
    *   **FN (False Negative)**：有病，判斷沒病 (X) -> 漏報 (Type II Error)。
*   **準確率 (Accuracy)**：答對的比例。 $(TP+TN) / All$。
    *   **陷阱**：如果 99% 的人沒病，模型全部猜「沒病」，準確率也有 99%，但完全沒用。
*   **精確率 (Precision)**：在所有被判斷為有病的人中，真的有病的比例。 $TP / (TP+FP)$。
    *   **應用**：垃圾郵件過濾（寧可漏抓，也不要誤把重要信件當垃圾信）。
*   **召回率 (Recall)**：在所有真的有病的人中，被成功抓出來的比例。 $TP / (TP+FN)$。
    *   **應用**：癌症篩檢（寧可誤判複檢，也不能漏掉任何一個病人）。
*   **F1-Score**：Precision 和 Recall 的調和平均數。兩者兼顧。
*   **AUC-ROC 曲線**：評估模型在不同閾值下的表現。AUC (Area Under Curve) 面積越大（越接近 1）越好。

### 迴歸指標 (Regression Metrics) {#sec-regression-metrics}

*   **均方誤差 (MSE, Mean Squared Error)**：誤差平方的平均。
    *   **特點**：會放大極端誤差（因為平方）。如果很在意大錯，就看這個。
*   **平均絕對誤差 (MAE, Mean Absolute Error)**：誤差絕對值的平均。
    *   **特點**：對離群值較不敏感，解釋直觀（平均差幾分）。

## 9.2 誤差分析與正則化 {#sec-error-analysis}

### 偏差-變異權衡 (Bias-Variance Tradeoff) {#sec-bias-variance}

*   **偏差 (Bias)**：模型準不準？
    *   **高偏差 (High Bias)**：模型太簡單，學不會資料的規律。稱為**欠擬合 (Underfitting)**。
*   **變異 (Variance)**：模型穩不穩？
    *   **高變異 (High Variance)**：模型太複雜，把雜訊也學進去了，換個資料集表現就大起大落。稱為**過擬合 (Overfitting)**。

### 防止過擬合技術 {#sec-prevent-overfitting}

*   **正則化 (Regularization)**：
    *   **L1 (Lasso)** / **L2 (Ridge)**：在損失函數加懲罰項，限制權重大小（參見 5.2 節）。
*   **Dropout**：
    *   在訓練神經網路時，隨機「關掉」一些神經元。這強迫網路不能依賴特定的神經元，必須學會更強健的特徵（像軍隊演習時隨機抽走指揮官，訓練部隊的應變能力）。
*   **早停 (Early Stopping)**：
    *   觀察驗證集的誤差。如果訓練集的誤差還在降，但驗證集的誤差開始上升，代表開始過擬合了，立刻停止訓練。
*   **資料增強 (Data Augmentation)**：
    *   如果資料不夠，就自己造！把圖片旋轉、裁切、調亮，產生更多訓練資料。
