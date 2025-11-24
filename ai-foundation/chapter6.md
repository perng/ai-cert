# 非監督式學習與強化學習

非監督式學習 (Unsupervised Learning) 就像是讓 AI 在沒有老師的情況下自學，尋找資料中的隱藏結構。而強化學習 (Reinforcement Learning) 則是讓 AI 像生物一樣，透過與環境互動、嘗試錯誤來學習生存策略。

## 6.1 分群演算法 (Clustering) {#sec-clustering}

分群的目標是「物以類聚」，將相似的資料點歸為同一群。

### K-means 演算法 {#sec-kmeans}

*   **概念**：隨機選定 $K$ 個中心點（質心），然後不斷調整這些中心點的位置，直到每一群的內部差異最小。
*   **步驟**：
    1.  隨機決定 $K$ 個中心。
    2.  將每個資料點分配給最近的中心。
    3.  重新計算每一群的平均位置，作為新的中心。
    4.  重複步驟 2-3，直到中心不再移動。
*   **缺點**：必須事先決定 $K$ 值（要分幾群？）；對離群值敏感。

### 階層式分群 (Hierarchical Clustering) {#sec-hierarchical-clustering}

*   **概念**：建立一個樹狀結構（Dendrogram），不需要事先決定 $K$ 值。
*   **做法**：
    *   **聚合式 (Agglomerative)**：一開始每個點都是一群，然後慢慢把最近的兩群合併，直到剩下一大群。
    *   **分裂式 (Divisive)**：一開始所有點是一大群，然後慢慢切分。

### DBSCAN (Density-Based Spatial Clustering of Applications with Noise) {#sec-dbscan}

*   **概念**：基於**密度**的分群。只要點夠密集就算同一群，如果不夠密集就被視為雜訊。
*   **優勢**：可以找出任意形狀的群聚（不像 K-means 傾向於圓形），且能自動識別並排除**離群值**。

## 6.2 關聯規則與降維 {#sec-association-rules}

### Apriori 演算法 (購物籃分析) {#sec-apriori}

*   **經典案例**：「啤酒與尿布」。沃爾瑪發現週五晚上買尿布的爸爸，通常也會順便買啤酒。
*   **指標**：
    *   **支持度 (Support)**：某個商品組合出現的頻率（例如：10% 的訂單同時有 A 和 B）。
    *   **信心度 (Confidence)**：買了 A 的人，有多大概率也會買 B（例如：買尿布的人有 70% 會買啤酒）。
    *   **提升度 (Lift)**：A 的出現是否有助於 B 的出現（Lift > 1 代表正相關，Lift < 1 代表負相關）。

### 主成分分析 (PCA) {#sec-pca}

（參見 4.3 節）PCA 也是一種非監督式學習，用於找出資料的主要變異方向，進行降維。

### 自動編碼器 (Autoencoder) {#sec-autoencoder}

*   **概念**：訓練一個神經網路，讓輸出等於輸入。
*   **結構**：
    *   **編碼器 (Encoder)**：將輸入壓縮成低維度的「潛在表示 (Latent Representation)」。
    *   **解碼器 (Decoder)**：將潛在表示還原回原始輸入。
*   **用途**：資料壓縮、去噪（Denoising）、異常偵測（如果還原不回來，代表是異常資料）。

## 6.3 強化學習 (Reinforcement Learning) {#sec-reinforcement-learning-detail}

強化學習是 AI 邁向自主決策的關鍵。

### 核心要素 {#sec-rl-elements}

*   **代理人 (Agent)**：學習的主角（如瑪利歐）。
*   **環境 (Environment)**：遊戲關卡。
*   **狀態 (State)**：瑪利歐的位置、敵人的位置。
*   **行動 (Action)**：跳躍、移動、發射火球。
*   **獎勵 (Reward)**：吃到金幣 (+10)、過關 (+100)。
*   **懲罰 (Penalty)**：碰到烏龜 (-10)、掉進洞裡 (-100)。

### 價值函數與策略 (Policy) {#sec-value-policy}

*   **價值函數 (Value Function)**：評估在某個狀態下，未來預期能拿到多少總獎勵。
*   **策略 (Policy)**：代理人的大腦。決定在某個狀態下該採取什麼行動的規則（例如：看到烏龜就跳）。

### 探索與利用 (Exploration vs. Exploitation) {#sec-exploration-exploitation}

*   **探索**：去沒去過的地方看看（可能發現寶藏，也可能踩雷）。
*   **利用**：走已知最安全的路（穩拿獎勵，但不會進步）。
*   **$\epsilon$-Greedy 策略**：丟銅板決定。90% 的時間利用已知知識，10% 的時間隨機探索。

### 演算法概論 {#sec-rl-algorithms}

*   **Q-Learning**：建立一張 **Q 表 (Q-Table)**，記錄在每個狀態下做每個動作的價值。就像作弊小抄。
*   **Deep Q-Network (DQN)**：當狀態太多（如圍棋棋盤），Q 表存不下時，用**深度神經網路**來預估 Q 值。DeepMind 用這個技術讓 AI 學會玩 Atari 遊戲。
