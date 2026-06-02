# Ink 后端技术图谱全能力盘点与实施细节审计

| 项 | 内容 |
| --- | --- |
| **版本** | v1.4 |
| **日期** | 2026-06-02 |
| **范围** | `ai-ink-brain-api-python/`（只读审计 + 本地可运行检查） |
| **触发** | `ai_coding_governance/narrative/prompts/PROMPT_后端Agent_技术图谱全能力审计_v1_zh.md` |
| **关联** | [续卷 GUIDE](../../../../ai_coding_governance/narrative/GUIDE_续卷编写_Ink后端真值对照_v1_zh.md) · [QA 技术图谱](../../../../ai_coding_governance/narrative/qa/QA_技术图谱_ai_md_graph_json与子图物化_v1_zh.md) |
| **约束** | 默认未改 `docs/_tech_graph/`、`tools/`、workflow；审计中误触 `render_ai` 已 `git checkout` 还原 |

**说明**：本地存在 sibling 仓 `../ai-ink-brain`，`tech_graph_contract_check.py` 可完整运行；GitHub 分支保护 API 调用超时，Required 检查结论以仓内 workflow + GUIDE / `HARNESS_V2_P0_ACCEPTANCE` 为准。

---

## A. 能力矩阵

| 能力域 | 具体能力 | 实现位置（文件/函数/workflow step） | 触发方式 | 人 vs 机器分工 | 成熟度 |
| --- | --- | --- | --- | --- | --- |
| 源稿维护 | 双轨 `.md` + `.ai.md`（flowchart 语义等价） | `docs/_tech_graph/*.md` / `*.ai.md`；规约 `99_mermaid_protocol.md`；规则 `.cursor/rules/10-tech-graph.mdc` | 本地 / Agent 约定（改代码后同 PR 改图） | **人/Agent 写** `.ai.md` 拓扑 + 锚点；**人读** `.md` 审 diff | **已上线** |
| 源稿维护 | Struct / Env / 规约（非 graph.json 轨） | `01_struct.md`（classDiagram）、`99_spec.md`、`02_version.md` | 本地 + 任务单 `@` 引用 | **人/Agent 写**；机器不导出为 graph.json | **已上线** |
| 导出 | `.ai.md` → `graph.json`（graph_v2） | `tools/tech_graph_graph_export.py`（`main()`）；schema `tools/tech_graph_graph_v2_schema.py`；CI step `Tech graph graph.json drift check` | PR CI + 本地 `python tools/tech_graph_graph_export.py --check` | **Agent/人改** `.ai.md` → **机器 export/check**；**禁止手改** `graph.json`（`99_spec.md` §Wiki桥接） | **已上线** |
| 等价检查 | 人读轨（`.ai.md` 参考图）vs 已提交 `graph.json` | `tools/tech_graph_graph_equivalence_check.py`（锚点 ≥95%、边 label ≥90%）；CI step `Tech graph graph_v2 equivalence check` | PR CI | **机器查**；不等价时 **人/Agent 修** `.ai.md` 再 export | **已上线** |
| 入口清单 | 端点 / RPC / 表 / env / anchors 真值 | `docs/_tech_graph/_manifest.json`（`schema_version: tech_graph_manifest_v1`）；校验 `tools/tech_graph_manifest_check.py::_run_backend_check` | PR CI step `Tech Graph manifest check` | **人/Agent 改** manifest（路由变更时）；**机器** 对 `api/index.py`、`api/*.py`、`supabase/sql/*.sql` 扫真值 | **已上线** |
| 契约清单 | Unified SSE/events 跨端契约 | `docs/_tech_graph/_contract_manifest.json`；`tools/tech_graph_contract_check.py`（扫 `api/unified_chat.py`、`agent.py`、`tools.py` + 前端 TS） | 独立 workflow `tech-graph-contract.yml` job `contract_check` | **人/Agent 改** contract JSON + 后端 emit；**机器** 校验 backend ⊇ contract、frontend ⊆ contract | **已上线** |
| 测试映射 | ERR ↔ pytest 映射（Phase B） | `docs/_tech_graph/_test_manifest.json`（12 entries，`freeze_id: GOV-L2-ANCHOR-TEST-MANIFEST@2026-05-27`）；`tools/tech_graph_test_manifest_check.py` | PR CI step `Tech Graph test manifest check (Phase B)` | **人/Agent 写** 条目 + task `failure_paths`；**机器** 校验 JSON/glob | **已上线** |
| 测试映射 | failure_paths 双向对照（Phase C） | 同上 + `--check-failure-paths` | PR CI step `Tech Graph test manifest check (Phase C · failure paths)` | **人写** task 表；**机器** 对照 manifest | **已上线** |
| 子图查询 | downstream / upstream / neighbors / has-path / describe-impact | `tools/tech_graph_graph_query.py`（`GraphQueryStore`、BFS） | **本地 / Agent 约定**（非 CI） | **Agent 读** 子图 JSON；**人** 维护源 `.ai.md` | **已上线** |
| 物化/上下文 | Token A/B 粗估（闸口附录，非 KPI） | `tools/tech_graph_token_estimate.py`；CI step `Tech graph token estimate (Gate A appendix)` | PR CI（采集 JSON） | **机器算**；**人** 解读（`heuristic_tokens = chars//4`，非 tiktoken） | **已上线**（2026-06-02：A≈15235、B≈5115 token 粗估，比≈0.34） |
| 物化/上下文 | jsonPKmermaid 实验臂（CTX_QUERY / CTX_V2_QUERY 等） | `docs/diary/jsonPKmermaid/`；规则 `10-tech-graph.mdc` §jsonPKmermaid | **仅 task 显式引用** | **实验结论**；默认 **graph_query** 子图（QA v1.2 · 2026-05-28） | **实验** |
| 漂移检测 | **文档字面量**覆盖（端点/RPC/表/关键 env 子串） | `tools/tech_graph_drift_check.py::main()`；CI step `Tech graph docs literal drift check` | PR CI + 本地 | **人/Agent** 补 `_tech_graph/*.md` 字面量；**机器 fail** | **已上线**（方案 A · commit `da4e7b7` · 2026-06-02） |
| 漂移检测 | **graph.json 与 export 一致性** | `tech_graph_graph_export.py --check`（exit 4 = 语义不一致） | PR CI | **机器拦**；**人/Agent** 改 `.ai.md` + `export` | **已上线** |
| 自动片段 | manifest → `00_main.ai.md` AUTO 区块 | `tools/tech_graph_render_ai.py`（`AUTO:ENDPOINTS_AND_ANCHORS`）；`manifest_check` 通过时 TIP 提示 | 本地（**无** `--help`，无 argparse） | **机器 render** 端点/锚点列表；**人/Agent** 仍手写拓扑 Mermaid | **已上线**（局部） |
| Agent 改图 | 同 PR 改图纪律 | `.cursor/rules/10-tech-graph.mdc`、`20-tech-graph-update.mdc`；`docs/tasks/templates/TASK_TEMPLATE.md` | Agent 约定 + Harness 任务单 | **Agent 起草** `.ai.md`/manifest → **人审** diff → **机器** CI | **已上线**（纪律 + 门禁；非无人审查全仓） |
| Harness 门禁 | 执行产物 human_gate | `tools/harness_human_gate_check.py --pr-diff`；CI step `Harness human_gate check` | PR CI | **人** 改 `approved`；**机器** 拦 pending | **已上线** |
| Harness 门禁 | 变更 task 单 schema 校验 | `tools/harness_task_validate.py`；workflow `task_validate` job（仅 `docs/tasks/` diff 时） | PR CI（条件触发） | **人/Agent 写** task；**机器** validate | **已上线** |
| Coding Wiki 桥接 | L2 `graph_nodes` 种子 → query | `docs/coding_wiki/syntheses/query-rewrite-observability.md`；`tools/coding_wiki_graph_nodes_lint.py`（`99_spec.md`） | 本地 / Wiki ingest task | **人/Agent** 写 frontmatter；影响面仍靠 **graph_query** | **试点**（T4 Pilot 2026-05-27） |

