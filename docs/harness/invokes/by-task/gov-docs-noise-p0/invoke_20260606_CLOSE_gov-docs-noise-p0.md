# invoke_20260606_CLOSE_gov-docs-noise-p0

> **帽**：CLOSE  
> **round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`  
> **merge_policy**：`stop_before_merge`

---

## §3 Prompt（CLOSE 帽 · 全文）

```text
【角色】Harness CLOSE · Round T1

【你必须完成】
1. 落盘 invoke_YYYYMMDD_CLOSE_gov-docs-noise-p0.md
2. 更新 docs/tasks/_views/（若 task 仍 active 则暂不 git mv；PR 合并后再 done）
3. git push -u origin task/gov-docs-noise-p0-v1
4. gh pr create --title "docs(governance): docs-noise P0 fix C1-C3 README pointers" \
     --body 含 Summary / Test plan（docs-only · CI Required）
5. gh pr checks --watch；全绿后 stop_before_merge → 向人报告 PR URL，不 merge
6. HANDOFF_CLOSE_TRACE + Harness 状态栏 B
```

---

## 关账摘要

| 项 | 值 |
| --- | --- |
| **Round** | T1 串行链完成：explore → 22 → 30 → 40 |
| **交付** | C1 invokes/README · C2 docs/README §1 · C3 tech_graph/README · SPEC §3 done |
| **test_strategy** | not_applicable（无 pytest） |
| **merge_policy** | stop_before_merge — CI 绿后等人 merge |

---

## Commit 链（api-python @ task/gov-docs-noise-p0-v1）

| 序 | hash | message |
| --- | --- | --- |
| 1 | f8498eb | explore C1-C3 差分 |
| 2 | c7585b7 | 22 R1 审核 |
| 3 | 134476b | 30 C1-C3 执行 |
| 4 | 35c7642 | 40 自检 |

（前置：2110f4a PROMPT 模板 · 2b79820 task 草案）

---

## PR

（CLOSE 阶段回填 PR URL 与 CI 状态）
