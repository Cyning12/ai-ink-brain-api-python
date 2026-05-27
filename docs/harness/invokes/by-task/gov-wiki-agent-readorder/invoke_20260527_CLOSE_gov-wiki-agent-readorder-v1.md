# Invoke · CLOSE · gov-wiki-agent-readorder

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | CLOSE |
> | task | `docs/tasks/done/task_governance_wiki_agent_readorder_v1.md` |
> | task_slug | gov-wiki-agent-readorder |
> | freeze_id | GOV-WIKI-AGENT-READORDER@2026-05-27 |
> | git_branch | task/gov-wiki-agent-readorder-v1 |

---

## §1 ST1–ST6 合规自检

| # | 检查 | 结果 |
|---|------|------|
| ST1 | review R1 + invoke_22 | ✅ |
| ST2 | invoke_30 + 业务 commit | ✅ |
| ST3 | invoke_40 + task §自检 | ✅ |
| ST4 | reinspect + invoke_50 | ✅ |
| ST5 | done 头部 + git mv + _views + CLOSE invoke | ✅ |
| ST6 | RECENT §6.6/§8 · 无 Loop round 字段 | ✅ |

---

## §2 关账 hygiene（H1–H5）

| # | 项 | 结果 |
|---|----|------|
| H1 | reinspect 文件名 | ✅ `reinspect_gov-wiki-agent-readorder_20260527_v1.md` |
| H2 | `_views/done.md` | ✅ |
| H3 | RECENT §8 | ✅ |
| H4 | §6.6 Agent 读序 → done | ✅ |
| H5 | 交叉引用路径 | ✅ |

---

## §3 执行路线与 Commit 回溯

| 帽 | commit | 摘要 |
|----|--------|------|
| 22 | （见 git log） | R1 review + invoke_22 |
| 30 | （见 git log） | AGENTS + rules + CODING_WIKI + gen_agents_md + invoke_30 |
| 40 | （见 git log） | invoke_40 + task §自检 |
| 50 | （见 git log） | reinspect + invoke_50 |
| 关账 | （见 git log） | git mv · _views · RECENT · CLOSE invoke |

---

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：CLOSE
├── task：task_governance_wiki_agent_readorder_v1.md（done）
├── 分支：task/gov-wiki-agent-readorder-v1
├── 本棒交付：关账 + ST1–ST6 + hygiene
├── 下一棒：开 PR → gov-wiki-ingest-batch（用户授权不等待 CI）
└── 阻塞：无
```

---

## §5 给 PR reviewer

- 纯 docs/rules；合并前 `tech_graph_manifest_check.py` 应仍绿。
- 下一 Epic：`gov-wiki-ingest-batch`（10 slug syntheses）。
