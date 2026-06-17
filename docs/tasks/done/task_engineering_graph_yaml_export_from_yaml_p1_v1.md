# Task · 图谱 graph.json 导出改读 YAML（Export-from-YAML · P1）

> **状态**：`done`（**HG-TASK-DRAFT approved** · 串行链 **#2/2** · 40 PASS · HG-REINSPECT signed）  
> **schedule_ref**：RECENT **§1.6 续 #2**  
> **blocked_by**：[`task_engineering_graph_yaml_doc_hygiene_p0_v1.md`](../done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md) · **done** + HG-REINSPECT + **P0 PR CI 全绿且已 merge 入 `main`**  
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
| **HG-REINSPECT** | **signed** | done | 2026-06-17 · 40 自检 PASS · skip 50 |

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

- [x] **D1** 新增 YAML→graph_v2 构建路径（建议 `tools/tech_graph_graph_v2_yaml.py` 或扩展现有 reference 模块）：遍历 `*.graph.yaml`，合并为与 `build_reference_graph_v2` **等价** 的 graph_v2 对象
- [x] **D2** `tools/tech_graph_graph_export.py` · `build_graph_payload()` 改调 YAML 路径；CLI/docstring 更新为「默认读 `.graph.yaml`」
- [x] **D3** 保留 `.ai.md` 解析函数供 **单测 / 迁移对照**，但 **CI 主路径不再依赖** `.ai.md` 内容
- [x] **D4** `tools/tech_graph_manifest_check.py` L487–492：移除或替换「同步 `00_main.ai.md` auto 区块」TIP → 指向 `_manifest.json` / `00_main.graph.yaml`
- [x] **D5** 更新 `docs/_tech_graph/99_spec.md` §机器轨：`graph.json` 由 **YAML export** 生成（`.ai.md` 只读 deprecated 对照）
- [x] **D6** 扩展 pytest：
  - `tests/test_tech_graph_graph_export.py`：`--check` exit 0 + F3 回归
  - **回归**：在临时 fixture 中故意污染 `.ai.md` Mermaid，确认 export **仍**仅认 YAML（证明 CI 不依赖 ai 轨）
- [x] **D7** `bash scripts/verify-tech-graph.sh` 步骤顺序不变 · 全绿

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

- [x] `python tools/tech_graph_graph_export.py --check` → **exit 0**
- [x] `python scripts/graph_yaml_compile.py --all --check` → exit 0（无回归）
- [x] `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` 全绿
- [x] 回归测试证明 export **不**依赖 `.ai.md` 漂移（F3）
- [x] `99_spec` / export 模块 docstring 无「graph.json 仍由 ai 导出」过渡歧义
- [x] `manifest_check` 无误导性 `00_main.ai.md` TIP
- [x] task §自检结论已填 · invoke 30/40 落盘

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
| `tools/tech_graph_graph_v2_yaml.py` | 新增 YAML→graph_v2 builder：`build_yaml_graph_v2()` 遍历 `*.graph.yaml`，映射 mark/type/sync/label，补全 anchor symbol/line，输出与 graph_v2 schema 对齐的载荷 |
| `tools/tech_graph_graph_export.py` | `build_graph_payload()` 改调 `build_yaml_graph_v2()`；docstring / CLI 描述更新为「默认读 `.graph.yaml`」；保留 `collect_raw_edges` / `raw_edges_to_graph_dict` 等 ai.md 解析函数供单测 |
| `tools/tech_graph_graph_equivalence_check.py` | 参考构建器切为 `build_yaml_graph_v2()`，与 export 主路径一致；docstring 更新为 YAML 参考 |
| `tools/tech_graph_manifest_check.py` | 移除 `00_main.ai.md` auto 区块 TIP；改提示 `.graph.yaml` 编辑源 + `_manifest.json` 真值 |
| `docs/_tech_graph/99_spec.md` | §机器轨更新：`graph.json` 由 YAML export 生成；`.ai.md` 为 deprecated 只读对照 |
| `docs/_tech_graph/graph.json` | 由 `python tools/tech_graph_graph_export.py` 重新生成：拓扑一致，节点/边标签按 YAML 真值校正（如 `CTX`→"Context Build"、条件边去 `?>` 前缀 artifact、补回 `includes`/`select`/`service_role` 等语义标签）；`graphs[]` 新增 `source_yaml_path` 并保留 `source_ai_path` 作 deprecated 对照 |
| `tests/test_tech_graph_graph_export.py` | 现有 `build_graph_payload` 用例改为 YAML fixture；新增 `test_build_graph_payload_from_yaml_golden`、`test_build_graph_payload_yaml_protocol_marks`、`test_build_graph_payload_yaml_class_diagram`、`test_run_check_yaml_matches`、`test_run_check_ignores_ai_md_drift`（F3） |
| `tests/test_tech_graph_graph_v2_equivalence.py` | `test_run_check_passes_on_synthetic_v2` 改为 YAML fixture |
| `tests/test_tech_graph_graph_v2_p4_export.py` | `test_export_includes_graphs_and_graph_id` 改为 YAML fixture（节点 ID 不跨图重复） |

### 自检结论

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `python tools/tech_graph_graph_export.py --check` | 0 | 与已提交 graph.json 语义一致 |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7/7 graph slices OK |
| 3 | `bash scripts/verify-tech-graph.sh` | 0 | 全步骤通过（manifest / test manifest / human_gate / compile --check / export --check / drift / graph_v2 equivalence / token estimate） |
| 4 | `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` | 0 | 109 passed, 1 skipped |
| 5 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 419 passed, 1 skipped, 2 deselected |
| 6 | `ruff check api tests` | 0 | All checks passed |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-16 | HG-TASK-DRAFT approved · 30 blocked_by P0 |
| 2026-06-16 | 初稿 · export 单源 · 串行链 P1 · blocked_by P0 |
