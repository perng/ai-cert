import os

def insert_after_heading(filepath, heading, content):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if line.startswith(heading):
            # Insert the content right after the heading
            lines.insert(i + 1, f"\n```{{mermaid}}\n{content}\n```\n")
            break
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# chapter 1
insert_after_heading('chapter1.qmd', '## 代理人的組成', 
"""graph TD
    User([使用者]) --> |自然語言輸入| LLM
    LLM[大型語言模型 LLM]
    Profile[(Profile 角色設定)] -.-> LLM
    Memory[(Memory 記憶系統)] <--> LLM
    Tools[[外部工具 Tools]] <--> LLM
    Planning((規劃能力 Planning)) <--> LLM
    LLM --> |執行行動| Env[外部環境]""")

insert_after_heading('chapter1.qmd', '## 代理人如何思考和行動', 
"""flowchart LR
    A(思考 Thought) --> B(行動 Action)
    B --> C(觀察 Observation)
    C -. 回饋 .-> A""")

# chapter 2
insert_after_heading('chapter2.qmd', '## MCP 的三個角色', 
"""graph LR
    Host[MCP 主機 Host<br/>例如 Claude Desktop] --> Client[MCP 客戶端 Client]
    Client <--> |標準化協議 MCP| Server[MCP 伺服器 Server]
    Server --> ToolA[[檔案讀寫工具]]
    Server --> ToolB[[資料庫資源]]""")

# chapter 3
insert_after_heading('chapter3.qmd', '## 上下文工程', 
"""graph TD
    BasePrompt[靜態基礎提示詞] --> ContextManager{上下文工程}
    Memory[記憶與歷史對話] --> ContextManager
    ToolFeedback[工具回傳結果] --> ContextManager
    ContextManager --> |動態修剪、防混淆過濾| LLM[LLM 產生決策]""")

insert_after_heading('chapter3.qmd', '## 記憶管理', 
"""graph TD
    Short[短期記憶 Short-Term<br/>受限於上下文視窗] --> |向量化與摘要化| Long[(長期記憶 Long-Term<br/>向量資料庫)]
    Long --> |相似性語意檢索| Short
    Working((工作記憶 Working<br/>執行任務時的暫存變數)) -.輔助.-> Short""")

# chapter 4
insert_after_heading('chapter4.qmd', '## Hermes Agent', 
"""flowchart TD
    Task(收到新任務) --> Eval{有現成的技能嗎？}
    Eval --> |Yes| Exec[直接套用執行]
    Eval --> |No| LLM[啟動推理迴圈嘗試解決]
    LLM --> Success{成功完成嗎？}
    Success --> |Yes| Pack[自我學習並封裝為新技能]
    Pack --> Exec""")

# chapter 5
insert_after_heading('chapter5.qmd', '## 常見的多代理協作模式', 
"""graph TD
    subgraph 協調者-執行者模式
    Coord(協調者 Coordinator) --> Exec1(資料搜集代理)
    Coord --> Exec2(邏輯分析代理)
    Coord --> Exec3(報告撰寫代理)
    end""")

insert_after_heading('chapter5.qmd', '## 代理人之間如何「說話」', 
"""graph LR
    AgentA[代理人 A] --> |發送代理名片與請求| Router{事件佇列 Event Queue}
    Router --> |分配與轉交對話上下文| AgentB[代理人 B]
    AgentB -.-> |回傳工作產物 Artifact| Router""")

print("Successfully injected mermaid figures.")
