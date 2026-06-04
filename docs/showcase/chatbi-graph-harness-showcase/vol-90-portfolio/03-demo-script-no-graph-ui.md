---
title: "无 Graph UI 演示脚本"
slug: vol-90-03-demo
series: chatbi-graph-harness-showcase
vol: "90"
chapter: "03"
status: compiled
draft_version: v0.10
aligned_spec: docs/spec/governance/投递冲刺_20260609_v1_zh.md
---

# 03 · 演示脚本（无 Graph UI · 约 8 分钟）

> **场景**：远程面试 / 录屏 · **无 Ink Graph 页面**（P1 前正常）  
> **前提**：本地或 GitHub 上 main 已含 **#106 + #107**（`f53327a` 及之前）

---

## 0. 开场白（30 秒）

「这段演示的是 **后端治理 + P0 地基**，不是成品 Graph 对话。我会用 CI、pytest、curl 和 Harness 落盘证明：main 全绿、Legacy 未改、Graph 路由已 stub 注册。真实 Agent 环在 P1。」

---

## 1. GitHub Actions 全绿（~1 min）

**展示**：仓库 `ai-ink-brain-api-python` → Actions

| PR | 看什么 |
| --- | --- |
| [#106](https://github.com/Cyning12/ai-ink-brain-api-python/pull/106) | pytest · tech-graph（manifest + drift） |
| [#107](https://github.com/Cyning12/ai-ink-brain-api-python/pull/107) | 同上 · 注意 #107 曾触发 **drift_check** 后修复 |

**口播**：「#107 教会我 manifest 登记了端点，叙述层 `99_spec.md` 也要写，否则 drift 仍红。」

---

## 2. 终端 · 合并前必绿（~2 min）

```bash
cd ai-ink-brain-api-python

# 全集
pytest tests -m "not intent_eval and not intent_benchmark" -q
# 口播：287 passed — 含 #106 清掉的 10 个 v3 基线测

# P0 专测
pytest tests/test_chatbi_graph_p0_foundation.py -q
# 口播：10 passed — P0 五步 red-green

# 图谱三门
python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
# 口播：三门 OK — contract label 在 #106 已登记
```

**D-2 Spot check**（可选 · 10 秒）：

```bash
git log -1 --oneline f53327a
git diff 26e1c45..f53327a -- api/unified_chat.py
# 期望：无输出
```

---

## 3. curl · Graph stub vs Legacy（~2 min）

**启动 API**（按本机 PROJECT_CONFIG；以下为示意）：

```bash
# 若已有 dev server 在 8000，跳过
# uvicorn api.index:app --reload --port 8000
```

```bash
# Graph JSON stub（Q-8）
curl -sS -X POST "http://127.0.0.1:8000/api/py/unified/chat/graph" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"demo stub"}' | jq .

# 期望：ok=true, graph_stub=true, run_id=...

# Graph SSE stub
curl -sS -N -X POST "http://127.0.0.1:8000/api/py/unified/chat/graph/stream" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"demo stream"}' | head -15
```

**口播**：

- 「这是 **stub**，不是 RAG/Text2SQL 真回答。」
- 「Ink 页面仍走 `/unified/chat/stream` — **产品行为未切 Graph**。」

鉴权 token 获取方式见 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（勿在录屏中泄露密钥）。

---

## 4. Harness 落盘 · 可追责（~2 min）

**浏览器打开**（相对仓根）：

1. [`docs/showcase/chatbi-graph-harness-showcase/README.md`](../README.md) — 系列读序
2. [`vol-01-baseline-merge-gate/06-evidence-index.md`](../vol-01-baseline-merge-gate/06-evidence-index.md) — #106 证据
3. [`vol-02-p0-foundation/07-evidence-index.md`](../vol-02-p0-foundation/07-evidence-index.md) — #107 证据
4. [`docs/tasks/reinspect_results/`](../../../tasks/reinspect_results/) — **50 独立复检**（Fresh Context）

**口播**：「50 不复读 30 invoke 长文，只对照 task + diff + 命令 — 这是 P1 规约里的 Fresh Context。」

---

## 5. 收尾 · 诚实边界（~30 秒）

| 已完成 | 未做（P1+） |
| --- | --- |
| main CI 绿 · 共享层 · Graph stub 路由 | Graph 真实 Agent 环 |
| Harness 两 PR 闭环 · reinspect 落盘 | Ink Graph Timeline / BFF 选路 |
| Legacy Unified **行为不变** | clarify/plan 上图 · SSE parity |

**禁演示**：Ink 上「Graph 模式」切换 · 多 Agent handoff 平台（6/9 后另 task）。

---

## 6. 故障备选

| 情况 | 备选 |
| --- | --- |
| 本地无 Supabase/密钥 | 只演示 **GitHub Actions + 文档落盘**；pytest 用 CI 截图 |
| curl 401 | 改讲专测 `test_graph_*_route_stub` 已覆盖 HTTP 200 |
| 面试官要前端 | 打开 Ink **现有** Unified Chat，强调「Legacy 路径未变」 |

---

## 指针

- 电梯稿：[`01-elevator-30s.md`](01-elevator-30s.md)
- STAR：[`02-star-skeleton.md`](02-star-skeleton.md)
- 证据索引：[`_meta/EVIDENCE_LINKS.md`](../_meta/EVIDENCE_LINKS.md)
