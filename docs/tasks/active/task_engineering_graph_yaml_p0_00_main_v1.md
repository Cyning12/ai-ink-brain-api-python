# Task · 图谱 YAML 源 P0（00_main · Graph Source v3 试点）

> **状态**：`active`（**HG-TASK-DRAFT approved** · 可派 00/10）  
> **schedule_ref**：图谱 YAML 试点 · P0  
> **epic**：Engineering · `_tech_graph` Graph Source v3  
> **关联图谱**：`[00_main.md](../_tech_graph/00_main.md)` · `[QNA_graph_wiki_history_upgrade_v1_zh.md](../_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md)`  
> **invoke 入口**：`[PROMPT_START_00_v1.md](../harness/invokes/by-task/graph-yaml-p0-00-main/PROMPT_START_00_v1.md)`  
> **关账 checklist**：`[HG-GRAPH-P0-CLOSE_checklist_v1_zh.md](../harness/invokes/by-task/graph-yaml-p0-00-main/HG-GRAPH-P0-CLOSE_checklist_v1_zh.md)`

---

## Harness 元信息


| 字段                     | 值                                                 |
| ---------------------- | ------------------------------------------------- |
| **task_slug**          | `graph-yaml-p0-00-main`                           |
| **test_strategy**      | `required`                                        |
| **test_strategy_note** | YAML→MD 转换须可失败单测；与现有 `graph.json` diff 校验         |
| **audit_profile**      | `full`                                            |
| **orchestration**      | **00 总调度** → 10（R0–R5）→ 22 → 30 → 40 → 50 → CLOSE |
| **git_branch**         | `task/graph-yaml-p0-00-main`                      |
| **worktree_root**      | `ai-ink-brain-api-python/`                        |
| **kpi_rubric**         | `KPI_RUBRIC_v1_2`                                 |
| **kpi_aggregator**     | `CLOSE`                                           |
| **experience_capture** | `recommended`                                     |
| **freeze_id**          | （30 完成后填，如 `GRAPH_YAML_P0_FREEZE_YYYYMMDD`）       |


### 人工闸


| human_gate_id           | status       | blocks_hats | 说明                                                                                                                                               |
| ----------------------- | ------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **HG-TASK-DRAFT**       | **approved** | 10, 22, 30  | task 初稿 · SPEC/QNA 对齐 · **人签后开 10**                                                                                                              |
| **HG-AUDIT-R1**         | pending      | 30          | 22 R1 落盘 + 思考轮闭合 · 人签后 30                                                                                                                        |
| **HG-REINSPECT**        | pending      | CLOSE       | 50 复检落盘 · 人签后 CLOSE                                                                                                                              |
| **HG-GRAPH-P0-SIGNOFF** | pending      | done        | `[HG-GRAPH-P0-CLOSE_checklist](../../harness/invokes/by-task/graph-yaml-p0-00-main/HG-GRAPH-P0-CLOSE_checklist_v1_zh.md)` 全勾 · 人签后 `git mv` done |


### 帽序（硬 · 由 00 总调度执行）

```text
[HG-TASK-DRAFT approved]
  → 10（R0–R5 多轮思考 · invoke PROMPT_10）
  → 22 R1（审查思考 + task 完整性）
  → [HG-AUDIT-R1 approved]
  → 30（00_main.graph.yaml + 转换器 + CI 校验 · 不删 .ai.md）
  → 40
  → 50
  → [HG-REINSPECT approved]
  → CLOSE + [HG-GRAPH-P0-SIGNOFF approved]
  → git mv → done/
```

---

## 背景与目标

在 **不接入 `@cyning/harness` 产品包**、不推翻现有 `graph.json` / manifest / CI 的前提下，试点 **YAML 作为 flowchart 编辑源**，生成 **统一 `.md`（人+AI 共读）**，为后续废 `.ai.md`（P1–P2）奠基。

**P0 完成态**：

- `docs/_tech_graph/00_main.graph.yaml` 为 **00_main 唯一编辑源**
- 脚本生成 `00_main.md`（含 Mermaid + 结构化表格/元数据）
- CI 或 pre-commit：**YAML 与现有 `graph.json` 中 `00_main` 切片一致**（或 documented diff）
- **保留** `00_main.ai.md`（标记 `@deprecated · 源迁 YAML`），P0 **不删除**

**理论依据**：`[QNA_graph_wiki_history_upgrade_v1_zh.md](../_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md)`

---

## 范围

- [ ] `00_main.graph.yaml` schema 草案（nodes/edges/anchors/graph_id · 对齐 `99_mermaid_protocol.md`）
- [ ] 转换脚本（建议 `scripts/graph_yaml_compile.py` 或 `tools/`）
- [ ] 生成 `00_main.md`（人类可读 + AI 可解析 frontmatter/表格）
- [ ] 与 `graph.json` / `00_main` 节点集 **diff 校验**（脚本 + 文档）
- [ ] 10–50 invoke/review 按 `by-task/graph-yaml-p0-00-main/` 落盘
- [ ] 关账：HG-GRAPH-P0-CLOSE checklist 维护者全勾

