# Task · 图谱 YAML 文档卫生（Doc Hygiene · P0）

> **状态**：`done`（**HG-TASK-DRAFT approved** · 串行链 **#1/2** · 40 PASS · HG-REINSPECT signed）  
> **schedule_ref**：RECENT **§1.6 续 #1**  
> **前置**：[`task_engineering_graph_yaml_post_epic_fix_v1.md`](../done/task_engineering_graph_yaml_post_epic_fix_v1.md) · **done**  
> **blocks**：[`task_engineering_graph_yaml_export_from_yaml_p1_v1.md`](./task_engineering_graph_yaml_export_from_yaml_p1_v1.md) · P1 须 **P0 PR CI 绿 + merge 入 main** 后开 30  
> **invoke**：[`PROMPT_START_30_v1.md`](../harness/invokes/by-task/graph-yaml-doc-hygiene-p0/PROMPT_START_30_v1.md) · 串行链 [`PROMPT_START_SERIAL_v1.md`](../harness/invokes/by-task/graph-yaml-inform-closure-chain/PROMPT_START_SERIAL_v1.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-doc-hygiene-p0` |
| **test_strategy** | `required` |
| **test_strategy_note** | 改 compile 模板 + 须 pytest 锁 Sub-graph 无 `.ai.md` 链 |
| **audit_profile** | `post_close` |
| **orchestration** | `Claude Code`（30→40 · 50 skip） |
| **git_branch** | `task/graph-yaml-doc-hygiene-p0` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **freeze_id** | `GRAPH-YAML-DOC-HYGIENE-P0` |
| **epic** | 图谱 YAML 迁移 · 续（Inform 闭环） |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | **approved** | 30 | 2026-06-16 人签 · 范围与非范围确认 |
| **HG-REINSPECT** | **signed** | done | 2026-06-16 · 40 自检 PASS · skip 50 |

---

## 背景与目标

Post-Epic 修复已更新 `99_spec`（YAML 编辑源 · `.ai.md` deprecated），但 **人类导航仍指向 `.ai.md`**：

1. `scripts/graph_yaml_compile.py` · `generate_sub_graph_links()` 仍输出「AI 协议版」链至 `*.ai.md`
2. 由脚本生成的 `00_main.md` §Sub-graph Links 与规约矛盾
3. QNA 未记录 **幽灵节点**（边引用未在 `nodes` 声明）为已知设计遗留，易误判为 YAML bug

**完成态**：Sub-graph 链指向 `.graph.yaml` 编辑源；`00_main.md` 重生成；QNA 一行遗留说明；pytest 防回归。**不**改 export、**不**删 `.ai.md`。

---

## 范围

- [x] **D1** 修改 `generate_sub_graph_links()`：子图链改为 `（编辑源：[*.graph.yaml](*.graph.yaml)）`，**移除**「AI 协议版」`.ai.md` 链
- [x] **D2** `python scripts/graph_yaml_compile.py --graph-id 00_main` 重生成 `docs/_tech_graph/00_main.md`（仅 Sub-graph / `generated_at` 漂移）
- [x] **D3** `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` 增 **§已知遗留 · 幽灵节点**（1～3 句：边可引用未声明节点 · 继承 graph.json · `external_ref` 另 task）
- [x] **D4** `docs/_tech_graph/` 内 grep：除 `*.ai.md` 自身与 `@deprecated` 注释外，**无**正文将 `.ai.md` 标为编辑源（发现则改 pointer，清单写入 §实现备忘）
- [x] **D5** `tests/test_graph_yaml_compile.py` 新增：`test_00_main_subgraph_links_no_ai_md_href`（生成 MD 的 Sub-graph 段不含 `.ai.md`）

## 非范围

- **不** 改 `tools/tech_graph_graph_export.py`（→ P1 task）
- **不** 改 `tools/tech_graph_manifest_check.py` TIP（→ P1 task）
- **不** 删除任意 `.ai.md`
- **不** 手改 `graph.json` 拓扑
- **不** 引入 `external_ref` schema

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-subgraph-regress` | 新 pytest 失败 | exit 1 · 修模板或测试 |
| F2 | `fp-00-main-drift` | 重生成后 `--check --graph-id 00_main` 失败 | 修 YAML 或 compile 逻辑 |

---

## 验收标准

- [x] `generate_sub_graph_links()` 源码与 `00_main.md` 均无 `.ai.md` 导航链
- [x] QNA §已知遗留 已增 · 修订记录 v1.2 行
- [x] `pytest tests/test_graph_yaml_compile.py -q` 全绿（含新用例）
- [x] `python scripts/graph_yaml_compile.py --all --check` → exit 0
- [x] `bash scripts/verify-tech-graph.sh` 全绿
- [x] task §自检结论已填 · invoke 30/40 落盘 · 本 task → `done/`
- [ ] P0 PR **CI 全绿** 且 **已 merge 入 `main`**（**此后** P1 方可开 30 · 见串行链硬闸门）

**合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 依赖与引用

| 依赖项 | 路径 |
| --- | --- |
| Post-Epic | `docs/tasks/done/task_engineering_graph_yaml_post_epic_fix_v1.md` |
| 编译脚本 | `scripts/graph_yaml_compile.py` · L170 `generate_sub_graph_links` |
| 规约 | `docs/_tech_graph/99_spec.md` §机器轨 |
| Mermaid 协议 | `docs/_tech_graph/99_mermaid_protocol.md` |

---

## 给执行帽的必读列表

- `AGENTS.md`
- `docs/tasks/active/task_engineering_graph_yaml_doc_hygiene_p0_v1.md`（本单）
- `scripts/graph_yaml_compile.py` · `generate_sub_graph_links`
- `docs/_tech_graph/00_main.md` · `QNA_graph_wiki_history_upgrade_v1_zh.md`

---

## 实现备忘（30 回填）

| 路径 | 说明 |
| --- | --- |
| `scripts/graph_yaml_compile.py` · `generate_sub_graph_links()` | 7 张子流程链由「AI 协议版 *.ai.md」改为「编辑源 *.graph.yaml」；Struct / Version 亦补编辑源链 |
| `docs/_tech_graph/00_main.md` | `--graph-id 00_main` 重生成，仅 Sub-graph Links 与 `generated_at` 漂移 |
| `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` | 增 §已知遗留 · 幽灵节点；版本 Frontmatter v1.0→v1.2；修订记录增 v1.2 行；关联 L0 指针 00_main.ai.md → 00_main.graph.yaml |
| `docs/_tech_graph/graph_v2_schema.md` | 更新 graphs[] 说明：id 默认与 *.graph.yaml 去后缀一致；source_ai_path 标注历史来源 .ai.md（YAML 迁移中）；导出说明自 *.graph.yaml |
| `tests/test_graph_yaml_compile.py` | 新增 `test_00_main_subgraph_links_no_ai_md_href` 防回归 |

### 自检结论

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `pytest tests/test_graph_yaml_compile.py -q` | 0 | 11 passed |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7/7 graph slices OK |
| 3 | `bash scripts/verify-tech-graph.sh` | 0 | 全步骤通过（manifest / test manifest / human_gate / compile --check / export --check / drift / graph_v2 equivalence / token estimate） |
| 4 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 417 passed, 1 skipped, 2 deselected |
| 5 | `ruff check api tests` | 0 | All checks passed |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-16 | HG-TASK-DRAFT approved · 可串行执行 |
| 2026-06-16 | 初稿 · Post-Epic 遗留 · 串行链 P0 |
