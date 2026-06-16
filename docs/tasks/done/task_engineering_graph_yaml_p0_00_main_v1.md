# Task · 图谱 YAML 源 P0（00_main · Graph Source v3 试点）

> **状态**：`done`（**HG-GRAPH-P0-SIGNOFF approved** · 2026-06-16）  
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
| **HG-AUDIT-R1**         | **approved** | 30          | 22 R1 落盘 + 思考轮闭合 · 人签后 30                                                                                                                        |
| **HG-REINSPECT**        | **approved** | CLOSE       | 50 复检落盘 · 人签后 CLOSE                                                                                                                              |
| **HG-GRAPH-P0-SIGNOFF** | **approved** | done        | `[HG-GRAPH-P0-CLOSE_checklist](../../harness/invokes/by-task/graph-yaml-p0-00-main/HG-GRAPH-P0-CLOSE_checklist_v1_zh.md)` 全勾 · 人签后 `git mv` done |


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


| 字段                    | 值                                                                                                                                                                                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **actual_last_round** | `R3`                                                                                                                                                                                                                                                        |
| **early_stop**        | `yes`                                                                                                                                                                                                                                                       |
| **early_stop_reason** | `R3 已收敛：方案推荐（YAML→MD 单向）明确；CI 仅追加 diff 校验不改动现有 workflow；failure_paths F1/F2/F3 均可操作；P0 与 _manifest 不联动；R4/R5 为执行期命令占位与远期规划，可在 22 审查中书面确认，无需额外思考轮`                                                                                                           |
| **residual_risks**    | `1) graph.json 中 00_main 节点无 kind 字段（P2-0 遗留），YAML schema 需决定是否补 kind 或允踱缺失；2) 锚点仅在 Q→E、U1→AUTH、U2→AUTH、U2→EV_TYPES 四条边存在，YAML→MD 生成时锚点渲染格式须与 99_mermaid_protocol.md 对齐；3) P1 迁移 10_flow_rag 时其 .ai.md 含 Mermaid + AUTO 块，YAML schema 需扩展以支持子图引用与 AUTO 注入块` |


### R0 · 读 task / QNA / 非范围

- **范围清晰**：P0 仅限 00_main，目标为 YAML 源 → .md 生成 + diff 校验，不删 .ai.md，不接 cyning-harness。
- **非范围清晰**：不迁移 10_flow_* 共 6 张、不改前端仓、不回灌 harness 产品模板、不做 trace.json / .version/ History。
- **缺口清单**：
  1. YAML schema 未在 task 中定义，须 30 帽参照 QNA §2 示例 + graph_v2_schema 节点/边结构起草；
  2. `scripts/graph_yaml_compile.py` 仅为建议路径，未确认放 `scripts/` 还是 `tools/`；
  3. 00_main.ai.md 中 `AUTO:ENDPOINTS_AND_ANCHORS` 块为 manifest 自动生成，YAML→MD 是否复刻该块或改为引用 _manifest.json 待决策。

### R1 · 代码与图谱事实（00_main.ai.md · graph.json 切片）

- **00_main 节点**：graph.json 中 26 个节点（graph_id=00_main），无 `kind` 字段（P2-0 遗留），含 Q/E/U1/U2/C1/CR1/CR2/A1/A2/CH/CV/HL/H1/SQ/RAG/T2S/FTS/RPC/EV_TYPES/AUTH 等业务节点 + RAG_DOC/T2S_DOC/FTS_DOC/RPC_DOC/OBS_DOC/E2E_DOC 等文档引用节点。
- **00_main 边**：36 条，类型仅 `depends_on`（32）与 `branches`（4）；`branches` 集中在 U1/U2 → RAG/T2S（::branches 标记）。
- **锚点**：仅 4 条边带 anchors（Q→E、U1→AUTH、U2→AUTH、U2→EV_TYPES），其余 32 条边 anchors=[]。
- **现有 CI**：`.github/workflows/tech-graph.yml` → `bash scripts/verify-tech-graph.sh` 已含 manifest_check / export --check / drift / equivalence / token_estimate；**无** YAML 相关步骤。P0 须追加 `graph_yaml` 校验步骤（或 pre-commit），但**不改动**现有 `verify-tech-graph.sh` 核心链路（避免破坏其他 graph 校验）。
- **00_main.ai.md**：含 Mermaid 图 + AUTO:ENDPOINTS_AND_ANCHORS 自动生成块（来自 _manifest.json）+ 子图链接列表。
- **00_main.md**：人类友好版，Mermaid 更简洁，无 AUTO 块，无 AI 协议标记。

