---
title: "图谱 CI 三分工"
slug: vol-03-03-ci
series: chatbi-graph-harness-showcase
vol: "03"
chapter: "03"
status: stub
---

# 03 · manifest / contract / drift

## 大纲（待编写）

- [ ] 三命令职责对比表（vol-02-06 展开）
- [ ] PR Required checks：`pytest` · `tech-graph` jobs
- [ ] Runbook 路径 A：同 PR 更 manifest + contract + md
- [ ] 本系列两次 CI 故事：#106 contract label · #107 drift 端点

## 必绿命令块

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
```
