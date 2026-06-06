> **ARCHIVED** — 本交付包已被 `docs/spec/` + `docs/harness/` supersede。
> 当前 SDD 真值见 [`docs/spec/`](../../spec/) · Harness 过程库见 [`docs/harness/README`](../../harness/README.md)。

---

# v0.2.0-code-rag 交付清单

> 为 ai-ink-brain-api-python 增加代码语义检索能力。
> 支持自然语言查询项目 Python 代码，返回精确到函数/类级别的代码片段。

---

## 背景与目标

### 背景
当前系统仅支持 Markdown 文档的 RAG 检索。作为开发者，经常需要快速定位代码实现（如"chat 函数怎么实现流式的"），现有系统无法回答。

### 目标
- 将项目自身的 Python 代码向量化存入数据库
- 提供自然语言查询接口，返回相关代码片段
- 支持 Cursor/Kimi 等工具通过 HTTP API 调用

### 非目标（P1 不做）
- 多语言支持（P1 仅 Python）
- MCP 协议集成（P2）
- 实时增量索引（P2，P1 全量重删再插）
- 跨项目索引（P2，P1 仅当前项目）

---

## 交付物清单

### SDD（设计规格）

| 文档 | 状态 | 说明 |
|-----|------|------|
| [SPEC-01-architecture.md](sdd/SPEC-01-architecture.md) | ✅ 已完成 | 整体架构、数据流、数据库设计 |
| [SPEC-02-ingest-pipeline.md](sdd/SPEC-02-ingest-pipeline.md) | ✅ 已完成 | AST 解析、Chunk 生成规则 |
| [SPEC-03-query-api.md](sdd/SPEC-03-query-api.md) | ✅ 已完成 | 接口详细契约、错误码 |

### TDD（测试驱动）

| 文档 | 状态 | 说明 |
|-----|------|------|
| [TEST-01-ingest-unit.md](sdd/TEST-01-ingest-unit.md) | ✅ 已完成 | AST 解析单元测试 |
| [TEST-02-query-contract.md](sdd/TEST-02-query-contract.md) | ✅ 已完成 | API 契约测试 |
| [TEST-03-integration.md](sdd/TEST-03-integration.md) | ✅ 已完成 | 端到端集成测试 |

### Harness（验收脚手架）

| 脚本 | 状态 | 说明 |
|-----|------|------|
| [INFORM.md](harness/INFORM.md) | ✅ 已完成 | 输入数据、环境配置、前置条件 |
| [CONSTRAIN.md](harness/CONSTRAIN.md) | ✅ 已完成 | 约束条件、边界、限制 |
| [VERIFY.md](harness/VERIFY.md) | ✅ 已完成 | 验证方法、断言标准、通过准则 |
| [CHECKLIST.md](harness/CHECKLIST.md) | ✅ 已完成 | 人工验收清单 |
| [verify-ingest.http](harness/verify-ingest.http) | ✅ 已完成 | 入库接口验收 |
| [verify-query.http](harness/verify-query.http) | ✅ 已完成 | 查询接口验收 |
| [test_code_rag.py](harness/test_code_rag.py) | ✅ 已完成 | Python 自动化测试 |
| [run-all.sh](harness/run-all.sh) | ✅ 已完成 | 一键执行所有验收 |

---

## 技术决策记录

| 决策 | 选择 | 理由 |
|-----|------|------|
| 接入方式 | 方案 B：HTTP API | 简单直接，MCP（方案 A）放 P2 |
| 支持语言 | Python | 先跑通，再扩展 |
| 数据表 | 新建 `code_chunks` | 不混用 `documents`，字段语义不同 |
| 索引范围 | 当前项目 | 先固定，再参数化支持 `repo_path` |
| 数据库 | Supabase 免费版（复用） | 个人项目够用，企业场景再考虑本地 |

---

## 部署记录

| 日期 | 版本 | 操作 | 状态 |
|-----|------|------|------|
| - | - | 尚未部署 | 🚧 |

---

## 验收标准

- [ ] `POST /admin/ingest?type=code` 成功索引当前项目所有 .py 文件
- [ ] `POST /code/query` 对"chat 函数"类问题返回正确片段
- [ ] 返回结果包含 file_path、start_line、signature
- [ ] Hybrid Search 生效：vector + keyword 都有召回
- [ ] Cursor 侧脚本可成功调用并展示结果
- [ ] 不破坏现有 documents/Markdown 链路

---

## 开工前置条件（必须）

开始研发前请先完成：

- [ ] 阅读并执行 `docs/EXEC-00-prerequisites.md`
- [ ] 补齐数据库脚本（`code_chunks` 表 + FTS + RPC），并在 Supabase 执行
- [ ] 补齐测试依赖（pytest/requests）到 `requirements.txt`

---

## 后续演进

| 阶段 | 内容 |
|-----|------|
| P2 | MCP 协议支持、多项目 repo_path、增量索引 |
| P3 | 多语言（JS/TS/Go）、代码图谱（调用关系）、IDE 插件 |
