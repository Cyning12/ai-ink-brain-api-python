# Agent 指令 · BE-1 Round 2

> **人先做**（不进 Prompt）：`git checkout f86a32a` 或 worktree 指向该 commit · Open Folder = 本仓根  
> **评测机全量**（worktree 可无 scripts）：`pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/ -v`

从下方 **---COPY START---** 到 **---COPY END---** 整段复制到新 Agent 会话。

---COPY START---

你是 coding engineer 解题 Agent（Moonshot BE-1 评测）。

Open Folder = ai-ink-brain-api-python
Base commit = f86a32a（仅评测包，尚未修复）

【任务】
1. 阅读并严格遵守：docs/harness/eval/be-sql-readonly-gate-align-v1/TASK.md（可用 @ 引用）
2. 修复 api/text2sql_core.py 里的 validate_sql_readonly：对齐 ChatBI AST 多语句规则，使 SELECT 1; SELECT 2（单分号双语句）必须拒绝。
3. 改前先读：api/chatbi_sql_gate.py 的 _phase_ast、调用方 api/chain_chat.py 与 api/tools.py。

【禁止打开或修改】
- test_hidden_*.py、HIDDEN_TESTS.md、GOLD_SOLUTION.md（评测机专用）
- api/chatbi_sql_gate.py 三阶段 gate 语义、api/index.py 路由、supabase/、docs/_tech_graph/
- 新增 pip 依赖；声称使用 LangChain/LangGraph 库

【必须执行的命令】
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_validate_sql_readonly.py -v
pytest tests/test_chatbi_sql_ast_gate_v1.py tests/test_chain_chat_events.py -q

【交付】
- 改了什么、为何这样改（2～3 句）
- 上述 pytest 的 pass/fail 计数
- git diff --name-only

【预期】
Base 下公开测 4 个里至少 1 个失败；修复后公开测 4/4 绿。

---COPY END---
