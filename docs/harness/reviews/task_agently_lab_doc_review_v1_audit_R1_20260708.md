# Task 审核 · Agently Lab 文档审查（D1–D10）· R1

| 项 | 内容 |
| --- | --- |
| **task_path** | `docs/harness/tasks/active/task_agently_lab_doc_review_v1.md` |
| **spec_path** | `docs/harness/guides/RUNTIME_agently_parallel_learning_track_v0_zh.md` |
| **master_dispatch** | `docs/harness/invokes/by-task/parallel-tracks-orchestration/DISPATCH_parallel_tracks_master_v1_zh.md` |
| **audit_round** | `R1` |
| **review_date** | `2026-07-08` |
| **audit_profile** | `full` |
| **invoke_snapshot** | `docs/harness/invokes/by-task/agently-lab-doc-review/invoke_20260708_0000_22_agently_lab_doc_review_v1.md` |
| **prev_review_path** | `无` |
| **hat_self** | `pass-with-notes` |

---

## 审查结论摘要

本 task 作为 Agently 并行学习轨 **线 A** 的首个完整 lab，已按 HARNESS_V2_PLAN §5 补齐关键元信息：

- `test_strategy: required` + `test_strategy_note` 说明 import/auth/结构化输出三条测试红线；
- `failure_paths` 7 条覆盖配置、import 边界、路径白名单、schema、auth、线上 FS 依赖、repo root 缺失；
- `human_gate` / `orchestration` / `audit_profile` / `experience_capture` / `kpi_rubric` / `kpi_aggregator` 均已声明；
- 验收标准 D1–D10 按 RUNTIME 总规 §8 的 2 周冲刺日历展开，M1/M2/M3 里程碑可观测。

结论：**task 内容无硬阻塞，可进入执行帽；但 `HG-TASK-DRAFT` 仍 `pending`，须维护者人签 `approved` 后 30 方可开工。** 本帽不代签。

---

## 对照 HARNESS_V2_PLAN §5 检查项

| 字段 | task 状态 | 检查结论 |
| --- | --- | --- |
| `test_strategy` | `required` | 符合 §5.1；note 解释 import 边界、auth、结构化输出三处必须机械测试 |
| `test_strategy_note` | 存在 | 符合 §5.1；明确 red-green 顺序要求 |
| `failure_paths` | 7 条 | 符合 §5.3；含触发条件、系统行为、可观测、是否可重试 |
| `audit_profile` | `full` | 符合 §5.5 |
| `orchestration` | `epic: parallel-tracks-orchestration · parallel_group: A · depends_on: —` | 符合 §5.6 / Master Dispatch |
| `human_gate` | `HG-TASK-DRAFT` `pending` `blocks_hats: 30` | 符合 §5.6；本帽遇 pending 不代签 |
| `experience_capture` | `required` | 符合 §5.7；task 末尾已提示知识沉淀重点 |
| `kpi_rubric` | `KPI_RUBRIC_v1_2` | 符合 §5.8 |
| `kpi_aggregator` | `CLOSE` | 符合 §5.8（默认值显式写出） |
| `### KPI（00）` | 存在 | 符合 §5.8；关账前须按 rubric 汇总 |
| 验收标准可观测性 | D1–D10 每条含命令/状态/产物 | 符合 §0.2 / §3 执行帽要求 |
| `gates_before_code` | 未显式声明（默认隐式 `true`） | 无冲突；失败路径与必读列表已齐备 |

---

## 阻塞 / 非阻塞

### 阻塞项

**无。**

### 非阻塞建议（任务帽可在开工前回填，也可由 30 执行帽顺手补）

1. **回填 `audit_review_path`**：task「执行帽必读列表」第 6 条要求将 R1 审查路径回填到 `audit_review_path`，但 task 头部元信息表无此字段。建议 10-task 在头部元信息新增一行 `audit_review_path`，填入本审查文档路径，方便 30 自检。
2. **引用 `freeze_id`**：Master Dispatch 冻结点为 `PARALLEL-TRACKS-ORCH-V1`，task 头部 `freeze_id` 可选但当前为空。建议回填，便于 D7–D10 BFF/线上阶段与总规版本对齐。
3. **D8 降级条件具体化**：「未就绪则降级为 paste 模式」建议明确触发器（如 `AGENTLY_LAB_GITHUB_TOKEN` 缺失 / GitHub API 非 200 / rate limit），可与 failure_paths 新增 `F8` 或并入 `F4/F7` 的可观测描述。
4. **D10 试审对象**：可预先指定一份低风险 task（如本 task 自身或某份已关闭 task）作为线上首审样本，避免执行帽临时挑选。

---

## 需任务帽回填清单

