# 第三篇：資料科學與大數據 (Data Science & Big Data)

在 AI 的世界裡，演算法是引擎，而**資料 (Data)** 就是燃料。沒有高品質的燃料，再好的引擎也跑不動。這一篇我們將探討如何開採、提煉並使用這些珍貴的數位石油。

## 第八章：資料處理基礎 (Data Processing Basics)

### 資料：AI 的糧食

資料科學 (Data Science) 是一門從數據中挖掘知識的學問。在餵給 AI 吃之前，我們必須先處理好這些食材。

#### 1. 資料收集與清洗 (Data Collection & Cleaning)
現實世界中的數據往往是髒亂的。
*   **資料收集**：來源可能來自資料庫、網頁爬蟲、感測器 (IoT) 或問卷調查。
*   **資料清洗**：這是資料科學家花最多時間的地方（通常佔 80%）。
    *   **缺失值處理**：有的欄位是空的怎麼辦？補平均值？補 0？還是直接刪掉這筆資料？
    *   **異常值處理**：年齡欄位出現 200 歲？這明顯是錯誤，需要修正或剔除。
    *   **格式統一**：日期格式有 `2023/01/01` 也有 `Jan 1, 2023`，必須統一才能運算。

#### 2. 資料視覺化 (Data Visualization)：讓數據說話
人類對數字不敏感，但對圖形很敏感。好的視覺化能讓你一眼看出數據背後的故事。

*   **圓餅圖 (Pie Chart)**：適合看**比例**。例如：市佔率（A公司 30%, B公司 20%...）。
*   **長條圖 (Bar Chart)**：適合**比較大小**。例如：各部門的營收比較。
*   **折線圖 (Line Chart)**：適合看**趨勢**。例如：股價走勢、氣溫變化。
*   **直方圖 (Histogram)**：適合看**分佈**。例如：全校學生的身高分佈（大部分集中在中間，兩邊人少）。
*   **散佈圖 (Scatter Plot)**：適合看**相關性**。例如：唸書時間 vs 考試成績（通常是正相關，點點往右上跑）。
*   **熱力圖 (Heatmap)**：用顏色深淺代表數值。例如：網站點擊熱圖，紅色代表最多人點的地方。

> **Figure Prompt:** A dashboard style illustration showing multiple charts. Top left: A colorful Pie Chart. Top right: A rising Line Chart. Bottom left: A Bar Chart comparing 3 items. Bottom right: A Scatter Plot with a trend line. Style: Modern UI dashboard, dark mode.

---

## 第九章：大數據技術與應用 (Big Data Technologies)

### 當資料大到無法想像：大數據 (Big Data)

當資料量大到一台電腦存不下、算不完時，我們就進入了「大數據」的領域。大數據通常具備 **3V** 特性：
1.  **Volume (大量)**：資料量極大 (TB, PB 等級)。
2.  **Velocity (高速)**：資料產生速度極快 (如即時交易、社群媒體貼文)。
3.  **Variety (多樣)**：資料格式千奇百怪 (文字、圖片、影片、Log 檔)。

### 大數據的統計學基礎

在處理大數據時，我們依然依賴統計學來幫助我們理解全貌。
*   **敘述性統計**：用平均數、中位數、標準差來描述這堆數據長什麼樣子。
*   **推論性統計**：從大數據中抽樣一小部分來研究，然後推斷整體的狀況（因為全部分析可能太慢了）。
*   **假設檢定**：科學地驗證你的猜想。例如：「改版後的網站真的有提高轉換率嗎？」還是只是運氣好？

### 駕馭大數據的工具

工欲善其事，必先利其器。處理大數據需要特殊的工具：

1.  **分散式運算 (Distributed Computing)**：
    *   **Hadoop (MapReduce)**：大數據的祖師爺。它的概念是「分而治之」。把一個大任務切成一千份，分給一千台電腦算，最後再把結果合併起來。
    *   **Spark**：Hadoop 的進化版。它把資料放在**記憶體 (RAM)** 裡運算，速度比 Hadoop 快 100 倍。現在是主流。

2.  **NoSQL 資料庫**：
    傳統的 SQL 資料庫（像 Excel 表格）在面對超大數據時會變慢。NoSQL 放棄了一些嚴格的規則，換取極致的速度和擴充性。
    *   **MongoDB**：文件型。存資料像存 JSON 檔案一樣自由，適合存結構不固定的資料。
    *   **Redis**：鍵值型 (Key-Value)。資料存在記憶體裡，讀寫速度快如閃電，常用來做快取 (Cache)。
    *   **Cassandra**：寬欄型。Facebook 開發的，寫入速度極快，適合存大量的 Log 或感測器數據。

3.  **資料流處理 (Stream Processing)**：
    *   **Kafka**：就像一個超大容量的數位水管。它可以承接每秒百萬筆的數據洪流（如使用者點擊、交易紀錄），然後穩穩地輸送給後端的系統去處理。

### 大數據與 AI 的強強聯手

大數據是 AI 的最佳拍檔。
*   **鑑別式 AI**：需要大數據來訓練出更準確的模型（如 Google 的廣告推薦）。
*   **生成式 AI**：需要海量的文本（整個網際網路的資料）來訓練 LLM（如 GPT-4）。

同時，我們也要注意**資料隱私**。在使用大數據時，必須遵守法規（如 GDPR），做好去識別化，保護用戶的隱私權。

> **Figure Prompt:** An illustration of the "3Vs of Big Data". Three icons arranged in a triangle. 1. Volume: A stack of server racks or hard drives. 2. Velocity: A speedometer or a fast-moving train. 3. Variety: A collage of icons representing video, text, images, and audio. Style: Infographic style.

這篇我們學習了如何處理和分析資料，以及在大數據時代不可或缺的技術棧。掌握了燃料，下一篇我們將探討如何安全地駕駛這輛 AI 跑車——AI 的倫理與治理。
