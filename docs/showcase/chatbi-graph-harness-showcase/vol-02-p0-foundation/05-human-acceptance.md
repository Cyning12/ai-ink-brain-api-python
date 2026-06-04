---
title: "人类验收 · P0"
slug: vol-02-05-acceptance
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "05"
status: stub
---

# 05 · 人类验收

## 能感受到

- [ ] 新路由 stub 200 / SSE 心跳（curl + 鉴权）
- [ ] 全集 pytest 287 passed（rebase 后）
- [ ] 代码树出现 `api/graph/` · 共享模块

## 感受不到

- [ ] 现有 Ink Unified Chat 页面行为
- [ ] 真实 Graph Agent 回答 / Timeline 新事件类型

## 复现（待填输出）

```bash
pytest tests/test_chatbi_graph_p0_foundation.py -q
curl -X POST .../api/py/unified/chat/graph -H "Authorization: Bearer ..." -d '{"query":"ping"}'
```
