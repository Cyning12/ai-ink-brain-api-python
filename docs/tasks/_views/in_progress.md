# Tasks 状态视图：进行中（in_progress）

> 说明：本视图只做聚合索引，不改变原任务文件。

## 进行中（`in_progress` 状态）

- `../active/task_docs_tasks_reorg_move_v1.md`（`in_progress`：tasks 目录规整迁移）

> **说明**：`active/` 内另有 `pending` / `planning` / `todo` / `backlog` 等任务（如 ChatBI V3），**不**计入本视图；仅以头部 **`in_progress`** 为准，避免与「目录非空」混淆。

## 已迁出本视图

- 原 **Text2SQL 多轮 grounding** → `../done/task_chatbi_v2_text2sql_multiturn_grounding_v1.md`；**V2 未交付项** → `../active/task_chatbi_v3_debt_from_v2_multiturn_v1.md`（`backlog`）

## 缺少状态字段（请补齐后再归类）

> 见 `design.md` 的“缺少状态字段”清单（统一维护，避免重复）。

