# Invoke · 30 — docs governance archive and done index

## 元信息（版本 B 摘要）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `RECENT_TASK_SCHEDULE` · P0 治理归档（纯后端仓） |
| audit_profile | post_close |
| git_branch | `task/docs-governance-harness-archive-and-done-index` |
| human_gate | 无 |
| next | push 分支并创建 PR 到 `main` |
| block | 无 |

---

## §3 可复制 Prompt 快照（执行记录）

```text
目标：完成 RECENT_TASK_SCHEDULE · P0 治理归档

执行项：
1) 归档 task_harness_in_repo_prompts_and_rules_v1：
   - 状态头改为 done（2026-05-22 验收通过）
   - git mv active -> done
   - _views/done.md 追加索引

2) _views/done.md 遗漏 18 条核验：
   - 按 §6.1 清单逐条核对
   - 当前分支结果：18 条已全部存在，无需重复追加

3) 更新 RECENT_TASK_SCHEDULE.md：
   - §1 快照改为 active=7、done=53、done 索引遗漏=0
   - §1.1 移除 harness_in_repo（已归档）
   - §2 两条“立即”标记 done
   - §8 新增 2026-05-23 修订记录

4) 验证：
   - active/ 无“头部 done 但未 mv”文件
   - （可选）pytest 文档任务可跳过

5) Git：
   - commit docs/invokes/tasks 变更
   - push 分支并 gh pr create --base main
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-23 | v1：P0 治理归档执行 invoke 落盘 |
