# Invoke · 22 任务审核 · R3 · gov-l2-r3-test-manifest

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md` |
> | task_slug | `gov-l2-r3-test-manifest` |
> | freeze_id | `GOV-L2-R3-TEST-MANIFEST@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 母 Loop：`task_harness_wiki_loop_t4_l2_v1.md` · `HG-LOOP-BATCH` = approved。
- R1/R2 均已在 `done/`。
- 下一棒：30 执行编码。

## §2 审查结论

**零阻塞。可进入 30。**

- R1/R2 前置检查通过。
- 范围明确：`_test_manifest.json` + `99_spec` + `CODING_WIKI` + RECENT done。
- L2 SPEC schema 可读（§4.1）。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop T4+L2 **R3** 的 **30 执行编码帽**。上一帽（22 任务审核）已结束；本帽只按下文执行。

【元信息】
- round: R3
- hat: 30
- task: docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md
- task_slug: gov-l2-r3-test-manifest
- freeze_id: GOV-L2-R3-TEST-MANIFEST@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 当前状态
- R1/R2 均已在 done/
- L2 SPEC 已读取（`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.1 schema）

### 30 帽交付
1. 创建 `docs/_tech_graph/_test_manifest.json`（schema 见 L2 SPEC §4.1）：
   - `version`: 1
   - `freeze_id`: `GOV-L2-ANCHOR-TEST-MANIFEST@2026-05-27`
   - `entries`: ≥5 条真实 ERR/pytest 映射
   - 至少 1 条含 `graph_nodes_optional`（引用 R1 Pilot id：C1/RAG/RAG_DOC/FTS）
   - `test_paths` 仅 glob，必须以 `tests/` 开头
2. `docs/_tech_graph/99_spec.md` 增「测试 manifest」小节（链 L2 SPEC + 脚本表）。
3. `docs/coding_wiki/CODING_WIKI.md` §8 一行链 L2 SPEC。
4. `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.6：Wiki Loop T4+L2 行 → **done**。
5. `docs/harness/invokes/by-task/wiki-loop-t4-l2/README.md` 增验收一行（可选）。
6. `git add` 本轮路径 → `git commit`（HANDOFF_AUTO_COMMIT）。
7. 输出 40 自检 invoke。

### 硬约束
- 不改 api/、tests/、docs/harness/prompts/、CI workflow。
- 仅 docs + _test_manifest.json；test_strategy = not_applicable。

### VERIFY（40 须重跑）
```bash
test -f docs/_tech_graph/_test_manifest.json
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5"
python tools/tech_graph_manifest_check.py
python tools/tech_graph_graph_export.py --check
```
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_l2_r3_test_manifest_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：review 落盘 + invoke 落盘
├── 下一棒：A=30 执行编码 · B=—
├── 推荐：A
└── 阻塞：无
```
