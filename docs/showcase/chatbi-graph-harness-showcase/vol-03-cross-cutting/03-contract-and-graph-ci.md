---
title: "图谱 CI 三分工"
slug: vol-03-03-ci
series: chatbi-graph-harness-showcase
vol: "03"
chapter: "03"
status: compiled
---

# 03 · manifest / contract / drift

> **横切要点**：新增端点/字段时 **三门可能依次红** — 本系列 #106 与 #107 各踩一次，规则相同。

---

## 1. 三命令职责对比

| 脚本 | 查什么 | 真值文件 | 典型失败 |
| --- | --- | --- | --- |
| `tech_graph_manifest_check.py` | 代码/SQL 中的端点、RPC、表、env **结构化登记** | `docs/_tech_graph/_manifest.json` | Q-8 路由未登记 |
| `tech_graph_contract_check.py` | 前后端 **契约锚点**（SSE/JSON 字段等） | `_contract_manifest.json` | 前端读 `label` 未声明 |
| `tech_graph_drift_check.py` | 端点/RPC/env/表 **字面量子串** 须出现在 `docs/_tech_graph/*.md` | 叙述层（集中 **`99_spec.md` 索引**） | 代码有 path · md 全文无子串 |

**核心教训（vol-02-06）**：

```text
manifest_check OK  ≠  drift_check OK
```

manifest 只保证 **机器轨 JSON** 与源码一致；drift 还要求 **人类/Agent 读的 md 叙述** 不静默过期。

---

## 2. PR Required checks（本仓）

| Workflow | Job / Step | 包含 |
| --- | --- | --- |
| `pytest.yml` | pytest | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| `tech-graph.yml` | manifest_check | `tech_graph_manifest_check.py`（内嵌 drift） |
| `tech-graph-contract.yml` | contract | `tech_graph_contract_check.py` |

**合并前本地一条龙**（维护者 / 50 同口径）：

```bash
pytest tests -m "not intent_eval and not intent_benchmark" -q
python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
```

---

## 3. Runbook 路径 A（同 PR 修）

适用：**已知字段/端点 ADDED**，非契约 breaking change。

| 步骤 | 文件 |
| ---: | --- |
| 1 | 实现代码（如 `api/index.py` 注册路由） |
| 2 | `_manifest.json` 登记 path |
| 3 | `_contract_manifest.json`（若涉前端可读字段） |
| 4 | `99_spec.md` drift 索引 **追加字面量** |
| 5 | `02_version.md` 时间线（可选但推荐） |

Runbook：[`RUNBOOK_graph_contract_ci_red_v1.md`](../../../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md) §2 路径 A。

---

## 4. 本系列两次 CI 故事

### 故事 A · #106 contract `label`（vol-01）

| 项 | 内容 |
| --- | --- |
| **现象** | `contract_check`：`label` 未在 manifest 声明 |
| **根因** | 前端 SSE 消费者已读 UI 辅助字段 · 机器轨未登记 |
| **修复** | `_contract_manifest.json` → `frontend_ts_ignore_payload_like_keys` + `"label"` |
| **与 P0 关系** | main **已红** · P0 50 对照证明 **非 b43ae3e 引入** |

Scenario：`baseline-contract-label-declared` · `fp-baseline-contract-label-drift`

### 故事 B · #107 drift 端点（vol-02）

| 项 | 内容 |
| --- | --- |
| **现象** | `manifest_check` job 内 **drift_check** fail |
| **根因** | Q-8 两 path 已在 `_manifest.json` · **`99_spec.md` 索引未写** |
| **修复** | `99_spec.md` L46 追加 `/api/py/unified/chat/graph` 等 |
| **口播** | 「登记 manifest 不够，叙述层也要补一行」 |

---

## 5. 新增端点 checklist（P1 复用）

```text
[ ] api/index.py（或 handler）注册
[ ] _manifest.json 登记
[ ] 若前端可读字段 → _contract_manifest.json
[ ] 99_spec.md drift 索引追加
[ ] pytest / 专测 smoke
[ ] 02_version 或 flow 图（按变更大小）
```

Graph P1 新增 SSE type 时，contract 轨 **优先**于 drift。

---

## 6. failure_paths 与 CI 映射（节选）

| Scenario ID | 相关 CI | 本系列 |
| --- | --- | --- |
| `fp-baseline-contract-label-drift` | contract_check | vol-01 |
| `manifest-graph-endpoints` | manifest_check | vol-02 pass |
| drift 端点未覆盖 | drift_check | vol-02 #107 修 |

Phase C：`_test_manifest.json` 双向对照 — 见 `99_spec.md` · 本系列未改 test manifest。

---

## 指针

- vol-01-04 · vol-02-06 个案展开
- drift playbook（按需）：`docs/diary/2026-06-02-tech-graph-drift-check-option-A_playbook_v1_zh.md`
