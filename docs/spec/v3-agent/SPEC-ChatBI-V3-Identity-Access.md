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
| **数据域** | 行级/表级可见集合（**Supabase RLS** / **应用层过滤** / **组合** — **实现 PR 落地时必选其一为真值**）。**个人项目 / 首期**：**可**在 **实际开发 PR** 再拍板，本子规 **不阻塞**身份矩阵与 Bearer 链；定案后写入 **`PROJECT_CONFIG` + migration 注释**。 |

> **与 §3 命名**：**§3.2** 以 **`user_kind` slug**（如 `super_admin`、`temp_admin`）为 **产品真值**；上表 **抽象角色名** 与企业 Gap 对齐，**映射**（例如 `super_admin` → 管理类能力）由 **实现 PR** 落在矩阵与代码常量，本子规 **不**强制一一重命名。

---

## 3. 产品用户类型、模块矩阵与落表方向（扩充）

> **与总规关系**：对应 Overview **§2.1 P1-3**；**先于**「仅做 SQL AST」（Security P1-1）把 **谁可以进哪个模块** 定清，可避免 Unified Chat / Text2SQL / 澄清话术 **越权展示** 返工。  
> **现状真值**：Ink / BFF / Python 当前多为 **env 明文 Admin Key + 非 admin 二元**（见 `PROJECT_CONFIG`、`unified_chat` 鉴权）；下列为目标态 **产品语义**，DDL 以 **实现 PR + Supabase migration** 为准。

### 3.0 迭代拍板（与产品对齐 · 2026-05-11）

| # | 决议 | 说明 |
|---|------|------|
| **1** | **前端注册延后** | **首迭代** 不设公开注册；**注册用户**（及若需 **profile 行** 的 **超管 / 临时**）由 **运维在 Supabase 手工插入**（或 Dashboard）直至注册另立任务。**说明**：**仅走 env 超管（§5.1 路径 A）** 时 **可不建** `auth.users` / `app_user_profile` 超管行；**表内 Bearer 超管 / 临时** 的 `created_by` 等若引用用户 id，以 **实现 PR** 为准。 |
| **2** | **超管 + 临时：个人项目简化** | **超管**：**路径 A** — **`NEXT_PUBLIC_ADMIN_SECRET`**（及后端对齐 secret）作 **env Bearer 超管**（**§5.1**）。**路径 B（可选）** — **`super_admin_api_keys`**：本机造 token、生产 **只**验表内 token（与 **§3.7**、**§5.3** 一致）。若 **路径 A 保管可信**，路径 B 的 **建设优先级可降低**（§3.7）。**临时 / 演示**：**只**给对方 **生成后 opaque token**；**`CHATBI_TEMP_ADMIN_SECRET`** **仅**本机/CLI **写 `temp_admin_keys`** 的根材料（**§5.1**），**不**进请求链、**不**给对方；滥用防护：**TTL / 吊销 / 限流**。 |
| **3** | **临时管理员 key 由超管在页内生成** | **超管**在 **当前管理页** 点击 **生成** → **每次** 写入 DB（哈希）→ **当页一次性展示** 明文（离开页面不再展示）；**有效期暂定 12 小时**（`expires_at = now() + 12h`，实现可用常量或 env 覆盖）。 |

### 3.1 设计顺序（建议）

1. **冻结**本子规 **§3.2–§3.3**（四类用户 + 模块矩阵）。  
2. **用户表 / 密钥表** 逻辑模型（**§3.6**）→ migration / RLS 草案 → **任务单** 验收 `- [ ]`。  
3. **BFF + Python** 统一鉴权中间件：解析主体 → `user_kind` / `scopes` → 路由与 **Unified Chat** 入口闸门。  
4. 与 **`SPEC-ChatBI-V3-Security.md`**（表白名单）、**`SPEC-ChatBI-V3-Multiturn-Debt.md` §4**（澄清话术表名脱敏）**对表**。

### 3.2 四类用户（产品定义）

