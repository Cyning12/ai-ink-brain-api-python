# Task：闸口 A — 静态 `graph.json` vs Mermaid 语料（代号 A/B）性能对比（后端主导 · v1）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：`done（2026-05-15 验收通过）`  
> **关联规划**：`docs/tech_graph/改进方向.md`（闸口 A / 极低 token 叙事）；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`  
> **父文档（真值口径）**：`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md` — **「下一阶段：静态 graph.json vs 旧 Mermaid — 初步对比方案（v0）」**（§2 代号 A/B、§3 指标表、§3.1 后端子表；**§3.2 浏览器**默认 **N/A** 于主结论，见父文档「结论」主口径）  
> **SOP / 记录模板**：`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md`（**已落盘**；与父文档 **二选一主真值**：本轮采用 **专文** 为总表 / §9 数字单一真值，见「实现备忘」）  
> **invoke_snapshot**：`docs/harness/invokes/invoke_20260515_10_gate-a-scheme1-perf-compare-requirements.md`（需求帽）；`docs/harness/invokes/invoke_20260515_22_gate-a-scheme1-perf-compare-task-audit-r2.md`（任务审核帽 R2）  
> **test_strategy**：`recommended`  
> **test_strategy_note**：对比以 **可复现命令 + 表格化数据** 为主；**P50/P95** 等统计可本地或 Agent 批跑；**不要求**为闸口 A 主结论先把对比写进 **失败即红** 的 pytest 断言（若后续要 CI 钉死再升 `required` 并另开子 task）。  
> **freeze_id**：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`  

---

## 1. 背景与目标

方案1 已具备 **`graph.json` 导出、`--check`、token 粗估附录与 CI**（见 `docs/tasks/done/` 下 graph export / token compare 两单及父文档 §6）。下一阶段需在 **固定样本与固定规则** 下，对比 **代号 A（消费 `graph.json`）** 与 **代号 B（消费与 A 拓扑等价的 Mermaid 源文）** 的关键指标，为「是否继续加码运行时 Mermaid / 何时进入方案2 筹备」提供 **书面证据**，并把 **主结论句** 写回 **`gate_a_scheme1_backend.md`** 的 **「结论」** 与 **§6**（链回要求见父文档 §116–§121）。

**完成态（一句话）**：维护者可仅凭 **本仓文档 + PR 描述** 在固定 commit 上复现 A/B 声明、等价性检查、§3.1 子集与 `token_estimate --json`；父文档「结论」与 §6 勾选状态与本轮数据一致且无 **FP-A～I** 类违规。

---

## 2. 范围 / 非范围

**范围**

- **后端（本仓）**：按父文档 §2 / §3.1 与 `gate_a_scheme1_perf_compare_backend_detail.md`（首 PR 创建或等价内嵌）完成 **采集 SOP、表格模板、failure_paths 样例**；在 **`gate_a_scheme1_backend.md`** 回填 **§3.1 可复现数字**（或明确「与上表一致」引用 **同一小节内已有表**），并更新 **「结论」** 中与 A/B 对比相关的 **一句主结论**（不得与 §0 **(B)** /「结论」中 **§3.2 浏览器 N/A** 策略矛盾）。  
- **父文档 §6 勾选（本 task 负责子集）**：在 **§3.2 仍为 N/A** 的前提下，推动 §6 清单达到 **可签收形态**（见下文 **§4.1** 与 **§9 文档张力** 的执行口径）。  
- **代号 B 默认样本**：与父文档 §2 一致 — **同一母集合** `docs/_tech_graph/*.ai.md`（**跳过 `99_*.md`**），按导出/token 工具相同 fence 规则得到 **Mermaid 语料总串**（默认实现即 `tools/tech_graph_token_estimate.py` 对 B 侧）；若改用「仅最大单文件」等 **其它 B**，须在对比文档 **显式另起一行声明**，并与默认 B **分列**，禁止 silent 混用。  
- **等价性最低门槛**：节点数 / 边数 / 标签字符量 + **一次 spot-check**（记录执行人/日期或 PR 评论链）；若 A/B 规模不一致，结果仅作 **附录**，不得作为主结论（父文档 §2）。  
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
| 性能对比 SOP（首 PR 创建或等价） | `ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md` |
| 规划 | `docs/tech_graph/改进方向.md` |
| SPEC 方案1 | `docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md` |
| 导出 / 校验 | `ai-ink-brain-api-python/tools/tech_graph_graph_export.py` |
| Token 粗估 | `ai-ink-brain-api-python/tools/tech_graph_token_estimate.py` |
| 已完成基线 task | `ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md`；`ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_a_token_compare_v1.md` |
| 工作区收口（上下文） | `docs/harness/tasks/done/task_engineering_tech_graph_gate_a_closeout_v1.md` |

