---
title: "人类验收"
slug: vol-01-05-acceptance
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "05"
status: stub
---

# 05 · 人类验收

## 大纲（待编写）

### 能感受到

- [ ] main / PR **pytest + contract** 全绿
- [ ] 本地开发者：10 v3 测不再因 `.env` 低阈值神秘失败

### 感受不到

- [ ] Unified Chat **UI / 回答质量** 无 intentional 变化
- [ ] 无新路由、无 Graph

## 复现命令（待粘贴 40/50 输出要点）

```bash
pytest tests/test_unified_chat_backend_v2_agent.py -k "v3 and (plan or low_confidence)" -q
python tools/tech_graph_contract_check.py
```
