# Task · 图谱 graph.json 导出改读 YAML（Export-from-YAML · P1）

> **状态**：`active`（**HG-TASK-DRAFT approved** · 串行链 **#2/2** · 30 待 **P0 CI 绿 + merge**）  
> **schedule_ref**：RECENT **§1.6 续 #2**  
> **blocked_by**：[`task_engineering_graph_yaml_doc_hygiene_p0_v1.md`](../done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md) · 须 **done** + HG-REINSPECT + **P0 PR CI 全绿且已 merge 入 `main`** 后再开 30  
> **前置 Epic**：[`task_engineering_graph_yaml_migration_epic_v1.md`](../done/task_engineering_graph_yaml_migration_epic_v1.md) · **done**  
> **invoke**：[`PROMPT_START_30_v1.md`](../harness/invokes/by-task/graph-yaml-export-yaml-p1/PROMPT_START_30_v1.md) · 串行链 [`PROMPT_START_SERIAL_v1.md`](../harness/invokes/by-task/graph-yaml-inform-closure-chain/PROMPT_START_SERIAL_v1.md)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-export-yaml-p1` |
| **test_strategy** | `required` |
| **test_strategy_note** | 改 export 主路径 · 须 `--check` + 既有 export/v2 pytest 全绿 |
| **audit_profile** | `post_close` |
| **orchestration** | `Claude Code`（30→40 · 50 skip） |
| **git_branch** | `task/graph-yaml-export-yaml-p1` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **freeze_id** | `GRAPH-YAML-EXPORT-YAML-P1` |
| **epic** | 图谱 YAML 迁移 · 续（Inform 闭环） |
| **blocked_by** | P0 done + **P0 PR CI 绿 + merge** |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | **approved** | 30 | 2026-06-16 人签 · 30 blocked_by **P0 CI 绿 + merge** |
| **HG-REINSPECT** | pending | done | 40 后 · skip 50 |

### P1 开 30 硬闸门（维护者 / P1 Agent 须逐项核对）

| # | 条件 |
| --- | --- |
| 1 | **P0** task 在 `docs/tasks/done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md` · HG-REINSPECT **signed** |
| 2 | P0 PR **GitHub Actions CI 全绿**（`tech-graph` · 合并前必绿 pytest） |
| 3 | P0 PR **已 merge 入 `origin/main`** |
| 4 | `git checkout main && git pull` 含 P0 merge commit |

---

## 背景与目标

当前 **双源** 状态：

| 环节 | 读源 | 问题 |
| --- | --- | --- |
| 编辑 + compile | `*.graph.yaml` | ✅ 已单源 |
| CI `graph_yaml_compile.py --all --check` | YAML ↔ graph.json 切片 | ✅ Post-Epic 已加 |
| **`tech_graph_graph_export.py --check`** | **`*.ai.md` Mermaid** | ❌ 与 YAML 编辑源脱节 |

维护者改 YAML 后，若 `.ai.md` 未同步，`graph.json` export 仍可能通过 `--check`（因 committed 与 stale ai 一致），**YAML 与 graph.json 语义可能静默分叉**。

**完成态**：`build_graph_payload()` 默认自 **7× `.graph.yaml`** 构建 graph_v2 载荷；`--check` 仍与已提交 `graph.json` **语义一致**（无拓扑变更）；`manifest_check` 不再 TIP 同步 `00_main.ai.md`；`99_spec` 去掉 export「过渡」表述。**不**删 `.ai.md` 文件。

---

## 范围

- [ ] **D1** 新增 YAML→graph_v2 构建路径（建议 `tools/tech_graph_graph_v2_yaml.py` 或扩展现有 reference 模块）：遍历 `*.graph.yaml`，合并为与 `build_reference_graph_v2` **等价** 的 graph_v2 对象
- [ ] **D2** `tools/tech_graph_graph_export.py` · `build_graph_payload()` 改调 YAML 路径；CLI/docstring 更新为「默认读 `.graph.yaml`」
- [ ] **D3** 保留 `.ai.md` 解析函数供 **单测 / 迁移对照**，但 **CI 主路径不再依赖** `.ai.md` 内容
- [ ] **D4** `tools/tech_graph_manifest_check.py` L487–492：移除或替换「同步 `00_main.ai.md` auto 区块」TIP → 指向 `_manifest.json` / `00_main.graph.yaml`
- [ ] **D5** 更新 `docs/_tech_graph/99_spec.md` §机器轨：`graph.json` 由 **YAML export** 生成（`.ai.md` 只读 deprecated 对照）
- [ ] **D6** 扩展 pytest：
  - `tests/test_tech_graph_graph_export.py` 或新文件：`--check` exit 0
  - **回归**：在临时 fixture 中故意污染 `.ai.md` Mermaid，确认 export **仍**仅认 YAML（证明 CI 不依赖 ai 轨）
- [ ] **D7** `bash scripts/verify-tech-graph.sh` 步骤顺序不变 · 全绿

## 非范围

- **不** 删除 7× `.ai.md`（G0 本体扫描 · 另 task）
- **不** 手改已提交 `graph.json` 节点/边（除非 export 算法 bug 且须最小 fix · 须 §实现备忘书面说明）
- **不** 幽灵节点 `external_ref` schema
- **不** 改 `graph_yaml_compile.py` Sub-graph 模板（P0 已做）
- **不** 引入 `.cyning-harness/`

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | `fp-export-check-fail` | `--check` 与 committed 不一致 | exit 4 · CI 红 · 修 YAML builder 或对齐 graph.json |
| F2 | `fp-yaml-export-parse` | YAML 缺字段 / 类型错误 | exit 2 · stderr 含 graph_id |
| F3 | `fp-ai-md-still-required` | 回归测试：仅改 ai 仍影响 export | 打回 30 · YAML 路径未真正接管 |

---

## 验收标准

- [ ] `python tools/tech_graph_graph_export.py --check` → **exit 0**
- [ ] `python scripts/graph_yaml_compile.py --all --check` → exit 0（无回归）
- [ ] `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` 全绿
- [ ] 回归测试证明 export **不**依赖 `.ai.md` 漂移（F3）
- [ ] `99_spec` / export 模块 docstring 无「graph.json 仍由 ai 导出」过渡歧义
- [ ] `manifest_check` 无误导性 `00_main.ai.md` TIP
- [ ] task §自检结论已填 · invoke 30/40 落盘

**合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 依赖与引用

| 依赖项 | 路径 |
| --- | --- |
| P0（须先 done） | `docs/tasks/done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md` |
| YAML compile | `scripts/graph_yaml_compile.py` · `load_yaml` · `all_graph_ids` |
| 现有 export | `tools/tech_graph_graph_export.py` |
| graph_v2 参考 | `tools/tech_graph_graph_v2_reference.py` · `tools/tech_graph_graph_v2_schema.py` |
| 历史 export task | `docs/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md` |
| CI | `scripts/verify-tech-graph.sh` · `.github/workflows/tech-graph.yml` |

---

## 实现提示（非强制 · 供 30 参考）

1. **合并策略**：对每个 `graph_id`，从 YAML 读 `nodes`/`edges`/`anchors`，映射为 graph_v2 边对象（`sync`/`type` 与现有 `_classify_label` 一致）。
2. **graphs[] 元数据**：`source` 字段改为 `docs/_tech_graph/{id}.graph.yaml`（或并存 `source_yaml_path`，deprecate `source_ai_path` 命名 · 最小 diff 优先）。
3. **等价验证**：先让 YAML builder 产出与当前 `--check` 一致，再切换 `build_graph_payload` 默认入口。
4. **勿**复制粘贴 7 份解析逻辑 — 复用 `graph_yaml_compile` 的 YAML load + 现有 v2 schema 校验。

---

## 给执行帽的必读列表

- `AGENTS.md`
- 本 task + **确认 P0 已 done**
- `tools/tech_graph_graph_export.py`
- `tools/tech_graph_graph_v2_reference.py`
- `scripts/graph_yaml_compile.py`
- `tests/test_tech_graph_graph_export.py` · `tests/test_tech_graph_graph_v2_equivalence.py`

---

## 实现备忘（30 回填）

| 路径 | 说明 |
| --- | --- |
| | （30 回填） |

### 自检结论

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| | | | |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-16 | HG-TASK-DRAFT approved · 30 blocked_by P0 |
| 2026-06-16 | 初稿 · export 单源 · 串行链 P1 · blocked_by P0 |
