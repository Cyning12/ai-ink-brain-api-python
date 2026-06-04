---
title: "人类验收 · P0"
slug: vol-02-05-acceptance
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "05"
status: compiled
---

# 05 · 人类验收（P0）

> **前提**：`main` 已含 **#106 + #107**（`f53327a` 及之前 merge）

---

## 1. 能感受到的变化

| # | 验收项 | 如何感受 | 证据 |
| ---: | --- | --- | --- |
| 1 | **新 Graph 路由可调用** | curl POST 两路径 → 200 | Q-8 stub |
| 2 | **代码树出现 `api/graph/`** | 浏览仓结构 | state · runner |
| 3 | **共享模块独立文件** | `chatbi_events` 等可单独 import | agent 瘦身 |
| 4 | **全集 pytest 绿** | rebase 后 287 passed | #106 清基线债 |
| 5 | **CI 图谱门禁绿** | manifest + contract + drift | vol-02-06 |

---

## 2. 感受不到的变化（预期内）

| 项 | 说明 |
| --- | --- |
| **Ink Unified Chat 页面** | D-2 · 仍走 Legacy 路由 |
| **回答质量 / Timeline 新事件** | stub 非真实 Agent；**无** `graph.*` SSE |
| **Text2SQL / RAG 走 Graph** | P1 范围 |
| **前端选 Graph 入口** | D-4 defer · BFF 未改 |

---

## 3. 推荐验收脚本

```bash
cd ai-ink-brain-api-python

# A. P0 专测（10 项）
pytest tests/test_chatbi_graph_p0_foundation.py -q
# 期望：10 passed

# B. 合并前必绿全集（main 含 #106+#107）
pytest tests -m "not intent_eval and not intent_benchmark" -q
# 期望：287 passed, 1 skipped

# C. 图谱门禁
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_drift_check.py
# 期望：均 OK

# D. D-2：Legacy 未改
git diff 26e1c45..f53327a -- api/unified_chat.py
# 期望：空
```

---

## 4. Graph stub curl（本地 dev）

须配置与 Unified 相同的鉴权（Bearer / API key 视部署而定）。测试仓内用 override；**生产 curl 以 PROJECT_CONFIG 为准**。

```bash
# JSON stub（路径以本地 PORT 为准）
curl -sS -X POST "http://127.0.0.1:8000/api/py/unified/chat/graph" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"P0 graph stub"}' | jq .

# 期望字段示例：
# { "ok": true, "graph_stub": true, "run_id": "..." }

# SSE stub
curl -sS -N -X POST "http://127.0.0.1:8000/api/py/unified/chat/graph/stream" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"P0 graph stream"}' | head -20

# 期望：含 chain / done 事件与 graph_stub 标记
```

与专测断言一致：[`tests/test_chatbi_graph_p0_foundation.py`](../../../../tests/test_chatbi_graph_p0_foundation.py) `test_graph_*_route_stub`。

---

## 5. 与 vol-01 联合验收

若 **B 步仍 10 fail**，说明 **未** pull 含 #106 的 main — 先读 vol-01，勿误判 P0 回归。

---

## 6. 面试一句话

> 「P0 把 agent 里可复用的 SSE/失败处理抽成共享层，加了 Graph 并行 stub 路由和 10 个专测，Legacy unified_chat 零 diff；基线红项单独 PR #106 清掉后再合 Graph。」

---

## 指针

- 40 自检：task `### 自检结论（执行者）`
- 架构三层：[`_meta/ARCHITECTURE_LAYERS.md`](../_meta/ARCHITECTURE_LAYERS.md)
