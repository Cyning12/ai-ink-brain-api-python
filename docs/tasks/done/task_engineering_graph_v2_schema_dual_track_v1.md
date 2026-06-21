# Task · 规范层 · graph_v2 JSON Schema 双轨（Inform · Post-G0）

> **状态**：`done（2026-06-17）`（PR #182 merge `a59a2a8` · HG-TASK-DRAFT approved · 30/40 关账）  
> **schedule_ref**：RECENT **§1.8**  
> **L3 真值**：`[GUIDE_inform_spec_layer_format_selection_v1_zh.md](../../../../ai_coding_governance/methodology/graph/GUIDE_inform_spec_layer_format_selection_v1_zh.md)` §3.2 · §5  
> **blocked_by（软）**：`[task_cyning_harness_g1_hgm_v2_v1.md](../../harness/tasks/done/cyning-harness/task_cyning_harness_g1_hgm_v2_v1.md)` · **done**  
> **前置 Inform**：`[task_engineering_graph_yaml_export_from_yaml_p1_v1.md](../done/task_engineering_graph_yaml_export_from_yaml_p1_v1.md)` · **done**  
> **invoke**：`[PROMPT_START_30_v1.md](../../harness/invokes/by-task/graph-v2-schema-dual-track/PROMPT_START_30_v1.md)`

---

## Harness 元信息


| 字段                     | 值                                                                      |
| ---------------------- | ---------------------------------------------------------------------- |
| **task_slug**          | `graph-v2-schema-dual-track`                                           |
| **test_strategy**      | `required`                                                             |
| **test_strategy_note** | schema JSON 与现有 `validate_graph_v2` 行为等价 · pytest 全绿 · `tech-graph` CI |
| **audit_profile**      | `post_close`                                                           |
| **orchestration**      | `Claude Code`（30→40 · 50 按仓常模）                                         |
| **git_branch**         | `task/graph-v2-schema-dual-track`（立项后定）                                |
| **worktree_root**      | `ai-ink-brain-api-python/`                                             |
| **freeze_id**          | `GRAPH-V2-SCHEMA-DUAL-TRACK`                                           |
| **epic**               | Inform 规范层 · Post-YAML                                                 |


### 人工闸（草案）


| human_gate_id     | status   | blocks_hats | 说明                                  |
| ----------------- | -------- | ----------- | ----------------------------------- |
| **HG-TASK-DRAFT** | approved | 22, 30      | 维护者签 · 可与 G1 并行立项文档 · **实现建议 G1 后** |
| **HG-REINSPECT**  | approved | done        | 50 或 post_close 免检按 task 定稿         |


### 开 30 硬闸门（维护者 / Agent 须逐项核对）


| #   | 条件                                                                         |
| --- | -------------------------------------------------------------------------- |
| 1   | Inform 闭环 **done**（P0–P1 export-from-YAML · G0 删 `.ai.md`）                 |
| 2   | **（推荐）** 工作区 G1 task **done** 或维护者 invoke 书面「与 G1 并行、不改 cyning-harness 金样」 |
| 3   | Open Folder `**ai-ink-brain-api-python/`** · 只读本仓 `_tech_graph` / `tools/` |
| 4   | **禁止** 同 PR 混入 HGM / `events/*.jsonl` / 产品仓 `cyning-harness` 改动            |


---

## 背景与目标

### 现状


| 载体                                                                           | 角色                              | 问题                                   |
| ---------------------------------------------------------------------------- | ------------------------------- | ------------------------------------ |
| `[graph_v2_schema.md](../_tech_graph/graph_v2_schema.md)`                    | 人读 · 字段表 · failure_paths · 工具入口 | Agent/CI **不应**默认当 schema 真值全文读入     |
| `[tech_graph_graph_v2_schema.py](../../tools/tech_graph_graph_v2_schema.py)` | 运行时 `validate_graph_v2()`       | 规则 **硬编码在 Python** · 与 MD 表格可能 drift |
| `[graph.json](../_tech_graph/graph.json)`                                    | 拓扑 **实例** · export 产物           | 已有校验 · 禁止手改                          |


