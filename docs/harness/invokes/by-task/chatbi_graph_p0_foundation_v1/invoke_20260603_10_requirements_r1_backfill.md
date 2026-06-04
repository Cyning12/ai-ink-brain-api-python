# Invoke · 10 需求帽 · R1 回填 · chatbi_graph_p0_foundation_v1 · 2026-06-03

| 字段 | 值 |
| --- | --- |
| **hat_code** | 10 |
| **task_slug** | `chatbi_graph_p0_foundation_v1` |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **audit_review** | `docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md` |
| **交付** | task R1 回填（B-2～B-4；B-1 仍待人签闸） |

## §3 快照（开帽 Prompt 全文）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md（**SDD 三轮** · §4 待确认清单 · §5 完成后下一棒）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
按 22 帽 R1 审查清单回填 `task_chatbi_graph_p0_foundation_v1`：对齐 Harness validate、清零 SDD §10 待确认（至少 Q-8 Graph 路由 path），补 §行为变更 Delta；不扩 scope、不写业务代码。回填完成后输出路径 A（22 R2）与路径 B（仅当人已预批且清单已清零时）两条下一棒 Prompt。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md
ai-ink-brain-api-python/docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md
ai-ink-brain-api-python/docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md
ai-ink-brain-api-python/docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md
ai-ink-brain-api-python/docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md

【SDD 三轮状态】（§2 合法取值之一）
轮0+1+2 已完成，清单有待确认项

【是否新建或重大修订 SPEC】
否

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 docs/harness/invokes/README.md 落盘到 docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. **SDD 纪律（硬）**：
   - 若 `{{NEW_OR_MAJOR_SPEC}}` = **是**：须遵守三轮模型（§1）；**禁止** 在本帽一次生成整本 L1 SPEC。
   - 若 SDD 状态含 **「清单有待确认项」**：下一棒 **只许推荐路径 A** 或输出阻塞清单，**禁止** 推荐路径 B。
   - 当状态 = **`轮0+1+2 已完成，清单已人确认`**：可据 §下一棒 A/B 规则推荐 A 或 B；**三轮完成 ≠ 自动跳过 22**（见 SPEC §5）。
   - 本轮回填：**否** 新 SPEC · 须逐条闭合 R1「需任务帽回填清单」B-1～B-4。
2. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
3. 按审查 R1 回填清单逐条映射到 task 小节；文末注明「按审查 R1 回填」。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值。
5. 对话回复 — **下一棒须输出两条 Prompt（由人择一执行，不可只给一条）**：
   - 先输出 **推荐判定**（1～3 行）：本轮回填后 **推荐路径 A（22 R2）**；清单未清零前 **禁止** 推荐 B。
   - **路径 A · 22 任务审核 R2**：标题 `### 下一棒 A：22 任务审核 R2（推荐）`；正文 = TEMPLATE-task-audit-invoke §3 全文（`PREV_REVIEW_PATH` 指向 R1 审查 md）。
   - **路径 B · 30 执行（跳过 22）**：标题 `### 下一棒 B：30 执行（跳过 22）`；**不推荐**；若人强制选 B 须在 task 写明事后补 22。
6. 回复末尾输出 HANDOFF_SEMI_AUTO.md §3.4 `📋 Harness 状态栏（版本 B）`；**不得** 代填 `human_gate: approved`（除非人二次确认授权）。
7. **自动 commit**：若本轮已落盘 invoke 或已按用户授权写入 task，按 HANDOFF_AUTO_COMMIT.md 分仓 commit（仅本轮路径；对话报 short-hash）。用户写明「不要 commit」则跳过。
```
