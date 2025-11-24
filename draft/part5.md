# AI 程式語言 (AI Programming)

想親手打造自己的 AI 嗎？ 那你必須學會與電腦溝通的語言。 在 AI 領域， 這個語言只有一個霸主， 那就是 **Python**。 

## Python 基礎 (Python Basics)

### 為什麼是 Python？ 

Python 之所以成為 AI 界的通用語言， 原因很簡單：
1.  **簡單易學**：它的語法非常接近英文， 讀起來像在讀文章， 而不是在解密碼。 
2.  **生態系豐富**：擁有海量的 AI 函式庫（如 TensorFlow, PyTorch, Scikit-learn）， 別人已經幫你寫好 90% 的程式碼了， 你只需要學會怎麼「呼叫」它們。 

### Python 語法速成

讓我們從最基礎的語法開始， 踏出程式設計的第一步。 

#### 1. 變數 (Variables)：資料的容器
變數就像是一個貼了標籤的箱子， 用來裝資料。 
*   **命名規則**：
    *   可以包含字母、 數字、 底線 `_`。 
    *   **不能以數字開頭**：`3_Pig` 是錯的， `Pig_3` 是對的。 
    *   **區分大小寫**：`Apple` 和 `apple` 是兩個不同的箱子。 
*   **範例**：

```python
name = "Alice"   # 字串 (String)
age = 25         # 整數 (Integer)
height = 1.65    # 浮點數 (Float)
is_student = True # 布林值 (Boolean)
```

#### 2. 輸出 (Print)：讓電腦說話
用 `print()` 函數把結果顯示在螢幕上。 
*   **基本用法**：`print("Hello World")`
*   **進階用法**：可以用逗號分隔多個東西， 預設會用空白隔開。 

*   **範例**：

```python
print(5, 10)          # 輸出: 5 10
print(5, 10, sep=',') # 輸出: 5,10 (指定分隔符號為逗號)
```

#### 3. 運算子 (Operators)：數學計算
*   **基本運算**：`+`, `-`, `*`, `/` (除法， 結果是小數)。 
*   **特殊運算**：
    *   `//` **求商數** (地板除法)：`7 // 2` 等於 `3` (只取整數部分)。 
    *   `%` **取餘數**：`7 % 2` 等於 `1` (7 除以 2 餘 1)。 
    *   `**` **次方**：`2 ** 3` 等於 `8` (2 的 3 次方)。 

#### 4. 邏輯控制 (Logic Control)：決定程式的走向
*   **if...else** (如果...否則)：

```python
score = 80
if score >= 60:
    print("及格")
else:
    print("不及格")
```

#### 5. 迴圈 (Loops)：重複做一樣的事
*   **for 迴圈**：當你知道要跑幾次， 或要遍歷一個清單時。 

```python
for i in range(5): # 跑 5 次 (0 到 4)
    print(i)
```
*   **while 迴圈**：當你不知道要跑幾次， 只知道停止條件時。 

```python
count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("跑完了") # while...else: 當迴圈正常結束時執行
```
*   **控制指令**：
    *   `break`：立刻跳出迴圈（不跑了）。 
    *   `continue`：跳過這一次， 直接進入下一輪。 

#### 6. 資料結構 (Data Structures)：收納資料的櫃子
*   **List (列表)**：最常用的， 什麼都能裝， 且有順序。 
    *   `fruits = ["apple", "banana", "cherry"]`
    *   可以用 `fruits[0]` 拿到 "apple"。 
*   **Tuple (元組)**：跟 List 很像， 但是**不可變** (Immutable)。 一旦建立就不能修改。 
    *   `point = (10, 20)`
    *   適合用來存座標或設定檔， 保護資料不被誤改。 
*   **Dictionary (字典)**：用「鍵-值對 (Key-Value)」來存資料， 像查字典一樣。 
    *   `student = {"name": "Bob", "age": 20}`
    *   可以用 `student["name"]` 拿到 "Bob"。 
*   **Set (集合)**：一堆**不重複**的資料， 沒有順序。 
    *   `numbers = {1, 2, 2, 3}` -> 實際存的是 `{1, 2, 3}` (自動去重)。 
    *   常用來做集合運算（交集、 聯集）。 

> **Figure Prompt:** A visual cheat sheet for Python Data Structures. Four quadrants. 1. List: A train with numbered cars [0], [1], [2]. 2. Tuple: A sealed glass box containing items (Immutable). 3. Dictionary: A library card catalog with "Key" labels pointing to "Value" books. 4. Set: A basket of unique fruits (no duplicates allowed). Style: Cute, educational illustrations.

恭喜你！你已經完成了這本書的旅程。 從 AI 的基本概念， 到機器學習的原理， 再到實際的應用與程式實作。 這只是起點， AI 的世界浩瀚無垠， 期待你繼續探索， 用 AI 創造更美好的未來！
