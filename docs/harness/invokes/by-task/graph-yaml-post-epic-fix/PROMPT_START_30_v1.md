# 启动 Prompt · 30 执行 · graph-yaml-post-epic-fix

> **用法**：Open Folder **`ai-ink-brain-api-python/`** → 新对话 → 复制下方代码块。  
> **前置**：task [`task_engineering_graph_yaml_post_epic_fix_v1.md`](../../../tasks/active/task_engineering_graph_yaml_post_epic_fix_v1.md) · **HG-TASK-DRAFT approved**  
> **背景**：Epic YAML 迁移 done · 复查发现 `--all` bug · md 漂移 · CI/文档双源

| 项 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-post-epic-fix` |
| **git_branch** | `task/graph-yaml-post-epic-fix` |
| **test_strategy** | `required` |

---

```text
你是 **30 执行 Agent**（Ink 后端仓 · 图谱 YAML Post-Epic 修复）。

严格遵循：
- docs/tasks/active/task_engineering_graph_yaml_post_epic_fix_v1.md（范围 D1–D7 · 非范围）
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- AGENTS.md · docs/_tech_graph/99_mermaid_protocol.md

【开帽 · GATE_SCAN】
- HG-TASK-DRAFT 须 approved，否则 STOP（只报 gate_id）
- cwd: ai-ink-brain-api-python/
- 在分支 task/graph-yaml-post-epic-fix 工作（无则创建）

---

## 复查问题真值（你必须修复）

### BUG-1 · `--all --check` 失败
`scripts/graph_yaml_compile.py` 中 `all_graph_ids()` 使用 `Path.stem`，对 `00_main.graph.yaml` 得到 `00_main.graph`，导致查找 `00_main.graph.graph.yaml`。

**修复**：graph_id = 文件名去掉 `.graph.yaml` 后缀（勿含 `.graph`）。
**验证**：`python scripts/graph_yaml_compile.py --all --check` → exit 0

### BUG-2 · `10_flow_rag.md` 与 YAML 编译漂移
已提交 `10_flow_rag.md` 的 Mermaid body 与 `generate_mermaid(yaml)` 不一致（锚点行数偏多）。
**修复**：`--all` 重生成 7 张 `.md`；若 `notes` 字段被覆盖，从 git 历史或 Epic 关账版恢复 notes 后再编译。

### GAP-1 · CI 未校验 YAML
`scripts/verify-tech-graph.sh` 仅有 `tech_graph_graph_export.py --check`（读 `.ai.md`）。
**修复**：在 export 步骤 **之前** 增加：
```bash
echo "==> verify-tech-graph: graph.yaml compile --check (all graphs)"
python scripts/graph_yaml_compile.py --all --check
```
**禁止** 本 task 改 export 读 YAML（非范围）。

### GAP-2 · 文档仍写机器轨 = .ai.md
更新（最小 diff）：
- `docs/_tech_graph/99_spec.md` §Wiki↔图谱 · **机器轨** 行
- `docs/_tech_graph/99_mermaid_protocol.md` 双轨说明（编辑源 YAML · `.ai.md` deprecated）
- `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` 修订记录一行

**目标表述（示意）**：
- **编辑源**：`*.graph.yaml`
- **人类可读**：`scripts/graph_yaml_compile.py` → `*.md`
- **聚合/查询**：`graph.json`（export 仍自 `.ai.md` · **过渡** · 另 task 迁移）
- **`.ai.md`**：deprecated · 勿再编辑

### GAP-3 · 正文仍链 `.ai.md`
检查 `15_e2e_boundary.md` / `.graph.yaml` 的 `notes` 或边 label 是否指向 `14_runtime_observability.ai.md` → 改为 `.md` 或相对路径无 `.ai.md`。

---

## 执行顺序（硬）

### Step 1 · 修 compile + 测试（D1 D2）
1. 修 `all_graph_ids()`
2. 在 `tests/test_graph_yaml_compile.py` 增加：
   - `test_all_graph_ids_returns_seven_ids_without_graph_suffix`
   - `test_compile_all_check_mode_exits_zero`
3. 跑：`pytest tests/test_graph_yaml_compile.py -q`

### Step 2 · 重生成 .md（D3）
```bash
python scripts/graph_yaml_compile.py --all
python scripts/graph_yaml_compile.py --all --check
```
确认 7 张 `.md` Mermaid body（去掉 frontmatter `generated_at`）与 compile 一致。
**禁止** 手改 Mermaid 块。

### Step 3 · CI 脚本（D4）
改 `scripts/verify-tech-graph.sh` 按 GAP-1。
本地若 human_gate 步失败可跳过该步；**不得** 跳过 YAML --check。

### Step 4 · 文档（D5 D6 D7）
按 GAP-2 GAP-3 更新；不改无关段落。

### Step 5 · 全量验证（40 自检）
```bash
pytest tests/test_graph_yaml_compile.py tests/test_graph_yaml_p1_10_flow_rag.py \
  tests/test_graph_yaml_p2_11_flow_text2sql.py tests/test_graph_yaml_p3a_12_flow_fts.py \
  tests/test_graph_yaml_p3b_13_flow_supabase_rpc.py tests/test_graph_yaml_p4_14_runtime_observability.py \
  tests/test_graph_yaml_p5_15_e2e_boundary.py -q

python tools/tech_graph_graph_export.py --check
python tools/tech_graph_manifest_check.py
python scripts/graph_yaml_compile.py --all --check
```
回填 task §自检结论。

### Step 6 · 落盘与 commit
- invoke: `docs/harness/invokes/by-task/graph-yaml-post-epic-fix/invoke_YYYYMMDD_30_graph-yaml-post-epic-fix.md`
- HANDOFF_AUTO_COMMIT · 勿 commit `.ai.md` 内容变更（除非仅 @deprecated 头 · 本 task 不应改 ai 拓扑）

---

## 非范围（再次强调 · 违反则拒收）

- 不删 `.ai.md`
- 不改 `tools/tech_graph_graph_export.py` 输入源
- 不手改 `graph.json`
- 不接 cyning-harness
- 不做 export-YAML 大迁移（仅文档写「过渡」）

---

## 完成标准

- [ ] BUG-1 BUG-2 GAP-1 GAP-2 GAP-3 均有文件级证据
- [ ] `--all --check` 与相关 pytest 绿
- [ ] task §实现备忘 · §自检结论已填
- [ ] 输出 40 自检摘要（3–5 行）供维护者签 HG-REINSPECT（本 task skip 50 · post_close）

关键词：graph-yaml-post-epic-fix、all_graph_ids、verify-tech-graph、99_spec、10_flow_rag
```
