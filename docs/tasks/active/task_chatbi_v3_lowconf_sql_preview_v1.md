# Task：ChatBI V3 — 低置信 Text2SQL 预览 + 确认放行（§5-2 关账）

> **状态**：`in_progress`（2026-05-31 · 00 开帽 · `CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31`）  
> **schedule_ref**：RECENT §1.1 #4 子项 · 母单 §5.1 **5-2**  
> **登记日期**：2026-05-31  
> **父 task**：[`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`](task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md)（§5.0 已验收 · §5.1 **5-2** 本单关账）  
> **需求真值（L1）**：[`docs/spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`](../spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md) **§2 Text2SQL 预览**、**§4 确认令牌**  
> **前置（done）**：[`task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`](../done/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md) · 母单 **§5.0** 方案 B（2026-05-13）  
> **KPI 试点**：首条 **业务** Harness 帽链验证（`kpi_rubric: KPI_RUBRIC_v1_2`）  
> **前端依赖**：**无阻塞**（Ink FE-1 烟测可选；见母单 §5.0.1）

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **task_slug** | `chatbi-v3-lowconf-sql-preview` |
| **test_strategy** | `required` |
| **freeze_id** | `CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **experience_capture** | `recommended` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `00` |
| **git_branch** | `task/chatbi-v3-lowconf-sql-preview` |

### 阶段状态（00 维护 · 2026-05-31）

| 帽 | 状态 | 备注 |
|----|------|------|
| 00 | done | `invoke_20260531_00_*` |
| 22 | done | R1 零阻塞 |
| 30 | done | G1–G4 pytest 补齐 |
| 40 | done | 自检回填 §10 |
| 50 | pending | **须新会话** Fresh Context |
| CLOSE | pending | 待 50 + HG-REINSPECT 人签 |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 本草案人扫通过后改 `approved` |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 |
| HG-REINSPECT | approved | done | 50 通过后 merge 前人签 |

---

## 0. 现网基线（re-baseline · 2026-05-31 · `main`）

> **勿**按母单「5-2 未做」理解 scope。下列能力 **已在 `main`**，本 task 以 **缺口补齐 + 验收关账 + Harness 落盘** 为主。

| 项 | 现网证据（摘要） |
|----|------------------|
| `agent.plan.preview` | `api/agent.py` 澄清分支 · `preview_only=True` 调 `text2sql_execute` |
| `plan_execution_token` | `api/chatbi_plan_token.py` · JSON 续跑 `body.plan_execution_token` |
| 契约 | `docs/_tech_graph/_contract_manifest.json` 含 `agent.plan.preview` payload 键 |
| env | `PROJECT_CONFIG` §C · `CHATBI_V3_PLAN_PREVIEW_CONFIRM` / `CHATBI_PLAN_TOKEN_TTL_S` 等 |
| JSON 测例 | `tests/test_unified_chat_backend_v2_agent.py` · `test_v3_plan_preview_*` · `test_v3_plan_execution_token_json_bypasses_clarify` |
| 单元 | `tests/test_chatbi_plan_token.py` |

**本单仍须补齐**（见 §2 范围）：无效/过期 token **API 层** deny、**SSE** 路径 parity、预览失败路径测例、母单 §5.1 **5-2** 状态同步、Harness invoke/review/reinspect + **`### KPI（00）`**。

---

## 1. 背景与目标

低置信 **Text2SQL** 场景下，用户须在执行前看到 **SQL 草案预览**，并通过 **`plan_execution_token`** 显式确认后再跑通一轮查数（SPEC §2、§4）。方案 B（§5.0）已消除「假 rag」观测问题；**5-2** 聚焦 **预览 + 只读闸 + 确认放行** 的 **可测、可关账** 完成态。

**完成态**：

- JSON **与** SSE Unified Chat 路径：低置信澄清时可见 **`agent.plan.preview`** + 带 TTL 说明的 **`agent.clarify`**；合法 token 续跑跳过澄清并执行 Text2SQL。
- 无效 token / 预览失败 / 开关关闭等 **failure_paths** 有 pytest 证据。
- 母单 §5.1 **5-2** 标记 **已验收**；本 task 经 **00→22→30→40→50→CLOSE** 关账并填 KPI 表。

---

## 2. 范围

