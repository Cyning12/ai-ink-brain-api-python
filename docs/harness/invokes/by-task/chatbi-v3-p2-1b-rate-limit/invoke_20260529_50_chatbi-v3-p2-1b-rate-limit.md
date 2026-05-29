# Invoke 快照（50 独立复检帽 · P2-1b 限流）

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| task_slug | `chatbi-v3-p2-1b-rate-limit` |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md` |
| git_branch | `task/chatbi-v3-p2-1b-rate-limit` |
| worktree_root | `ai-ink-brain-api-python/` |
| reinspect_mode | 独立复检 |
| freeze_id | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| test_strategy | `required` |
| audit_profile | `post_close` |
| 前置帽结论 | 22-R1 approved（零阻塞）；30 实现 `f803f87`；40 自检 `e7d9b0d` |
| 审查结论路径 | `docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/task_chatbi_v3_p2_resilience_rate_limit_v1_audit_R1_20260529.md` |
| 复检输出路径 | `docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_1b_rate_limit_20260529_v1.md` |
| 落盘日期 | 2026-05-29 |

---

## §3 快照（用户消息全文 · 占位符已替换）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md（§一 独立复检；§二 全局验收）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: required 时关注测试与实现关系）
- 根目录 AGENTS.md §8、docs/harness/ACCEPTANCE_LANDING.md（落盘结构）

输入（已由人工替换占位符；若你仍看到 {{…}} 或 REINSPECT_MODE 非三选一字面，须先追问用户，不得开工）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md
- 子仓根（相对 Projects/；用于理解 diff 与路径）：
ai-ink-brain-api-python
- 模式（必须恰好为以下之一：独立复检 / 全局验收 / 两者）：
独立复检
- diff 或变更范围说明（全局验收单独模式可写「无」）：
git diff origin/main...HEAD — P2-1b 限流：api/chatbi_rate_limit.py、api/index.py、tests/test_rate_limit_routes.py、PROJECT_CONFIG；自检基线 e7d9b0d
- 任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/task_chatbi_v3_p2_resilience_rate_limit_v1_audit_R1_20260529.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列分节实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/by-task/chatbi-v3-p2-1b-rate-limit/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。

【当模式为「独立复检」或「两者」时 — 对应 hat §一】
0. **落盘（硬）**：将完整复检正文写入 `docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_1b_rate_limit_20260529_v1.md`（结构见 docs/harness/ACCEPTANCE_LANDING.md）；落盘并 commit 后再在对话给摘要。
1. 读取 task 内「### 自检结论（执行者）」；若缺失 → 阻塞首条：要求先跑 TEMPLATE-self-check-invoke + 40。
2. 输入裁剪：以 diff、命令输出要点、自检验收表为主；避免执行过程长文。
3. 对 task 每条验收项输出表格：验收项 | pass/fail | 证据（文件:行 / 测试名 / 日志片段）| 备注；fail 须写复现步骤或缺失证据。
4. 汇总阻塞合并项；给出是否建议合并（供维护者决策）。
5. 禁止：替执行者改代码（除非用户明确要求复检提交 patch）；缺口退回需求/审查帽。

对话回复：若建议合并且无返工 → 输出「执行路线与 Commit 回溯」（docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md），勿编造下一棒 Prompt；若须打回 → 输出下一棒可复制 Prompt（含打回、二次审查、上一棒修复）。
8. **自动 commit**：`reinspect_results` 报告 + 本轮 `invokes/`（若有）按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md commit。用户写明「不要 commit」则跳过。
```
