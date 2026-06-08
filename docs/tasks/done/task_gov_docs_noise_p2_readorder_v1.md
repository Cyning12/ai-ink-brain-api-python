# Task：docs-noise 治理 · P2 读序对齐与 legacy 消化

> **状态**：`done（2026-06-06 · PR #126 @ 08d51bd）`
> **Epic**：docs-noise 治理线 · **P2**（Claude Code 串行 Task 链）
> **关联 SPEC 导图**：[`docs/spec/governance/docs-noise-inventory/README.md`](../spec/governance/docs-noise-inventory/README.md)
> **关联 SPEC 正文**：[`docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md`](../spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md) §8.3
> **freeze_id**：`GOV-DOCS-NOISE-INVENTORY@2026-06-06`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `gov_docs_noise_p2_readorder_v1` |
| **orchestration** | **Claude Code** · Lead 主会话 + **串行 spawn** `.claude/agents/harness-*` |
| **semi_auto** | `true` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs 指针修正；无 `api/` / 契约 / CI workflow 变更 |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-docs-noise-p2-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **blocked_by** | P1（`done` · PR #123 @ `2de2902`） |
| **blocks** | P3 子批（未建） |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **merge_policy** | `docs_only_ci_green_merge` |
| **close_action** | `merge` — CI Required 全绿后 **00/CLOSE 可执行** `gh pr merge --squash` |
| **experience_capture** | `recommended` |
| **experience_capture_note** | 执行简报落盘 diary；关账后可蒸馏 P2 PROMPT 惯例 |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1, 30 | task 草案人扫；纯 docs 可预批后直进 30 |
| HG-GOV-P2-EXEC | approved | explore, 22, 30, 40, CLOSE | P2 执行链开干前人签 |

---

## 背景与目标

P0 已修 C1–C3 真冲突；P1 已为 `delivery/`、`flows/` 加 archived / superseded 标注。P2 聚焦 **导航入口收敛** 与 **legacy 任务消化**，解决 SPEC §8.3 所列四项：

- **C4**：`PROJECT_CONFIG` 仍提 `.cursorrules`（已不存在）→ P2-1
- **C5**：根 `README.md` Unified Chat 端点 / 关键 env 不完整 → P2-3
- **C2 复核**（P0 已修 flows 降级）：P2-2 补 AGENTS ↔ `docs/README` **互链**与 **canonical 读序子集**对齐（不要求 docs/README 全节逐步一致）
- **C6**（`HARNESS_V2_PLAN` vs `AGENTS` 权威链）：**本批非范围**，留 P3 或单独小修
- `docs/tasks/legacy/` 6 份缺状态 / 未入 `_views/` → P2-4

**完成态**：

- `PROJECT_CONFIG` §B 更新为 `.cursor/rules/*.mdc` 真值，移除 `.cursorrules` 过时表述
- `AGENTS.md` 与 `docs/README.md` §1 **canonical 子集**一致、**双向互链**；docs/README 保留 UI/text2sql/diary 等扩展导航条
- 根 `README.md` 补充 Unified Chat 端点指针（或明确「完整契约见 PROJECT_CONFIG §F」）
- `docs/tasks/legacy/` 6 文件消化：移 `done/` 或标 `archived` + `_views/` 索引更新

---

## 范围（P2）

| ID | 交付 | 文件 | 现状 |
|----|------|------|------|
| **P2-1** | `PROJECT_CONFIG` 更新 `.cursorrules` 段落 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §B | `.cursorrules` 已不存在；当前规则载体为 `.cursor/rules/*.mdc` |
| **P2-2** | `AGENTS.md` 与 `docs/README.md` 互链 §7 读序 | `AGENTS.md` + `docs/README.md` | AGENTS 已推 `_tech_graph`；docs/README 可能有 legacy 读序 |
| **P2-3** | 根 `README.md` Unified Chat pointer | `README.md` | 端点/env 不完整（缺 `/api/py/unified/chat`、`/api/py/unified/chat/stream` 等） |
| **P2-4** | 消化 `docs/tasks/legacy/`（6 文件） | `docs/tasks/legacy/` 6 文件 | 无统一状态字段，未进入 `_views/` 索引 |

### P2-1 内容要求（SPEC §8.3）

