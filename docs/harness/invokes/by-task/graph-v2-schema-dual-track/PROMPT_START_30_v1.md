# 启动 Prompt · 30 执行 · graph-v2-schema-dual-track

> **用法**：Open Folder **`ai-ink-brain-api-python/`** → **新对话** → 复制下方 **整段代码块** 发送。  
> **人签**：**HG-TASK-DRAFT approved** · **HG-REINSPECT approved**（post_close · 50 可 skip）  
> **硬闸门**：G1 **done** · Inform 闭环 **done** · **禁止** 改 `cyning-harness/` / HGM

| 项 | 值 |
| --- | --- |
| **task_slug** | `graph-v2-schema-dual-track` |
| **git_branch** | `task/graph-v2-schema-dual-track` |
| **test_strategy** | `required` |
| **freeze_id** | `GRAPH-V2-SCHEMA-DUAL-TRACK` |
| **invoke 索引** | [`README.md`](./README.md) |

---

```text
你是 **30 执行 Agent**（Ink 后端仓 · Inform 规范层 · graph_v2 JSON Schema 双轨）。

【开帽 · GATE_SCAN · 硬闸门 · 缺一 STOP】
- HG-TASK-DRAFT: **approved** ✓（核对 task 表 · 非仅 invoke 假设）
- HG-REINSPECT: **approved** ✓（post_close · 50 skip 按 task）
- Inform 闭环 done：P0–P1 export-from-YAML + G0 删 .ai.md
- 工作区 G1 HGM **done**（资源调度已满足 · 本 task 与 G1 **轨正交**）
- Open Folder: **ai-ink-brain-api-python/**（仅此仓写代码）
- **禁止** 改 cyning-harness/ · events/*.jsonl · harness graph ingest
- **禁止** 同 PR 混入 HGM / 产品仓变更（F4）
- cwd: ai-ink-brain-api-python/
- 分支: task/graph-v2-schema-dual-track（无则从 main 创建）

严格遵循：
- docs/tasks/active/task_engineering_graph_v2_schema_dual_track_v1.md（D1–D7 · 非范围 · failure_paths）
- docs/harness/prompts/hats/30-execute-code.md
- AGENTS.md · docs/_tech_graph/99_spec.md

【canonical 读序】
1. docs/harness/invokes/by-task/graph-v2-schema-dual-track/README.md
2. docs/tasks/active/task_engineering_graph_v2_schema_dual_track_v1.md
3. ai_coding_governance/methodology/graph/GUIDE_inform_spec_layer_format_selection_v1_zh.md §3.2
4. docs/_tech_graph/graph_v2_schema.md
5. tools/tech_graph_graph_v2_schema.py（现有 validate_graph_v2 行为 = pytest 基准）
6. docs/_tech_graph/graph.json（committed 实例 · 禁止手改拓扑）
7. tests/test_tech_graph_graph_v2*.py · tests/test_tech_graph_graph_export.py

═══════════════════════════════════════════════════════════
 背景
═══════════════════════════════════════════════════════════

flowchart 已 YAML 单源（*.graph.yaml → export → graph.json）。
**规范层** graph_v2 结构说明仍在 MD + Python 硬编码双份，可能 drift。

目标：
  graph_v2.schema.json   ← 机器 canonical
  graph_v2_schema.md     ← 人读 + 指向 JSON
  validate_graph_v2()    ← 薄封装 · 单一真值

Agent 消费不变：graph_query 子图 · **不**默认 @ schema 全文。

═══════════════════════════════════════════════════════════
 30 执行 · D1–D7
═══════════════════════════════════════════════════════════

【0 · 分支】
git checkout main && git pull
git checkout -b task/graph-v2-schema-dual-track

【D1 · graph_v2.schema.json 落盘】
- 路径：优先 `docs/_tech_graph/graph_v2.schema.json`（与 graph.json 同目录 · 30 前在 task §实现备忘 定格）
- 内容：覆盖 P2-0 + P2-4a（nodes[].kind · graphs[] · edges[].ref · FP-4-4 无 graphs 仍合法）
- 基准：与当前 `validate_graph_v2()` **行为等价** · 以现有 pytest 为真值 · 不收紧未文档化约束

【D2 · 重构 tech_graph_graph_v2_schema.py】
- 校验规则从 JSON 加载（或 JSON 为唯一字段表 · Python 只执行逻辑）
- **禁止** MD 表格与 JSON 双份维护无 CI 约束
- 保留 GraphV2SchemaError · validate_graph_v2 公开签名不变
- D7 可选：graph_id_from_source_path docstring `.ai.md` → `.graph.yaml` / stem

【D3 · 更新 graph_v2_schema.md】
- 文首：`canonical schema: graph_v2.schema.json`
- 字段表：摘要 + 链 JSON · 标注「以 JSON 为准」
- 保留 failure_paths · §8 工具表 · 修订记录

【D4 · CI / verify】
- export --check 仍绿 · schema 校验接在 export 链或既有 tech-graph workflow
- 可选最小：MD 文首 canonical 行存在性检查

【D5 · pytest】
- 现有 test_tech_graph_graph*.py · test_graph_yaml*.py 全绿
- 新增 F1：故意破坏 JSON（缺 schema_version / 非法 ref）→ validate 非 0
- 回归：committed graph.json 仍 pass validate_graph_v2

【D6 · 99_spec.md】
- §机器轨 增一行：graph_v2 schema 双轨 · JSON canonical · MD 人读

【D7 · 可选 docstring】
- 仅措辞 · 无 export 行为变更

═══════════════════════════════════════════════════════════
 非范围（STOP）
═══════════════════════════════════════════════════════════
- HGM · hgm_event_v1.schema.json · cyning-harness 任何路径
- 规范层整体 YAML 化（99_mermaid_protocol · 01_struct 全文）
- external_ref schema · drift/manifest 自动生成
- 手改 graph.json 节点/边（除非 export bug · 须 §实现备忘 书面说明）
- 改 *.graph.yaml flowchart 拓扑

═══════════════════════════════════════════════════════════
 验收命令（40 须独立复跑）
═══════════════════════════════════════════════════════════

python tools/tech_graph_graph_export.py --check
python scripts/graph_yaml_compile.py --all --check
pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q
bash scripts/verify-tech-graph.sh
pytest tests -m "not intent_eval and not intent_benchmark" -q
ruff check api tests

═══════════════════════════════════════════════════════════
 40 自检 + CLOSE
═══════════════════════════════════════════════════════════

- 独立复跑验收命令
- 回填 task §实现备忘 · §自检结论
- invoke 落盘：
  docs/harness/invokes/by-task/graph-v2-schema-dual-track/invoke_YYYYMMDD_30_graph-v2-schema-dual-track.md
  docs/harness/invokes/by-task/graph-v2-schema-dual-track/invoke_YYYYMMDD_40_graph-v2-schema-dual-track.md
- PR → main · CI 全绿 · merge
- task → docs/tasks/done/ · 更新 RECENT §1.8 · HG-REINSPECT 已签则直接关账

【回报格式 · 硬】
## Deliverables（JSON 路径 · 改动文件列表）
## 验收命令输出摘要
## PR URL · CI 状态
## Blockers
```

---

## 前置检查（开 30 前）

```bash
cd ai-ink-brain-api-python
test -f docs/tasks/active/task_engineering_graph_v2_schema_dual_track_v1.md || exit 1
test -f docs/_tech_graph/graph.json || exit 1
test -f tools/tech_graph_graph_v2_schema.py || exit 1
python tools/tech_graph_graph_export.py --check
echo "OK: 可开 graph-v2-schema-dual-track 30"
```
