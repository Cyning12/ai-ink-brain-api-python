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

### 3.0 迭代拍板（与产品对齐 · 2026-05-11）

| # | 决议 | 说明 |
|---|------|------|
| **1** | **前端注册延后** | **首迭代** 不设公开注册；**注册用户 / 超管 / 临时管理员** 均由 **运维在 Supabase 中手工插入**（或 Dashboard 操作）直至注册功能另立任务。 |
| **2** | **超管 key 生成不对外开放** | 仅 **本地可调用** 的生成能力（CLI / `tools/*.py`），使用 **env 配置的根物料**（命名由实现 PR 定，例：`CHATBI_ROOT_KEY_MATERIAL`）参与 **随机 opaque token** 的派生与 **入库哈希**；**禁止**暴露「任意人可调用的 HTTP 生成接口」。**与临时管理员校验必须可区分**：推荐 **分表**（`super_admin_api_keys` vs `temp_admin_keys`）或 **同表强制 `key_kind` 枚举 + 独立校验分支**；可选更强方案见 **§3.7**。 |
| **3** | **临时管理员 key 由超管在页内生成** | **超管**在 **当前管理页** 点击 **生成** → **每次** 写入 DB（哈希）→ **当页一次性展示** 明文（离开页面不再展示）；**有效期暂定 12 小时**（`expires_at = now() + 12h`，实现可用常量或 env 覆盖）。 |

### 3.1 设计顺序（建议）

1. **冻结**本子规 **§3.2–§3.3**（四类用户 + 模块矩阵）。  
2. **用户表 / 密钥表** 逻辑模型（**§3.6**）→ migration / RLS 草案 → **任务单** 验收 `- [ ]`。  
3. **BFF + Python** 统一鉴权中间件：解析主体 → `user_kind` / `scopes` → 路由与 **Unified Chat** 入口闸门。  
4. 与 **`SPEC-ChatBI-V3-Security.md`**（表白名单）、**`SPEC-ChatBI-V3-Multiturn-Debt.md` §4**（澄清话术表名脱敏）**对表**。

### 3.2 四类用户（产品定义）

| 用户类型 | 建议 slug | 创建 / 发放入口 | 凭证与存储 | 初版模块范围 |
|----------|-------------|-----------------|-------------|--------------|
| **超管** | `super_admin` | **首期**：与注册用户一致，由 **运维在 Supabase 手工维护**；**根级 API key** 的 **批量/轮换生成** 走 **§3.7 本地 CLI**（不开放公网接口） | **根级密钥**：表内存 **哈希 + 审计**；派生依赖 **env 根物料**（仅本机/CI 持有）；**禁止**把根物料写入前端 bundle | **全部**（含 **Unified Chat**、学习日志、学习资源、任务及未来管理模块） |
| **注册用户** | `registered_user` | **首期**：**无**前端注册 — **全部由本人在 Supabase 插入**（或等价后台操作）；**公开注册** 延后至独立任务 | 与超管/临时区分：**Auth 用户行** 或 **profile 表 `user_kind=registered`** + 后续会话方案（实现 PR 定） | **浏览为主**：**学习日志**、**学习资源**、**任务**；**默认不含** Unified Chat |
| **临时管理员** | `temp_admin` | **超管**在 **管理页** 点击生成（**§3.0 #3**）；**无**自助注册 | **12h TTL** API key：仅存 **哈希**；明文 **仅当页一次展示**；详见 **§3.4** | 三学习模块 **+** **Unified Chat** |
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

### 3.4 临时管理员 key 生命周期（拍板 + 实现留白）

| 主题 | 要求（当前拍板） |
|------|------------------|
| **入口** | **仅超管**：管理页 **「生成临时管理员 key」** 按钮；**非超管**不可见、不可调。 |
| **生成** | 每次点击生成 **新** opaque token → **立即** `INSERT`（哈希、`expires_at`、`scopes`、`created_by`）；**同一页**展示 **完整明文一次**（刷新/路由离开即不再展示；**禁止**仅依赖 `alert` 长期留存 — 实现可用可复制文本框 + 复制确认）。 |
| **TTL** | **默认 12 小时**：`expires_at = created_at + 12h`（可用 env 常量覆盖，如 `TEMP_ADMIN_KEY_TTL_HOURS`，默认 `12`）。 |
| **存储** | DB **仅存哈希** + `expires_at` + `revoked_at` + `scopes` + `created_by`；**禁止**日志打印明文。 |
| **校验** | API 查 **`temp_admin_keys`**（或带 `key_kind=temp_admin` 的分支），**必须**校验未过期、未吊销；与 **超管 key 表/分支** 分离（**§3.7**）。 |
| **失效** | 到期、`revoked_at`、超管 **手动吊销**；是否允许多 key 并存 — **默认可**（每次生成一条新记录），旧 key 可按产品选择 **立即吊销** 或 **自然到期**。 |
| **与 JWT** | 若 Unified Chat 使用短期 JWT：**签发 claims** 须含 `user_kind`/`scopes`；**吊销**是否与 key 表联动 — **待决**。 |

### 3.5 与 env 明文 Admin Key 的迁移关系

| 阶段 | 行为 |
|------|------|
| **现状** | `API_KEY`、`NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` 等 — 适合 **开发 / 单操作者**；与 **多角色、审计、临时用户** 不兼容。 |
| **过渡** | 可保留 **单根 bootstrap** 用于紧急运维；**新**超管 / 临时管理员以 **Supabase 表** 为准。 |
| **目标** | 注册用户 **仅** Auth；**临时 / 超管** **不**依赖浏览器长期持有明文 env；**对外表述** 在迁移完成前仍遵守 Gap / 简历分层。 |

