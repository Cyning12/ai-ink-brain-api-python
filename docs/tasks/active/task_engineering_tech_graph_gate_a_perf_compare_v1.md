# Task：闸口 A — 静态 `graph.json` vs Mermaid 语料（代号 A/B）性能对比（后端主导 · v1）

> **状态**：`draft`  
> **关联规划**：`docs/tech_graph/改进方向.md`（闸口 A / 极低 token 叙事）；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`  
> **父文档（真值口径）**：`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md` — **「下一阶段：静态 graph.json vs 旧 Mermaid — 初步对比方案（v0）」**（§2 代号 A/B、§3 指标表、§3.1 后端子表；**§3.2 浏览器**默认 **N/A** 于主结论，见父文档「结论」主口径）  
> **SOP / 记录模板**：`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md`（**若仓内尚无此文件**，由本 task 首 PR **创建**或与父文档 §116 起内容 **二选一对齐**，并在「实现备忘」写清路径）  
> **invoke_snapshot**：（开帽后由执行者回填，建议含需求帽 / 审核帽首轮）  
> **test_strategy**：`recommended`  
> **test_strategy_note**：对比以 **可复现命令 + 表格化数据** 为主；**P50/P95** 等统计可本地或 Agent 批跑；**不要求**为闸口 A 主结论先把对比写进 **失败即红** 的 pytest 断言（若后续要 CI 钉死再升 `required` 并另开子 task）。  
> **freeze_id**：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`

---

## 1. 背景与目标

方案1 已具备 **`graph.json` 导出、`--check`、token 粗估附录与 CI**（见 `docs/tasks/done/` 下 graph export / token compare 两单及父文档 §6）。下一阶段需在 **固定样本与固定规则** 下，对比 **代号 A（消费 `graph.json`）** 与 **代号 B（消费与 A 拓扑等价的 Mermaid 源文）** 的关键指标，为「是否继续加码运行时 Mermaid / 何时进入方案2 筹备」提供 **书面证据**，并把 **主结论句** 写回 **`gate_a_scheme1_backend.md`** 的 **「结论」** 与 **§6**（链回要求见父文档 §116）。

---

## 2. 范围 / 非范围

**范围**

- **后端（本仓）**：按父文档 §2 / §3.1 与 `gate_a_scheme1_perf_compare_backend_detail.md`（或首 PR 创建之）完成 **采集 SOP、表格模板、failure_paths 样例**；在 **`gate_a_scheme1_backend.md`** 回填 **§3.1 可复现数字**（或明确「与上表一致」引用），并更新 **「结论」** 中与 A/B 对比相关的 **一句主结论**（不得与 §0 **(B)** 浏览器 N/A 策略矛盾）。  
- **代号 B 默认样本**：与父文档 §2 一致 — **同一母集合** `docs/_tech_graph/*.ai.md`（**跳过 `99_*.md`**），按导出/token 工具相同 fence 规则得到 **Mermaid 语料总串**（默认实现即 `tools/tech_graph_token_estimate.py` 对 B 侧）；若改用「仅最大单文件」等 **其它 B**，须在对比文档 **显式另起一行声明**，并与默认 B **分列**，禁止 silent 混用。  
- **等价性最低门槛**：节点数 / 边数 / 标签字符量 + **一次 spot-check**；若 A/B 规模不一致，结果仅作 **附录**，不得作为主结论（父文档 §2）。  
- **与现有工具对齐**：`tech_graph_graph_export.py`、`tech_graph_token_estimate.py`（`--json`）命令与 **同一 `freeze_id` 提交** 记录在「仓库或 CI 快照引用」或本 task「实现备忘」。

**非范围**

- **方案2 / Neo4j** 实现与立项（仍受父文档「暂缓」约束；本 task **产出证据**而非启动方案2）。  
- **§3.2 浏览器全表**（LCP、chunk、首帧等）：**默认不做**；仅当 **`ai-ink-brain` 产品确认**需用户页大图谱 Mermaid 时，由 **另开前端 task** 启用 §3.2，并在父文档 **显式删除 §3.2 N/A** 后再采 —— 本单正文 **不**假装已完成 §3.2。  
- 修改 **`graph.json` schema 语义**、**契约 manifest**、**导出解析器行为**（除非对比暴露 **必须**修的 bug，则走 **独立 bugfix task** 引用本单）。  
- 替代 **`tech-graph` / `tech-graph-contract` / `pytest` 门禁** 的既有 CI 语义。

---

## 3. 依赖链接（相对工作区根 `Projects/`）

