# PROMPT · Claude Code T1 · 后端 api 模块化 Epic（W2～W8 · 续跑）

> **Round**：T1 · **W2→W8**（W1 **done** · PR [#146](https://github.com/Cyning12/ai-ink-brain-api-python/pull/146)）  
> **MANIFEST**：[task_standards_backend_api_modularization_manifest_v1.md](../../tasks/active/task_standards_backend_api_modularization_manifest_v1.md)  
> **前置**：P3+P4 **done** [#145](https://github.com/Cyning12/ai-ink-brain-api-python/pull/145) · L2 **v1.2** · `ruff check api tests` CI Required  
> **Open Folder**：**`ai-ink-brain-api-python/` 仓根**  
> **通用模板**：[PROMPT_claude_chain_serial_v1.md](PROMPT_claude_chain_serial_v1.md)  
> **对称 Cursor 版**：[PROMPT_cursor_task_chain_serial_v1_T1_standards-backend-api-modularization-w1-w8_zh.md](PROMPT_cursor_task_chain_serial_v1_T1_standards-backend-api-modularization-w1-w8_zh.md)

---

## 0. 开跑前门禁

```bash
git checkout main && git pull origin main
test -f ruff.toml && test -f .cursor/rules/31-coding-standards-l2.mdc
ruff check api tests && pytest tests -m "not intent_eval and not intent_benchmark" -q
```

任一失败 → **BLOCKED**（只报命令与路径，不开工 W2）。

**已完成（勿重复）**：

| ID | PR | 说明 |
|----|-----|------|
| W1 | [#146](https://github.com/Cyning12/ai-ink-brain-api-python/pull/146) | `index.py` env → `rag_env` · [`done/task_api_env_rag_env_consolidation_w1.md`](../../tasks/done/task_api_env_rag_env_consolidation_w1.md) |

**Epic 纪律（MANIFEST D1～D5）**：单 PR 单主题 · 先测后拆 · 契约不变 · graph_query 先行 · ruff+pytest 绿 · **>8 个 `api/*.py` 拒合并**。

---

## 1. §3 Lead 正文（复制给 Claude Code · W2→W8 全跑）

见本文件末尾 **§8 一键复制块**。

---

## 2. Epic 批次表（W2～W8 · 当前执行范围）

| ID | 主题 | slug | git_branch | 风险 |
|----|------|------|------------|------|
| **W2** | Legacy chat 路由下沉 | `api-routes-legacy-chat-split` | `task/api-routes-legacy-w2` | Medium |
| **W3** | Admin ingest 路由下沉 | `api-routes-admin-ingest-split` | `task/api-routes-admin-w3` | Medium |
| **W4** | Unified JSON 路径 | `api-unified-json-split` | `task/api-unified-json-w4` | High |
| **W5** | Unified SSE 路径 | `api-unified-sse-split` | `task/api-unified-sse-w5` | High |
| **W6** | Agent 循环 | `api-agent-loop-split` | `task/api-agent-w6` | High |
| **W7** | Tool 注册表 | `api-tools-registry-split` | `task/api-tools-w7` | Medium |
| **W8** | Intent 栈 | `api-intent-stack-split` | `task/api-intent-w8` | Medium |

**执行顺序**：**W2 → W3 → W4 → W5 → W6 → W7 → W8**（串行 · 每批 merge 后 `pull main`）。

---

## 3. 每 W* Round（Lead 重复 7 次）

### 3.1 DRAFT_TASK

`docs/tasks/active/task_<slug>_w{n}.md` · 跑 `python tools/harness_task_validate.py <path>`

### 3.2 帽链（串行 spawn）

`explore → 22 → 30 → 40 → 50 → CLOSE → PR → CI → merge → pull main`

| 帽 | subagent | Git |
|----|----------|-----|
| explore / 22 | 只读 · 禁改 api/tests | Lead commit invoke/review |
| 30 | 实现 · **subagent 禁止 commit** | Lead commit + push |
| 40 / 50 | 验证 / 复检 | Lead commit 落盘 |
| CLOSE | `gh pr merge --squash` · task → `done/` | Lead commit 文档 |

**50 交付**：`docs/tasks/reinspect_results/<task_basename>_reinspect_*.md`（**required**）

### 3.3 W* 实现提示

| ID | 关键文件 | 测试锚点 |
|----|----------|----------|
| W2 | `api/index.py` → `api/routes/legacy_chat.py` | legacy chat/retrieve route tests |
| W3 | `api/index.py` → `api/routes/admin_ingest.py` | ingest admin tests |
| W4 | `api/unified_chat.py` → `api/unified/json_handler.py` | `test_unified_chat_backend_v1` · **_contract_manifest** |
| W5 | `api/unified_chat.py` → `api/unified/sse_handler.py` | SSE contract tests · **_contract_manifest** |
| W6 | `api/agent.py` 子模块 | agent / unified agent tests |
| W7 | `api/tools.py` 分文件 | tool registry tests |
| W8 | `api/intent_agent.py` · `intent_router.py` | `intent_*` tests |

**defer（勿偷做）**：`rag_recall_tools` · `chatbi_sql_gate` · `code_retrieval` · `ingest_pipeline` 深拆

---

## 4. EPIC_CLOSE（W8 merge 后）

- [ ] MANIFEST 验收全勾 · W1～W8 **done**
- [ ] `index.py` <400 行 · `unified_chat.py` <800 或 `api/unified/` package
- [ ] RECENT §1.5 → **CLOSE**
- [ ] 可选：`REPORT_completion_*` · Coding Wiki synthesis

---

## 5. BLOCKED

| Scenario | 行为 |
|----------|------|
| fp-mega-refactor-pr | >8 个 `api/*.py` · 拆 PR |
| fp-contract-break | W4/W5 contract 红 · 50 阻塞 |
| CI 红 | 修后重跑 40 |
| human_gate pending | 只报 gate_id |

---

## 6. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-09 | v1：W1 done 后续跑 W2～W8 · CC Lead 链 |

---

## 7. §8 一键复制块（Claude Code Lead）

```text
你 = Harness Lead（Claude Code · Epic T1 · 后端 api 模块化 W2～W8）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md（本文件 §0～§5）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/standards/CODING_BACKEND_L2_v1_zh.md（P-01 薄路由 · P-03 env 真值）

输入：
- MANIFEST：docs/tasks/active/task_standards_backend_api_modularization_manifest_v1.md
- epic：standards-engineering / api-modularization
- merge_policy：ci_green_merge（每 W* 独立 PR · Required 全绿再 merge）
- resume：W1 **done** PR #146 · 从 **W2** 开跑
- 顺序：W2 → W3 → W4 → W5 → W6 → W7 → W8

Epic 状态机：
  FOR W in [W2..W8]:
    DRAFT_TASK(W) → explore → 22 → 30 → 40 → 50 → CLOSE → PR → CI → merge → pull main
  → EPIC_CLOSE → MANIFEST done → RECENT §1.5 CLOSE

纪律：
1. Open Folder 本仓根；禁止在 main 上连续改代码
2. 每 W*：独立 git_branch（见 PROMPT §2 表）· 独立 PR · merge 后再开下一 W*
3. Git **仅 Lead**：invoke/review 落盘 → commit → spawn subagent → 收 ≤10 行；subagent **禁止** commit
4. test_strategy=required：40 后必须 50 落盘 docs/tasks/reinspect_results/
5. 单 PR 触达 >8 个 api/*.py → 拒合并 · 拆 PR
6. W4/W5 须对照 docs/_tech_graph/_contract_manifest.json
7. 合并前必绿：tech-graph + contract + pytest + ruff

开跑前自检：
git checkout main && git pull origin main
ruff check api tests && pytest tests -m "not intent_eval and not intent_benchmark" -q

W2 首批：
- 分支 task/api-routes-legacy-w2
- 目标：index 内 legacy chat/retrieve → api/routes/legacy_chat.py；index 仅 register
- 禁止 mega-refactor；先 pytest 锁行为

完成后：Epic MANIFEST 验收 · RECENT §1.5 CLOSE · HANDOFF_CLOSE_TRACE
```
