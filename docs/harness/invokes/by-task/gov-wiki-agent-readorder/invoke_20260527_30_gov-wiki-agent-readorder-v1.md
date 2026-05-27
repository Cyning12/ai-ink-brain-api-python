# Invoke · 30 执行编码 · gov-wiki-agent-readorder

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 30 |
> | task_slug | gov-wiki-agent-readorder |
> | freeze_id | GOV-WIKI-AGENT-READORDER@2026-05-27 |
> | git_branch | task/gov-wiki-agent-readorder-v1 |

---

## §1 交付摘要

| # | 交付物 | 路径 |
|---|--------|------|
| 1 | AGENTS 必读第 5 条 | `AGENTS.md` |
| 2 | Cursor 规则 | `.cursor/rules/11-coding-wiki-readorder.mdc` |
| 3 | 自动同步规则小节 | `python tools/gen_agents_md.py` → `AGENTS.md` §Coding Wiki Readorder |
| 4 | CODING_WIKI §7 一句 | `docs/coding_wiki/CODING_WIKI.md` |

## §2 SPEC §2.3 对照

- 标题：**Coding Wiki（L2 编译层 · 关账回顾默认读序）** ✅
- 链：`CODING_WIKI.md` · Readorder SPEC · `index.md` ✅
- 读序：index → syntheses → L1；改代码仍 L0 ✅
- 禁止：不替代 L0 · 不默认 glob 全 invokes ✅
- L2 pointer：`_test_manifest` + L2 SPEC ✅

## §3 非范围确认

未改 `api/` · `tests/` · `.github/workflows/` · ingest 批量 · Harness prompts 正文。

## §4 下一棒（40）

重跑 SPEC §4 VERIFY · 回填 task §自检 · 落盘 invoke_40。

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── 本棒交付：AGENTS + rules + CODING_WIKI §7 + gen_agents_md
├── 下一棒：40 自检
└── 阻塞：无
```
