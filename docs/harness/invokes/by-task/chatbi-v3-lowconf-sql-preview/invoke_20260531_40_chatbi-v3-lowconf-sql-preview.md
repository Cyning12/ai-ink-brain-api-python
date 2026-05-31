# Invoke 快照 · 40 自检 · chatbi-v3-lowconf-sql-preview

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| task_slug | chatbi-v3-lowconf-sql-preview |
| task_path | docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-sql-preview |
| freeze_id | CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31 |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演 Harness「自检帽」，严格遵循 40-self-check.md、HANDOFF_SEMI_AUTO.md。

输入：
- task：docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md
- 30 交付：tests/test_unified_chat_backend_v2_agent.py 新增 G1–G4 测例；272 pytest 绿；contract OK
- 禁止：粘贴 30 长文；仅 diff 要点 + 命令表

你必须完成：
1. 复跑 task §6 建议命令并记录退出码。
2. 回填/核对 task ### 自检结论（执行者）§10。
3. 输出 50 invoke（Fresh Context 说明）并 commit。
4. 不代签 HG-REINSPECT；不关账（待 50）。

Judgment（40）：
- experience_capture: recommended
- gate/risk: HG-REINSPECT 仍阻塞 merge
- hat_self: pass
```