---

## B. 数据流

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ 维护轨（人 / Agent 同 PR 改）                                              │
│  *.ai.md（拓扑+锚点）  *.md（人读）  _manifest.json  _contract_manifest.json │
│  _test_manifest.json  01_struct.md / 99_spec.md                          │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 render_ai.py              graph_export.py         manifest_check.py
 (仅 00_main AUTO 块)       → graph.json            test_manifest_check.py
        │                       │                  contract_check.py
        │                       ▼                       │
        │              equivalence_check.py             │
        │              token_estimate.py                │
        ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PR CI: tech-graph.yml (manifest_check job) + tech-graph-contract.yml      │
│ 拦：manifest / test_manifest / export --check / drift_check / equivalence │
│     / token / human_gate / (条件) task_validate                           │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ merge 后
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Agent 消费（默认，10-tech-graph.mdc）                                     │
│  graph_query.py downstream|upstream|neighbors <node_id> <depth>          │
│  → 子图 JSON + anchors；按需 _manifest / _contract 切片                    │
│  禁止：整包 graph.json / graph_v1 整图 / 默认 jsonPKmermaid 实验 fixtures   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## C. CI 与合并门禁

### C.1 workflow 对照

| Workflow 文件 | GitHub name | 主要 job / step |
| --- | --- | --- |
| `.github/workflows/pytest.yml` | `pytest` | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| `.github/workflows/tech-graph.yml` | `tech-graph` | `manifest_check`：7 步 Python 检查 + `harness_human_gate_check`；`task_validate`：条件 task 校验 |
| `.github/workflows/tech-graph-contract.yml` | `tech-graph-contract` | checkout 后端 + 前端 `production` → `contract_check` |
| `.github/workflows/verify-fast.yml` | `verify-fast` | 与 pytest 同命令的重复 job |

### C.2 `tech-graph.yml` step 明细（`manifest_check` job）

| Step 名 | 本地等价命令 |
| --- | --- |
| Tech Graph manifest check | `python tools/tech_graph_manifest_check.py` |
| Tech Graph test manifest check (Phase B) | `python tools/tech_graph_test_manifest_check.py` |
| Tech Graph test manifest check (Phase C · failure paths) | `python tools/tech_graph_test_manifest_check.py --check-failure-paths` |
| Harness human_gate check (PR execution artifacts) | `python tools/harness_human_gate_check.py --pr-diff --base origin/main` |
| Tech graph graph.json drift check (graph_v2 export) | `python tools/tech_graph_graph_export.py --check` |
| Tech graph docs literal drift check | `python tools/tech_graph_drift_check.py` |
| Tech graph graph_v2 equivalence check | `python tools/tech_graph_graph_equivalence_check.py` |
| Tech graph token estimate (Gate A appendix) | `python tools/tech_graph_token_estimate.py --json` |

### C.3 Required 状态（仓内文档真值）

