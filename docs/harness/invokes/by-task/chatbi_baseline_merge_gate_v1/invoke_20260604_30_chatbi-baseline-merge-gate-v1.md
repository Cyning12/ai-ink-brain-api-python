# Invoke 快照 · 30 执行编码 · chatbi_baseline_merge_gate_v1

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_baseline_merge_gate_v1` |
| **hat** | `30-execute-code` |
| **round** | — |
| **task_path** | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` |
| **git_branch** | `task/chatbi-baseline-merge-gate-v1` |
| **freeze_id** | （无新 L1 SPEC；行为真值以 v3 单测 + `_contract_manifest.json` 为准） |
| **audit_review** | `ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_baseline_merge_gate_v1_audit_R1_20260604.md` |
| **date** | `20260604` |

## 快照（§3 调用体）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/hats/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8（合并前必绿命令真值，若与本条 VERIFY 冲突以 task + 子仓 workflow 为准）

输入（已由人工替换占位符；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致，见 docs/harness/README.md「并行分支与 Git worktree」）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests -m "not intent_eval and not intent_benchmark" && python tools/tech_graph_contract_check.py
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_baseline_merge_gate_v1_audit_R1_20260604.md
- 关联 SPEC / 总规（无则「无」）：
无

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `<子仓>/docs/harness/invokes/by-task/<task_slug>/` 或工作区 `Projects/docs/harness/invokes/by-task/<task_slug>/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 `human_gate`（见 docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md）。若任一对 **本帽（30）** 为 `pending` → 仅输出须人改的 `gate_id` 与路径，**拒开工**；禁止代填 `approved`。**例外**：若 invoke 声明 gate 已「人 kickoff 预批」但文件仍为 `pending`，Agent 须向用户二次确认（见 HANDOFF_SEMI_AUTO.md §2.3 预批与二次确认），获得明确文字授权后方可代填，且须在 commit message 注明 `human_gate 由 Agent 按人授权代填`。
1. 通读 task 全文：头部 `gates_before_code`、`audit_profile`、`semi_auto`、`test_strategy` / `test_strategy_note`、`freeze_id`、`failure_paths`、拒开工条件、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足（缺 failure_paths 可操作性、缺验收命令、必读未覆盖等）→ **仅输出 Markdown 阻塞清单**（缺什么、建议回填的小节标题、推荐下一棒角色），**不写**业务实现代码。
3. `test_strategy: required` 时：先增加或调整 **可失败** 的自动化测试（或与实现同 PR 且满足 task 所述 red-green / 可复现失败语义），再改实现；禁止「只写实现、后补测」绕过 task 约定。
4. 在 `ai-ink-brain-api-python` 内按 task 范围改代码/配置（**禁止**在并行另一 worktree/checkout 改同一子仓）；禁止静默扩大 scope；SPEC/task 矛盾走变更请求或交回需求帽，不擅自调和为代码假设。
5. 在 `ai-ink-brain-api-python` 执行 `pytest tests -m "not intent_eval and not intent_benchmark" && python tools/tech_graph_contract_check.py`（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 `hats/40-self-check.md` 将结论与命令摘要 **回填** 至 task 正文 **`### 自检结论（执行者）`**（无则新增该小节）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
9. **半自动下一棒（可选）**：若 task `semi_auto: true` 且下一棒（如 40）无 `human_gate` 阻塞：先将 **下一棒 §3 全文** 落盘新 invoke 并 commit，再切换角色执行；规则见 HANDOFF_SEMI_AUTO.md §3。否则仅输出下一棒 Prompt 供人开新会话。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出。
**Fresh Context（P1）**：40→50/22 交接时 **禁止**粘贴本帽 invoke 全文或长思考链；仅交 diff 要点、验收表、`### 自检结论`。
```
