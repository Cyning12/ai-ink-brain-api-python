# Task：ChatBI V2 Agent（P1 行为正确性）— 意图准确率、性能基准与缓存

状态：pending  
范围：仅后端 `ai-ink-brain-api-python`  
前置：P0 已完成（`task_chatbi_v2_agent_p0_backend.md` 已归档）  
关联：
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` — 性能指标 P50/P95
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Intent.md` — 测试集 60 条、缓存策略
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Gap-Checklist.md` — P1 缺口项

---

## 背景与目标

P0 完成了 V2 Agent 骨架（ReAct 循环、事件流、契约、回归测试），但当前测试基于 **stub（mock 意图决策）**，未验证真实 LLM 意图识别的准确率与性能。

P1 目标：
1. **真实 LLM 意图验证**：关闭 stub，验证 DeepSeek-V3 / Qwen-Turbo 的实际决策质量
2. **准确率基准**：60 条测试集，macro-F1 > 90%
3. **性能基准**：Intent P50 < 200ms，P95 < 500ms
4. **缓存落地**：`_intent_cache` LRU 实现，降低重复 query 成本

---

## 范围 / 非范围

### 范围

1. **真实 LLM 意图测试**
   - 关闭 `CHATBI_V2_INTENT_LLM=false`，用真实 SiliconFlow API 跑 60 条测试集
   - 记录每条 query 的：实际 tool、confidence、reasoning、延迟
   - 输出准确率报告（macro-F1 / per-class F1 / confusion matrix）

2. **性能基准测试**
   - Intent 决策延迟：P50 / P95 / P99
   - Agent 单步延迟：P50 / P95
   - 整体端到端延迟：P50 / P95

3. **意图缓存实现**
   - `api/intent_agent.py` 中 `_intent_cache` 落地
   - LRU 策略：maxsize=1000，TTL=300s（5 分钟）
   - 缓存 key：query + history_hash（最近 3 轮对话的 hash）

4. **测试集扩展**
   - 从当前 10 条 stub 扩展到 60 条真实用例
   - 分类：Text2SQL 20 + RAG 20 + Direct 10 + 多轮 10
   - 覆盖口语化、模糊表达、边界 case

### 非范围

- 不改动 P0 已稳定的骨架代码（agent.py / tools.py / unified_chat.py）
- 不在本任务内新增事件类型（事件/契约变更请见：`task_unified_chat_router_evidence_event_v1.md`）
- 不改动前端

---

## 验收标准（必须可操作）

### 1) 准确率验收（阻断项，P1）

- [ ] 60 条测试集全部跑过（真实 LLM）
- [ ] macro-F1 > 90%
- [ ] Text2SQL 召回率 > 85%（20 条中至少 17 条正确）
- [ ] RAG 召回率 > 90%（20 条中至少 18 条正确）
- [ ] Direct Answer 准确率 > 95%（10 条中至少 9 条正确）
- [ ] 多轮准确率 > 80%（10 条中至少 8 条正确）

### 2) 性能验收（阻断项，P1）

| 指标 | P50 目标 | P95 目标 | 测试方法 |
|------|---------|---------|---------|
| Intent LLM 调用 | < 200ms | < 500ms | 100 次压力测试 |
| Agent 单步 | < 1.5s | < 3s | 50 次压力测试 |
| 整体端到端 | < 3s | < 8s | 端到端测试 |

- [ ] 压力测试脚本产出 latency 分布报告

### 3) 缓存验收（阻断项，P1）

- [ ] 相同 query 第二次命中缓存，Intent 延迟 < 10ms
- [ ] 缓存 TTL 到期后自动失效
- [ ] 缓存不污染不同 history 的 query（key 包含 history_hash）

### 4) 回归验收（阻断项，P1）

- [ ] P0 全部 38 个测试仍通过
- [ ] `CHATBI_USE_AGENT=false` 时 V1 行为不变

---

## 实现备忘

### 1. 测试集格式

```python
# tests/test_intent_agent_accuracy.py

