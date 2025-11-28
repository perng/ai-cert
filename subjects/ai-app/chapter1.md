# 第一章：進階自然語言處理技術

本章將深入探討自然語言處理（NLP）的核心技術，包括詞向量模型的差異、Transformer 架構的細節，以及 BERT 等預訓練模型的運作機制。這些技術是現代 AI 理解與生成語言的基石。

## 1. 詞向量模型 (Word Embeddings)

詞向量 (Word Embeddings) 是將詞彙轉換為數值向量的技術，讓電腦能夠理解詞彙之間的語意關係。在向量空間中，語意相近的詞（如「國王」與「皇后」）距離會比較近。

> **數學直覺：詞向量運算**
>
> 經典的例子是：
> $$ \vec{King} - \vec{Man} + \vec{Woman} \approx \vec{Queen} $$
>
> 這代表如果把「國王」的向量減去「男人」的特徵，再加上「女人」的特徵，結果會非常接近「皇后」的向量。這證明了向量空間成功捕捉了「性別」與「皇室」的語意維度。

<!-- IMAGE_PROMPT: 
title: 詞向量空間示意圖
style: stick figure style, colorful
content: 畫一個三維座標空間，裡面漂浮著幾個詞彙球體。
- "國王" (King) 和 "皇后" (Queen) 的球體靠得很近。
- "男人" (Man) 和 "女人" (Woman) 的球體靠得很近。
- 畫一個箭頭從 "國王" 指向 "皇后"，另一個平行的箭頭從 "男人" 指向 "女人"，標示 "語意關係向量"。
- 一個火柴人戴著眼鏡，指著這些球體說：「電腦透過這些距離來理解詞義喔！」。
-->

### Word2Vec vs. GloVe

雖然 Word2Vec 與 GloVe 都能產生高品質的詞向量，但它們的訓練原理有所不同，這也是考試中常見的比較題型：

*   **Word2Vec**：
    *   **核心概念**：屬於**基於預測 (Prediction-based)** 的模型。它像是一個神經網路學生，不斷做填空題來學習。
    *   **運作方式**：透過一個淺層神經網路，利用滑動視窗 (Sliding Window) 掃描文本。
    *   **兩種架構**：
        *   **CBOW (Continuous Bag of Words)**：
            *   **原理**：利用**周圍詞 (Context)** 來預測 **中心詞 (Target)**。例如句子是 "The cat sits on the mat"，CBOW 會嘗試用 "The", "cat", "on", "the", "mat" 來預測 "sits"。
            *   **特性**：訓練速度快，對頻繁出現的詞效果好，因為它將上下文平均化了。
        *   **Skip-gram**：
            *   **原理**：利用 **中心詞 (Target)** 來預測 **周圍詞 (Context)**。例如用 "sits" 來預測 "The", "cat", "on" 等。
            *   **特性**：對於**罕見詞 (Rare Words)** 的處理效果較好。因為在 Skip-gram 中，即使是罕見詞作為中心詞，它也會產生多個預測任務（一對多），讓模型有更多機會學習它的特徵。

*   **GloVe (Global Vectors)**：
    *   **核心概念**：屬於**基於計數 (Count-based)** 的模型。它像是一個統計學家，先看完所有書，統計完所有詞的關係後才下結論。
    *   **運作方式**：利用全域的**共現矩陣 (Co-occurrence Matrix)** 進行統計分析。它計算兩個詞在整個語料庫中一起出現的機率。
    *   **數學意義**：它明確地將詞義向量化為共現機率的對數比，結合了矩陣分解（全域統計）與局部視窗（上下文關係）的優點。

<!-- IMAGE_PROMPT: 
title: Word2Vec vs GloVe
style: stick figure style, colorful
content: 分左右兩邊。
- 左邊 (Word2Vec): 一個火柴人學生正在做填空題試卷，題目是 "The cat ___ on the mat"，他在格子裡填寫 "sits"。標籤寫：「基於預測 (Prediction)」。
- 右邊 (GloVe): 一個火柴人教授戴著眼鏡，拿著巨大的計算機和厚厚的統計報表，報表上寫著 "共現矩陣 (Co-occurrence Matrix)"。標籤寫：「基於統計 (Count-based)」。
-->

### 其他重要詞向量技術 (FastText, ELMo)

除了 Word2Vec 和 GloVe，還有兩個在 NLP 發展史上承先啟後的重要技術：

