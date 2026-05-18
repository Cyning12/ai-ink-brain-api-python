# 任务审核：技术图谱 — 闸口 C（graph_v2 查询轨 vs 双轨原文）

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md`（**v0.1**） |
| **关联 SPEC / 总规** | `Projects/docs/tech_graph/改进方向.md`（**R4** 对比实验）；`Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| **轮次** | **R1**（首轮） |
| **审查日期** | 2026-05-18 |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_22_tech-graph-gate-c-v2-dual-track-audit-r1.md` |
| **需求帽 invoke** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_10_tech-graph-gate-c-v2-dual-track-requirements.md` |
| **对照规约** | `docs/harness/prompts/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5、`HANDOFF_SEMI_AUTO.md` |
| **git_branch** | `task/engineering-tech-graph-gate-c-v2-dual-track-v1` |
| **audit_profile** | `post_close` |
| **前置结论（引用、不重跑）** | `conclusion_gate_ctx_ab_final_zh.md`（闸口 A）；`conclusion_gate_b_ctx_query_v1_zh.md`（闸口 B） |
| **materialize 参考** | `fixtures/gate_ctx_b_v1/scripts/materialize_gate_b_payloads.py` |

---

## 审查结论摘要

task **v0.1** 与 **R4** 阶段对比实验、闸口 A/B 归档结论、Harness §5 字段 **整体对齐**。**§0.3** 双臂 **D（`CTX_V2_QUERY`）** / **E（`CTX_DUAL_MD`）** 定义可执行；**NR-1 / NR-2** 与 **FP-C-1** 三重约束「禁止重跑 A/B 主实验」；**P0～P2** 分期与 **PR-1/2/3** 关账边界清楚；**`failure_paths`** 五条可映射到 materialize exit / 拒开工语义；**`test_strategy: required`** 在 `test_strategy_note` 与 §3.1 中要求 materialize + pytest，满足 §5.1。

**本轮结论**：**零硬阻塞**（无需任务帽 R2）。**不**代填 **`HG-AUDIT-R1`**（及任何 `human_gate`）。执行帽 **须待人** 将 **`HG-AUDIT-R1`** 改为 `approved` 后方可开 **30**（见下文）。

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **人工闸（非文档阻塞）** | HG-1 | **`HG-AUDIT-R1`** 为 `pending`（`blocks_hats: 30`）；按 `HANDOFF_SEMI_AUTO` §2.3，**30 拒开工**直至人改 `approved`。另：**`HG-P0-PROTOCOL`**、**`HG-GATE-C-SIGNOFF`** 为执行期/关账闸，不阻 R1 书面通过 |
| **非阻塞（文案一致）** | N-1 | task 标题下仍写「待 `HG-TASK-DRAFT` 人签」，但 Harness 表内 **`HG-TASK-DRAFT` 已为 `approved`**；建议任务帽改状态行，避免执行帽误读 |
| **非阻塞（执行期细化）** | N-2 | **`dual_track_manifest.json`** 的 per-task **token 上限**仅写「写明」，无数值默认；P0 `protocol_version.yaml` 落盘时给出即可 |
| **非阻塞（freeze 细则）** | N-3 | 头部 `freeze_id` 已占位；**bump 细则**建议在 P0 `protocol_version.yaml` 写清：`freeze_id`（闸口 C 协议）与 **`graph_v2_freeze_id`**（引用 `TECH_GRAPH_S2_FREEZE_20260517_V2_0` 或图变更后新 id）**分列**；改 arms/题集/seeds/manifest → bump 协议 `freeze_id` 末段；**仅** `graph.json` 再生且语义不变 → 只更新 `graph_v2_freeze_id` |
| **非阻塞（D 臂查询面）** | N-4 | D 臂种子可含 `describe-impact`；闸口 B materialize **仅** `downstream`。执行帽以 **`query_seeds.json`** 为准，勿默认复制 B 脚本 op 集合 |
| **非阻塞（Harness）** | N-5 | **P3**（`改进方向.md` 闸口 C 行）为 recommended，不阻 PR-1/2 |
| **已核对通过** | ✓-1 | **§0.3 D vs 闸口 B `CTX_QUERY`**：新协议 `gate_ctx_c_v1`、独立 `TECH_GRAPH_GATE_C_FREEZE_*`、主对比 **D vs E**；B 三臂与 batch **NR-2** 不重跑 — 见下表 |
| **已核对通过** | ✓-2 | **§0.3 E / §5.2**：`CTX_DUAL_MD` = `dual_track_manifest` 精选 **`.ai.md` + 配对 `.md`**，**非**整仓 seven 文件 — 与 FP-C-2、§5.2 一致 |
| **已核对通过** | ✓-3 | **NR-1 / NR-2 / FP-C-1** 与 §0.2、§1.2、前置结论路径互链 |
| **已核对通过** | ✓-4 | **§4 FP-C-2～C-5** 可观测（路径校验、exit 4、token 上限、无 key 阻塞 P1） |
| **已核对通过** | ✓-5 | **`gates_before_code`**、`semi_auto`、`audit_profile`、§5 必读五条齐全 |
| **已核对通过** | ✓-6 | **§3** 验收含 pytest 主链 + batch 目录 + 结论 `accepted` 前人签 **HG-GATE-C-SIGNOFF** |
| **已核对通过** | ✓-7 | 闸口 B **`query_seeds.json`** 已用 `ENV`/`U2`/`A2`（非废弃 `AUTH→RAG` 示例）；task §1.1 / §5.3 禁止沿用废弃种子 — **与现网一致** |

### 臂 D（本 task）vs 闸口 B `CTX_QUERY`（对照表）

| 维度 | 闸口 B · `CTX_QUERY` | 本 task · 臂 D · `CTX_V2_QUERY` |
|------|----------------------|--------------------------------|
| 协议目录 | `gate_ctx_b_v1` | **`gate_ctx_c_v1`（新）** |
| `freeze_id` | `TECH_GRAPH_S2_FREEZE_20260517_V2_0` | **`TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0`**（P0 锁定） |
| 实验问题 | 查询子图 vs 整包 Mermaid/JSON | **查询子图 vs 精选双轨原文（臂 E）** |
| 主跑 arms | A/B 引用 + C 新跑 | **仅 D、E 新跑**（A/B 仅引用结论） |
| 技术共性 | `tech_graph_graph_query.py` 子图、`ref` 不参与 | 同左（§0.3 写明） |
| 与 E 差异 | （无 E 臂） | D = 结构化子图 JSON；E = 原文 Markdown 双轨 |

### R1 重点核对清单（逐项）

| # | 核对项 | 结论 |
|---|--------|------|
| 1 | §0.3 双臂 D/E 可审、不可默改 | **通过** |
| 2 | §1.2 NR-1/2 + P0～P2 + PR 切片 | **通过** |
| 3 | CTX_DUAL_MD 非整包 | **通过**（§0.3、§5.2、FP-C-2） |
| 4 | D vs B `CTX_QUERY` 差异 | **通过**（新协议 + 新 freeze + 对比轴 D/E；见上表） |
| 5 | `freeze_id` / bump | **通过（带 N-3）**；P0 锁定即可，不阻 R1 |
| 6 | §4 `failure_paths` + §5 必读 | **通过** |
| 7 | `test_strategy: required` | **通过** |
| 8 | `HG-TASK-DRAFT` | **approved** — 已开 R1 |
| 9 | 禁止代填 `HG-AUDIT-R1`、禁止指示 30 在 pending 时开工 | **遵守** |

### 对照前置材料（摘要）

- **闸口 A**：`accepted` · `TECH_GRAPH_S1_FREEZE_20260514_V1_1_3` — task **NR-1** 禁止作主实验重跑。  
- **闸口 B**：`accepted` · `CTX_QUERY` 默认采纳 — task **NR-2** 禁止 `gate_ctx_b_v1` 全 arms 重跑；本 task **不推翻** B 结论（§1.1 P2）。  
- **materialize_gate_b_payloads.py**：子进程调用 `tech_graph_graph_query.py`、`query_seeds.json` 驱动 — 可作为 **臂 D** 实现参考，须新脚本 + 新 schema/arm 名，**勿**覆盖 B 产物目录。

---

## 需任务帽回填清单

**无**（零硬阻塞，不要求 R2 才能执行）。

可选（非阻塞）：**N-1** 修正 task 头部状态行与 `HG-TASK-DRAFT: approved` 一致。

---

## 是否建议执行帽开工

| 条件 | 建议 |
|------|------|
| **文档层（R1）** | **可进入执行帽**（零硬阻塞） |
| **人工闸** | **否** — 须人先将 task 表内 **`HG-AUDIT-R1`** 改为 `approved` 后，方可用下文「下一棒可复制 Prompt」开 **30** |
| **执行期闸** | P0 草案可在 **`HG-P0-PROTOCOL`** pending 下推进；**付费 batch（P1）** 须 **`HG-P0-PROTOCOL: approved`**（§5 必读第 5 条） |
| **分支** | 仅在 `task/engineering-tech-graph-gate-c-v2-dual-track-v1` 提交 |

---

## 签收 / 关闭

- **本轮（R1）**：**不声明 task 可结束**；task 仍为 `active`；**`HG-AUDIT-CLOSE`** 未设（关账用 **`HG-GATE-C-SIGNOFF`**）。  
- **R1 书面审查**：**通过（零硬阻塞）**；**不**代改 **`HG-AUDIT-R1`** 为 `approved`（由人阅本文后改 task 元信息表）。  
- **任务正式关闭条件（供终轮引用）**：§3 P0～P2 全勾选 + 结论 `accepted` + **`HG-GATE-C-SIGNOFF`** approved + 终轮审查 / CLOSE_TRACE（若适用）。

---

## 下一棒可复制 Prompt

以下与 **对话回复** 中「下一棒」块 **逐字一致**。使用前须完成：**人改** task **`HG-AUDIT-R1`** → `approved`。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）
- 子仓 AGENTS.md、task 内「给执行帽的必读」、根 AGENTS.md §8

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入（占位符已替换）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 子仓根：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md
- 关联 SPEC / 总规：
Projects/docs/tech_graph/改进方向.md
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-v2-dual-track-execute.md（元数据表 + 快照 fenced code）。
0b. 复读 task Harness 表：若 HG-AUDIT-R1 仍为 pending → 仅输出须人改的 gate_id 与路径，拒开工。
1. 通读 task：§0.3 臂 D/E、§1.2 NR-1/2、P0～P2、§4 failure_paths、§5 必读；gates_before_code 已齐。
2. test_strategy required：先增 pytest（manifest 路径存在、query 种子节点在 graph_v2、D 臂子图规模阈值），再实现 fixtures/gate_ctx_c_v1/ 与 materialize_gate_c_payloads.py。
3. P0：protocol_version.yaml（锁定 freeze_id、graph_v2_freeze_id 引用、token 上限）；dual_track_manifest.json（每题 .ai.md + .md，非整包）；query_seeds.json（ENV/U2/A2 等真值节点）；勿覆盖 gate_ctx_ab_v1 / gate_ctx_b_v1 历史 run。
4. 臂 D：参考 materialize_gate_b_payloads.py，arm/schema 改为 CTX_V2_QUERY / gate_ctx_c_*；臂 E：按 manifest 拼接双轨原文。
5. 禁止：重跑闸口 A/B 主 batch（FP-C-1）；HG-P0-PROTOCOL pending 时跑付费 batch；整仓 .ai.md 灌入 E 臂。
6. PR-1 目标：P0 materialize exit 0 + 上述 pytest 绿；跑 task §3.3 主链 pytest；回填 task「### 自检结论（执行者）」。
7. 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮路径；对话报 short-hash。

禁止：HG-AUDIT-R1 未 approved 时写业务代码；代填 human_gate；git add -A。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-18 | R1：零硬阻塞；HG-AUDIT-R1 待人签；附 30 执行 Prompt（须 HG-AUDIT-R1 approved 后使用） |