---

## 4. 验收标准（可勾选）

### 4.1 与父文档 §6「交付物清单」的对照（避免误签收）

| §6 条目 | 本 task 默认（§3.2 N/A）下的签收要求 |
|--------|--------------------------------------|
| 总对比表（§3 各维度） | **须存在**一张表或分表：浏览器向维度 **显式标 N/A** 并链至父文档「结论」主口径；**Agent 向**（载荷/token 等）**须有数或引用** `tech_graph_token_estimate.py --json` 与 `wc -c` 等。 |
| 后端子表（§3.1） | **已填**或可链至 **同一 PR 内** `gate_a_scheme1_perf_compare_backend_detail.md`（或父文档已内嵌且声明「主表在此」）；含 **导出 / `--check` / 产物字节 / pytest / CI step** 的可测子集与 **commit + 日期**。 |
| 前端子表（§3.2） | **一行**：产品无用户页大图谱 Mermaid → §3.2 N/A；链 **「结论」→ 主结论口径**；**不**留空白假装已测。 |
| 等价性说明 | **有**：节点/边/标签量 + spot-check 记录；若不一致则 **附录** 声明且不进主结论。 |
| 书面结论一句 | 与「结论」互链或同文更新；语义与 **暂缓方案2** 等父文档约束一致。 |

**§6 勾选门闸（防假签收）**：父文档 **§6 四行 `[ ]`** 仅当 **「总对比表」已在仓库内存在可导航锚点**（`gate_a_scheme1_perf_compare_backend_detail.md` 专文或父文档内小节标题）、且与 **「仓库或 CI 快照引用」** / **「结论」** 互链一致后，方可改为 **`[x]`**；禁止「仅改勾选、主表未落盘或未互链」。

### 4.2 原子验收（勾选）

- [x] **`gate_a_scheme1_perf_compare_backend_detail.md`**：已存在且含 **（1）环境固定说明**（cwd、Python 版本建议、`freeze_id`）、**（2）逐步采集命令**、**（3）记录表头（建议含：指标名 / 代号或计时消歧 / 原始值 / N / commit / 备注）**、**（4）failure_paths 模板（可与 §5 同构）**；或经审查认可在「实现备忘」声明 **「与父文档 §116–§3.1 等价内嵌，不另文件」** 并指出锚点标题。  
- [x] **代号 A/B 声明**：对比文档（detail 或父文档增节）中 **显式**写出本轮 **A 输入**（`docs/_tech_graph/graph.json` 路径 + `wc -c` 或等价）与 **B 输入**（默认拼接规则引用 `tech_graph_token_estimate.py` 行为描述，或备选 B 另行列出）。  
- [x] **指标最小集（后端子集）**：至少覆盖父文档 §3.1 表中 **导出 wall、`--check`、产物字节、`pytest tests/test_tech_graph_graph_export.py` 耗时** 的可测子集，并给出 **同一 commit / 日期**；**Agent/LM 向**：**粘贴或链** `python tools/tech_graph_token_estimate.py --json` 输出（与既有附录一致或说明 bump 理由）。  
- [x] **计时消歧**：任何表格或正文若出现「A/B」计时，须标注为 **「§2 代号 A/B」** 或 **「计时 A / 计时 B（跑数环境）」**（父文档已有术语表；禁止混用两行指标）。  
- [x] **`gate_a_scheme1_backend.md`**：**「结论」** 与 **§6** 与本轮数据 **一致**；若 §3.2 仍为 N/A，**不得**用浏览器表作主结论依据；**「仓库或 CI 快照引用」** 可按父文档约定追加本轮 **对比分支/commit、跑数环境、原始日志或表格路径**（与父文档 §47 说明一致）。  
- [x] **PR / CI**：合入 PR 描述含 **复现命令** 与（若适用）**Actions run id** 或短 hash；**不**把 run id 写入本 task 的 **`freeze_id`** 行。  
- [x] **归档**：验收后按 `docs/tasks/README.md` **`git mv` → `done/`** 并更新 **`docs/tasks/_views/done.md`**；若曾列入 **`_views/design.md`** / **`in_progress.md`** 则同步。  

---

## 5. failure_paths