- [x] **G1 无效 token deny（F2）**：`test_v3_plan_execution_token_invalid_json_denies_bypass`（问句不匹配 + 篡改签）
- [x] **G2 SSE parity**：`test_v3_plan_preview_sse_parity`（22：**必须 parity**，无 defer）
- [x] **G3 预览失败（F3）**：`test_v3_plan_preview_fail_json_no_token`
- [x] **G4 只读闸证据**：`test_v3_plan_preview_json_includes_plan_preview_and_ttl_notice` 内 `assert preview_only is True`
- [ ] **G5 文档同步**：母单 [`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`](task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md) §5.1 **5-2** → **已验收** + 链本 PR；SPEC §6 Text2SQL 预览项勾选（若行为已满足）
- [ ] **G6 Harness 落盘**：`invokes/by-task/chatbi-v3-lowconf-sql-preview/` · `reviews/…` · `reinspect_results/reinspect_chatbi-v3-lowconf-sql-preview_*` · task **`### KPI（00）`**

## 3. 非范围

- **5-3** RAG 低置信预览、**5-4** 全量审计字段/product 化（另 task）
- Intent vNext 多候选（`task_chatbi_v3_intent_classification_debt_v1.md`）
- Ink 前端 FE-1 烟测（可选跟进；不阻塞本仓关账）
- 新增 `chain.type` 键名（沿用现网 `agent.plan.preview`）
- 改 `api/` 外模块的大重构

---

## 4. 行为变更（Delta）

> 相对 **`main@2026-05-31`**：以 **测试 + 文档 + 边界行为** 钉住已有预览/token 能力；若发现与 SPEC 偏差，在本 PR **最小修正** 并更新 Delta。

### ADDED

- **Requirement**：无效 `plan_execution_token` 不得绕过低置信澄清门槛。  
  - **Scenario**：`lowconf-token-invalid-deny` — GIVEN 低置信澄清已触发 WHEN 续跑携带过期/篡改 token THEN 仍走 clarify 或返回结构化拒放（与 F2 表一致）且 **无** Text2SQL 全量执行。

- **Requirement**：SSE 与 JSON 在预览开关开启时观测等价（事件 type + 关键 payload 键）。  
  - **Scenario**：`lowconf-plan-preview-sse-parity` — GIVEN `CHATBI_V3_PLAN_PREVIEW_CONFIRM=1` WHEN SSE Unified Chat 低置信澄清 THEN 流中含 `agent.plan.preview` 且含 `plan_execution_token`。

### MODIFIED

- **Requirement**：母单 §5.1 **5-2** 状态与验收表述（Previously: 「未做」）  
  - **Scenario**：`parent-task-5-2-closed` — GIVEN 本 PR 合并 WHEN 读母单 §5.1 THEN **5-2** 为 **已验收** 并链本子 task / PR。

### REMOVED

无

---

