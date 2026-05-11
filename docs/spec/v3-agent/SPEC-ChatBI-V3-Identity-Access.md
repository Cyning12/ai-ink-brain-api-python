# ChatBI V3 — 身份与访问控制（RBAC + 数据域）

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2.1** P1-3  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §3.1、§4.2 P0

---

## 1. 目标

从 **简单 Token 鉴权**（V2 明确不覆盖企业级权限）演进到：**角色（Role）**、**权限（Permission）**、**数据域（Data scope）** 可表述、可审计、可与 Text2SQL / RAG 工具链 **接合**。

---

## 2. 概念模型（初版 — 设计 PR 可调整命名）

| 概念 | 说明 |
|------|------|
| **主体** | 人用户 / 服务账号（若未来有） |
| **角色** | 如 `admin`、`analyst`、`viewer` |
| **权限** | API 路由级 + 工具级（能否触发 `text2sql_execute`、能否导出） |
| **数据域** | 行级/表级可见集合（与 Supabase RLS 或应用层过滤二选一或组合 — **实现 PR 必选其一为真值**） |

---

## 3. 产品用户类型、模块矩阵与落表方向（扩充）

> **与总规关系**：对应 Overview **§2.1 P1-3**；**先于**「仅做 SQL AST」（Security P1-1）把 **谁可以进哪个模块** 定清，可避免 Unified Chat / Text2SQL / 澄清话术 **越权展示** 返工。  
> **现状真值**：Ink / BFF / Python 当前多为 **env 明文 Admin Key + 非 admin 二元**（见 `PROJECT_CONFIG`、`unified_chat` 鉴权）；下列为目标态 **产品语义**，DDL 以 **实现 PR + Supabase migration** 为准。

### 3.1 设计顺序（建议）

1. **冻结**本子规 **§3.2–§3.3**（四类用户 + 模块矩阵）。  
2. **用户表 / 密钥表** 逻辑模型（**§3.6**）→ migration / RLS 草案 → **任务单** 验收 `- [ ]`。  
3. **BFF + Python** 统一鉴权中间件：解析主体 → `user_kind` / `scopes` → 路由与 **Unified Chat** 入口闸门。  
4. 与 **`SPEC-ChatBI-V3-Security.md`**（表白名单）、**`SPEC-ChatBI-V3-Multiturn-Debt.md` §4**（澄清话术表名脱敏）**对表**。

### 3.2 四类用户（产品定义）

| 用户类型 | 建议 slug | 创建 / 发放入口 | 凭证与存储 | 初版模块范围 |
|----------|-------------|-----------------|-------------|--------------|
| **超管** | `super_admin` | **仅** Supabase 后台或受控 seed / Admin API；**无**前端自注册 | **根级密钥**：写入 Supabase（**哈希 + 审计列**）；**禁止**长期依赖前端 `.env` 明文分发（迁移策略见 **§3.5**） | **全部**（含 **Unified Chat**、学习日志、学习资源、任务及未来管理模块） |
| **注册用户** | `registered_user` | **前端注册**（实现 PR 在 **Supabase Auth** 与 **自建 `app_users` 扩展** 二选一或组合中拍板） | 标准 **Auth 会话**（JWT / cookie）；**非**共享 Admin Bearer | **浏览为主**：**学习日志**、**学习资源**、**任务**；**默认不含** Unified Chat（除非后续改矩阵） |
| **临时管理员** | `temp_admin` | **仅**后台生成；**无**前端注册 | **短 TTL API key** 存表（**仅哈希**、`expires_at`、`revoked_at`、`scopes`）；**轮换 / 续期** 流程见 **§3.4** | 注册用户三模块 **+** **Unified Chat**（及依赖的 BFF → Python API） |
| **未登录** | `anonymous` | — | 无有效凭证 | **仅**注册、登录与公开静态资源；**无**上述业务模块入口 |

### 3.3 模块 ↔ 权限矩阵（初版）

| 模块（产品名） | 超管 | 注册用户 | 临时管理员 | 未登录 |
|----------------|------|----------|------------|--------|
| 学习日志 | ✓ | ✓ | ✓ | ✗ |
| 学习资源 | ✓ | ✓ | ✓ | ✗ |
| 任务 | ✓ | ✓ | ✓ | ✗ |
| Unified Chat（ChatBI 等） | ✓ | ✗ | ✓ | ✗ |
| 其它后台 / 配置（若有） | ✓ | ✗ | ✗（默认；若单列需再开矩阵行） | ✗ |