| ID | 触发 | 行为 / 语义 | 可重试 | 用户可见类型 |
|----|------|-------------|--------|----------------|
| FP-A | A/B **拓扑或规模未对齐**仍写入主结论 | **禁止合入**；退回补 spot-check 或改附录 | 修数据后可重试 | 审查 / CI |
| FP-B | **更换 B 样本定义**未在文档单列声明、与默认 B **混用** | **禁止**作为主结论；退回改文档 | 更正表述后可重试 | 同上 |
| FP-C | 仅更新父文档 **结论句**但 **无**可复现命令/commit | 视为验收 **不通过**（父文档 FP-2 类） | 补链后可重试 | 维护者 |
| FP-D | 将 **§3.2 浏览器**数据在 **未启用产品场景**下写入主结论 | 与闸口 **(B)** 冲突；退回删改或先立产品 task | 策略澄清后可重试 | 产品 / 架构 |
| FP-E | §6 **总对比表**在 §3.2 N/A 时仍留 **空白浏览器列**且无 N/A 声明 | 视为文档 **未完成**；与 FP-D 同类风险 | 补 N/A 行与链后可重试 | 审查 |
| FP-F | 父文档 §164「主结论仍以 §3 **全表**为准」被误读为 **必须填满浏览器数值** | **本 task 签收口径**：§3.2 N/A 时全表浏览器维 **允许且应当** N/A；主结论语义以「结论」+ Agent 向 + §3.1 为准（见 **§9**） | 澄清文档后可重试 | 维护者 |
| FP-G | 已创建 `gate_a_scheme1_perf_compare_backend_detail.md` 但 **缺 §9（或等价锚点）**，或与 **§7 单一真值**策略冲突（两处数字漂移） | **禁止合入**；退回补小节或合并真值 | 更正后可重试 | 审查 |
| FP-H | 复现命令或正文从 **`docs/tech_graph/改进方向.md` §1.4** 抄 **`export_graph_json.py`** 等 **非本仓落地脚本名** 作为本 task 证据链 | **禁止**；本仓 CLI 真值以 **§3 依赖表** 与 **`tech_graph_graph_export.py`** 为准（§1.4 仅为规划示例，**易过期**） | 更正命令后可重试 | 维护者 |
| FP-I | 表格/正文将 **「计时 A/B」** 与 **「§2 代号 A/B（JSON/Mermaid）」** 混在同一列名或脚注且未拆开 | 视为 **术语违规**；审查不通过（与代号/计时混读同类风险） | 更正后可重试 | 审查 |

---

## 6. 测试策略（Harness §5）

- **`test_strategy`**：`recommended`（见头部 `test_strategy_note`）。  
- **自检建议**：在 task「自检结论」中贴 **`python tools/tech_graph_token_estimate.py --json`**、**`time`/`/usr/bin/time`** 或等价输出要点，以及 **`pytest tests/test_tech_graph_graph_export.py -q`**（若本轮触达）。

---

## 7. 给执行帽的必读列表

1. **`gate_a_scheme1_backend.md`** 全文：**「结论」主口径** vs **§3.2 N/A** vs **§164 后端子表说明**。  
2. **§2 代号 A/B** 与 **「计时 A/B」** 术语表，避免读错行。  
3. **`tech_graph_token_estimate.py`** 与 **`tech_graph_graph_export.py`** 的 **输入根与跳过 `99_*`** 规则与导出 golden **一致**。  
4. 若触达前端 §3.2：**先**有 **`ai-ink-brain`** task 与产品确认，**再**采数。  
5. **`gate_a_scheme1_perf_compare_backend_detail.md`**（已落盘）：须含可导航 **§9（`#sec9-perf-backend`）** 与 **§4（`#sec4-master-table`）**；与父文档 **「后端 §3.1 采样记录」** 的 **单一真值策略**（只在一处维护数字，另一处引用），避免双轨漂移。  
6. **`docs/tech_graph/改进方向.md` §1.4**：仍可能出现 **`export_graph_json.py`** 等历史示例名 — **不得**采为本 task 复现真值；触犯见 **FP-H**。

---

## 8. 假设与待确认

| 类型 | 内容 |
|------|------|
| **假设** | 本轮仍 **无**用户页大图谱 Mermaid；§3.2 保持 N/A。 |
| **待确认** | 若产品侧变更需启用 §3.2：**停止**以本单名义合入浏览器主结论；另开前端 task 后再采。 |
| **已选** | 「总对比表」主真值落盘 **`gate_a_scheme1_perf_compare_backend_detail.md`**（§4 `#sec4-master-table` / §9 `#sec9-perf-backend`）；PR 描述须写一句，与父文档 `gate_a_scheme1_backend.md`「后端先行（SOP）」段一致。 |

---

## 9. 文档张力（矛盾披露 · 执行口径）

以下 **非代码冲突**，为 **措辞/读者误读** 张力；执行与审查时以 **本小节口径** 为准。

