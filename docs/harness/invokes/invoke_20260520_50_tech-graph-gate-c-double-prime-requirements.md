# Harness invoke snapshot · 闸口 C″ 立项（需求帽）

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| template | `Projects/docs/harness/prompts/TEMPLATE-requirements-invoke.md` §3 |
| task_paths | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md` |
| related_review_or_none | 无（初稿） |
| created_utc_or_local | 2026-05-20 CST |
| git_branch | `task/engineering-tech-graph-gate-c-double-prime-v1`（建议） |
| notes | **P0** 实验对比先行；**P1** rules 关账后置；**禁止** batch 前改 `10-tech-graph.mdc` |

## 可复制 Prompt 快照（10 · 需求与任务分析）

```text
你正在扮演工作区 Harness「需求与任务分析帽（10）」，严格遵循：
- Projects/docs/harness/prompts/10-requirements.md
- Projects/docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、freeze_id）
- 工作区 AGENTS.md §7（_tech_graph 双轨；实验不替代维护真值）

【产品优先级（本闸口 · 强制 · 覆盖一切泛泛「图谱大改」冲动）】

P0 — 实验对比先行（闸口 C″）：
  在 **graph_v2 + CTX_V2_QUERY 默认轨不变** 前提下，用 **最小可复现变量**（分题物化 / query 种子 / 切片策略）做 **D vs E** 新 batch，相对 **canonical 052803** 与 **C′ 083014** 量化 ΔF1/Δtoken。
  **胜出定义**：达到 task 内书面验收（见下「建议验收」）且 **不推翻** 闸口 C accepted「维持 CTX_V2_QUERY 默认」。

P1 — 关账后才改 Cursor rules（后置门闸 · 非本 task 开工条件）：
  仅当 C″ 结论 **accepted** 且写明「可升格为工程默认消费规约」时，才允许 PR 更新：
  - ai-ink-brain-api-python/.cursor/rules/10-tech-graph.mdc
  - （按需）docs/_tech_graph/graph_v2_schema.md 路径与 freeze 指针
  **禁止** 在 batch 跑完、结论未签收前改 rules（避免「方案未验证先写进规则」）。

P-禁止 — 暂不作为 C″ 主路径：
  - **全面**重写 graph 拓扑 / graph_v3 / 退役 *.ai.md / 整包 graph.json 或 15_e2e 灌 prompt
  - 「先大改 graph.json → 再与旧方案对比」
  - 升 CTX_DUAL_MD 为默认
  - 覆盖或改写 conclusion_gate_c_v2_dual_track_v1_zh.md / conclusion_gate_c_prime_f1_v1_zh.md 正文

【目标与上下文】

立项 **闸口 C″（gate_ctx_c_double_prime_v1）**：承接 C′ 结论 §4 follow-up。
- C′ 已解决 **T002** D impact（0.429→0.923），但 **T003** D impact 回落（0.400→0.222）；T001 基本持平。
- 根因假设：**分题物化缺失** + LLM 填 impacts 偏 ref 非 path，**非** 应改默认轨。
- 用户暂最优先：**用实验验证窄改进是否净收益**；净收益且签收后 **再** 把新消费规约写入 Cursor rules。

【已有材料路径（必读 · 相对 Projects/ 或子仓根）】

前置 task（done · 只读）：
- ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_prime_f1_v1.md
- ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_query_coverage_v1.md
- ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md

结论与基线 batch（只读）：
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/（canonical）
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014/（C′ 主 run）

协议 / 物化 / 评分（可扩展 · 不重写主实验历史目录）：
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/protocol_version.yaml
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/query_seeds.json
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json
- ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py

机器轨真值（对照 · 非手改源）：
- ai-ink-brain-api-python/docs/_tech_graph/graph.json（graph_v2 · freeze TECH_GRAPH_S2_FREEZE_20260519_V2_3）
- ai-ink-brain-api-python/.cursor/rules/10-tech-graph.mdc（**关账前只读**；列出拟变更 diff 清单即可）

规划 SPEC：
- Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
- Projects/docs/tech_graph/改进方向.md（R4 闸口分工；C″ 新增一行索引即可，非本 task 主交付）

