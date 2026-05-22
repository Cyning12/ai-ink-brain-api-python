# 任务审核：闸口 D — `gate_ctx_ab_v2` 题集扩域（v2 五题）

## 元信息

| 项 | 内容 |
| --- | --- |
| **关联 task** | [`docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md`](../../tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md) |
| **轮次** | R1 |
| **审查日期** | 2026-05-20 |
| **invoke_snapshot** | [`docs/harness/invokes/invoke_20260520_22_tech-graph-gate-d-v2-tasks-audit-r1.md`](../invokes/invoke_20260520_22_tech-graph-gate-d-v2-tasks-audit-r1.md) |
| **需求帽 invoke** | [`docs/harness/invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md`](../invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md) |
| **对照 task（done）** | [`docs/tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md`](../../tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md) |
| **对照规约** | `Projects/docs/harness/prompts/22-task-audit.md`、`Projects/docs/harness/HARNESS_V2_PLAN.md` §5 |
| **git_branch / worktree** | `task/engineering-tech-graph-gate-d-v2-tasks-v1` · `ai-ink-brain-api-python-wt-gate-d-v2` |

---

## 审查结论摘要

对照 **10 帽 invoke**、**C″ done task**、方法论 **§6.1 / §7** 与草案 `draft_gate_ctx_ab_v2_expansion_v1.md`，本 task 在 **Harness §5** 字段（`test_strategy: required`、`failure_paths` 八条、`gates_before_code`、`freeze_id` 占位、`audit_profile: post_close`）上 **齐备且可操作**；**NR-1～NR-8** 与 **FP-GD1～GD8** 互锁，能约束历史 run 与 C 系结论文；**表 1** 回归基线与 run `102810` 的 `gold_f1.json`（D 臂 `CTX_V2_QUERY`）**数值一致**。

**结论**：**零硬阻塞**；**不建议** 交 **10 帽** 强制回填。建议维护者将 **HG-TASK-DRAFT**、**HG-AUDIT-R1** 由 `pending` 改为 **`approved`** 后，再开 **30 执行帽**（仍须满足 `HANDOFF_SEMI_AUTO.md` · 禁止 Agent 代签）。

---

## 专项核对

### §7 矛盾裁定（22 帽确认 / 可维持）

| 矛盾 | 本 task 裁定 | R1 意见 |
| --- | --- | --- |
| `gate_ctx_ab_v2` 目录名 vs `gate_ctx_c_v1` 脚本/协议 | **ab_v2** 仅 `tasks.json`；协议/batch **沿用** `gate_ctx_c_v1`，以 `gate_d_v2_tasks_freeze_id` 区分 | **维持**。与现仓 `protocol_version.yaml` 的 `tasks_ref`、物化/batch 脚本落点一致；避免复制 B/C 整棵 fixture 树。 |
| 草案「新建整套 `fixtures/gate_ctx_ab_v2/`」vs 单文件 | **最小**：`ab_v2/tasks.json` + 扩展 c_v1 侧车 | **维持**。与 C″「增量配置、不重斗整树」纪律同型。 |
| 路线图 M2 路径 vs 治理仓真值 | 治理仓 `methodology/graph/` 为准；SPEC 用 `Projects/docs/tech_graph/SPEC/…` | **维持**。task 头部依赖链已双写，无执行歧义。 |

**建议（非阻塞）**：§7 表末「待 22 帽可改」可在关账前改为「R1 已确认（2026-05-20）」，避免后续 Agent 误改裁定。

### T004 / T005 gold 可测性

| 检查项 | 结果 |
| --- | --- |
| 方法论 §7 要点是否落入 task | **是**（§2.2 入口/影响面/E 臂/物化模式；§1.1 PR-1 约束） |
| 量化验收 | **是**（§3.1：各题 ≥3 entrypoints、≥3 impacts；PR-3 表 2 KPI） |
| 核验纪律 | **是**（FP-GD2；§2.2「rg + graph.json 节点 id」；禁止整包 `15_e2e`） |
| `test_strategy: required` 可失败自动化 | **是**（物化 pytest、schema、种子节点 ∈ `graph_v2`；全仓 pytest 命令明示） |
| batch 可扩展性 | **可执行**（task §5 要求扩展 `run_gate_c_batch.py` 题列表或读 `ab_v2/tasks.json`；当前脚本硬编码三题为 **已知实现债**，属 30 帽范围，**非** R1 拒审理由） |

