# Task：ChatBI V2 — Text2SQL 多轮语义承接（已实现基线 + 值域锚点后续）

> **状态**：`in_progress`（**A 已落地代码**；**B/C 待实现**，验收未全绿前保持本状态）  
> **范围**：仅后端 `ai-ink-brain-api-python`（Text2SQL 工具链、会话记忆形状；不涉及前端 transcript UI）  
> **关联规格**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md`（L1–L4 分层、§3 指代与 rewrite、§4 结构化上下文）  
> **父任务索引**：`docs/tasks/active/task_chatbi_v2_agent_p1_behavior.md`（P1 总览；本子任务可视为其下「多轮 + Text2SQL 真值」专项）  
> **真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（环境变量与路由以该文件为准，本文不复制）  
> **关联（V2 可观测 / RAG 改写 / LLM Prompt）**：`docs/tasks/active/task_chatbi_v2_rewrite_timeline_llm_prompt_capture_v1.md`

---

## 背景与目标

多轮场景下，用户首轮明确表名（如 `agent_info`），次轮用「刚刚那张表 / 其中有多少男性」等**省略主语**的问法时，系统需在语义上接得住：**Intent 仍走结构化查库、Text2SQL 检索与生成能继承上轮表/语境**，避免出现「未查到数据」或**选错表**（如 `agent_info` 与 `customer_info` 混用）、**条件字面量与库内枚举不一致**等问题。

本子任务落盘两部分：

1. **A（已实现）**：在 Text2SQL 路径注入会话历史，用于 DDL 检索与 SQL 生成提示（基线修复）。  
2. **B/C（待改进）**：值域/同义词字典（或 DISTINCT 采样）与上轮结构化锚点（表/SQL 摘要），与规格 §4 对齐。

---

## 范围

### A. 多轮历史注入 Text2SQL（已实现）

- [x] `text2sql_execute`：不再丢弃 `history`；用 `history_to_rewrite_block` 生成对话块。  
- [x] DDL 检索：检索串合并历史 + 当前问题（`_text2sql_retrieve_query`，长度上限 `TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`，默认 1200）。  
- [x] `build_sql_prompt`：可选 `dialogue_context`，注入「近期对话（指代消解）」说明块。  
- [x] `AgentMemoryStore.save`：内存缓存条目与 `load` 一致为 `{query, response}`，避免同进程次轮解析出空历史。

### B. 枚举 / 同义词 / 列值域提示（待实现）

- [ ] 维护可版本化的**业务字典**或**从库 DISTINCT 采样**（如 `gender`：`男`/`女`；`commission_structure`：底薪加提成、提成结构、固定佣金等），注入 `build_sql_prompt` 或独立「术语→条件」小节。  
- [ ] 明确与 DDL 文档的边界：字典为**补充真值**，不替代 `public.*` 表结构来源。  
- [ ] 可选 env：字典文件路径、是否启用 DISTINCT 探针、每列最大 distinct 条数等（具体名以 `PROJECT_CONFIG` 增补为准）。

### C. 上轮结构化锚点（已实现基线；澄清策略仍为 P1+）

- [x] 成功执行 Text2SQL 后，在 `rag_conversation_logs.tool_results` 写入 **`text2sql_grounding`**（`v`、`primary_table`、`resolved_tables`、`sql_excerpt`，由 SQL 解析，无新 DB 列）。  
- [x] 次轮 `AgentMemoryStore.load` 将 `text2sql_grounding` 合并进 `history[]`；`history_to_rewrite_block` 与 Intent 侧 assistant 正文**前缀**注入锚点行，工具侧 `call_history` 沿用原列表引用。  
- [ ] 低置信指代时的澄清策略（规格 §4.3）作为 **P1+**，不在本子任务验收内。

## 非范围

- 前端 Unified Chat `session_id` 传参与 Timeline UI（见前端任务单与 `_tech_graph`）。  
- Intent 模型选型与 60 条集准确率（见 `task_chatbi_v2_agent_p1_eval_benchmark_v1.md`）。  
- 修改 `SPEC-ChatBI-V2-Multiturn-Semantics.md` 正文（以规格为引用真值；任务单只跟踪实现）。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 多轮语义规格 | `docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md` |
| Agent 总规 §2.6 记忆 | `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` |
| Text2SQL 实现 | `api/tools.py`、`api/text2sql_core.py` |
| 会话记忆 | `api/agent_memory.py`、`api/agent.py`（`turn_history` / `call_history`） |
| 历史格式化复用 | `api/query_rewrite.py`（`history_to_rewrite_block`） |
| 样例 DDL/数据 | `docs/text2sql/v1/sql/supabase_init.sql` |

---

## 验收标准

### A（已实现，回归防回归）

- [x] 同一 `session_id` 下，首轮问「统计 agent_info 表有多少条」、次轮问「刚刚的表里多少男性」时，`text2sql` 路径的检索串或生成 prompt 中**能出现**首轮语境中的表名锚点（日志或 debug 可核对）。  
- [x] `pytest`：`tests/test_unified_chat_backend_v2_agent.py`、`tests/test_intent_cache.py` 等与 Agent 路径相关用例不因本次改动失败。

### B（待实现）

- [ ] 对「男性 / 女 / commission 口语」等用例，生成 SQL 中 **WHERE 字面量与库内枚举一致**（fixture 以 `supabase_init.sql` 或约定测试库为准）。  
- [ ] 字典或 DISTINCT 与真实库**漂移**时有文档说明（更新频率或 CI 校验策略）。

### C（已实现基线）

- [x] 自动化用例：`tests/test_text2sql_grounding.py`（表抽取、`tool_results` 块形状、`history_to_rewrite_block` 含 `[Text2SQL 锚点]`）。  
- [x] 无新 Supabase 列：沿用 `tool_results` JSONB；与 `supabase/sql/create_rag_conversation_logs.sql` 现结构一致。

---

## 实现备忘（子 Agent 回填）

| 项 | 内容 |
|----|------|
| **A 已涉及文件** | `api/tools.py`（`_text2sql_retrieve_query`、`text2sql_execute`）、`api/text2sql_core.py`（`build_sql_prompt(..., dialogue_context=)`）、`api/agent_memory.py`（`save` 缓存形状） |
| **A 新增 env** | `TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`（默认 `1200`，可选） |
| **C 已涉及文件** | `api/text2sql_grounding.py`（新建）、`api/unified_chat.py`（`_text2sql_grounding_from_agent_result` / 落库）、`api/agent_memory.py`（load 合并）、`api/query_rewrite.py`、`api/agent.py`、`tests/test_text2sql_grounding.py` |
| **B 待拆 PR** | 字典 YAML、`build_sql_prompt` 值域注入 |
| **图谱** | 若流程变更跨请求锚点，同步 `_tech_graph/` 中 Text2SQL / Agent 子流程（遵守双轨与 Mermaid 协议） |

---

## 给 Cursor 的稳定关键词

多轮、Text2SQL、`dialogue_context`、`history_to_rewrite_block`、`_text2sql_retrieve_query`、`TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`、`AgentMemoryStore`、指代消解、枚举字典、DISTINCT、resolved_table、SQL 摘要、L3、SPEC-ChatBI-V2-Multiturn-Semantics、grounding