## 5. 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| SPEC | [`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`](../spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md) |
| 母单 | [`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`](task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md) |
| PROJECT_CONFIG | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) §C |
| 契约 | `docs/_tech_graph/_contract_manifest.json` |
| 代码入口 | `api/agent.py`、`api/chatbi_plan_token.py`、`api/unified_chat.py` |
| KPI / Harness | [`KPI_RUBRIC_v1_2.md`](../harness/guides/KPI_RUBRIC_v1_2.md) · [`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) |
| 图谱（按需） | `docs/_tech_graph/10_flow_unified_chat*.md`（仅结构变化时更新） |

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-lowconf-unconfirmed-exec` | 低置信未确认即执行全量 Text2SQL | 仍 clarify / 预览，不 bypass | 是 | 需预览或确认 |
| F2 | `fp-lowconf-token-invalid` | `plan_execution_token` 无效/过期/问句不匹配 | 拒放：clarify 或结构化错误（**禁止**静默执行） | 否 | 确认失效 · 须重问预览 |
| F3 | `fp-lowconf-preview-fail` | `preview_only` Text2SQL 失败 | 无 token；clarify 含失败说明 | 是 | 无法预览 SQL |
| F4 | `fp-lowconf-preview-off` | `CHATBI_V3_PLAN_PREVIEW_CONFIRM=0` | 仅 clarify，无 `agent.plan.preview` | 是 | 无 SQL 预览 |
| F5 | `fp-lowconf-contract-drift` | `agent.plan.preview` payload 键与 manifest 不一致 | `tech_graph_contract_check` **fail** | 是 | CI 红 |

---

## 验收标准

> **§6** · 关账核对清单

- [ ] §2 **G1–G6** 全部满足或有 22 书面 **defer** 理由（须人签）  
- [ ] 新增/扩展 pytest **先红后绿**（`test_strategy: required`）；触达契约时 **`python tools/tech_graph_contract_check.py`** 通过  
- [ ] **`pytest tests -m "not intent_eval and not intent_benchmark"`** 全绿  
- [ ] Harness：**00/22/30/40/50** invoke §3 ≥15 行 · review R1 · reinspect 建议合并  
- [ ] task **`### KPI（00）`** 非空（`kpi_aggregator: 00`）  
- [ ] **HG-REINSPECT** → `approved` 后 merge PR  

**建议验证命令（30/40/50 共用）**：

```bash
cd ai-ink-brain-api-python
pytest tests/test_unified_chat_backend_v2_agent.py -k "plan_preview or plan_execution" -q
pytest tests/test_chatbi_plan_token.py -q
python tools/tech_graph_contract_check.py
pytest tests -m "not intent_eval and not intent_benchmark"
python tools/harness_task_validate.py docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md
```

---

## 7. 计划帽链

```text
00（可选编排）→ 22 R1 → 30 → 40 → 50（新会话 Fresh Context）→ 00/CLOSE（KPI + 关账）
```

| 帽 | 落盘 |
|----|------|
| 00 | `invoke_*_00_*`（若用 `kpi_aggregator: 00`） |
| 22 | `reviews/by-task/chatbi-v3-lowconf-sql-preview/` |
| 30–50 | `invokes/by-task/chatbi-v3-lowconf-sql-preview/` |
| 50 | `reinspect_results/reinspect_chatbi-v3-lowconf-sql-preview_YYYYMMDD_v1.md` |

---

## 8. 开跑前确认（草案 · 待人拍板）

| # | 项 | 建议 |
|---|-----|------|
| C1 | 第一棒 | **22** 或 **00**（`kpi_aggregator: 00` 时 00 开帽） |
| C2 | 50 | **新会话** Fresh Context |
| C3 | SSE G2 | 必须 parity **或** 22 书面 defer + 后续子 task |
| C4 | 分支 | `task/chatbi-v3-lowconf-sql-preview` 从最新 `main` |

---

## 9. ### KPI（00）

> **rubric**: KPI_RUBRIC_v1_2 · **汇总**: 待 50 后 CLOSE · **状态**: pending-50 · **帽**: 00→22→30→40 已落盘

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
|----------|-------|------------|----|----|----|----|-----|----------------|
| 00 | open | main_chat | pass | pass | pass | pass | — | 编排 22→30→40；50 交 Fresh Context |
| 22 | R1 | main_chat | pass | pass | pass | pass | — | 零阻塞；G2 必须 SSE parity |
| 30 | R1 | main_chat | pass | pass | pass | pass | pass | +3 pytest；272 passed；contract OK |
| 40 | R1 | main_chat | pass | pass | pass | pass | — | 自检 §10；待 50 填 D5 |
| 50 | — | — | — | — | — | — | — | **待新会话** |
| CLOSE | — | — | — | — | — | — | — | 待 50 + G5 + HG-REINSPECT |

**Task_KPI%**：（50/CLOSE 后由 00 重算）

---

## 10. ### 自检结论（执行者）

> **40 帽 · 2026-05-31** · 分支 `task/chatbi-v3-lowconf-sql-preview`

### 命令与退出码

| 命令 | cwd | 退出码 | 要点 |
|------|-----|--------|------|
| `pytest tests/test_unified_chat_backend_v2_agent.py -k "plan_preview or plan_execution or invalid_json or preview_fail or sse_parity" -q` | 仓根 | 0 | 5 passed |
| `python tools/tech_graph_contract_check.py` | 仓根 | 0 | OK |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 仓根 | 0 | 272 passed, 1 skipped |
| `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md` | 仓根 | 0 | OK |
| `python tools/harness_human_gate_check.py --task …` | 仓根 | 1 | **预期**：HG-REINSPECT pending |

### 验收表（§6 摘要）

| 项 | 结果 | 证据 |
|----|------|------|
| G1–G4 | pass | 见 §2 测例名 |
| G5 母单 5-2 | pending | CLOSE 轮同步 |
| G6 Harness | partial | 缺 50/reinspect |
| pytest | pass | 见上表 |

### OpenSpec × TDD

| 维度 | 结论 |
|------|------|
| Completeness | pass — F1–F5 + Scenario ID |
| Correctness | pass — 先补测后验证现网行为，无 api 大改 |
| Coherence | pass — re-baseline 与 SPEC §2/§4 一致 |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v0.1 草案：§5-2 子 task · re-baseline · KPI v1.2 首条业务链 |

---

## 给 Cursor

`chatbi-v3-lowconf-sql-preview`、`plan_execution_token`、`agent.plan.preview`、`kpi_rubric:KPI_RUBRIC_v1_2`、`kpi_aggregator:00`、§5-2、re-baseline、Harness 业务验证
