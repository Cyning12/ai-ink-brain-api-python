# 架构对比：当前实现 vs LangChain 生态

> **记录日期**: 2026-04-27  
> **对比版本**: 当前代码（ai-ink-brain-api-python） vs LangChain 1.2.15 + LangGraph 1.1.6  
> **记录目的**: 跟踪架构演进，为后续重构/引入框架提供决策依据  
> **下次对比触发条件**: 新增 Agent、引入 LangGraph、或架构重大调整

---

## 一、代码规模与工程指标

| 指标 | 数值 |
|------|------|
| API 文件数 | 18 个 |
| 总代码行 | 5,864 行 |
| 平均每文件 | 325 行 |
| 环境变量 | 39 个，散落在 74 个位置 |
| `os.getenv` 调用 | 77 处 |
| `try/except` 块 | 大量（unified_chat 23 个） |
| `noqa: BLE001` 标记 | 50+ 处（裸 except） |
| `print` 调试 | 22 处 |
| 日志系统 | ❌ 无 |
| 测试文件/API 文件 | 9/18 = 50% |

---

## 二、逐项对比

### 1. 模型接口

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| 调用方式 | 直接 `OpenAI SDK` | `ChatOpenAI` / `ChatModel` 统一接口 | 当前更简单直接 |
| 多模型切换 | 硬编码 `deepseek-ai/DeepSeek-V3` | 一行配置切换 | ❌ 当前需改代码 |
| Fallback | ❌ 无 | 自动切换备用模型 | ❌ 当前无此能力 |
| Rate Limit | ❌ 无 | 内置退避重试 | ❌ 当前无此能力 |
| Streaming | ✅ SSE 自定义实现 | 标准化流式接口 | 当前更灵活 |
| Batch | ❌ 无 | 批量请求优化 | ❌ 当前无此能力 |
| Async | ⚠️ `asyncio.to_thread` 包装 | 原生 async | ⚠️ 当前有性能损耗 |

**结论**: 当前模型调用够用但简陋，LangChain 更健壮。

---

### 2. 检索召回

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| 向量检索 | Supabase `match_documents` | `PGVector` / `FAISS` 统一接口 | 当前更精细（自定义 RPC） |
| 关键词检索 | `keyword_documents` (FTS) | 部分支持 | ✅ 当前 FTS 策略更成熟 |
| 多路召回 | Vector + FTS + Structured + Keyword | 通常只支持 Vector | ✅ **当前更强** |
| RRF 融合 | 自定义 `fuse_hits_rrf` | 无内置 RRF | ✅ **当前更强** |
| i18n 扩展 | `keyword_query_text_with_i18n_meta` | 无 | ✅ **当前独创** |
| 日期召回 | `structured_recall_by_date` | 无 | ✅ **当前独创** |
| Embedding 缓存 | ❌ 无 | 有 | ❌ 当前无此能力 |

**结论**: ✅ **当前检索层比 LangChain 默认实现更强**，这是核心优势。

---

### 3. Prompt 管理

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| 模板化 | ❌ 字符串拼接，散落 10+ 文件 | `PromptTemplate` / `ChatPromptTemplate` | ❌ 当前短板 |
| 参数化 | ❌ 无 | 支持变量注入 | ❌ 当前短板 |
| 版本管理 | ❌ 无 | 可追踪迭代 | ❌ 当前短板 |
| Few-shot | ❌ 无 | 示例注入机制 | ❌ 当前短板 |

**当前代码示例**:
```python
system = (
    "你是一个检索增强问答助手。请仅基于提供的上下文回答；"
    "若上下文不足以回答，请明确说明不确定。\n"
    "回答要求：中文、简洁、给出关键结论；必要时引用上下文要点。"
)
user = f"【上下文】\n{context}\n\n【问题】\n{query}\n"
```

