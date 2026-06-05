# SPEC: ChatBI V2 —— Tool 设计与封装

> **状态**：draft  
> **版本**：v1  
> **日期**：2026-04-27  
> **父文档**：`SPEC-ChatBI-V2-Agent-Overview.md`

---

## 1. 设计目标

将 V1 的 RAG、Text2SQL、Direct Answer 能力封装为统一 Tool 接口，供 Agent 调用。

**原则**：
- 复用 V1 代码，不重复实现
- 统一输入输出格式
- 支持同步和异步执行
- 详细的错误信息返回

---

## 2. Tool 接口定义

```python
from dataclasses import dataclass
from typing import Any, Callable, Awaitable

@dataclass
class ToolResult:
    """Tool 执行结果"""
    success: bool
    data: Any
    error: str | None = None           # 人类可读错误描述（仅用于日志/调试）
    error_code: str | None = None      # 机器可读错误码（FailureTypeHandler 唯一判定依据）
    error_stage: str | None = None     # 错误发生的阶段（如 text2sql.generate / rag.retrieve）
    latency_ms: int = 0

@dataclass  
class Tool:
    """Tool 定义"""
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema
    execute: Callable[..., Awaitable[ToolResult]]
```

---

## 3. Tool 列表

### 3.1 RAG Search Tool

```python
rag_search_tool = Tool(
    name="rag_search",
    description=(
        "从文档库中检索信息，适合以下场景：\n"
        "- 概念解释（如'什么是 RAG'）\n"
        "- 技术文档查询\n" 
        "- 非结构化数据问题\n"
        "- 需要引用文档来源的问题\n"
        "不适合：数据统计、金额计算、SQL 查询"
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "检索关键词或问题"
            }
        },
        "required": ["query"]
    },
    execute=rag_search_execute
)

async def rag_search_execute(query: str) -> ToolResult:
    """
    复用 V1 RAG 流程：
    1. query_rewrite
    2. embedding
    3. multi-channel retrieve (vector + fts + structured + keyword)
    4. RRF fusion
    5. generate answer
    """
    started_at = time.perf_counter()
    try:
        # 复用 api/rag_recall_tools.py + api/unified_chat.py 的 RAG 逻辑
        hits = await _rag_retrieve(query)
        answer = await _rag_generate(query, hits)
        
        return ToolResult(
            success=True,
            data={
                "answer": answer,
                "sources": hits[:5],
                "source_count": len(hits)
            },
            latency_ms=_elapsed_ms(started_at)
        )
    except Exception as e:
        return ToolResult(
            success=False,
            data=None,
            error=str(e),
            latency_ms=_elapsed_ms(started_at)
        )
```

### 3.2 Text2SQL Query Tool

```python
text2sql_tool = Tool(
    name="text2sql_query",
    description=(
        "查询数据库获取结构化数据，适合以下场景：\n"
        "- 数据统计（如'销售额'、'用户数'）\n"
        "- 金额、数量、平均值计算\n"
        "- 时间趋势分析\n"
        "- 排名、分组、汇总\n"
        "不适合：概念解释、文档检索"
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string", 
                "description": "自然语言查询"
            }
        },
        "required": ["query"]
    },
    execute=text2sql_execute
)

async def text2sql_execute(query: str) -> ToolResult:
    """
    复用 V1 Text2SQL 流程：
    1. retrieve DDL examples
    2. LLM generate SQL
    3. validate SQL
    4. execute SQL
    5. summarize result
    """
    started_at = time.perf_counter()
    try:
        # 复用 api/text2sql_core.py + api/text2sql_store.py
        sql = await _generate_sql(query)
        columns, rows = await _execute_sql(sql)
        summary = await _summarize(query, sql, columns, rows)
        
        return ToolResult(
            success=True,
            data={
                "sql": sql,
                "columns": columns,
                "rows": rows[:20],
                "row_count": len(rows),
                "summary": summary
            },
            latency_ms=_elapsed_ms(started_at)
        )
    except Exception as e:
        return ToolResult(
            success=False,
            data=None,
            error=str(e),
            latency_ms=_elapsed_ms(started_at)
        )
```

### 3.3 Direct Answer Tool

```python
direct_answer_tool = Tool(
    name="direct_answer",
    description=(
        "直接回答通用问题，无需检索或查库，适合以下场景：\n"
        "- 翻译\n"
        "- 润色、改写\n"
        "- 写作、生成内容\n"
        "- 头脑风暴\n"
        "- 通用知识问答（不依赖内部文档）\n"
        "不适合：需要查数据、查文档的问题"
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "用户问题"
            }
        },
        "required": ["query"]
    },
    execute=direct_answer_execute
)

async def direct_answer_execute(query: str) -> ToolResult:
    """直接调用 LLM 回答"""
    started_at = time.perf_counter()
    try:
        oai = openai_siliconflow_client()
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")
        
        res = oai.chat.completions.create(
            model=chat_model,
            messages=[
                {"role": "system", "content": "你是一个中文助手。请直接回答用户问题。"},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        answer = (res.choices[0].message.content or "").strip()
        
        return ToolResult(
            success=True,
            data={"answer": answer},
            latency_ms=_elapsed_ms(started_at)
        )
    except Exception as e:
        return ToolResult(
            success=False,
            data=None,
            error=str(e),
            latency_ms=_elapsed_ms(started_at)
        )
```