| 用户类型 | 建议 slug | 创建 / 发放入口 | 凭证与存储 | 初版模块范围 |
|----------|-------------|-----------------|-------------|--------------|
| **超管** | `super_admin` | **路径 A**：**`NEXT_PUBLIC_ADMIN_SECRET`**（与现 BFF/Python 一致），**可无** Supabase profile 行。**路径 B**：本机/CLI 写 **`super_admin_api_keys`**（仅存哈希），请求带 **生成后 token**（§3.7）。A/B **并存** 时校验顺序 **§5.3**；若产品仅需其一，另一路径 **实现可关** | **路径 A**：env secret（**勿**进仓库）。**路径 B**：表内 **仅哈希** + 过期/吊销 | **全部** |
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
| **与 JWT** | 若 Unified Chat 使用短期 JWT：**签发 claims** 须含 `user_kind`/`scopes`（字段名实现自定）。**吊销与 `temp_admin_keys` / `super_admin_api_keys` 联动**（如 `jti`↔行 id、版本号、黑名单表）— **个人项目 / 首期可开发 PR 再定**，本子规 **不阻塞**；若做联动须在 **任务单 + Security 子规** 写清验收（**撤销 key 后旧 JWT 最长存活窗口**）。 |

### 3.5 与 env 明文 Admin Key 的迁移关系

| 阶段 | 行为 |
|------|------|
| **现状** | `API_KEY`、`NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` 等 — 适合 **开发 / 单操作者**。 |
| **个人项目过渡（§5）** | **超管**：**路径 A** **`NEXT_PUBLIC_ADMIN_SECRET`**；**可选路径 B** **`super_admin_api_keys`**（本机造 token、生产只验表，**§5.1**）。**临时**：**`temp_admin_keys`**（对方 **只**持 **生成后 token**）+ 可选 **`CHATBI_TEMP_ADMIN_SECRET`**（**仅**本地写 **temp** 表，**§5.1**）。**不强制**首期上齐两表。 |
| **目标（远期）** | 注册用户 **仅** Auth；高权限 **减少** 对长期 env 明文依赖；**对外表述** 仍遵守 Gap / 简历分层。 |

### 3.6 用户与密钥 — 逻辑模型（非最终 DDL）

以下 **表名可调整**；列仅为 **设计占位**，真值以 **migration + `PROJECT_CONFIG`** 为准。

1. **`auth.users`**（Supabase 内置）：**注册用户** 主键来源；**首期** 可与 **§3.0** 一致由运维 **手工建用户**，无自助注册流。  
2. **`app_user_profile`**（建议）：`user_id` FK → `auth.users`、`user_kind`（`registered` / `super_admin` 等 — **实现 PR 枚举**）、`created_at`、展示名等。  
3. **`super_admin_api_keys`**（推荐 **与临时表分表**）：`id`、`key_hash`、`label`（可选）、`expires_at` nullable（超管 key 可 **长期** 或 **也设轮换周期** — 与临时 **12h** 策略分离）、`revoked_at`、`created_at`、`metadata`；**校验路径** 仅匹配本表。  
4. **`temp_admin_keys`**：`id`、`key_hash`、`label`（可选）、`expires_at`（**默认 +12h**）、`revoked_at`、`scopes` JSON、`created_by`（超管 user id）；**校验路径** 仅匹配本表。  
5. **`role_module_matrix`（可选）**：若不想硬编码在仓库，可将 **§3.3** 迁入 DB；初版亦可 **代码常量 + 单测**。

**RLS**：注册用户仅能读写 **本人** 学习日志等行 — **实现 PR** 与 Security 子规 **§2** 协同拍板；**首期无 RLS、仅应用层过滤** 亦为个人项目可接受，**上线前**在 PR 说明威胁面与补救路径即可。

### 3.7 超管 API key：本地生成与和「临时管理员」的安全隔离