- `PROJECT_CONFIG` §B「Cursor / Agent 规则」段落：
  - 将 `.cursorrules` 描述从「仍常保留」改为「**已移除**；若外部引用仍以 `.cursorrules` 为准，须迁移至 `.cursor/rules/*.mdc`」
  - 确认 `.cursor/rules/*.mdc` 为「当前推荐的人类/Agent 真值入口」
  - 保留 `.cursor/rules` 要点摘要（RAG 日志、pgvector Cosine、session_id、Legacy vs Unified 端点区分、Hybrid 融合）
- 同步更新 `PROJECT_CONFIG` **§A L17**（若仍写 `.cursorrules` 为兼容/历史参考，改为「已移除；真值 `.cursor/rules/*.mdc`」）

### P2-2 内容要求（SPEC §8.3 · 子集对齐）

**角色区分**：

- `AGENTS.md` = Agent **最小读序地图**（7 步，含 `.mdc` / harness / Wiki / 跨仓）
- `docs/README.md` §1 = **docs 分类导航**（可含扩展条目）；**不要求**与 AGENTS 逐步完全一致

**Canonical 子集**（须与 SPEC §7 / 导图 §5 一致，且在两文件 **§1 前 5 条**对齐）：

1. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
2. `docs/_tech_graph/`（`graph_query` 按需）
3. `docs/tasks/RECENT_TASK_SCHEDULE.md` → `active/task_*.md`（docs/README 可写 `_views/` 入口，语义等价）
4. 涉 ChatBI → `docs/spec/v3-agent/`（docs/README 扩展条可保留）
5. 关账回顾 → `docs/coding_wiki/`（AGENTS 写 `index.md` / syntheses 指针）

**AGENTS.md 必做**：

- 保持现有 7 步地图；在「必读」节末或「非必读」节前增加显式互链：`docs/README.md` §1
- 可选：增加一行 pointer 至 SPEC §7 canonical（导图或正文）

**docs/README.md §1 必做**：

- **前 3–5 条**按上表 canonical 子集重写/排序（PROJECT_CONFIG → `_tech_graph` → tasks 入口）
- `docs/flows/` 保持 **Legacy · 非 L0**（P0 已降级，勿改回「当前入口」）
- 在 §1 末或文首增加显式互链：`AGENTS.md`
- **保留** UI / text2sql / diary / PR spec 等扩展条（不删）

### P2-3 内容要求（SPEC §8.3）

- 根 `README.md`「Endpoints」段落：
  - 补充 `POST /api/py/unified/chat`（JSON `events[]`）
  - 补充 `POST /api/py/unified/chat/stream`（SSE 事件链）
  - 补充 `GET /api/py/chat/history`（已存在但可能缺失）
  - 或统一改为：「完整端点与契约见 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §F」
- 根 `README.md`「Required Environment Variables」：
  - 补充 `CHATBI_*` 系列关键 env（至少 `CHATBI_USE_AGENT`、`CHATBI_PROMPT_GUARD_MODE`）或改为 pointer

### P2-4 内容要求（SPEC §8.3）

> **explore 必做**：`task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` 须 `rg rag_fts_alias supabase/`（或等价）判定 done vs archived；**禁止** 30 帽无证据 `git mv`。

- 对 `docs/tasks/legacy/` 6 文件逐一判定：

| 文件 | 判定建议 | 动作 |
|------|----------|------|
| `Task 04.md` | 引用溯源已实现（sources header + 流末尾分隔符） | `git mv` → `done/` + 补状态字段 `done` |
| `task_03_hybrid_search_implementation.md` | Hybrid Search（Vector + FTS + RRF）已落地 | `git mv` → `done/` + 补状态字段 `done` |
| `task_rag_b1_metadata_structured_recall_v1.md` | metadata `date_norm` 已落地 | `git mv` → `done/` + 补状态字段 `done` |
| `task_rag_b2_fts_alias_backfill_v1.md` | FTS alias（日期）已落地 | `git mv` → `done/` + 补状态字段 `done` |
| `task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` | FTS alias v2（分隔符/版本号/标识符）部分落地 | 若代码/SQL 已合入 → `done/`；若仅设计 → 保留 `legacy/` 但补 `状态: archived` + pointer |
| `task_rag_keyword_websearch_date_normalize_v1.md` | keyword `websearch_to_tsquery` + 日期归一化已落地 | `git mv` → `done/` + 补状态字段 `done` |

