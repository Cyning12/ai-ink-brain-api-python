# 单元 B · L2 Phase C 实现全链（cc · PR-B）

> **前置**：**PR-A 已合 `main`** ([#79](https://github.com/Cyning12/ai-ink-brain-api-python/pull/79))  
> **分支**：`task/wiki-unit-ab-plan-v1`（**不换分支**）

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_l2_phase_c_impl_v1.md` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.4 |
| **Unit AB** | `docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md` §3 |
| **SKILL** | `SKILL-harness-task.md` · `SKILL-docs-governance.md` |
| **22→关账** | [`PROMPT_TASK_22_to_CLOSE_v1.md`](./PROMPT_TASK_22_to_CLOSE_v1.md) |
| **test_strategy** | `required` → **须 50** |

---

## 1. 执行前自检

```bash
git checkout task/wiki-unit-ab-plan-v1
git pull origin main

grep -E 'HG-TASK-DRAFT.*approved' docs/tasks/active/task_governance_l2_phase_c_impl_v1.md \
  || { echo 'BLOCK: HG-TASK-DRAFT not approved'; exit 1; }

python tools/harness_human_gate_check.py --task docs/tasks/active/task_governance_l2_phase_c_impl_v1.md
```

---

## 2. 可复制 Prompt（cc · 全文）

见 [`PROMPT_TASK_22_to_CLOSE_v1.md`](./PROMPT_TASK_22_to_CLOSE_v1.md) §3。

---

## 3. PR-B diff 白名单（硬）

| 允许 | 禁止 |
|------|------|
| `tools/tech_graph_test_manifest_check.py` | `docs/coding_wiki/` 批量 |
| `tests/test_*phase*c*` 或等价 | `docs/harness/prompts/` 帽子正文 |
| `docs/_tech_graph/_test_manifest.json`（可选增量） | 与 PR-A 重复的 docs-only 大范围 |
| `docs/_tech_graph/99_spec.md` VERIFY 行 | |