**非阻塞缺口**：表 2 备选 KPI「相对 **无题专属物化** 基线 Δ ≥ +0.15」未定义 **基线采集命令/目录**（仅写「执行帽记录」）。建议在 **结论文模板** 或 §3.2 增一句：基线 = 关闭 T004/T005 专属 `manifest_slice`/`impact_surface` 的 D 臂物化（或一次性 ablation run），并写入 `conclusion_gate_d_ctx_v2_tasks_v1_zh.md` 表 2 脚注；**不阻塞** PR-1/PR-3 开工。

### 表 1 / 表 2 / token 阈值

| 表 / 指标 | task 约定 | R1 核对 |
| --- | --- | --- |
| **表 1**（v1 回归 vs `102810`） | T001～T003 D 臂 impact F1 单题下降 ≤ **0.10** | 基线 **已核对** `runs/gate_ctx_c_v1_batch_20260518_102810/gold_f1.json`：T001 impact **0.200**、entry **0.857**；T002 impact **0.800**、entry **0.923**；T003 impact **0.857**、entry **0.923**。与 §2.1 表一致。 |
| **表 1 可调** | HG-TASK-DRAFT 可调 | **合理**；与 C″ 同类表述一致。 |
| **表 2**（v2 扩展） | T004 **或** T005：impact F1 ≥ **0.45** **或** Δ ≥ **+0.15** | 与方法论 §6.1 验收草案 **一致**；「至少 1 题」可观测。 |
| **表 3** | D vs E token 中位数 + F1 | 与 C 系报告结构 **一致**；非 R1 缺口。 |
| **token** | 单题 < **8192**；五题 D 中位数 ≤ **max(601, C″×1.25)** ≈ **701** | C″ `materialize_report.json` 记录 D 中位数 **561** → 门槛 **701** **算术正确**；与 `protocol_version.yaml` `payload_limits` **对齐**。 |
| **entry F1 回归** | 未列入 §3.2 表 1 | **非阻塞**：C″ 主 KPI 亦为 impact；若产品要强守 entry，可由人签时写入 HG-TASK-DRAFT 说明。 |

### NR-1～NR-8

| ID | R1 |
| --- | --- |
| NR-1 | 与 FP-GD6、C 系 accepted 只读 **一致** |
| NR-2 | 与 FP-GD1、§5 必读第 6 条 **一致**；历史路径在仓内 **存在** |
| NR-3 | 与 FP-GD6 **一致** |
| NR-4 | 与 FP-GD5、§0.3 P0 **一致** |
| NR-5 | 与路线图阶段 D 边界 **一致** |
| NR-6 | 与 §0.3、T004 E 臂约束 **一致** |
| NR-7 | 与方法论 §5 禁止叙事、表 1/2 分表 **一致** |
| NR-8 | 与范围「仅实验题集 + 物化」 **一致** |

### `human_gate` 表

| human_gate_id | blocks_hats | R1 |
| --- | --- | --- |
| **HG-TASK-DRAFT** | `22-R1`, `30` | 表结构符合 `HANDOFF_SEMI_AUTO.md` §2。本轮 R1 由用户 **显式开帽**；**不** 代填 `approved`。执行前建议人扫 §3 阈值与 NR 后批准。 |
| **HG-AUDIT-R1** | `30` | R1 书面结论：**零硬阻塞**。人签后 30 可开工。 |
| **HG-GATE-D-SIGNOFF** | `50`, `done` | 关账闸；与 `post_close` 终轮一致，**不在** 本轮声明关闭。 |

**注意**：task 头部 `HG-TASK-DRAFT` 含 `22-R1` 时，纪律上初稿应先人审；本次审查不否定已产出的 R1 文档，但 **30 仍须双闸 approved**。

---

## 阻塞 / 非阻塞

| 类型 | 说明 |
| --- | --- |
| **硬阻塞** | **无** |
| **非阻塞（可选 · 10 或 30）** | （1）§3.2 或结论文模板补 **「无专属物化」基线** 操作定义一行。（2）§7 标注 R1 已确认裁定。（3）表 1 是否守卫 entry F1 由人签择一。（4）`run_gate_c_batch.py` / `score_gold_f1.py` 的 `--tasks` 在 PR-3 切至 `gate_ctx_ab_v2/tasks.json`（task §5 已暗示）。 |

