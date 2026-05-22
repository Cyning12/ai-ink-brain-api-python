# 任务审核：Rewrite 可观测性（task_05 · R1）

## 元信息

| 项 | 内容 |
|----|------|
| **task_path** | `docs/tasks/active/task_05_query_rewrite_observability.md` |
| **关联 SPEC** | 无 |
| **轮次** | R1 |
| **审查日期** | 2026-05-22 |
| **invoke_snapshot** | `docs/harness/invokes/invoke_20260522_22_task05-audit-r1.md` |
| **对照规约** | `docs/harness/prompts/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5 |
| **git_branch** | `task/query-rewrite-obs` |

---

## 审查结论摘要

task 已按 **TASK_TEMPLATE** 补齐 Harness 字段（`post_close`、`test_strategy: recommended`、`failure_paths`、人工闸表）。**实现**已在 `api/index.py` 写入 `metadata.match.query_compare`（Keyword 双路计数 + `compare_anchor_tokens`）；本轮试点增补 **`tests/test_query_rewrite_compare_anchor.py`** 覆盖锚点丢失判定。

**结论**：**零阻塞**；**建议** 人将 `HG-AUDIT-R1` 改为 `approved` 后进入 **30 执行帽** 终验（试点已在同分支补测通过，见下表）。

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **无阻塞** | — | 验收可观测；失败路径 F1–F3 已列；非范围清晰 |
| **非阻塞** | N-1 | `freeze_id` 为 task 级简写，无 SPEC 冻结点 — 可接受 |
| **非阻塞** | N-2 | 端到端依赖 Supabase 的集成测未列入 — `recommended` 下以单测 + DEBUG_RAG 人工抽检为主 |
| **已核对** | ✓ | `audit_profile: post_close` 与闸 1/2 一致；`git_branch` 已声明 |

---

## 是否建议执行帽开工

| 项 | 结论 |
|----|------|
| 执行帽（30） | **是**（**前提**：`HG-AUDIT-R1` → `approved`，**仅人**可改） |
| 回填任务帽（10） | **否** |

---

## 签收 / 关闭

- **本 task 未关闭**（试点 P0-B/C 进行中）：R1 为 **闸 1** 书面审；关账须 **50** + `HG-REINSPECT` / 全局签收 + 归档 `done/`。
- **R1 签收**：task 文档与契约 **可进入执行终验**（实现已存在，重点为单测与自检回填）。

---

## 下一棒可复制 Prompt

```text
你正在执行 task_05 的 **30 执行帽终验**（P0-B/C 试点）：在分支 `task/query-rewrite-obs` 上确认 `api/index.py` 的 `query_compare` 与单测、回填 task「自检结论」、落盘 50 复检至 `docs/tasks/reinspect_results/`。

前提：用户已将 task 内 HG-AUDIT-R1 改为 approved。

命令：pytest tests/test_query_rewrite_compare_anchor.py -q；可选全量 pytest -m "not intent_eval and not intent_benchmark"。

禁止：代填 human_gate；未 approved 时拒执行 30。
```