### 目标完成态

```text
graph_v2.schema.json     ← 机器 canonical（JSON Schema 或等价 JSON 结构定义）
graph_v2_schema.md       ← 人读说明 + 指向 .json + 修订记录
validate_graph_v2        ← 读 .json 或与其同步的单一真值（Python 薄封装）
Agent 消费               ← 仍 graph_query + manifest 切片 · 不默认 @ schema 全文
```

---

## 范围

- [x] **D1** 落盘 `docs/_tech_graph/graph_v2.schema.json`
- [x] **D2** 重构 `tools/tech_graph_graph_v2_schema.py`
- [x] **D3** 更新 `graph_v2_schema.md`
- [x] **D4** CI / `verify-tech-graph.sh`
- [x] **D5** pytest（含 F1 可失败用例）
- [x] **D6** 更新 `99_spec.md` §机器轨
- [x] **D7** `graph_id_from_source_path` docstring

---

## 非范围

- HGM · `hgm_event_v1.schema.json` · 产品 `harness graph ingest`（Track G · 工作区 G1）
- 规范层整体 YAML 化（`99_spec` · `99_mermaid_protocol` · `01_struct`）
- `[task_engineering_graph_yaml_external_ref_backlog_v1.md](./task_engineering_graph_yaml_external_ref_backlog_v1.md)` · `external_ref` 字段
- drift_check 从 `_manifest` 自动生成（另 task · GUIDE §6 第二项）
- 改 `cyning-harness/` 金样或产品 Y1 schema 抽象（可后续工作区 task 引用本仓 JSON 为试点）

---

## 失败路径


| #   | Scenario ID                  | 触发                                  | 行为                         | 可重试 | 用户可见               |
| --- | ---------------------------- | ----------------------------------- | -------------------------- | --- | ------------------ |
| F1  | `fp-schema-json-drift`       | JSON 与 `validate_graph_v2` 行为不一致    | pytest 红 · 打回 30           | 是   | CI tech-graph 失败   |
| F2  | `fp-committed-graph-invalid` | 现有 `graph.json` 不 pass 新校验          | STOP · 先修 export 或 JSON 定义 | 是   | `--check` exit 非 0 |
| F3  | `fp-md-json-field-drift`     | MD 摘要与 JSON 必填字段集不一致（若启用 D4 可选检查）   | warn 或 CI 红 · task 定稿      | 是   | stderr 列字段差        |
| F4  | `fp-g1-golden-collision`     | 同会话改 Ink schema + cyning-harness 金样 | **禁止** · 拆 PR / 等 G1 CLOSE | —   | 维护者拒 merge         |


---

## 依赖与引用


| 类型               | 路径                                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L3 格式选型          | `[GUIDE_inform_spec_layer_format_selection_v1_zh.md](../../../../ai_coding_governance/methodology/graph/GUIDE_inform_spec_layer_format_selection_v1_zh.md)`                     |
| YAML 迁移报告        | `[REPORT_inform_yaml_migration_before_after_benefits_v1_zh.md](../../../../ai_coding_governance/methodology/graph/REPORT_inform_yaml_migration_before_after_benefits_v1_zh.md)` |
| 现有 schema 说明     | `[docs/_tech_graph/graph_v2_schema.md](../_tech_graph/graph_v2_schema.md)`                                                                                                      |
| 校验实现             | `[tools/tech_graph_graph_v2_schema.py](../../tools/tech_graph_graph_v2_schema.py)`                                                                                              |
| Export           | `[tools/tech_graph_graph_export.py](../../tools/tech_graph_graph_export.py)`                                                                                                    |
| G1（软 blocked_by） | `[task_cyning_harness_g1_hgm_v2_v1.md](../../harness/tasks/done/cyning-harness/task_cyning_harness_g1_hgm_v2_v1.md)` · **done** |
| Agent 消费纪律       | `[AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md](../../../../ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md)` §2.2                          |


