---
title: "CI 排障 · drift_check"
slug: vol-02-06-drift
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "06"
status: compiled
---

# 06 · CI 事故：drift_check

> **场景**：PR #107 首跑 Required · `manifest_check` job 内 **`tech_graph_drift_check` 失败**  
> **修复**：同 PR 内更新 `99_spec.md` drift 索引 + `02_version.md` · 随 **`f53327a`** 合入 main

---

## 1. 现象

| 项 | 内容 |
| --- | --- |
| **Workflow** | `.github/workflows/tech-graph.yml` · job 调 `tech_graph_manifest_check.py` |
| **manifest_check** | `_manifest.json` 与代码端点 **已对齐**（Q-8 两 path 已登记）→ 本子检查 **可绿** |
| **drift_check** | 扫描 `api/*.py` 等提取端点字面量，要求在 `docs/_tech_graph/*.md` **某处出现子串** → **红** |
| **典型 stderr** | 端点 `/api/py/unified/chat/graph`（及 `/stream`）**未**在 `*.md` 叙述层命中 |

**教训**：`manifest_check OK` **≠** `drift_check OK` — 两套真值互补（vol-03 横切展开）。

---

## 2. 根因

P0 ④ 在 `api/index.py` **新增** Q-8 路由，且 `_manifest.json` 已登记，但 **叙述层** `99_spec.md` 的 drift 索引 **未追加** 新 path。

drift_check（方案 A）设计：防止「代码/manifest 已变、文档静默过期」。见 playbook：`docs/diary/2026-06-02-tech-graph-drift-check-option-A_playbook_v1_zh.md`（按需打开）。

---

## 3. 修复

在 `docs/_tech_graph/99_spec.md` **drift_check 叙述层索引** 追加：

```markdown
**HTTP 端点（示例）**：... `/api/py/unified/chat/graph` `/api/py/unified/chat/graph/stream`
```

同步 `02_version.md` 时间线记录 P0 Graph 路由落地。

**验证**：

```bash
python tools/tech_graph_drift_check.py
# OK

python tools/tech_graph_manifest_check.py
# OK（含 manifest + drift 子步骤）
```

修复与 P0 实现 **同一 PR #107** squash 合入（merge commit `f53327a`）。

---

## 4. 两脚本对比（速查）

| 脚本 | 检查什么 | P0 踩坑点 |
| --- | --- | --- |
| `tech_graph_manifest_check.py` | `_manifest.json` ↔ 代码/SQL 结构化真值 | 忘记登记 Q-8 path |
| `tech_graph_drift_check.py` | 端点/RPC/env/表 **字面量** ↔ `docs/_tech_graph/*.md` 全文 | manifest 已登记但 **99_spec 索引未写** |

**新增端点 checklist**（P0 后固化习惯）：

1. `api/index.py` 注册  
2. `_manifest.json` 登记  
3. `99_spec.md` drift 索引 **追加一行**  
4. 必要时 `02_version.md` + flow 图（P1 再补 `.ai.md`）

---

## 5. 与 contract_check 的区分（避免混淆）

| 红项 | 本卷 | 修在哪 |
| --- | --- | --- |
| `contract … label` | **vol-01** · #106 | `_contract_manifest.json` |
| drift 端点未覆盖 | **本页** · #107 | `99_spec.md` |

P0 50 时 contract `label` 仍为 main 基线债；**不属于** P0 Delta — 由 vol-01 清。

---

## 6. Runbook 指针

- 图谱 CI 红：`docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md`（contract 专篇）
- drift 方案 A：`tools/tech_graph_drift_check.py` 头注释 + `99_spec.md` §drift_check

---

## 指针

- 修复文件：`docs/_tech_graph/99_spec.md` L46 附近 · `02_version.md`
- merge：`f53327a`（#107）
