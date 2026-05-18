# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | task/engineering-tech-graph-gate-c-v2-dual-track-v1 |
| notes | PR-2 · P1 gate_ctx_c_v1 batch runner + dry-run pytest |

## 可复制 Prompt 快照

```text
你正在扮演工作区 Harness「执行编码帽（P1 · batch）」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
子仓 ai-ink-brain-api-python 分支：task/engineering-tech-graph-gate-c-v2-dual-track-v1

输入：
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md 
- 子仓根：ai-ink-brain-api-python
- 合并前验证：
pytest tests -m "not intent_eval and not intent_benchmark"
- 任务审核（R1）：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md
- SPEC / 总规：
Projects/docs/tech_graph/改进方向.md
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

【P0 已交付 · 勿重复造轮子】
- protocol / payloads：docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/
- materialize：fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
- pytest：tests/test_gate_ctx_c_v1_materialize.py

【对照实现（闸口 B · 仅参考，禁止改 B 的 run 目录）】
- fixtures/gate_ctx_b_v1/scripts/run_s0_gate_b.py
- fixtures/gate_ctx_b_v1/scripts/run_gate_b_batch.py
- 底层 S0 引擎：fixtures/gate_ctx_ab_v1/scripts/run_s0_minimal.py
- F1 打分（视臂名扩展或薄封装）：fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py

开帽前硬检查：
0. 将本消息全文落盘 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-p1-batch.md。
0b. 扫描 task human_gate：若对 30 为 pending → 拒开工并列出 gate_id。
1. 通读 task §0.3（D=CTX_V2_QUERY、E=CTX_DUAL_MD）、§1.2 NR-1/2、§3.2 P1、§4 FP-C-1/5、§5 必读。
2. test_strategy required：先增可失败测试（如 dry-run/mock 解析 batch_index、arm 路径映射），再实现 runner；禁止只跑脚本无测试。
3. 实现 gate_ctx_c_v1 batch（新文件，勿覆盖 gate_ctx_b_v1 / gate_ctx_ab_v1 历史 runs）：
   - run_s0_gate_c.py：臂映射
     · CTX_V2_QUERY → payloads/CTX_V2_QUERY/{task_id}.subgraph.json
     · CTX_DUAL_MD → payloads/CTX_DUAL_MD/{task_id}.dual_track.md
     · 复用 run_s0_minimal._execute_arm；protocol 读 gate_ctx_c_v1/protocol_version.yaml
     · schema 用 gate_ctx_c_*（勿写 gate_ctx_b_*）
   - run_gate_c_batch.py：3 题 × 默认两臂 CTX_V2_QUERY,CTX_DUAL_MD；输出
     docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_<ts>/
     含 batch_index.json、round_*/raw/*.jsonl、index.json
   - 跑 batch 前须 materialize exit 0；模型/温度与 protocol 一致（DeepSeek-V4-Flash · 0.2）
4. 执行 batch（须 SILICONFLOW_API_KEY / RUBRIC_REVIEW_BACKEND=siliconflow）：
   python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py
   若无 key（FP-C-5）→ 停止扩写，task 自检写明环境阻塞，不伪造 jsonl。
5. batch 成功后调用或扩展 score_gold_f1（臂名 D/E）；将复现命令写入 run README 或 batch_index 备注（供 P2 报告 §0）。
6. pytest 全绿；更新 task：§1.1 P1、§3.2 勾选；§6 实现备忘；§3.3 共用 pytest 勾选；追加「### 自检结论（执行者）」P1 小节。
7. HANDOFF_AUTO_COMMIT：仅 add 本轮路径；对话报 short-hash。

禁止：
- 调用 run_gate_b_batch / 重跑 gate_ctx_b_v1 全 arms（NR-2、FP-C-1）
- 修改 gate_ctx_ab_v1 / gate_ctx_b_v1 已有 runs/
- 整仓 .ai.md 作 E 臂（必须用已物化 dual_track）
- 代填 human_gate；git add -A
```
