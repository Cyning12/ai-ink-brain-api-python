---
title: "P1 Harness 路径预览"
slug: vol-04-04-harness
series: chatbi-graph-harness-showcase
vol: "04"
chapter: "04"
status: compiled
planning_only: true
---

# 04 · Harness 路径预览

> **性质**：Task-B **开工前** 帽链预案 · 真值以未来 `docs/tasks/active/task_chatbi_graph_p1_*.md` 为准。  
> **横切规则**：[`vol-03`](../vol-03-cross-cutting/) 全卷必读。

---

## 1. 预计帽链

```text
00 轮 0 意图卡（可复用本卷 02-intent-card-draft）
  → 10 task 草案 + invoke
  → 22 R1（SSE/contract/D-2 重点审）
  → [10 回填] → 22 R2（若 R1 有阻塞）
  → 人签 HG-TASK-DRAFT · HG-AUDIT-R1
  → 30 实现（runner MVP · 节点 · SSE 发射）
  → 40 自检（parity 命令 + 专测）
  → 50 独立复检（Fresh Context · 必落盘）
  → PR 后端
  → [可选] Task-B-FE 前端仓 10→30（工作区 Projects/）
```

**与 P0 差异**：P0 有 **基线闸前置 PR**；P1 预期 **无** 另开基线 task（除非 50 发现新的 main 红项）。

---

## 2. 50 必须（涉 api/ + SSE）

| 检查 | 说明 |
| --- | --- |
| `test_strategy: required` | P1 专测 + 全集回归 |
| SSE / contract | 新增 type 须 `_contract_manifest` · drift 索引 |
| D-2 | `git diff … -- api/unified_chat.py` **空** |
| Fresh Context | **禁** 30 invoke 全文 · 对照 diff + 40 表 |
| human_gate | commit-level 追溯 |

50 可参考 P0 模板：[`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`](../../../tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md)

---

## 3. 22 审查焦点（预判）

| 维度 | R1 可能阻塞项 |
| --- | --- |
| **Delta** | MODIFIED runner vs ADDED 节点边界不清 |
| **SSE parity** | 验收表无快照/contract 字面命令 |
| **§10 冻结** | Q-7（Intent 超时 SSE `ok`）须在 P1 _closure 或 defer 记录 |
| **失败路径** | 缺 `fp-p1-*` Scenario 与测试映射 |
| **跨仓** | BFF 是否另 task · 本 PR 禁止夹带 `ai-ink-brain/` |

---

## 4. 跨仓与 Open Folder

| 任务 | Open Folder | 落盘 |
| --- | --- | --- |
| **Task-B**（后端） | `ai-ink-brain-api-python/` | invoke/review/reinspect 本仓 |
| **Task-B-FE**（BFF） | `ai-ink-brain/` 或工作区 `Projects/` | 前端 `content/tasks/` 或该仓 harness |

工作区规则：[`Projects/AGENTS.md`](../../../../Projects/AGENTS.md) §2 · 跨仓须 **分 PR**。

---

## 5. semi_auto 与 commit 纪律

| 项 | 建议 |
| --- | --- |
| **semi_auto** | `true`（与 P0 一致 · 人签后链式） |
| **分支** | `task/chatbi-graph-p1-mvp-v1` |
| **invoke** | 每帽 `docs/harness/invokes/by-task/<slug>/` |
| **禁止** | main 上链式提交 · 未落盘 invoke 换帽 |

---

## 6. 图谱与 CI 清单（30 开工前）

复用 vol-03-03 checklist：

1. 代码注册 Q-8（已存在则 **改行为** 非删路由）
2. `_manifest.json`
3. `_contract_manifest.json`（新 SSE type）
4. `99_spec.md` drift 索引
5. P1 专测
6. `02_version.md` / `10_flow_agent_graph.ai.md`（按变更量）

---

## 7. P1 关账后本系列更新

| 动作 | 路径 |
| --- | --- |
| 本卷 `status` | `planned` → `done` |
| 新增 | `06-evidence-index.md`（PR · task · reinspect） |
| `_meta/TIMELINE.md` | append Task-B 事件 |
| vol-90 | 可选 v0.11（含 P1 一句 · 禁 overclaim） |

---

## 指针

- 半自动通则：[`HANDOFF_SEMI_AUTO`](../../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)
- Agent 检查单：[`vol-03-04-agent-playbook.md`](../vol-03-cross-cutting/04-agent-playbook.md)
