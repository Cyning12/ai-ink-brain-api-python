# 任务审核：技术图谱 graph_v2 + graph_query + 闸口 B

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md` |
| **关联 SPEC** | `docs/tech_graph/SPEC/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md`；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| **轮次** | R1 |
| **审查日期** | 2026-05-17 |
| **invoke_snapshot** | 无（本轮用户未提供已落盘 Invoke §3 快照路径） |
| **对照规约** | `docs/harness/prompts/hats/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5 |
| **用户焦点** | task **§2.1** `graph_v2` 字段集是否过重；是否应先砍 `ref` / 分图做最小集 |

---

## 审查结论摘要

task 与 **机器轨 SPEC 草案**、闸口 A 定稿、G-END 决议 **方向一致**；`test_strategy: required`、`failure_paths`（FP-1～FP-5）、阶段表 **P2-0～P2-4** 与 Harness §5 **对齐良好**。

**§2.1 v2 字段集（用户焦点）**：相对闸口 A 已证缺口与方案2 查询需求，**当前草案表偏「终局富化」、偏重**；**建议执行前由任务帽将 §2.1 拆为 P2-0 最小集 + P2-4/follow-up 延后项**，其中 **`graphs[]` 分图与 `edges[].ref` 应延后**，首版维持与 v1 同型的 **单图扁平拓扑 + 语义富化**（锚点、边 `mark`/`label`）。

**结论**：**有非硬阻塞的设计缺口**；**不建议执行帽开工**，直至任务帽回填 **§2.1 字段分层**（及下表两项轻量澄清）。回填后须 **R2** 再审。

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **建议阻塞执行（设计）** | B-D1 | §2.1 未区分 **P2-0 最小 v2** 与 **P2-4 富化**；易导致 P2-0 过度设计（分图 + ref） |
| **非阻塞（执行前宜澄清）** | N-1 | `graph_v2` 落盘为 **升级现有 `graph.json`** 还是 **并列文件** — task 写「PR 二选一」，执行前须在 §2.1 或 §8 定一句默认 |
| **非阻塞（执行前宜澄清）** | N-2 | `freeze_id: TECH_GRAPH_S2_FREEZE_TBD` — draft 可接受；**merge 前**须与 `protocol_version.yaml` 对齐 |
| **非阻塞（Harness）** | N-3 | 闸口 B 指标/样本量未量化 — 不阻 P2-0～P2-2，阻 **签收**（§4.3） |
| **已核对通过** | ✓ | G-END 与闸口 A「不默认 v1 整包」一致；非范围含方案3/退役 `.ai.md`；Agent 加载顺序（§2.1 C）与 SPEC §4 规范层边界一致；`failure_paths` 可观测；`test_strategy: required` 有 note |

---

## §2.1 v2 字段集专项审查（相对 v1 与闸口 A）

### 现状基线（v1）

仓库内 `docs/_tech_graph/graph.json` 为 **`graph_v1`**：扁平 `edges[]`（`from`/`to`/`type`/`sync`）+ `nodes` 为 **id 字符串列表**，**无** `anchors`、`mark`、边 `label`、分图、`ref`。闸口 A 已将其定性为 **有损投影**，P1/P2 偏 Mermaid。

### 字段逐项（task §2.1 表）

| 字段/结构 | P2-0 最小集 | 理由 |
|-----------|-------------|------|
| `schema_version` / `generated_at` / `freeze_id` | **保留** | CI 与方案1 惯例延续 |
| `nodes[].id` | **保留** | query 与拓扑基础 |
| `nodes[].label` | **建议保留** | 低成本补闸口 A「节点标签缺失」；利于 P1 可读子图 |
| `nodes[].kind` | **可延后** | 非等价检查与 BFS 必需 |
| `edges[].from/to` | **保留** | 同 v1 |
| `edges[].mark` | **保留** | 协议边语义；等价检查核心 |
| `edges[].type` / `sync` | **保留** | 与 v1 兼容 |
| `edges[].label` | **保留** | 闸口 A 边文案缺口；query 返回须能带上下文 |
| `edges[].anchors[]` | **保留** | 闸口 A 主缺口；等价门禁核心 |
| `graphs[]`（分图） | **延后 → P2-4** | v1 已扁平合并；方案2 仅需单图邻接；分图不解决 token，反增导出/校验复杂度 |
| `edges[].ref` | **延后 → P2-4** | 依赖分图模型；首版 query 用 k-hop 子图即可，无需跨图硬引用 |

