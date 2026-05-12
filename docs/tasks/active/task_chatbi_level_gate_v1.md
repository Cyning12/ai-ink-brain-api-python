# Task：ChatBI V3 — 分级权限闸门（Bearer + 表策略 + Text2SQL）

> **状态**：`pending`（待执行 Agent 编码）  
> **关联 SPEC**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access.md`、`docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md`（**§一、§五**）  
> **关联安全子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md`（AST / 表白名单）  
> **关联真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`  
> **前端依赖**：无（首期仅后端 Bearer；Ink 仅透传 Header 即可）

> 落盘规则：验收通过后状态改为 `done` 并 `git mv` 至 `docs/tasks/done/`（与仓库既有任务规范一致）。

---

## 背景与目标

用户在 **Unified Chat / Text2SQL** 链路上，仅能在 **`access_level`（0=Super / 1=Admin / 2=终端用户）** 与 **`chatbi_sql_table_policy`** 及 **OpenItems §1.5 双闸** 允许范围内执行 SQL；越权返回结构化错误与「您无此权限」等话术。同一主体抽象 **`principal_kind` + `access_level` + `subject_user_id`** 预留 **RAG**（**P4** 仅占位）。**L2** 写路径以 **`chatbi_user_portrait`** 为准（见 OpenItems **§1.3.1**）。

首期登录 **不强制** 管道 A（`login_exchange`）：**`Authorization: Bearer` + DB `key_hash` 比对** 即可（见 OpenItems **§五**）。

---

## 范围

- [ ] **P0**：将 OpenItems **§1.4 已拍板**（软删、L2 禁 JOIN/INSERT、肖像表、Super 非 env 长期真值、双闸、日志）写入代码 / YAML 注释  
- [ ] **P1**：在 Supabase 按序执行 **§Supabase SQL 执行顺序**（含 **`chatbi_04_user_portrait`**）；`PROJECT_CONFIG` 补充表名与可选 `CHATBI_ACCESS_TOKEN_PEPPER`  
- [ ] **P2**：FastAPI `Depends`：Bearer → `chatbi_access_tokens` → **`ChatBiPrincipal`**（`principal_kind`：`super`/`admin`/`end_user`，`access_level`，`subject_user_id`，`token_id`）；**L2 行须含 `subject_user_id`**  
- [ ] **P3**：**前闸**（schema/表字典裁剪）+ **后闸**（AST + 表白名单 + 等级）：Admin **禁物理 `DELETE`/`TRUNCATE`**、**允许软删 `UPDATE`**；L2 **禁 JOIN**、**禁 INSERT**、**仅 `chatbi_user_portrait` 且列白名单 `UPDATE`**（**不可改 `user_id`**）；拒绝 **4xx + 结构化 body**  
- [ ] **P3b**（可与 P3 同 PR）：`CHATBI_JSON_LOG` 按 OpenItems **§1.6** 写 `auth_ok` / `auth_fail` / `sql_gate_deny`（等）字段  
- [ ] **P4**：RAG 检索入口增加只读 `principal_kind` / `access_level` / `subject_user_id`，默认 no-op  

## 非范围

- 管道 A（`login_exchange`）、httpOnly cookie 优先策略、吊销 UI（归入 **P5 / 另任务**）  
- `auth.users` 自助注册、RLS 全表策略（可另任务；本任务以 **应用层闸门** 为主）  
- 多租户 `tenant_id`（V4）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 姊妹规（等级语义 + P0–P5） | `docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` |
| SQL 脚本（Supabase 可复制） | `docs/text2sql/v1/sql/chatbi_01_access_tokens.sql` |
| | `docs/text2sql/v1/sql/chatbi_02_sql_table_policy.sql` |
| | `docs/text2sql/v1/sql/chatbi_03_seed_table_policy_demo.sql`（**可选**，演示种子） |
| | `docs/text2sql/v1/sql/chatbi_04_user_portrait.sql`（**T3** L2 肖像表） |
| 样例业务数据（若需） | `docs/text2sql/v1/sql/supabase_init.sql` |
| 图谱（建议更新） | `docs/_tech_graph/` 增量：鉴权 → Text2SQL 闸门子流程 |

---

## Supabase SQL 执行顺序（运维 / 执行 Agent 自检）

在 **Supabase Dashboard → SQL Editor** 中 **按序**执行（每文件顶部有中文「用途」说明，可直接整段复制）：

| 顺序 | 文件 | 用途 |
|------|------|------|
| 1 | `docs/text2sql/v1/sql/chatbi_01_access_tokens.sql` | 创建 **`public.chatbi_access_tokens`**（T1：Bearer 哈希 + `access_level`） |
| 2 | `docs/text2sql/v1/sql/chatbi_02_sql_table_policy.sql` | 创建 **`public.chatbi_sql_table_policy`**（T2：表级 min_* 等级） |
| 3（可选） | `docs/text2sql/v1/sql/chatbi_03_seed_table_policy_demo.sql` | 为 `agent_info` 写入 **演示** policy（可按环境删改） |
| 4 | `docs/text2sql/v1/sql/chatbi_04_user_portrait.sql` | 创建 **`public.chatbi_user_portrait`**（L2 习惯 / 长久 Prompt） |

**插入访问令牌行**：**不要**在 SQL 里写明文 token；在本地生成 `key_hash` 后只执行 `INSERT`（见下节 RUNBOOK）。

---

## RUNBOOK：生成 `key_hash`（本地执行，勿提交明文）

与实现代码 **必须一致**（推荐 SHA-256 十六进制 **小写**；可选 env **pepper**）：

```bash
python3 -c "import hashlib, os; t=b'在此处粘贴明文token'; p=os.environ.get('CHATBI_ACCESS_TOKEN_PEPPER','').encode(); print(hashlib.sha256(p+t).hexdigest())"
```

将输出写入：

```sql
insert into public.chatbi_access_tokens (key_hash, access_level, subject_user_id, label)
values ('<上一步输出的hex>', 0, null, 'Super-demo');
-- access_level: 0=Super, 1=Admin, 2=L2；L2 须填 subject_user_id（与 chatbi_user_portrait.user_id 一致）
```

**策略判定（与 `chatbi_02` 文件头注释一致）**：`access_level` 越小权限越高；某操作 `min_*_level` **为 NULL** → 该操作对**所有**等级关闭；非 NULL 时 **允许当且仅当** `主体.access_level <= min_*_level`。

---

## 验收标准

### P0 口径

- [ ] 实现与 OpenItems **§1.4** 一致：**软删允许**；L2 **禁 INSERT**、**禁 JOIN**；**肖像表**写模型；Super **目标态**不依赖 env 长期真值（过渡期须在 `PROJECT_CONFIG` 说明）

### P1 数据面

- [ ] Supabase 上存在 `chatbi_access_tokens`、`chatbi_sql_table_policy`、`chatbi_user_portrait`（及可选 policy 种子），与 `docs/text2sql/v1/sql/chatbi_0*.sql` 一致

### P2 鉴权

- [ ] 无 `Authorization: Bearer` 或哈希不匹配 → **401**（或与现网统一错误模型）  
- [ ] `revoked_at is not null` 或 `expires_at < now()` → 视为无效  

### P3 Text2SQL 闸门（含前/后双闸）

- [ ] **前闸**：进入模型的 schema / 表字典与 OpenItems **§1.5** 一致（缩小暴露面）  
- [ ] **后闸**：AST + 表白名单 + `access_level`；**Admin**：物理 `DELETE`/`TRUNCATE` 拒绝、软删类 `UPDATE` 允许  
- [ ] **L2**：拒绝 **JOIN**、**INSERT**；**UPDATE** 仅 **`chatbi_user_portrait`** 且 **不得 SET `user_id`**，列须在白名单（首期 `long_term_prompt`）  
- [ ] 越权：用户可见「您无此权限」+ 结构化 `code`（如 `CHATBI_SQL_DENIED`）  

### P3b 日志（可与 P3 同 PR）

- [ ] 开启 `CHATBI_JSON_LOG` 时，按 OpenItems **§1.6** 写入 `auth_*` / `sql_gate_*` 事件（无 Bearer 明文、无完整 SQL 或已脱敏）

### P4 RAG 预留

- [ ] 检索函数签名或上下文 dataclass 含 `principal_kind` / `access_level` / `subject_user_id`，默认不改变检索结果  

---

## 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `<回填>` |
| 关键 env | `CHATBI_ACCESS_TOKEN_PEPPER`（可选，与 RUNBOOK/Python 一致） |
| SQL 执行顺序 | `chatbi_01` → `chatbi_02` →（可选）`chatbi_03` → `chatbi_04` |
| 接口变更 | `<回填：哪些路由挂载 Depends>` |
| 图谱变更点 | `<回填>` |

---

## 给 Cursor 的稳定关键词

`task_chatbi_level_gate_v1`、`chatbi_access_tokens`、`chatbi_sql_table_policy`、`chatbi_user_portrait`、`Text2SQL`、`Bearer`、`access_level`、`OpenItems`、`CHATBI_JSON_LOG`
