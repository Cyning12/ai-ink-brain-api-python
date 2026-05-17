# 治理层三相塌缩：Ink 技术图谱与 AI Coding 应用说明

| 项 | 内容 |
| --- | --- |
| **版本** | v0.1 |
| **日期** | 2026-05-17 |
| **定位** | 将 [`三相塌缩等价性论文_拓扑综合.md`](./三相塌缩等价性论文_拓扑综合.md) 的**可迁移思想**用于仓库 **AI coding 治理**；**不包含** Transformer / MoE / CIS 模型层改造 |
| **关联实验** | [`reports/conclusion_gate_ctx_ab_final_zh.md`](./reports/conclusion_gate_ctx_ab_final_zh.md)（闸口 A · `accepted`） |
| **关联 task** | [`docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md`](../../tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md) |
| **关联 SPEC 草案** | [`docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md`](../../../../docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md) |
| **符号表** | [`NOTATION_zh.md`](./NOTATION_zh.md) |

---

## 摘要

论文在**计算流形**上证明：贝叶斯传播（\(P\)）、频域截断（\(L_{\mathrm{norm}}\) 谱）、图谱划分（\(G_k\)）在 SBM 结构下可**等价塌缩**（ARI = 1），并推论 MoE Softmax 在 \(\tau \to 0\) 时退化为 **SelectEnd**（硬路由）。

本文说明：在**不修改 LLM Transformer** 的前提下，如何把同一思想落到 **Ink `docs/_tech_graph/` 机器轨**——用 **可验证等价 + 确定性子图查询** 抑制图谱漂移、压缩 Agent 上下文。结论与闸口 A 一致：**`graph_v1` 整包替代 `*.ai.md` 既不显著省 token，又损害 P1/P2**；改进方向是 **graph_v2 + graph_query（方案2）**，而非换文件格式 alone。

---

## 目录

