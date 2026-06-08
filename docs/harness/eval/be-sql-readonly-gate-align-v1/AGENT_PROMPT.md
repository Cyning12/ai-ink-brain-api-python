## Agent 指令 · BE-1 Round 2（复制到新会话）

你是 **coding engineer 解题 Agent**。Open Folder = **`ai-ink-brain-api-python`**。

### 任务

1. 阅读并遵守：
   `docs/harness/eval/be-sql-readonly-gate-align-v1/TASK.md`
2. **不要**打开 `test_hidden_*.py` 或 `HIDDEN_TESTS.md`（评测机专用）。
3. 加固 `api/text2sql_core.py::validate_sql_readonly`，对齐 ChatBI AST **多语句**规则。
4. 自测通过：

```bash
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_validate_sql_readonly.py -v
```

5. 回归：

```bash
pytest tests/test_chatbi_sql_ast_gate_v1.py tests/test_chain_chat_events.py -v
```

### 交付

- 仅修改 TASK 白名单内文件
- 回复末尾给出：改了什么、公开测命令输出摘要、`git diff --name-only`

### 禁止

- 改 `api/chatbi_sql_gate.py` gate 语义、改路由、改 `_tech_graph`
- 声称使用 LangChain/LangGraph 库

---

**当前 base 预期**：公开测 4 个中至少 1 个失败（多语句负例），修复后应 4/4 绿。
