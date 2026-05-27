# Reinspect · gov-wiki-agent-readorder · 2026-05-27

> **task_slug**: gov-wiki-agent-readorder
> **freeze_id**: GOV-WIKI-AGENT-READORDER@2026-05-27
> **分支**: task/gov-wiki-agent-readorder-v1
> **复检人**: Agent（独立重跑）
> **结论**: **建议合并 · 无阻塞项**

---

## §1 独立 VERIFY

| # | 检查项 | 命令 | 结果 |
|---|--------|------|------|
| 1 | AGENTS 必读链 | `rg -n 'coding_wiki\|Coding Wiki' AGENTS.md` | **pass** |
| 2 | Readorder SPEC 存在 | `test -f docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md` | **pass** |
| 3 | rules 存在 | `test -f .cursor/rules/11-coding-wiki-readorder.mdc` | **pass** |
| 4 | 图谱 hygiene | `python tools/tech_graph_manifest_check.py` | **pass** |
| 5 | L0 必读未删 | `rg -n 'docs/_tech_graph/' AGENTS.md` | **pass**（L0 项仍为第 3 条） |
| 6 | 禁止项 | `rg '不替代|glob.*invokes' AGENTS.md .cursor/rules/11-coding-wiki-readorder.mdc` | **pass** |
| 7 | CODING_WIKI §7 | `rg 'SPEC-Governance-Wiki-Agent-Readorder' docs/coding_wiki/CODING_WIKI.md` | **pass** |

## §2 范围纪律

| 检查项 | 结果 |
|--------|------|
| 未改 `api/` | pass |
| 未改 `tests/` | pass |
| 未改 workflow | pass |
| 未改 Harness prompts 正文 | pass |

## §3 结论

**7/7 pass · 建议合并。** 下一棒：关账（git mv · _views · RECENT §6.6 · CLOSE invoke · ST1–ST6）。
