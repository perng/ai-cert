# 模型評估與效能優化 (Model Evaluation & Optimization)

訓練完模型只是第一步，更重要的是知道它「好不好用」。如果沒有正確的評估，你可能會把一個只會死記硬背的模型誤認為天才。

## 9.1 評估流程與指標 {#sec-evaluation-metrics}

### 資料集劃分 (Data Splitting) {#sec-data-split}

為了考試公平，我們不能拿「練習題」來當「期末考題」。

1.  **訓練集 (Training Set)**：**課本**。用來訓練模型，調整權重。通常佔 60-80%。
2.  **驗證集 (Validation Set)**：**模擬考**。用來調整**超參數 (Hyperparameters)**（如學習率、樹的深度），挑選最佳模型。
3.  **測試集 (Test Set)**：**期末考**。考完就定案了，用來評估最終效能。**絕對不能偷看**（不能用於訓練或調整參數）！

### K-fold 交叉驗證 (Cross-Validation) {#sec-cross-validation}

如果資料很少，切成三份太浪費怎麼辦？

*   **做法**：將資料切成 $K$ 等份（例如 $K=5$）。
    *   第 1 輪：拿第 1 份當驗證集，剩下 4 份當訓練集。
    *   第 2 輪：拿第 2 份當驗證集，剩下 4 份當訓練集。
    *   ...以此類推，跑 5 次。
*   **結果**：取 5 次評估分數的**平均值**。
*   **優點**：每一筆資料都被當過驗證集，評估結果更客觀穩健，不會因為剛好切到簡單/困難的資料而失準。

### 分類指標 (Classification Metrics) {#sec-classification-metrics}

對於二元分類問題（如：有病/沒病），我們使用**混淆矩陣 (Confusion Matrix)**：

| | 預測：有病 (Positive) | 預測：沒病 (Negative) |
|---|---|---|
| **實際：有病 (True)** | **TP** (True Positive) <br> 抓到了！(真陽性) | **FN** (False Negative) <br> 漏報！(假陰性) |
| **實際：沒病 (False)** | **FP** (False Positive) <br> 誤報！(假陽性) | **TN** (True Negative) <br> 沒事！(真陰性) |

*   **準確率 (Accuracy)**：答對的比例。
    *   $$ Accuracy = \frac{TP + TN}{TP + TN + FP + FN} $$
    *   **陷阱**：如果 99% 的人沒病，模型全部猜「沒病」，準確率也有 99%，但完全沒用（抓不到病人）。**資料不平衡時別用 Accuracy**。
*   **精確率 (Precision)**：在所有**被判斷為有病**的人中，真的有病的比例。
    *   $$ Precision = \frac{TP}{TP + FP} $$
    *   **應用**：垃圾郵件過濾（寧可漏抓，也不要誤把重要信件當垃圾信）。希望 FP 越低越好。
*   **召回率 (Recall)**：在所有**真的有病**的人中，被成功抓出來的比例。
    *   $$ Recall = \frac{TP}{TP + FN} $$
    *   **應用**：癌症篩檢、地震預警（寧可誤判複檢，也不能漏掉任何一個病人）。希望 FN 越低越好。
*   **F1-Score**：Precision 和 Recall 的調和平均數。
    *   $$ F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall} $$
    *   當需要兼顧兩者時使用。
*   **AUC-ROC 曲線**：
    *   **ROC 曲線**：描繪在不同閾值下，TPR (Recall) 與 FPR (誤報率) 的關係。
    *   **AUC (Area Under Curve)**：曲線下的面積。AUC = 0.5 代表亂猜，AUC = 1 代表完美。AUC 越接近 1 越好。

### 迴歸指標 (Regression Metrics) {#sec-regression-metrics}

*   **均方誤差 (MSE, Mean Squared Error)**：
    *   $$ MSE = \frac{1}{n} \sum (y_{true} - y_{pred})^2 $$
    *   **特點**：會放大極端誤差（因為平方）。如果很在意大錯，就看這個。
*   **平均絕對誤差 (MAE, Mean Absolute Error)**：
    *   $$ MAE = \frac{1}{n} \sum |y_{true} - y_{pred}| $$
    *   **特點**：對離群值較不敏感，解釋直觀（平均差幾分）。
*   **R-squared ($R^2$)**：
    *   衡量模型解釋了資料多少變異。1 代表完美擬合，0 代表跟用平均值猜一樣爛。

## 9.2 誤差分析與正則化 {#sec-error-analysis}

### 偏差-變異權衡 (Bias-Variance Tradeoff) {#sec-bias-variance}

*   **偏差 (Bias)**：模型準不準？（訓練集誤差）
    *   **高偏差 (High Bias)**：模型太簡單，學不會資料的規律。稱為**欠擬合 (Underfitting)**。
    *   *解法*：增加模型複雜度（加層數、加特徵）、減少正則化。
*   **變異 (Variance)**：模型穩不穩？（訓練集 vs 驗證集誤差差距）
    *   **高變異 (High Variance)**：模型太複雜，把雜訊也學進去了，導致在訓練集考 100 分，驗證集不及格。稱為**過擬合 (Overfitting)**。
    *   *解法*：增加資料量、正則化、簡化模型。

### 防止過擬合技術 (Regularization) {#sec-prevent-overfitting}

1.  **L1/L2 正則化**：在損失函數加懲罰項，限制權重大小（參見 5.2 節）。
2.  **Dropout**：
    *   在訓練神經網路時，隨機「關掉」一些神經元（設為 0）。
    *   *類比*：軍隊演習時隨機抽走指揮官，強迫部隊不能依賴特定的人，必須每個人都學會作戰。這能讓網路學出更強健的特徵。
3.  **早停 (Early Stopping)**：
    *   觀察驗證集的誤差。如果訓練集的誤差還在降，但驗證集的誤差開始上升，代表開始過擬合了，立刻停止訓練。
4.  **資料增強 (Data Augmentation)**：
    *   如果資料不夠，就自己造！
    *   例如：把圖片旋轉、裁切、調亮、水平翻轉，產生更多訓練資料。這在影像辨識中非常有效。