| 主题 | 要求 |
|------|------|
| **个人项目默认** | **超管** 以 **`NEXT_PUBLIC_ADMIN_SECRET`**（及后端对齐变量）为主。**若 env 超管保管可信**，**`super_admin_api_keys` 表** 与 **CLI 轮换** 的 **实施优先级降低**（可后置）。 |
| **暴露面（可选表路径）** | **无**公网「生成超管 key」API；若启用表：仅 **本机 CLI** 读取 **env 根物料**（可与超管 secret **不同**的 `CHATBI_ROOT_KEY_MATERIAL`）生成 opaque → 哈希 → **INSERT `super_admin_api_keys`**。 |
| **表内超管与 temp 同理（拍板）** | **`super_admin_api_keys`**：**仅**本机/CLI **造 token + 写哈希**；**生产 HTTP** **只**用 **生成后的 Bearer token** 与本表做常量时间比对（+ 过期/吊销）；**根物料 env** **仅**脚本读、**不参与**请求期 Authorization 与表内 token 的混用对照。与 **`temp_admin_keys`** **不同表**、**不同 TTL/吊销策略**、**不同校验函数**（§3.7 分路）。 |
| **根物料（可选表路径）** | 与 **`NEXT_PUBLIC_ADMIN_SECRET`** 分离命名，**不得**提交 git；**不得** `NEXT_PUBLIC_*` 泄露根物料。 |
| **与临时 key 区分（必选其一）** | **A 分表**（推荐）：`super_admin_api_keys` vs `temp_admin_keys`，鉴权中间件 **先解析 token 形态或前缀**（实现 PR 定义，如 `sk_super_` / `tk_temp_`）再查对应表。**B 同表**：必须 `key_kind ∈ {super_admin, temp_admin}` + **两段独立校验函数**，临时 **强制** `expires_at` 与 **12h** 策略；超管可走不同 TTL 或无 TTL。 |
| **更安全演进（可选）** | 根物料仅用于 **KMS 包装** 或 **Supabase Vault**；bearer 为 **短期交换票据**；或临时访问改为 **Edge Function 代发 JWT**。首迭代 **不强制**，在任务单记录 **技术债**。 |
| **请求校验顺序（建议）** | 与 **§5.3** **须一致**（实现与文档同链）：**`temp_admin_keys`**（**必须** `expires_at`）→ **（若建设）`super_admin_api_keys`**（按该表 TTL/吊销策略）→ **`NEXT_PUBLIC_ADMIN_SECRET` / admin_secret** → **（若保留）`API_KEY`** → **401**。**`CHATBI_TEMP_ADMIN_SECRET`**、**写表用根物料 env** **不参与** HTTP 对照。**禁止**两表共用同一模糊查找入口导致 **类型混淆**；可用 **token 前缀**（实现 PR 定）先分路再查库。 |

### 3.8 正式环境如何校验？要不要前端 `input`？

