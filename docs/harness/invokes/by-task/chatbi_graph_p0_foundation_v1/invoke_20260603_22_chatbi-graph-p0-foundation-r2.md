# Invoke 快照 · 22 任务审核 · chatbi_graph_p0_foundation_v1 · R2

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_graph_p0_foundation_v1` |
| **hat** | `22`（任务审核） |
| **audit_round** | `R2` |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **prev_review** | `ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md` |
| **date** | `20260603` |
| **task_path** | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |

---

## 快照（用户消息 §3 全文）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/hats/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths 等与 task 字段对齐）

输入（已由人工替换占位符；若你仍看到 {{…}} 或本段「待填」字样，须先追问用户，不得开工）：
- 待审 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md
- 关联 SPEC / 总规路径（无则写「无」）：
ai-ink-brain-api-python/docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md
ai-ink-brain-api-python/docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md
ai-ink-brain-api-python/docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md
ai-ink-brain-api-python/docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md
- 上一轮审查文档路径（首轮写「无」；复审必填）：
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md

落盘文件建议名（须与文内元信息一致；若与用户输入冲突以用户为准并追问）：
- 待审 task 在 **`ai-ink-brain-api-python/docs/tasks/`** 下：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md`（全文真值）；工作区 `docs/harness/reviews/` 可仅存指针链至此路径。  
- 否则：`docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md`

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `docs/harness/invokes/by-task/<task_slug>/`（含元数据表 + 快照 fenced code）。你在步骤 3 落盘审查 md 时，须在文首元信息表增加 **`invoke_snapshot`** 指向该 invoke 文件（相对 `Projects/`）。同一会话内追问 **不** 再新增快照文件。
1. 通读待审 task 全文及头部元信息（状态、freeze_id、gates_before_code、test_strategy、failure_paths、验收、必读链接）。
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性、required 与可失败自动化测试说明。
3. 落盘一篇审查文档至 **上表路径**（与 `reviews/README.md`、`hats/22-task-audit.md` 子仓规则一致）。
4. 文内结构：元信息 → 审查结论摘要 → 阻塞 / 非阻塞 → 需任务帽回填清单（若有）→ 是否建议执行帽开工 → 「签收 / 关闭」→ 收尾二选一：**有下一棒** → **「下一棒可复制 Prompt」**（`text` 围栏，§3 全文）；**终轮无下一棒** → **「执行路线与 Commit 回溯」**（见 docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md，含阶段表 + 分仓 commit 列表）。
5. 禁止仅在对话里说「过了」而不写 reviews；禁止在仍有阻塞时指示执行帽开工。
6. **Fresh Context（P1）**：**新对话**开帽；**禁止**要求阅读 30 invoke 全文；输入限于 task、reviews、40 自检、diff 摘要。
6. 不要写业务实现代码；不要擅自改写 task 正文。
7. **对话与归档**：与步骤 4 审查 md 末节 **逐字或语义一致**——有下一棒则对话输出完整 Prompt；无下一棒则输出完整回溯表，**禁止**用空 Prompt 占位。
8. **自动 commit**：完成步骤 3–7 后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 在相关 git 根分别 commit（仅本轮路径；对话末尾一行报 short-hash）。用户本轮写明「不要 commit」则跳过。
```