---

## 验收标准

- [x] `docs/_tech_graph/graph_v2.schema.json` 存在且可被校验脚本加载
- [x] `python tools/tech_graph_graph_export.py --check` → exit 0
- [x] `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` 全绿
- [x] `graph_v2_schema.md` 含 canonical 指针 · 无「仅 MD 为真值」歧义
- [x] 故意破坏 JSON 必填字段的 pytest 用例 **可失败**（F1）
- [x] task §实现备忘 · §自检结论 · invoke 30/40
- [x] RECENT §1.8 状态同步

---

## 实现备忘（30 帽回填）


| 项              | 内容                                     |
| -------------- | -------------------------------------- |
| 文件列表           | `docs/_tech_graph/graph_v2.schema.json`<br>`tools/tech_graph_graph_v2_schema.py`<br>`docs/_tech_graph/graph_v2_schema.md`<br>`docs/_tech_graph/99_spec.md`<br>`scripts/verify-tech-graph.sh`<br>`tests/test_tech_graph_graph_v2_p4_schema.py` |
| JSON 路径决策      | `docs/_tech_graph/graph_v2.schema.json`（与 `graph.json` 同目录 · task 建议优先路径） |
| 与 Python 同步策略  | 校验器在导入时加载 JSON：必填字段集、允许 `kind`、类型映射、互斥规则均来自 JSON；Python 仅保留跨引用检查（节点存在性、graph_id 存在性、重复 id）与 `GraphV2SchemaError` 语义。 |
| PR / merge SHA | PR [#182](https://github.com/Cyning12/ai-ink-brain-api-python/pull/182) · merge `a59a2a8` · 后续回填 `af363db` |


---

## 自检结论（40 帽回填）

- `python tools/tech_graph_graph_export.py --check` → exit 0
- `python scripts/graph_yaml_compile.py --all --check` → 7/7 OK
- `pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q` → 113 passed, 1 skipped
- `bash scripts/verify-tech-graph.sh` → OK（新增 `graph_v2 schema validation` 步骤）
- `pytest tests -m "not intent_eval and not intent_benchmark" -q` → 423 passed, 1 skipped, 2 deselected
- `ruff check api tests` → All checks passed
- D1 JSON 覆盖 P2-0 + P2-4a：`nodes[].kind`、`graphs[]`、`edges[].ref`、FP-4-4 无 graphs 仍合法
- D2 Python 校验器单一真值来源 JSON；公开签名 `validate_graph_v2` / `GraphV2SchemaError` / `SCHEMA_VERSION_V2` / `ALLOWED_NODE_KINDS` 不变
- D3 `graph_v2_schema.md` 文首 canonical pointer 已加
- D4 `verify-tech-graph.sh` 显式接入 `tools/tech_graph_graph_v2_schema.py`
- D5 新增 F1 回归：缺 `schema_version`、非法 `ref.node_id`；回归 `graph.json` 直接 validate
- D6 `99_spec.md` 机器轨已增 schema 双轨指针
- D7 `graph_id_from_source_path` docstring `.ai.md` → `.graph.yaml`/中性 stem

---

## 给 Cursor

`graph-v2-schema-dual-track` · `test_strategy: required` · `docs/_tech_graph` · `graph_v2.schema.json` · Inform 规范层 · **非 G1** · G1 CLOSE 后开 30 推荐 · `GUIDE_inform_spec_layer_format_selection`

---

## 修订记录


| 日期         | 说明                                          |
| ---------- | ------------------------------------------- |
| 2026-06-17 | 初稿 · deferred · 链 L3 GUIDE §6 · RECENT §1.8 |
| 2026-06-17 | G1 done · active · invoke 30 落盘 |
| 2026-06-17 | T1 30/40 完成 · JSON schema 双轨落盘 · task 关账 |


