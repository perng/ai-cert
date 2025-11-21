# 第四篇：AI 倫理、 治理與風險 (AI Ethics, Governance & Risks)

能力越強， 責任越大。 AI 就像一把雙面刃， 用得好可以造福人類， 用不好則可能帶來災難。 在這一篇， 我們將探討如何安全、 負責任地開發和使用 AI。 

## 第十章：AI 治理與風險 (AI Governance & Risks)

### AI 的潛在威脅

AI 並不是完美的， 它也會犯錯， 甚至被惡意利用。 我們必須認識這些風險， 才能有效地防範。 

1.  **AI 幻覺 (AI Hallucination)**：
    *   **現象**：AI 有時候會一本正經地胡說八道。 例如， 問它「林肯總統是哪一年發明燈泡的？ 」， 它可能會編造一個看起來很真實的年份， 但事實上林肯根本沒發明燈泡。 
    *   **原因**：生成式 AI 的本質是「機率預測」， 它只是在預測下一個字最可能接什麼， 而不是在查證事實。 
    *   **對策**：對於關鍵事實（如醫療、 法律建議）， 必須進行人工查核 (Human-in-the-loop)。 

2.  **偏見 (Bias)**：
    *   **現象**：如果訓練數據本身就有偏見， AI 就會學壞。 例如， 如果訓練數據中大部分的工程師都是男性， AI 可能會誤以為「女性不適合當工程師」， 在篩選履歷時歧視女性。 
    *   **對策**：使用多樣化、 平衡的數據集， 並在模型上線前進行公平性測試。 

3.  **Deepfake (深偽技術)**：
    *   **現象**：利用 AI 生成極度逼真的假影片或假聲音。 這可能被用來製造假新聞、 詐騙（假裝親人聲音借錢）或毀壞他人名譽。 
    *   **對策**：開發 Deepfake 偵測工具， 並推動數位浮水印技術。 

4.  **對抗式攻擊 (Adversarial Attacks)**：
    *   **現象**：駭客在圖片上加入人類看不見的微小雜訊， 就能騙過 AI。 例如， 在一張熊貓的照片上加一點點雜訊， AI 竟然會把它誤判成長臂猿。 
    *   **對策**：進行對抗式訓練 (Adversarial Training)， 讓模型看過這些攻擊樣本， 增強抵抗力。 

5.  **模型漂移 (Model Drift)**：
    *   **現象**：世界在變， 數據也在變。 一個半年前訓練好的模型， 現在可能已經不準了。 例如， 消費者的購物習慣改變了， 原本的推薦系統就會失效。 
    *   **對策**：持續監控模型效能， 並定期重新訓練 (Retrain)。 

> **Figure Prompt:** An illustration of "AI Hallucination". A robot wearing glasses is reading a book and confidently telling a story to a human, but the speech bubble contains a mix of real facts and obvious fantasy elements (like a unicorn). The human looks confused. Style: Cartoonish, humorous.

---

## 第十一章：AI 倫理 (AI Ethics)

### AI 應該遵守的道德規範

除了技術上的風險， 我們還必須考慮 AI 對社會的影響。 AI 倫理就是一套指導原則， 確保 AI 的發展符合人類的價值觀。 

#### 1. 隱私保護 (Privacy)
AI 需要大量數據， 這往往涉及個人隱私。 
*   **資料匿名化 (Data Anonymization)**：在收集數據時， 去除可以識別個人身分的資訊（如姓名、 身分證號）， 只保留分析所需的特徵。 
*   **用戶同意 (Consent)**：必須明確告知用戶我們會收集什麼資料、 用來做什麼， 並取得用戶同意。 

#### 2. 透明度與可解釋性 (Transparency & Explainability)
AI 不應該是一個黑盒子 (Black Box)。 
*   **問題**：如果 AI 拒絕了你的貸款申請， 你一定想知道「為什麼？ 」。 如果銀行說「不知道， 是 AI 算的」， 這顯然無法接受。 
*   **原則**：對於影響重大的決策（如醫療、 司法、 金融）， AI 的決策過程必須是可解釋的， 讓人們理解它是依據什麼邏輯做出判斷。 

#### 3. 公平性 (Fairness)
AI 應該公平地對待每一個人， 不分種族、 性別、 年齡或宗教。 
*   **算法公正性**：開發者必須意識到自己的偏見， 並積極消除模型中的歧視。 

### 案例分析：AI 倫理的兩難

*   **自駕車的電車難題**：如果自駕車煞車失靈， 前方有五個路人， 轉向會撞死一個路人（或乘客自己）， AI 該如何選擇？ 這是一個沒有標準答案的倫理難題。 
*   **醫療診斷輔助**：AI 可以幫忙看 X 光片， 但如果 AI 誤診了， 責任在誰？ 是醫生？ 是 AI 開發商？ 還是醫院？ 

> **Figure Prompt:** A conceptual illustration of "Explainable AI". On the left, a "Black Box" AI with a question mark, outputting a decision "Rejected". On the right, a "Glass Box" AI (transparent) showing the internal gears and logic, outputting "Rejected because: Income too low". Style: Comparative diagram.

AI 治理不僅僅是技術問題， 更是法律、 社會和哲學問題。 只有建立完善的治理框架， 我們才能安心地享受 AI 帶來的便利。 