## 非范围

- **不** `npx @cyning/harness init/upgrade`（Harness 迁移另 task）
- **不** 删除任意 `.ai.md`（P0 仅 00_main）
- **不** 迁移 `10_flow_`* 共 6 张（P1+）
- **不** 改 `ai-ink-brain` 前端仓
- **不** 回灌 `cyning-harness` 产品模板（P0 验收后另 Epic）
- **不** `trace.json` / `.version/` History（QNA 远期）

---

## 行为变更（Delta）

**无** — 纯工程/文档管线；运行时 API 行为不变。

---

## 依赖与引用


| 依赖项             | 路径                                                         |
| --------------- | ---------------------------------------------------------- |
| Q&A 升级方案        | `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` |
| 拓扑协议            | `docs/_tech_graph/99_mermaid_protocol.md`                  |
| graph v2 schema | `docs/_tech_graph/graph_v2_schema.md`                      |
| 聚合图             | `docs/_tech_graph/graph.json`                              |
| manifest        | `docs/_tech_graph/_manifest.json`                          |
| CI 红 RUNBOOK    | `docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md`  |
| 00 总调度          | `docs/harness/prompts/hats/00-orchestrator.md`             |
| 10 思考轮          | `docs/harness/prompts/hats/10-requirements.md` §思考轮        |


---

## 给执行帽的必读列表

- `AGENTS.md`
- `docs/_tech_graph/00_main.ai.md`（迁移前真值）
- `docs/_tech_graph/graph.json`（`graph_id: 00_main` 切片）
- `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` §2 YAML 工作流

---

## 失败路径


| #   | Scenario ID     | 触发条件                  | 系统行为             | 可重试 | 用户可见                |
| --- | --------------- | --------------------- | ---------------- | --- | ------------------- |
| F1  | `fp-yaml-parse` | YAML 语法错误             | 转换脚本 exit 1 + 行号 | 是   | CI 失败日志             |
| F2  | `fp-graph-diff` | 生成图与 graph.json 不一致   | diff 脚本 exit 1   | 是   | CI 报告节点/边清单         |
| F3  | `fp-gate-draft` | HG-TASK-DRAFT pending | 10/30 拒开工        | 是   | gate-check / task 表 |


---

## 思考轮次（10 帽预置 · HG-TASK-DRAFT 签后执行）

> invoke：`[PROMPT_10_rethink_R0_R5_v1.md](../../harness/invokes/by-task/graph-yaml-p0-00-main/PROMPT_10_rethink_R0_R5_v1.md)`

### 思考轮控制


| 字段                    | 值      |
| --------------------- | ------ |
| **actual_last_round** | `（待填）` |
| **early_stop**        | `（待填）` |
| **early_stop_reason** | `（待填）` |
| **residual_risks**    | `（待填）` |


### R0 · 读 task / QNA / 非范围

**回填区：** `（待填）`

### R1 · 代码与图谱事实（00_main.ai.md · graph.json 切片）

**回填区：** `（待填）`

### R2 · 方案对比（YAML schema · 生成 MD 结构 · 脚本语言）

**回填区：** `（待填）`

### R3 · 边界 / CI / failure_paths / 与 manifest 关系

**回填区：** `（待填）`

### R4 · pytest / 校验命令 / PR 策略

**回填区：** `（待填）`

### R5 · 图谱增量 · P1 路线图 · 关账条件

**回填区：** `（待填）`

---

## 验收标准

- [ ] `00_main.graph.yaml` 落盘且可解析
- [ ] `python scripts/graph_yaml_compile.py`（或等价）生成 `00_main.md`
- [ ] diff 校验：`00_main` 节点/边与 `graph.json` **一致**（或书面记录例外 + 维护者签 checklist §2）
- [ ] `pytest` 含 ≥1 转换/校验用例（`test_strategy: required`）
- [ ] 10/22/30/40/50 invoke 落盘 · 22 R1 approved · 50 reinspect 落盘
- [ ] **HG-GRAPH-P0-CLOSE** checklist 维护者全勾 · task → `done/`
- [ ] **未** 引入 `.cyning-harness/` · **未** 删 `.ai.md`

**合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 实现备忘（30 回填）


| 路径                                                    | 说明       |
| ----------------------------------------------------- | -------- |
| `docs/_tech_graph/00_main.graph.yaml`                 | P0 编辑源   |
| `scripts/graph_yaml_compile.py`                       | 待建       |
| `docs/harness/invokes/by-task/graph-yaml-p0-00-main/` | invoke 链 |


### 自检结论（执行者）


| #   | 命令      | 退出码 | 摘要  |
| --- | ------- | --- | --- |
| —   | （40 回填） | —   | —   |


### KPI（00）


| 维度  | 结论         |
| --- | ---------- |
| —   | （CLOSE 回填） |


---

## 修订记录


| 日期         | 说明                                                |
| ---------- | ------------------------------------------------- |
| 2026-06-16 | 初稿 · 00→10→50→人签 checklist 帽序 · 不接 cyning-harness |