| 检查 | 是否合并必绿 | 依据 |
| --- | --- | --- |
| `pytest` | **是** | `AGENTS.md` §8 · GUIDE §3.4 |
| `tech-graph` | **是**（与 pytest **并列**） | GUIDE §3.4 · `task_governance_l2_manifest_ci` HG-CI-WORKFLOW |
| `tech-graph-contract` | **是** | 独立 workflow，PR 同触发 |
| `verify-fast` | **否** | `HARNESS_V2_P0_ACCEPTANCE.md` §6.1 · `VERIFICATION_CI_PATTERN.md` |

> GitHub 分支保护 Required 勾选无法远程确认（2026-06-02 API 超时）；上表为仓内规范真值。

### C.4 `tech-graph-contract` 校验范围

| 侧 | 路径 / 字段 |
| --- | --- |
| **契约真值** | `docs/_tech_graph/_contract_manifest.json` |
| **后端真值扫描** | `api/unified_chat.py`、`api/agent.py`、`api/tools.py` |
| **前端消费** | `../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx` |
| **Next BFF** | `../ai-ink-brain/app/api/py/unified/chat/stream/route.ts` |
| **规则** | backend **必须覆盖** contract 声明；frontend **读取键** ⊆ contract |

---

## D. 「试点 → Agent 模仿推广」可落地性

### D.1 是否存在金样板？

**有，且多层：**

