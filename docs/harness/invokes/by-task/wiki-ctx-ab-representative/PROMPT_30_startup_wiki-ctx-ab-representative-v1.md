# 启动 Prompt · 30 执行帽 · Wiki-CTX-AB Representative（v1.0）

> **帽链**：22 → **30** → 40 → 50 → 关账  
> **用法**：22 R1 无阻塞后 · 同会话 semi_auto 续跑 → 复制下方代码块。  
> **前置**：`docs/harness/reviews/by-task/wiki-ctx-ab-representative/task_governance_wiki_ctx_ab_representative_audit_R1_20260527.md`

---

```text
你正在扮演 Harness「执行帽（30）」（Wiki-CTX-AB **代表性 6 slug** · 实验 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/templates/TEMPLATE-execute-invoke.md §3
- docs/spec/governance/SPEC-Governance-Wiki-CTX-AB-Representative-v1.md
- docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md（方法论 · 只读）
- docs/tasks/done/task_wiki_ctx_ab_multi_slug_v1.md（2 slug 先例 · 只读）
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc

【开帽】将本 user 消息全文落盘至：
docs/harness/invokes/by-task/wiki-ctx-ab-representative/invoke_YYYYMMDD_30_wiki-ctx-ab-representative-v1.md

输入：
- 主 task：docs/tasks/active/task_governance_wiki_ctx_ab_representative_v1.md
- git_branch：task/wiki-ctx-ab-representative-v1
- freeze_id：WIKI-CTX-AB-REP@2026-05-27
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab-representative/task_governance_wiki_ctx_ab_representative_audit_R1_20260527.md
- test_strategy：not_applicable

锁定 slug（HG-AB-REP-SLUGS · 6）：
1. harness-p1-docs-consolidation
2. tech-graph-gate-d-v2-tasks
3. chatbi-v3-p2-health-ready
4. governance-l2-manifest-ci
5. wiki-ctx-ab-v1
6. harness-wiki-loop-t4-l2

0b. 全部 human_gate 须 approved（含 HG-AB-REP-RUN）。

你必须完成（按序）：

1. 物化 payload（**仅** docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/）：
   · W：每 slug `python tools/wiki_ctx_ab_materialize_w.py --slug <slug>`，复制到本实验 payloads/，更新元信息 freeze_id 为 WIKI-CTX-AB-REP@2026-05-27（**禁止覆盖** wiki_ctx_ab_v1/payloads/）
   · H-lean：按 TEMPLATE-H-lean + Multi 先例（README §1+§2.1 · invokes README 摘录 · done task 全文 · RECENT 关键词行），每 slug 一份 H-lean_<slug>.md + payload_char_count

2. 按 questions.md 跑题：每 slug **Q1–Q4** × **H-lean** × **W**；W 臂 **禁止** harness/done 全文。

3. 填写 scorecard.md（逐条 + §聚合 T7/T8/T6）。

4. 撰写 conclusion_representative_zh.md：签收 / 局限 / **前端 P1-4 建议**（SPEC §5）。

5. 更新 docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md **#46**（附条件外推 · 链 scorecard）。

6. 回填 task §实现备忘 · §自检结论（30 草稿）。

7. Commit：实验目录、task、invoke；message 含 WIKI-CTX-AB-REP@2026-05-27。

8. semi_auto：落盘 invoke_30 并 commit 后 **续跑 40**（同会话）。

禁止：改 api/、tests/、CI、前端仓；改 wiki_ctx_ab_v1 已冻结结论文；擅自改 6 slug 名单

关键词：30、Representative、6 slug、H-lean、W、scorecard、conclusion_representative、P1-4 证据
```
