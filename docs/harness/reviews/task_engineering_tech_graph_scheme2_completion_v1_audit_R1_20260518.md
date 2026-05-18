# 任务审核：技术图谱 — 方案2 补全（scheme2 completion）

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md`（**v0.2**） |
| **关联 SPEC / 总规** | `Projects/docs/tech_graph/改进方向.md`（§方案2 · §2.3～2.7）；`Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| **轮次** | **R1**（首轮） |
| **审查日期** | 2026-05-18 |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_22_tech-graph-scheme2-completion-audit-r1.md` |
| **需求帽 invoke** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_10_tech-graph-scheme2-completion-requirements.md` |
| **对照规约** | `docs/harness/prompts/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5、`HANDOFF_SEMI_AUTO.md` |
| **git_branch** | `task/engineering-tech-graph-scheme2-completion-v1` |
| **audit_profile** | `post_close` |
| **前置 task（done）** | `task_engineering_tech_graph_v2_graph_query_v1.md` · `task_engineering_tech_graph_v2_p4_bc_followup_v1.md` |

---

## 审查结论摘要

task **v0.2** 与前置 **graph_query** 交付物、闸口 B 定稿、Harness §5 字段 **整体对齐**；§0.4 矛盾裁定（C-1～C-5）与 §1.2 非范围 **无互斥**；§0.5 对 `has_path` / `describe_impact` 的锁定与现有 `tech_graph_graph_query.py`（`_bfs_reachable`、`EXIT_FP4`/`EXIT_FP5`、`ref` 边跳过）**可落地**；§3 验收与 §4 `failure_paths` **可观测、可命令断言**；`test_strategy: required` 在头部 `test_strategy_note` 与 §5.6 **明确先测后实现**。

**本轮结论**：**零硬阻塞**（无需任务帽回填后再 R2）。**不**代填 `HG-TASK-DRAFT` / `HG-AUDIT-R1`。执行帽 **须待人** 将两闸改为 `approved` 后方可开工（见下文）。

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **人工闸（非文档阻塞）** | HG-1 | `HG-TASK-DRAFT`、`HG-AUDIT-R1` 均为 `pending`；按 `HANDOFF_SEMI_AUTO` §2.3，**30 拒开工**直至人改 `approved` |
| **非阻塞（执行前宜遵守）** | N-1 | S2-B 改 **工作区** `Projects/docs/tech_graph/` 与子仓代码宜 **同 PR 或双 PR 链式**；task §5.4 已写，执行帽在自检/PR 描述中写明关系即可 |
| **非阻塞（执行期澄清）** | N-2 | `describe_impact` 人类可读串的 **最小字段**（id / label / 方向词）未在 task 逐字规定；§0.5 + §3.1 子串断言已够执行，若 CLOSE 争议可回填 §6 样例 |
| **非阻塞（S2-C）** | N-3 | MCP / Harness 模板挂钩为 **recommended**；未做不阻 R1/开工，关账须 §3.4 + §6 写明顺延理由 |
| **非阻塞（Harness）** | N-4 | `FP-S2-3`（文档宣称 MCP 无入口）主要约束 **关账**；PR-1 不阻 |
| **已核对通过** | ✓-1 | §0.4 C-1～C-5 可执行且与 §1.2（NR-1、NR-重命名、NR-union、Neo4j、schema、workflow、`.ai.md`）一致 |
| **已核对通过** | ✓-2 | §0.5 `has_path` 复用 `store.downstream` + `_bfs_reachable`；`get_all_affected` 明确非本模块（C-5 + `tech_graph_gate_b_query_union.py`） |
| **已核对通过** | ✓-3 | §3.3 命令化回归与根 `AGENTS.md` §8 后端 pytest 一致 |
| **已核对通过** | ✓-4 | §4 FP-S2-5/6 对齐现模块 FP-4/FP-5；FP-S2-2 + NR-1 覆盖闸口 batch 误用 |
| **已核对通过** | ✓-5 | 禁止项（闸口 B 重跑、Neo4j、schema 语义变更、改 workflow、重命名模块）均在 §1.2 / §5 写明 |

### R1 重点核对清单（逐项）

| # | 核对项 | 结论 |
|---|--------|------|
| 1 | §0.4 C-1～C-5 vs §1.2 | **通过**。例：C-1 保持 `tech_graph_graph_query.py` ↔ NR-重命名；C-5 ↔ NR-union；C-4 ↔ S2-C recommended、不改母版硬阻塞 |
| 2 | §0.5 锁定与 `get_all_affected` 非范围 | **通过**。实现真值已有 `_bfs_reachable`、邻接构建跳过 `ref`；并集由 P2-4 done 模块承担 |
| 3 | §3 可观测 + `test_strategy: required` | **通过**。§3.1～3.3 可 pytest/CLI/脚本断言；`test_strategy_note` + §5.6 要求先红测 |
| 4 | §4 FP-4/FP-5 与 scope | **通过**。FP-S2-5/6 映射 FP-4/5；FP-S2-2 拒 batch（NR-1） |
| 5 | `HG-TASK-DRAFT` pending 时不指示 30 开工 | **遵守**。本节仅书面 R1，不代签人工闸 |
| 6 | 禁止项 | **通过**。task 未扩 scope 至闸口实验 / Neo4j / 退役 `.ai.md` / workflow |

### 对照代码与 SPEC（摘要）

- `tools/tech_graph_graph_query.py`：已声明 `EXIT_FP4`/`EXIT_FP5`，`GraphQueryStore` 构建时跳过 `ref`，`test_tech_graph_graph_query.py` 含 FP-4/FP-5 与 CLI 冒烟模式 — 与 task §0.5、§4 一致。
- `scheme_2_graph_query.md` §「待需求方补充」与 `改进方向.md` §2.3 仍写 `graph_query.py` / 规划函数名 — **属 S2-B 必做范围**，非 R1 硬缺口。
- 闸口 B：`conclusion_gate_b_ctx_query_v1_zh.md` 路径已在 task 链出，**引用不重跑** — 与 §0.2、NR-1 一致。

---

## 需任务帽回填清单

**无**（零硬阻塞，不要求 R2 才能执行）。

---

## 是否建议执行帽开工

| 条件 | 建议 |
|------|------|
| **文档层（R1）** | **可进入执行帽**（零硬阻塞） |
| **人工闸** | **否** — 须人先将 task 表内 **`HG-TASK-DRAFT`**、**`HG-AUDIT-R1`** 改为 `approved` 后，方可用下文「下一棒可复制 Prompt」开 **30** |
| **分支** | 仅在 `task/engineering-tech-graph-scheme2-completion-v1` 提交实现 |

---

## 签收 / 关闭

- **本轮（R1）**：**不声明 task 可结束**；task 仍为 `active`；`HG-AUDIT-CLOSE` 仍 `pending`。
- **R1 书面审查**：**通过（零硬阻塞）**；**不**代改 `HG-AUDIT-R1` 为 `approved`（由人阅本文后改 task 元信息表）。
- **任务正式关闭条件（供终轮引用）**：§3 全勾选 + §3.3 回归绿 + S2-B 文档对齐 +（S2-C 完成或顺延理由）+ 终轮 **HG-AUDIT-CLOSE** + CLOSE 审查签收。

---

## 下一棒可复制 Prompt

以下与 **对话回复** 中「下一棒」块 **逐字一致**。使用前须完成：**人改** task `HG-TASK-DRAFT`、`HG-AUDIT-R1` → `approved`。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）
- 子仓 AGENTS.md、task 内「给执行帽的必读」、根 AGENTS.md §8

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-scheme2-completion-v1

输入（占位符已替换）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md
- 子仓根：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md
- 关联 SPEC / 总规：
Projects/docs/tech_graph/改进方向.md
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_30_tech-graph-scheme2-completion-execute.md（元数据表 + 快照 fenced code）。
0b. 复读 task Harness 表：若 HG-TASK-DRAFT 或 HG-AUDIT-R1 仍为 pending → 仅输出须人改的 gate_id 与路径，拒开工。
1. 通读 task：gates_before_code、§0.4～0.5、§1 范围/非范围（NR-1、禁止重跑闸口 B batch、禁止 Neo4j/schema/workflow/重命名）、§3 验收、§4 failure_paths、§5 必读。
2. test_strategy required：先在 tests/test_tech_graph_graph_query.py 为 has_path、describe_impact 写可失败用例，再实现 tools/tech_graph_graph_query.py + CLI（has-path、describe-impact）；禁止只实现后补测。
3. S2-A：has_path 复用 _bfs_reachable/downstream；未知节点 FP-4；describe_impact 组合 query_downstream/upstream 格式化为 str（非裸 JSON 替代）。
4. S2-B：更新工作区 scheme_2_graph_query.md、改进方向.md §2.3～2.7、子仓 docs/_tech_graph/graph_v2_schema.md §9 工具表；与 §2.1 映射表一致。
5. S2-C（recommended）：C1 MCP 示例或 C2 Harness 模板可选步骤二选一；未做须在 §6/CLOSE 写顺延理由。
6. 禁止：run_gate_b_batch 全 arms；改 .github/workflows；graph_v2 schema 语义变更；tech_graph_graph_query.py 重命名为 graph_query.py。
7. 跑 task §3.3：tech_graph_graph_export.py --check、tech_graph_graph_equivalence_check.py、上述 pytest；回填 task「### 自检结论（执行者）」。
8. 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮路径；对话报 short-hash。

禁止：HG 未 approved 时写业务代码；默认整包 v1 作 query；扩 scope 到闸口实验 / Neo4j / 退役 .ai.md。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-18 | R1：零硬阻塞；HG 待人签；附 30 执行 Prompt（须 HG approved 后使用） |
