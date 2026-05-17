# 架构对比：当前实现 vs LangGraph

> **记录日期**: 2026-04-27  
> **对比版本**: 当前代码（ai-ink-brain-api-python） vs LangGraph 1.1.6  
> **记录目的**: 跟踪架构演进，为后续引入图编排提供决策依据  
> **下次对比触发条件**: 引入 LangGraph、实现多 Agent 协作、或编排层重大调整

---

## 一、核心架构差异

### 当前架构：函数式 + 硬编码分支

```
用户请求
    ↓
handle_unified_chat()  ← 1000+ 行
    ↓
decide_intent()        ← 返回 mode
    ↓
if mode == "text2sql":    ← 硬编码分支
    # 180 行 Text2SQL 逻辑
    # 嵌套：retrieve → generate_sql → execute → summarize
    # 每个步骤：tool.call.start → 执行 → tool.call.end → error? → latency
    
elif mode == "rag":       ← 硬编码分支
    # 220 行 RAG 逻辑
    # 嵌套：rewrite → embed → retrieve → generate
    # 同样的事件模式重复 4 次
    
elif mode == "no_data":   ← 硬编码分支
    # 40 行直接回答
```

**特点**:
- 一个巨函数包含所有逻辑
- 状态散落在局部变量
- 事件构造重复 8+ 次
- Stream 和非 Stream 两个版本完全重复（~350 行 × 2）

---

### LangGraph 架构：状态机 + 图编排

```python
# 1. 定义状态
class ChatState(TypedDict):
    query: str
    mode: str
    events: list[dict]
    error: str | None
    # ...

# 2. 定义节点（纯函数）
def router_node(state: ChatState) -> ChatState:
    decision = decide_intent(query=state["query"])
    state["mode"] = decision.final_mode
    state["events"].append({"type": "router.decision", ...})
    return state

def rewrite_node(state: ChatState) -> ChatState:
    rewritten = rewrite_query(...)
    state["rewritten"] = rewritten
    state["events"].append({"type": "tool.call.end", ...})
    return state

# 3. 构建图
workflow = StateGraph(ChatState)
workflow.add_node("router", router_node)
workflow.add_node("rewrite", rewrite_node)
workflow.add_node("embed", embed_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("router")
workflow.add_conditional_edges("router", lambda s: s["mode"], {
    "rag": "rewrite",
    "text2sql": "retrieve_ddl",
    "no_data": "generate"
})

# 4. 编译执行
app = workflow.compile()
result = app.invoke({"query": "用户问题"})
```

**特点**:
- 每个节点独立、可测试
- 状态集中管理
- 图的拓扑可视化
- Stream 和非 Stream 同一套节点

---

## 二、逐项对比

### 1. 状态管理

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 状态定义 | 散落在局部变量 | 集中 `State` 对象 | LangGraph 更清晰 |
| 类型安全 | 无 | `TypedDict` / Pydantic | LangGraph 更安全 |
| 状态传递 | 函数参数 | 图自动传递 | LangGraph 更简洁 |
| 状态持久化 | 手动写数据库 | `checkpoint` 自动 | LangGraph 更方便 |
| 状态回溯 | ❌ 无 | ✅ Time Travel | LangGraph 更强 |

**当前代码问题**:
```python
# 6 个不同的 error 变量
retrieve_err: str | None = None
gen_err: str | None = None  
exec_err: str | None = None
sum_err: str | None = None
rw_err: str | None = None
emb_err: str | None = None

# 5 个不同的 latency 变量
t_retrieve_ms = ...
t_gen_ms = ...
t_exec_ms = ...
t_sum_ms = ...
t_rw_ms = ...
```

**LangGraph 方式**:
```python
# 一个状态对象
state["errors"] = {}      # 统一错误收集
state["latencies"] = {}   # 统一耗时收集
# 节点只关心自己的字段，不污染命名空间
```

**结论**: ❌ **当前状态管理混乱，LangGraph 更清晰**。

---

### 2. 代码复用

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 节点复用 | ❌ 复制粘贴 | ✅ 定义一次 | LangGraph 更优 |
| Stream/非 Stream | ❌ 两套代码 | ✅ 同一套 | LangGraph 更优 |
| 新增模式 | 改 4+ 文件 | 改 1 文件 | LangGraph 更优 |
| 测试节点 | ❌ 难独立测试 | ✅ 单独测试 | LangGraph 更优 |

**当前代码重复**:
```python
# unified_chat.py: handle_unified_chat()      ← 350 行
# unified_chat.py: handle_unified_chat_stream() ← 350 行（完全重复）
# index.py: 独立的 RAG 逻辑                    ← 200 行（不共享）
```

**事件构造重复统计**:
- `tool.call.start`: 8 处
- `tool.call.end`: 6 处
- `error`: 7 处
- `latency`: 8 处

**LangGraph 方式**:
```python
# 节点定义一次
def retrieve_node(state): ...

# 两种调用方式
app.invoke(state)        # 非流式
app.astream(state)       # 流式（同一套节点）

# 多个入口复用
rag_graph = build_rag_graph()
# /chat 用
# /api/py/chat 用  
# 新 Agent 也用
```

