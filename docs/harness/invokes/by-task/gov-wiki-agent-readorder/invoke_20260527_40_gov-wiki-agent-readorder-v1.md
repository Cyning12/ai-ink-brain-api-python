# Invoke · 40 自检 · gov-wiki-agent-readorder

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 40 |
> | task_slug | gov-wiki-agent-readorder |
> | freeze_id | GOV-WIKI-AGENT-READORDER@2026-05-27 |
> | git_branch | task/gov-wiki-agent-readorder-v1 |

---

## §1 VERIFY（SPEC §4 + task）

| # | 命令 / 检查 | 结果 |
|---|-------------|------|
| R1 | `rg -n 'coding_wiki\|Coding Wiki' AGENTS.md` | **pass**（必读第 5 条 + 自动生成节） |
| R2 | AGENTS/rules 含「不替代 L0」「不默认扫全 invokes」 | **pass** |
| R3 | L2 `_test_manifest` / L2 SPEC pointer | **pass** |
| R4 | `python tools/tech_graph_manifest_check.py` | **pass** |
| — | `test -f docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md` | **pass** |
| — | `test -f .cursor/rules/11-coding-wiki-readorder.mdc` | **pass** |

## §2 task §自检回填

见 `docs/tasks/done/task_governance_wiki_agent_readorder_v1.md` §自检结论（关账 commit 同步）。

## §3 下一棒（50）

独立复检 · `reinspect_gov-wiki-agent-readorder_20260527_v1.md`。

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── VERIFY：4/4 pass
├── 下一棒：50 独立复检
└── 阻塞：无
```
