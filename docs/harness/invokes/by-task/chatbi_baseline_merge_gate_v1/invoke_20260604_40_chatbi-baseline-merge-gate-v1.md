# Invoke · 40 自检帽 · chatbi_baseline_merge_gate_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 40 |
| **task_slug** | `chatbi_baseline_merge_gate_v1` |
| **git_branch** | `task/chatbi-baseline-merge-gate-v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **VERIFY** | `pytest tests -m "not intent_eval and not intent_benchmark" && python tools/tech_graph_contract_check.py` |
| **diff_note** | `git diff origin/main...HEAD` — conftest INTENT_MIN_CONFIDENCE · contract label · agent clarify_gate on |

## §3 快照（开帽 Prompt 全文）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/hats/40-self-check.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 的 test_strategy 等一致）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（运行验证命令的 cwd；见 docs/harness/README.md「并行分支与 Git worktree」）：
ai-ink-brain-api-python
- 主验证命令（与 CI / task 一致；task 另有命令须一并执行并在结论中分列）：
pytest tests -m "not intent_eval and not intent_benchmark" && python tools/tech_graph_contract_check.py
- 变更范围说明（无则写「无」）：
git diff origin/main...HEAD — conftest INTENT_MIN_CONFIDENCE · contract label · agent clarify_gate on

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `<子仓>/docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/` 或工作区 `Projects/docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 通读 task 全文中的验收标准与「验证 / 自检 / 合并前」相关命令列表；逐条运行所列命令（至少包含主验证命令），在对话中给出：命令、cwd、退出码、关键通过/失败行或断言摘要。
2. 输出 **验收表**（每项 pass/fail + 证据：命令名/测试名/日志摘录）；fail 时写明是否可重试（环境/flaky）。
3. 将 **`### 自检结论（执行者）`** 写入 **task 路径** 指向的 task 正文（若尚无该小节则新增；位置与团队习惯一致即可）：含命令列表、退出码、验收摘要、已知未测项。
4. 禁止：凭记忆声称「测过」；把独立复检的深度走查塞进本帽（本帽以命令与验收表为主）。
5. **Fresh Context（P1）**：交接 50/22 时 **禁止**粘贴 30 invoke 全文；仅交 diff 要点、验收表、`### 自检结论`。

对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
6. **自动 commit**：在输出下一棒 Prompt 且 task 内「### 自检结论（执行者）」已写入后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 分仓 commit（仅本轮路径；对话报 short-hash）。用户写明「不要 commit」则跳过。
```
