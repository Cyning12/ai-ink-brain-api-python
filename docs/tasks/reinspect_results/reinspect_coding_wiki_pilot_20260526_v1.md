# 独立复检 · Coding Wiki 试点（v1）

## 1. 元信息

| 字段 | 值 |
|------|-----|
| **task_path** | `docs/tasks/active/task_coding_wiki_pilot_v1.md` |
| **task_slug** | `coding-wiki-pilot` |
| **freeze_id** | `CODING-WIKI-PILOT@2026-05-25` |
| **git_branch** | `task/coding-wiki-pilot-v1` |
| **commit** | `92e4e64` |
| **复检日期** | 2026-05-26 |
| **帽** | 50（独立复检 + 全局验收） |
| **40 关系** | 独立重跑 `PROMPT_40` VERIFY (1)–(5)；对照 task `### 自检结论（执行者）` |
| **22 R1 关系** | `task_coding_wiki_pilot_v1_audit_R1_20260526.md`（零硬阻塞基线） |
| **diff 范围** | `92e4e64^..HEAD` · `docs/coding_wiki/`（+270 行，7 文件） |

---

## 2. 40 自检结论存在性

| 检查 | 结果 |
|------|------|
| task 含 `### 自检结论（执行者）` | **pass**（`task_coding_wiki_pilot_v1.md` L162–182） |
| 含命令与退出码摘要 | **pass** |

**阻塞**：无（不因缺失 40 表而拒检）。

---

## 3. 独立重跑 VERIFY (1)–(5)

| # | 命令/动作 | 50 独立结果 | 证据 |
|---|-----------|-------------|------|
| **(1)** | `test -f` CODING_WIKI / index / log | **pass** · exit 0 | 三文件存在 |
| **(2)** | `find syntheses concepts -name '*.md' \| wc -l` | **pass** · **4**（≥2） | 3× `syntheses/` + 1× `concepts/` |
| **(3)** | `git diff --name-only -- docs/harness/prompts/` | **pass** · **0** 行；`git diff --quiet` exit 0 | 未改 Harness 执行链 |
| **(4)** | `rg -l 'coding_wiki' docs/README.md docs/tasks/README.md` | **pass（工作区）** / **部分（Git）** | 两文件均有匹配；见 §5 非阻塞 |
| **(5)** | 抽检 2× syntheses | **pass** | `harness-p1-docs-consolidation.md`、`docs-tasks-reorg-move.md`：含 `source_task: docs/tasks/done/...`；无 `/Users/`；摘要非 SPEC 全文 |

**补充（50）**：三份 `source_task` 指向的 done 文件均 `test -f` 通过；`rg` 扫描 `docs/coding_wiki/` 无绝对本机路径。

---

## 4. 对照 22 R1（双真值 / 非范围）

| 项 | 结果 | 证据 |
|----|------|------|
| L2 非第二真值 | **pass** | `CODING_WIKI.md` L9–17、L17 明示禁止 Wiki 当真值 |
| 未替代 `_tech_graph` / graph.json | **pass** | schema §6 边界表；syntheses 仅 pointer |
| 未改 `docs/harness/prompts/` | **pass** | VERIFY (3) |
| 未迁 review 全文 | **pass** | syntheses ≤33 行/页，链 L1 |
| 未改 `api/`、CI workflow | **pass** | `git diff 92e4e64^..HEAD` 无 `api/`、`.github/workflows/` |
| F2 无整份 SPEC 复制 | **pass** | 抽检 + `tech-graph-gate-d-v2-tasks.md` 链 diary 报告为 pointer |

---

## 5. task §验收标准