*   **FastText**：
    *   **核心改進**：解決了 Word2Vec **無法處理未登錄詞 (OOV, Out-Of-Vocabulary)** 的問題。
    *   **原理**：它不把整個詞當作最小單位，而是將詞拆解成 **Character n-grams (字元級 n-gram)**。
        *   例如 "apple" 會被拆成 `<ap`, `app`, `ppl`, `ple`, `le>` 等。
    *   **優勢**：即使遇到沒見過的詞（如 "applelike"），只要看過其組成部分（"apple", "like"），就能推算出它的向量。這對**構詞變化豐富**的語言（如德文、俄文）特別有效。

*   **ELMo (Embeddings from Language Models)**：
    *   **核心改進**：解決了 Word2Vec **一詞多義 (Polysemy)** 的問題。
    *   **靜態 vs. 動態**：Word2Vec 是**靜態 (Static)** 的，"Bank" 在「銀行」和「河岸」這兩個意思下，向量是一樣的。ELMo 是**動態 (Contextualized)** 的。
    *   **原理**：使用雙向 LSTM (Bi-LSTM) 根據上下文動態生成詞向量。
    *   **優勢**：在 "I went to the **bank** to deposit money" 和 "I sat by the river **bank**" 兩句話中，ELMo 會賦予 "bank" 兩個完全不同的向量，精準捕捉語境意義。

<!-- IMAGE_PROMPT: 
title: ELMo 的一詞多義
style: stick figure style, colorful
content: 
- 畫兩個句子。
- 句子 A: "Deposit money at the **bank**." -> "bank" 變成一個金幣形狀的向量。
- 句子 B: "Fishing by the **bank**." -> "bank" 變成一個河流形狀的向量。
- 旁邊一個火柴人驚訝地說：「同一個字，形狀竟然會變！」。
- 標籤：「動態詞向量 (Contextualized Embedding)」。
-->

### TF-IDF 的限制

TF-IDF (Term Frequency-Inverse Document Frequency) 是一種傳統的關鍵詞提取技術，但在處理現代複雜文本時有其侷限。

> **範例：TF-IDF 計算**
>
> 假設文件 A 只有一句話："Cat loves cat food."
> *   **TF ("cat")** = 2 (出現兩次) / 4 (總詞數) = 0.5
> *   **IDF ("cat")** = log(總文件數 / 有 "cat" 的文件數)
>     *   如果 "cat" 在每份文件都出現，IDF = log(1) = 0。
>     *   這代表 "cat" 雖然在文件 A 很常出現，但因為它太普遍了，所以 TF-IDF 分數會被拉低，顯示它不是關鍵字。

*   **原理回顧**：
    *   **TF (詞頻)**：詞出現越多次越重要。
    *   **IDF (逆文件頻率)**：詞在越少文件中出現越獨特（重要）。
    *   **公式概念**：權重 = TF × IDF。
*   **長文本問題**：在處理**篇幅較長**的文本時，TF-IDF 往往無法準確反映關鍵詞重要性。
    *   **原因**：長文本中，某些普通詞彙（非停用詞，但也非關鍵詞）的**詞頻 (Term Frequency)** 可能會因為文章長度而自然偏高。這導致它們的權重被過度放大，掩蓋了真正具區別力的關鍵詞。
    *   **解決**：通常需要對 TF 進行正規化（如除以文章總詞數），或使用 BM25 等改進演算法。

### N-gram 語言模型的限制

N-gram 模型是一種機率語言模型，透過計算前 N-1 個詞來預測下一個詞。

*   **運作**：例如 3-gram (Trigram) 只看前兩個詞來預測第三個詞。
*   **主要限制**：**無法捕捉長距離依賴關係 (Long-range Dependencies)**。
    *   **例子**：句子 "The **boy** who was wearing a red shirt and playing with a ball in the park ...... **is** my brother."
    *   **問題**：要決定最後是用 "is" 還是 "are"，必須看開頭的 "boy"。但如果中間隔了 20 個詞，N-gram (若 N 小於 20) 根本「看」不到開頭的 "boy"，因此無法正確預測單複數。它假設詞與詞之間的關係僅限於固定的視窗大小。

## 2. Transformer 架構深入解析

Transformer 模型徹底改變了 NLP 領域，其核心在於**自注意力機制 (Self-Attention Mechanism)**，解決了 RNN 無法平行運算且難以捕捉長距離依賴的問題。

### 自注意力機制 (Self-Attention)