| 类型 | 证据 |
| --- | --- |
| done task | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md`；`task_tech_graph_p4_ci_guardrail_v1.md` 等 P0–P7；`task_05_query_rewrite_observability.md` |
| Wiki L2 Pilot | `docs/coding_wiki/syntheses/query-rewrite-observability.md`（`graph_nodes: C1/RAG/...`） |
| Harness invoke | `docs/harness/invokes/by-task/gov-l2-manifest-ci/` |
| 对内 FAQ | `ai_coding_governance/narrative/qa/QA_技术图谱_ai_md_graph_json与子图物化_v1_zh.md` |

**缺**：仓内未索引「单一示例 PR URL」；few-shot 靠 task + invoke + diary。

### D.2 改 `api/index.py` 路由时，机器是否强制同步？

| 产物 | CI 强制 | 机制 |
| --- | --- | --- |
| `_manifest.json` | **是** | `manifest_check` |
| `00_main.ai.md` AUTO 块 | **否**（TIP） | 通过后提示 `render_ai.py` |
| 流程 `.ai.md` Mermaid | **否** | 无路由→节点自动映射 |
| `_contract_manifest.json` | **仅 Unified/SSE** | 普通路由不触发 |
| `graph.json` | **间接是** | `.ai.md` 已改未 export → `export --check` 失败 |

### D.3 Agent 自动改 `.ai.md` 并 export？

| 层 | 实况 |
| --- | --- |
| 脚本 | `graph_export.py`、`render_ai.py`（局部）、`graph_query.py` 已存在 |
| Rules | `10-tech-graph.mdc`、`20-tech-graph-update.mdc` |
| Harness | `TASK_TEMPLATE.md` 关联图谱；**无** `auto_export_graph` 字段 |
| CI | **不会**替 Agent export 写回 |
| **结论** | **Agent 起草 + 人审 + 机器查** |

### D.4 `graph.json` 手改会被 CI 拒绝吗？典型修复流程

**会。** `export --check` exit **4** = 语义不一致。

1. 定位受影响 `docs/_tech_graph/*.ai.md`
2. 修改 `.ai.md`（必要时同步 `.md`）
3. 若动端点：更新 `_manifest.json` → `python tools/tech_graph_render_ai.py`
4. `python tools/tech_graph_graph_export.py`
5. 本地跑：`manifest_check` → `test_manifest_check --check-failure-paths` → `export --check` → `equivalence_check`

### D.5 维护成本

| 模式 | 本仓实况 |
| --- | --- |
| 一次性建链 | P0–P7 + L2 manifest/test_manifest + graph_v2 + contract CI |
| 按 PR 摊薄 | 仅改触及链路；`render_ai` 只维护 `00_main` 端点块 |
| 非全仓手绘 | 134 nodes / 7 graphs 已导出 |

---

## E. 与公众稿 / GUIDE 快照差异

**GUIDE 快照日期**：2026-05-27 → **相对 2026-06-02 已部分过期**。

| 声明（卷二/卷五/GUIDE §3.2） | 仓内实况 | 建议 |
| --- | --- | --- |
| GUIDE §3.2：`tech-graph` step 列表 | 缺 `--check-failure-paths`、`human_gate`、`task_validate` | **升 GUIDE 快照** |
| 「manifest + graph_v2 drift + equivalence」 | CI「drift」= **`export --check`**，非 `drift_check.py` | 公众稿写清两种 drift |
| `99_spec` P0_3 drift_check done + 链 workflow | **已闭合**（方案 A · `da4e7b7`） | GUIDE §3.2 补 drift_check step · 升快照日期 |
| 卷二 §8.6 阶段 2 | **已落地** | 可写 Ink 后端达阶段 2 |
| 卷五 §24.2 增量图谱 CI 未承诺 | 仍全量 export --check | **维持** |
| 卷五 §24.2 人改图+机器查 | 一致；文档字面量 drift 未 CI | 对内补缺口 |

---

## F. 缺口清单

### P0

本次审计未发现影响「合并必绿」的 P0（manifest / export / equivalence / test_manifest / contract 本地均 exit 0）。

### P1

| ID | 缺口 | 状态 |
| --- | --- | --- |
| ~~P1-1~~ | ~~`drift_check.py` 未进 CI~~ | **已关闭** · 方案 A · §M |
| P1-2 | 路由变更不强制同步 Mermaid 子图 |  open |
| P1-3 | `render_ai.py` 无 `--dry-run`/`--help`，误跑即写文件 | open |
| P1-4 | 无单一金样板 PR 索引 | open |

### P2

| ID | 缺口 |
| --- | --- |
| P2-1 | `docs/_tech_graph/README.md` 缺失 |
| P2-2 | `PROJECT_CONFIG` §E 图谱 CI 描述偏简 |
| P2-3 | `20-tech-graph-update.mdc` 与 `10-tech-graph.mdc` query 优先略冲突 |

---

## G. 最小可演示命令

```bash
cd ai-ink-brain-api-python

# 1) 入口清单 + 代码真值
python tools/tech_graph_manifest_check.py

# 2) graph.json 与 .ai.md 一致 + 叙述层字面量（方案 A）
python tools/tech_graph_graph_export.py --check && python tools/tech_graph_drift_check.py && python tools/tech_graph_graph_equivalence_check.py

# 3) Agent 默认读法：RAG Chat 节点 2 跳子图
python tools/tech_graph_graph_query.py downstream C1 2
```

**可选（有 sibling 前端）**：`python tools/tech_graph_contract_check.py`

---

## H. 本地命令执行记录

| 命令 | 退出码 | 摘要 |
| --- | ---: | --- |
| `tech_graph_manifest_check.py` | 0 | OK + TIP render_ai |
| `tech_graph_test_manifest_check.py` | 0 | 12 entries |
| `... --check-failure-paths` | 0 | Phase C OK |
| `tech_graph_graph_export.py --check` | 0 | 一致 |
| `tech_graph_graph_equivalence_check.py` | 0 | 通过 |
| `tech_graph_token_estimate.py --json` | 0 | A/B 比 ~0.34 |
| `tech_graph_graph_query.py --help` | 0 | 5 种 op |
| `tech_graph_render_ai.py --help` | 0 | 无 argparse；误执行会写文件 |
| `tech_graph_drift_check.py` | 0 | OK（v1.3 还债后；审计初扫时为 exit 1） |
| `tech_graph_contract_check.py` | 0 | 跨仓 OK |

**graph.json 元数据**：`schema_version=graph_v2`，`freeze_id=TECH_GRAPH_S2_FREEZE_20260519_V2_3`，`generated_at=2026-05-18T07:07:16Z`，7 graphs，134 nodes，185 edges。

---

## I. tools/tech_graph_*.py 脚本摘要

| 脚本 | 用途 | CLI / 退出码 |
| --- | --- | --- |
| `tech_graph_manifest_check.py` | manifest vs 代码/SQL 真值 | 默认后端；`--repo frontend --repo-root`；0 OK / 1 drift / 2 错误 |
| `tech_graph_test_manifest_check.py` | `_test_manifest.json` 校验 | `--check-failure-paths` · `--strict` |
| `tech_graph_graph_export.py` | `.ai.md` → `graph.json` | `--check`；0 OK / 2 FP-1·4 / 3·4 FP-2 |
| `tech_graph_graph_equivalence_check.py` | 参考 v2 vs 已提交 | 0 / 2 FP-1 / 3 FP-3 / 5 FP-5 v1 |
| `tech_graph_graph_query.py` | 子图 BFS 查询 | `downstream\|upstream\|neighbors\|has-path\|describe-impact`；4 FP-4 / 5 FP-5 |
| `tech_graph_contract_check.py` | 跨端 SSE 契约 | 0 OK / 1 不一致 / 2 错误 |
| `tech_graph_drift_check.py` | docs 字面量覆盖 | 0 OK / 1 缺子串 / 2 缺 index.py |
| `tech_graph_render_ai.py` | manifest → 00_main AUTO 块 | 无 CLI；exit 0；**直接写盘** |
| `tech_graph_token_estimate.py` | A/B token 粗估 | `--json` |
| `tech_graph_graph_v2_schema.py` | graph_v2 schema 校验 | 库模块 |
| `tech_graph_graph_v2_reference.py` | 等价检查参考图构建 | 库模块 |
| `tech_graph_ci_stderr.py` | CI 失败格式化 | 库模块 |
| `tech_graph_contract_demo.py` | 契约演示 | 非 CI |

---

## J. 总判断

| 模式 | 状态 |
| --- | --- |
| **人写 + 机器查**（manifest、export、equivalence、test_manifest、contract、human_gate） | **已上线** |
| **Agent 起草 + 人审 + 机器查**（同 PR 改图；CI 不自动改图） | **可落地** |
| **半自动全仓改图** | **未成熟**（与卷五 §24.2 一致） |

**对齐公众稿**：规矩（协议）+ 试点（L2 Wiki/query-rewrite）+ 日常（PR CI 查漂移）+ 半自动（Agent 同 PR 改图、人审）——**与仓内真值基本一致**；P1-1 叙述轨 drift 已闭合（**§M**）；仍须升 GUIDE §3.2 快照。 AST 锚点升级见 **§L**。


---

## K. 「Agent 起草 + 人审 + 机器查」可落地方案与全仓半自动演进

> 本节承接 **§J 总判断**，展开可操作定义、未成熟原因与改进路线图（2026-06-02 对话产出）。

### K.1 角色分工

| 环节 | 执行者 | 做什么 | 不做什么 |
| --- | --- | --- | --- |
| **起草** | Agent（`.cursor/rules/10-tech-graph.mdc`、`20-tech-graph-update.mdc`） | 改代码前 `graph_query` 取子图；改代码后同步 **触及** 的 `.ai.md`、`_manifest.json`、（若涉 SSE）`_contract_manifest.json`；跑 export | 不手改 `graph.json`；不默认整包灌 `graph.json` |
| **人审** | 维护者 | 看 PR diff：Mermaid 拓扑、manifest 条目、Harness `human_gate` 是否 `approved` | 不跳过「同 PR 改图」；不自批 human_gate |
| **机器查** | CI `tech-graph` + `tech-graph-contract` | manifest / test_manifest / export `--check` / equivalence / token 附录 / human_gate | **不会**替 Agent 写回 `graph.json`；**不会**自动改 `10~15_flow_*.ai.md` |

**一句话**：Agent 是 **同 PR 内的图谱 co-author**；人是 **语义与签收 gate**；机器是 **真值与导出一致性 gate**。

### K.2 单条需求标准作业流（六步）

以「改 Unified Chat / 新增端点 / 改 RAG 链路」为例：

```text
① 读（Agent）
   task 单 → graph_query downstream <入口节点> 2
          → 按需 _manifest / _contract 切片
          → 01_struct / 99_spec（若动表或 env）

② 改代码 + 同步维护轨（Agent 起草）
   api/*.py
   + 对应 *.ai.md（拓扑/锚点）
   + _manifest.json（端点/RPC/表/env/anchors）
   + _contract_manifest.json（仅 SSE/事件链变更时）
   + 可选：task failure_paths ↔ _test_manifest 新条目

③ 再生机器轨（Agent 或人本地）
   python tools/tech_graph_render_ai.py          # 仅 00_main 端点/锚点 AUTO 块
   python tools/tech_graph_graph_export.py       # → graph.json

④ 本地预检（Agent）
   manifest_check → test_manifest_check [--check-failure-paths]
   → export --check → drift_check → equivalence_check
   →（有前端 sibling）contract_check

⑤ 人审（PR）
   看 .ai.md / manifest / graph.json 导出 diff
   Harness reviews / human_gate approved

⑥ 机器查（CI）
   tech-graph + tech-graph-contract + pytest 并列必绿
```

此即公众稿「**同一 PR 里 Agent 按范本改图，人审 diff**」在后端的 **可操作定义**。

### K.3 范本 / few-shot 来源

| 类型 | 路径 | 用途 |
| --- | --- | --- |
| 规则范本 | `.cursor/rules/10-tech-graph.mdc`、`20-tech-graph-update.mdc` | Agent 读序、禁止项、改后必 export |
| 任务范本 | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md`、P0–P7 tech_graph 系列 | manifest + CI 闭环 |
| Wiki 试点 | `docs/coding_wiki/syntheses/query-rewrite-observability.md` | `graph_nodes` 种子 → query 影响面 |
| Harness invoke | `docs/harness/invokes/by-task/gov-l2-manifest-ci/` | 帽号链 + 落盘纪律 |
| 对内 FAQ | `ai_coding_governance/narrative/qa/QA_技术图谱_ai_md_graph_json与子图物化_v1_zh.md` | 双轨 / 子图 / 物化边界 |

**缺口（P1-4）**：仓内无「单一 PR 链接走完全链」索引；few-shot 靠 task + invoke 拼装。

### K.4 与「全自动化」的边界

| 已成熟 | 未成熟 |
| --- | --- |
| manifest 与代码真值 **CI 强制** | 路由变更 **不强制** 改 `10_flow_*.ai.md` 拓扑 |
| `graph.json` 手改会被 **export --check** 拦 | CI **不会**在 PR 里自动跑 export 写回 |
| `render_ai` 机械同步 **00_main 端点块** | 子流程图仍 **人工/Agent 手写** Mermaid |
| Agent 默认 **graph_query 子图** 读图 | **无**「改 index.py → 自动推断节点/边」 |

**「可落地」** = 纪律 + 脚本 + CI 门禁已齐；**≠**「Agent 开 PR 只改图就能合、人也几乎不看」。

---

### K.5 「半自动全仓改图」未成熟：原因分析

#### K.5.1 维护对象不可全机械

| 对象 | 能否全自动 | 原因 |
| --- | --- | --- |
| `_manifest.json` | **部分能** | 端点/RPC/表/env 可从代码扫；已在 `manifest_check` |
| `00_main.ai.md` AUTO 块 | **部分能** | `render_ai` 只做列表，不做拓扑 |
| `10~15_flow_*.ai.md` | **基本不能** | 业务语义、分支、失败路径须人/Agent 理解；无 AST→Mermaid 映射 |
| `.md` 人读轨 | **不能** | 与 `.ai.md` 语义等价但格式不同，无双向编译器 |
| `01_struct` / `99_spec` | **不能** | classDiagram、Env 表、规约叙述非 flowchart 导出范围 |

**结论**：「全仓改图」里只有 **清单类 + 主图端点块** 可半自动；**拓扑图是核心成本**，仍依赖 Agent/人。

#### K.5.2 CI 设计是「查」不是「改」

- `tech-graph.yml` 全是 **check**，无 export 写回 step。
- 刻意避免：CI bot 与 PR 作者争抢 `graph.json`、无审自动合图。
- 与卷五 §24.2「Agent 自动开 PR 只改图谱即可合 → 禁止双 PR 死锁」同向。

#### K.5.3 两种 drift 只拦了一种

| 工具 | 查什么 | 是否在 CI |
| --- | --- | --- |
| `export --check` | `.ai.md` 编译结果 vs 已提交 `graph.json` | **是** |
| `drift_check.py` | 代码符号是否在 `docs/_tech_graph/*.md` **字面量**出现 | **是**（方案 A · §M） |

**机器轨漂移**有门禁；**文档叙述层静默过期**仍可能漏网——公众稿「漂移降低非归零」成立。

#### K.5.4 其他制约

| 因素 | 说明 |
| --- | --- |
| Agent 读写未闭环 | 读：`graph_query` 成熟；写：靠 rule/task，无 `graph_touch_list` / `auto_export` 等 Harness 字段 |
| jsonPKmermaid 实验轨 | `docs/diary/jsonPKmermaid/` 非必读、非 CI，不能当生产 autopilot |
| 跨仓叠加 | 后端 + 前端各自 `_tech_graph` + `_contract_manifest` 双 checkout |
| 渐进策略 | 卷二 §8.6：**PR 触及链路时顺手改图**，非每 PR 扫 134 nodes |

#### K.5.5 与公众稿对齐

| 公众稿说法 | 仓内实况 |
| --- | --- |
| 半自动：Agent 同 PR 改图，人审 | **可落地**（K.2） |
| 半自动：无人审查自动改全仓图已成熟 | **不可宣称** |
| 增量图谱 CI 未作公众承诺 | **属实**——仍全量 `export --check` |
| 维护成本 10%～15%，>20% 应减项 | 全仓 autopilot 会推高 touch 面 |

---

### K.6 未来落地改进方向

按 **投入 / 风险 / 对「半自动」贡献** 排序；**非**承诺时间表。

#### K.6.1 P1：补齐「最后一公里」（低投入、高可信）

| 方向 | 做什么 | 解决什么 |
| --- | --- | --- |
| ~~drift_check 决策~~ | **已落地方案 A**（fail · §M） | — |
| render_ai 安全 | 加 `--check` / `--dry-run` / `--help` | 误跑写盘 |
| 金样板 PR 索引 | 增 `EXAMPLE_tech_graph_pr.md` 链 done task + PR 摘要 | Agent few-shot（§F P1-4） |
| rule 统一 | `20-tech-graph-update.mdc` 改前读序与 `10-tech-graph.mdc` 一致 | Agent 行为歧义（§F P2-3） |

#### K.6.2 P2：扩大可机械同步面（中投入）

| 方向 | 做什么 | 边界 |
| --- | --- | --- |
| 路由 → manifest 辅助 | diff `api/index.py`，输出 manifest patch **建议** | 不自动改 `.ai.md` 拓扑 |
| local hook | commit 前 `export --check` + `equivalence` | 仍本地，非 CI 写回 |
| task 字段 | `graph_touch` / `graph_entry_node` | Harness 可校验「声明了却没改图」 |
| test_manifest 联动 | 新 failure_path checklist 提示补 `_test_manifest` | 已有 Phase C，文档化进 invoke |

#### K.6.3 P3：子图级半自动（中高投入，仍非全仓）

| 方向 | 做什么 | 难点 |
| --- | --- | --- |
| 单 flow 模板 + LLM 补丁 | 限定 `10_flow_*.ai.md` 改分支/锚点，export + equivalence 兜底 | 需 per-flow 范本与 review 清单 |
| describe-impact 进 invoke | 30 帽前强制 `graph_query describe-impact`，落 PR 描述 | jsonPKmermaid 部分能力生产化 |
| Wiki graph_nodes lint 进 CI | `coding_wiki_graph_nodes_lint.py` 并列 | 仅 L2 syntheses |

#### K.6.4 P4：接近「半自动全仓」（高投入、需产品决策）

| 方向 | 前提 | 风险 |
| --- | --- | --- |
| 增量 export CI | 只校验 PR diff 触及的 `graphs[]` | 卷五暂未对外承诺 |
| CI bot export 写回 | 同 PR 追加 commit | 双 PR 死锁、审图责任模糊 |
| 代码→图 AST 映射 | 路由/handler/RPC 调用图 | 误报率高 |
| 前后端联合 autopilot | 统一 manifest + 双仓 workflow | 组织与版本同步复杂 |

**务实建议**：P4 不宜作近期目标；**P1 + P2 + 单链路 P3 试点** 与公众稿「一条链金样板」一致。

#### K.6.5 目标态（对内）

```text
近期目标态：
  Agent 在「task 声明的入口节点 + 触及文件」范围内起草 .ai.md/manifest/export；
  人审拓扑语义 + Harness 签收；
  CI 拦 manifest / export / equivalence / contract / test_manifest。

远期目标态（可选）：
  扩大机械同步面（清单、端点块、单 flow 补丁）+ 可选增量 export；
  仍不承诺「零人审全仓数字孪生 autopilot」。
```

### K.7 本节结论（直接回答）

| 问题 | 答案 |
| --- | --- |
| **「Agent 起草 + 人审 + 机器查」可落地方案？** | **单 PR 六步流**（K.2）+ rules + TASK_TEMPLATE + tech-graph/contract CI + Harness human_gate；金样板靠 done task + invoke + query-rewrite Wiki pilot |
| **半自动全仓改图为何未成熟？** | 拓扑不可全机械、CI 只查不改（**叙述轨 drift 已接入**）、子流程手写、实验轨未生产化、渐进策略与「全仓」冲突（K.5） |
| **改进方向？** | P1 修链 → P2 清单/任务辅助 → P3 单 flow 试点 → P4 增量 export/CI bot 仅作远期（K.6） |


---

## L. 锚点升级轨（AST）— 语义点 + 强锚点三轨模型

> 本节承接 **§K.6 改进方向**，明确 AST 在图谱体系中的定位：**升级锚点内容、提高对准率**，**不**替代 `.ai.md` 语义拓扑。对话共识：2026-06-02。

### L.1 核心理解（可否「对图谱中的点进行升级优化」）

**可以这么理解，精确表述如下：**

AST 主要升级的不是 **流程图上的业务语义节点**（如 `C1` RAG Chat、`VEC` Vector RPC），而是 **节点/边上锚点（`path::symbol`）所指向的代码内容**——相当于给图谱里的点 **加装更准、更省的「代码探头」**。

| 层次 | 是什么 | 例子 | AST 改什么 |
| --- | --- | --- | --- |
| **语义节点** | `.ai.md` 里的业务格 | `C1`、`RAG`、`FUSE` | **一般不自动生成**（人/Agent 维护拓扑与边标记） |
| **锚点（铆钉）** | `// → api/foo.py::bar` 或 `_manifest.anchors` | `unified_chat.py::rpc_execute_with_retry` | **AST 升级的对象** |

**一句话**：语义点不变（或人/Agent 改）；锚点从 **弱字符串指针** 升级为 **可校验、可切片、可漂移检测的代码索引**。

### L.2 三轨架构（在 §K 双轨之上）

```text
┌─────────────────────────────────────────────────────────┐
│ 维护轨：*.ai.md / *.md     — 语义流程（人/Agent 写）      │
│ 机器轨：graph.json         — 拓扑查询（export + CI）      │
│ 代码轨：symbol_index / slice — AST 锚点索引（脚本生成）   │
└─────────────────────────────────────────────────────────┘
         anchors (path::symbol) 是三轨的铆钉
```

**Agent 默认读法（增强版，目标态）**：

```text
task 入口节点
  → graph_query downstream N          # 仍：只看子图，不整包 graph.json
  → 收集子图 edges/nodes 上的 anchors[]
  → code_parser 裁切每个 anchor 的 ParsedChunk
  → 按需 _manifest / _contract 切片
```

与 jsonPKmermaid 实验中的 `manifest_slice` / `impact_surface` **同向**，但生产路径应 **收窄为锚点物化**，非复活整包实验 fixtures（见 `10-tech-graph.mdc` · QA v1.2）。

### L.3 升级前后对比

```text
升级前（现状）：
  图节点 C1 ──锚点字符串──► 「去看 unified_chat.py」（常退化为整文件）

升级后（AST 轨）：
  图节点 C1 ──锚点──► AST 索引
                      ├─ symbol 是否存在
                      ├─ 起止行号
                      ├─ 函数签名 + 函数体 slice
                      └─ （可选）1～2 hop 静态 callee 提示
```

**减读取量**：子图 + 3～5 个 `def` slice，而非整模块（如 `unified_chat.py` 800+ 行）。  
**提准确率**：改码/改图时锚点对准真函数，少漏 manifest、少幻觉分支。

### L.4 AST 能覆盖 vs 不能覆盖

| 信息类型 | 当前载体 | AST |
| --- | --- | --- |
| 路由 / handler / RPC / table / env | `_manifest.json`（regex） | **能**，且应比 regex 准 |
| 符号定位与行号 | `.ai.md` 锚点、`manifest.anchors` | **能** |
| 同仓静态调用（粗 call graph） | 散落代码 | **部分能** |
| 业务语义（`::branches`、`[ok]/[err]`、外部 API） | `10_flow_*.ai.md` | **不能**单靠 AST |
| 跨边界（Supabase RPC、SSE 契约） | 子流程 + `_contract_manifest` | **不能**单靠 Python AST |

**禁止方向**：AST → 全自动生成 `10_flow_*.ai.md` 或手改 `graph.json`（破坏现有 export + equivalence 链）。

### L.5 仓内可复用资产

| 已有 | AST 锚点轨如何复用 |
| --- | --- |
| `api/code_parser.py` | `ast.parse` → `ParsedChunk`（起止行、signature、body）；**直接作 slice 引擎** |
| `_manifest.json` · `anchors[]` | AST 校验存在性；PR diff → 应改清单 |
| `.ai.md` · `// → path::symbol` | 批量解析 → 驱动 slice |
| `graph_query` · `describe-impact` | 可扩展为「impact + anchor slices」一条命令 |
| `tech_graph_manifest_check.py` | Phase A：regex 逐步换 AST 抽路由/RPC（`--suggest` 不自动写） |

### L.6 分阶段落地（与 §K.6 对齐）

| 阶段 | 内容 | 收益 | 风险 |
| --- | --- | --- | --- |
| **A** | manifest 真值 AST 化（路由、`def` 配对） | manifest 准确率 ↑ | 低 |
| **B** | `tech_graph_code_slice.py`（query → anchors → ParsedChunk JSON） | **读取量 ↓** | 低 |
| **C** | 锚点存在性 / 行号漂移 CI（warn → fail） | **改图对准率 ↑** | 中（需与 `.ai.md` 注释格式对齐） |
| **D** | 轻量 `api/` call graph ↔ graph 节点交叉 **报告**（不自动改图） | 影响面更贴代码 | 中（动态调用缺失） |
| **E（不做）** | AST 生成整图 Mermaid / CI bot 写回 graph | — | 高误报、审图责任模糊 |

### L.7 与 §K「Agent 起草 + 人审 + 机器查」的关系

| 环节 | 图谱 | AST 锚点轨 |
| --- | --- | --- |
| Agent 起草 | 改 `.ai.md` 拓扑、补锚点 | 改码后 slice 验证锚点仍指向正确 `def` |
| 人审 | Mermaid / manifest diff | 可选：锚点是否仍指着真函数 |
| 机器查 | export / equivalence / manifest / **drift_check（叙述轨）** | 未来可加 **symbol** 级锚点 drift（§L Phase C，与叙述轨互补） |

**结论**：AST **增强点的落地精度**（强锚点），**不替换**语义拓扑维护；与 §K 六步流 **完全兼容**。

### L.8 本节结论

| 问题 | 答案 |
| --- | --- |
| 能否理解为「对图谱中的点升级优化」？ | **能**——更准确是 **升级锚点所绑定的代码内容**，语义节点仍人/Agent 维护 |
| 主要收益？ | **减 Agent 读码量**（slice 替整文件）+ **提 manifest/锚点对准率** |
| 与全仓半自动改图？ | **无关且不应合并**；AST 锚点轨是 §K.6 P2/P3 的加速器，不是 P4 autopilot |


---

## M. P1-1 闭合 · 叙述层 drift_check 方案 A 落盘摘要

> **状态**：**已关闭**（2026-06-02）  
> **决策**：方案 A — `drift_check` 并入 `tech-graph` CI，**fail**（非 warn）  
> **证据**：commit `da4e7b7` · playbook [`2026-06-02-tech-graph-drift-check-option-A_playbook_v1_zh.md`](./2026-06-02-tech-graph-drift-check-option-A_playbook_v1_zh.md)（`docs/diary/` 正式版；本目录 tmp 为工作副本）

### M.1 审计项对照

| 审计原缺口（§F P1-1） | 落盘后 |
| --- | --- |
| `99_spec` P0_3 标 done 但 CI 未接 | `tech-graph.yml` 新增 step，与 `99_spec` Backlog 一致 |
| 本地 `drift_check` exit 1 | 还债后 **exit 0**（2026-06-02 复验） |
| manifest 有端点、md 搜不到 | **第三层门禁**：叙述轨字面量子串匹配 |

### M.2 三层 drift（终态）

| 俗称 | 工具 | CI |
| --- | --- | --- |
| **机器轨** | `graph_export.py --check` | **是** |
| **门牌号轨** | `manifest_check.py` | **是** |
| **叙述轨** | `drift_check.py` | **是**（方案 A） |

### M.3 变更文件（`da4e7b7`）

| 文件 | 变更 |
| --- | --- |
| `.github/workflows/tech-graph.yml` | export `--check` 与 equivalence 之间增加 `drift_check` step |
| `docs/_tech_graph/99_spec.md` | 新增 **drift_check 叙述层索引** 集中维护段 |
| `docs/_tech_graph/14_runtime_observability.md` | `/api/py/live` · `/api/py/ready` + DEBUG 字面量 |
| `docs/_tech_graph/01_struct.md` | `chatbi_access_tokens` classDiagram 条目 |
| `docs/diary/2026-06-02-tech-graph-drift-check-option-A_playbook_v1_zh.md` | 操作指引 v1.0 |

**未改**：`tools/tech_graph_drift_check.py` 逻辑；`.ai.md` 拓扑 / `graph.json`。

### M.4 日常维护（并入 §K.2 ④）

```bash
python tools/tech_graph_manifest_check.py
python tools/tech_graph_test_manifest_check.py --check-failure-paths
python tools/tech_graph_graph_export.py --check
python tools/tech_graph_drift_check.py          # v1.3 起与 CI 同序
python tools/tech_graph_graph_equivalence_check.py
```

**同 PR 规则**：新端点 / 表 / 关键 env → `_manifest.json` + **某篇** `_tech_graph/*.md` 出现相同字面量（env 优先 `99_spec` 索引段）。

### M.5 仍开放与分工（playbook §6 · §7–§8）

| ID | 状态 | 负责 |
| --- | --- | --- |
| P1-2 路由→子图自动 | 不做 | — |
| P1-3 render_ai `--dry-run` | 待做 | **后端 Agent** |
| P1-4 金样板 PR 索引 | 待做 | **后端 Agent** |
| GUIDE §3.2 快照 | 待做 | **后端 Agent**（维护文字） |

**分工（playbook §7）**：方案 A 机制已由叙事侧推动落地（2026-06-02）；**后续** `api/`、`tools/`、`_tech_graph/` 源稿、workflow **仅后端 Agent PR**。叙事 Agent 限 `ai_coding_governance/narrative/` 与 REFER/GUIDE 文字。

### M.7 playbook §7–§8 摘要

- **§7**：叙事 vs 后端 Agent 边界；Git 真源 `docs/diary/` playbook（`tmp/` 在 `.gitignore`）。
- **§8**：P1-3/P1-4、GUIDE §3.2、可选 P2；**勿做** CI bot export 写回 / 全仓 AST→Mermaid。

### M.6 与 §L（AST 锚点轨）关系

- **叙述轨 drift_check**：代码符号是否在 **md 全文** 可搜到（粗、cheap、已 CI）。  
- **AST 锚点轨（§L）**：`path::symbol` 是否存在、行号、slice（细、待 Phase B/C）。  
- **互补**，非替代；公众稿 **不必展开**（见对话共识 2026-06-02）。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-02 | 全能力审计完整落盘（对话产出） |
| v1.1 | 2026-06-02 | 增补 §K：可落地方案、全仓半自动原因与演进路线图 |
| v1.2 | 2026-06-02 | 增补 §L：AST 锚点升级轨（语义点 + 强锚点三轨模型） |
| v1.3 | 2026-06-02 | P1-1 闭合：§F 更新 · 增补 §M（方案 A drift_check 进 CI · `da4e7b7`） |
| v1.4 | 2026-06-02 | §M 对齐 playbook §7–§8 分工；审计拷至 `docs/diary/` |
