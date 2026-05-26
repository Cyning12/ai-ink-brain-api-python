---
title: 测试过程档案以单测/契约为先，不在 Wiki 维护用例清单
slug: unit-first-test-archive
layer: L2
status: compiled
freeze_id: CODING-WIKI-T1C@2026-05-26
closed_date: 2026-05-26
---

# 决策：L2 只存档测试变更过程，不镜像 pytest 全集

## 决议（append-only）

1. **禁止**在 `docs/coding_wiki/` 维护与 `tests/` 目录同步的「用例清单真值表」或 coverage 数字（见 `CODING_WIKI.md` §8、task T1c `failure_paths` F2）。
2. **可观测 / metadata 类**交付（如 RAG `query_compare`、ChatBI `text2sql_phases_ms`）在 Wiki 中记录 **意图、新增/修改的单测路径、验收命令 pointer**；是否补 Supabase/SSE 全链路 e2e 由 **L1 task 非范围** 与 CI 既有 marker 决定，**不以 Wiki 为准**。
3. **机器校验**（锚点、`_test_manifest`、图谱 `ERR_*`）归 **L0 工具链**；Wiki 仅帮助 Agent 理解「为何这样测」。

## 背景

- ingest：`task_05_query_rewrite_observability`、`task_chatbi_v3_text2sql_tool_latency_obs_v1`（T1c 锁定范围）。
- 对比表缺口 #15：`decisions/` 首条；关账后对比表 #7、#15 可标 **done**。

## 指针

- Schema：→ `docs/coding_wiki/CODING_WIKI.md` §8  
- 策略概念：[[../concepts/test-strategy-ink-backend]]  
- 主 task：→ `docs/tasks/done/task_coding_wiki_t1c_test_archive_v1.md`（关账后路径）
