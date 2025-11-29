# 第 2 章：資料前處理

資料前處理 (Data Preprocessing) 是數據分析流程中最耗時但也最關鍵的步驟，包含資料清洗、型別轉換、標準化與編碼等。

## 2.1 Pandas 資料處理基礎

Python 的 Pandas 套件是處理結構化資料的利器。

### 2.1.1 敘述性統計與聚合

*   **計算總和**：`df['欄位名'].sum()` (A)。
*   **敘述性統計**：`df['欄位名'].describe()` 可一次產出計數、平均值、標準差、四分位數等 (B)。
    *   **解讀 `describe()`**：
        *   `count`：非缺失值的資料筆數。
        *   `mean`：平均值。
        *   `std`：標準差。
        *   `25%` (Q1)：第一四分位數。
        *   `50%` (Median)：中位數。
        *   `75%` (Q3)：第三四分位數。

### 2.1.2 缺失值處理 (Missing Values)

*   **偵測缺失值**：
    *   `df.isnull().sum()` 或 `df.isna().sum()` (C)。`isNaN` 與 `isnan` 非 Pandas 標準 DataFrame 方法。
*   **型別影響**：
    *   若 CSV 中的整數欄位 (如 Year) 含有缺失值 (NaN)，Pandas 載入時會自動將該欄位轉為 **float64** (B, C 雖有部分道理，但主因是 NaN 為浮點數特性)。更精確地說，是因為 NaN 在 NumPy/Pandas 早期版本中是浮點數，導致整欄轉型 (B)。
*   **轉換為整數**：
    *   若需將含 NaN 的 float 欄位轉為整數，可使用 `Int64` (大寫 I) 型別，它支援缺失值：`data['Year'] = data['Year'].astype('Int64')` (D)。
    *   或者先填補缺失值再轉型：`fillna(0).astype(int)`。

## 2.2 類別資料處理 (Categorical Data)

### 2.2.1 標籤編碼 (Label Encoding)

*   **方法**：將類別映射為整數 (如 A->0, B->1, C->2)。
*   **風險**：
    *   會引入**類別之間的虛假順序關係** (B)。例如模型可能認為 2 > 1 > 0，但實際上類別間無此關係 (Nominal Data)。
    *   適用於**有序類別 (Ordinal Data)** (如：低、中、高)。

### 2.2.2 獨熱編碼 (One-Hot Encoding)

*   **方法**：將每個類別轉換為一個二元特徵 (0 或 1)。
*   **優點**：避免順序誤判。
*   **缺點**：
    *   **維度爆炸 (Curse of Dimensionality)**：若類別數量極多 (High Cardinality)，會產生過多欄位 (A)。
    *   樹模型 (如 Gradient Boosting Tree) 有時可直接處理 Label Encoding 或使用 Target Encoding，不一定非要 One-Hot (視實作而定，但題目強調 Label Encoding 的順序風險)。

## 2.3 數值資料縮放 (Scaling)

### 2.3.1 標準化 (Standardization / Z-score Normalization)

*   **方法**：$x' = \frac{x - \mu}{\sigma}$。
*   **效果**：平均值為 0，標準差為 1。
*   **適用**：大多數距離型演算法 (如 SVM, KNN, K-means)，可改善收斂速度 (C)。

### 2.3.2 正規化 (Normalization / Min-Max Scaling)

*   **方法**：$x' = \frac{x - min}{max - min}$。
*   **效果**：將數值壓縮至 [0, 1] 之間。

### 2.3.3 穩健縮放 (Robust Scaling)

*   **情境**：當資料中存在**極端值 (Outliers)** 時。
*   **方法**：利用中位數與四分位距 (IQR) 進行縮放，受極端值影響較小 (C)。

## 2.4 資料分箱 (Binning)

*   **目的**：將連續變數轉換為離散區間。
*   **優點**：提升模型可解釋性，處理非線性關係。
*   **風險**：若分段方式不當，可能導致**資訊損失**或邊界偏誤 (D)。