| 环节 | 说明 |
|------|------|
| **本地生成在做什么** | 只在 **造密钥 + 哈希 + 写入 Supabase**；**不参与**线上请求。 |
| **正式环境校验发生在哪里** | **只在服务端**：Ink **BFF** 或 **`ai-ink-brain-api-python`** 读取 **`Authorization: Bearer …`**（或现网 **`X-Admin-Token` / `X-Blog-Admin-Token`**），按 **§5.3** 顺序尝试：**`temp_admin_keys`**、**`super_admin_api_keys`**（若建设）、**env 超管 secret**、**`API_KEY`**；对 **表路径** 做 **常量时间比较** + **过期/吊销**。**前端不「校验」**，只负责 **是否把 token/secret 放进请求**（或由 BFF 代放）。 |
| **可不可以用前端 `input`** | **可以，但只是入口形态**：例如「管理员设置」页用 **`<input type="password">` 粘贴一次」** 把 key 交给 **服务端**，由 **Server Action / Route Handler** 写入 **httpOnly + Secure + SameSite** 的会话 cookie，或换 **短期 session**；**避免**把高权限 key **长期**放在 **`localStorage` / `NEXT_PUBLIC_*`**（XSS 与泄露面）。 |
| **临时管理员** | 超管页生成后 **复制发给对方**；对方若用浏览器访问产品：同样 **一次粘贴 → 服务端会话** 优于长期本地明文；若仅用 **curl / SDK**，则与 P0 验收一样 **每请求 Header 带 Bearer** 即可，**无需**常驻 input。 |
| **与现网过渡** | 在表鉴权未上线前，仍可并行保留 **env `API_KEY` / Admin secret`** 作为 bootstrap；上线后逐步收口到 **表内哈希校验**。 |

### 3.9 前端 `input`、信道安全与会话 token（改进草案 · 纠偏 MD5/SHA）

> **背景**：产品希望 **前端有 password `input`**、先取「临时加密材料」再调登录、成功后发 **会话 token**、全站携带、失效 **401** 登出。下列在 **保留意图** 的前提下 **纠正密码学表述** 并给出 **可落地两档方案**。

#### 3.9.0 概念纠偏（实现前必读）

| 误区 | 正解 |
|------|------|
| 「**SHA-256 非对称加解密**」 | **SHA-256 / MD5 均为散列**，单向、**无可逆解密**；**不是**非对称加密。 |
| 「**MD5 加密 password**」 | **禁止**用 MD5 处理口令（已破解、无盐历史包袱）；**不得**称「解密 MD5」。 |
| 「非对称」若确有需要 | 使用 **RSA-OAEP / ECDH + AES-GCM**（WebCrypto）等；见 **§3.9.2 B 管道**。 |
| 默认信道机密性 | **HTTPS（TLS）** 已加密传输；多数场景 **不必**在 TLS 上再叠 MD5/SHA「假加密」。 |

#### 3.9.1 意图对齐（与你原 8 步对应）

| 意图 | 本子规落点 |
|------|------------|
| 登录前有 **独立一步** 取材料 | **`POST …/auth/exchange`**（可对外仍叫 `auth_code`，但响应体建议命名 `exchange_token` / `exchange_id`）。 |
| 材料 **短时、入库、消费一次即失效** | 表字段：`exchange_hash`、`expires_at`（建议 **60–120s**）、`consumed_at`；成功登录 **必须**写 `consumed_at`。 |
| 前端 **`input`** 输入口令 | **允许**；口令 **仅出现在 TLS 内的请求体**（见 **A 管道**）。 |
| 成功后发 **前端 token**、请求全带、失效 **401** | **会话 cookie（httpOnly）** 或 **短 TTL JWT**；中间件统一校验，**401 → 清会话 + 登出**。 |

#### 3.9.2 推荐两档实现

**A 管道 — 简单（首迭代推荐）：TLS + 一次性 exchange（无额外「密码学表演」）**

| 步 | 端 | 行为 |
|----|-----|------|
| 1 | 前端 | 调 **`POST /auth/exchange`**（无密码）。 |
| 2 | 后端 | 生成高熵 **`exchange_token`** → **只存哈希** + `expires_at` → 响应返回 **明文一次**（离开响应即依赖前端不记录日志）。 |
| 3 | 前端 | 用户在 **`input[type=password]`** 输入口令；**`POST /auth/login`** 带 Header **`X-Login-Exchange`**（或 body 字段）+ **password 明文 JSON**（**全程 HTTPS**）。 |
| 4 | 后端 | 校验 exchange（未过期、未消费、`compare_digest`）→ **立即标记 consumed** → 校验用户/API key 身份 → 发 **Set-Cookie** 或 **JWT**；**失败**亦建议 **吊销该 exchange** 或计失败次数。 |
| 5 | 前端 | **优先** **httpOnly + Secure + SameSite** cookie；若必须 `localStorage` 存 JWT：**短 TTL** 并记录 **技术债**。 |
| 6 | 全站 | BFF/Python **鉴权中间件**；会话无效 **401**；前端 **登出**。 |

**B 管道 — 若强制「口令不以明文 JSON 出浏览器逻辑层」**（复杂，vNext 可）

| 步 | 行为 |
|----|------|
| 1 | **`/auth/exchange`** 返回 **`exchange_id` + RSA/ECDH 公钥**（服务端私钥不落盘到前端）。 |
| 2 | 前端 **WebCrypto**：用公钥封装 **AES-256-GCM** 对称密钥 → 加密载荷 **`{ password, exchange_id, iat }`**。 |
| 3 | **`/auth/login`** 只收密文包；服务端私钥解密 → 再走与 **A** 相同的 **身份校验 + 会话签发**；**exchange 单次消费**。 |

> **选型**：默认 **A**；**B** 记入任务单 **技术债**，**除非**威胁模型明确要求。

#### 3.9.3 对你原 8 条逐条修订（便于 PR 描述对照）

| # | 原表述 | 修订 |
|---|--------|------|
| 1 | env 生成「加密 key」返前端 | 改为 **`exchange_token`**：**随机高熵**；可用 env **仅作 HMAC pepper** 绑定 `exchange_id`，**不要**与长期 session secret 混名。 |
| 2 | 用 key 对 password **MD5** | **废止**；口令依赖 **TLS** 传；若上 **B** 管道则用 **AES-GCM 密文** 代替 MD5。 |
| 3 | 加密后的 key 调 auth | 改为：带 **`X-Login-Exchange` + password（A）** 或 **密文包（B）**。 |
| 4 | 后端「解密 MD5」 | 改为：**验 exchange** + **身份源校验**（表内 key / 未来 Argon2 口令哈希）。 |
| 5 | 成功后失效前端材料 | **必须**：`consumed_at`；失败多次 **可选** 吊销 exchange。 |
| 6–7 | 返回 token、全请求携带 | **cookie 优先**；JWT 则 **access 短 + refresh 策略** 另文。 |
| 8 | 401 | **保留**：统一中间件；**401** 与 **403** 语义分离（可选）。 |

#### 3.9.4 附加要求（补充）

- **速率限制**：`/auth/exchange`、`/auth/login` **按 IP / 指纹 / 用户** 限流。  
- **CSRF**：cookie 会话时，对 **状态变更** 路由带 **CSRF token** 或 **SameSite=strict** 策略拍板。  
- **审计**：登录成功/失败写 **结构化日志**（**无**口令明文）；可与 **`CHATBI_JSON_LOG`** 字段对齐（另任务）。  
- **与 §3.7 表内 API key**：人类 **口令登录流**（§3.9）与 **Bearer API key**（§3.7/§3.8）可 **并存**；路由层 **勿**混用同一 handler 导致绕过。

#### 3.9.5 端点名草稿（实现可改名）

| 路由（草稿） | 职责 |
|--------------|------|
| `POST /api/py/auth/exchange` | 签发 **一次性 exchange**（对应原 **`auth_code`** 意图） |
| `POST /api/py/auth/login` | 消费 exchange + 建立会话 |
| `POST /api/py/auth/logout` | 吊销会话 |

#### 3.9.6 个人项目选型（2026-05-11 拍板）

- **仅实施 §3.9 A 管道**（TLS + `exchange` + cookie / 短 JWT）；**不**做 RSA/WebCrypto **B 管道**。  
- **威胁模型**：个人 / 小团队 **「较为安全即可」**；仍以 **HTTPS + httpOnly + 限流** 为基线。

### 3.10 本子规须显式留痕的交叉项（其余进任务单）

> **`exchange` 表、BFF 转发、middleware、多 secret 顺序、`PROJECT_CONFIG`、Ink 任务链等** — **不在**本子规逐条展开，由 **implementation 任务单** 收敛即可。

| 项 | 说明 |
|-----|------|
| **与 `CHATBI_JSON_LOG` 对齐（可选）** | 登录 / 鉴权 / **表内 key 身份**（`temp_admin` / **表内** `super_admin` 等，**无** token 原文）相关 **结构化日志**（**无**口令、**无** Bearer 明文）若开启 **`CHATBI_JSON_LOG`**，字段与 **`run_id` / `request_id`** 口径见 [`SPEC-ChatBI-V3-Logging-Trace.md`](SPEC-ChatBI-V3-Logging-Trace.md) 与 P0 RUNBOOK；**是否**纳入首包由任务单 `- [ ]` 决定。 |

---

## 4. 与 ChatBI 链路的接合点（须在设计文档中画清）

| 接合点 | 要求 |
|--------|------|
| **Unified Chat 入口** | 解析身份 → 注入 `AgentMemoryStore` / Tool 上下文中的 **只读域提示** |
| **Text2SQL** | 生成 SQL 前已有 **表白名单** 或等价约束（与安全子规 **§2** 协同） |
| **RAG** | 检索命名空间或 `metadata` 过滤与角色绑定 |

---

## 5. 迁移策略（个人项目 · 拍板 2026-05-11）

### 5.1 目标姿态（简化 · 与产品对齐）

| 主题 | 拍板 |
|------|------|
| **登录 / 会话** | **仅**实施 **§3.9 A 管道**（TLS + 一次性 `exchange` + **httpOnly cookie** 或短 TTL JWT）；**不做** §3.9 B（RSA/WebCrypto）。 |
| **超管** | **路径 A（与现网一致）**：**`NEXT_PUBLIC_ADMIN_SECRET`**（及后端对齐的 **`CHAT_API_SECRET` / `admin_secret()`** 等）作 **Bearer 超管**。**路径 B（可选表）**：与 **temp** **同理** — **本机/CLI** 生成 opaque → **`super_admin_api_keys` 仅存哈希**；**生产只验** 请求里 **那条生成后 token** 命中本表（与 **`temp_admin_keys`** **分表**）。A/B **可并存**；校验顺序 **§5.3**。 |
| **`CHATBI_TEMP_ADMIN_SECRET`（本机造 token）** | **范围（拍板收窄）**：**仅**作者 **本地 / CLI** 在 **生成 opaque token 并写入 `temp_admin_keys`（哈希）** 时读取的 **根材料**（HMAC pepper、派生盐等实现自定）；**不**作为给对方复制的 **Bearer**；**不**进入对方浏览器/聊天。**对方** **只**收到 **生成后的那条 token**（与 **§3.0#3** 管理页「当页一次展示」或 CLI 输出一致），线上请求 **只**用该 token 命中 **`temp_admin_keys`**。**请求期鉴权** **不应**再匹配本 env（见 **§5.3**）。滥用防护：**短 TTL**、**吊销**、**限流 / 配额**（数值任务单定）。**历史可选**：若代码曾支持「env 直作 Bearer」，个人项目 **默认关闭**，避免与「只发 token」模型混淆。 |
| **超管 env 可信时的优先级** | **`NEXT_PUBLIC_ADMIN_SECRET`** 保管可信时，**`super_admin_api_keys` 表** 与 **CLI** **可后置**；开发重心放在 **temp 演示链** + **滥用防护**。 |
| **公开注册** | **延后**（§3.0 #1）；用户 **仅 Supabase 手工插入**。 |

### 5.2 本地重新生成（忘记密钥）

| 场景 | 动作 |
|------|------|
| **忘记 `temp_admin_keys` 中某条明文** | **无法再取出**；超管 **管理页重新生成** 或本机 **CLI INSERT 新行**，旧行 **`revoked_at`** 或依赖自然到期。 |
| **忘记可选 `super_admin_api_keys` 表内 key** | 本机 **CLI 再生成** → **UPDATE/INSERT 哈希**；旧行 **`revoked_at`**；**不影响** `NEXT_PUBLIC_ADMIN_SECRET` 仍可用。 |
| **忘记 `NEXT_PUBLIC_ADMIN_SECRET` 本身** | **运维旋转** env 并同步 **Ink / BFF / Python**；**无**应用内自助找回。 |

### 5.3 鉴权优先级建议（实现 PR 与代码一致）

**Bearer 校验**建议顺序（实现与代码一致）：**`temp_admin_keys` 命中且未过期**（Bearer **仅**为 **生成后 token**）→ **（若建设）`super_admin_api_keys` 命中**（同上，**分表**）→ **`NEXT_PUBLIC_ADMIN_SECRET` / admin_secret 等价**（env 超管，**路径 A**）→ **（若保留）`API_KEY`** → **401**。**`CHATBI_TEMP_ADMIN_SECRET`**、**表写入用根物料 env** **不参与**本链（**仅**离线/本机写表，**§5.1**、**§3.7**）。**temp** 路径 **必须** 校验 `expires_at`；**super** 表路径按该表策略（可无 TTL 或另设）。

### 5.4 仍为待决 / 须进任务单

- **`CHATBI_TEMP_ADMIN_SECRET`**：实现上 **禁止**与 **`temp_admin_keys` Bearer** 混为同一校验分支；**限流/配额** 数值。  
- **`super_admin_api_keys` 是否建设**：env 超管可信则 **优先级低**（§5.1）。  
- **`login_exchange`、cookie、CSRF、middleware、BFF** 等 — **任务单** 收敛（本子规 **§3.10** 仅保留 **日志对齐** 一条）。  

**结论**：**§3**、**§5** 与 **§3.10（日志）** 须在 **implementation 任务单** 拆验收 `- [ ]`；**不与** Security AST 同 PR 亦可，但 **模块闸门** 与 **unified 鉴权** 建议先于复杂 SQL AST。

---

## 6. 非范围

- 多租户 **tenant_id** 全链路（划入 V4 / Enterprise §4.3）。  
- SSO/OAuth 完整 IdP 集成 —— **可**列为 V3.1，本初版不强制。

---

## 7. 关联

- [**待决项 / 分议题收敛（姊妹篇）**](SPEC-ChatBI-V3-Identity-Access-OpenItems.md)：数据域等级、企业命名映射、个人项目会话与 Bearer 等 **逐条迭代**；**实施顺序**见该文 **§五（P0–P5）**；**Super / Admin / L2、肖像表、软删、表白名单双闸、结构化日志** 等最新拍板见该文 **§1.4～§1.6**（与主规 §3.2 四类用户命名若冲突，以姊妹篇为迭代真值直至主规回写）  
- [`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md)  
- [`SPEC-ChatBI-V3-Logging-Trace.md`](SPEC-ChatBI-V3-Logging-Trace.md)（`CHATBI_JSON_LOG` / `run_id` 口径）  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

