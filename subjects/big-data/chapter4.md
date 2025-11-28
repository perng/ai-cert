# 第 4 章：資料視覺化

資料視覺化是探索性資料分析 (EDA) 與結果呈現的重要工具。

## 4.1 視覺化原則

### 4.1.1 數據密度 (Data Density)

*   **Edward Tufte 原則**：優秀的圖表應最大化數據墨水比 (Data-Ink Ratio)。
*   **高密度設計**：
    *   若需在單一頁面呈現多區域、多產品線的趨勢，應避免過度分割或簡化。
    *   **最佳實踐**：使用顏色區分產品線，於同一圖表中整合多區域趨勢線 (若不雜亂)，或使用**小多圖 (Small Multiples)**。但在題目選項中，(B) 整合多區域趨勢線並保持清晰，最符合在有限空間呈現大量資訊的密度原則。

## 4.2 常用圖表與應用

### 4.2.1 箱型圖 (Box Plot)

*   **用途**：顯示數據的分佈、四分位數及**離群值 (Outliers)**。
*   **觀察**：若 IQR 很小但上鬚線很長且有高金額離群值，代表大部分消費集中，但有少數極高消費。
*   **策略**：若要凸顯不同消費層級差異 (尤其是高金額族群)，可使用**對數刻度 (Log Scale)** 繪製，以縮小極端值造成的視覺壓縮 (A)。

### 4.2.2 長條圖 (Bar Chart)

*   **Pandas 繪圖**：
    *   統計各平台銷售總額：`data.groupby("Platform")["Global_Sales"].sum().plot(kind="bar")` (A)。
*   **Seaborn 繪圖**：
    *   比較多區域銷售 (需轉為長格式)：`sns.barplot(x="variable", y="value", data=pd.melt(...))` (C)。
    *   Top 5 排行榜：`sns.barplot(x="Name", y="NA_Sales", data=data.nlargest(5, "NA_Sales"))` (B)。

### 4.2.3 雙軸圖與其他

*   **多變數關聯**：
    *   若要分析四檔股票的**相關性與共變動性**，**熱力圖 (Heatmap)** 搭配相關係數矩陣是最直觀的方式 (D)。
    *   雙軸折線圖適合比較兩個量級不同的時間序列，但不適合同時比較四個變數的交互關聯。

## 4.3 Python 視覺化工具

*   **Matplotlib / Pandas Plotting**：基礎繪圖。
*   **Seaborn**：基於 Matplotlib，提供更美觀且高階的統計繪圖介面 (如 `barplot`, `heatmap`, `boxplot`)。
