# SAMPLES-01：Text2SQL v1 最小样本（3–5 条）

> 约束：仅允许 `SELECT`；不得生成 `INSERT/UPDATE/DELETE/DDL`。

## 1) 查询某个城市的订单总收入

- **问题**：北京市的订单总收入是多少？
- **涉及表/字段**：
  - `crs_orders.total_revenue`
  - `crs_orders.city`
- **SQL**：

```sql
select sum(total_revenue) as total_revenue_sum
from crs_orders
where city = '北京市';
```

## 2) 查询某个代理人的佣金结构

- **问题**：姓名为“张勇”的代理人佣金结构是什么？
- **涉及表/字段**：
  - `agent_info.name`
  - `agent_info.commission_structure`
- **SQL**：

```sql
select commission_structure
from agent_info
where name = '张勇'
limit 1;
```

## 3) 按产品状态统计产品数量

- **问题**：不同产品状态分别有多少个产品？
- **涉及表/字段**：
  - `product_info.product_status`
- **SQL**：

```sql
select product_status, count(*) as product_count
from product_info
group by product_status
order by product_count desc;
```

## 4) 查询某个客户状态的客户数量

- **问题**：当前“活跃客户”有多少人？
- **涉及表/字段**：
  - `customer_info.customer_status`
- **SQL**：

```sql
select count(*) as customer_count
from customer_info
where customer_status = '活跃客户';
```

## 5) 查询某个保单号的理赔记录

- **问题**：保单号为 “POL29795” 的理赔记录有哪些？
- **涉及表/字段**：
  - `claim_info.policy_number`
  - `claim_info.claim_number`
  - `claim_info.claim_status`
  - `claim_info.claim_amount`
- **SQL**：

```sql
select claim_number, claim_status, claim_amount, claim_date
from claim_info
where policy_number = 'POL29795'
order by claim_date desc;
```

