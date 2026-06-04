---
title: "人类验收"
slug: vol-01-05-acceptance
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "05"
status: compiled
---

# 05 · 人类验收（基线闸）

> 维护者 / 面试演示用：**15 分钟内**可核对「本 PR 到底改变了什么」。

---

## 1. 能感受到的变化

| # | 验收项 | 如何感受 | 证据 |
| ---: | --- | --- | --- |
| 1 | **main CI 基线绿** | GitHub Actions `pytest` + `contract_check` 在 #106 合并后稳定 | merge `26e1c45` |
| 2 | **本地 10 v3 测不再神秘失败** | 即使 `.env` 有 `INTENT_MIN_CONFIDENCE=0.3`，pytest 仍过 | `conftest` 固定 0.6 |
| 3 | **contract CI 不再因 label 红** | `tech_graph_contract_check` exit 0 | manifest 已登记 |
| 4 | **P0 可 rebase 合 main** | vol-02 PR #107 在 rebase 后 **287 passed** | 系列时间轴 |

---

## 2. 感受不到的变化（预期内）

| 项 | 说明 |
| --- | --- |
| **Ink Unified Chat 页面** | 无新 UI、无新路由；回答风格不应 intentional 变化 |
| **Graph Agent** | 本 PR **无** `api/graph/*` |
| **新 SSE 事件类型** | 无 `graph.*`；v3 事件集合不变 |
| **产品级 plan/clarify 大改** | 修复以 **测试/配置/manifest 真值** 为主（见 vol-01-04） |

若演示时用户觉得「聊天变聪明了」，应怀疑 **环境/数据** 而非本 PR。

---

## 3. 推荐验收脚本（复制即用）

```bash
cd ai-ink-brain-api-python   # 仓根

# A. 10 个 v3 基线用例
pytest tests/test_unified_chat_backend_v2_agent.py \
  -k "v3 and (plan or low_confidence)" -q
# 期望：10 passed

# B. 合并前必绿全集
pytest tests -m "not intent_eval and not intent_benchmark" -q
# 期望：277 passed, 1 skipped（2026-06-04 基线口径）

# C. 契约与 manifest
python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py
# 期望：均 OK

# D. 确认未夹带 P0
git diff 26e1c45^..26e1c45 --name-only | rg 'api/graph|p0_foundation' || echo "无 P0 路径"
```

---

## 4. 与 vol-02 的衔接验收

基线闸合并后，在 **`origin/main`** 上：

```bash
git fetch origin main && git checkout main && git pull
pytest tests -m "not intent_eval and not intent_benchmark" -q
```

应 **全绿**（含后续 P0 合入后为 287 passed）。若仍红，**不要**开 P0 叙事 — 先查是否未 pull 最新 main。

---

## 5. 面试 / 投递一句话

> 「P0 Graph 50 复检发现 main 有 10 个 v3 测和 contract 红项，我们按 Harness 单独开基线 task，PR #106 先合 main，再 rebase 合 P0；本地与 CI 真值对齐，没有删测过关。」

短稿扩写：[`vol-90-portfolio/01-elevator-30s.md`](../vol-90-portfolio/01-elevator-30s.md)

---

## 指针

- 40 自检表：task `### 自检结论（执行者）`
- 50 验收表：[`reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md`](../../../tasks/reinspect_results/reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md)