### R2 · 方案对比（YAML schema · 生成 MD 结构 · 脚本语言）


| 方案                                                | 描述                                                                                            | 推荐     | 弃选/保留理由                                                                                                                     |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------- |
| **方案 1**：YAML 源 → Python 生成 .md + 校验 graph.json   | 编辑 `00_main.graph.yaml` → 脚本生成 `00_main.md`（含 Mermaid + 结构化表格）→ 同时校验与 graph.json 00_main 切片一致 | **推荐** | 最小 diff：只新增 YAML 源 + 生成脚本 + 校验；保留现有 graph.json 机器轨不动；与 QNA §2 工作流一致；人类读 .md，AI 未来读 YAML                                     |
| **方案 2**：YAML 源 → 直接 emit graph.json 子集 + 再生成 .md | YAML 同时作为 graph.json 的 00_main 子集来源                                                           | 弃选     | P0 目标不是替换 graph.json 导出器（现有 `tech_graph_graph_export.py` 已负责 .ai.md → graph.json）；改 graph.json 来源会触发现有 CI 等价校验大面积变动，超 P0 范围 |
| **方案 3**：JSON 源替代 YAML                            | 手写 JSON 作为 00_main 编辑源                                                                        | 弃选     | JSON 无注释、手写拓扑差、与 QNA 推荐方向矛盾；仅适合聚合（_manifest.json）                                                                           |


**结论**：方案 1（YAML → .md + diff 校验）为 P0 唯一可行路径；脚本语言 Python（与现有 tools/ 一致）。

### R3 · 边界 / CI / failure_paths / 与 manifest 关系

- **F1 `fp-yaml-parse`**：可操作 —— PyYAML 解析异常 catch → exit 1 + 行号，CI 日志可见。
- **F2 `fp-graph-diff`**：可操作 —— 脚本比对 YAML 生成的节点/边集合与 graph.json 00_main 切片，diff 输出节点/边清单，exit 1。
- **F3 `fp-gate-draft`**：已滿足 —— HG-TASK-DRAFT approved，HG-AUDIT-R1 pending 阻塞 30。
- **pre-commit vs CI**：建议 **CI only**（`.github/workflows/tech-graph.yml` 追加 job 或 `verify-tech-graph.sh` 追加步骤）；pre-commit 可选（本地开发便利），但非 P0 必须。
- **与 _manifest 关系**：P0 **不联动** —— _manifest.json 仍由现有机制维护；YAML 中不嵌入 manifest 数据；00_main.md 中 AUTO:ENDPOINTS_AND_ANCHORS 块在 P0 可保留现状（由现有工具生成），或改为静态引用 _manifest.json（30 帽决策）。
- **与 graph.json 关系**：YAML 为**新增源**，graph.json 仍为**机器真值**；P0 只校验一致性，不反向写入。

### R4 · pytest / 校验命令 / PR 策略

（跳过 · 见思考轮控制）

“ R4 为执行期命令占位，核心命令已在 task 验收标准中列出：

- `python scripts/graph_yaml_compile.py --check`（或 `tools/` 等价路径）
- `pytest tests -m "not intent_eval and not intent_benchmark"`（含 ≥1 转换/校验用例）
- 现有 graph CI：`bash scripts/verify-tech-graph.sh`
- 追加：`python scripts/graph_yaml_compile.py` 生成 `00_main.md` 后，可人工 diff 审阅

### R5 · 图谱增量 · P1 路线图 · 关账条件

（跳过 · 见思考轮控制）

“ **P1 迁移目标**：`10_flow_rag`（RAG 子流程最复杂，含 Mermaid + AUTO 块 + 子图引用）；其次 `11_flow_text2sql`、`12_flow_fts`、`13_flow_supabase_rpc`、`14_runtime_observability`、`15_e2e_boundary`。
“ **回灌 cyning-harness**：P0 验收后、HG-GRAPH-P0-SIGNOFF 签后，另起 Epic（非本 task）；v1.1+ 时评估 harness 模板是否吸收 YAML→MD 模式。
“ **关账条件**：与 HG-GRAPH-P0-CLOSE_checklist_v1_zh.md §2 对齐 —— 00_main.graph.yaml 落盘、生成 00_main.md、diff 校验通过、pytest ≥1 用例、invoke 链完整、未删 .ai.md、未引入 .cyning-harness/。

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


