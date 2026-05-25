## Invoke 快照（30 执行帽 · P2-1a health/ready）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| git_branch | `task/chatbi-v3-p2-1a-health` |
| worktree_root | `ai-ink-brain-api-python` |
| test_strategy | `required` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| human_gate_scan | `task 内未显式列 human_gate；按指令视作 HG-TASK-DRAFT，人 kickoff 本次对话已明确授权开工` |

### 用户输入快照（本消息全文）

```text
你正在扮演本仓（ai-ink-brain-api-python）Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、拒开工、test_strategy: required）
- docs/harness/prompts/40-self-check.md（命令证据、回填 ### 自检结论（执行者））
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（semi_auto 链式 40；human_gate 禁止静默代填）
- docs/harness/HARNESS_V2_PLAN.md §5
- 本仓 AGENTS.md（合并前必绿）

【开帽】将本消息全文落盘至：
docs/harness/invokes/invoke_YYYYMMDD_30_chatbi-v3-p2-1a-health.md
（元数据表 + 快照 fenced code；同一会话追问不重复落盘）

输入（占位符已替换）：
- 主 task 路径：
  docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md
- 逻辑子仓 / git cwd：
  ai-ink-brain-api-python（仓库根）
- 分支（须已 checkout）：
  task/chatbi-v3-p2-1a-health
- 合并前验证命令：
  pytest tests -m "not intent_eval and not intent_benchmark"
- 任务审核书面结论：
  无（路径 B；可选 docs/harness/reviews/ 零阻塞落盘，不挡 30）
- 关联 SPEC / 母单：
  docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md（§4 健康检查）
  docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md（拆单母单）
  docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md

0b. 人工闸：扫描 task 的 human_gate（若 task 无表，视为 HG-TASK-DRAFT 须人确认后再开工）。
    任一 blocks 30 且 pending → 仅报 gate_id + 路径，拒开工。
    人 kickoff 预批时：须对话明确授权；代填 gate 须在 commit message 注明（见 meta SKILL）。

你必须完成：
1. 通读 task：范围 / 非范围 / failure_paths / 验收 / test_strategy: required。
2. 只读对照 api/index.py 现有 GET /api/py/health，再实现：
   - GET /api/py/live — 轻量 200，不打重外呼
   - GET /api/py/ready — 依赖探测；未就绪 503 + JSON components[]
   - 保留或兼容现有 /api/py/health（与 task/SPEC 对齐后写入 PROJECT_CONFIG）
3. test_strategy required：先写可失败 pytest（live 200、ready 503 注入场景），再改实现。
4. 跑 pytest；回填 task「### 自检结论（执行者）」；勾选验收项。
5. 按 HANDOFF_AUTO_COMMIT 仅 add 本轮路径并 commit（禁止 git add -A）。
6. semi_auto：落盘 40 invoke → commit → 切 40 自检；无 pending 闸可继续 50（本 task 若要求 reinspect）。

硬约束：
- 禁止实现 P2-1b 限流、P2-1c 熔断
- 禁止改 CI workflow、前端仓
- 禁止无命令输出即勾选验收

对话末尾输出 📋 Harness 状态栏（版本 B）；40 通过后给 50 invoke 摘要或下一棒 Prompt。
```
