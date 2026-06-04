---
title: "P0 五步交付"
slug: vol-02-02-deliverables
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "02"
status: compiled
---

# 02 · 五步交付

> 对齐 Roadmap **§4A.2** 执行顺序 · 实现 commit `b43ae3e`（rebase 前）· merge **`f53327a`**（#107）

---

## 1. 总览

| 步 | 交付 | 验收锚点 | 50 |
| ---: | --- | --- | ---: |
| ① | 共享层抽取 | `chatbi_events` · `chatbi_agent_models` · `chatbi_failure` | pass |
| ② | State + 边表 | `api/graph/state.py` · D-3 分表 | pass |
| ③ | runner stub | `api/graph/runner.py` · `run_graph_stub` | pass |
| ④ | 骨架路由 | `index.py` · `unified_chat_graph.py` · `_manifest` | pass |
| ⑤ | 专测 | `tests/test_chatbi_graph_p0_foundation.py` | **10/10** |

---

## 2. ① 共享层抽取

**动机**：`api/agent.py` 约 **1342 行**，SSE 事件构造、模型 dataclass、失败路由与 `run()` 耦在一起，Graph 与 Legacy 无法共用。

**迁出模块**：

| 模块 | 职责 |
| --- | --- |
| `api/chatbi_events.py` | `agent_chain` 等 SSE 事件工厂 |
| `api/chatbi_agent_models.py` | Agent 侧模型 / 常量 |
| `api/chatbi_failure.py` | `FailureTypeHandler` · 错误码路由 |

**结果**：`agent.py` **~1078 行**（50 复跑 `wc -l`）；**行为不变** — Legacy import 共享层，对外 SSE 类型集合不变。

专测：`test_chatbi_shared_modules_importable`

---

## 3. ② State + 边表（D-3）

```python
# api/graph/state.py（概念）
ChatBIState(run_id, query, current_node, partial, ...)
failure_edges_legacy()   # LLM_API_TIMEOUT → intent_v1_fallback
failure_edges_graph()    # LLM_API_TIMEOUT → direct_answer（方案 A）
resolve_failure_edge(..., graph=True/False)
```

| 测试 | 断言 |
| --- | --- |
| `test_graph_intent_timeout_scheme_a` | Graph 侧超时 → `direct_answer` |
| `test_legacy_intent_timeout_v1_fallback` | Legacy 保留 v1 fallback |
| `test_failure_edges_cover_main_codes` | 主错误码两表均覆盖 |

**Q-7 defer**：边表 **结构** 在 P0 冻结；SSE `ok` 字段语义 **不在本 Loop 冻结** → P1 Task-B。

---

## 4. ③ runner stub

`api/graph/runner.py` · `run_graph_stub(state)`：

- 设置 `current_node = "stub"`
- `partial["graph_stub"] = True`
- **无** ReAct 环 · **无** tool 调用

专测：`test_run_graph_stub_sets_node`

---

## 5. ④ 骨架路由（Q-8）

| 文件 | 职责 |
| --- | --- |
| `api/unified_chat_graph.py` | Graph HTTP 薄 handler（JSON / SSE） |
| `api/index.py` | 注册 `POST .../graph` · `.../graph/stream` |
| `docs/_tech_graph/_manifest.json` | Q-8 两 path 登记 |

鉴权模式与 Unified 一致（测试用 `install_unified_chat_auth_override`）。

专测：

- `test_graph_json_route_stub` — 200 · `ok` · `graph_stub` · `run_id`
- `test_graph_stream_route_stub` — SSE 含 chain/done · `graph_stub`

**D-2 证据**：

```bash
git diff origin/main...HEAD -- api/unified_chat.py
# （P0 分支）空
```

---

## 6. ⑤ 专测（required red-green）

```bash
pytest tests/test_chatbi_graph_p0_foundation.py -q
# 10 passed in ...
```

| # | 测试名 | 覆盖 |
| ---: | --- | --- |
| 1–3 | `test_failure_edges_*` | 边表 + D-3 |
| 4 | `test_run_graph_stub_sets_node` | runner |
| 5 | `test_chatbi_shared_modules_importable` | 共享层 |
| 6–7 | `test_graph_*_route_stub` | Q-8 HTTP |
| 8–10 | （边表 resolve 等） | Delta Scenario |

**全集 pytest**：P0 50 时 **277 pass · 10 fail**（main 基线债 · 非 P0 回归）；#106 合入 rebase 后 **287 pass**（见 vol-02-03）。

---

## 7. P0 Done vs 路线图

| 项 | P0（本卷） | P1（vol-04） |
| --- | --- | --- |
| Graph 真实 Agent 环 | stub only | intent→tool 环 |
| SSE parity | 最小 stub 事件 | Timeline 对齐 |
| 前端 BFF | 无改动 | 选 Graph endpoint |
| clarify/plan 上图 | 非范围 | Task-B |

---

## 指针

- Roadmap §4A：`docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`
- 50 验收表：`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`