---

## 需任务帽回填清单

**无**（零硬阻塞，不触发 10 帽强制回填）。

---

## 是否建议执行帽开工

**建议 30 开工**，前提：

1. **HG-TASK-DRAFT** = `approved`  
2. **HG-AUDIT-R1** = `approved`（本 R1 供人签依据）  
3. cwd = **`ai-ink-brain-api-python-wt-gate-d-v2`**，分支 = **`task/engineering-tech-graph-gate-d-v2-tasks-v1`**  
4. **禁止** 覆盖 `052803` / `083014` / `102810`；**禁止** 改 C 系 accepted 结论文  

---

## 签收 / 关闭

- **本轮（R1）**：**不声明 task 可结束**（`audit_profile: post_close`；PR-1～PR-3 与 **HG-GATE-D-SIGNOFF** 未满足）。  
- **任务正式关闭条件（供终轮）**：§3 验收全勾、`conclusion_gate_d_ctx_v2_tasks_v1_zh.md` **accepted**、**HG-GATE-D-SIGNOFF** + 终轮 **HG-AUDIT-CLOSE**（若 task 后续增补）人签、`docs/tasks/done/` 归档。

---

## 下一棒可复制 Prompt

以下与对话 **下一棒** 块逐字一致（`TEMPLATE-execute-invoke.md` §3，占位符已替换）。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8（合并前必绿命令真值，若与本条 VERIFY 冲突以 task + 子仓 workflow 为准）

输入（已由人工替换占位符；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致，见 docs/harness/README.md「并行分支与 Git worktree」）：
ai-ink-brain-api-python-wt-gate-d-v2
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_d_v2_tasks_v1_audit_R1_20260520.md
- 关联 SPEC / 总规（无则「无」）：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 `human_gate`（见 docs/harness/prompts/HANDOFF_SEMI_AUTO.md）。若任一对 **本帽（30）** 为 `pending` → 仅输出须人改的 `gate_id` 与路径，**拒开工**；禁止代填 `approved`。
1. 通读 task 全文：头部 `gates_before_code`、`audit_profile`、`semi_auto`、`test_strategy` / `test_strategy_note`、`freeze_id`、`failure_paths`、拒开工条件、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足（缺 failure_paths 可操作性、缺验收命令、必读未覆盖等）→ **仅输出 Markdown 阻塞清单**（缺什么、建议回填的小节标题、推荐下一棒角色），**不写**业务实现代码。
3. `test_strategy: required` 时：先增加或调整 **可失败** 的自动化测试（或与实现同 PR 且满足 task 所述 red-green / 可复现失败语义），再改实现；禁止「只写实现、后补测」绕过 task 约定。
4. 在 `ai-ink-brain-api-python-wt-gate-d-v2` 内按 task 范围改代码/配置（**禁止**在并行另一 worktree/checkout 改同一子仓）；禁止静默扩大 scope；SPEC/task 矛盾走变更请求或交回需求帽，不擅自调和为代码假设。
5. 在 `ai-ink-brain-api-python-wt-gate-d-v2` 执行 `pytest tests -m "not intent_eval and not intent_benchmark"`（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 `40-self-check.md` 将结论与命令摘要 **回填** 至 task 正文 **`### 自检结论（执行者）`**（无则新增该小节）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 docs/harness/prompts/HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
9. **半自动下一棒（可选）**：若 task `semi_auto: true` 且下一棒（如 40）无 `human_gate` 阻塞：先将 **下一棒 §3 全文** 落盘新 invoke 并 commit，再切换角色执行；规则见 HANDOFF_SEMI_AUTO.md §3。否则仅输出下一棒 Prompt 供人开新会话。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出；覆盖 runs/gate_ctx_c_v1_batch_20260518_052803、083014、102810。
```

**开 30 前请确认**：task 内 **HG-TASK-DRAFT**、**HG-AUDIT-R1** 已为 `approved`（仅人改）。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-20 | R1：零硬阻塞；§7 维持；表 1 基线核对 102810；建议人签后 30 |
