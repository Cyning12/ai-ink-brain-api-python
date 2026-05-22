# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | PR-1 · P0 gate_ctx_c_v1 materialize + pytest |

## 可复制 Prompt 快照

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）
- 子仓 AGENTS.md、task 内「给执行帽的必读」、根 AGENTS.md §8

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入（占位符已替换）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- 子仓根：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md
- 关联 SPEC / 总规：
Projects/docs/tech_graph/改进方向.md
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-v2-dual-track-execute.md（元数据表 + 快照 fenced code）。
0b. 复读 task Harness 表：若 HG-AUDIT-R1 仍为 pending → 仅输出须人改的 gate_id 与路径，拒开工。
1. 通读 task：§0.3 臂 D/E、§1.2 NR-1/2、P0～P2、§4 failure_paths、§5 必读；gates_before_code 已齐。
2. test_strategy required：先增 pytest（manifest 路径存在、query 种子节点在 graph_v2、D 臂子图规模阈值），再实现 fixtures/gate_ctx_c_v1/ 与 materialize_gate_c_payloads.py。
3. P0：protocol_version.yaml（锁定 freeze_id、graph_v2_freeze_id 引用、token 上限）；dual_track_manifest.json（每题 .ai.md + .md，非整包）；query_seeds.json（ENV/U2/A2 等真值节点）；勿覆盖 gate_ctx_ab_v1 / gate_ctx_b_v1 历史 run。
4. 臂 D：参考 materialize_gate_b_payloads.py，arm/schema 改为 CTX_V2_QUERY / gate_ctx_c_*；臂 E：按 manifest 拼接双轨原文。
5. 禁止：重跑闸口 A/B 主 batch（FP-C-1）；HG-P0-PROTOCOL pending 时跑付费 batch；整仓 .ai.md 灌入 E 臂。
6. PR-1 目标：P0 materialize exit 0 + 上述 pytest 绿；跑 task §3.3 主链 pytest；回填 task「### 自检结论（执行者）」。
7. 按 HANDOFF_AUTO_COMMIT 仅 commit 本轮路径；对话报 short-hash。

禁止：HG-AUDIT-R1 未 approved 时写业务代码；代填 human_gate；git add -A。
```
