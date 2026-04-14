## Task 04：引用溯源显示与 UI 透明化（可验收任务）

### 任务目标
- 将后端检索到的 **Top-k 来源（sources）** 以标准化结构传递给前端。
- 前端在 AI 回答下方以“水墨风”来源卡片展示，确保“每一句回答有据可查”。
- 在不破坏现有 **流式输出（StreamingResponse）** 的前提下完成（前端仍按文本流渲染）。

### 范围与约束
- 后端来源数据来自 Supabase `public.documents` 的 `metadata + content`（融合排序后的 Top-k）。
- 需要遵循项目约定：**Metadata Persistence**，尤其是 `relativePath` 必须可被前端解析到文章页面或预览内容。
- 不改变 `/api/py/chat` 的鉴权方式与基本入参；允许在“流的末尾”追加机器可解析的 sources。

---

## 1) 后端输出标准化（`api/index.py`）

### 1.1 元数据清洗（必须）
在 RRF 融合与（可选）日期锚点注入完成后，取 Top-k（建议 8~12）生成 `sources[]`：
- `id`：documents.id
- `relativePath`：`metadata.relativePath`（优先）
- `filename`：`metadata.filename`
- `slug`：`metadata.slug`
- `original_link`：`metadata.original_link`（若存在）
- `category`：`metadata.category`
- `chunk_index`：`metadata.chunk_index`
- `snippet`：从 `content` 截取 200~400 字符的摘要（去掉前缀元信息行，如 `[Document Context]`、`Title:` 等）
- `score`：`fused_score`（或向量 similarity / keyword score 的组合信息，至少保留 fused_score）

> 注意：sources 中不要塞完整 content，避免 payload 过大；保留 snippet 够 UI 预览即可。

### 1.2 响应结构（流式兼容）
采用 **“流末尾分隔符 + JSON”** 的方式（推荐），避免依赖自定义 header（header 不适合承载大 JSON）：
- 文本流正常输出 assistant 内容
- 在流结束前追加一个分隔符行与 JSON：
  - 分隔符：`\n\n---RAG_SOURCES_JSON---\n`
  - JSON：`{"sources":[...], "retrieval":{...}}`

前端解析策略：
- 若响应中存在分隔符，则将其后的 JSON 解析为 sources；分隔符之前仍视为正常回答文本。
- 若不存在分隔符（兼容旧版本），UI 不展示 sources 卡片。

### 1.3 验收（后端）
- 调用 `POST /api/py/chat`：
  - 流式文本正常返回（前端不报错）
  - 末尾能解析到 `sources[]`（长度 >0 时展示）
- `sources[]` 中至少包含 `relativePath` 或 `original_link`，并且 `snippet` 非空。

### 1.4 回滚
- 只需移除“分隔符 + JSON”附加逻辑即可恢复旧行为（不影响检索与日志）。

---

## 2) 前端 UI 实装（`ai-ink-brain`）

### 2.1 新增组件：`<SourceCitation />`
展示位置：AI 单轮回答下方。

### 2.2 视觉规范（水墨风）
- 背景：`#F9F9F7`（纸张质感）
- 边框：极细灰线（1px，低对比）
- 字体：Serif（衬线体）
- 布局：极简 + 大量留白

### 2.3 交互
- 点击来源卡片：
  - 若有 `original_link`：新开或弹层预览（由前端决定）
  - 否则用 `relativePath` 定位到站内文章（或弹层预览 snippet）

### 2.4 验收（前端）
- 聊天仍可流式显示
- 若 sources 存在：回答下方出现来源卡片
- 点击卡片可打开/预览对应内容（至少能展示 snippet）

---

## 3) 端到端验收用例（E2E）
1) 提问命中文档的关键词问题 → sources 至少 3 条，且能点开预览。
2) 提问语义问题 → sources 仍有命中，卡片展示正常。
3) 无命中问题 → 不展示 sources 卡片（或展示“无引用”状态，不影响回答）。