【是否按任务审核文档回填】
无

【你必须完成】

0. **Invoke 快照**：将本消息全文落盘到
   ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_50_tech-graph-gate-c-double-prime-requirements.md
   （元数据表 + 本 fenced 快照；同会话追问不重复落盘）

1. 产出可落盘 task 正文（建议路径）：
   ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md
   命名：task_engineering_tech_graph_gate_c_double_prime_v1.md
   头部须含：状态 draft、test_strategy required、新 freeze_id（建议字面量
   TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0）、graph_v2_freeze_id 指针、git_branch 建议。

2. task 必须写清的结构（不可省略）：

   §0 背景：C″ 与 C/C′ 分工表；**P0 实验先行 / P1 rules 后置** 写进「架构决议」小节。

   §1 范围（建议 PR 切片）：
   - PR-1：**分题物化**（主变量 · 预期主攻 **T003**）
     · T003：Admin Ingest 域 manifest_slice + impact_surface（对齐 tasks.json gold path/kind）
     · T001：仅在有假设时加轻量切片；T002 **继承 C′ 物化**，避免重复争论
     · 可选：T003 query_seeds 微调（仍 graph_query；禁止整图）
     · materialize + pytest 扩展；bump protocol gate_c_double_prime_freeze_id
   - PR-2：token 守门（仅 PR-1 超限；裁 slice → depth → union）
   - PR-3：新 batch `gate_ctx_c_v1_batch_<YYYYMMDD>_*` + score_gold_f1
     · 臂：CTX_V2_QUERY vs CTX_DUAL_MD（与 C 同型）
     · 新结论：conclusion_gate_c_double_prime_v1_zh.md（**不**改 C/C′ accepted 正文）
   - PR-4（**条件 · 仅 HG 签收后**）：更新 10-tech-graph.mdc + 必要索引
     · 写明：从 C′ 物化策略 + C″ 验证结果 **提炼** 的 Agent 读取顺序/禁止项
     · **阻塞**：HG-GATE-C-DOUBLE-PRIME-SIGNOFF ≠ approved 时 **禁止** 合并 PR-4

   §1.2 非范围 NR：与 C′ NR-1～7 对齐；另增
     · NR-8：禁止「全面 graph 方案改进后再实验」作为主路径
     · NR-9：禁止未签收结论前改 .cursor/rules
     · NR-10：禁止 GraphRAG / 博客向量试点混入本闸口

   §2 建议验收（供 22/30 引用 · 可微调但须可量化）：
   - 主 KPI（OR）：**T003** D impact F1 ≥ 0.45，或相对 C′ 083014 的 T003 Δimpact ≥ +0.15
   - 守卫：T002 D impact 不得低于 C′ 083014 的 0.923−0.05（≥ 0.873）
   - entry：三题无单题下降 > 0.05；中位数 ≥ 0.80
   - token：D 臂中位数 ≤ max(canonical D×1.25, C′ D×1.25)；单题 < 8192
   - 产品：维持 CTX_V2_QUERY 默认；E 臂仅对照
   - rules 升格：仅当上述通过 + 结论 accepted → PR-4 清单勾选

   §3 failure_paths：物化失败、query 空子图、batch 失败、F1 不达标、误改历史 run 目录

   §4 human_gate 表：HG-TASK-DRAFT、HG-AUDIT-R1、HG-GATE-C-DOUBLE-PRIME-SIGNOFF（blocks PR-4 + done）

3. 输出 **下一棒 22 任务审核帽** 可复制 Prompt（TEMPLATE-task-audit-invoke），绑定上述 task 路径。

4. 禁止：写业务实现代码；改 CI；绝对本机路径；代填 human_gate approved。

5. 若用户已授权落盘 task：写入 active/ 后按 HANDOFF_AUTO_COMMIT 仅子仓 commit；报 short-hash。
```

## 产出索引（10 帽本轮）

| 产出 | 路径 |
| --- | --- |
| task 初稿 | `docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md` |
| 下一棒 22 Prompt | 见 task 修订记录或审查 md 末节（本轮对话已给出） |

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-20 | v1：C″ 需求帽 invoke 落盘；task active 初稿；实验先行 · rules 后置 |
