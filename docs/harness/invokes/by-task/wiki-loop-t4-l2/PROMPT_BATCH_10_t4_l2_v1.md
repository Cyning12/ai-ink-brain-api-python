# 启动 Prompt · 一次性 Batch-10 · Wiki Loop T4+L2（v1）

> **只运行一次**（**已执行** 见 [`invoke_20260527_10_batch_t4_l2_v1.md`](./invoke_20260527_10_batch_t4_l2_v1.md)）。后续每轮 **仅** [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md)。  
> **分支**：`task/gov-spec-t4-l2-v1`

---

```text
你正在扮演 Harness「需求与任务分析帽（10）· Batch 模式」……

【背景】
治理 P2：T4 Wiki↔图谱桥接 + L2 _test_manifest 已有 draft SPEC（commit b3a4c06+）。
第四轮 harness-loop-batch **真实业务** Loop；**先 T4（R1→R2）再 L2（R3）**；单 PR docs-only。

【loop-slug】wiki-loop-t4-l2
【git_branch】task/gov-spec-t4-l2-v1
【freeze_id 母】WIKI-LOOP-T4-L2@2026-05-27

【开帽】invoke → docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_YYYYMMDD_10_batch_t4_l2_v1.md

【须落盘 1 母 + 3 子 task】路径见 invoke_20260527_10_batch_t4_l2_v1.md 表。

母 task：HG-LOOP-BATCH pending · R1→R2→R3→META · 链 MANIFEST / PROMPT_LOOP / PROMPT_START
R1：T4 Pilot · query-rewrite-observability · CODING_WIKI · RECENT in_progress
R2：99_spec T4 小节 · VERIFY（依赖 R1 done）
R3：_test_manifest.json ≥5 · 99_spec/CODING_WIKI 指针 · RECENT done（依赖 R2 done）

【停】勿执行 22；人批闸后 PROMPT_START 全链。
```

完整字段真值见已落盘 task 正文 · [`SKILL-harness-loop-batch.md`](../../../tasks/skills/SKILL-harness-loop-batch.md)。
