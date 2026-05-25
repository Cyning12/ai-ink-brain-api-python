## Invoke 快照（30 执行帽）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_v1.md` |
| git_branch | `task/chatbi-v3-p2-resilience-spec` |
| semiauto | `true` |
| audit_profile | `post_close` |
| 记录时间 | `2026-05-23` |

### 用户输入快照（原文）

```text
你正在扮演本仓（ai-ink-brain-api-python）Harness **执行链**，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 本仓 AGENTS.md（合并前必绿）

【模式】全预批 + semi_auto 关账试验：HG-TASK-DRAFT / HG-AUDIT-R1 / HG-REINSPECT 均已 **approved**（人 kickoff 预批）。**禁止** Agent 修改任何 human_gate 状态。**仍须**完整跑 30→40→50 交付物，不得因预批跳过 50/reinspect。

输入：
- 主 task 路径：
  docs/tasks/active/task_chatbi_v3_p2_resilience_v1.md
- 逻辑子仓 / cwd（git、pytest 均在此根）：
  ai-ink-brain-api-python（当前仓库根）
- git 分支（须已 checkout）：
  task/chatbi-v3-p2-resilience-spec
- 合并前验证命令：
  pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核：
  无（路径 B；22 可选零阻塞落盘，不新增 pending 闸）
- 关联 SPEC / 排期：
  docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md
  docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md
  docs/tasks/RECENT_TASK_SCHEDULE.md

0. **Invoke 快照（30 开帽）**：将 **本用户消息全文** 落盘
   docs/harness/invokes/by-task/chatbi-v3-p2-resilience-spec/invoke_20260523_30_chatbi-v3-p2-resilience-spec.md
   （含元数据表 + 快照 fenced code；本仓落盘，**非** Projects/）

0b. **人工闸扫描**：
   - 若 HG-TASK-DRAFT 或 HG-AUDIT-R1 对 30 为 pending → **拒开工**（仅报 gate_id + 路径）
   - 若三闸均已 approved → **继续**（HG-REINSPECT 预批 **不**挡 30/40/50，仅关账时不再等人签）

1. **30 执行帽** — 通读 task；按 **非范围**（本 PR **仅拆单/docs**，**禁止** `api/` 实现）：
   - 审计 `api/index.py` `/api/py/health` 与 Unified Chat 高消耗路径（只读对照）
   - 填 task **§实现拆单**（P2-1a health/ready、P2-1b 限流、P2-1c 熔断）
   - 新建子 task 草案：`docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` 等（2～3 个）
   - 更新 `docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§3** 任务索引行
   - 勾选/更新 task 验收项（docs-only diff）
   - （可选）22 零阻塞：`docs/harness/reviews/task_chatbi_v3_p2_resilience_v1_audit_R1_YYYYMMDD.md`

2. **40 自检帽**（semi_auto 同会话切换）：
   - 落盘 invoke：`docs/harness/invokes/by-task/chatbi-v3-p2-resilience-spec/invoke_20260523_40_chatbi-v3-p2-resilience-spec.md`
   - 跑 pytest；回填 task **`### 自检结论（执行者）`**（退出码、passed 数、纯 docs 说明）
   - commit 本轮路径（HANDOFF_AUTO_COMMIT）

3. **50 独立复检帽**（**不可省略**，即使 HG-REINSPECT 已预批）：
   - 落盘 invoke：`docs/harness/invokes/by-task/chatbi-v3-p2-resilience-spec/invoke_20260523_50_chatbi-v3-p2-resilience-spec.md`
   - 落盘 **`docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_resilience_20260523.md`**
     （验收表 + diff 证据 + 「建议合并」；对照 task 全部验收项）
   - commit

4. **关账**（HG-REINSPECT 已 approved → **允许归档**）：
   - task 头部 → `done（YYYY-MM-DD 验收通过 · P2-1 拆单）`
   - `git mv` → `docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`
   - 更新 `docs/tasks/_views/done.md`；从 `_views/design.md` 移除
   - 输出 **HANDOFF_CLOSE_TRACE**（执行路线 + commit 回溯）
   - commit 关账变更

5. **PR**（**开 PR，不 merge main**，除非用户另明示「CI 绿后 merge」）：
   - `git push -u origin task/chatbi-v3-p2-resilience-spec`
   - `gh pr create --base main` — 标题含「P2-1 拆单」；正文：Summary（拆单表 + 子 task 路径）+ Test plan（pytest 绿、docs-only）

6. **每棒结束**：回复末尾 **`📋 Harness 状态栏（版本 B）`**；40/50/关账各落 invoke + commit。

硬约束：
- **禁止**改 `api/`、CI workflow、前端仓
- **禁止**代填/回改 human_gate
- **禁止**无 reinspect 文件即 done
- **禁止** `git add -A`；仅 add 本轮路径
- test_strategy 为 not_applicable：不得引入「先写实现再补测」

若 pytest 失败或验收缺项：停止扩 scope，输出阻塞清单与修复建议，**不**开 PR。
```