1. [论文什么能借、什么应放弃](#1-论文什么能借什么应放弃)
2. [治理层「三相」与文件载体](#2-治理层三相与文件载体)
3. [轨道分层（人读 / 协议 / 机器 / 规范）](#3-轨道分层人读--协议--机器--规范)
4. [抗漂移与省 token 在治理层的含义](#4-抗漂移与省-token-在治理层的含义)
5. [与 gate_ctx_ab 的对照](#5-与-gate_ctx_ab-的对照)
6. [改进方向（不必换赛道）](#6-改进方向不必换赛道)
7. [论文适用范围与禁止外推](#7-论文适用范围与禁止外推)
8. [决策树与成功标准](#8-决策树与成功标准)
9. [相关路径索引](#9-相关路径索引)

---

## 1. 论文什么能借、什么应放弃

| 论文块 | 内容 | 治理层可迁移？ |
| --- | --- | --- |
| 引理 2.1 / 定理 2.2 | \(P\) 与 \(L_{\mathrm{norm}}\) 谱同构，\(\Phi(v)=D^{1/2}v\) | **精神**：多种表示须落在**同一图 \(G\)** 上，且划分/影响闭包一致 |
| 定理 4.1 | SBM 上 \(B_k,F_k,G_k\) 分区 ARI = 1 | **不直接外推**至 Ink flowchart；改为本仓**等价检查阈值**（拓扑 + 锚点 + 边标签） |
| 推论 4.2 | \(\tau\to0\)：Softmax → **SelectEnd** | **是**：`graph_query` 子图 + manifest 切片，非整包 Mermaid/JSON |
| §5 数值验证 | 4096×4096 **合成 SBM** | **不**当作 Ink 图已证 ARI=1；§7.3 自述未在真实预训练模型验证 |
| BLOCKER P1 | 同拓扑、不同度量（Z-order vs 欧氏） | **是**：JSON 字段序/分图 id/`path::symbol` 稳定化 |
| BLOCKER P3 | FFN 中层不完全塌缩 | **是**：治理层用 **输出 schema / Harness**，不单靠换格式 |
| §6 CIS | Z-order、回滚、MoE | **放弃**（改动与资源过大，非本专题范围） |

---

## 2. 治理层「三相」与文件载体

### 2.1 勿混淆：论文三相 ≠ 三种文件

| 论文「三相」 | 数学对象 | Ink **工程三相**（建议用语） |
| --- | --- | --- |
| **B** · 贝叶斯塌缩 | \( \pi P^k \)，概率质量集中 | **传播相**：依赖传播 / 影响闭包（`downstream` / `upstream`） |
| **F** · 频域塌缩 | Fiedler 低频子空间 | **约束相**：Env、规约、低通式「按需加载」`99_spec`、contract |
| **G** · 图谱塌缩 | 谱聚类 / 社区划分 | **结构相**：flow 拓扑、子图 id、manifest 端点/RPC 分区 |

**三种文件载体**（`*.ai.md`、`graph.json`、`_manifest.json`）是 **同一项目图 \(G\) 的不同序列化**，不是论文里的 B/F/G。它们之间须 **等价门禁**；`graph_v1` 已证为**有损投影**（非等价塌缩）。

### 2.2 对照图

```text
论文（同一 G 上三种算子）          Ink 治理（同一仓库真值图）
────────────────────────────────────────────────────────────
B_k  随机游走 / 影响传播    ≈   graph_query：k-hop 影响集（确定性，非 P^k 概率）
F_k  谱低通 / 截断          ≈   按需 99_spec / env / contract（不默认灌全文）
G_k  谱聚类 / 模块划分      ≈   分图 00_main、10_flow_* + manifest 分区

载体（须等价，非「三相」本身）：
  *.ai.md  ──export──►  graph.json(v2)     _manifest.json
         └─ 维护真值（短期）    └─ 机器轨      └─ 清单锚点
```

---

## 3. 轨道分层（人读 / 协议 / 机器 / 规范）

| 轨道 | 路径 | 读者 | 维护 |
| --- | --- | --- | --- |
| **人读轨** | `*.md`（`00_main`、`10_flow_*` 人读版等） | 人 | 人 + Agent |
| **协议轨** | `*.ai.md` | Agent、导出器 | 人 + Agent（**非**日常人扫读） |
| **机器轨 · 清单** | `_manifest.json`、`_contract_manifest.json` | Agent、CI | 脚本校验 + 人审 |
| **机器轨 · 拓扑** | `graph.json`（v1 → **v2**） | Agent、CI、query | **导出**，禁止手改 |
| **机器轨 · 消费** | `graph_query`（方案2，待建） | Agent | 代码 |
| **规范层（人机同读）** | `01_struct`、`02_version`、`99_spec`、`99_mermaid_protocol` | 人 + Agent（**按需**） | 人 + Agent |

**演进（机器轨 only）：**

```text
【旧】 manifest + contract + *.ai.md（整包消费）

【方案1·已交付】 + graph_v1（有损拓扑导出）

【目标】 manifest + contract + graph_v2 + graph_query
        （*.ai.md 短期仍为 export 源；退役见 G-END-4）
```

`01_struct` / `99_*` **不**纳入 v1 flow 导出是**设计边界**（表结构、Env 规约与流程拓扑正交），不是遗漏。

---

## 4. 抗漂移与省 token 在治理层的含义

### 4.1 「忽略漂移」在治理层的可操作定义

| 机制 | 作用 |
| --- | --- |
| `tech_graph_graph_export --check` | 拓扑相对 `.ai.md` 不 silent 偏离 |
| v2 **等价检查**（待建） | 锚点、边标签、分图与协议轨一致率达阈值 |
| `tech_graph_manifest_check` | 端点/RPC/表/锚点可解析 |
| `tech_graph_contract_check` | SSE 等契约不漂 |
| `freeze_id` | 实验与任务引用版本钉死 |

这是 **「仓库机器真值不漂」**，不是保证 LLM 永不幻觉。Agent 若默认 **query + manifest 切片**，起点比每次扫 **~20KB Mermaid 总串** 更一致。

### 4.2 「更省 token」如何实现

| 路径 | 评价 |
| --- | --- |
| v1 **整包** `graph.json` 替 `.ai.md` | **否**（闸口 A：主载荷 token ≈ 1:1；P1/P2 更差） |
| **graph_query** + manifest 相关切片 | **是（主路径）**；对应 SelectEnd，子图可能 **数量级** 小于整包 |
| v2 富化（锚点进 JSON） | **为少开 ai.md 片段**，不单为减字节 |
| 规范层全文进 prompt | **否**；按改表/Env/契约 **按需**读 `01_struct` / `99_spec` |

论文省的主要是 **推理时概率尾（Softmax）**；治理层省的是 **上下文装配体积**——机制不同，勿混谈。

### 4.3 Agent 推荐加载顺序（草案）

```text
1. graph_query(入口节点, depth)     ← 硬路由子图
2. _manifest / _contract 切片       ← 端点、锚点、契约
3. 按需 01_struct（改表）
4. 按需 99_spec（Env/约束）
5. 最后 10_flow_*.ai.md 片段        ← query 不足时
```

---

## 5. 与 gate_ctx_ab 的对照

| 维度 | 论文 | gate_ctx_ab（闸口 A） |
| --- | --- | --- |
| 场景 | SBM / MoE / CIS | Ink 三题：入口、影响、交接 |
| 主载荷对比 | — | CTX_JSON vs CTX_MERMAID（各 ~5k token 级） |
| 结论 | 推理可零温硬选 | **不签收**一律 JSON；P1/P2 偏 Mermaid；P3/P4 略偏 JSON |
| 未测 | — | **CTX_QUERY**（v2 + query）→ **闸口 B** |

论文 **支持** SelectEnd 式消费；**不支持** v1 整包 JSON 作为默认主载荷。

---

## 6. 改进方向（不必换赛道）

### 6.1 必做（与论文治理层对齐、不碰模型）

1. **graph_v2** + **等价检查**（拓扑 + 锚点 + 边标签）。  
2. **graph_query（方案2）** 为默认消费；规则禁止默认整包 v1。  
3. **分层加载**（§4.3）写入 task / `.cursor/rules`。  
4. **闸口 B**：`CTX_QUERY` vs 整包 Mermaid / 整包 v1。

### 6.2 可选

- manifest 与 graph `node_id` 互引；物化 JSON **稳定排序**（缓解 P1 式畸变）。  
- 任务单强制 `freeze_id`。

### 6.3 不建议（本阶段）

- 以论文 SBM **ARI=1** 作为 Ink 验收。  
- 为省 token 删除 `.ai.md`（闸口 B 前）。  
- 在 Ink 图上做谱聚类/Fiedler 模块发现（非刚需）。  
- 实现 CIS / Z-order / 改 MoE。

### 6.4 成功标准（旧 vs 新）

| 易误解（旧） | 可执行（新） |
| --- | --- |
| JSON 替代 Mermaid 省解析 | **query** 替代整包灌图省 token |
| 三相 = md / ai.md / json 三文件 | 三相 = **传播 / 结构 / 约束** 三种治理操作 |
| 论文 4096 证明适用于本仓 | 本仓自建等价阈值 + 闸口 B |

---

## 7. 论文适用范围与禁止外推

1. **定理 4.1 的 ARI=1** 在 **合成 SBM** 上成立；**不能**直接用于声明 `docs/_tech_graph` 的 `graph_v1` 与 `*.ai.md` 等价。  
2. **Mermaid / JSON / manifest** 不是论文 B/F/G；至多构成 **待测等价** 的多种载体。  
3. **不改 Transformer** 时，不声称实现「三相在隐空间塌缩」；只声称 **仓库边界上的确定性图消费**。  
4. **P3（中层）** 用 Harness、Rubric、`evidence[]` / `next_steps[]` 等补齐，不指望换 JSON 自动改善交付质量。  
5. **闸口 A 已否定**「生产默认仅 v1 JSON」；后续默认应是 **query + 可选 v2 片段**。

---

## 8. 决策树与成功标准

### 8.1 方向选择（总）

```text
目标是否为「仓库真值稳定 + Agent 少读废话」？
├─ 是 → 继续 tech_graph；核心 = v2 等价 + graph_query          【采纳】
└─ 否（要改模型推理）→ 论文 §6 CIS；已排除
```

### 8.2 已记录抉择（产品/架构 · 2026-05-17）

```text
是否接受「抗漂移 = CI + 版本 + 等价」，而非「LLM 永不犯错」？
├─ 是 → 治理层方案成立                                        【✓ 已选】
└─ 否 → 任何图谱都会失望；需改期望

token 主因是否放在「少读子图」而非「JSON 替 Mermaid」？
├─ 是 → 与 gate_ctx_ab、论文 SelectEnd 一致                     【✓ 已选】
└─ 否 → 会重复 v1 中间态别扭
```

| 抉择 | 含义（执行层） |
| --- | --- |
| **抗漂移 = CI+版本+等价** | 以 `export --check`、manifest/contract、v2 等价门禁、`freeze_id` 钉住**仓库机器真值**；不承诺模型零幻觉。 |
| **token 主因 = 少读子图** | 投入 **graph_query + 按需清单/规范层**；**不**以「用 JSON 整包替换 `.ai.md`」为默认策略。 |

### 8.3 关于「JSON 替换 Mermaid.ai.md」的结论（与 §8.2 一致）

在**同一次对话、主载荷信息量等价**的前提下：

- **JSON 与 Mermaid 对 LLM 理解/「记忆」的边际差异很小**（闸口 A 主载荷 token ~1% 级；质量差异主要来自 **v1 有损** 与 **是否整包灌入**，而非语法 JSON vs Mermaid）。
- 因此：**追求「用 JSON 替换 `.ai.md` 以提升理解/记忆」意义不大**；有意义的是：
  1. **机器轨**：CI 可 diff、确定性 query、与 manifest 分工；
  2. **消费轨**：**读得更少**（子图），不是 **换一种格式读同样多**。
- **例外（仍值得做 JSON，但不是「替 ai.md」）**：导出物给 **脚本/query/CI** 用；v2 富化后 **query 结果自足**，减少再打开 `.ai.md` 片段。维护真值短期仍可留在 `.ai.md`，或由 v2 反渲染只读图给人 PR 看。

**一句话**：把三相塌缩用于 AI coding 治理 = **固定项目图 \(G\) + 可验证等价 + SelectEnd 式上下文（query + 清单）**；与 `tech_graph` 方向一致；**已放弃**「整包 JSON 替 `.ai.md` 以改善 LLM 理解」作为主目标。

---

## 8A. 本方案与「Agent 长期记忆」的关系（FAQ）

**问：参照的方案（tech_graph、graph.json、graph_query、manifest）是否在做 Agent 长期记忆？**

**答：主要是「单次/多轮会话内的外部真值与上下文装配」，不是模型权重意义上的长期记忆；与常见「记忆产品」部分重叠但目标不同。**

| 维度 | 本方案（治理层 tech_graph） | 典型「Agent 长期记忆」 |
| --- | --- | --- |
| **存什么** | 仓库内 **可版本化** 的图、清单、契约、规范（Git + CI） | 用户偏好、历史对话摘要、向量库里的 episodic memory |
| **解决什么** | **图谱相对代码的漂移**；影响分析时 **少读、读准** | 跨天/跨任务 **记住用户说过什么** |
| **谁真值** | `docs/_tech_graph/` + 脚本门禁 | 记忆服务 / DB / 摘要 pipeline |
| **与 token** | 当轮 prompt **裁剪**（query 子图） | 检索后 **注入** 历史片段 |
| **与 gate_ctx_ab S1/S2** | β 摘要仍可能 **膨胀**（段·S1/S2）；图谱只优化 **α 主载荷**，不自动解决 **对话历史记忆** | — |

```text
         ┌─────────────────────────────────────┐
         │  Git 仓库：_tech_graph（慢变真值）   │
         │  CI 抗漂移 · freeze_id             │
         └──────────────┬──────────────────────┘
                        │ query / manifest 切片
                        ▼
         ┌─────────────────────────────────────┐
         │  当轮 Agent 上下文（快变、可裁剪）  │  ← 本方案主战场
         └──────────────┬──────────────────────┘
                        │ 可选叠加
                        ▼
         ┌─────────────────────────────────────┐
         │  会话摘要 / 向量记忆（S1/S2 β 等）   │  ← 另线；非 graph_v1 能单独解决
         └─────────────────────────────────────┘
```

若要做 **跨会话长期记忆**，应在 **摘要策略、记忆存储、检索** 上单独立项；**graph_query** 可与之间接配合（例如只把「与当前改动节点相关的子图」写入记忆索引），但 **不能替代** 记忆层设计。

---

## 9. 相关路径索引

| 类型 | 路径 |
| --- | --- |
| 论文（本目录） | [`三相塌缩等价性论文_拓扑综合.md`](./三相塌缩等价性论文_拓扑综合.md) |
| 实验定稿 | [`reports/conclusion_gate_ctx_ab_final_zh.md`](./reports/conclusion_gate_ctx_ab_final_zh.md) |
| 实验日志 | [`EXPERIMENT_LOG.md`](./EXPERIMENT_LOG.md) |
| Task v2+query | [`docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md`](../../tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md) |
| 机器轨架构草案 | [`docs/tech_graph/spec/.../machine_track_architecture_draft_zh.md`](../../../../docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md) |
| 图谱真值 | `docs/_tech_graph/` |
| 改进方向（工作区） | `docs/tech_graph/改进方向.md` |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-17 | 初稿：治理层应用说明，与论文同目录落盘 |
| v0.2 | 2026-05-17 | §8.2 抉择回填；§8.3 JSON 替 ai.md 结论；§8A 长期记忆 FAQ |
