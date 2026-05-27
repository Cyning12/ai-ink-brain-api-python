# 任务审核 — L2 锚点与 `_test_manifest` 草案（R3）

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | task | `docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md` |
> | task_slug | `gov-l2-r3-test-manifest` |
> | freeze_id | `GOV-L2-R3-TEST-MANIFEST@2026-05-27` |
> | round | R3 |
> | audit_profile | post_close |
> | invoke_snapshot | `docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_20260527_22_gov-l2-r3-test-manifest-v1.md` |

---

## 审查结论摘要

**零阻塞。建议执行帽开工。**

- 前置检查：R1/R2 均已在 `done/` ✅。
- 母闸 `HG-LOOP-BATCH` 状态 `approved`。
- 任务范围明确：`_test_manifest.json` + `99_spec` + `CODING_WIKI` + RECENT done。
- 验收标准可执行：VERIFY 命令已列明。

---

## 已核对项

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | R1 在 `done/` | pass | `docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md` |
| 2 | R2 在 `done/` | pass | `docs/tasks/done/task_governance_wiki_t4_r2_l0_align_v1.md` |
| 3 | `HG-LOOP-BATCH` = approved | pass | 母 task §human_gate |
| 4 | task 含验收标准 + VERIFY | pass | task §验收标准 |
| 5 | task 含 failure_paths | pass | task §失败路径 |
| 6 | 不改 api/tests/prompts/CI | pass | task §非范围 |
| 7 | L2 SPEC schema 可读 | pass | `SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.1 |

---

## 阻塞 / 非阻塞

**无阻塞。**

---

## 签收 / 关闭

本 task **R3 可进入执行帽**。30 帽负责：
1. 创建 `docs/_tech_graph/_test_manifest.json`（≥5 entries，≥1 条含 `graph_nodes_optional`）。
2. `99_spec.md` 增测试 manifest 小节。
3. `CODING_WIKI.md` §8 链 L2 SPEC。
4. RECENT §6.6 **done** 行 + `_views/done.md` + invoke README 验收一行。
5. 40 → 50 → 关账。

---

## 下一棒可复制 Prompt

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