TEST_CASES = [
    # Text2SQL 场景（20条）
    {"query": "昨天销售额", "expected": "text2sql_query", "category": "时间+金额", "note": "口语化"},
    {"query": "用户增长趋势", "expected": "text2sql_query", "category": "趋势", "note": "无关键词"},
    {"query": "Top10产品", "expected": "text2sql_query", "category": "排名", "note": "英文+数字"},
    {"query": "平均客单价", "expected": "text2sql_query", "category": "平均", "note": "业务术语"},
    {"query": "这个月有多少订单", "expected": "text2sql_query", "category": "数量", "note": "口语化"},
    {"query": "看看昨天的数据", "expected": "text2sql_query", "category": "模糊-数据", "note": "模糊表达"},
    {"query": "最近7天收入多少", "expected": "text2sql_query", "category": "时间范围", "note": "自然语言"},
    {"query": "哪个产品卖得最好", "expected": "text2sql_query", "category": "排名", "note": "口语化"},
    {"query": "同比去年增长了多少", "expected": "text2sql_query", "category": "对比", "note": "同比"},
    {"query": "各渠道转化率", "expected": "text2sql_query", "category": "分组", "note": "无统计词"},
    # ... 再补 10 条
    
    # RAG 场景（20条）
    {"query": "什么是RAG", "expected": "rag_search", "category": "概念", "note": "标准概念"},
    {"query": "怎么优化向量检索", "expected": "rag_search", "category": "如何", "note": "技术操作"},
    {"query": "为什么检索不准", "expected": "rag_search", "category": "为什么", "note": "原因分析"},
    {"query": "这篇文档讲了什么", "expected": "rag_search", "category": "文档", "note": "内容总结"},
    {"query": "分析一下", "expected": "rag_search", "category": "模糊-分析", "note": "极度模糊"},
    {"query": "MCP 是什么", "expected": "rag_search", "category": "概念", "note": "新术语"},
    {"query": "ReAct 和 Plan-and-Execute 区别", "expected": "rag_search", "category": "对比", "note": "技术对比"},
    {"query": "怎么部署这个项目", "expected": "rag_search", "category": "如何", "note": "操作文档"},
    {"query": "Text2SQL 的原理", "expected": "rag_search", "category": "概念", "note": "技术原理"},
    {"query": "向量数据库选型", "expected": "rag_search", "category": "如何", "note": "选型建议"},
    # ... 再补 10 条
    
    # Direct Answer 场景（10条）
    {"query": "翻译：Hello", "expected": "direct_answer", "category": "翻译", "note": "明确翻译"},
    {"query": "帮我写周报", "expected": "direct_answer", "category": "写作", "note": "内容生成"},
    {"query": "润色这段话", "expected": "direct_answer", "category": "润色", "note": "文本处理"},
    {"query": "用 Python 写快排", "expected": "direct_answer", "category": "代码", "note": "代码生成"},
    {"query": "头脑风暴：新产品idea", "expected": "direct_answer", "category": "创意", "note": "发散"},
    {"query": "总结这段话", "expected": "direct_answer", "category": "总结", "note": "文本处理"},
    {"query": "把这段英文翻译成中文", "expected": "direct_answer", "category": "翻译", "note": "语言转换"},
    {"query": "帮我写一封邮件", "expected": "direct_answer", "category": "写作", "note": "商务写作"},
    {"query": "解释一下量子计算", "expected": "direct_answer", "category": "解释", "note": "通用知识"},
    {"query": "给这段代码加注释", "expected": "direct_answer", "category": "代码", "note": "代码辅助"},
    
    # 多轮对话场景（10条）
    {"query": "它有什么缺点", "expected": "rag_search", "category": "多轮-指代", 
     "history": [{"role": "user", "content": "什么是RAG"}, {"role": "assistant", "content": "RAG是..."}],
     "note": "指代消解"},
    {"query": "那怎么优化", "expected": "rag_search", "category": "多轮-省略", 
     "history": [{"role": "user", "content": "RAG检索不准"}, {"role": "assistant", "content": "可能原因..."}],
     "note": "省略主语"},
    # ... 再补 8 条
]
```

### 2. 缓存实现

```python
# api/intent_agent.py

