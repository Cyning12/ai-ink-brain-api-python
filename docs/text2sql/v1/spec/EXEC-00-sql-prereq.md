# EXEC-00：Text2SQL v1 前置（SQL 初始化与样例语料）

## 1. 本次目标

- 将 `docs/text2sql/v1/sql/`（MySQL 导出）转换为 **Supabase/Postgres 可执行脚本**
- 提供可重复初始化方式（drop → create → insert）
- 为 Text2SQL v1 MVP 提供最小数据集（每表 ≥10 行）

## 2. 产物

- **Supabase 初始化脚本**：`docs/text2sql/v1/sql/supabase_init.sql`
  - 统一 snake_case 小写字段名（便于 Text2SQL 生成）
  - 移除 MySQL 方言（SET NAMES / FOREIGN_KEY_CHECKS / ENGINE / CHARSET / AUTO_INCREMENT 等）
  - 每表保留前 10 行样例数据

## 3. 执行方式（Supabase SQL Editor）

1) 打开 Supabase Dashboard → SQL Editor  
2) 粘贴并执行 `docs/text2sql/v1/sql/supabase_init.sql`

## 4. 表清单（v1 MVP）

- `agent_info`
- `beneficiary_info`
- `claim_info`
- `customer_info`
- `employee_info`
- `policy_info`
- `product_info`
- `crs_orders`
- `heros`

## 5. 注意事项

- 本脚本是 v1 MVP 的“可用最小集”，后续若需要完整数据量，可在保持 DDL 不变的前提下扩展 INSERT 行数。

