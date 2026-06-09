# PROMPT · Cursor T1 · 后端 api 模块化 Epic（W1～W8 · 串行多 task）

> **Round**：T1 · **ALL**（W1 **done** · W2→W8 续跑）  
> **MANIFEST**：[task_standards_backend_api_modularization_manifest_v1.md](../../tasks/active/task_standards_backend_api_modularization_manifest_v1.md)  
> **前置**：P3+P4 **done** [#145](https://github.com/Cyning12/ai-ink-brain-api-python/pull/145) · W1 **done** [#146](https://github.com/Cyning12/ai-ink-brain-api-python/pull/146) · L2 **v1.2**  
> **Open Folder**：**`ai-ink-brain-api-python/` 仓根**（非工作区 `Projects/`）  
> **通用模板**：[PROMPT_cursor_task_chain_serial_v1.md](PROMPT_cursor_task_chain_serial_v1.md)  
> **编排指南**（若存在）：[GUIDANCE_epic_orchestration_task_chain_v1_zh.md](../guides/GUIDANCE_epic_orchestration_task_chain_v1_zh.md)

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞 |
| --- | --- | --- |
| `HG-EPIC-P3P4` | P3+P4 已合入 `main` | 全 Epic |
| `HG-TASK-DRAFT` | 各 W* 子 task 10 帽起草后 `approved` | 该 W* 的 22/30 |

**硬前置（Lead 自检）**：

```bash
git checkout main && git pull origin main
test -f ruff.toml && test -f .cursor/rules/31-coding-standards-l2.mdc
ruff check api tests && pytest tests -m "not intent_eval and not intent_benchmark" -q
```

任一失败 → **BLOCKED**（只报命令与路径，不开工 W1）。

**Epic 纪律（MANIFEST D1～D5 · 全 W* 继承）**：

| # | 纪律 |
|---|------|
| D1 | 单 PR 单主题 · 仅动该行「目标模块」+ 直接依赖 |
| D2 | `test_strategy: required` · 拆前补/锁行为测试 |
| D3 | 对外 path / `_contract_manifest.json` 不破坏 |
| D4 | 开工前 `python tools/tech_graph_graph_query.py neighbors <node>` |
| D5 | `ruff check` + pytest 绿 |

---

## 1. §3 Lead 正文（复制给新 Agent · 一次性跑 W1～W8）

```text
你 = Harness 00 总调度（Cursor · Epic T1 · 后端 api 模块化 W1～W8）。遵循：
- ai-ink-brain-api-python/docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md
- ai-ink-brain-api-python/docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_standards-backend-api-modularization-w1-w8_zh.md（本文件 §2～§8）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/standards/CODING_BACKEND_L2_v1_zh.md（P-01 薄路由 · B-01）

输入：
- MANIFEST：docs/tasks/active/task_standards_backend_api_modularization_manifest_v1.md
- epic：standards-engineering / api-modularization
- merge_policy：ci_green_merge（每 W* 独立 PR · Required 全绿再 merge）
- planned_hats（每 W*）：explore → 22 → 30 → 40 → 50 → CLOSE → PR → CI → merge
- 执行顺序：W1 → W2 → W3 → W4 → W5 → W6 → W7 → W8（禁止跳序大改 index/unified_chat）

Epic 状态机：
  EPIC_INIT → FOR W in [W1..W8]:
    DRAFT_TASK(W) → ROUND(W) → MERGE(W) → pull main
  → EPIC_CLOSE → MANIFEST done → RECENT §1.5 CLOSE

纪律：
1. Open Folder 本仓根；禁止在 main 上连续改代码
2. 每 W*：独立 git_branch（见 §3 表）· 独立 PR · merge 后再开下一 W*
3. 每帽：invoke 落盘 → commit → Task 串行 → 收 ≤10 行；禁止子 Task 再派 Task
4. test_strategy=required：40 后必须 50 落盘 docs/tasks/reinspect_results/
5. 单 PR 触达 >8 个 api/*.py 且无 MANIFEST 授权 → 拒合并 · 拆 PR（fp-mega-refactor-pr）
6. 禁止代签 human_gate；W4/W5 须对照 _contract_manifest.json
7. 合并前必绿：tech-graph + contract + pytest + ruff

开跑前：确认 PR #145 已在 main；更新 RECENT §1.5 P3+P4 → done（若尚未归档 task）

完成后：Epic MANIFEST 验收勾选 · RECENT §1.5 CLOSE · 可选 Coding Wiki synthesis
```

---

## 2. Epic 批次表（W1～W8 · slug / 分支 / 风险）

| ID | 主题 | 建议 slug | git_branch | 风险 | 帽链 |
|----|------|-----------|------------|------|------|
| **W1** | `rag_env` 收敛 | `api-env-rag-env-consolidation` | `task/api-env-rag-env-w1` | Low | explore→22→30→40→50→CLOSE |
| **W2** | Legacy chat 路由下沉 | `api-routes-legacy-chat-split` | `task/api-routes-legacy-w2` | Medium | 同上 |
| **W3** | Admin ingest 路由下沉 | `api-routes-admin-ingest-split` | `task/api-routes-admin-w3` | Medium | 同上 |
| **W4** | Unified JSON 路径 | `api-unified-json-split` | `task/api-unified-json-w4` | High | 同上 |
| **W5** | Unified SSE 路径 | `api-unified-sse-split` | `task/api-unified-sse-w5` | High | 同上 |
| **W6** | Agent 循环 | `api-agent-loop-split` | `task/api-agent-w6` | High | 同上 |
| **W7** | Tool 注册表 | `api-tools-registry-split` | `task/api-tools-w7` | Medium | 同上 |
| **W8** | Intent 栈 | `api-intent-stack-split` | `task/api-intent-w8` | Medium | 同上 |

**并行约束**：W2∥W3、W4∥W5 理论上可并行，但 **本 Prompt 要求串行**（降低冲突 · 每批 pull main）。

---

## 3. 每 W* Round 循环（Lead 重复 8 次）

### 3.1 DRAFT_TASK（10 帽 · 若 `active/task_*` 不存在）

在 `docs/tasks/active/` 新建，文件名示例：`task_api_env_rag_env_consolidation_w1.md`。

**必填 frontmatter 块**（复制 MANIFEST §子 task 文档模板）：

```markdown
> **epic**：`standards-engineering/api-modularization`
> **manifest_ref**：W{n} · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**：`required`
> **非范围**：MANIFEST 表内未列出的 `api/*.py` 文件
```

Harness 元信息表须含：`task_slug` · `git_branch` · `orchestration: Cursor Task 链` · `chain_prompt: 本文件` · `freeze_id: CODING_BACKEND_L2@2026-06-09`

跑：`python tools/harness_task_validate.py docs/tasks/active/<task>.md`

### 3.2 ROUND(Wn) — 帽链

#### explore（`Task` · explore · 只读）

**invoke**：`docs/harness/invokes/by-task/<slug>/invoke_*_explore_*.md`

```text
【角色】Harness explore · W{n} · 只读

【读序】
1. MANIFEST W{n} 行 + L2 P-01
2. 目标文件 wc -l · 顶层 import / os.getenv 散落点
3. python tools/tech_graph_graph_query.py neighbors <相关 node>
4. tests/ 内已有覆盖（route / handler / 纯函数）

【forbidden】改 api/** · tests/** · 扩 scope 到 MANIFEST 外模块

【交付】explore_<slug>_gap.md（影响面 · 建议抽离函数列表 · 测试缺口）
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

#### 22（`Task` · harness-22-audit 或 generalPurpose 只读审查）

**交付物**：`docs/harness/reviews/by-task/<slug>/task_*_audit_R1_*.md`

```text
【角色】Harness 22 · R1

【审查】D1 范围 · D2 测试计划 · D3 契约 · failure_paths · 是否 mega-refactor
【禁止】改 api/ · 代签 gate
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

#### 30（`Task` · generalPurpose · **实现帽**）

```text
【角色】Harness 30 · 实现 · W{n}

【读序】task · R1（无阻塞）· explore · L2 P-01

【必须】
- 先补/锁 pytest（行为不变）
- 再抽模块 / 迁 import；index 或 unified 仅 register
- ruff check api tests 绿
- 若改拓扑：更新 docs/_tech_graph 对应 flow + graph.json 导出

【forbidden】MANIFEST 非范围 api/*.py · 改 HTTP 契约（除非 task 明示）· git commit

【回报】Status / Deliverables（文件清单）/ Blockers / Judgment（各≤10行）
```

Lead：收报告后 `git add` 范围路径 → commit → `git push` 开 PR。

#### 40（`Task` · harness-40-check 或 shell）

```text
【角色】Harness 40 · 自检

【验证】
- pytest tests -m "not intent_eval and not intent_benchmark"
- ruff check api tests
- python tools/harness_task_validate.py <task_path>
- bash scripts/verify-pr-local.sh（可选 · 与 CI 对齐）

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

#### 50（`Task` · harness-50-reinspect · **required**）

**交付物**：`docs/tasks/reinspect_results/<task_basename>_reinspect_*.md`

```text
【角色】Harness 50 · 独立复检

【验证】契约未破坏 · 测试覆盖拆分点 · diff 仅 MANIFEST 授权范围
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

#### CLOSE(Wn)

Lead：

1. `gh pr checks --watch` → Required 全绿  
2. `gh pr merge --squash`（无 automerge · 含 api/tests）  
3. `git checkout main && git pull`  
4. `git mv` task → `docs/tasks/done/` · 更新 `_views/done.md` · MANIFEST 表 W{n} 行注 **done**  
5. invoke CLOSE + commit（`HANDOFF_CLOSE_TRACE`）

---

## 4. W* 实现提示（非强制 · 供 30 帽参考）

| ID | 目标摘要 | 关键文件 | 测试锚点 |
|----|----------|----------|----------|
| W1 | `index` 顶散落 env → `rag_env` helper | `api/rag_env.py`, `api/index.py` | env 读取单测 / mock |
| W2 | chat/retrieve → `api/routes/legacy_chat.py` | `api/index.py` | `test_unified_chat_*` · legacy route |
| W3 | admin/sync → `api/routes/admin_ingest.py` | `api/index.py`, `ingest_pipeline` 边界 | ingest admin tests |
| W4 | JSON handler → `api/unified/json_handler.py` | `api/unified_chat.py` | `test_unified_chat_backend_v1` |
| W5 | SSE stream → `api/unified/sse_handler.py` | `api/unified_chat.py` | SSE contract tests |
| W6 | tool 调度 / persist 子模块 | `api/agent.py` | agent e2e / unified agent tests |
| W7 | text2sql vs RAG tools 分文件 | `api/tools.py` | tool registry tests |
| W8 | intent 表驱动 vs LLM 分文件 | `api/intent_agent.py`, `intent_router.py` | intent_* tests |

**显式 defer**（MANIFEST · 勿在本 Epic 偷做）：`rag_recall_tools` · `chatbi_sql_gate` · `code_retrieval` · `ingest_pipeline` 深拆

---

## 5. EPIC_CLOSE（W8 merge 后）

- [ ] MANIFEST Epic 验收标准全勾（或 defer 行 + 人签）  
- [ ] `index.py` <400 行 · `unified_chat.py` <800 或 `api/unified/` package  
- [ ] `git mv` MANIFEST → `docs/tasks/done/`（或保留 active 仅改 status **done** · 按 task README）  
- [ ] RECENT §1.5 编码规范 Epic → **CLOSE**  
- [ ] invoke `REPORT_completion_*`（可选 · 长 Loop 见 SKILL-harness-loop-batch）

---

## 6. 失败与 BLOCKED

| Scenario | 行为 |
|----------|------|
| fp-mega-refactor-pr | >8 个 `api/*.py` · 拆 PR |
| fp-contract-break | W4/W5 · pytest contract 红 · 50 阻塞 |
| fp-manifest-skip-order | 未 W1 即 index 大改 · 22 要求回退 |
| CI 红 | BLOCKED · 修后重跑 40 |
| human_gate pending | 只报 gate_id · 不 Task |

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-09 | v1：Epic W1～W8 Cursor 串行链 · 前置 P3+P4 #145 |