---

## 4. Tool Registry

```python
# api/tools.py

from typing import list

class ToolRegistry:
    """Tool 注册中心"""
    
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)
    
    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())
    
    def get_tool_descriptions(self) -> str:
        """生成给 LLM 的 Tool 描述文本"""
        parts = []
        for tool in self._tools.values():
            parts.append(f"### {tool.name}\n{tool.description}\n参数：{tool.parameters}")
        return "\n\n".join(parts)

# 全局注册表
_registry = ToolRegistry()
_registry.register(rag_search_tool)
_registry.register(text2sql_tool)
_registry.register(direct_answer_tool)

def get_registry() -> ToolRegistry:
    return _registry
```

---

## 5. Tool 描述优化（给 LLM 的 Prompt）

```python
def build_tools_prompt(tools: list[Tool]) -> str:
    """构建 LLM 的 Tool 选择 Prompt"""
    lines = ["# 可用工具\n"]
    for tool in tools:
        lines.append(f"## {tool.name}")
        lines.append(f"描述：{tool.description}")
        lines.append(f"参数 schema：{json.dumps(tool.parameters, ensure_ascii=False)}")
        lines.append("")
    
    lines.append("# 选择规则")
    lines.append("- 如果问题涉及数据统计、金额、数量、趋势，选择 text2sql_query")
    lines.append("- 如果问题涉及概念解释、技术文档、非结构化信息，选择 rag_search")
    lines.append("- 如果问题是翻译、润色、写作、通用问答，选择 direct_answer")
    lines.append("- 如果不确定，优先选择 rag_search")
    
    return "\n".join(lines)
```

---

## 6. 错误处理规范（结构化错误码）

> **原则**：Tool 返回的错误必须携带 `error_code` + `error_stage`，`error` 字符串仅用于日志。Agent 的 `FailureTypeHandler` 只认 `error_code`，绝不解析 `error` 字符串。

| 错误类型 | error_code | error_stage | Tool 返回示例 | Agent 处理 |
|---------|-----------|-------------|--------------|-----------|
| SQL 生成为空 | `SQL_GEN_EMPTY` | `text2sql.generate` | `success=False, error_code="SQL_GEN_EMPTY", error="..."` | 重试 1 次 → 仍失败则换 `rag_search` |
| SQL 语法错误 | `SQL_GEN_SYNTAX` | `text2sql.generate` | `success=False, error_code="SQL_GEN_SYNTAX", error="..."` | 重试 1 次 → 仍失败则换 `rag_search` |
| 表不存在 | `SQL_EXEC_TABLE_NOT_FOUND` | `text2sql.execute` | `success=False, error_code="SQL_EXEC_TABLE_NOT_FOUND", error="..."` | 换 `rag_search`（查文档看正确表名） |
| 权限错误 | `SQL_EXEC_PERMISSION_DENIED` | `text2sql.execute` | `success=False, error_code="SQL_EXEC_PERMISSION_DENIED", error="..."` | 换 `rag_search` |
| SQL 无数据 | `SQL_EXEC_NO_DATA` | `text2sql.execute` | `success=False, error_code="SQL_EXEC_NO_DATA", error="..."` | 直接回答"未查到数据" |
| RAG 检索无命中 | `RAG_RETRIEVE_EMPTY` | `rag.retrieve` | `success=False, error_code="RAG_RETRIEVE_EMPTY", error="..."` | **gated**：满足结构化聚合意图才换 `text2sql_query`，否则换 `direct_answer` |
| RAG 生成不确定 | `RAG_GENERATE_UNCERTAIN` | `rag.generate` | `success=False, error_code="RAG_GENERATE_UNCERTAIN", error="..."` | 换 `direct_answer` 或追问 |
| LLM API 超时 | `LLM_API_TIMEOUT` | `llm.call` | `success=False, error_code="LLM_API_TIMEOUT", error="..."` | 降级到 V1 规则路由 |
| LLM API 其他错误 | `LLM_API_ERROR` | `llm.call` | `success=False, error_code="LLM_API_ERROR", error="..."` | 重试 1 次 |
| 参数缺失 | `TOOL_PARAM_MISSING` | `tool.validate` | `success=False, error_code="TOOL_PARAM_MISSING", error="..."` | 重新生成参数 |
| 未知错误 | `UNKNOWN` | `unknown` | `success=False, error_code="UNKNOWN", error="..."` | 使用 intent 预设 fallback |

---

## 7. 验收标准

- [ ] 3 个 Tool 封装完成，复用 V1 代码
- [ ] Tool 执行返回统一格式
- [ ] 错误信息清晰，Agent 可据此决策
- [ ] Tool Registry 可动态注册新 Tool
- [ ] 单元测试覆盖每个 Tool
