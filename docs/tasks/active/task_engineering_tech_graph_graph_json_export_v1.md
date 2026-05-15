# Task：技术图谱 — 方案1 静态 `graph.json` 导出与 CI 门禁（后端仓）

> **状态**：`in_progress`（后端仓 `agent-v3`：导出脚本 / pytest / `tech-graph` CI 已落地；合并 `main` 后可改 `implemented` 并归档）  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**（含 **2026-05-15** 勘误行：R1 与 scheme_1「PR 必绿」一致）；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`  
> **invoke_snapshot**：`docs/tech_graph/invokes/invoke_20260514_0000_10_tech-graph-scheme1-dual-task-draft.md`；`docs/harness/invokes/invoke_20260514_0031_10_tech-graph-scheme1-exec-converge.md`；`docs/harness/invokes/invoke_20260515_0000_10_tech-graph-scheme1-exec-converge-hat10.md`（链：`docs/harness/invokes/invoke_20260514_20_tech-graph-scheme1-review-hat20.md`）  
> **test_strategy**：`required`  
> **test_strategy_note**：方案1 核心是 **确定性解析 + 无漂移门禁**；若无 pytest 锁解析与 `--check` 行为，PR 易静默破坏图语义，违背 Harness §5 与 SPEC「CI 门禁」。  
> **freeze_id**：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`

---

## 1. 背景与目标

从本仓 **`docs/_tech_graph/*.ai.md`**（及 SPEC 约定的扫描范围）解析 Mermaid **flowchart** / **classDiagram** 边，生成与同目录对齐的 **`docs/_tech_graph/graph.json`**（schema 含版本与生成时间等，细节在实现 PR 与 SPEC 对齐）。

在 CI 与本地提供 **`--check`**：再生成并与仓库内已提交文件 **无 diff**，否则 **非零退出**。

与 **`tools/tech_graph_contract_check.py`** + **`docs/_tech_graph/_contract_manifest.json`** **并行互补**（契约 vs 架构依赖）：**不得**合并为同一脚本；CI 中 **顺序执行、各自独立失败** 即可。

---

## 2. 范围 / 非范围

**范围**

- 导出脚本落点（建议 `tools/`，例如 `tech_graph_graph_export.py` 或由 SPEC 定名）、`graph.json` schema 初版。  
- **`--check`** 与 `git diff` / 内建 diff 语义写清。  
- **pytest** 覆盖解析与 golden（最小）。  
- 在现有 **quality / pytest workflow** 或专用 step 中接入（本 task **不写死** YAML patch 正文，由执行帽按仓内惯例落 PR）。  
- 与 `tech_graph_contract_check.py` 的调用关系在 PR / 本单「实现备忘」中文档化。

**非范围**

- 方案2 / 方案3。  
- 跨仓合并 `graph.json`。  
- 改写 **`99_mermaid_protocol.md`** 语义（仅遵守）。  
- 替代 **`_contract_manifest`**。

---

## 3. 依赖链接（相对工作区根 `Projects/`）