### 3.6 用户与密钥 — 逻辑模型（非最终 DDL）

以下 **表名可调整**；列仅为 **设计占位**，真值以 **migration + `PROJECT_CONFIG`** 为准。

1. **`auth.users`**（Supabase 内置）：**注册用户** 主键来源；**首期** 可与 **§3.0** 一致由运维 **手工建用户**，无自助注册流。  
2. **`app_user_profile`**（建议）：`user_id` FK → `auth.users`、`user_kind`（`registered` / `super_admin` 等 — **实现 PR 枚举**）、`created_at`、展示名等。  
3. **`super_admin_api_keys`**（推荐 **与临时表分表**）：`id`、`key_hash`、`label`（可选）、`expires_at` nullable（超管 key 可 **长期** 或 **也设轮换周期** — 与临时 **12h** 策略分离）、`revoked_at`、`created_at`、`metadata`；**校验路径** 仅匹配本表。  
4. **`temp_admin_keys`**：`id`、`key_hash`、`label`（可选）、`expires_at`（**默认 +12h**）、`revoked_at`、`scopes` JSON、`created_by`（超管 user id）；**校验路径** 仅匹配本表。  
5. **`role_module_matrix`（可选）**：若不想硬编码在仓库，可将 **§3.3** 迁入 DB；初版亦可 **代码常量 + 单测**。

**RLS**：注册用户仅能读写 **本人** 学习日志等行 — **实现 PR** 与 Security 子规 **§2** 协同拍板。

### 3.7 超管 API key：本地生成与和「临时管理员」的安全隔离

| 主题 | 要求 |
|------|------|
| **暴露面** | **无**公网可调用「生成超管 key」API；仅 **开发者本机**（或受控 CI）运行 **本地命令**，读取 **env 根物料** 完成 **随机 token 生成 + bcrypt/scrypt/argon2 类哈希** 后，由操作者 **手动粘贴 SQL** 或使用 **Supabase service role 脚本** 写入 **`super_admin_api_keys`**。 |
| **根物料** | env 中 **单一高熵 secret**（实现 PR 命名并写入 `PROJECT_CONFIG` / `.env.example`）；**不得**提交到 git；**不得**进入 Next `NEXT_PUBLIC_*`。 |
| **与临时 key 区分（必选其一）** | **A 分表**（推荐）：`super_admin_api_keys` vs `temp_admin_keys`，鉴权中间件 **先解析 token 形态或前缀**（实现 PR 定义，如 `sk_super_` / `tk_temp_`）再查对应表。**B 同表**：必须 `key_kind ∈ {super_admin, temp_admin}` + **两段独立校验函数**，临时 **强制** `expires_at` 与 **12h** 策略；超管可走不同 TTL 或无 TTL。 |
| **更安全演进（可选）** | 根物料仅用于 **KMS 包装** 或 **Supabase Vault**；bearer 为 **短期交换票据**；或临时访问改为 **Edge Function 代发 JWT**。首迭代 **不强制**，在任务单记录 **技术债**。 |
| **请求校验顺序（建议）** | `Authorization` Bearer →（可选前缀路由）→ 查 **temp** 表且校验 TTL → 未命中再查 **super** 表 → 均失败则 401；**禁止**两表同一哈希算法却共用同一查找入口导致 **类型混淆**。 |

### 3.8 正式环境如何校验？要不要前端 `input`？

| 环节 | 说明 |
|------|------|
| **本地生成在做什么** | 只在 **造密钥 + 哈希 + 写入 Supabase**；**不参与**线上请求。 |
| **正式环境校验发生在哪里** | **只在服务端**：Ink **BFF** 或 **`ai-ink-brain-api-python`** 收到请求时，读取 **`Authorization: Bearer …`**（或与现网一致的 **`X-Admin-Token` / `X-Blog-Admin-Token`**），对 **`super_admin_api_keys` / `temp_admin_keys`** 做 **常量时间比较** + **过期/吊销** 检查；**前端不「校验」**，只负责 **是否把 secret 放进请求**（或由 BFF 代放）。 |
| **可不可以用前端 `input`** | **可以，但只是入口形态**：例如「管理员设置」页用 **`<input type="password">` 粘贴一次」** 把 key 交给 **服务端**，由 **Server Action / Route Handler** 写入 **httpOnly + Secure + SameSite** 的会话 cookie，或换 **短期 session**；**避免**把高权限 key **长期**放在 **`localStorage` / `NEXT_PUBLIC_*`**（XSS 与泄露面）。 |
| **临时管理员** | 超管页生成后 **复制发给对方**；对方若用浏览器访问产品：同样 **一次粘贴 → 服务端会话** 优于长期本地明文；若仅用 **curl / SDK**，则与 P0 验收一样 **每请求 Header 带 Bearer** 即可，**无需**常驻 input。 |
| **与现网过渡** | 在表鉴权未上线前，仍可并行保留 **env `API_KEY` / Admin secret`** 作为 bootstrap；上线后逐步收口到 **表内哈希校验**。 |

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
- **首个** 超管用户行与 **首条** `super_admin_api_keys`（**§3.6**）由 **§3.7 本地 CLI** 还是纯 SQL seed 生成、谁保管根物料？  
- 是否允许「无角色 = 仅 **anonymous**（§3.2）」直至开放注册？  

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
| 2026-05-11 | **§3.0 拍板**：注册延后全手工插入；超管 key 仅本地生成 + **§3.7** 与临时校验隔离；临时 key 超管页生成、当页展示、**TTL 12h**；**§3.6** 分表建议 |
| 2026-05-11 | **§3.8**：正式环境服务端校验 Bearer；前端 `input` 仅作一次性录入 + 优先 httpOnly 会话，避免长期 localStorage |
