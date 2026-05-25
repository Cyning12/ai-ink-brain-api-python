# 任务审核：技术图谱 graph_v2 + graph_query + 闸口 B（R2）

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md`（**v0.2** · 按审查 R1 回填） |
| **上一轮审查** | `ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_v2_graph_query_v1/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md` |
| **关联 SPEC** | `docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md`；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| **轮次** | R2 |
| **审查日期** | 2026-05-17 |
| **invoke_snapshot** | `docs/harness/invokes/invoke_20260517_22_tech-graph-v2-task-audit-r2.md`（相对工作区根 `Projects/`） |
| **对照规约** | `docs/harness/prompts/hats/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5 |
| **对照材料** | `ai-ink-brain-api-python/docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md`（§8.2～§8.3、§8A）；闸口 A `docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` |

---

## 审查结论摘要

task **v0.2** 已按 **R1 回填清单** 六项在正文落盘；与 **机器轨 SPEC 草案**、**治理层应用文**（§8.2～§8.3、§8A）、闸口 A 结论 **无方向性矛盾**。Harness §5 字段（`test_strategy: required` + note、`failure_paths` FP-1～FP-5、阶段表）**可支撑执行帽拒开工门闸**。

**R1 阻塞项 B-D1（§2.1 字段过重未分层）已闭合。**

**结论（零硬阻塞）**：**建议执行帽从 P2-0 开工**（最小 v2 schema 文档 + 等价检查草案；**禁止** P2-0 实现 `graphs[]` / `edges[].ref`）。

---

## R1 回填清单 — 逐项核对

| # | R1 要求 | task 落点 | 结论 |
|---|---------|-----------|------|
| 1 | §2.1：**P2-0 最小集** vs **P2-4 延后** 两表；P2-0 **禁止** `graphs[]`、`ref` | §2.1 A 表 L67–89；§8 必读 L212 | **通过** |
| 2 | 默认落盘 = **同路径** `graph.json` + `schema_version: graph_v2` | §2.1 A L62；§8 L213 | **通过** |
| 3 | §6 与 P2-0/P2-4 一致 | §6 L189–193：P2-0 无 graphs/ref；P2-4 含 graphs/ref/kind/manifest 互引 | **通过** |
| 4 | **G-END-6**、治理层链、与闸口 A「不默认 v1 整包」一致 | §0 G-END-5/6 L23–24；§1 L45–51；§3 L132；§8 L211 | **通过** |
| 5 | **非范围**：跨会话长期记忆单独立项 | §2.2 L118（链治理层 §8A） | **通过** |
| 6 | §7：**禁止外推**论文 SBM ARI=1 | §7 L201；头部 L7 | **通过** |

### 1 号项摘录（供复检）

**P2-0 必达**：`schema_version` / `generated_at` / `freeze_id`；`nodes[].id` + `label`；`edges[]` 的 `from`/`to`/`mark`/`type`/`sync`/`label`/`anchors[]`；**无** `graphs[]`、**无** `edges[].ref`；`nodes[].kind` 标为延后。

**P2-4 延后**：显式列出 `graphs[]`、`edges[].ref`、`nodes[].kind`、manifest↔node 互引，并写 **「禁止 P2-0 依赖」**。

---

## Harness §5 与可读性（R2 增量核对）

| 字段 / 小节 | 状态 | 备注 |
|-------------|------|------|
| `test_strategy: required` + note | ✓ | 与 P2-0～P2-2、闸口 B 范围匹配 |
| `failure_paths` | ✓ | FP-1～FP-5 含触发/行为/可重试；FP-5 禁止静默 v1 降级 |
| `freeze_id` | 草案 `TECH_GRAPH_S2_FREEZE_TBD` | **非阻塞**（沿用 R1 **N-2**：merge 前与 `protocol_version.yaml` 对齐） |
| 验收 §4.1～4.3 | ✓ | 工程 + 闸口 B + 签收门槛分层清晰 |
| 必读列表 §8 | ✓ | 与 §2.1、G-END、治理层 §8.2～§8.3 一致 |

---

## 对照：治理层应用文 & 机器轨 SPEC