from functools import lru_cache
import hashlib

class IntentCache:
    """意图识别缓存：query + history_hash -> IntentDecision"""
    
    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        self._cache: dict[str, tuple[float, IntentDecision]] = {}
        self.maxsize = maxsize
        self.ttl = ttl
    
    def _key(self, query: str, history: list[dict] | None) -> str:
        history_str = json.dumps(history or [], ensure_ascii=False, sort_keys=True)
        history_hash = hashlib.md5(history_str.encode()).hexdigest()[:16]
        return f"{query}::{history_hash}"
    
    def get(self, query: str, history: list[dict] | None) -> IntentDecision | None:
        key = self._key(query, history)
        if key in self._cache:
            ts, decision = self._cache[key]
            if time.time() - ts < self.ttl:
                return decision
            del self._cache[key]
        return None
    
    def set(self, query: str, history: list[dict] | None, decision: IntentDecision) -> None:
        key = self._key(query, history)
        self._cache[key] = (time.time(), decision)
        # LRU: 超出大小时清理最旧的
        if len(self._cache) > self.maxsize:
            oldest = min(self._cache, key=lambda k: self._cache[k][0])
            del self._cache[oldest]
```

### 3. 性能测试脚本

```python
# tests/benchmark_intent_latency.py

import asyncio
import time
import statistics

async def benchmark_intent(n: int = 100):
    latencies = []
    for _ in range(n):
        start = time.perf_counter()
        await decide_intent_v2(query="昨天销售额", history=[])
        latencies.append((time.perf_counter() - start) * 1000)
    
    latencies.sort()
    p50 = latencies[n // 2]
    p95 = latencies[int(n * 0.95)]
    p99 = latencies[int(n * 0.99)]
    
    print(f"Intent Latency (n={n}):")
    print(f"  P50: {p50:.1f}ms")
    print(f"  P95: {p95:.1f}ms")
    print(f"  P99: {p99:.1f}ms")
    print(f"  Min: {min(latencies):.1f}ms")
    print(f"  Max: {max(latencies):.1f}ms")
```

---

## 交付物

1. `tests/test_intent_agent_accuracy.py` — 60 条真实 LLM 意图测试 + 准确率报告
2. `tests/benchmark_intent_latency.py` — 性能基准测试脚本 + 报告
3. `api/intent_agent.py` — 缓存实现（`_intent_cache` 落地）
4. `docs/diary/2026-04-29-p1-intent-benchmark.md` — 测试报告与优化建议

---

## 风险与应对

| 风险 | 应对 |
|------|------|
| 真实 LLM 准确率不达标 | 调优 Prompt（去关键词化强化）→ 增加 few-shot 示例 → 调整 confidence 阈值 |
| 延迟超标（P95 > 500ms）| 缓存命中优化 → 模型降级（Turbo 替代 V3）→ 异步预加载 |
| API 成本过高（60 条 × 多次调试）| 本地缓存已命中避免重复调用 → 夜间批量跑测试 |
| 缓存污染（不同 history 相同 query）| key 包含 history_hash → 定期清理 |

---

## 时间线

| 阶段 | 时间 | 产出 |
|------|------|------|
| Phase 1 | 4/30 | 缓存实现 + 10 条核心用例验证 |
| Phase 2 | 5/1-5/2 | 60 条测试集跑完 + 准确率报告 |
| Phase 3 | 5/3 | 性能基准测试 + 调优 |
| Phase 4 | 5/4 | 文档 + 归档 |
