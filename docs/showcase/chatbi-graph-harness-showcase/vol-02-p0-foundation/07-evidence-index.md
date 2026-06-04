---
title: "证据索引 · P0"
slug: vol-02-07-evidence
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "07"
status: compiled
---

# 07 · 证据索引（Vol-02）

> L1 真值指针；本页 **不复制** reinspect/task 全文。

---

## 1. PR 与 merge

| 项 | 值 |
| --- | --- |
| **PR** | [#107](https://github.com/Cyning12/ai-ink-brain-api-python/pull/107) |
| **标题** | feat(chatbi): P0 Graph 地基 — 共享层抽取与骨架路由 |
| **merge commit** | `f53327a` |
| **前置 PR** | [#106](https://github.com/Cyning12/ai-ink-brain-api-python/pull/106) · `26e1c45`（基线闸 · vol-01） |
| **分支** | `task/chatbi-graph-p0-foundation-v1`（已删） |

---

## 2. Task 与 Harness 落盘

| 类型 | 路径 |
| --- | --- |
| task | `docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |
| 22 R1 | `docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md` |
| 22 R2 | `docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md` |
| 50 | `docs/tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md` |
| invokes | `docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/` |

---

## 3. 实现 commit 链（时间序 · squash 前）

| commit | 说明 |
| --- | --- |
| （10 草案） | task + invoke |
| R1 / 回填 / R2 | 文档帽链 |
| `ab4ca03` | human_gate 人签 |
| `b43ae3e` | **P0 实现**（共享层 + graph + 专测） |
| `e3a0d60` | 40 自检回填 |
| （50 落盘） | reinspect + invoke |
| rebase + drift fix | `99_spec.md` · `02_version.md` |
| `f53327a` | **merge to main** (#107) |

---

## 4. 业务 diff 核心（runtime）

```
api/chatbi_events.py          # 新增
api/chatbi_agent_models.py    # 新增
api/chatbi_failure.py         # 新增
api/agent.py                  # 瘦身 · import 共享层
api/graph/state.py            # 新增
api/graph/runner.py           # 新增
api/unified_chat_graph.py     # 新增
api/index.py                  # Q-8 注册
docs/_tech_graph/_manifest.json
docs/_tech_graph/99_spec.md     # drift 索引
docs/_tech_graph/02_version.md
tests/test_chatbi_graph_p0_foundation.py
```

**刻意无 diff**：`api/unified_chat.py`（D-2）

---

## 5. 50 独立复跑摘要（2026-06-03 · P0 分支）

| 命令 | exit | 要点 |
| --- | ---: | --- |
| P0 专测 | 0 | **10/10** |
| 全集 pytest | 1 | 277 pass · **10 fail**（= main 同集） |
| manifest_check | 0 | OK |
| contract_check | 1 | `label`（main 同 · vol-01 范围） |
| unified_chat diff | — | **0 行** |
| agent.py 行数 | — | **1078** |

**50 总评**：pass-with-notes · P0 增量 OK · Strict merge 待 #106

---

## 6. merge 后 main 口径（2026-06-04）

| 命令 | 期望 |
| --- | --- |
| `pytest tests/test_chatbi_graph_p0_foundation.py -q` | 10 passed |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | **287 passed** |
| `tech_graph_manifest_check.py` | OK |
| `tech_graph_contract_check.py` | OK |
| `tech_graph_drift_check.py` | OK |

---

## 7. 系列内交叉引用

| 卷 / 文件 | 关系 |
| --- | --- |
| vol-01 | 基线闸 · 选 B 前置 |
| vol-03 | Harness / CI 横切 |
| [`_meta/EVIDENCE_LINKS.md`](../_meta/EVIDENCE_LINKS.md) | 全系列 L1 一览 |
| [`_meta/SERIES_MANIFEST.yaml`](../_meta/SERIES_MANIFEST.yaml) | `evidence_freeze_main: f53327a` |

---

## 8. SPEC / 图谱指针

| 文档 | 用途 |
| --- | --- |
| `SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md` §4.3 | D-1～D-5 |
| `SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md` §4A | P0 五步 |
| `docs/_tech_graph/_manifest.json` | Q-8 端点真值 |
