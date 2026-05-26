# 任务审核 R1 · Coding Wiki 试点（v1）

## 元信息

| 字段 | 值 |
|------|-----|
| **task_path** | `docs/tasks/active/task_coding_wiki_pilot_v1.md` |
| **task_slug** | `coding-wiki-pilot` |
| **audit_round** | R1 |
| **freeze_id** | `CODING-WIKI-PILOT@2026-05-25` |
| **invoke_snapshot** | `docs/harness/invokes/by-task/coding-wiki-pilot/invoke_20260526_22_coding-wiki-pilot.md` |
| **audit_profile** | `post_close`（本 R1 为试点开工前合同审） |

## 审查结论摘要

**零硬阻塞**。task 验收可观测、`failure_paths` 可操作、`test_strategy: not_applicable` 理由充分；`HG-TASK-DRAFT` 与 `HG-WIKI-INGEST-SCOPE` 均为 **approved**；首期 ingest 三件套路径存在且为 `done`；非范围明确禁止改 `docs/harness/prompts/` 与 CI。

## 已核对项

| # | 项 | 结果 |
|---|-----|------|
| 1 | Harness §5 字段（semi_auto、gates、freeze_id） | pass |
| 2 | 验收标准可 grep/可列目录验证 | pass |
| 3 | ingest 名单与 done task 文件存在 | pass |
| 4 | L0/L1/L2 边界（不替代 `_tech_graph` / Harness 执行链） | pass |
| 5 | F1–F4 失败路径与审查/ingest 纪律一致 | pass |
| 6 | 关联 SPEC T1b 与排期一致 | pass |

## 阻塞 / 非阻塞

| 类型 | 项 |
|------|-----|
| **阻塞** | 无 |
| **非阻塞** | 指导意见正文在工作区 `Projects/docs/harness/guides/`；子仓可增 pointer，不阻塞 30 |
| **非阻塞** | `semi_auto` 头部拼写 `atuo` 建议 30 帽顺带改为 `true` |
| **非阻塞** | 启动 Prompt 文件尚未生成；30 帽可一并落盘 `PROMPT_*` |

## 需任务帽回填清单

无。

## 是否建议执行帽开工

**是**。`HG-TASK-DRAFT`、`HG-WIKI-INGEST-SCOPE` 已 approved，可进入 **30** 交付 `docs/coding_wiki/`。

## 签收 / 关闭

本 R1 为 **post_close** 流程的开工前合同审；**不** 宣告 task `done`。关账前仍须 40 自检 + 50 复检 + 人签。

## 下一棒可复制 Prompt

```text
你正在扮演 Harness「执行帽（30）」，遵循：
- docs/harness/prompts/hats/30-execute-code.md（若存在）或 TEMPLATE-execute-invoke §3
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md

输入：
- task：ai-ink-brain-api-python/docs/tasks/active/task_coding_wiki_pilot_v1.md
- 审查：docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md
- WORKTREE_ROOT：ai-ink-brain-api-python/
- VERIFY_COMMAND：（纯文档）见 task test_strategy not_applicable 自检表
- human_gate：HG-* 均已 approved

交付：docs/coding_wiki/ 全骨架 + 3 份 syntheses ingest + docs/README 或 docs/tasks/README 一行入口；禁止改 docs/harness/prompts/ 与 CI。
完成后落盘 invoke_20260526_30_* 并回填 task 实现备忘；semi_auto 链至 40。
```
