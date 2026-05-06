# Task：ChatBI V2 Agent（P1-C）— IntentCache（LRU+TTL）与可观测性（v1）

状态：pending  
范围：仅后端 `ai-ink-brain-api-python`  
前置：P1-P0 已具备评测闭环脚本（accuracy/latency/agent-e2e）  
关联：
- `docs/tasks/active/task_chatbi_v2_agent_p1_behavior.md`（P1 总览）
- `docs/tasks/active/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`（P1-Eval：评测/基准主线；与本任务并行时共享「CI 不调外部 LLM」约束）
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Intent.md`（缓存策略：key=query+history_hash）

---

## 背景与目标

前置建议：P1-Eval 已具备 **accuracy / latency** 最小脚本与门禁口径后再合入缓存对比数据更顺；若并行开发，以各任务单验收为准。

当前 `api/intent_agent.py` 已具备最小缓存对象 `_intent_cache`，但仍存在缺口：

- **key 不包含 history**：相同 query 在不同上下文可能产生不同意图，必须隔离缓存污染
- **缺少明确可观测字段**：难以在日志/trace 中衡量 cache hit 对延迟的收益
- **缺少“命中率/收益”复跑口径**：无法在 diary 报告里给出可复现的提升数据

目标：在不引入新事件类型、不破坏现有行为的前提下，把 IntentCache 按 spec 完整落地，并产出可复跑的基准对比。

---

## 范围 / 非范围

### 范围

- [ ] 在 `api/intent_agent.py` 落地 IntentCache：**LRU + TTL**（maxsize=1000，TTL=300s）
- [ ] 缓存 key：`query + history_hash`（仅取最近 3 轮对话）
- [ ] 记录 cache_hit/cache_miss（字段级）：允许写入现有日志/trace（不得新增事件 type）
- [ ] 产出对比数据：同一组 query 连续跑两轮（冷启动 vs 热缓存）对比 Intent P50/P95

### 非范围

- 不做 Prompt 调优（P1-D）
- 不引入新事件 type / 新接口
- 不改动前端交互体验

---

## 设计约束（必须遵守）

- **CI 不触发真实 LLM 外部调用**：真实评测由本地手动开关执行
- **不新增事件类型**：仅允许在已有 payload / metadata / server log 中新增字段
- **安全**：缓存内容不得包含敏感信息；仅缓存意图决策结构（tool/mode/confidence/reasoning摘要）

---

## 实现要点（建议方案）

### 1) history_hash 计算口径（必须稳定）

- 取最近 3 轮对话：`history[-6:]`（user/assistant 交替）或按现有 intent_history 的格式取 `[-3:]`
- 仅使用 `role + content`，并做 JSON 序列化（`sort_keys=True`，`ensure_ascii=False`）
- hash：`sha256(...).hexdigest()[:16]`（或 md5[:16] 亦可，但建议 sha256）

### 2) cache value（建议）

缓存 `IntentDecision`（或可序列化的 dict）即可；无需缓存 raw_response 全量（避免体积与敏感信息风险）。

### 3) 可观测字段（不新增事件类型）

优先在 `IntentDecision.raw_response` 增加字段（示例）：

- `cache`: `"hit" | "miss"`
- `cache_key_hash`: `str`（可选，避免暴露 query）
- `latency_ms`: `int`（若 intent_agent 内可测量）

也允许写 server log（仅在 DEBUG 开关下）：

- `[intent-cache] hit/miss key=... latency_ms=...`

---

## 验收标准（阻断项）

### 功能验收

- [ ] key 包含 history_hash：不同 history 的同 query **不会**命中同一缓存
- [ ] TTL 到期后自动失效
- [ ] maxsize 生效：超过容量后按 LRU 淘汰

### 性能验收（本地手动）

- [ ] 相同 query 第二次命中缓存：Intent 延迟 < 10ms（本地测量）
- [ ] `tests/benchmark_intent_latency.py` 支持“冷/热两轮对比”输出（或新增最小脚本）

### 可观测性验收

- [ ] 评测输出（JSONL/console）中能看到 cache_hit/cache_miss
- [ ] diary 报告能给出一次“冷启动 vs 热缓存”的 P50/P95 对比（可复跑）

---

## 交付物

- `api/intent_agent.py`：IntentCache（LRU+TTL）+ key=query+history_hash（最近 3 轮）
- `tests/benchmark_intent_latency.py`（或新增 `tests/benchmark_intent_latency_cache.py`）：冷/热对比输出
- `docs/diary/YYYY-MM-DD-p1-intent-cache.md`：命中率与延迟收益（含复跑命令）

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件（预期） | `api/intent_agent.py`、`tests/benchmark_intent_latency.py`、`docs/diary/*.md` |
| env（预期） | 复用 `CHATBI_V2_INTENT_LLM`；可新增 `DEBUG_INTENT_CACHE=1`（如确需） |
| 输出格式 | JSONL（逐条记录 cache 字段 + latency） |