| 验收项 | pass/fail | 证据 | 备注 |
|--------|-----------|------|------|
| `CODING_WIKI.md` 含 ingest/query/lint 与 L0/L1/L2 | **pass** | `CODING_WIKI.md` §1、§4.1–4.3 | L2 表 L9–15 |
| `index.md` 列试点页；`log.md` 含日期 ingest | **pass** | `index.md` L15–21；`log.md` L5–7 | `grep 2026-05-26`、`ingest` |
| ≥2 张 Wiki 链回真实 done task | **pass** | 3× syntheses + `index.md` 表 | 相对路径 |
| `docs/harness/prompts/` 未改 | **pass** | VERIFY (3) | |
| 22 R1 落盘 | **pass** | `reviews/by-task/coding-wiki-pilot/..._R1_20260526.md` | |
| 双入口 `docs/tasks/README.md` + `docs/README.md` | **部分** | `docs/tasks/README.md` L26 **已跟踪**；`docs/README.md` L17 仅工作区 | `git ls-files docs/README.md` 为空；`.gitignore:115` `docs/*` 未例外 |
| （可选）Wiki vs 扫 3 done task 行数对比 | **跳过** | task 标可选 | 建议关账会话或 Wiki-CTX-AB |

---

## 6. T1b 完成态（全局验收）

| T1b 要素 | 状态 | 证据 |
|----------|------|------|
| `docs/coding_wiki/` + `CODING_WIKI.md` | **满足** | 已提交 7 文件 |
| `index.md` + `log.md` | **满足** | 已提交 |
| ≥2 页（syntheses/concepts） | **满足** | 4 页 |
| 入口链（可克隆仓库） | **基本满足** | `docs/tasks/README.md` L26；`coding_wiki/index.md` 自导航；`docs/README.md` **未入库** |
| SPEC T1b 行 | **交付中 → 可关账** | `SPEC-Governance-Wiki-Harness-Roadmap-v1.md` L47 写「40 已过 · 待 50/关账」；关账后建议人改 **done** |

### 6.1 `freeze_id` 与变更范围

| 项 | 结果 |
|----|------|
| Wiki schema `freeze_id` | `CODING-WIKI-PILOT@2026-05-25` 与 task 一致 |
| 契约升级 | 无；仅文档 + `.gitignore` 例外 `!docs/coding_wiki/` |
| `test_strategy: not_applicable` | 理由成立；未要求 pytest |

### 6.2 `human_gate` diff 审查（commit-level）

| gate | 当前 | 变更追溯 |
|------|------|----------|
| `HG-TASK-DRAFT` | approved | `e52a6a0`：`pending`→`approved`；**Author: cyning** |
| `HG-WIKI-INGEST-SCOPE` | approved | 同上 |

50 **未**代填 gate。gate 与业务交付分 commit（`e52a6a0` vs `92e4e64`），符合 `HANDOFF_SEMI_AUTO` 建议。

### 6.3 合并前必绿（本变更子仓）

| 项 | 状态 |
|----|------|
| pytest | **不适用**（无 `api/` 变更） |
| tech-graph CI | **未触达** `_tech_graph` 正文 |
| 纯文档 PR | 维护者合并前仍建议常规 `pytest` 绿（仓库纪律） |

---

## 7. 阻塞合并项

| 类型 | 项 |
|------|-----|
| **阻塞** | **无** |
| **非阻塞** | `docs/README.md` 的 Coding Wiki 入口未纳入 Git（`docs/*` ignore）；克隆仓仅 `docs/tasks/README.md` + Wiki `index`。关账可选：`!docs/README.md` 或修订 task 验收措辞 |

---

## 8. 结论

**建议关账**（无须回 **30** 修复 Wiki 骨架与 ingest）。

关账后建议（**人**执行，50 不做）：

1. 新对话 + `PROMPT_CLOSE_coding-wiki-pilot-v1.md` → `HANDOFF_CLOSE_TRACE`  
2. `git mv` task → `docs/tasks/done/`  
3. （可选）SPEC T1b 行改为 **done**；`!docs/README.md` 若需双轨追踪入口  

---

## 9. 给需求帽回填

| 缺口 | 建议 |
|------|------|
| 双入口与 `.gitignore` 张力 | 10/关账帽：明确 `docs/README.md` 是否应加入例外列表，或验收改为「至少一处已跟踪入口」 |

无其他文档真值缺口。

---

## 10. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-26 | v1：50 独立复检 + 全局验收；建议关账 |