> **实现注意**：「模块」在 Next 中对应 **路由 / layout 守卫**；在 Python 中对应 **路由前缀 + `text2sql_execute` 等工具闸门**；矩阵变更时同步 **Ink 任务单** 与 **`_tech_graph`** 身份边。

### 3.4 临时管理员 key 生命周期（待实现 PR 细化）

| 主题 | 要求 / 选项 |
|------|----------------|
| **生成** | 仅 **超管**或受控 Server Action / Edge Function；记录 `created_by`、`label`（可选）。 |
| **存储** | DB **仅存哈希**；明文 **仅一次**展示给操作者（下载即焚或复制后即不再显示 — 产品可配置）。 |
| **校验** | API 层 `hmac.compare_digest` 同类比较；**禁止**日志打印明文。 |
| **失效** | `expires_at` 到期、`revoked_at` 非空、或 **手动吊销**；是否允许 **同 label 多 key 并存** 待决。 |
| **与 JWT** | 若 Unified Chat 使用短期 JWT：**签发 claims** 须含 `user_kind`/`scopes`；**吊销**是否与 key 表联动 — **待决**。 |

### 3.5 与 env 明文 Admin Key 的迁移关系

| 阶段 | 行为 |
|------|------|
| **现状** | `API_KEY`、`NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` 等 — 适合 **开发 / 单操作者**；与 **多角色、审计、临时用户** 不兼容。 |
| **过渡** | 可保留 **单根 bootstrap** 用于紧急运维；**新**超管 / 临时管理员以 **Supabase 表** 为准。 |
| **目标** | 注册用户 **仅** Auth；**临时 / 超管** **不**依赖浏览器长期持有明文 env；**对外表述** 在迁移完成前仍遵守 Gap / 简历分层。 |

### 3.6 用户与密钥 — 逻辑模型（非最终 DDL）

以下 **表名可调整**；列仅为 **设计占位**，真值以 **migration + `PROJECT_CONFIG`** 为准。

1. **`auth.users`**（Supabase 内置）：**注册用户** 主键来源。  
2. **`app_user_profile`**（建议）：`user_id` FK → `auth.users`、`user_kind`（`registered`）、`created_at`、展示名等。  
3. **`service_api_keys`**（超管 bootstrap 或服务账号）：`id`、`key_hash`、`kind`（`super_bootstrap` 等）、`expires_at` nullable、`revoked_at`、`metadata` JSON。  
4. **`temp_admin_keys`**：`id`、`key_hash`、`label`、`expires_at`、`revoked_at`、`scopes` JSON（模块键与 **§3.3** 对齐）、`created_by`。  
5. **`role_module_matrix`（可选）**：若不想硬编码在仓库，可将 **§3.3** 迁入 DB；初版亦可 **代码常量 + 单测**。

**RLS**：注册用户仅能读写 **本人** 学习日志等行 — **实现 PR** 与 Security 子规 **§2** 协同拍板。

---

## 4. 与 ChatBI 链路的接合点（须在设计文档中画清）

| 接合点 | 要求 |
|--------|------|
| **Unified Chat 入口** | 解析身份 → 注入 `AgentMemoryStore` / Tool 上下文中的 **只读域提示** |
| **Text2SQL** | 生成 SQL 前已有 **表白名单** 或等价约束（与安全子规 **§2** 协同） |
| **RAG** | 检索命名空间或 `metadata` 过滤与角色绑定 |

---

## 5. 迁移策略（待决）

- **现有 env 明文 key** 如何映射到 **§3.2** 中的 `super_admin` / `temp_admin` / bootstrap？是否保留 **单 env 紧急入口**？  
- **首个** Supabase 超管 seed 与 **首条** `service_api_keys` 谁生成、谁保管？  
- 是否允许「无角色 = 仅 **anonymous**（§3.2）」直至注册完成？  

**结论**：**§3** 矩阵与 **§3.6** 表结构须在 **implementation 任务单** 中拍板（含验收 `- [ ]`）后，再将本规相关段落标为 `stable` 子段；**不与** Security AST **同一 PR 混验收** 亦可，但 **模块闸门** 应先于或并行于 **SQL 深度防护** 以免产品越权。

---

## 6. 非范围

- 多租户 **tenant_id** 全链路（划入 V4 / Enterprise §4.3）。  
- SSO/OAuth 完整 IdP 集成 —— **可**列为 V3.1，本初版不强制。

---

## 7. 关联

- [`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md)  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

---

## 8. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
| 2026-05-11 | **§3**：四类用户、模块矩阵、临时 key 生命周期、env 迁移、逻辑表模型；原 §3–§7 顺延为 §4–§8 |