| 对照点 | 治理层 / SPEC | task v0.2 | 一致性 |
|--------|---------------|-----------|--------|
| 抗漂移 = CI + 版本 + 等价 | §8.2 | G-END-6 ①；等价检查 + `freeze_id` | ✓ |
| token 主因 = 少读子图（query） | §8.2～§8.3 | §1 目标；`graph_query`；闸口 B **CTX_QUERY** | ✓ |
| 非「JSON 整包替 `.ai.md` 提理解」 | §8.3 | §1、G-END-5、FP-5 | ✓ |
| 长期记忆另立项 | §8A | §2.2 非范围 L118 | ✓ |
| 禁止外推 ARI=1 | §7 | task §7 L201 | ✓ |
| v2 不合并规范层全文 | SPEC §4 | §2.2、§2.1 C 加载顺序 | ✓ |
| 等价验收 = 拓扑 + 锚点 + 边标签 | SPEC §5 | §2.1 阈值；§4.1 | ✓ |

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **硬阻塞** | — | **无** |
| **非阻塞（执行期）** | N-2 | `freeze_id` 仍为 TBD；P2-1 起导出/CI 前须 bump（R1 已记） |
| **非阻塞（签收期）** | N-3 | 闸口 B Rubric 样本量「≥3 题」仍粗；**不阻 P2-0～P2-2**（R1 已记） |
| **非阻塞（文案）** | N-R2-1 | §2.2「方案3 Neo4j（**R2 未满足**）」易与 **本轮 R2 审查** 混淆；建议任务帽改为「非本 task 范围」或「另立项」 |
| **非阻塞（路径）** | N-R2-2 | 治理层文物理路径为 `ai-ink-brain-api-python/docs/diary/jsonPKmermaid/...`；task 用子仓相对 `docs/diary/...` — **在子仓 cwd 正确** |

---

## 是否建议执行帽开工

**建议**。从 **§6 P2-0** 开工：落盘最小 **graph_v2** schema 文档 + **等价检查**草案/脚本骨架；**不得**在 P2-0 引入 `graphs[]`、`edges[].ref` 或对其的测试依赖。

合并前须绿（本子仓）：`pytest tests -m "not intent_eval and not intent_benchmark"`（与根 `AGENTS.md` §8 一致）；图谱相关变更另遵 `tech-graph.yml`。

---

## 签收 / 关闭

- **本轮（R2）**：**不声明 task 实现完成**（仍为 `draft`，§4 验收未勾）。
- **本轮声明**：**任务文档层已满足执行开工条件**；B-D1 已闭合；**可交执行帽 P2-0**。
- **任务正式关闭条件（供终轮引用）**：§4.1 + §4.2 闸口 B + §4.3 B-1～B-3；§9 实现备忘填齐；等价 CI 连续绿；终轮审查 **签收** 与 task `done` 一致。

---

## 下一棒可复制 Prompt

以下与 **对话回复** 中「下一棒」块 **逐字一致**。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入（占位符已替换）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md
- 子仓根（相对 Projects/）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_v2_graph_query_v1/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md
- 关联 SPEC / 总规：
docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md
docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md
docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

你必须完成：
0. Invoke 快照：按 docs/harness/invokes/README.md 将本消息全文落盘后再开工。
1. 通读 task v0.2：从 §6 **P2-0** 开工——最小 graph_v2 schema 文档 + 等价检查草案；**禁止** P2-0 实现 graphs[]、edges[].ref（见 §2.1、§8）。
2. 必读：治理层应用文 §8.2～§8.3（路径 ai-ink-brain-api-python/docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md）；task §7 禁止外推 SBM ARI=1。
3. test_strategy: required——先失败测试/门禁再扩实现；P2-0 阶段以 schema + equivalence 脚本/测试为主，勿扩到 graph_query 或闸口 B。
4. 默认落盘：同路径 docs/_tech_graph/graph.json，schema_version: graph_v2（勿默认并列 graph_v2.json）。
5. 子仓根执行 pytest（上列 VERIFY）；结论回填 task「### 自检结论（执行者）」。
6. 对话回复：输出下一棒可复制 Prompt（自检帽或任务审核，视阻塞而定）。

禁止：静默整包 v1 作 query 默认；合并 tech_graph_contract_check 与 graph 导出；扩 scope 至方案3/退役 .ai.md/长期记忆产品。
```

---

## 给下一棒

下一棒：**执行编码帽**，从 **P2-0** 开工；依赖本文件 **R2** 结论与 task **§8** 必读列表。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-17 | R2：R1 回填六项通过；零硬阻塞；建议执行帽 P2-0 开工 |