| ID | 陈述 A（出处） | 陈述 B（出处） | **执行口径（本 task）** |
|----|----------------|----------------|-------------------------|
| T-1 | 父文档 §164：性能对比主结论仍以 **§3 全表** 为准。 | 父文档「结论」：§3.2 **N/A** 时浏览器向 **不**入主结论。 | §3 全表在 §3.2 N/A 时 **浏览器相关格填 N/A + 理由**；**数值主结论**以 Agent 向 + §3.1 + token 附录支撑，**不**强行套用 §5 浏览器阈值。 |
| T-2 | 父文档链至 `gate_a_scheme1_perf_compare_backend_detail.md` §9。 | 历史 draft 阶段该文件 **常不存在**。 | **已创建**专文并含 §9（`#sec9-perf-backend`）与 §4（`#sec4-master-table`）；父文档 **§6** 与快照区已互链，死链消除。 |
| T-3 | **`改进方向.md` §1.4** 规划示例：`tools/export_graph_json.py`。 | 本仓落地与 task 依赖为 **`tech_graph_graph_export.py`** / **`tech_graph_token_estimate.py`**。 | 本 task **书面证据与复现命令**以依赖表与父文档为准；误抄规划示例 → **FP-H**；规划文勘误可 **另开** 小单，**不**阻塞本单证据链若未引用错误脚本名。 |

---

## 10. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
|----|------|
| PR / commit | **`PR #28`** 合入 `main`（merge **`2315937`**）；文档交付链 tip **`47a6f9e`**（**勿**将 Actions run id 写入头部 `freeze_id` 行） |
| detail 路径 | `ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md`（§4 `#sec4-master-table`、§9 `#sec9-perf-backend`） |
| 父文档 §6 / 结论更新 commit | `gate_a_scheme1_backend.md`（§3 **3.0**、§6 `[x]`、专文互链、快照区 `--json` 迁至专文 §9） |

### 自检结论（`test_strategy: recommended`）

**cwd**：`ai-ink-brain-api-python` 仓根。

```bash
python tools/tech_graph_token_estimate.py --json
wc -c docs/_tech_graph/graph.json
pytest tests/test_tech_graph_graph_export.py -q
```

**输出要点（本轮本地）**

- `token_estimate --json`：`A.bytes_utf8` **20224**，`B.bytes_utf8` **20953**，`heuristic_tokens` **5056 / 5026**，`ratio_B_per_A.heuristic_tokens` **0.9941**；`rules` 明示 **非官方 tiktoken**。  
- `wc -c docs/_tech_graph/graph.json`：**20224**（与 JSON 内 **A** 一致）。  
- `pytest tests/test_tech_graph_graph_export.py -q`：**6 passed**（收集 + 执行约 **0.01s** 量级，以终端为准）。  

**PR 描述一句（必选）**：**总对比表主真值在 `gate_a_scheme1_perf_compare_backend_detail.md` 专文（§4 / §9）**；父文档仅保留 **结论**、**§3.0** 导航行与 **§6** 勾选互链（单一真值策略）。

---

## 11. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-15 | 执行帽：新建 `gate_a_scheme1_perf_compare_backend_detail.md`；父文档 §3 **3.0**、§6、`--json` 单一真值迁专文 §9；§8 **已选** 与 **§10 自检结论** 回填。 |
| 2026-05-15 | 需求帽细化：§4.1 §6 对照、计时消歧验收、FP-E/FP-F、假设与待确认、§9 文档张力、§7 单一真值策略、§11 修订记录骨架。 |
| 2026-05-15 | 需求帽补丁：§4.1 **§6 勾选门闸**；FP-G/FP-H/FP-I；§9 **T-3**（规划示例脚本名 vs 落地）；§7 必读第 6 条；头部 **invoke_snapshot**；完成态用语扩至 FP-A～I。 |
| 2026-05-15 | 维护：`PR #28` 合入 `main`（merge `2315937`）；§4.2「PR / CI」「归档」勾选；§10 `PR / commit` 回填；头部 **`done（2026-05-15 验收通过）`**；`git mv` 至 `docs/tasks/done/` 并更新 `_views`；**按审查 R2 回填** 见 [`task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md`](../../harness/reviews/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md)。 |

> **按审查回填**：工作区 closeout **R4** 对 `task_engineering_tech_graph_gate_a_closeout_v1` **无硬性回填项**至本单；见 [`docs/harness/reviews/task_engineering_tech_graph_gate_a_closeout_v1_audit_R4_20260515.md`](../../../../docs/harness/reviews/task_engineering_tech_graph_gate_a_closeout_v1_audit_R4_20260515.md)（可选追溯）。**按审查 R2 回填**（§4.2 收尾、§10、`invoke_snapshot`、归档）：[`task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md`](../../harness/reviews/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md)。

---

## 给 Cursor

`gate_a`、`graph.json`、**代号 A/B**、`tech_graph_token_estimate`、`freeze_id`、`§3.1`、`§3.2`、`docs/tasks/done`、`failure_paths`、`§6`
