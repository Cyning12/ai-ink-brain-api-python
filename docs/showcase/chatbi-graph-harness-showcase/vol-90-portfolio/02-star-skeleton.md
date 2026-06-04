---
title: "STAR 骨架"
slug: vol-90-02-star
series: chatbi-graph-harness-showcase
vol: "90"
chapter: "02"
status: compiled
draft_version: v0.10
aligned_spec: docs/spec/governance/投递冲刺_20260609_v1_zh.md
---

# 02 · STAR 骨架（ChatBI Graph · Harness 两 PR）

> **与投递冲刺 §9 区分**：§9 是 **般果 Cursor 试点** 骨架；**本页** 是 **Ink 后端 ChatBI Graph P0 + 基线闸** 案例，可单独讲 3～5 分钟。

---

## S · Situation（背景）

- ChatBI V2 Agent 堆在 `api/agent.py`（约 1300+ 行），Unified 编排与 SSE/失败路由耦合，难单测、难演进 Graph。
- 路线图已冻结 **D-1～D-5**（自研 StateGraph、并行 Graph 路由、Legacy 不动等），准备落 **P0 地基**。
- 开 PR 前 **50 独立复检** 发现：P0 增量本身 pass，但 **main 已有 10× v3 pytest + contract `label` 红** — 与 P0 diff 无关，却挡 Strict merge。

**可展示证据**：`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md` · vol-01-01 选 B 表。

---

## T · Task（任务）

- **交付 P0**：共享层抽取 · State/边表 · Graph stub 路由（Q-8）· 专测 10/10 · **`unified_chat.py` 零行为变更**。
- **不破坏治理**：基线债 **不得** 混进 P0 PR；Required CI 须字面全绿再合 main。
- **个人角色（AI Coding）**：写 task/Delta/失败路径 · 戴 Harness 帽链 · 人签 human_gate · 50 Fresh Context 复检 · 维护者决策两 PR 顺序。

---

## A · Action（行动）

| 阶段 | 做了什么 |
| --- | --- |
| **P0 Loop** | 10 草案 → 22 R1 阻塞 → 10 回填 §10 冻结 → 22 R2 零阻塞 → 人签 → 30 实现 → 40/50 |
| **50 判定** | pass-with-notes：**P0 无回归** · Strict merge 被基线债阻塞 → 维护者 **选 B** |
| **基线 Loop（vol-01）** | 独立 task：`conftest` 固定 `INTENT_MIN_CONFIDENCE=0.6` · agent clarify 支持 `on` · contract 登记 `label` → **PR #106** |
| **P0 续合** | rebase on #106 → 全集 **287 pass** → **PR #107** |
| **CI 排障** | #107 首跑 `drift_check` 红（Q-8 端点未写入 `99_spec.md` 索引）→ 同 PR 补叙述层 → merge |
| **Harness 落盘** | task · reviews · invokes · reinspect — 可审计，非「口头说测过了」 |

**关键词（面试官爱听）**：Fresh Context 50 · human_gate 人签 · Delta 边界 · manifest vs drift 双轨。

---

## R · Result（结果）

| 指标 | 结果 |
| --- | --- |
| pytest 全集 | **287 passed**（rebase 后 · 合并前必绿口径） |
| P0 专测 | **10/10** · `tests/test_chatbi_graph_p0_foundation.py` |
| Legacy 行为 | `git diff … -- api/unified_chat.py` **空** |
| 代码结构 | `agent.py` 瘦身 ~260 行迁出共享模块 · 新增 `api/graph/*` stub |
| Graph 路由 | Q-8 两 POST **200**（JSON/SSE stub · curl 可验） |
| 治理 | 两 PR merge `26e1c45` + `f53327a` · 系列 L1 证据链完整 |

**定性结论（无 KPI 数字）**：main 恢复可续 Loop 的 **绿基线**；P1 Graph MVP 可在清晰模块边界上开工，而非在单体 agent 上硬改。

---

## 追问备答（3 条）

| 追问 | 答法 |
| --- | --- |
| 为什么不在 P0 PR 里顺手修 10 测？ | **Delta 可审计** — 基线债与 Graph 五步是不同 task；50 已证明 fail 集与 P0 commit 无关。 |
| Harness 和「写 prompt 让 AI 写代码」差在哪？ | task 含验收/失败路径/test_strategy · 22/50 独立审查 · human_gate · reinspect 落盘 — **合并前可追责**。 |
| Graph 用户能用了吗？ | **不能** — P0 是 stub；Ink 仍 Legacy。P1 才做真实 Agent 环与 SSE parity（vol-04 planned）。 |

---

## 指针

- vol-01 · vol-02 全卷
- 横切 Harness/CI：[`vol-03`](../vol-03-cross-cutting/)（compiled stub）
- 投递冲刺禁 overclaim：[`投递冲刺_20260609_v1_zh.md`](../../../spec/governance/投递冲刺_20260609_v1_zh.md) §8
