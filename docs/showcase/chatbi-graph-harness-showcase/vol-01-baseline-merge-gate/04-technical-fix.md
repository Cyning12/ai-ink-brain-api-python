---
title: "技术修复摘要"
slug: vol-01-04-technical
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "04"
status: stub
---

# 04 · 技术修复（非新功能）

## 大纲（待编写）

- [ ] `tests/conftest.py`：`INTENT_MIN_CONFIDENCE=0.6` · 与 `.env` 0.3 冲突根因
- [ ] `api/agent.py`：`CHATBI_V3_LOW_CONFIDENCE_CLARIFY` 增 `"on"`
- [ ] `_contract_manifest.json`：`frontend_ts_ignore_payload_like_keys` + `label`
- [ ] **未改** `unified_chat.py` 事件语义（task §9 根因摘要）
- [ ] Delta ADDED/MODIFIED 与实现一致表

## diff 锚点

- `tests/conftest.py` L25-27
- `api/agent.py` clarify_gate tuple
- `docs/_tech_graph/_contract_manifest.json`