*   **功能**：允許模型在處理序列中的每個詞時，同時關注序列中的其他所有詞，並計算它們之間的關聯強度（注意力權重）。
*   **核心公式**：
    $$ Attention(Q, K, V) = softmax(\frac{QK^T}{\sqrt{d_k}})V $$
    *   **Q (Query)**：查詢向量（我想找什麼？）
    *   **K (Key)**：鍵值向量（我有什麼特徵？）
    *   **V (Value)**：數值向量（我的內容是什麼？）
    *   **直觀理解**：拿 Q 去跟所有的 K 做匹配（點積），匹配度越高的，對應的 V 就越重要（加權平均）。
*   **優勢**：
    1.  **捕捉長距離依賴**：無論兩個詞在句子中相距多遠，Self-Attention 都能直接計算它們的關係，距離為 1。這顯著提升了長篇文件的翻譯與理解品質。
    2.  **平行運算**：不像 RNN 需要按順序讀取，Transformer 可以同時處理整個句子的所有詞。

<!-- IMAGE_PROMPT: 
title: 自注意力機制運作
style: stick figure style, colorful
content: 畫一個句子 "The animal didn't cross the street because it was too tired."
- 畫出 "it" 這個詞發出多條光線連接到句子其他詞。
- 連接到 "animal" 的光線特別粗、特別亮（代表注意力權重高）。
- 連接到 "street" 的光線很細（代表注意力權重低）。
- 一個火柴人拿著放大鏡看著 "it" 和 "animal" 的連線，說：「原來 'it' 是指 'animal' 啊！」。
-->

### 注意力崩塌 (Attention Collapse)

*   **現象**：在非常深層的 Transformer 模型中（例如堆疊了幾十層），有時會發生注意力分佈過於平均或趨同的現象。這意味著模型對所有詞的關注度都差不多，導致無法有效聚焦於關鍵資訊，特徵表達能力下降。
*   **解決策略**：
    *   **稀疏化約束 (Sparsity Constraint)**：這是一種有效的改善方法。透過在損失函數中加入正則化項，或改變 Attention 的計算方式，強迫模型只關注最重要的少數詞彙（將不重要的權重推向 0），避免權重過度分散。這有點像強迫學生畫重點時「只能畫最重要的三個字」，而不是整頁塗滿螢光筆。

## 3. BERT 模型

BERT (Bidirectional Encoder Representations from Transformers) 是 Google 開發的預訓練模型，它只使用了 Transformer 的 **Encoder** 部分。

### 遮罩語言模型 (Masked Language Model, MLM)

這是 BERT 最具創新性的訓練策略，也是它能理解上下文的關鍵。

*   **傳統限制**：過去的語言模型（如 GPT 的前身）通常是單向的（從左到右），因為如果同時看左右，模型會「偷看」到答案。
*   **BERT 的突破**：
    *   **作法**：隨機**遮罩 (Mask)** 輸入序列中約 15% 的詞彙（例如將詞換成 `[MASK]` 符號）。
    *   **任務**：強迫模型根據**雙向上下文 (Bidirectional Context)**（即被遮罩詞的前面和後面所有詞）來預測被遮罩的詞是什麼。
    *   **例子**：句子 "我喜歡吃 [MASK] 裡的蘋果"。模型必須同時看前面的 "吃" 和後面的 "蘋果"，才能推斷出 [MASK] 可能是 "籃子" 或 "冰箱"。
*   **目的**：這使得 BERT 能建立深度的雙向語意理解能力。

<!-- IMAGE_PROMPT: 
title: BERT 的遮罩訓練
style: stick figure style, colorful
content: 畫一個機器人 BERT 正在看一張紙條。
- 紙條上寫著："今天天氣真 [MASK]，我們去公園玩吧！"
- 機器人左眼看著 "今天天氣真"，右眼看著 "，我們去公園玩吧！"。
- 機器人腦袋浮現燈泡，顯示答案："好 (Good)"。
- 旁邊一個火柴人老師打勾，說：「正確！你同時看了前後文！」。
-->

### 應用場景

由於 BERT 是雙向理解專家，它特別適合需要理解整句或整段語意之間關係的任務：
*   **情感分析**：判斷整句評論是褒是貶。
*   **問答系統 (QA)**：判斷這段文章是否包含問題的答案，以及答案在哪裡。
*   **命名實體識別 (NER)**：判斷每個詞的詞性（人名、地名等），這需要上下文資訊。
*   **自然語言推理 (NLI)**：判斷兩個句子是否矛盾或蘊含。
