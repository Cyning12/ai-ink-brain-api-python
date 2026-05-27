# Review · gov-wiki-agent-readorder · R1 · 2026-05-27

> **task_slug**: gov-wiki-agent-readorder
> **freeze_id**: GOV-WIKI-AGENT-READORDER@2026-05-27
> **task**: `docs/tasks/active/task_governance_wiki_agent_readorder_v1.md`
> **SPEC**: `docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md`
> **invoke_snapshot**: `docs/harness/invokes/by-task/gov-wiki-agent-readorder/invoke_20260527_22_gov-wiki-agent-readorder-v1.md`

---

## 审查结论摘要

**结论：可进入执行帽 · 无阻塞。**

本 task 将 Wiki-CTX-AB P2 **推荐默认读序** 常模化写入 `AGENTS.md` 必读链（+ 可选 `.cursor/rules`），并同步 `CODING_WIKI.md` §7 一句 pointer。

### 已核对项

| # | 项 | 结果 | 备注 |
|---|----|------|------|
| 1 | `HG-TASK-DRAFT` | approved | SPEC + AGENTS 改稿人扫 |
| 2 | `HG-AUDIT-R1` | approved | 本 review 为 R1 落盘 |
| 3 | `HG-READORDER-WORDING` | approved | 长链一次性执行授权 |
| 4 | 分支 | `task/gov-wiki-agent-readorder-v1` | 从 origin/main 拉出 |
| 5 | task 元信息 | 完整 | freeze_id / semi_auto / test_strategy N/A |
| 6 | 范围 | 清晰 | AGENTS · rules · CODING_WIKI §7 · Harness 落盘 |
| 7 | 验收 | 可执行 | SPEC §4 VERIFY + manifest_check hygiene |
| 8 | 非范围 | 明确 | 无 api/tests/ingest 批量/前端 |
| 9 | P2 依据 | 存在 | `conclusion_p2_zh.md` §3 推荐默认读序 |
| 10 | L2 前置 | done | `task_governance_l2_manifest_ci_v1` 已关账 |
| 11 | failure_paths F1–F3 | 可检 | 50 可对照 AGENTS 禁止项与 L0 保留 |
| 12 | ST1–ST6 | 可执行 | 单 task 帽链 invoke/reinspect 路径已约定 |

### 阻塞项

无。

---

## 需任务帽回填清单

无。

---

## 签收 / 关闭

本 task **可进入 30 执行编码帽**。22→30→40→50→关账 同会话连续执行。

---

## 下一棒可复制 Prompt

```text
你正在执行 gov-wiki-agent-readorder **30 执行编码**。

【必读】
- docs/tasks/active/task_governance_wiki_agent_readorder_v1.md
- docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md §2.3
- docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md §3

【交付】
1. AGENTS.md 必读第 5 条（Coding Wiki · 读序 · 禁止项 · L2 pointer）
2. .cursor/rules/11-coding-wiki-readorder.mdc + python tools/gen_agents_md.py
3. docs/coding_wiki/CODING_WIKI.md §7 一句链 Readorder SPEC
4. RECENT §6.6 Agent 读序行（draft→done 在关账 commit）

【VERIFY】
rg -n 'coding_wiki|Coding Wiki' AGENTS.md
python tools/tech_graph_manifest_check.py

【commit】HANDOFF_AUTO_COMMIT
```
