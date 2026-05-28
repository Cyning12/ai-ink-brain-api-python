# Scorecard · gov-l2-manifest-ci · Claude Code

| 字段 | 值 |
| --- | --- |
| **freeze_id** | `SKILL-XPLAT-GOV-L2-MCI@2026-05-27` |
| **task_slug** | `gov-l2-manifest-ci` |
| **platform** | `claude-code` |
| **model** | Claude Opus 4.7（Co-Authored-By 留证） |
| **date** | 2026-05-27 |
| **SKILL** | [`SKILL-harness-task`](../../../../../tasks/skills/SKILL-harness-task.md) · [`SKILL-docs-governance`](../../../../../tasks/skills/SKILL-docs-governance.md) |
| **PROMPT 入口** | [`PROMPT_START_full_chain_v1.md`](../../../invokes/by-task/gov-l2-manifest-ci/PROMPT_START_full_chain_v1.md) |
| **业务 PR** | [#70](https://github.com/Cyning12/ai-ink-brain-api-python/pull/70) · merge `main` |
| **hygiene PR** | [#71](https://github.com/Cyning12/ai-ink-brain-api-python/pull/71) · ST5/H5/invoke §3 补债 |

---

## 三维总评（业务 PR 后 · hygiene 前）

```text
业务实现     ████████████████████  95%  ← 可合并
Harness 落盘  ██████████████░░░░░░  70%  ← ST5 + invoke §3 + H5 有债
开 PR 就绪度   ████████████░░░░░░░░  60%  ← 建议先 hygiene 补丁
```

## 三维总评（hygiene PR #71 后 · 预期）

```text
业务实现     ████████████████████  95%
Harness 落盘  ██████████████████░░  90%  ← ST5/H5/§3 已补；历史 PROMPT_START 仍含 active 路径（可接受）
开 PR 就绪度   ████████████████████  95%  ← docs-only hygiene 可 merge
```

| 维度 | 分（前） | 分（后） | 依据 |
| --- | --- | --- | --- |
| 业务实现 | 95 | 95 | manifest 12 entries · `tech_graph_test_manifest_check.py` · pytest 12 · workflow step · 7/7 VERIFY 绿 |
| Harness 落盘 | 70 | 90 | 22→CLOSE 5 commit 齐全；前：task 仍 draft、§3 stub、H5 active 链；后：Part A hygiene |
| 开 PR 就绪度 | 60 | 95 | 前：业务可 PR、Harness 债另开；后：双 PR 闭环 |

---

## ST1–ST6（hygiene 前 → 后）

| # | 前 | 后 | 备注 |
| --- | --- | --- | --- |
| ST1 | partial | pass | review ✅；§3 原 &lt;15 行 → 已扩写 |
| ST2 | pass | pass | `6fbc862` 业务 commit |
| ST3 | pass | pass | task §自检结论已回填 |
| ST4 | pass | pass | `reinspect_gov-l2-manifest-ci_20260527_v1.md` |
| ST5 | fail | pass | 前：仅 git mv；后：done 头部 + `- [x]` |
| ST6 | partial | pass | RECENT §6.6 已有；§8 hygiene 行 + H5 |

---

## 平台偏差（Claude Code 特有）

| 项 | 观测 |
| --- | --- |
| **rules 加载** | 无 Cursor `.mdc`；依赖 `PROMPT_START` 显式必读列表 · **须人粘贴路径** |
| **semi_auto** | **同会话** 22→30→40→50→关账 · 5 commit · 未跳帽 |
| **invoke §3** | 首次执行多为 stub（30 占位「40 帽回填」）· 与 T4 expand 同类 |
| **关账顺序** | CLOSE commit 含 git mv + _views，**未**同批改 task 头部 done |
| **改进落盘** | `PROMPT_RETRO_hygiene_bc_v1.md` · PR #71 · rubric 收入本实验 |

---

## VERIFY 证据（业务 · 可复现）

```bash
python tools/tech_graph_test_manifest_check.py          # OK 12 entries
pytest tests/test_tech_graph_test_manifest_check.py -q  # 12 passed
pytest tests -m "not intent_eval and not intent_benchmark" -q  # 233 passed
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
```

---

## 证据链

| 类型 | 路径 |
| --- | --- |
| invoke | `docs/harness/invokes/by-task/gov-l2-manifest-ci/invoke_20260527_{22,30,40,50,CLOSE}_*.md` |
| review | `docs/harness/reviews/by-task/gov-l2-manifest-ci/task_governance_l2_manifest_ci_audit_R1_20260527.md` |
| reinspect | `docs/tasks/reinspect_results/reinspect_gov-l2-manifest-ci_20260527_v1.md` |
| task | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |
| commit（帽链） | `13d58d7` · `6fbc862` · `0084299` · `40f6b28` · `38a4711` |
| commit（hygiene） | `6ac40fe`（PR #71） |
