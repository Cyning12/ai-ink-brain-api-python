# Invoke · 22 任务审核 / R1 审查 · graph-yaml-p0-00-main

| 字段 | 值 |
|------|-----|
| **task_slug** | `graph-yaml-p0-00-main` |
| **hat** | `22` |
| **date** | `20260616` |
| **git_branch** | `task/graph-yaml-p0-00-main` |
| **audit_round** | `R1` |
| **prev_review** | `无` |

---

## Prompt 正文快照（ fenced code 内）

```text
你正在扮演 **Harness 22 任务审核 Agent**，执行 task `graph-yaml-p0-00-main` 的 R1 审查。

## 开帽确认
- 前置：10 帽已完成，task 正文已回填 R0–R3
- HG-TASK-DRAFT = approved
- HG-AUDIT-R1 = pending（本帽产出审查后仍须维护者人工签 approved）
- git_branch: `task/graph-yaml-p0-00-main`
- cwd: `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python`

## 必须遵循
- `docs/harness/prompts/hats/22-task-audit.md`（身份、禁止项、输出形状、交接物）
- `docs/harness/reviews/README.md`（文件命名、R1/R2 闭环）
- `docs/harness/HARNESS_V2_PLAN.md` §5（test_strategy、failure_paths 等）
- `docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md`

## 输入
- 待审 task 路径（相对工作区根 Projects/）：
  `ai-ink-brain-api-python/docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md`
- 关联 SPEC / 总规路径：
  `ai-ink-brain-api-python/docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md`
  `ai-ink-brain-api-python/docs/_tech_graph/99_mermaid_protocol.md`
  `ai-ink-brain-api-python/docs/_tech_graph/graph_v2_schema.md`
- 上一轮审查文档路径：无
- 10 帽 invoke 快照：`ai-ink-brain-api-python/docs/harness/invokes/by-task/graph-yaml-p0-00-main/invoke_20260616_10_graph-yaml-p0-00-main.md`

## 落盘文件
`ai-ink-brain-api-python/docs/harness/reviews/by-task/graph-yaml-p0-00-main/task_graph-yaml-p0-00-main_audit_R1_20260616.md`

## 你必须完成
0. **Invoke 快照（开帽起点）**：先将本用户消息全文按 `docs/harness/invokes/README.md` 落盘到 `docs/harness/invokes/by-task/graph-yaml-p0-00-main/invoke_20260616_22_graph-yaml-p0-00-main.md`（含元数据表 + 快照 fenced code）。
1. 通读待审 task 全文及头部元信息（状态、freeze_id、audit_profile、orchestration、test_strategy、failure_paths、验收、必读链接）。
2. 重点审查：
   - 10 帽思考轮是否闭合（R0–R3，early_stop=yes 是否成立）
   - YAML schema 方案是否可行（对照 QNA §2 + graph_v2_schema）
   - CI 策略是否不破坏现有 `verify-tech-graph.sh`
   - 非范围是否守住（不删 .ai.md、不接 cyning-harness、仅 00_main）
   - failure_paths F1/F2/F3 是否可操作
   - 验收标准是否可观测（≥1 pytest、diff 校验、00_main.md 生成）
3. 落盘审查文档至上述路径。文内结构：
   - 元信息（含 task_path、invoke_snapshot、audit_round=R1）
   - 审查结论摘要
   - 阻塞 / 非阻塞清单
   - 需任务帽回填清单（若有）
   - 是否建议执行帽开工
   - 「签收 / 关闭」 verdict
   - 下一棒：若有阻塞 → 退回 10 的 Prompt；若无阻塞 → 输出 30 执行 Prompt（但须注明 HG-AUDIT-R1 仍 pending，30 须人签后方可开工）
4. 禁止仅在对话里说「过了」而不写 reviews；禁止在仍有阻塞时指示执行帽开工。
5. 不要写业务实现代码；不要擅自改写 task 正文（但可在审查 md 中列出 task 需回填项）。
6. 自动 commit：完成落盘后，按 HANDOFF_AUTO_COMMIT.md 在相关 git 根 commit（仅本轮路径：invokes + reviews + 如有 task 修改）。对话末尾一行报 short-hash。

## 审查原则
- `audit_profile: full` + `test_strategy: required` → 须确保 30 帽可失败测试方案书面化
- 残余风险（kind 缺失、锚点渲染、AUTO 块策略）须书面钉住
- 若审查不通过，必须退回 10，禁止附带 30 Prompt

## 返回给 00 总调度的报告格式
1. 本帽结论（pass / blocked / 退回 10）
2. 审查 md 路径
3. invoke 路径
4. 阻塞项 / 需 10 回填清单（若有）
5. 是否建议 30 开工（须等 HG-AUDIT-R1 approved）
6. commit hash
7. 下一步：若 pass → 等待维护者签 HG-AUDIT-R1；若 blocked → 退回 10
```