---

## 8. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
| 2026-05-11 | **§3**：四类用户、模块矩阵、临时 key 生命周期、env 迁移、逻辑表模型；原 §3–§7 顺延为 §4–§8 |
| 2026-05-11 | **§3.0 拍板**：注册延后全手工插入；超管 key 仅本地生成 + **§3.7** 与临时校验隔离；临时 key 超管页生成、当页展示、**TTL 12h**；**§3.6** 分表建议 |
| 2026-05-11 | **§3.8**：正式环境服务端校验 Bearer；前端 `input` 仅作一次性录入 + 优先 httpOnly 会话，避免长期 localStorage |
| 2026-05-11 | **§3.9**：登录 exchange + 会话 token 草案；纠偏 MD5/SHA；**A/B** 两档（TLS+单次码 vs RSA+AES-GCM）；端点名草稿 |
| 2026-05-11 | **§3.0#2 / §3.7 / §3.5** 与 **§5** 对齐：`NEXT_PUBLIC_ADMIN_SECRET` 超管、**`CHATBI_TEMP_ADMIN_SECRET`**、本地再生；**§3.9.6** 个人项目仅 A 管道；**§3.10** 遗漏清单 |
| 2026-05-11 | **`CHATBI_TEMP_ADMIN_SECRET`**：演示/可控/防 token 滥用；env 超管可信则 **表内超管 key 优先级降低**；**§3.10** 仅保留 **CHATBI_JSON_LOG** 交叉一条 |
| 2026-05-11 | **`CHATBI_TEMP_ADMIN_SECRET`** 收窄：**仅**本机/CLI **写 `temp_admin_keys` 造 token**；对方 **只**持 **生成后 opaque**；**§5.3** 请求鉴权 **不含**该 env（弃用「env 直作 Bearer」文档化默认关） |
| 2026-05-11 | **`super_admin_api_keys`** 与 temp **同理**（本机造 token、生产 **只**验表内 token）；**§3.7** 新行 + **§5.3** 插入表内超管链 |
| 2026-05-11 | **全文对齐**：§3.0/§3.2/§3.5/§3.7/§3.8 与 **§5.3** Bearer 链一致；§3.0#1 区分 env 超管 **可无 profile**；§2 与 §3 slug **映射说明**；§3.9.2 文案；§3.10 日志条扩至表内超管身份 |
| 2026-05-11 | **§2 数据域 / §3.4 JWT–key 吊销 / §3.6 RLS**：明确 **个人项目可开发 PR 再定**，子规不阻塞；联动与窗口写入任务单与安全子规 |
| 2026-05-12 | **§7**：姊妹篇索引更新：**§五（P0–P5）**、**§1.4～§1.6**（Super/Admin/L2、肖像表、软删、双闸、`CHATBI_JSON_LOG` 字段草案） |
