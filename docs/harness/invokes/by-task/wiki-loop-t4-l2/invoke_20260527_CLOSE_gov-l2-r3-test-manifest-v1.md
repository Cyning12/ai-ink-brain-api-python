# Invoke · 关账 · R3 · gov-l2-r3-test-manifest

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | CLOSE |
> | task | `docs/tasks/done/task_governance_l2_r3_test_manifest_v1.md` |
> | task_slug | gov-l2-r3-test-manifest |
> | freeze_id | GOV-L2-R3-TEST-MANIFEST@2026-05-27 |
> | git_branch | task/gov-spec-t4-l2-v1 |
> | cross_round_semi_auto | true |

---

## §1 关账结论

R3 L2 manifest 关账完成。全部验收通过，无阻塞。

## §2 执行路线与 Commit 回溯

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/wiki-loop-t4-l2/*` | api-python@52ac63d |
| 2 | 30 执行编码 | _test_manifest.json + 4 文件修改 | 5 文件 | api-python@b3c7770 |
| 3 | 30 invoke | invoke 落盘 + 40 Prompt | `invoke_20260527_30_*` | api-python@23e01c6 |
| 4 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@80397da |
| 5 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspec_*_20260527_v1.md` + `invoke_20260527_50_*` | api-python@48501c9 |
| 6 | **关账** | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | api-python@7c7e666 |

### 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- 7c7e666 docs(task): R3 关账 — gov-l2-r3-test-manifest → done/ + _views 更新
- 48501c9 docs(harness): 50 R3 独立复检 + CLOSE_TRACE
- 80397da docs(harness): 40 R3 自检 + task 回填 + 50 下一棒 Prompt
- 23e01c6 docs(harness): 30 R3 执行编码 invoke + 40 下一棒 Prompt
- b3c7770 docs(governance): R3 L2 manifest 交付 — _test_manifest.json + 99_spec + CODING_WIKI + RECENT
- 52ac63d docs(harness): 22 R3 任务审核落盘 + invoke
```

## §3 续跑 META

按 LOOP_MANIFEST 与 cross_round_semi_auto 授权，R3 关账后同会话续 META。

**META 任务**：`docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md`
**META slug**：`wiki-loop-t4-l2`
**META freeze_id**：`WIKI-LOOP-T4-L2@2026-05-27`

### META 启动 Prompt

```text
你正在执行 Wiki Loop T4+L2 **META 关账**。三轮子 task 均已在 `done/`，严格遵循：
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §长 Loop 完成汇报
- semi_auto: true

【元信息】
- round: META
- task: docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md
- task_slug: wiki-loop-t4-l2
- freeze_id: WIKI-LOOP-T4-L2@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### META 交付
1. 确认三轮子 task 均在 `done/`：
   - R1: task_governance_wiki_t4_r1_pilot_v1.md
   - R2: task_governance_wiki_t4_r2_l0_align_v1.md
   - R3: task_governance_l2_r3_test_manifest_v1.md
2. 更新母 task 状态（`status: done` 等）。
3. 落盘 `REPORT_completion_*`：
   `docs/harness/invokes/by-task/wiki-loop-t4-l2/REPORT_completion_20260527_v1.md`
4. 输出执行路线与 Commit 回溯（HANDOFF_CLOSE_TRACE）。
5. `git add` 本轮路径 → `git commit`（HANDOFF_AUTO_COMMIT）。

### REPORT 结构（§1～§5 落盘）
- §1 任务定位
- §2 核心成果（按 round）
- §3 Harness 工件链
- §4 Commit 回溯
- §5 验收项核对
- §6 仅对话（禁止落盘）

### 硬约束
- §6 「待你侧后续」仅对话，禁止写入 REPORT。
- 不 push / 不改 CI / 不代填 human_gate。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：CLOSE · R3 关账
├── task：task_governance_l2_r3_test_manifest_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：git mv → done/ + _views 更新 + CLOSE invoke 落盘
├── 下一棒：META 关账（wiki-loop-t4-l2）
├── 推荐：—（按 MANIFEST 自动续跑）
└── 阻塞：无
```