**LangChain 方式**:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}。请基于上下文回答：{requirements}"),
    ("human", "【上下文】\n{context}\n\n【问题】\n{query}"),
])
```

**结论**: ❌ **当前 Prompt 管理是明显短板**。

---

### 4. 输出解析 / 结构化输出

| 维度 | 当前实现 | LangChain / OpenAI SDK | 对比结论 |
|------|----------|------------------------|----------|
| 解析方式 | 字符串解析，正则提取 | `PydanticOutputParser` / `response_format` | ❌ 当前脆弱 |
| 类型安全 | ❌ 无 | Pydantic 校验 | ❌ 当前短板 |
| 自动修复 | ❌ 无 | Output Fixing | ❌ 当前短板 |
| JSON Mode | ❌ 未使用 | `response_format={"type": "json_object"}` | ❌ 当前短板 |

**结论**: ❌ **当前全靠字符串解析，维护成本高**。

---

### 5. 文档处理

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| Document Loader | ❌ 只支持 Markdown | 多格式（PDF/Word/HTML等） | ❌ 当前短板 |
| Text Splitter | ⚠️ 简单字符分块 | `RecursiveCharacterTextSplitter` | ⚠️ 当前简单 |
| Chunk 策略 | ⚠️ 固定大小 512/50 | 语义分块、层次化索引 | ⚠️ 当前无优化 |
| 增强文本 | ✅ `build_enhanced_chunk_text` | 无内置 | ✅ 当前有元数据注入 |

**结论**: ⚠️ **当前分块策略简单，但元数据注入设计好**。

---

### 6. 记忆 / 对话历史

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| 持久化 | ✅ Supabase `rag_conversation_logs` | 可选内存/Redis/数据库 | ✅ 当前更持久 |
| 历史注入 | ✅ `rewrite_query_with_history` | `ConversationBufferMemory` | 持平 |
| 查询改写 | ✅ 有 | `CondenseQuestionChain` | 持平 |
| 摘要压缩 | ❌ 无 | `ConversationSummaryMemory` | ❌ 当前短板 |
| 向量记忆 | ❌ 无 | `VectorStoreMemory` | ❌ 当前短板 |

**结论**: 当前记忆够用但简单，长对话会失控。

---

### 7. Agent 能力

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| Tool 定义 | ❌ 无 | `@tool` 装饰器 | ❌ 当前无工具抽象 |
| ReAct | ❌ 无 | 推理+行动循环 | ❌ 当前无此能力 |
| Plan-and-Execute | ❌ 无 | 规划+执行 | ❌ 当前无此能力 |
| Tool Calling | ❌ 无 | 原生工具调用 | ❌ 当前无此能力 |
| Agent 追踪 | ✅ 自定义事件流 | `LangSmith` | ✅ 当前轻量且直接 |

**当前架构**:
```
用户提问 → Intent Router → RAG / Text2SQL / 直接回答
```
这是**路由**，不是 **Agent**。

**真正的 Agent**:
```
用户提问 → Agent 思考 → 选择工具 → 执行 → 观察 → 循环 → 生成答案
```

**结论**: ❌ **当前无 Agent 能力，只有硬编码路由**。

---

### 8. 工作流编排

| 维度 | 当前实现 | LangGraph | 对比结论 |
|------|----------|-----------|----------|
| 编排方式 | 硬编码 if/else | `StateGraph` 状态机 | ❌ 当前耦合严重 |
| 可视化 | ❌ 读代码 | 自动生成 Mermaid 图 | ❌ 当前差 |
| 节点复用 | ❌ 复制粘贴 | 定义一次，多处使用 | ❌ 当前差 |
| Stream/非 Stream | ❌ 两套代码 | 同一套节点 | ❌ 当前重复 |
| 条件分支 | 嵌套 if/else | 条件边 | ❌ 当前不清晰 |
| 循环 | ❌ 难实现 | 天然支持 | ❌ 当前无 |
| 并行 | ❌ 顺序执行 | `Send` / `map` | ❌ 当前慢 |

**当前代码**: `unified_chat.py` 1000+ 行，3 个 mode 分支，事件构造重复 8+ 次。

**结论**: ❌ **当前编排层是最大短板**。

---

### 9. 配置管理

| 维度 | 当前实现 | LangChain / Pydantic | 对比结论 |
|------|----------|----------------------|----------|
| 管理方式 | `os.getenv` 散落 77 处 | `BaseSettings` 集中定义 | ❌ 当前混乱 |
| 类型校验 | ❌ 无 | Pydantic 自动校验 | ❌ 当前运行时才发现 |
| 默认值 | 散落在各处 | 一处定义 | ❌ 当前不一致风险 |
| 文档化 | ❌ 无 | 自动生成 | ❌ 当前差 |

**结论**: ❌ **当前配置管理混乱**。

---

### 10. 错误处理

| 维度 | 当前实现 | LangChain | 对比结论 |
|------|----------|-----------|----------|
| 异常捕获 | `except Exception` (noqa: BLE001) | 分类异常 | ❌ 当前粗糙 |
| 错误分类 | ❌ 无 | `OutputParserException` 等 | ❌ 当前无 |
| 自动重试 | ❌ 无 | 内置退避 | ❌ 当前无 |
| 错误追踪 | ⚠️ 事件流记录 | 结构化追踪 | ⚠️ 当前可读性差 |

**统计**: 50+ 处 `noqa: BLE001`（裸 except 标记）。

**结论**: ❌ **当前错误处理粗糙**。

---

### 11. 日志系统

| 维度 | 当前实现 | Python 标准 / LangChain | 对比结论 |
|------|----------|-------------------------|----------|
| 日志框架 | ❌ 无 | `logging` | ❌ 当前用 print |
| 分级控制 | ❌ 无 | DEBUG/INFO/WARNING/ERROR | ❌ 当前无 |
| 生产可用 | ❌ 否 | 可配置输出到文件/ES | ❌ 当前差 |

**统计**: 22 处 `print()` 调试。

**结论**: ❌ **当前无日志系统**。

---

### 12. 缓存

| 维度 | 当前实现 | Python / LangChain | 对比结论 |
|------|----------|--------------------|----------|
| 缓存方式 | 3 个全局 `_CACHE` 变量 | `lru_cache` / Redis | ⚠️ 当前手动管理 |
| 失效策略 | 手动检查 mtime | 自动 LRU / TTL | ⚠️ 当前繁琐 |
| Embedding 缓存 | ❌ 无 | 有 | ❌ 当前无 |

**结论**: ⚠️ **当前缓存手动管理，易出错**。

---

### 13. 测试覆盖

| 维度 | 当前实现 | LangChain 生态 | 对比结论 |
|------|----------|----------------|----------|
| 测试文件/API 文件 | 9/18 = 50% | 接近 100% | ❌ 当前不足 |
| 基础设施测试 | ❌ 几乎无 | 完整 | ❌ 当前差 |
| Mock/Fixture | 少量 | 丰富 | ❌ 当前难独立测试 |
| 集成测试 | 有 | 有 | 持平 |

**结论**: ❌ **当前测试覆盖不足**。

---

### 14. 可观测性 / 监控

| 维度 | 当前实现 | LangChain / LangSmith | 对比结论 |
|------|----------|----------------------|----------|
| 调用链追踪 | ✅ 自定义 event 流 | `LangSmith` 自动 | ✅ 当前轻量 |
| Token 统计 | ❌ 无 | 自动统计 | ❌ 当前无 |
| Latency | ✅ `perf_counter` 手动 | 自动记录 | ⚠️ 当前灵活但繁琐 |
| 前端展示 | ✅ SSE 实时事件流 | 需额外配置 | ✅ 当前更直接 |

**结论**: ✅ **当前事件流设计好，但缺乏自动化统计**。

---

## 三、当前优势（LangChain 没有的）

1. **多路混合召回**: Vector + FTS + Structured + Keyword + RRF
2. **i18n 跨语言检索**: 中英文术语自动扩展
3. **日期结构化召回**: 支持中文日期解析（"二零二六年四月十四号"）
4. **意图路由 + 证据校验**: 规则候选 + DDL/FTS 证据 + fallback 保护
5. **事件流设计**: 前端可实时消费的详细事件格式
6. **简洁性**: 无框架依赖，部署简单

---

## 四、当前短板（LangChain 有的）

1. **Prompt 管理**: 散落字符串，无模板化
2. **结构化输出**: 全靠字符串解析
3. **配置管理**: 39 个环境变量散落 74 处
4. **错误处理**: 50+ 裸 except
5. **日志系统**: print 调试
6. **Agent 能力**: 无工具抽象，无推理循环
7. **工作流编排**: 1000+ 行 if/else
8. **并行执行**: 顺序执行
9. **缓存**: 手动全局变量
10. **测试覆盖**: 50% 文件无测试

---

## 五、改进建议

### 短期（保持现状，局部优化）

1. 抽象 LLM 客户端（`llm_client.py`）减少重复
2. 引入 Pydantic 做配置管理和结构化输出
3. 加 `logging` 替换 `print`
4. 用 `lru_cache` 替换手动 `_CACHE`
5. 并行化 RAG 召回（`asyncio.gather`）

### 中期（学习 LangChain 思想，不一定用框架）

1. 学习 `PromptTemplate` 模式，集中管理 Prompt
2. 学习 `OutputParser` 模式，用 Pydantic 做输出校验
3. 学习 Agent 设计（ReAct、Tool Use）
4. Side Project 试 LangGraph

### 长期（需要时引入框架）

信号：
- 新增第 3 个 Agent
- 需要 Agent 之间协作
- 需要复杂工作流（循环、人工介入）
- 团队扩大，需要标准化

---

## 六、一句话总结

> **当前检索层和意图路由是优势，但工程化（配置、错误处理、日志、测试）和 Agent 能力是明显短板。**
>
> **LangChain 不是银弹，但它的工程化实践值得学习。目标是"吸收思想，不一定用框架"。**

---

## 七、参考文档

- [LangChain 1.x 官方文档](https://python.langchain.com/)
- [LangGraph 教程](https://langchain-ai.github.io/langgraph/)
- 本仓库: `docs/_tech_graph/` 技术图谱
- 本仓库: `AGENTS.md` Agent 导航

---

*记录人: Kimi Code CLI*  
*下次对比计划: 新增 Agent 或引入 LangGraph 时*
