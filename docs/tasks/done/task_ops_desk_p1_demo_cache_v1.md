# Task · Ops Desk P1-6 · Demo Cache

> **状态**：`done（2026-06-22 验收通过）`  
> **SPEC**：§4.3 · §7  
> **invoke**：[`ROUND_07_R6_demo_cache_chat.md`](../../../../docs/harness/invokes/by-task/ops-desk-kimi-code-spec-refine/rounds/ROUND_07_R6_demo_cache_chat.md)  
> **依赖**：P1-3 orchestrator merge **`b0af89df`**  
> **后继**：P1 Demo 人类验收（与 P1-5 合并 · 非 merge 阻塞）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p1-demo-cache` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P1-DEMO-CACHE` |
| **git_branch** | `task/ops-desk-p1-demo-cache` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |

---

## 背景与目标

`ops_demo_answers` 表 + fast path / deep 首次结果缓存 · 支撑面试 Demo 与 LLM 断联兜底。

### 完成态

- [x] `supabase/sql/ops_desk_p1_demo_cache.sql` + rollback
- [x] D1–D3 metrics 类 demo 题：sync 后可预计算或按需写入（R6 §3.2）
- [x] D4/D6 类深析：首次 deep run 成功后缓存 24h（`expires_at`）
- [x] Orchestrator fast path：`demo hit` 读缓存 · 无 LLM
- [x] `tests/ops_desk/test_demo_cache_p1.py`（required）
- [ ] 可选：GHA 或 sync 后 hook 预计算 D1–D3（最小：脚本 + 单测 mock）

---

## Demo 题（P1 最小 4 题）

| demo_id | 意图 | 说明 |
| --- | --- | --- |
| D1 | metrics_trend | open issue 30 天 |
| D2 | metrics_trend | PR cycle time |
| D3 | metrics_trend | review time |
| D4 | issue_contribution | #545 适合我做吗（默认 issue） |

---

## 非范围

- 前端 Chat UI（P1-5）
- graph/scan demo（P2 · D5/D8）
- 人类 checklist（并入 P1 Demo）

---

## 验收标准

脚本级 merge 卡点：

- [x] pytest `test_demo_cache_p1.py` + 全量 pytest 绿
- [x] fast demo 命中无 LLM 调用（assert）
- [x] TTL 过期后 miss → 正常路径
- [x] ruff check api/ops tests/ops_desk 绿
- [x] `verify-tech-graph` 未改图谱，无需执行

---

## 失败路径

| 失败场景 | 影响 | 兜底 |
| --- | --- | --- |
| `ops_demo_answers` 表不存在 | demo cache 全 miss | 命中 demo 题后走原有 fast/deep 路径，不阻塞对话 |

---

## 给 Cursor

`ops-desk-p1-demo-cache` · 可与 P1-5 **并行** · 独立 PR merge。
