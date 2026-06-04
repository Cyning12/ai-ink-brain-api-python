---
title: "两类基线红项"
slug: vol-01-02-problem
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "02"
status: compiled
---

# 02 · 问题：两类基线红项

> 以下问题在 **`origin/main` 上已存在**；本卷 PR #106 的目标是 **消除合并阻塞**，而非新增 ChatBI 产品能力。

---

## 1. 红项 A：10× v3 plan/clarify pytest

### 1.1 位置与典型症状

- **文件**：`tests/test_unified_chat_backend_v2_agent.py`
- **主题**：ChatBI v3 **plan preview**、**execution_token**、**low-confidence clarify** 短路
- **典型断言**：SSE/JSON 应含 `agent.plan.preview` 等事件；或 clarify 路径应跳过 text2sql

### 1.2 完整用例名单（10 个）

| # | 测试函数 |
| ---: | --- |
| 1 | `test_v3_low_confidence_clarify_json_skips_text2sql` |
| 2 | `test_v3_plan_preview_json_includes_plan_preview_and_ttl_notice` |
| 3 | `test_v3_plan_execution_token_json_bypasses_clarify` |
| 4 | `test_v3_plan_execution_token_invalid_json_denies_bypass` |
| 5 | `test_v3_plan_preview_fail_json_no_token` |
| 6 | `test_v3_plan_preview_sse_parity` |
| 7 | `test_v3_rag_plan_preview_json_includes_rewrite_query` |
| 8 | `test_v3_rag_plan_execution_token_json_bypasses_clarify` |
| 9 | `test_v3_rag_plan_preview_fail_json_no_token` |
| 10 | `test_v3_rag_plan_preview_sse_parity` |

### 1.3 本地快速复现（修复前）

```bash
pytest tests/test_unified_chat_backend_v2_agent.py \
  -k "v3 and (plan or low_confidence)" -q
# 修复前：10 failed（开发者 .env 低 INTENT_MIN_CONFIDENCE 时尤其稳定复现）
```

### 1.4 根因（本 PR 口径 · 见 vol-01-04）

并非「生产代码缺 emit 逻辑」为主因，而是 **测试环境真值** 与 CI/规格默认不一致：

- 开发者 `.env` 常见 `INTENT_MIN_CONFIDENCE=0.3`
- stub 意图 confidence=**0.35** 无法触发 clarify 分支
- CI 无 `.env` 时默认 **0.6**，行为与本地不一致 → **main 与本地表现分裂**

---

## 2. 红项 B：`tech_graph_contract_check` · `label`

### 2.1 症状

```text
contract 未声明字段: label
（frontend_anchors.sse_consumer_files 扫描）
```

- 前端 `UnifiedChatPageClient.tsx` 读取 SSE payload 上的 **`label`**
- `_contract_manifest.json` **未**声明或列入 ignore 列表
- Runbook：**路径 A** — 若判定为 UI 辅助字段，同 PR 更新 manifest

### 2.2 与 P0 的关系

P0 抽取 `chatbi_events.py` 后，contract 扫描面变大，但 **`label` 漂移在 main 已红**；50 复检已区分「P0 增量 OK」与「基线债阻塞 Strict merge」。

---

## 3. 验收口径（task 字面）

| 命令 | 期望 |
| --- | --- |
| 上述 10 测 | **全部 pass** |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | **全绿** |
| `python tools/tech_graph_contract_check.py` | **exit 0** |

合并前必绿见根 `AGENTS.md` §8 与本仓 `pytest.yml` workflow 名 **`pytest`**。

---

## 4. 本卷明确不做

- P0 Graph 五步（`api/graph/*`、Q-8 路由、`test_chatbi_graph_p0_foundation.py`）
- 删测、放宽断言、改 marker 排除
- 修改 `unified_chat.py` 产品语义（本 PR 以环境/配置/manifest 对齐为主）

## 指针

- Runbook：[`RUNBOOK_graph_contract_ci_red_v1.md`](../../../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md)
- 失败路径 Scenario：`fp-baseline-v3-plan-regression` · `fp-baseline-contract-label-drift`（task §失败路径）