- [ ] （建议）头部元信息新增 `audit_review_path: ai-ink-brain-api-python-wt-agently-lab/docs/harness/reviews/task_agently_lab_doc_review_v1_audit_R1_20260708.md`
- [ ] （建议）头部元信息新增 `freeze_id: PARALLEL-TRACKS-ORCH-V1`
- [ ] （可选）D8 补充降级触发器说明或新增 failure path
- [ ] （可选）D10 指定线上首审目标 task

> 以上均为 **建议项**；即使不回填，30 仍可开工。若维护者要求严格闭合，则回填后触发 **R2** 复审。

---

## 是否建议执行帽开工

**建议开工，但受 `HG-TASK-DRAFT` pending 阻塞。**

本帽结论 task 内容已达执行条件；下一棒为 30 执行帽。依据 HARNESS_V2_PLAN §5.6 与 Master Dispatch §3.2，`HG-TASK-DRAFT` 状态 `pending` 时 30 必须 **拒开工**。因此下一棒 Prompt 已准备，但须维护者将 `HG-TASK-DRAFT` 改 `approved` 后方可粘贴给 30。

---

## 签收 / 关闭

- **本轮状态**：R1 书面审通过（`pass-with-notes`）。
- **是否可关闭 task**：否；待 30→40→CI→50/CLOSE 链跑完。
- **task 状态**：维持 `active`。
- **人工闸**：`HG-TASK-DRAFT` 须人签 `approved`；`HG-AUDIT-R1` 可设 pending 待人签（由维护者决定是否在本轮追加）。

---

## 下一棒可复制 Prompt

待 `HG-TASK-DRAFT` 维护者改 `approved` 后，复制下文粘贴给 30 执行帽：

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8

输入（占位符已全部替换；若你看到 {{…}} 或「待填」须先追问，不得开工）：
- 主 task 路径（相对工作区根 Projects/）：
docs/harness/tasks/active/task_agently_lab_doc_review_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python-wt-agently-lab
- Worktree 研发目录（所有 git/pytest 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致）：
ai-ink-brain-api-python-wt-agently-lab
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests/agently_lab -m "not agently_lab_online"
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python-wt-agently-lab/docs/harness/reviews/task_agently_lab_doc_review_v1_audit_R1_20260708.md
- 关联 SPEC / 总规（无则「无」）：
docs/harness/guides/RUNTIME_agently_parallel_learning_track_v0_zh.md

你必须完成：
0. Invoke 快照（开帽起点）：在输出实质性结果之前，先将本用户消息全文按 docs/harness/invokes/README.md 落盘到 ai-ink-brain-api-python-wt-agently-lab/docs/harness/invokes/by-task/agently-lab-doc-review/invoke_20260708_0000_30_agently_lab_doc_review_v1.md（含元数据表 + 快照 fenced code）。同一会话追问不再新增快照文件。
0b. 人工闸：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、test_strategy / test_strategy_note、failure_paths、拒开工条件、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足 → 仅输出 Markdown 阻塞清单，不写业务实现代码。
3. test_strategy: required 时：先增加或调整可失败的自动化测试（或同 PR 满足 red-green 语义），再改实现；禁止只写实现、后补测。
4. 在 ai-ink-brain-api-python-wt-agently-lab/ 内按 task 范围改代码/配置；禁止在并行另一 worktree/checkout 改同一子仓；禁止静默扩大 scope；SPEC/task 矛盾走变更请求或交回需求帽。
5. 执行 pytest tests/agently_lab -m "not agently_lab_online"（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）」。
7. 对话回复：生成可完整复制的 Prompt 用于直接交给下一棒；兼顾打回、二次审查等情形。
8. 自动 commit：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python-wt-agently-lab/ 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
9. 链式下一棒：若 task 由 00 / Lead 按 PROMPT_*_chain_serial_* 编排 → 不在本帽同会话自动换帽；仅输出下一棒 §3 或交还父 Agent。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出。

Judgment（本帽 · 对话末尾必填）：
- experience_capture: 维持 | 建议升级 required | 维持 n/a（≤1 行理由）
- gate/risk: 无 | human_gate:<id> | 证据不足
- hat_self: pass | pass-with-notes | blocked
```

---

## Judgment（20-task-audit · R1）

- **experience_capture**: `required` 已合适。理由：本 task 为 Agently 学习 lab 首课，涉及 Runtime 映射、结构化输出 parser、import 边界、线上无状态部署等多处跨任务可复用决策，关账时必须有经验摘要或回灌 mapping/gap matrix。
- **gate/risk**: `HG-TASK-DRAFT` 当前 `pending`，`blocks_hats: 30`。建议维护者人签 `approved` 后再派 30；本帽不代签。另建议追加 `HG-AUDIT-R1` 待人签，但非强制。
- **hat_self**: `pass-with-notes`（非阻塞建议已列出，task 内容可执行）。
