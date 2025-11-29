# 第 4 章：模型訓練與優化

## 4.1 優化演算法

### 4.1.1 梯度下降與變形

*   **非凸函數 (Non-convex)**：
    *   在訓練非線性模型時，目標函數多為非凸，容易陷入**局部最優解 (Local Minima)** (C)。
*   **動量 (Momentum)**：
    *   **Adam (Adaptive Moment Estimation)**：內建動量機制與自適應學習率 (B)。
    *   SGD 需額外加上 Momentum。

### 4.1.2 超參數調整

*   **學習率 (Learning Rate)**：
    *   控制權重更新速度。
    *   若模型收斂不穩定 (忽快忽慢)，應調整**學習率** (C)。
*   **搜尋策略**：
    *   **Random Search** vs Grid Search：
    *   Random Search 能**更有效率搜尋高維參數空間** (D)，因為它不會浪費時間在不重要的參數維度上。

## 4.2 正則化與過擬合

### 4.2.1 防止過擬合 (Overfitting)

*   **策略**：
    *   L1/L2 正則化。
    *   Dropout。
    *   早期停止 (Early Stopping)。
    *   **錯誤觀念**：擴增輸入特徵變數通常會增加模型複雜度，反而可能加劇過擬合 (D)。

### 4.2.2 正則化技術實作

*   **L1 (Lasso)**：產生稀疏模型 (C)。
*   **Dropout**：
    *   程式碼特徵：`mask = np.random.binomial(1, p, size=x.shape)`，訓練時隨機遮蔽神經元，並除以 p 保持期望值不變 (Inverted Dropout)。
    *   此為 **Dropout** 實作 (C)。

## 4.3 訓練策略

### 4.3.1 早期停止 (Early Stopping)

*   **機制**：監控驗證集損失 (Validation Loss)。
*   **策略**：設定**耐心值 (Patience)**，在連續多輪未改善後停止 (B)。
*   **損失曲線判讀**：
    *   通常 Training Loss (藍實線) 持續下降。
    *   Validation Loss (紅虛線) 先降後升 (過擬合)。
    *   題目圖表：空格 1 (藍實線) 為 Training，空格 2 (紅虛線) 為 Validation (C)。

### 4.3.2 概念漂移 (Concept Drift)

*   **情境**：原有驗證集無法反映現況 (如設備環境改變)。
*   **對策**：採用**時間序列交叉驗證**或**滑動視窗驗證**，動態更新驗證資料 (D)。
