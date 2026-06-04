---
title: "Agent 复用手册"
slug: vol-03-04-playbook
series: chatbi-graph-harness-showcase
vol: "03"
chapter: "04"
status: compiled
---

# 04 · Agent 复用手册

> **横切要点**：vol-01/02 的成功 **可复制** 到 vol-04 P1 — 本页是 Cursor Agent 开 Loop 前的 **检查单**，非业务 SPEC。

L1 帽正文：[`docs/harness/prompts/hats/`](../../../harness/prompts/hats/) · 半自动：[`HANDOFF_SEMI_AUTO`](../../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)

---

## 1. 开帽前（任何帽）

```bash
git branch --show-current
# 期望：task/<slug> — 若在 main → checkout -b task/<slug>
```

| 检查 | 命令 / 动作 |
| --- | --- |
| task 可读 | `docs/tasks/active/task_<slug>.md` |
| validate | `python tools/harness_task_validate.py --task …` |
| human_gate（开 30 前） | `python tools/harness_human_gate_check.py --task …` → exit 0 |
| 必读列表 | task 内链接已打开（PROJECT_CONFIG · 图谱 · SPEC） |
| 范围 | 非范围明确 — **拒**顺手修基线/夹带 |

**禁止**：在 `main` 上连续 semi_auto commit · 未落盘 invoke 就戴下一帽。

---

## 2. 22 任务审核

| 做 | 不做 |
| --- | --- |
| 对照 Delta · 验收表 · 失败路径 · §10 冻结 | 代填 `human_gate` approved |
| 有阻塞 → 交 **10 回填** 再 R2 | 在 R1 直接改 `api/` |
| 落盘 `reviews/task_<slug>_audit_R<n>_*.md` | 把审查结论只写进对话 |

**P0 范例**：R1 有阻塞（B-1～B-4）→ 10 回填 §10 → R2 零阻塞 → 人签 → 30。

理论对齐：[`SPEC-Governance-Harness-Theory-Align-P1-v1.md`](../../../spec/governance/SPEC-Governance-Harness-Theory-Align-P1-v1.md)

---

## 3. 30 执行

| 做 | 不做 |
| --- | --- |
| 遵守 `test_strategy` · 先测/同 PR 测 | scope 外「顺手修 main 红项」 |
| 缺 failure_paths / 验收不可执行 → **仅输出阻塞清单** | 静默扩 SPEC 范围 |
| 涉 `api/` + required → 预留 **50 落盘** | 跳过 40 自检表 |

**test_strategy: required** 且拒开工条件：

- 无 `## 失败路径` 或未映射 Scenario ID
- `gates_before_code` 未满足
- human_gate pending

---

## 4. 40 自检

| 做 | 不做 |
| --- | --- |
| **独立复跑** task 验收命令 | 复制粘贴 30 终端输出不 rerun |
| 回填 task `### 自检结论（执行者）` | 在 40 代填 50 结论 |
| invoke 落盘 + commit | 只口头「测过了」 |

**诚实记录**：P0 40 写明「全集 pytest 未绿」— 为 50 与维护者 **选 B** 留证据，非失败。

---

## 5. 50 独立复检 · Fresh Context

| 输入（优先） | 禁止 |
| --- | --- |
| task · reviews · **git diff** · 40 自检表 | **30 invoke 全文** |
| 独立复跑命令输出 | 执行过程长文草稿 |
| human_gate **commit-level** diff | 只看 task 最终 status |

**须新对话开 50 帽**（P1 规约 · 50 帽 §Fresh Context）。

落盘：

```text
docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_vN.md
```

必含：**验收项 | pass/fail | 证据 | 备注** · **是否建议 merge** · Judgment（`experience_capture` 等）。

本系列 P0 50：**pass-with-notes** — P0 增量 OK · Strict merge 被基线挡 → 触发 vol-01。

---

## 6. semi_auto · invoke · commit

```text
帽 N 完成
  → 写 invokes/by-task/<slug>/invoke_* §3 全文
  → git add + commit（HANDOFF_AUTO_COMMIT）
  → 若无 human_gate pending → 戴帽 N+1
  → 关账 → HANDOFF_CLOSE_TRACE + Harness 状态栏 B
```

**Loop 质量门禁**：30/40/50 换帽前 invoke §3 **≥15 行**（Loop Batch 同规）。

---

## 7. 本系列 Agent 禁止项（复盘）

| 禁止 | 曾接近踩坑 |
| --- | --- |
| P0 PR 夹带修 10 v3 测 | 50 明确 main 同 fail · 选 B 开独立 task |
| 50 读 30 invoke 当证据 | Fresh Context 只认 diff + 命令 |
| drift 只改 manifest | #107 须改 `99_spec.md` |
| 展示稿当 L0 真值 | showcase L2 · 矛盾以 task/reinspect 为准 |

---

## 8. P1（vol-04）开工前复读

1. 本页 §1–§6  
2. vol-03-02 required · vol-03-03 三门 CI  
3. vol-03-05 教训清单  
4. Roadmap §5 P1 Delta 模板

---

## 指针

- 22 帽：[`22-task-audit.md`](../../../harness/prompts/hats/22-task-audit.md)
- 50 帽：[`50-independent-reinspect.md`](../../../harness/prompts/hats/50-independent-reinspect.md)
- Cursor 规则：`.cursor/rules/05-harness-semi-auto.mdc`
