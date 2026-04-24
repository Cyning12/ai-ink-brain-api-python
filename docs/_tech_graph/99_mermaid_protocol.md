<!-- docs/_tech_graph/99_mermaid_protocol.md -->
# AI-Ink-Brain API — Mermaid 拓扑协议（Python/FastAPI 适配版）

> 基于通用拓扑协议 v2，绑定 Python/FastAPI 语义。
> 目标：让 LLM 用 Python 语法习惯生成 Mermaid，降低幻觉。

---

## 1. 边标记：Python 惯用语法

### 1.1 执行流

| 标记 | Python 语义 | 示例 | 何时用 |
|------|-----------|------|--------|
| `->` | 顺序执行 | `process()` → `save()` | 同步调用 |
| `~>` | `await` 异步 | `await embed_text()` | async def 调用 |
| `=>` | 赋值/映射 | `result = transform(data)` | 数据转换 |
| `?>` | `if` / `try/except` 分支 | `if not valid:` / `except:` | 条件/异常 |

### 1.2 错误处理（Python 风格）

| 标记 | Python 语义 | Mermaid 示例 |
|------|-----------|-------------|
| `[ok]` | 无异常，正常返回 | `validate() --"[ok]"--> save()` |
| `[err]` | `raise` / `except` | `parse() --"[err]"--> fallback()` |
| `[retry=N]` | `tenacity` 重试 | `call_api() --"[retry=3]"--> call_api()` |
| `[timeout]` | `asyncio.timeout` / `httpx.Timeout` | `fetch() --"[timeout]"--> cache_get()` |

### 1.3 元关系（:: 命名空间）

| 标记 | 语义 | 示例 |
|------|------|------|
| `::yields` | `yield` / `yield from` | 流式响应、生成器 |
| `::triggers` | `BackgroundTasks.add_task` | 后台任务触发 |
| `::gates` | `Depends()` 依赖注入 | FastAPI 依赖校验 |
| `::branches` | `asyncio.gather` | 并行分支 |
| `::merges` | `gather` 结果合并 | 多路归并 |
| `::signoff` | 事务提交 / `db.commit()` | 持久化确认 |
| `::archives` | 写入日志 / `logger.info` | 归档记录 |

---

## 2. 节点标记：Python/FastAPI 类型

### 2.1 形状约定

| 形状 | 含义 | Python 对应 | 示例 |
|------|------|-----------|------|
| `[[...]]` | 阶段/流程 | 路由处理阶段 | `[[Query]]` |
| `[...]` | 函数/操作 | `def` / `async def` | `[embed_text()]` |
| `[(...)]` | 数据/模型 | `class` / `TypedDict` / `Pydantic` | `[(Document)]` |
| `{...}` | 判断/路由 | `if` / `try/except` / 路径参数 | `{valid?}` |
| `>...]` | 里程碑 | 关键完成点 | `>Ingested]` |
| `((...))` | 循环/归档 | `for` / `while` / 日志归档 | `((归档))` |

### 2.2 前缀约定

| 前缀 | 含义 | 示例 |
|------|------|------|
| `def ` | 同步函数 | `[def process_text]` |
| `async ` | 异步函数 | `[async def embed]` |
| `class ` | 类/模型 | `[(class Document)]` |
| `@` | 装饰器路由 | `[@router.post]` |
| `>> ` | 外部服务 | `[>> SiliconFlow]` |
| `DB:` | 数据库操作 | `[(DB: documents)]` |

---

## 3. 锚点规则（强制）

每条硬边必须可追溯到代码位置：

| 写法 | 指向 |
|------|------|
| `// → api/rag_recall_tools.py#L45` | 具体代码行 |
| `// → api/index.py::match_documents` | 函数定义 |
| `// → supabase/sql/init_vector.sql#L12` | SQL 迁移 |
| `// → docs/_tech_graph/10_flow_rag.md` | 关联文档 |

---

## 4. 分层规则：何时展开/折叠

| 条件 | 操作 |
|------|------|
| 子图节点 ≤ 7 | 直接展开 |
| 子图节点 > 7 | 折叠为 `[[Phase]]`，链接独立 `.mmd` 文件 |
| 跨模块调用 | 用 `::triggers` 或虚线边，不展开内部 |

---

## 5. 用法速查

```
Query 阶段（软为主）:
    用户输入 --"理解"--> 拆解需求 --"歧义"--> {明确?}

Work 阶段（硬为主）:
    [async def embed] ~> [(DB: documents)]
    [def search] ?> {results?} --"[ok]"--> [async def rerank]
                              --"[err]"--> [def fallback]

Summarize 阶段（软硬混）:
    [def draft] --"聚合"--> [def polish] --"::archives"--> ((日志))
```

---

## 6. 文件命名

| 类型 | 命名 | 示例 |
|------|------|------|
| 流程图 | `{NN}_flow_{name}.mmd` | `10_flow_rag.mmd` |
| 架构图 | `{NN}_arch_{name}.mmd` | `20_arch_ingest.mmd` |
| 状态图 | `{NN}_state_{name}.mmd` | `30_state_chat.mmd` |

---

## 7. 验证清单

生成图后检查：

- [ ] 所有 `[[Phase]]` 有锚点注释
- [ ] Work 阶段无裸边（必须有 `->` `~>` `?>` `[ok]` `[err]`）
- [ ] 异步函数标记 `async ` 前缀，边用 `~>`
- [ ] 异常分支外挂，HappyPath 走主干
- [ ] 子图 >7 节点已折叠并链接独立文件
