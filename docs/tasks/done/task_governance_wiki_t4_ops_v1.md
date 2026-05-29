# Task：治理 — T4 运营化（lint + L0 pointer + 汇总页 hygiene）

> **状态**：done（2026-05-29）  
> **前置**：T4 SPEC **active** · Pilot/扩面/Unit A R2 铺量 **done**（syntheses **25** · 含 `graph_nodes` 决策 **22** 篇 · 纯叙事 `[]` **8** 篇）  
> **规划 SPEC**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) §4.3 · §5.1 未勾项  
> **排期**：[`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §0「T4 运营扩面」

> 落盘：验收后 `git mv` → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6 · Bridge SPEC §5.1 勾选。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `recommended` |
| **test_strategy_note** | 新增 `tools/coding_wiki_graph_nodes_lint.py` + pytest；**不**改 `api/`、**不**将 lint 升为 CI Required（属 P3 另单）。 |
| **freeze_id** | `GOV-WIKI-T4-OPS@2026-05-29` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读路径", "验收命令"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-wiki-t4-ops-v1` |
| **task_slug** | `gov-wiki-t4-ops` |
| **executor** | `claude-code` 或 Cursor（建议与 Unit A/B 同半自动纪律） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1, 30 | 人扫本 task + §范围 + lint 行为（是否仅 syntheses） |
| HG-AUDIT-R1 | approved | 30 | 22 R1 落盘后人签 |
| HG-REINSPECT | approved | done | 50 落盘后人签 · 合并 PR 前 |

---

## 背景与目标

T4 **Pilot → 扩面 → Unit A R2 铺量** 已完成：`graph_nodes` 已在绝大多数 synthesis 落地。但 Bridge SPEC §5.1 仍留 **L0 pointer**、**自动化 lint** 缺口；3 篇 **T4 元叙事汇总页** 无 frontmatter 决策；`99_spec.md` **无** Wiki 桥接链；Agent 仍依赖手工 `graph_query neighbors` 烟雾。

**完成态**：

1. **`tools/coding_wiki_graph_nodes_lint.py`**：扫描 `docs/coding_wiki/syntheses/*.md`（可选含 `concepts/`）frontmatter · 校验 `graph_nodes[].id`（`graph_query neighbors` exit 0）· `relation` 枚举（T4 SPEC §3.1）  
2. **`tests/test_coding_wiki_graph_nodes_lint.py`**：至少 1 个 **可失败** 用例（fixture 非法 id）+ 生产树 **集成 smoke**  
3. **`docs/_tech_graph/99_spec.md`**：增 **≤30 行**「Wiki 桥接」pointer → Bridge SPEC + `CODING_WIKI.md` §4  
4. **3 篇汇总 synthesis** 补 `graph_nodes: []` + 一句「纯叙事 · T4 索引页」  
5. **`CODING_WIKI.md`**：T4 覆盖表更新为 **25/25** 决策可见  
6. Bridge SPEC §5.1 已交付项 **勾选** · RECENT §6.6 增本 task **done** 行  
7. 22→30→40→**50**→关账 · 单 PR（lint + docs 可同 PR · 白名单见下）

---

## 范围

### 必须改

- [x] **Lint 工具** `tools/coding_wiki_graph_nodes_lint.py`  
  - CLI：`python tools/coding_wiki_graph_nodes_lint.py`（默认 `docs/coding_wiki/syntheses/`）  
  - 缺省 `graph_nodes` 键 → **warn**（汇总页除外见下表）或 **fail**（30 帽在 invoke 说明取舍；**推荐** 对 syntheses **强制** 存在键）  
  - 空数组 `graph_nodes: []` → **pass**  
  - 非空：逐 id 调 `tech_graph_graph_query`（或 subprocess 等价）· relation 白名单  
- [x] **pytest** `tests/test_coding_wiki_graph_nodes_lint.py`
- [x] **`99_spec.md`** Wiki 桥接小节（pointer only · 不改 VERIFY 表 Phase C 行）
- [ ] **汇总页 frontmatter**（3 篇 · 纯叙事 `[]`）：

| synthesis slug | 理由 |
| --- | --- |
| `governance-wiki-t4-expand` | T4 扩面索引 · 不绑单 node |
| `governance-wiki-t4-r1-pilot` | R1 Pilot 索引 |
| `harness-wiki-loop-t4-l2` | Loop 母叙事 · pointer 为主 |

- [x] [`CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §3/§4：25/25 覆盖表 + lint 命令行
- [x] [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) §5.1 勾选 + §7 VERIFY 增 lint 行 + 修订记录
- [x] [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §0 · §6.6 · §8
- [x] Harness：22 review · 30/40 invoke · `reinspect_gov-wiki-t4-ops_20260529_v1.md`

### 建议核对（无矛盾即可）

- [x] 既有 **17** 篇含非空 `graph_nodes` 的 synthesis：lint 全绿（若 fail → 修 id 或降级为 `[]` + 文内说明）  
- [ ] `docs/coding_wiki/concepts/test-strategy-ink-backend.md`：**暂不** 强制 graph_nodes（留 Batch/T4+ 概念网）

## 非范围

- **Batch-4 ingest** 新 slug（另单 · 可与本 task **并行** 不同分支）  
- `coding_wiki_lint.py` **CI Required** / `.github/workflows/` 新 step（**P3**）  
- 手改 `graph.json` · 改 `api/`  
- `docs/harness/prompts/` 帽子正文  
- 全 `concepts/` 铺 `graph_nodes`（本 task 仅 **可选** lint 扫描 concepts）

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| T4 SPEC | `docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` |
| 铺量 done | `docs/tasks/done/task_governance_wiki_t4_rollout_v1.md` |
| graph_query | `tools/tech_graph_graph_query.py` |
| SKILL | `docs/tasks/skills/SKILL-harness-task.md` · `SKILL-docs-governance.md` |
| 读序 | `docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | lint 发现未知 `graph_nodes.id` | exit 1 · 22/40 **fail** | 修 id 或 `[]` | CI/本地 FAIL 列表 |
| F2 | 用 Wiki 替代 `graph_query` 做影响分析 | 22/50 **阻塞** | 回 L0 | 审查阻塞 |
| F3 | diff 含 `api/` 或未白名单路径 | 30 拒开工 / 50 fail | 是 | PR 范围违规 |
| F4 | 升 CI Required 未人批 | **禁止** 改 workflow | — | 范围违规 |

---

## 验收标准

- [x] §范围「必须改」全部勾选
- [x] `python tools/coding_wiki_graph_nodes_lint.py` **exit 0**（main 树）
- [x] `pytest tests/test_coding_wiki_graph_nodes_lint.py -q` 绿
- [x] 合并前常模：`pytest tests -m "not intent_eval and not intent_benchmark" -q` 绿
- [x] 图谱门禁不退化：`tech_graph_graph_export.py --check` · `tech_graph_manifest_check.py` 绿
- [x] 22→50 落盘 · `semi_auto` 链式执行

**VERIFY**：

```bash
# 1) lint 全树
python tools/coding_wiki_graph_nodes_lint.py

# 2) lint 单测
pytest tests/test_coding_wiki_graph_nodes_lint.py -q --tb=short

# 3) 25/25 synthesis 含 graph_nodes 键（含 []）
python - <<'PY'
from pathlib import Path
root = Path("docs/coding_wiki/syntheses")
missing = [p.name for p in root.glob("*.md") if "graph_nodes:" not in p.read_text(encoding="utf-8")]
assert not missing, missing
print("OK:", len(list(root.glob("*.md"))), "syntheses")
PY

# 4) 99_spec Wiki pointer
rg -n "Wiki|T4|graph_nodes|TechGraph-Bridge" docs/_tech_graph/99_spec.md

# 5) 合并前必绿
pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short

# 6) 图谱
python tools/tech_graph_graph_export.py --check
python tools/tech_graph_manifest_check.py

# 7) 关账前人闸
python tools/harness_human_gate_check.py --task docs/tasks/active/task_governance_wiki_t4_ops_v1.md
```

---

## PR diff 白名单（硬）

| 允许 | 禁止 |
|------|------|
| `tools/coding_wiki_graph_nodes_lint.py` | `api/` |
| `tests/test_coding_wiki_graph_nodes_lint.py` | `.github/workflows/`（CI Required） |
| `docs/coding_wiki/syntheses/governance-wiki-t4-*.md` · `harness-wiki-loop-t4-l2.md` | `docs/coding_wiki/syntheses/` **其它** 批量正文改写 |
| `docs/coding_wiki/CODING_WIKI.md` | `docs/harness/prompts/` |
| `docs/_tech_graph/99_spec.md`（≤30 行增量） | 手改 `graph.json` |
| `docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` | |
| `docs/tasks/` · `docs/harness/`（invoke/review/reinspect） | |

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `tools/coding_wiki_graph_nodes_lint.py` · `tests/test_coding_wiki_graph_nodes_lint.py` · 3 synthesis · `CODING_WIKI.md` · `99_spec.md` · Bridge SPEC · RECENT · Harness |
| PR | （待开） |
| lint 行为 | missing key: **fail** · concepts 扫描: **否** |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| VERIFY §1–§4 | pass |
| VERIFY §5–§6 | pass |
| 结论 | **pass** |

---

## 给 Cursor / Claude Code

`gov-wiki-t4-ops`、`GOV-WIKI-T4-OPS`、T4 运营、lint、graph_nodes、99_spec pointer、semi_auto、22→关账