| 项 | 路径 |
|----|------|
| 父文档（对比方案 + 口径） | `ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md` |
| 性能对比 SOP（待创建则首 PR 落盘） | `ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md` |
| 规划 | `docs/tech_graph/改进方向.md` |
| SPEC 方案1 | `docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md` |
| 导出 / 校验 | `ai-ink-brain-api-python/tools/tech_graph_graph_export.py` |
| Token 粗估 | `ai-ink-brain-api-python/tools/tech_graph_token_estimate.py` |
| 已完成基线 task | `ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md`；`ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_a_token_compare_v1.md` |
| 工作区收口（上下文） | `docs/harness/tasks/done/task_engineering_tech_graph_gate_a_closeout_v1.md` |

---

## 4. 验收标准（可勾选）

- [ ] **`gate_a_scheme1_perf_compare_backend_detail.md`**：已存在且含 **采集步骤、记录表头、failure_paths 模板**；或明确写在本 task「实现备忘」**「与父文档 §116–§3.1 等价内嵌，不另文件」** 并经审查认可。  
- [ ] **代号 A/B 声明**：对比文档（detail 或父文档增节）中 **显式**写出本轮采用的 **A 输入**（路径或 `wc -c` 引用 **`docs/_tech_graph/graph.json`**）与 **B 输入**（默认拼接规则或备选 B 声明）。  
- [ ] **指标最小集（后端子集）**：至少覆盖父文档 §3.1 表中 **导出 wall、`--check`、产物字节、`pytest tests/test_tech_graph_graph_export.py` 耗时** 中的可测子集，并给出 **同一 commit / 日期**；**Agent/LM 向**：补充或引用 **`tech_graph_token_estimate.py`** 对 A/B 的 **`--json` 对照**（与既有附录一致或说明 bump）。  
- [ ] **`gate_a_scheme1_backend.md`**：**「结论」** 与 **§6** 与本轮数据 **一致**；若 §3.2 仍为 N/A，**不得**用浏览器表作主结论依据。  
- [ ] **PR / CI**：合入 PR 描述含 **复现命令** 与（若适用）**Actions run id** 或短 hash；**不**把 run id 写入本 task 的 **`freeze_id`** 行。  
- [ ] **归档**：验收后按 `docs/tasks/README.md` **`git mv` → `done/`** 并更新 **`docs/tasks/_views/done.md`**；若曾列入 **`_views/design.md`** / **`in_progress.md`** 则同步。

---

## 5. failure_paths

| ID | 触发 | 行为 / 语义 | 可重试 | 用户可见类型 |
|----|------|-------------|--------|----------------|
| FP-A | A/B **拓扑或规模未对齐**仍写入主结论 | **禁止合入**；退回补 spot-check 或改附录 | 修数据后可重试 | 审查 / CI |
| FP-B | **更换 B 样本定义**未在文档单列声明、与默认 B **混用** | **禁止**作为主结论；退回改文档 | 更正表述后可重试 | 同上 |
| FP-C | 仅更新父文档 **结论句**但 **无**可复现命令/commit | 视为验收 **不通过**（父文档 FP-2 类） | 补链后可重试 | 维护者 |
| FP-D | 将 **§3.2 浏览器**数据在 **未启用产品场景**下写入主结论 | 与闸口 **(B)** 冲突；退回删改或先立产品 task | 策略澄清后可重试 | 产品 / 架构 |

---

## 6. 测试策略（Harness §5）

- **`test_strategy`**：`recommended`（见头部 `test_strategy_note`）。  
- **自检建议**：在 task「自检结论」中贴 **`python tools/tech_graph_token_estimate.py --json`**、**`time`/`/usr/bin/time`** 或等价输出要点，以及 **`pytest tests/test_tech_graph_graph_export.py -q`**（若本轮触达）。

---

## 7. 给执行帽的必读列表

1. **`gate_a_scheme1_backend.md`** 全文：**「结论」主口径** vs **§3.2 N/A**。  
2. **§2 代号 A/B** 与 **「计时 A/B」** 术语表，避免读错行。  
3. **`tech_graph_token_estimate.py`** 与 **`tech_graph_graph_export.py`** 的 **输入根与跳过 `99_*`** 规则与导出 golden **一致**。  
4. 若触达前端 §3.2：**先**有 **`ai-ink-brain`** task 与产品确认，**再**采数。

---

## 8. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
|----|------|
| PR / commit | （回填） |
| detail 路径 | （回填：若新建 `gate_a_scheme1_perf_compare_backend_detail.md`） |
| 父文档 §6 / 结论更新 commit | （回填） |

---

## 给 Cursor

`gate_a`、`graph.json`、**代号 A/B**、`tech_graph_token_estimate`、`freeze_id`、`§3.1`、`§3.2`、`docs/tasks/active`