| 项 | 路径 |
|----|------|
| 规划 | `docs/tech_graph/改进方向.md` |
| SPEC 方案1 | `docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md` |
| SPEC 索引 | `docs/tech_graph/SPEC/README.md` |
| 契约门禁 | `ai-ink-brain-api-python/tools/tech_graph_contract_check.py` |
| 契约真值 | `ai-ink-brain-api-python/docs/_tech_graph/_contract_manifest.json` |
| 拓扑协议 | `ai-ink-brain-api-python/docs/_tech_graph/99_mermaid_protocol.md`（若存在） |
| 闸口 A · token 附录 | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_token_compare_v1.md`；`tools/tech_graph_token_estimate.py` |

---

## 4. 验收标准（可勾选 / 可命令）

- [x] 在本仓根执行：`python tools/tech_graph_graph_export.py` 生成/更新 `docs/_tech_graph/graph.json`。  
- [x] `python tools/tech_graph_graph_export.py --check`：与仓库内已提交 `graph.json` 一致则 **退出码 0**；不一致则 **非 0**，且 stderr 指明差异类型（文件缺失 / schema / 边集合等）。  
- [x] **pytest**：`tests/test_tech_graph_graph_export.py`（解析失败、空图、flowchart / classDiagram golden、`--check` 路径）。  
- [x] `python tools/tech_graph_contract_check.py` 仍可通过（与 graph 导出 **并行**，见 `tech-graph-contract.yml`）。  
- [ ] PR 说明中写清：**contract 门禁** 与 **graph 门禁** 两条命令及顺序（模板见下「CI 命令摘要」）。

**CI 命令摘要（可粘贴 PR）**

1. Graph：`python tools/tech_graph_manifest_check.py` → `python tools/tech_graph_graph_export.py --check` → `python tools/tech_graph_token_estimate.py --json`（`.github/workflows/tech-graph.yml` · job `manifest_check`）。  
2. Contract：`python tools/tech_graph_contract_check.py`（`.github/workflows/tech-graph-contract.yml`，双 checkout；与上并行、独立失败）。

---

## 5. failure_paths

| ID | 触发 | 行为（退出码/日志） | 可重试 | 用户可见类型 |
|----|------|---------------------|--------|----------------|
| FP-1 | `.ai.md` 语法不符合解析器子集 | 非 0；stderr 含文件路径与行级提示 | 修图后本地可重试 | 开发者：CI 失败 / 本地脚本失败 |
| FP-2 | `--check` 下 `graph.json` 漂移 | 非 0；diff 摘要 | 重新生成并提交或修图 | 同上 |
| FP-3 | 仅改 manifest 未跑 contract | （既有）contract 脚本失败 | 同既有流程 | 契约 CI |
| FP-4 | 与 contract 脚本共享 Python 环境损坏 | import 失败 | 重装依赖 | 环境 |

---

## 6. 闸口 A（方案1 后）

在子仓或工作区 **`docs/tech_graph/`** 下增加 **对比实验** 最低结构：**现状 vs 方案1**；须含：

- **指标**：解析正确性抽样方法、`graph.json` 行数/节点数维护成本、CI 增加耗时或失败率观察。  
- **复现命令**：导出 + `--check` + pytest。  
- **仓库或 CI 快照引用**：commit / run id。  
- **结论**：是否进入方案2 筹备。

路径与文件名由执行帽在 PR 中定稿，并在本单 **「实现备忘」** 回填链接。

---

## 7. 给执行帽的必读列表

1. `scheme_1_graph_json.md`：**输入根** `docs/_tech_graph`（相对本仓根）。  
2. 与 **`tech_graph_contract_check.py` 并行**，勿合并逻辑。  
3. **`--check`** 语义与 **已提交文件** 对齐 SPEC。  
4. **闸口 A** 文档与 `graph.json` **同批次或紧随** 的合入策略写在 PR 描述中。

---

## 8. 实现备忘（由执行帽回填）

| 项 | 内容 |
|----|------|
| 导出脚本路径 | `tools/tech_graph_graph_export.py` |
| pytest 路径 | `tests/test_tech_graph_graph_export.py` |
| CI workflow / job | `.github/workflows/tech-graph.yml` → job `manifest_check`（`tech_graph_manifest_check.py` → `tech_graph_graph_export.py --check` → `tech_graph_token_estimate.py --json`）；契约门禁仍为 `.github/workflows/tech-graph-contract.yml` → `contract_check`（**与 graph 并行、独立脚本**） |
| 闸口 A 结论文档 | `docs/tech_graph/gate_a_scheme1_backend.md` |
| 契约变更后 freeze_id | 若 bump 规划 / SPEC，须与前端 task **同一行**更新 **freeze_id**；实现 PR 可将 **短 commit hash** 记入 PR 描述（**不**写入本行 `freeze_id`，以免破坏机械比对） |

---

## 给 Cursor

`graph.json`、`tech_graph_contract_check`、`_contract_manifest`、`--check`、`pytest`、`scheme_1`、`failure_paths`、`test_strategy`、`docs/_tech_graph`