- 更新 `docs/tasks/_views/done.md` 索引（新增条目）
- 若 `legacy/` 清空，可在 `docs/tasks/README.md` 中标注「legacy 已消化，新增任务直接落 `active/`」

---

## 非范围

- **不** 删除 `docs/harness/invokes/`、`reviews/`、`reinspect_results/` 历史全文
- **不** 重写 `docs/tasks/done/` 已有 113 份 task 正文
- **不** 改 `api/`、`tests/`、`.github/workflows/`
- **不** 执行 P3 治理（SPEC 收敛 / showcase 索引）
- **不** 修改 SPEC 正文或导图 README 的冲突寄存器状态（P2 非真冲突，属读序对齐）
- **不** 要求 legacy 文件内容全文重写（仅补状态字段 + 必要时加 pointer）
- **不** 在本批解决 **C6**（`HARNESS_V2_PLAN.md` vs `AGENTS.md` 权威链互链 — 留 P3 或单独 task）
- **不** 要求 `docs/README.md` §1 与 `AGENTS.md` **逐步完全一致**（扩展导航条保留）

---

## 行为变更（Delta）

**无对外行为变更** — 纯 docs 指针与索引修正。相对现网增量：

### ADDED

- **Requirement**：`AGENTS.md` 与 `docs/README.md` 须 **双向互链**，且 **canonical 读序子集**一致
  - **Scenario**：`sc-p2-agents-docs-readme-link` — GIVEN Agent 打开 AGENTS.md WHEN 读「必读」节 THEN 看到指向 docs/README §1 的互链；打开 docs/README §1 THEN 看到指向 AGENTS.md 的互链；且两文件前 5 条与 SPEC §7 子集一致
- **Requirement**：根 `README.md` 须含 Unified Chat 端点 pointer
  - **Scenario**：`sc-p2-root-readme-unified` — GIVEN 新人打开根 README WHEN 浏览 Endpoints THEN 看到 Unified Chat 端点或「完整契约见 PROJECT_CONFIG §F」pointer
- **Requirement**：`docs/tasks/legacy/` 6 文件须进入 `_views/` 索引
  - **Scenario**：`sc-p2-legacy-indexed` — GIVEN 打开 `docs/tasks/_views/done.md` WHEN 浏览条目 THEN 看到 P2-4 消化的 6 份任务（或其中已完成的子集）

### MODIFIED

