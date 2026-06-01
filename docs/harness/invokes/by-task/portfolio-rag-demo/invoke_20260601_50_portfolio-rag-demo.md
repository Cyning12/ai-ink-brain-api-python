# Invoke 快照 · 50 独立复检 · portfolio-rag-demo

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| task_slug | portfolio-rag-demo |
| task_path | docs/tasks/active/task_portfolio_rag_demo_v1.md |
| git_branch | task/portfolio-rag-demo-v1 |
| freeze_id | PORTFOLIO-RAG-DEMO@2026-06-01 |
| REINSPECT_MODE | 独立复检 |
| audit_R1 | docs/harness/reviews/by-task/portfolio-rag-demo/task_portfolio_rag_demo_v1_audit_R1_20260601.md |
| date | 20260601 |

---

## §3 调用体（快照）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md（§一 独立复检；§二 全局验收）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: required 时关注测试与实现关系）
- 根目录 AGENTS.md §8、docs/harness/HARNESS_V2_P0_ACCEPTANCE.md（若本次变更触及合并前必绿子仓）

Open Folder = ai-ink-brain-api-python
git_branch = task/portfolio-rag-demo-v1

输入（已由人工替换占位符；若你仍看到 {{…}} 或 REINSPECT_MODE 非三选一字面，须先追问用户，不得开工）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_portfolio_rag_demo_v1.md
- 子仓根（相对 Projects/；用于理解 diff 与路径）：
ai-ink-brain-api-python
- 模式（必须恰好为以下之一：独立复检 / 全局验收 / 两者）：
独立复检
- diff 或变更范围说明（全局验收单独模式可写「无」）：
git diff origin/main...HEAD -- docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md docs/tasks/active/task_portfolio_rag_demo_v1.md docs/harness/reviews/by-task/portfolio-rag-demo/ docs/harness/invokes/by-task/portfolio-rag-demo/ docs/diary/samples/portfolio-rag-demo/
- 任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/by-task/portfolio-rag-demo/task_portfolio_rag_demo_v1_audit_R1_20260601.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列分节实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `docs/harness/invokes/by-task/portfolio-rag-demo/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。

【当模式为「独立复检」或「两者」时 — 对应 hat §一】
1. 读取 task 内「### 自检结论（执行者）」；若缺失 → 阻塞首条：要求先跑 TEMPLATE-self-check-invoke + 40。
2. 输入裁剪：以 diff、命令输出要点、自检验收表为主；避免执行过程长文。
3. 对 task 每条验收项输出表格：验收项 | pass/fail | 证据（文件:行 / 测试名 / 日志片段）| 备注；fail 须写复现步骤或缺失证据。
4. 汇总阻塞合并项；给出是否建议合并（供维护者决策）。
5. 禁止：替执行者改代码（除非用户明确要求复检提交 patch）；缺口退回需求/审查帽。
6. **W5 口径**：§6.2 / G-W5-* 若仍为「未测 / HG-W5 pending」，应标 **defer（非 30 阻塞）** 或 **fail（若声称 W5 已完成）**；勿与 W2/W3 文档 tranche 混判。

【当模式为「全局验收」或「两者」时 — 对应 hat §二】
6. 若 task 声明 freeze_id：核对 PR 变更是否在冻结基准内；契约升级是否在 SPEC/task 显式记录。
7. 输出 checklist 表（项 / 状态 / 签注栏「待人工」）；不伪造已签核；不跳过 CI 红灯叙事。

7. **落盘**：全文写入 `docs/tasks/reinspect_results/reinspect_portfolio_rag_demo_v1_20260601_v1.md`（结构见 ACCEPTANCE_LANDING / 50 帽）。

对话回复：若建议合并且无返工 → 输出「执行路线与 Commit 回溯」（docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md），勿编造下一棒 Prompt；若须打回 → 输出下一棒可复制 Prompt（含打回、二次审查、上一棒修复）。
8. **自动 commit**：落盘后按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 分仓 commit。用户写明「不要 commit」则跳过。

Judgment（本帽 · 对话末尾必填；任一项 warn/fail 须写 judgment_notes）：
- experience_capture: 维持 | 建议升级 required | 建议降 n/a | 维持 n/a（≤1 行理由）
- gate/risk: 无 | 须人审:<HG-id> | 证据不足
- hat_self: pass | pass-with-notes | blocked

Fresh Context（P1）：**禁止**阅读 30 invoke 全文；输入限于 task、reviews R1、diff 摘要、40 `### 自检结论`。
```