**结论**: ❌ **当前代码重复严重，LangGraph 更优**。

---

### 3. 扩展性

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 新增 Agent | ~200 行，改 4 文件 | ~30 行，改 1 文件 | LangGraph 更优 |
| 新增节点 | 插入 if/else | 加一条边 | LangGraph 更优 |
| 条件分支 | 嵌套 if/else | 条件边 | LangGraph 更清晰 |
| 循环 | ❌ 难实现 | ✅ 天然支持 | LangGraph 更强 |

**新增 "writing" 模式成本对比**:

当前成本:
```
1. intent_router.py     +20 行
2. unified_chat.py      +100 行（非 Stream）
3. unified_chat.py      +100 行（Stream）
4. 测试文件             +50 行
总计: ~270 行，4 个文件
```

LangGraph 成本:
```python
# 1. 定义节点（30 行）
def writing_node(state: ChatState):
    hits = retrieve_writing_docs(state["query"])
    article = llm.generate(...)
    state["answer"] = article
    return state

# 2. 加一条边（3 行）
workflow.add_node("writing", writing_node)
workflow.add_conditional_edges("router", lambda s: s["mode"], {
    "rag": "rewrite",
    "text2sql": "retrieve_ddl", 
    "writing": "writing",      # ← 新增
    "no_data": "generate"
})

总计: ~33 行，1 个文件
```

**结论**: ❌ **当前扩展成本极高，LangGraph 更优**。

---

### 4. 可视化与调试

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 流程图 | ❌ 读代码 | ✅ 自动生成 | LangGraph 更优 |
| 调用链追踪 | ✅ 自定义 events | ✅ LangSmith | 持平 |
| 节点 Replay | ❌ 无 | ✅ 任意节点重放 | LangGraph 更强 |
| Time Travel | ❌ 无 | ✅ 状态回溯 | LangGraph 更强 |
| 断点调试 | print | 可视化 | LangGraph 更优 |

**LangGraph 自动生成图**:
```
    ┌─────────┐
    │  router │────────┐
    └─────────┘        │
       │ rag            │ text2sql
       v                v
 ┌──────────┐    ┌──────────┐
 │  rewrite │    │retrieve  │
 └──────────┘    │  ddl     │
       │         └──────────┘
       v              │
 ┌──────────┐        v
 │  embed   │   ┌──────────┐
 └──────────┘   │generate  │
       │        │  sql     │
       v        └──────────┘
 ┌──────────┐        │
 │ retrieve │        v
 └──────────┘   ┌──────────┐
       │        │ execute  │
       v        └──────────┘
 ┌──────────┐        │
 │ generate │        v
 └──────────┘   ┌──────────┐
                │ summarize│
                └──────────┘
```

**当前架构可视化**:
```
读 1000 行代码，在脑中构建流程图
```

**结论**: ❌ **当前无可视化能力，LangGraph 更强**。

---

### 5. Human-in-the-loop

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 人工确认 | ❌ 不支持 | ✅ `interrupt` | LangGraph 更强 |
| 暂停/恢复 | ❌ 不支持 | ✅ `checkpoint` | LangGraph 更强 |
| 长时间任务 | ❌ 不支持 | ✅ 支持 | LangGraph 更强 |

**场景: SQL 返回 10 万行，需要用户确认**

当前实现:
```python
# ❌ 做不到
# 请求一旦开始就必须完成
# 或者自己实现复杂的状态机（成本极高）
```

LangGraph:
```python
workflow.add_node("check_rows", check_row_count)
workflow.add_node("ask_user", interrupt)  # ← 暂停，等用户输入
workflow.add_node("execute", execute_query)

workflow.add_conditional_edges("check_rows", lambda s: "ask_user" if s["row_count"] > 10000 else "execute")

# 用户通过 API 确认后
app.invoke(None, config={"checkpoint_id": "xxx"})  # ← 从断点恢复
```

**结论**: ❌ **当前无 HITL 能力，LangGraph 更强**。

---

### 6. 并行执行

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 并行召回 | ❌ 顺序执行 | ✅ `Send` / `map` | LangGraph 更优 |
| 并行工具 | ❌ 顺序执行 | ✅ 并行节点 | LangGraph 更优 |

**当前 RAG 召回**:
```python
# 顺序执行，总耗时 = 200 + 150 + 100 = 450ms
vector_hits = fetch_vector(...)      # 200ms
keyword_hits = fetch_keyword(...)    # 150ms  
structured_hits = fetch_structured(...)  # 100ms
```

LangGraph:
```python
# 并行执行，总耗时 = max(200, 150, 100) = 200ms
# 通过 fan-out / fan-in 模式
```

**结论**: ❌ **当前顺序执行慢，LangGraph 更优**。

---

### 7. 错误处理与重试

