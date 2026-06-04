---
title: "Harness 落盘地图"
slug: vol-03-01-artifacts
series: chatbi-graph-harness-showcase
vol: "03"
chapter: "01"
status: compiled
---

# 01 · Harness 落盘地图

> **横切要点**：同一套目录规则，贯穿 vol-01（#106）与 vol-02（#107）；P1 新 Loop **仍用此表**。  
> L1 真值：[`docs/harness/README.md`](../../../harness/README.md) §2.1

---

## 1. 帽 × 落盘 × 职责

| 帽 | 角色 | 必落盘路径 | 本系列案例 |
| ---: | --- | --- | --- |
| **10** | 需求 / task 草案 | `docs/tasks/active/task_<slug>.md` + invoke | 两 task 初稿 |
| **22** | 任务审核 R1/R2 | `docs/harness/reviews/task_<slug>_audit_R<n>_YYYYMMDD.md` | P0 有 R1→回填→R2 |
| **30** | 执行编码 | 代码 diff + invoke；**不**替代 task 验收表 | `eed212e` · `b43ae3e` |
| **40** | 自检 | task 内 `### 自检结论（执行者）` + invoke | 两 task 回填表 |
| **50** | 独立复检 | `docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_vN.md` | 选 B 依据在 P0 50 |

**invoke 快照**（每帽可选但 semi_auto 链 **强烈建议**）：

```text
docs/harness/invokes/by-task/<task_slug>/invoke_YYYYMMDD_<帽号>_<简述>.md
```

示例：

- `chatbi_baseline_merge_gate_v1/invoke_20260604_30_execute.md`
- `chatbi_graph_p0_foundation_v1/invoke_20260603_50_reinspect.md`

---

## 2. 三棵树分工（勿混）

| 树 | 路径 | 写什么 | 不写什么 |
| --- | --- | --- | --- |
| **invokes** | `docs/harness/invokes/by-task/<slug>/` | 下一棒 §3 Prompt 快照 · 半自动续跑锚点 | 审查结论全文 |
| **reviews** | `docs/harness/reviews/`（推荐 `by-task/<slug>/`） | 22 阻塞项 · 理论对齐 · R1/R2 判定 | 50 pass/fail 表 |
| **reinspect_results** | `docs/tasks/reinspect_results/` | 50 验收表 · Judgment · 是否建议 merge | 30 实现过程长文 |

**记忆口诀**：22 **审 task 能不能做** · 40 **执行者说做完了** · 50 **第三方对照 diff 验**

---

## 3. 本系列两 task 并列

| 字段 | 基线闸 vol-01 | P0 vol-02 |
| --- | --- | --- |
| **task_slug** | `chatbi_baseline_merge_gate_v1` | `chatbi_graph_p0_foundation_v1` |
| **task** | `docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` | `docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |
| **blocks** | — | 被 #106 阻塞（选 B） |
| **22** | R1 一次 · 人签后 30 | R1 阻塞 → 回填 → **R2** |
| **50** | pass-with-notes · merge #106 | pass-with-notes · Strict 被基线挡 · rebase 后合 #107 |
| **PR** | #106 · `26e1c45` | #107 · `f53327a` |

Invoke 目录：

- [`chatbi_baseline_merge_gate_v1/`](../../../harness/invokes/by-task/chatbi_baseline_merge_gate_v1/)
- [`chatbi_graph_p0_foundation_v1/`](../../../harness/invokes/by-task/chatbi_graph_p0_foundation_v1/)

---

## 4. human_gate 与脚本

task 元信息表示例：

```markdown
| human_gate_id | status | blocks_hats | 说明 |
| HG-TASK-DRAFT | approved | 22-R1, 30 | 人签 task 草案 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 |
```

**开 30 前**（硬）：

```bash
python tools/harness_human_gate_check.py \
  --task docs/tasks/active/task_<slug>.md
# exit 0 方可执行
```

**Agent 硬规则**：`pending` → **拒执行** `blocks_hats` 所列帽；**禁止**静默改 `approved`（50 须 commit-level 追溯 · 见 vol-03-04）。

两案例人签 commit：`bbd6ded`（基线）· `ab4ca03`（P0）· author 均为维护者，非 Agent 代填。

---

## 5. semi_auto 链与 commit 纪律

同会话 **无 pending 闸** 时可自动戴下一帽，但须：

1. 下一棒 §3 **全文**写入 `invokes/by-task/<slug>/`
2. **commit** 该路径后再切换帽子
3. 在 **`task/<slug>` 分支**上操作 — **禁止**在 `main` 上链式提交

关账输出：[`HANDOFF_CLOSE_TRACE`](../../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md) · 半自动通则：[`HANDOFF_SEMI_AUTO`](../../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)

---

## 6. 与 L2 展示系列的关系

| 层级 | 路径 | 用途 |
| --- | --- | --- |
| **L1** | task / reviews / reinspect | 可 fail 的验收真值 |
| **L2** | 本 showcase 系列 | 叙事 + 命令 + 面试口径 |
| **L0** | `_tech_graph` · 代码 | 拓扑与 runtime 真值 |

展示卷 **摘 narrative + 指针**，禁止复制 reinspect 全文替代 L1。

---

## 指针

- 字段细则：[`HARNESS_V2_PLAN.md`](../../../harness/HARNESS_V2_PLAN.md) §5
- 证据一览：[`_meta/EVIDENCE_LINKS.md`](../_meta/EVIDENCE_LINKS.md)