- **Requirement**：`PROJECT_CONFIG` §B 更新 `.cursorrules` 描述为「已移除」（Previously: 「仍常保留」）
  - **Scenario**：`sc-p2-project-config-cursorrules` — GIVEN Agent 读取 PROJECT_CONFIG §B WHEN 查看 Cursor 规则载体 THEN 知悉 `.cursorrules` 已不存在，真值为 `.cursor/rules/*.mdc`

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| SPEC 导图 | `docs/spec/governance/docs-noise-inventory/README.md` §5 · §8.3 |
| SPEC 正文 | `docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md` §8.3 |
| P1 precedent | `docs/tasks/done/task_gov_docs_noise_p1_archived_v1.md` |
| MANIFEST | `docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md` |
| T2c PROMPT | [`docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md) |
| PROJECT_CONFIG 目标文件 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（已存在） |
| AGENTS.md 目标文件 | `AGENTS.md`（已存在） |
| docs/README 目标文件 | `docs/README.md`（已存在） |
| 根 README 目标文件 | `README.md`（已存在） |
| legacy 目标文件 | `docs/tasks/legacy/*`（6 文件） |
| _views 目标文件 | `docs/tasks/_views/done.md`（已存在） |

---

## 失败路径

| # | Scenario ID | 触发 | 系统行为 | 可重试 | 用户可见 | 测试 |
|---|-------------|------|----------|--------|----------|------|
| F1 | `fp-gov-p2-project-config-misstate` | PROJECT_CONFIG 仍写 `.cursorrules` 为「当前有效」 | 30 执行帽拒交付；回退修正为「已移除」 | 是（人工补） | PR review 阻塞 | — |
| F2 | `fp-gov-p2-readme-diverge` | AGENTS.md 与 docs/README.md 读序仍不一致（如一个推 `_tech_graph`、一个推 `flows/`） | 22 审核帽拒过；回退至 SPEC §7 表述对齐 | 是 | PR review 阻塞 | — |
| F3 | `fp-gov-p2-root-readme-stale` | 根 README 端点仍缺 Unified Chat 且无 pointer | 30 执行帽拒交付；回退补 pointer | 是（人工补） | PR review 阻塞 | — |
| F4 | `fp-gov-p2-legacy-lost` | legacy 文件被误删（而非 `git mv` 到 done/ 或补状态字段） | **禁止**；仅做索引迁移或状态标注 | — | — | — |
| F5 | `fp-gov-p2-views-miss` | `_views/done.md` 未更新，导致 legacy 消化后索引仍缺失 | 40 自检帽拒 CLOSE；回退补索引 | 是 | — | `rg` 验证 |
| F6 | `fp-gov-p2-scope-creep` | T2c 执行时越界改 `api/`、`tests/`、CI workflow | 40 自检帽拒 CLOSE；diff 回滚 | 是 | — | `git diff --stat` |
| F7 | `fp-gov-p2-ci-red` | docs-only PR 触发 CI 异常（参考 P0/P1 教训） | 按 `merge_policy: docs_only_ci_green_merge` 阻塞 merge；排查后重跑 | 是 | PR status 红 | CI Required checks |

> **P0/P1 CI 教训**：P0 执行中 `harness_task_validate` 首轮红（`05be476` 修复）；P1 已验证 docs-only 变更的 CI 路径过滤。P2 须预检：若 docs-only 变更意外触发 api/tests 相关 CI，先排查 workflow 路径过滤，不强行 merge。

---

## 验收标准

- [ ] P2-1：`PROJECT_CONFIG` §B `.cursorrules` 描述已更新为「已移除」；`.cursor/rules/*.mdc` 为当前真值入口
- [ ] P2-1：PROJECT_CONFIG 要点摘要（RAG 日志、pgvector、session_id、Legacy/Unified 区分、Hybrid）保留未删
- [ ] P2-2：`AGENTS.md` 与 `docs/README.md` §1 **canonical 子集**（前 3–5 条）与 SPEC §7 一致
- [ ] P2-2：`AGENTS.md` ↔ `docs/README.md` **双向互链**存在；docs/README 扩展导航条保留
- [ ] P2-3：根 `README.md` Endpoints 含 Unified Chat 端点（或明确 pointer 至 PROJECT_CONFIG §F）
- [ ] P2-3：根 `README.md` env 列表含关键 `CHATBI_*` 项（或明确 pointer）
- [ ] P2-4：`docs/tasks/legacy/` 6 文件已消化（移 `done/` 或标 `archived` + 补状态字段）
- [ ] P2-4：`docs/tasks/_views/done.md` 已更新，包含 P2-4 消化条目
- [ ] 未删 `docs/harness/invokes/`、`reviews/`、`reinspect_results/` 历史全文
- [ ] 未改 `api/`、`tests/`、`.github/workflows/`
- [ ] 关账时更新 [`docs/spec/governance/docs-noise-inventory/README.md`](../../spec/governance/docs-noise-inventory/README.md) 冲突寄存器 **C4、C5** 为 `done`（C6 不改）
- [ ] 单 PR · docs-only · CI Required 全绿

**测试 / TDD**：

| test_strategy | 自检须含 |
|---------------|----------|
| `not_applicable` | `test_strategy_note` 已说明；自检以 `git diff --stat` + `rg` 验证为主 |

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md`）。

---

## 规划 artifact

### 规划摘要

- **Intent**：收敛导航入口读序（PROJECT_CONFIG / AGENTS / docs/README / 根 README），消化 legacy 任务索引缺口
- **Scope / 非范围**：见上文；核心约束「不删历史正文、不改 api/tests/workflows、legacy 仅做索引迁移」
- **Approach**：四核心 README 最小扰动（PROJECT_CONFIG §A/B、AGENTS、docs/README、根 README）+ 6 文件 legacy 索引迁移 + `_views/done.md` 更新（diff 大于 P1，30 帽禁止改 legacy 正文全文）

### 实施清单（T2c 执行用）

- 1.1 确认 `PROJECT_CONFIG` §B 当前 `.cursorrules` 表述（读 20 行）
- 1.2 修改 `.cursorrules` 描述为「已移除」；确认 `.cursor/rules/*.mdc` 为真值
- 2.1 确认 `AGENTS.md` 当前读序（读 §7 附近）
- 2.2 确认 `docs/README.md` §1 当前读序
- 2.3 对齐两文件读序；在各自文末/§7 加互链 pointer
- 3.1 确认根 `README.md` 当前 Endpoints / env 列表
- 3.2 补充 Unified Chat 端点（或 pointer）；补充关键 `CHATBI_*` env（或 pointer）
- 4.1 `ls docs/tasks/legacy/` 确认 6 文件清单
- 4.2 逐文件判定：已落地 → `git mv` done/ + 补状态 `done`；仅设计 → 补 `archived` + pointer
- 4.3 更新 `docs/tasks/_views/done.md` 索引
- 4.4 若 legacy/ 清空，更新 `docs/tasks/README.md` 标注
- 5.1 `git diff --stat` 确认仅 docs 目录变更
- 5.2 `rg` 验证互链存在、`.cursorrules` 表述已更新、legacy 已消化
- 6.1 40 帽自检 → 建议 CLOSE + PR
- 6.2 CLOSE → `gh pr create` → CI 绿 → `gh pr merge --squash`
- 6.3 `git mv` task → `done/` + 更新 `_views/done.md`

---

## 实现备忘（T2c 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（改）、`AGENTS.md`（改）、`docs/README.md`（改）、`README.md`（改）、`docs/tasks/legacy/*`（6 文件 · 移/改）、`docs/tasks/_views/done.md`（改） |
| 关键 env | 无 |
| SQL 执行顺序 | 无 |
| 接口变更 | 无 |
| 图谱变更点 | 无 |

---

### 自检结论（执行者）

> 30 帽执行回填 · 2026-06-06

#### 文件变更清单

- **P2-1**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
  - §A L17：`.cursorrules` 表述从「兼容/历史参考」改为「已移除；真值 `.cursor/rules/*.mdc`」
  - §B 表格：`.cursorrules` 改为「已移除」；`.cursor/rules/*.mdc` 为当前真值入口
  - 保留 `.cursor/rules` 要点摘要（RAG 日志、pgvector Cosine、session_id、Legacy/Unified 区分、Hybrid 融合）
- **P2-2**：
  - `AGENTS.md`：必读第 7 条后增加显式互链 `docs/README.md §1`
  - `docs/README.md`：§1 前 5 条按 canonical 子集排序（PROJECT_CONFIG → `_tech_graph` → tasks → ChatBI spec → coding_wiki），文首增加显式互链 `AGENTS.md`；保留 UI/text2sql/diary/PR spec 等扩展条
- **P2-3**：`README.md`
  - Endpoints 段落补充 `POST /api/py/unified/chat` 与 `POST /api/py/unified/chat/stream`
  - 增加 pointer「完整端点与契约见 PROJECT_CONFIG §F」
  - env 段落补充 `CHATBI_USE_AGENT`、`CHATBI_PROMPT_GUARD_MODE`，并增加 pointer「完整环境变量表见 PROJECT_CONFIG §C」
- **P2-4**：
  - `git mv` 6 份 legacy 文件至 `docs/tasks/done/`：
    - `Task 04.md`
    - `task_03_hybrid_search_implementation.md`
    - `task_rag_b1_metadata_structured_recall_v1.md`
    - `task_rag_b2_fts_alias_backfill_v1.md`
    - `task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md`
    - `task_rag_keyword_websearch_date_normalize_v1.md`
  - 每文件文首补 `状态: done` + 归档说明
  - `docs/tasks/_views/done.md` 新增 6 条条目

#### `git diff --stat` 输出

```
 AGENTS.md                                                        | 2 ++
 README.md                                                        | 8 ++++++++
 docs/README.md                                                   | 9 ++++++---
 docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md              | 8 ++++----
 docs/tasks/_views/done.md                                        | 6 ++++++
 docs/tasks/done/Task 04.md                                       | 3 +++
 docs/tasks/done/task_03_hybrid_search_implementation.md          | 3 +++
 docs/tasks/done/task_rag_b1_metadata_structured_recall_v1.md     | 3 +++
 docs/tasks/done/task_rag_b2_fts_alias_backfill_v1.md             | 3 +++
 .../task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md     | 3 +++
 docs/tasks/done/task_rag_keyword_websearch_date_normalize_v1.md  | 3 +++
 11 files changed, 44 insertions(+), 7 deletions(-)
```

#### 范围校验

- `git diff --stat HEAD -- api/ tests/ .github/workflows/`：无输出（未改动受限路径）
- `ls docs/tasks/legacy/`：空（legacy 已消化）
- 未删除 `docs/harness/invokes/`、`reviews/`、`reinspect_results/` 历史
- 未修改 legacy 正文全文（仅补状态字段 + 归档说明）

---

### 自检结论（40 帽回填 · T2c 后）

> **40 自检帽** · 2026-06-06

| 项 | 命令输出要点 | 结论 |
|----|--------------|------|
| `rg -n '\.cursorrules.*当前\|仍.*保留\|仍常保留' docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 无输出（未命中任何遗留表述） | 绿 |
| `rg -n 'AGENTS\.md\|docs/README\.md' AGENTS.md docs/README.md` | `AGENTS.md` L18 → `docs/README.md` §1；`docs/README.md` L6 → `AGENTS.md` | 绿 |
| `rg -n 'unified/chat\|PROJECT_CONFIG.*§F' README.md` | L12 命中 `POST /api/py/unified/chat` 与 `PROJECT_CONFIG §F` pointer | 绿 |
| `git diff --stat HEAD~2 -- api/ tests/ .github/workflows/` | 无输出（受限路径无变更） | 绿 |
| `ls docs/tasks/legacy/` | 无输出（目录已空 / 不存在，legacy 已消化） | 绿 |
| `rg -n 'task_rag_b\|task_03\|Task 04' docs/tasks/_views/done.md` | L8–13 命中 6 条条目（task_rag_b* / task_03 / Task 04） | 绿 |

**结论**：6 项检查全绿，无阻塞。建议 **CLOSE + PR / merge**。

---

### KPI（00 / CLOSE 回填）

> **rubric**: KPI_RUBRIC_v1_2 · **汇总**: 待填 · **状态**: 待填
> **评诊日期**: 待填

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
|----------|-------|------------|----|----|----|----|----|----------------|
| T0/10 | T0 | task_subagent | — | — | — | — | — | 写本 task + invoke |
| explore | R1 | task_subagent | — | — | — | — | — | 待填 |
| 22 | R1 | task_subagent | — | — | — | — | — | 待填 |
| 30 | R1 | task_subagent | — | — | — | — | — | 待填 |
| 40 | R1 | task_subagent | — | — | — | — | — | 待填 |
| CLOSE | close | main_chat | — | — | — | — | — | 待填 |

---

## Claude Code 执行编排

### Round 表

| Round | 帽链 | PROMPT 实例 | 说明 |
|-------|------|-------------|------|
| **T0** | Lead / harness-10 | [`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md) | 写 **本 task** + gate `pending` → **人签** |
| **T2c** | explore → 22 → 30 → 40 → CLOSE（**跳过 50**） | [`PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md) | P2 执行 · SPEC §8.3 |

**通用模板**：[`PROMPT_claude_chain_serial_v1.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1.md)

### Subagent roster（`.claude/agents/`）

| 文件 | 帽 | T0 | T2c |
|------|----|----|-----|
| `harness-10-requirements.md` | 10 | ✅ | — |
| `harness-explore-l0.md` | explore | — | ✅ |
| `harness-22-audit.md` | 22 | — | ✅ |
| `harness-30-docs.md` | 30 | — | ✅ |
| `harness-40-check.md` | 40 | — | ✅ |
| `harness-50-reinspect.md` | 50 | — | **跳过**（纯 docs · `not_applicable`） |

Invoke 落盘：T2c 执行后落盘至 `docs/harness/invokes/by-task/gov-docs-noise-p2/`

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-06 | T0：Claude 写 P2 task 草案 · 待 HG-TASK-DRAFT 人签 |
| 2026-06-06 | R1 改稿：P2-2 子集对齐 · C4/C5/C6 映射 · 关账 C4/C5 |
