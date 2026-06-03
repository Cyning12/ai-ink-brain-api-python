# SPEC — 治理：技术图谱 · SQL 闸对齐与锚点校验 backlog（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` — **选择性抽空实施**；单项 `planned` → `active` → `done` 在 §4 维护 |
| **freeze_id** | `GOV-TG-ANCHOR-SQLGATE-BACKLOG@2026-06-03` |
| **承接仓** | **样板**：`ai-ink-brain-api-python` · **可推广**：`ai-ink-brain`（§8） |
| **姊妹 SPEC** | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) · [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) · 前端 [`SPEC-tech_graph_v2_frontend_parity_v1.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC-tech_graph_v2_frontend_parity_v1.md) |
| **外部参考（非 L0）** | 治理仓 `10_REVIEW_Ink后端技术图谱第三轮深度测评_v1_zh.md` · `11_REVIEW_L3_L2理论层缺口分析_v1_zh.md` · `09_PLAN_Ink后端改进方案_可推广_v1_zh.md` |

---

## 0. 用途（一句话）

把 **「SQL AST 后闸已在代码、图谱未对齐」** 与 **「锚点轻量校验（非全仓 AST 扫图）」** 的改进项，按 **P0 → P1 → P2** 排序落盘；维护者 **按需抽空** 做单条 task，**不要求** 一次性全做。

---

## 1. 术语消歧

| 说法 | 本 SPEC 指什么 | 本 SPEC **不**指什么 |
| --- | --- | --- |
| **SQL AST** | `api/chatbi_sql_gate.py::apply_chatbi_sql_gate` 内 AST → 表白名单 → 档位三阶段（**已实现** · `task_chatbi_v3_sql_ast_text2sql_gate_v1` done） | 重写 gate 逻辑 |
| **锚点校验** | 扫 `.ai.md` 中 `// → path::symbol` / `path#Ln`，验 **文件与符号是否存在** | `graph.auto.json` 全仓依赖 AST 导出 |
| **Mermaid AST** | — | 用完整 Mermaid 解析器替换 `tech_graph_graph_export` 的 regex 子集 |

**已拒方向（勿在本 backlog 立项）**：`graph.auto.json` 主路径 · 全仓代码 AST 依赖图 · post-merge bot 自动改 `_tech_graph/`（见 FAQ F7 · `09_PLAN` §4.4）。

---

## 2. 与现有 CI 的分工

| 已有 | 缺口（本 backlog 填） |
| --- | --- |
| `graph_export --check` | `.ai.md` ↔ `graph.json` 拓扑一致；**不**验锚点是否仍对应当前执行路径 |
| `manifest_check` / `contract_check` | 端点 / SSE 契约 vs 源码；**不**扫 Mermaid 注释锚点 |
| `drift_check` | 表/env/端点 **字面量** 在 `.md` 中出现；**不**验 `path::symbol` |
| SQL AST pytest | 行为真值；**不**更新 `11_flow_text2sql` 节点 |

---

## 3. 优先级总表（实施顺序）

图例：**改动** S/M/L · **收益** 对 `graph_query` 影响面 / CI 拦截 / Agent 读图 · **状态** `planned`（默认）

| 序 | ID | 优先级 | 改动 | 收益 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | **TG-AST-01** | **P0** | S | 高 | `planned` |
| 2 | **TG-AST-02** | **P0** | S | 高 | `planned` |
| 3 | **TG-AST-03** | **P0** | M | 高 | `planned` |
| 4 | **TG-AST-04** | **P0** | S | 中 | `planned` |
| 5 | **TG-AST-05** | P1 | S | 中 | `planned` |
| 6 | **TG-AST-06** | P1 | M | 高 | `planned` |
| 7 | **TG-AST-07** | P1 | M | 中 | `planned` |
| 8 | **TG-AST-08** | P1 | S | 低 | `planned` |
| 9 | **TG-AST-09** | P2 | M | 中 | `planned` |
| 10 | **TG-AST-10** | P2 | L | 中（大仓） | `planned` |

**建议抽空组合**（单次 PR 可合并）：

- **包 A（≈0.5 人日）**：TG-AST-01 + 02 + 05 + export `--check`
- **包 B（≈1 人日）**：TG-AST-03 + 04 + pytest + `tech-graph.yml` 一步
- **包 C（按需）**：TG-AST-06 + 07（V3 盲区补节点）

---

## 4. 条目明细

### P0

#### TG-AST-01 · Text2SQL：VAL 拆分为 VAL_RAW + GATE

| 项 | 内容 |
| --- | --- |
| **问题** | 图谱 `VAL` 仅锚 `validate_sql_readonly`；有 `principal` 时实际走 `apply_chatbi_sql_gate`（AST 三阶段） |
| **交付** | 改 `docs/_tech_graph/11_flow_text2sql.ai.md` + 人读 `.md`：`VAL_RAW`（无 principal）→ `GATE`（有 principal，注释 AST→表策略→档位） |
| **验收** | `python tools/tech_graph_graph_export.py --check` 绿；`graph_query` 从 `GATE` 下游含 `chatbi_sql_gate` 相关节点/边 |
| **非范围** | 改 `chatbi_sql_gate.py` 行为 |
| **参考** | `10_REVIEW` §2.2 · §5 P0 |

#### TG-AST-02 · GATE 节点锚点 `apply_chatbi_sql_gate`

| 项 | 内容 |
| --- | --- |
| **问题** | `chatbi_sql_gate.py` 在测评「盲区表」：文字提及、无 `// →` 锚点 |
| **交付** | 在 TG-AST-01 的 `GATE` 节点增：`// → api/chatbi_sql_gate.py::apply_chatbi_sql_gate`（或协议允许的 `#Ln`） |
| **验收** | 锚点行符合 `99_mermaid_protocol.md`；export 后 `graph.json` 节点 metadata/anchors 与现网 export 规则一致 |
| **依赖** | TG-AST-01（可同 PR） |

#### TG-AST-03 · `tech_graph_anchor_check.py` v1（符号存在性）

| 项 | 内容 |
| --- | --- |
| **问题** | CI 绿但锚点 **存在却非当前路径**（VAL 类问题无法在 merge 前发现） |
| **交付** | 新脚本 `tools/tech_graph_anchor_check.py`：扫描 `docs/_tech_graph/*.ai.md` 锚点注释 → 校验 `api/`（及 SPEC 约定路径）内 **文件存在 + 符号/行号可解析**；stderr 复用 [`tech_graph_ci_stderr.py`](../../../tools/tech_graph_ci_stderr.py) 三段式 |
| **CI** | `tech-graph.yml` 增 step（与 `manifest_check` 顺序：建议 **export --check 之后**） |
| **验收** | 故意错锚点 → exit 非 0 + Runbook 链；`pytest tests/test_tech_graph_anchor_check.py`（golden ≥2） |
| **非范围（v1）** | 调用链是否仍引用该符号（→ TG-AST-09） |
| **参考** | `11_REVIEW` L2-1 · [`L2-Anchor-Test-Manifest`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) §3 |

#### TG-AST-04 · `99_mermaid_protocol.md`：P0 节点与 `path::symbol`

| 项 | 内容 |
| --- | --- |
| **问题** | 节点粒度无规约 → V3 模块常以「文字注释」代替结构化节点 |
| **交付** | 在 `99_mermaid_protocol.md` 增 §：**P0 节点**（路由 handler、Agent 核心类、安全闸函数）须独立节点 + 锚点格式 `path::symbol` |
| **验收** | 22/10 帽 README 或 AGENTS 链一节；**不**阻塞 merge（纯文档） |
| **参考** | `11_REVIEW` P0 L3 行 |

---

### P1

#### TG-AST-05 · Text2SQL 边标记修正（`~>` → `->`）

| 项 | 内容 |
| --- | --- |
| **问题** | GEN→VAL、EXEC→DB、SUM→OUT 在代码中为同步，图谱误标异步 |
| **交付** | 改 `11_flow_text2sql.ai.md` 三处边标记 |
| **验收** | export `--check` 绿 |
| **参考** | `10_REVIEW` §2.3 |

#### TG-AST-06 · Agent 核心节点（`ChatBIAgent` 等）

| 项 | 内容 |
| --- | --- |
| **问题** | `api/agent.py` 无结构化节点，影响 Agent 子图查询 |
| **交付** | 在 `11_flow_text2sql.ai.md` 扩图或新增 `16_flow_agent.ai.md`（须双轨 `.md`）；节点含 `ChatBIAgent` 等 + 锚点 |
| **验收** | export 绿；可选：`graph_query describe-impact` 含新节点 |
| **参考** | `10_REVIEW` §5 P0 第 1 行 |

#### TG-AST-07 · Intent V2 节点（`decide_intent_v2` 等）

| 项 | 内容 |
| --- | --- |
| **问题** | 图谱仍偏 V1 `intent_router`，与 `intent_agent.py` 脱节 |
| **交付** | 更新 Intent 阶段节点与锚点 |
| **验收** | 同 TG-AST-06 |
| **参考** | `10_REVIEW` §5 P0 第 2 行 |

#### TG-AST-08 · 其它 ChatBI 辅助模块锚点（批量小项）

| 项 | 内容 |
| --- | --- |
| **范围** | `chatbi_prompt_guard` · `chatbi_plan_token` · `chatbi_request_ctx` · `chatbi_json_log` 等（见 `10_REVIEW` §2.1 表） |
| **交付** | 各在对应流程图阶段补 **单节点或注释锚点**（不必一次补全 15 个盲区） |
| **验收** | 每批 ≥1 模块 + export 绿；TG-AST-03 绿 |

---

### P2

#### TG-AST-09 · 锚点校验 v2（关键节点调用链 / manifest 交叉）

| 项 | 内容 |
| --- | --- |
| **问题** | v1 仅「符号存在」；无法抓「存在但 dead path」 |
| **交付** | 扩展 `anchor_check`：对 SPEC 声明的 P0 节点列表，交叉 `_manifest.json` 或轻量静态引用（**禁止** 全仓 AST） |
| **验收** | 用 VAL→GATE 迁移类回归用例锁行为 |
| **依赖** | TG-AST-03 done |

#### TG-AST-10 · PR 触达子图增量 manifest（IMP-B-05）

| 项 | 内容 |
| --- | --- |
| **问题** | 全量 manifest CI 在大仓 PR 上耗时线性涨 |
| **交付** | task 声明 `graph_entry` → 仅跑触达子图相关 check 子集 |
| **验收** | 大 diff PR 时间可测下降；**不**替代全量 Required 的 baseline job |
| **参考** | `09_PLAN` IMP-B-05 · `ASSESS` U1 增量校验 |

---

## 5. 选择性实施纪律

1. **单条立项**：`docs/tasks/active/task_tg_ast_<ID>_v1.md`，头部 `freeze_id` 链本 SPEC + 条目 ID。  
2. **改 `api/` 时**：仍走既有 Harness（Delta · `test_strategy` · 50）；本 backlog **多数只动** `docs/_tech_graph/` + `tools/`。  
3. **状态回写**：条目 `done` 后更新 §3 表 + 本文件修订记录；**不**要求一次关整份 SPEC。  
4. **Agent 读序**：改拓扑前 `graph_query neighbors <node>`；改 gate 链前先读 `11_flow_text2sql.ai.md` + `api/tools.py` 中 `text2sql_execute` 分支。

---

## 6. 验收命令（包 A / B 通用）

```bash
# 仓库根 ai-ink-brain-api-python
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
python tools/tech_graph_anchor_check.py          # TG-AST-03 落地后
pytest tests/test_tech_graph_graph_export.py tests/test_tech_graph_anchor_check.py -q
pytest tests -m "not intent_eval and not intent_benchmark"
```

Runbook（契约/manifest 红）：[`docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md`](../../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md)

---

## 7. 非范围（全文）

- Mermaid 全语法 AST 解析器替换 export  
- `graph.auto.json` 与代码 AST 合并主路径  
- Neo4j / 方案3（见 `改进方向.md` R2）  
- 替代 ChatBI V3 安全 SPEC（`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md`）  
- 修改 jsonPKmermaid 已 **accepted** 实验结论  

---

## 8. 前端推广（`ai-ink-brain`）

### 8.1 结论

**可推广的是方法论与工具形态，不是后端业务条目。**  
前端已有：`docs/_tech_graph/` · `_manifest.json` · `.ai.md` 锚点（`components/`、`app/api/`、`lib/`）· 复用后端 `tech_graph_*` 脚本（`package.json` · `--repo frontend`）。  
**不推广**：TG-AST-01/02（Python SQL AST 后闸）；**跨仓契约**仍以后端 `_contract_manifest.json` 为真值 + 双 checkout `contract_check`。

### 8.2 条目映射（后端 ID → 前端等价）

| 后端 ID | 前端是否适用 | 前端等价动作 | 优先级 |
| --- | --- | --- | --- |
| TG-AST-01/02 | **否** | —（SQL gate 在后端）；前端仅 **BFF 转发链** 与 **SSE 消费** 对齐 `11_flow_api` / `contract_check` | — |
| TG-AST-03 | **是** | `anchor_check` 增 **`--repo frontend`**：扫 `docs/_tech_graph/*.ai.md` → 验 `app/`、`components/`、`lib/` 路径与 **导出符号/文件存在**（TS：文件存在 + 可选 `export`/`default` 轻量 grep，**非** ts-morph 全仓） | **P0** |
| TG-AST-04 | **是** | 前端 `99_mermaid_protocol.md` 已有；补 **P0 节点**（Route Handler、BFF 转发、关键 Client 组件）与 `path::symbol` / `path` 约定 | **P0** |
| TG-AST-05 | **是** | 前端 flow 图内 **`~>` 误用** 按同样规则修正（域内 grep `.ai.md`） | P1 |
| TG-AST-06/07 | **域替换** | 非 ChatBI Agent，而是 **Unified/Chain BFF**、**portfolio-chat-tier**、**auth gate** 等节点是否与 `11_flow_api` / `12_flow_auth` 一致 | P1 |
| TG-AST-08 | **是** | 补 `lib/chat/chatApi.ts`、SSE stream route 等 **稀疏锚点**（对齐 frontend parity §4 W2） | P1 |
| TG-AST-09 | **是** | v2：BFF route ↔ `_manifest.json` `routes[]` 交叉（manifest 已覆盖路由；锚点 v2 补 **组件↔route**） | P2 |
| TG-AST-10 | **是** | 大 PR 时仅触达 `10_flow_route` / `11_flow_api` 子图 + manifest 子集（与 IMP-B-05 同抽象） | P2 |

### 8.3 前端已有 vs 待补

| 能力 | 前端现状 | 本 backlog 推广后 |
| --- | --- | --- |
| `graph_export --check` | `quality.yml` + `pnpm tech-graph:graph-check` | 保持 |
| `manifest_check --repo frontend` | 脚本支持；CI 接入程度见 frontend parity SPEC | 保持并文档化 |
| `contract_check` | 双 checkout；消费后端契约 | **不**复制 manifest |
| `anchor_check` | **未做** | TG-AST-03 落地时 **一次实现双 profile**（后端默认 + `--repo frontend`） |
| IMP-B-01 stderr / PR 模板 | 前端 pr-post-ci 推进中 | 与后端 **语义对齐**，检查名用 `quality` / `verify` |

### 8.4 推广顺序（建议）

```text
1. 后端 TG-AST-03 实现时带 --repo frontend（单脚本双仓，避免 fork）
2. 前端 TG-AST-04 + 08（纯 docs/_tech_graph，包 A 级）
3. 前端 CI：quality 增 anchor_check step（与 graph-check 并列）
4. 跨仓：contract_check 已绿前提下，不重造 SSE 字段 AST
```

### 8.5 前端 task 命名

`ai-ink-brain/docs/tasks/active/task_tg_ast_frontend_<主题>_v1.md` · 头部链 **本 SPEC §8** + [`SPEC-tech_graph_v2_frontend_parity_v1.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC-tech_graph_v2_frontend_parity_v1.md)。

**禁止**：在前端仓复制 `chatbi_sql_gate` 或后端 Text2SQL 子图文件。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-03 | 初版：P0～P2 backlog · SQL 闸图谱对齐 + anchor_check v1/v2 · 选择性实施纪律 |
| v1.1 | 2026-06-03 | §8 前端推广：条目映射 · 双 profile anchor_check · 与 frontend parity 分工 |
