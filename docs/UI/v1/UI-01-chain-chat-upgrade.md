# UI-01：Chat UI 升级方案（v1）— Chain 可视化 + 图表

## 目标

把现有“简单 Chat UI”升级为“可观测链式对话 UI”：

- 同一轮对话中可看到完整 chain：LLM 输出、工具调用（开始/结束）、SQL 执行结果、图表
- 支持 Debug（sql/rows/retrieved/errors/latency）折叠展示
- 兼容后续扩展：多工具、多数据源、Text2SQL、Ticket Bot 等

> v1 聚焦“时间线（Timeline）可视化”，不强制做“链路图（Graph）”。

## 信息架构（v1）

三栏布局（参考你当前 demo 截图）：

1. **左栏：对话消息流**
   - user / assistant 的自然语言消息
2. **中栏：Chain 时间线（核心）**
   - 事件按时间顺序渲染：`assistant.message`、`tool.call.start/end`、`sql.result`、`chart`、`error`
   - 每个事件支持展开查看详情（输入/输出/耗时/原始 payload）
3. **右栏：工具与推荐**
   - 工具开关（enable/disable）
   - 推荐问法（prompt suggestions）

## 技术选型建议（前端）

### UI 组件库

- 推荐：**shadcn/ui（Radix + Tailwind）**
  - 适合 Timeline / Accordion / Tabs / Table / Badge / ScrollArea / Sheet 等组合
  - 与当前 Tailwind 风格契合，样式可控

### 图表

- 推荐：**Recharts**（v1 足够）
- 复杂交互可后续切换到 ECharts

### Chain 可视化（可选增强）

- v1：Timeline（Accordion/Steps）即可
- v2：如需链路图可引入 React Flow

## 数据契约（前后端对齐重点）

### 事件模型（建议）

后端在一次对话中返回 `events[]`（或流式事件），每个事件是统一结构：

- `type`：
  - `assistant.message`
  - `tool.call.start`
  - `tool.call.end`
  - `sql.result`
  - `chart.image` / `chart.spec`
  - `error`
- `ts`: number（ms）
- `run_id`: string（一次对话唯一）
- `step_id`: string（同一次 chain 内唯一）
- `payload`: object（事件内容，按 type 决定）

### v1 最小落地（不改后端也能跑）

对于 Text2SQL v1（当前已返回 JSON）：

- `sql / columns / rows / retrieved / errors / latency_ms` 可直接映射成：
  - `assistant.message`（answer）
  - `tool.call.*`（虚拟：text2sql.generate_sql / text2sql.execute / text2sql.summarize）
  - `sql.result`（rows/columns）

对于 Ticket Bot demo（WebUI 现状）：

- 生产建议改造为 API 返回上述事件模型；本地 demo 可先“跳转”作为入口

## v1 里程碑（建议）

- M1：页面布局 + Debug 折叠区（sql/rows/retrieved/errors）
- M2：Chain Timeline（至少 3 类事件：message / tool / sql）
- M3：图表渲染（rows→chart 或直接 image）

## 验收标准（v1）

- 一次对话能看到：
  - 用户问题
  - 生成的 SQL（若有）
  - SQL 结果表（最多展示前 20 行）
  - 错误信息（若有）
  - 关键 chain 事件（开始/结束/耗时）
- 不影响现有 Chat 页面（新增独立入口/页面即可）

