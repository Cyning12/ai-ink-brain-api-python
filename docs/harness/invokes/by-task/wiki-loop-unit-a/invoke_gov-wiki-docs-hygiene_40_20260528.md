# Invoke · gov-wiki-docs-hygiene · 40 · R1

| 项 | 值 |
| --- | --- |
| **round** | R1 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 30（文档已 commit @ 9a58509） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 30 已结束；本帽为 40 自检帽，只按下文执行。

执行 Wiki Loop 单元 A · R1 · 40 自检。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only。
task: docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
task_slug: gov-wiki-docs-hygiene
freeze_id: GOV-WIKI-DOCS-HYGIENE@2026-05-28

**自检步骤**
1. 逐条对照 task 验收标准，运行 VERIFY 命令
2. 粘贴 VERIFY 输出要点到本 invoke
3. 回填 task 内 `### 自检结论（执行者）`
4. 落盘 40 invoke + commit
5. 无阻塞则自动戴 50 帽

**VERIFY 命令清单**
- `git diff HEAD~1 --name-only`：确认修改范围
- `test -f docs/tasks/done/task_harness_wiki_loop_p2_followup_v1.md`：P2 SPEC 链接有效性
- `ls docs/coding_wiki/syntheses/*.md | wc -l`：syntheses 数量基线
- `git diff HEAD~2 --name-only | grep -E "^(api/|tests/|tools/)"`：确认无越界改动
- `wc -c docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_*`：invoke C2 体量检查
```

---

## 自检结果

### 验收标准逐项核对

| # | 验收项 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` #36→✅ T4 active+扩面 | **pass** | v1.4 修订记录；#36 行已改 active+扩面/✅ |
| 2 | `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` #37→✅ P1-4 done | **pass** | #37 行已改 done/✅ |
| 3 | `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` §7 P2 T4/前端行更新 | **pass** | §7 P2 T4 → done；P3 前端 parity → done |
| 4 | `SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md` 母单链 `done/` | **pass** | 链接已改 `../../tasks/done/...`；文件存在 |
| 5 | `RECENT_TASK_SCHEDULE.md` §6.6 增 Unit A / L2 Phase C 行 | **pass** | Unit A in_progress；L2 Phase C pending |
| 6 | Roadmap §5.2 链出 Unit AB SPEC | **pass** | 已追加 A/B 双 PR 收口行 |
| 7 | invoke C2 全绿 | **pass** | 22=2800 B，30=2747 B；§3 均 ≥15 行；元信息完整 |
| 8 | 无 api/tests/tools 改动 | **pass** | `git diff HEAD~2` 无越界路径 |

### VERIFY 输出摘要

```
PASS: task_harness_wiki_loop_p2_followup_v1.md exists in done/
PASS: task_governance_wiki_t4_expand_v2.md
PASS: task_governance_wiki_agent_readorder_v1.md
PASS: task_governance_wiki_ingest_batch_v1.md
PASS: task_governance_wiki_ctx_ab_representative_v1.md
PASS: task_governance_l2_manifest_ci_v1.md
syntheses count: 20
PASS: no api/tests/tools changes
invoke sizes: 2800 B / 2747 B (≥800 B)
```

### 结论

**全部验收项通过 · 零阻塞 · 可进入 50 复检**
