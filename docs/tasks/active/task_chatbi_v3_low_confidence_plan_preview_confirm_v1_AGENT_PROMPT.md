# 执行 Agent 任务交代：agent.py「方案 B」编排修正（P2 延伸 · 首包可只做本项）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本文件无 Wiki 增量（2.19 lint-wiki-delta） |


> **状态（2026-05-13）**：首包已在主任务单 **§5.0** 记为 **已验收**；若续拆 PR 请读 **`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`** **§5.1**（仍 backlog）。  
> **用途**：将本文件 **全文**复制给负责改代码的 Cursor Agent（或本对话续写），作为单一真值输入。  
> **仓库**：`ai-ink-brain-api-python`  
> **允许修改**：**`api/agent.py`（主战场）**；若 pytest 断言依赖 Timeline 字段，可改 **`tests/test_unified_chat_backend_v2_agent.py`**。  
> **本包不做**：SQL 草案生成、`plan_execution_token`、RAG 低置信扩展、manifest 新键（除非契约检查明确要求）；见 `docs/spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md` 全文能力另开 PR。

---

## 1. 背景（问题陈述）

当 **`CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1`** 且 **`prefer=auto`**、意图为 **`text2sql_query`**、**`intent.confidence < INTENT_MIN_CONFIDENCE`** 时：

1. 现有逻辑在 **418–426 行** 先把 **`step1_tool`** 换成 **`intent.fallback`**（常为 `rag_search`），故 **`step1_mode`** 变为 **`rag`**。  
2. **G2 emit** 在 **471–485 行** 发出 **`router.decision`**，其中 **`final_mode = step1_mode`** → Timeline 出现 **`final_mode: rag`**。  
3. 随后在 **603–666 行** **P1-4 澄清短路** 直接 **`return`**，**从未执行 RAG**。  

结果：观测上像「已路由到 RAG」，实际 **无任何工具调用**，与留档 `docs/spec/v3-agent/text2sql/P1-4-第二次对话测试.md` 一致，**易误解**。

**需求规（方案 B 摘要）**：澄清 / 将被短路的路径，在 **`router.decision`** 上 **不应**再表现为「已切到 rag 执行」；**`final_mode`** 应与 **真实意图候选**一致，或显式 **`held`**（本首包优先用 **`final_mode = intent.mode`**，**不新增** payload 键，避免动 `_contract_manifest.json`）。

---

## 2. 目标行为（验收口径）

- 在满足 **P1-4 澄清短路** 条件且 **`emit is not None`** 时，**`router.decision`** 的 **`final_mode`** 与 **`candidate_mode`** 一致（均为 **`intent.mode`**，对 `text2sql_query` 即 **`text2sql`**），**不再**出现 **`candidate_mode: text2sql` + `final_mode: rag`** 且随后无 `rag_search` 执行的组合。  
- **不改变**澄清是否触发：条件仍为现有 **`CHATBI_V3_LOW_CONFIDENCE_CLARIFY`** + **`prefer==auto`** + **`intent.tool=="text2sql_query"`** + **`confidence < self._min_confidence`**。  
- **`step1_tool` / `current_tool`** 在 **未**走澄清短路、进入 **`for step_idx`** 时，行为与 **改前一致**（低置信仍可先走 fallback 工具链——仅修正 **emit 的观测语义**，除非你与产品确认要把执行首步也锁在 `intent.tool` 上，**本任务不要求改执行首步**）。  
- **`python -m pytest tests/test_unified_chat_backend_v2_agent.py -q`** 全绿；若有断言写死 `final_mode == "rag"`，按新语义更新。  
- **`python tools/tech_graph_contract_check.py`** 通过（**不**增删 `router.decision` 的 **payload 键名**，只改 **`final_mode` 字符串取值** 时一般无需改 manifest）。

---

## 3. 实现要点（建议实现顺序）

1. **提前计算**与 **603–611 行** 完全相同的 **`_clarify_eligible`**（或同名变量），位置放在 **`step1_fallback` / `step1_tool` / `step1_mode` 赋值完成之后**、**`if emit is not None:` 的 G2 emit 块（约 439 行）之前**，保证 **`prefer` 强制路径** 与 **`auto` + `decide_intent_v2`** 两条分支都已写完 **`intent`**。  
2. 在 **`router.decision`** 的 **`payload`** 构造处（约 **471–472 行**）：  
   - 若 **`_clarify_eligible`** 为真，则 **`final_mode`** 使用 **`intent.mode`**（与 **`candidate_mode`** 一致）；  
   - 否则保持 **`final_mode = step1_mode`**。  
3. **删除**原 **603–611 行** 对 **`_clarify_eligible`** 的 **重复计算**，改为使用步骤 1 的变量（避免两处条件漂移）。  
4. 在 **`agent.py`** 内用 **简体中文** 加 **1–3 行**注释，说明：**P2 延伸 / 方案 B** —— 澄清短路前 **`router.decision`** 的 **`final_mode`** 表示「意图候选」而非「即将执行的 fallback 工具」，避免假 **rag**。  
5. 自测后跑 **§2** 中两条命令。

---

## 4. 关键代码锚点（改前真值）

文件：`api/agent.py` → `ChatBIAgent.run`

- **`step1_tool` / fallback**：约 **418–426** 行。  
- **`router.decision` emit**：**`_cand_mode` / `_final_mode`**，约 **471–485** 行。  
- **P1-4 澄清**：约 **603–666** 行（`CHATBI_V3_LOW_CONFIDENCE_CLARIFY`）。

---

## 5. 非范围（勿顺手做）

- 不实现 **`agent.plan.preview`**、不生成 **SQL 草案**、不发 **`plan_execution_token`**（见规格 **`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`**）。  
- 不扩展 **`rag_search`** 低置信澄清（当前门控仅 **`text2sql_query`**）。  
- 不做大范围重构；**diff 尽量集中在上述锚点**。

---

## 6. 回填

完成后在 **`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`** 的 **§6 实现备忘** 写明：PR 链接、改动文件列表、是否更新 pytest 用例名/断言。

---

## 7. 给 Cursor 的稳定关键词

`agent.py`、`router.decision`、`final_mode`、`方案B`、`_clarify_eligible`、`CHATBI_V3_LOW_CONFIDENCE_CLARIFY`、`P1-4`、`task_chatbi_v3_low_confidence_plan_preview_confirm_v1`