| 维度 | 当前实现 | LangGraph | 优劣 |
|------|----------|-----------|------|
| 节点重试 | 手动 try/except | 配置 `retry` | LangGraph 更优 |
| 错误恢复 | 硬编码 fallback | 条件边路由 | LangGraph 更灵活 |
| 部分失败 | ❌ 全失败 | ✅ 跳过失败节点 | LangGraph 更强 |

**当前代码**:
```python
try:
    sql_raw = llm_generate_sql(...)
    sql = validate_sql_readonly(sql_raw)
except Exception as exc:
    gen_err = str(exc)
    # 硬编码：返回错误
```

LangGraph:
```python
# 配置重试
workflow.add_node("generate_sql", generate_sql_node, retry=RetryPolicy(max_attempts=3))

# 或条件路由
workflow.add_conditional_edges("generate_sql", lambda s: "fix" if s["error"] else "execute")
```

**结论**: ❌ **当前错误处理硬编码，LangGraph 更灵活**。

---

## 三、当前优势（LangGraph 没有的）

### 1. 事件流设计

当前 `_event` 机制是非常好的设计:

```python
{"type": "tool.call.start", "ts": 123, "step_id": "t_rewrite", "payload": {...}}
{"type": "tool.call.end",   "ts": 456, "step_id": "t_rewrite", "payload": {...}}
{"type": "error",           "ts": 789, "step_id": "e_rewrite", "payload": {...}}
```

LangGraph 没有内置这么详细的**前端可消费的事件格式**，需要自行包装。

### 2. 检索层精细度

多路召回 + RRF + i18n + 日期召回，**比 LangGraph 默认 RAG 更强**。

### 3. 意图路由

`decide_intent` 有**证据校验 + fallback 保护**，设计很成熟。

### 4. 简洁性

无框架依赖，**部署更简单，理解成本更低**（对单人项目）。

---

## 四、综合评分

| 维度 | 当前实现 | LangGraph | 差距 |
|------|----------|-----------|------|
| 状态管理 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 大 |
| 代码复用 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 大 |
| 扩展性 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 大 |
| 可视化 | ⭐ | ⭐⭐⭐⭐⭐ | 极大 |
| 调试 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 大 |
| HITL | ⭐ | ⭐⭐⭐⭐⭐ | 极大 |
| 并行执行 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 大 |
| 错误恢复 | ⭐⭐ | ⭐⭐⭐⭐ | 中 |
| 事件流 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **当前更强** |
| 检索精细度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **当前更强** |
| 意图路由 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **当前更强** |
| 简洁性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **当前更强** |

---

## 五、改进建议

### 短期（保持现有架构，吸收思想）

1. **集中状态定义**: 用 `TypedDict` 替代散落变量
2. **节点装饰器**: 写装饰器自动构造 event，减少重复
3. **统一 Stream/非 Stream**: 同一套逻辑，不同调用方式
4. **并行化召回**: `asyncio.gather` 优化 RAG

### 中期（Side Project 验证）

1. 用 LangGraph 复刻简化版 ChatBI
2. 对比开发效率、可维护性、性能
3. 评估是否值得迁移

### 长期（信号触发时引入）

信号:
- 新增第 3 个 Agent
- 需要 Agent 之间协作
- 需要复杂工作流（循环、人工介入）
- 团队扩大，需要标准化

---

## 六、具体改进代码（不用 LangGraph）

```python
# 1. 集中状态定义
class ChatState(TypedDict):
    query: str
    mode: str
    events: list[dict]
    errors: dict[str, str]
    latencies: dict[str, int]

# 2. 节点装饰器（自动 event）
def node(name: str):
    def decorator(func):
        def wrapper(state: ChatState):
            started = time.perf_counter()
            state["events"].append({"type": f"{name}.start", ...})
            try:
                result = func(state)
                state["events"].append({"type": f"{name}.end", ...})
                return result
            except Exception as e:
                state["errors"][name] = str(e)
                state["events"].append({"type": "error", ...})
                raise
        return wrapper
    return decorator

# 3. 条件路由配置
ROUTES = {
    "rag": ["rewrite", "embed", "retrieve", "generate"],
    "text2sql": ["retrieve_ddl", "generate_sql", "execute", "summarize"],
    "no_data": ["generate"],
}
```

---

## 七、一句话总结

> **当前的检索和路由是优势，但编排层（状态、复用、扩展、可视化）是明显短板。**
>
> **LangGraph 不是必须的，但它的"状态机 + 图编排"思想非常值得学习。**
>
> **建议: 保持现有架构，用 LangGraph 的思想逐步改进，而不是直接换框架。**

---

## 八、参考文档

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph 概念: StateGraph](https://langchain-ai.github.io/langgraph/concepts/low_level/)
- [LangGraph 概念: Checkpoint](https://langchain-ai.github.io/langgraph/concepts/persistence/)
- [LangGraph 概念: Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
- 本仓库: `docs/_tech_graph/` 技术图谱
- 本仓库: `AGENTS.md` Agent 导航

---

*记录人: Kimi Code CLI*  
*关联文档: `2026-04-27-architecture-vs-langchain.md`*  
*下次对比计划: 引入 LangGraph 或实现多 Agent 协作时*