| 路径                                                    | 说明                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------- |
| `docs/_tech_graph/00_main.graph.yaml`                 | P0 编辑源（26 节点 / 36 边，对齐 graph_v2_schema + 99_mermaid_protocol） |
| `scripts/graph_yaml_compile.py`                       | YAML→MD 转换器 + --check diff 校验                                 |
| `docs/_tech_graph/00_main.md`                         | 人类可读版（Mermaid + 结构化表格 + frontmatter）                          |
| `tests/test_graph_yaml_compile.py`                    | 8 条 pytest 用例（red→green，覆盖 F1/F2 + R2 锚点格式）                   |
| `docs/harness/invokes/by-task/graph-yaml-p0-00-main/` | invoke 链（含本 30 执行 invoke）                                     |


**P0 决策备忘**：

- `00_main.md` 不嵌入 `AUTO:ENDPOINTS_AND_ANCHORS` 块（保持人类友好）；`_manifest.json` 仍由现有工具维护
- `00_main.ai.md` 保留并标记 `@deprecated · 源迁 YAML`，P0 不删除
- 脚本路径确认放 `scripts/`（与 `scripts/verify-tech-graph.sh` 同目录）

### 自检结论（执行者）


| #   | 命令                                                           | 退出码 | 摘要                                                                                        |
| --- | ------------------------------------------------------------ | --- | ----------------------------------------------------------------------------------------- |
| 1   | `pytest tests/test_graph_yaml_compile.py -v`                 | 0   | 8 passed（YAML 存在/解析、节点/边/锚点匹配、--check 模式、锚点格式）                                            |
| 2   | `python scripts/graph_yaml_compile.py --check`               | 0   | YAML 与 graph.json 00_main 切片一致                                                            |
| 3   | `pytest tests -m "not intent_eval and not intent_benchmark"` | 0   | 360 passed, 1 skipped, 2 deselected                                                       |
| 4   | `bash scripts/verify-tech-graph.sh`                          | 1   | manifest/test_manifest/harness gate 均 OK；exit 1 因其他 task 的 human_gate pending（非本 task 阻塞） |


**40 帽独立复跑确认（2026-06-16）**：

- 命令 1–3 全部通过，退出码与 30 帽记录一致
- 交付物核对全部通过（见下表）
- 无新增失败项，无需打回 30

**OpenSpec × TDD 三维自检**：

- Completeness：F1/F2/F3 均有测例或命令证据（YAML 解析失败、graph diff 失败、脚本 --check 模式）
- Correctness：锚点格式匹配 99_mermaid_protocol.md §3（// → path#line 或 // → path::symbol）
- Coherence：P0 不嵌入 AUTO 块，与 task 非范围一致；未删 .ai.md，未引入 cyning-harness

**残余风险处理**：

- R1-kind 缺失：YAML schema 允许 kind 缺失（graph.json 00_main 节点无 kind 字段），diff 校验兼容
- R2-锚点渲染：4 条边带 anchors，pytest 中断言锚点注释格式符合 protocol
- R3-AUTO 块策略：00_main.md 不嵌入 AUTO 块，已在生成 MD 中书面记录；_manifest.json 仍由现有工具维护

### KPI（00）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: 88% · **状态**: pass · **帽**: 10→22→30→40→50→CLOSE


| hat_code | round | agent_mode    | D1  | D2  | D3  | D4  | D5  | judgment_notes                                                            |
| -------- | ----- | ------------- | --- | --- | --- | --- | --- | ------------------------------------------------------------------------- |
| 10       | R0–R3 | task_subagent | 100 | 100 | 100 | 100 | —   | early_stop=yes 理由充分；A/B Prompt 全文输出                                       |
| 22       | R1    | task_subagent | 100 | 100 | 100 | 100 | —   | 零阻塞 PASS；残余风险 3 项书面钉住                                                     |
| 30       | R1    | task_subagent | 100 | 60  | 100 | 100 | —   | D2 warn：00_main.graph.yaml 头部注释误将新源标为「历史 AI 协议版」，00 发现并修正（commit d064915） |
| 40       | R1    | task_subagent | 100 | 100 | 100 | 100 | —   | 独立复跑 3 条命令全部通过                                                            |
| 50       | close | task_subagent | 100 | 100 | 100 | 100 | 100 | 独立复跑 + 7 项验收标准全 pass，建议 CLOSE                                             |
| 00       | CLOSE | main_chat     | 100 | 100 | 100 | 100 | 100 | gate 检查合规，未代签；分仓 commit 可追溯                                               |


**计算**：D1=100, D2=min(100,100,60,100,100,100)=60, D3=100, D4=100, D5=100 → 100×20% + 60×30% + 100×15% + 100×15% + 100×20% = 88%

---

## 修订记录


| 日期         | 说明                                                |
| ---------- | ------------------------------------------------- |
| 2026-06-16 | 初稿 · 00→10→50→人签 checklist 帽序 · 不接 cyning-harness |


