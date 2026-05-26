# 任务审核 R1 · Coding Wiki T1c — 测试迭代过程档案（v1）

## 元信息

| 字段 | 值 |
|------|-----|
| **task_path** | `docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md` |
| **task_slug** | `coding-wiki-t1c` |
| **audit_round** | R1 |
| **freeze_id** | `CODING-WIKI-T1C@2026-05-26` |
| **invoke_snapshot** | `docs/harness/invokes/by-task/coding-wiki-t1c/invoke_20260526_22_coding-wiki-t1c-v1.md` |
| **audit_profile** | `post_close`（开工前合同审；关账后统一人审） |
| **关联 SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.1 P1（T1c） |

## 审查结论摘要

**零硬阻塞**。task 与 `CODING_WIKI.md` §8–§9、治理 SPEC T1c、`WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` 第 7/15 行缺口对齐；`test_strategy: not_applicable` 理由成立；`HG-TASK-DRAFT`、`HG-T1C-INGEST-SCOPE` 均为 **approved**；本期 ingest 两源 task 均在 `docs/tasks/done/` 且含可蒸馏的测试交付信息；非范围明确禁止改 `api/`、`tests/`、CI 与 `docs/harness/prompts/`。

**结论：准许进入 30 执行帽。**

## 已核对项

| # | 项 | 结果 |
|---|-----|------|
| 1 | Harness §5：`semi_auto`、`freeze_id`、`gates_before_code`、`audit_profile` | pass |
| 2 | `human_gate`：`HG-TASK-DRAFT`、`HG-T1C-INGEST-SCOPE` = approved；blocks 22/30 已解除 | pass |
| 3 | §8「非 coverage 真值」：Wiki 记变更史/意图，不替代 pytest/CI/`_test_manifest` | pass；与 task 范围/非范围一致 |
| 4 | 验收可观测：decisions≥1、concept 页、2 synthesis 含 `## 测试变更`、index/log 更新 | pass（30 帽 VERIFY 已写在 PROMPT_30） |
| 5 | ingest 名单（2 个 done task）路径存在 | pass |
| 6 | ingest 源 task 含测试指针（非清单式真值表） | pass（见下表） |
| 7 | 失败路径 F1–F3 可操作；F2 与 22 审查纪律一致 | pass |
| 8 | 非范围：无多 slug AB、无 `api/`、无 Harness prompts 正文 | pass |
| 9 | 前置 T1b/P2：`docs/coding_wiki/` 骨架与 3 份既有 synthesis | pass |

### ingest 源 task 可操作性（30 帽素材）

| # | source_task | 预期 synthesis | 测试相关 L1 素材（摘要） |
|---|-------------|----------------|---------------------------|
| 1 | `docs/tasks/done/task_05_query_rewrite_observability.md` | `syntheses/query-rewrite-observability.md` | `tests/test_query_rewrite_compare_anchor.py`；验收命令 `pytest …`；实现备忘列 `api/*` + 单测 |
| 2 | `docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md` | `syntheses/chatbi-v3-text2sql-tool-latency-obs.md` | `tests/test_chatbi_json_log.py`；验收含分阶段 pytest/SSE；RUNBOOK 可 pointer |

> **纪律提醒（30）**：`## 测试变更` 须列 **路径 + pointer**，禁止把 pytest 全集或 coverage 数字维护为 Wiki 真值（对照 F2、§8）。

## 阻塞 / 非阻塞

| 类型 | 项 |
|------|-----|
| **阻塞** | 无 |
| **非阻塞** | `decisions/` 首条内容可由 ingest 中「暂不测/退役」类结论提炼，slug 由 30 帽自定（须 append-only） |
| **非阻塞** | `concepts/test-strategy-ink-backend.md` 宜链 L0 `ERR_*` / `graph_query` 与 L1 `failure_paths`，勿写第二架构真值 |
| **非阻塞** | ChatBI 源 task 体量大；synthesis 须摘要 + pointer，禁复制 RUNBOOK/SPEC 全文（`CODING_WIKI` §4.1） |
| **非阻塞** | 对比表 #23–#24（Lint 自动化）本 Epic 非硬验收；可后续周期任务 |

## 需任务帽回填清单

无。

## 是否建议执行帽开工

**是**。在 `task/coding-wiki-t1c-v1` 分支执行；**禁止** touch `api/`、`docs/harness/prompts/` 帽子正文。

## 签收 / 关闭

本 R1 为 **post_close** 开工前合同审；**不** 宣告 task `done`。关账仍须 **40 VERIFY** + **50 复检** + `PROMPT_CLOSE`（归档 `done/`、§6.6 T1c）。

## 下一棒可复制 Prompt

**新对话** · Open `ai-ink-brain-api-python/` · 复制：

`docs/harness/invokes/by-task/coding-wiki-t1c/PROMPT_30_startup_coding-wiki-t1c-v1.md`

（围栏内全文；落盘 invoke：`invoke_YYYYMMDD_30_coding-wiki-t1c-v1.md`）

```text
你正在扮演 Harness「执行帽（30）」（Coding Wiki T1c · 纯文档），遵循 PROMPT_30_startup_coding-wiki-t1c-v1.md 围栏全文。

硬前置：
- 22 R1：docs/harness/reviews/by-task/coding-wiki-t1c/task_coding_wiki_t1c_test_archive_v1_audit_R1_20260526.md（零阻塞）
- task：docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md
- git_branch：task/coding-wiki-t1c-v1
- freeze_id：CODING-WIKI-T1C@2026-05-26
- human_gate：HG-TASK-DRAFT、HG-T1C-INGEST-SCOPE = approved

交付要点：decisions/≥1 · concepts/test-strategy-ink-backend.md · 2 syntheses（含 ## 测试变更）· index+log · 禁止 api/ 与 harness prompts 正文。
下一棒：40（新对话 · PROMPT_40_startup_coding-wiki-t1c-v1.md）
```
