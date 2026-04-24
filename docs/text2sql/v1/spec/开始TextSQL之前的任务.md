# 开始 Text2SQL 之前的任务（v1 前置清单）

> 目标：为验证 Text2SQL 的准确率与真实性，先把 `docs/text2sql/v1/sql/` 下的示例 SQL 以 **Supabase SQL Editor 可直接执行** 的形式落地为数据表与样例数据，并准备最小可用的「表结构语料 + 示例问答」。

---

## 1. 范围 / 非范围

- **范围**
  - 仅处理 `docs/text2sql/v1/sql/` 下的 SQL 文件（表结构与样例数据）。
  - 确保这些 SQL 能在 Supabase（Postgres）中一键执行成功，生成可用于 Text2SQL 的数据表。
  - 为初版 Text2SQL 准备 3–5 条「相似历史问题 + 示例 SQL」样本（可手动录入）。

- **非范围**
  - 不关注仓库其他位置的数据、其他数据库、其他迁移脚本。
  - 暂不做权限控制、敏感字段过滤、审计日志等企业增强（由后续版本任务覆盖）。

---

## 2. 现状检查（必须先完成）

### 2.1 清点 SQL 文件

目录：`docs/text2sql/v1/sql/`

需要确认：
- 一共有多少张表（每个 `.sql` 是否只对应一张表）
- 每个文件是否包含：`DROP TABLE` + `CREATE TABLE` + `INSERT INTO ... VALUES (...)`
- 是否存在重复表名、字段名冲突、或表间依赖（外键/引用）

### 2.2 识别 MySQL 方言差异（需要改为 Postgres 兼容）

当前 SQL 文件明显来自 Navicat 导出的 MySQL 脚本，常见不兼容点（需要逐项处理）：
- 反引号：MySQL 使用 `` `table` ``，Postgres 需改为 `"table"` 或直接不用引号（推荐统一为 snake_case 小写并不加引号）。
- `SET NAMES`、`SET FOREIGN_KEY_CHECKS`：Postgres/Supabase 不支持或语义不同，需移除。
- `ENGINE=InnoDB`、`CHARACTER SET`、`COLLATE`、`AUTO_INCREMENT`、`ROW_FORMAT`：Postgres 不支持，需移除或替换。
- `text CHARACTER SET ...`：Postgres 直接 `text`。
- `datetime`：Postgres 一般用 `timestamp` / `timestamptz`（建议明确是否需要时区）。
- `double`：Postgres 可用 `double precision`。
- `bigint NULL DEFAULT NULL`：Postgres 可简化为 `bigint`（默认可空）或显式 `NULL` 不必写。

---

## 3. 目标产物（必须具备）

### 3.1 一份可直接执行的 Supabase SQL 脚本集合

要求：
- 能从空库开始执行并成功创建所有表
- 样例数据能成功插入（至少每表 10 行）
- 便于后续重复初始化（建议提供“重置”脚本策略：先 drop 再 create 再 insert）

建议产物形式（二选一即可，优先 A）：
- **A. 保持每表一个文件**：将每个 `.sql` 改为 Postgres 兼容版本（同目录覆盖或新建 `sql_pg/` 目录）
- **B. 汇总一个总脚本**：例如 `sql/supabase_init.sql`，按顺序包含建表与插数（更方便 SQL Editor 一次性运行）

### 3.2 一份最小可用的 Text2SQL 示例样本（3–5 条）

每条至少包含：
- 用户问题（自然语言）
- 目标 SQL（只允许 SELECT）
- 涉及的表与字段（用于提示 LLM “只能用这些字段”）

---

## 4. 验收标准（可勾选）

- [ ] `docs/text2sql/v1/sql/` 的示例 SQL 已具备 Supabase/Postgres 兼容版本，且在 Supabase SQL Editor 可直接执行成功
- [ ] 所有表均创建成功，且样例数据插入成功（每表至少 10 行）
- [ ] 已产出 3–5 条“历史问题 + 示例 SQL”样本（只允许 SELECT）
- [ ] 明确记录：表清单、字段清单、以及执行顺序（避免后续导入不稳定）
