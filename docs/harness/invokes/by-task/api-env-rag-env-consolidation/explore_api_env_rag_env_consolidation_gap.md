# Explore · W1 · api-env-rag-env-consolidation

> **hat**: explore · **date**: 2026-06-09 · **branch**: `task/api-env-rag-env-w1`

## 影响面

| 文件 | 行数 | env 散落 |
|------|------|----------|
| `api/rag_env.py` | 235 | 已有 Supabase/SiliconFlow/admin 真值 |
| `api/index.py` | 1205 | 6 模块级 + 5 函数内 `os.getenv` |

## index.py 待迁 helper

| env 变量 | 现状 | 建议 helper |
|----------|------|-------------|
| `CONTENT_DEFAULT_YEAR` | L86 模块常量 | `content_default_year()` |
| `SILICONFLOW_BASE_URL` | L87 重复 rag_env | `siliconflow_base()` |
| `SILICONFLOW_EMBEDDING_*` | L88-91 重复 | `siliconflow_embedding_model()` / `dimensions()` |
| `SILICONFLOW_CHAT_MODEL` | L92 | `siliconflow_chat_model()` |
| `MAX_X_SOURCES_HEADER_CHARS` | L101 | `max_x_sources_header_chars()` |
| `DEBUG_RAG`/`RAG_DEBUG`/`NODE_ENV` | L134-138 | `rag_debug_enabled()` |
| `API_KEY` | L203 | `api_key_optional()` |
| `SILICONFLOW_API_KEY` | L485,735 | `siliconflow_api_key_optional()` |

## 绑定点

- `code_retrieval.bind_index_symbols`（L264-271）须在 import 时用 helper 返回值传参
- `_collect_date_hints` 用 `content_default_year()` 替代 `DEFAULT_YEAR`

## 测试缺口

- 无 `test_rag_env*`；须新建 W1 单测覆盖默认/override/bool 解析

## Judgment

**可开工** · Low 风险 · 2 个 `api/*.py` · 无契约变更