### 与机器轨 SPEC 草案的一致性

- SPEC §4：**v2 仍可不合并** `01_struct` / `99_*` — 与 **砍分图** 不冲突；规范层继续走 **按需加载**（task §2.1 C 已写）。
- SPEC §5 等价性：**拓扑 + 锚点 + 边标签** — **最小集已覆盖**；`graphs[]`/`ref` 属 **组织富化**，非闸口 B 前必要条件。

### 建议写入 task 的 P2-0 最小集（供任务帽粘贴）

```text
P2-0 最小 graph_v2（单图，schema_version: graph_v2）：
  元数据：schema_version, generated_at, freeze_id
  nodes[]：id, label（可选 kind 延后）
  edges[]：from, to, mark, type, sync, label, anchors[]
禁止 P2-0 依赖：graphs[] 多分图、edges[].ref
P2-4 / follow-up：graphs[]、ref、manifest graph_node_id 交叉引用
```

---

## 需任务帽回填清单

- [ ] **§2.1 A**：在「最小字段集」下增 **「P2-0 最小集」** 与 **「P2-4 / follow-up 延后」** 两子表（或等价列表），按上文 **砍 `graphs[]` + `ref`**。
- [ ] **§2.1 A**：明确 **v2 首版落盘策略**（默认建议：**同路径 `graph.json` 升 `schema_version: graph_v2`**，v1 检查过渡在 PR 说明 — 二选一须写一句默认）。
- [ ] **§6**：P2-0 交付物改为「**最小 v2 schema + 等价检查草案**」；将「分图/ref」与 §2.1 延后项对齐到 **P2-4** 行（task 已有 P2-4 可选 manifest，可合并叙述）。

回填完成后：**R2 任务审核**（`PREV_REVIEW_PATH` 指向本文件）。

**2026-05-17 更新**：task 已 **v0.2 按 R1 回填** → 下一棒 invoke：`Projects/docs/harness/invokes/invoke_20260517_22_tech-graph-v2-task-audit-r2.md`；10 帽交接：`invoke_20260517_10_tech-graph-v2-r1-backfill-complete-handoff.md`。

---

## 是否建议执行帽开工

**不建议**。先由 **任务帽** 完成上表回填；**R2** 无 B-D1 后再建议执行帽从 **P2-0** 开工。

---

## 签收 / 关闭

- **本轮（R1）**：**不声明 task 可结束**；task 仍为 `draft`，且 §2.1 字段分层未落盘。
- **任务正式关闭条件（供终轮引用）**：§4.1 工程验收 + §4.2 闸口 B + §4.3 B-1～B-3；等价 CI 连续绿；§8 实现备忘填齐；终轮审查 **签收 / 关闭** 与 task `done` 一致。

---

## 下一棒可复制 Prompt

以下与 **对话回复** 中「下一棒」块 **逐字一致**。

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
按任务审核 R1 结论，回填 ai-ink-brain-api-python 后端 task：将 §2.1 graph_v2 字段拆为 P2-0 最小集（单图扁平 + anchors/label/mark）与 P2-4 延后项（graphs[]、edges[].ref）；并写清 graph.json 升版 vs 并列文件的默认策略。勿扩 scope 到方案3或退役 .ai.md。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md
docs/tech_graph/SPEC/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md
ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_v2_graph_query_v1/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_v2_graph_query_v1/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
3. 若 AUDIT 路径非「无」：按该审查文档的回填清单逐条映射到 task 小节建议，并在建议文末注明「按审查 R<n> 回填」应指向的文件名。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值。
5. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。

不强制落盘；若用户要求写入某 task 文件，须由用户明确路径后再编辑（本模板不预置写文件占位符）。
```

---

## 给下一棒

下一棒：**需求与任务分析帽**（回填 task §2.1 / §6）；完成后用 `TEMPLATE-task-audit-invoke.md` 发起 **R2** 任务审核。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-17 | R1：§2.1 字段过重结论；建议砍 graphs[]/ref；不建议执行帽开工 |
