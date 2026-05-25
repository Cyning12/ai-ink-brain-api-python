# Task：工作区 Harness taxonomy 推广（T3 · v1）

> **状态**：`pending`  
> **前置**：Wiki-CTX-AB P1 **accepted** — [`conclusion_p1_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md)  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) **T3**  
> **样板仓**：本仓 `docs/harness/` 已 **by-task**（勿重复 mv api-python）

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 工作区 `Projects/docs/harness/` 文档与 pointer；无 api-python 代码变更。 |
| **freeze_id** | `HARNESS-TAXONOMY-T3@2026-05-25` |
| **gates_before_code** | `["human_gate"]` |
| **semi_auto** | `false` |
| **audit_profile** | `post_close` |

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-T3-SCOPE | pending | 30 | 人确认：仅工作区 harness + 链前端说明，不动 api-python 真值 |

---

## 背景与目标

将后端已落地的 **invokes/reviews by-task** + `prompts/{hats,templates,handoff}` 规范 **同步到工作区** `Projects/docs/harness/`，以 **pointer + README** 为主，避免双份 invoke 正文漂移。

**完成态**：工作区 README §2.1 与 api-python 对齐；扁平历史 invoke 有索引或 pointer；`RECENT_TASK_SCHEDULE` / 根 `AGENTS.md` 若有链则更新一行。

---

## 范围

- [ ] 更新 `Projects/docs/harness/README.md` §2.1（taxonomy · 与 api-python 对称）
- [ ] 更新 `Projects/docs/harness/invokes/README.md`、`reviews/README.md`
- [ ] 对仍位于根下的历史 `invoke_*.md`：补 **pointer** 或迁移计划表（**不** 要求一次 mv 全量）
- [ ] 链至 `ai-ink-brain-api-python/docs/harness/README.md` 为子仓真值

## 非范围

- 不改 `ai-ink-brain-api-python/docs/harness/prompts/`（子仓真值）  
- 不跑 Coding Wiki ingest（`task_coding_wiki_pilot_v1`）  
- 不改 CI  

---

## 验收标准

- [ ] 工作区 Agent 读 harness 时有明确「默认读子仓 / 读 pointer」纪律  
- [ ] 无悬空链至已迁移路径  
- [ ] 22 R1 或人扫后记 `HG-T3-SCOPE` = `approved`

---

## 给 Cursor

`T3`、`taxonomy`、`Projects/docs/harness`、`pointer`、`Wiki-CTX-AB P1`
