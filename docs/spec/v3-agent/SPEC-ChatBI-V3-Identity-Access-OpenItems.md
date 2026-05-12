# ChatBI V3 — 身份子规「待决项」关联文档

> **状态**：`draft`（**非最终方案**；与主规冲突处以本文 **显式标注** 为准，并应在后续 PR 中 **回写** [`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md)）  
> **主规**：[`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md)  
> **用途**：将主规中「待明确」议题 **逐条收敛**；本条记录 **一～三** 的当前产品意图，**四** 起占位后续议题。

---

## 0. 使用方式

- 每条议题下含：**当前结论 / 草案**、**待补全（验收前必须回答）**、**与主规差异（若有）**。  
- 实现时以 **`PROJECT_CONFIG` + migration + Security（SQL AST）子规** 为真值；本文 **不替代** DDL。

---

## 一、数据域 + Text2SQL 执行等级（已补充口径 · 实现以 PR 为准）

### 1.1 产品意图（摘要）

- **档位**（库内 `access_level` 数值见 **§1.2**）与 **`chatbi_sql_table_policy`** 共同约束 Chat 链路中 **Text2SQL 产出 SQL** 的执行边界；终端用户 **不在前端手写 SQL**。  
- **Super**：业务上「权限较大的管理用户」，**目标态**仅在 **管理台** 创建/轮换凭证，**不作为**长期依赖的 env 明文超管（见 **§1.4** 第 4 点）。  
- **Admin**：合并原 **临时管理员** 与 **admin** 语义，**当前版本同一权限档**（见 **§1.2**）。  
- **L2**：改的是 **肖像 / 长久习惯**（见 **§1.3.1**），**不是**改他人核心业务用户信息；越权 → **「您无此权限」** 或等价结构化错误码。

### 1.2 档位、产品与库内 `access_level`

| `access_level` | 产品名 | 建议 slug | 表结构（DDL） | 数据 DML（摘要） |
|----------------|--------|-----------|---------------|-------------------|
| **0** | **Super** | `super` | **不得** DDL（结构变更仅 migration / 运维） | **物理** `DELETE` / `TRUNCATE` 是否开放由 **policy** 定（默认可高于 Admin）；**INSERT/UPDATE/SELECT** 受表白名单 + 等级 + 行数等约束。**目标态**：凭证 **仅管理台** 签发，**废弃**以 env 充当长期「超管真值」（过渡期须在 `PROJECT_CONFIG` 标 **deprecated** 与移除计划）。 |
| **1** | **Admin** | `admin` | **不得** DDL | **SELECT / INSERT / UPDATE**；**禁止物理 `DELETE` 与 `TRUNCATE`**。**允许软删除**：`UPDATE` 删除标志位 / `deleted_at` 等 **不视为**本条禁令（见 **§1.4-1**）。 |
| **2** | **终端用户（L2）** | `end_user` | **不得** DDL | **禁止 `INSERT`**。**禁止跨表**：单条 SQL **不得**含 `JOIN`（多表一律拒绝，由 **后闸** AST enforce）。**写**仅限 **`chatbi_user_portrait`**（§1.3.1）中对 **非 `user_id`** 列的 **`UPDATE`**；首期可改 **`long_term_prompt`**；后续列须经 **可改列白名单** 登记。**读**：仅与 `subject_user_id` 绑定的自身行。 |

> **措辞**：「不能改表结构」均指 **DDL**；**DML** 边界以本表 + policy 为准。

### 1.3 每表权限（`chatbi_sql_table_policy`）

- 每张参与 Text2SQL 的表具备元数据（表或 YAML），至少：`min_select_level`、`min_insert_level`、`min_update_level`、`min_delete_level`（**NULL = 该操作类型对全体关闭**）。  
- **数值语义**：`access_level` **越小权限越高**。某操作允许当且仅当 **`access_level <= min_*_level`**（非 NULL 时），与 `chatbi_02_*.sql` 头注释一致。  
- **L2 默认写表**：以 **`chatbi_user_portrait`** 为主；其它表的 `min_insert` 等对 L2 应配合 **NULL 关闭** 或等价策略，避免绕开肖像表。

### 1.3.1 用户肖像表（新增）

- **推荐表名**：`public.chatbi_user_portrait`（DDL：`docs/text2sql/v1/sql/chatbi_04_user_portrait.sql`）。  
- **用途**：存放 **习惯、长久 Prompt、肖像化偏好** 等，**与**「用户通讯录类核心业务宽表」**分离**；L2 的「保存自己习惯」**落在此表**，降低误改 PII 宽表面。  
- **首期列**：`user_id`（PK，**L2 禁止 UPDATE**）、`long_term_prompt`（`text`）、`updated_at`。  
- **演进**：新增可改列须同步 **可改列白名单**（实现可与 policy JSON 或旁路元数据表绑定）。

### 1.4 已拍板项（2026-05-12）

1. **软删除**：**不禁止**；`UPDATE` 软删字段 **不算** Admin 档对 **物理删** 的禁令；**仍禁止** Admin 执行 **`DELETE` / `TRUNCATE`**。  
2. **L2 不夸表**：禁止 **`JOIN`** / 多表语句；**肖像与习惯**走 **`chatbi_user_portrait`**，**不**把「改他人用户信息」纳入 L2 能力。  
3. **L2 不允许 `INSERT`**；写路径为肖像表 **`UPDATE` 且不得改 `user_id`**；首期列 **`long_term_prompt`**，后续列按白名单扩展。  
4. **Super 非 env 长期真值**：Super 为 **高权限管理用户**，**实际签发/轮换在管理台**；**Admin** = 原 **temp_admin** 与 **admin** 合并命名，**暂不拆分**（若未来拆分另升 SPEC 版本）。  
5. **表白名单与等级**：**前闸 + 后闸都启用**（区别见 **§1.5**）；等级与 L2 单表规则主要在 **后闸** 与执行引擎落实。  
6. **日志**：须 **写入结构化日志**（字段草案见 **§1.6**）。

### 1.5 表白名单：「前闸」与「后闸」区别（均已启用）

| 闸口 | 典型落点 | 回答的问题 | 单独依赖是否足够 |
|------|----------|------------|------------------|
| **前闸（生成前）** | Prompt 上下文裁剪、schema 字典仅暴露允许表、Router 拒答 | 模型在 **规划/生成前** 不应看到哪些表与列？ | **不足**：模型仍可能输出越权 SQL。 |
| **后闸（生成后 / 执行前）** | SQL **AST**、表白名单、**档位策略**（含 L2 禁 JOIN/禁 INSERT）、参数化执行 | 这条 **具体 SQL** 能否 **真正访问数据库**？ | **不足**：无前闸则暴露面与 Prompt 泄漏过大。 |
| **结论** | **两道都校验**：前闸 **缩面 + 降幻觉**；后闸 **硬保证**；与 `SPEC-ChatBI-V3-Security.md` **对表迭代**。 |

### 1.6 结构化日志（写入）

在 **`CHATBI_JSON_LOG`**（或等价开关）开启时，至少记录（**无** Bearer 明文、**无**口令；SQL 全文 **脱敏或仅摘要/hash**）：

| 事件 | 建议字段 |
|------|----------|
| 鉴权成功 | `event=auth_ok`，`principal_kind`（`super`/`admin`/`end_user`），`token_id`，`request_id` / `run_id` |
| 鉴权失败 | `event=auth_fail`，`reason`（`missing_bearer` / `bad_hash` / `expired` / `revoked`） |
| SQL 闸门拒绝 | `event=sql_gate_deny`，`deny_code`，`access_level`，`target_table`，`stmt_class`，`rule`（如 `l2_join_forbidden`、`l2_insert_forbidden`、`l2_pk_update_forbidden`、`below_min_level`） |
| SQL 闸门放行（可选采样） | `event=sql_gate_allow`，`target_table`，`stmt_class` |

与 **`SPEC-ChatBI-V3-Logging-Trace.md`**、`run_id` 口径对表；细节以实现 PR 为准。

### 1.7 复杂度说明（共识）

仍为 **横切**：鉴权 → `access_level` → policy → **前/后双闸** → 执行 → 日志；任务单与 **`_tech_graph`** 须同步更新。

---

## 二、命名与映射（企业命名是否可直接采用）

### 2.1 当前结论（草案）

- **可以采用企业侧习惯命名**，但运行时 **必须以 slug 为真值**，建议三档与 **`access_level` 映射**如下（与 **§1.2** 一致）：

| 企业显示名（示例） | 建议 slug | `access_level` | 与主规 `user_kind`（历史） |
|-------------------|-----------|----------------|---------------------------|
| 超管 / Owner | `super` | 0 | 对齐 `super_admin` 语义；**目标**改管理台签发，弱化 env |
| 管理员（含原临时管理员） | `admin` | 1 | 合并 `temp_admin` 与「企业 admin」**暂不拆分** |
| 终端用户 | `end_user` | 2 | 非管理；肖像表写路径见 **§1.3.1** |

- 映射表维护位置：`PROJECT_CONFIG` 或本仓库 Markdown **二选一**；**禁止**仅用中文角色名写 `if` 分支。

### 2.2 仍开放

- 企业「分析师」等是否 **再映射**到 `end_user` 或未来 **L3**（只读扩展）—— **V3.1** 再定；**V3 首包** 以上表足够。

---

## 三、注册用户与个人项目会话策略（当前拍板）

### 3.1 当前结论

1. **不做「自主注册用户」流程**（个人项目；无公开注册）。
2. **仅服务已有权限的主体**：由运维/本人 **手动下发临时 token**（与主规 `temp_admin_keys` / 管理页生成 **语义一致**，具体存储以实现为准）。
3. **认证管道**：采用主规 **§3.9 A 管道**（TLS + 一次性 `exchange` + 登录）。
4. 登录成功后的凭据：前端经 **`input`** 录入材料后，**保存 `Bearer` API key**（或等价 **长期 API key**）供后续请求携带 —— **与主规 §3.9.6「优先 httpOnly cookie」表述并存时，以本文档为个人项目拍板**；实现须在 PR 中写明 **XSS 与存储面**（若用 `localStorage` 存 Bearer，须列为 **已知风险** 或配套短 TTL + 轮换策略）。

### 3.2 待补全

- 「Bearer API key」与主规 **`temp_admin_keys` 表内哈希校验** 是否为 **同一枚 token**（推荐 **是**，避免两套并行秘密）。  
- 管道 A 的 **`/auth/login`** 主体是 **仅 Admin** 还是 **未来可扩展到 Super 专用口令**（当前：**仅服务有权限用户** → 范围可收窄为 **表内 key + exchange**）。

### 3.3 与主规差异（显式）


| 主题    | 主规倾向                                 | 本文档拍板                           |
| ----- | ------------------------------------ | ------------------------------- |
| 登录后凭据 | **优先** httpOnly **会话 cookie** 或短 JWT | 个人项目：**客户端持久化 Bearer API key**  |
| 注册用户  | 首期可运维手工插入 `auth.users` 等             | **首期不做注册用户维度**；仅手动 token + 管道 A |


**后续动作**：主规 **§3.0 / §3.2 / §5.1** 若采纳本文，应 **单开修订** 标注「个人项目简化版以 OpenItems 为准」。

---

## 四、其余议题（占位 · 与前期「待明确」清单对齐）

以下仍按主规 `[SPEC-ChatBI-V3-Identity-Access.md](SPEC-ChatBI-V3-Identity-Access.md)` **§3.10、§5.4** 进任务单，**不在本文展开**：

- `login_exchange` 表结构、BFF 转发、middleware、CSRF / SameSite、限流数值。  
- **`super_admin_api_keys` 是否首期建设**（与 env 超管过渡期并存策略）。  
- **JWT 与表内 key 吊销联动**、旧 JWT 最长存活窗口。  
- **RLS vs 纯应用层** 与 **第一节** 等级模型如何叠加（避免双重矛盾）。  
- **`CHATBI_JSON_LOG`**：字段级口径见 **§1.6**；与 `SPEC-ChatBI-V3-Logging-Trace.md` 对表细节在实现 PR 收敛。

---

## 五、实施阶段与任务流（执行顺序）

### 5.0 最终目的（对齐本文 §一）

用户在 Chat 中仅能在 **有效等级** 与 **表级策略** 允许范围内执行（经 Text2SQL 产出的）SQL；同一 **`effective_level`**（及可选 **`subject_user_id`**）作为未来 **RAG / 向量库** 的 **namespace 或 metadata 过滤** 对接面，避免另起一套权限模型。

### 5.0.1 对你三条「细节确认」的直接回答

| # | 问题 | 结论 |
|---|------|------|
| **1** | 第一步是否要先确认需要多少表？ | **是。** 先产出 **逻辑表清单 + 每表一句职责**（见 **§5.1**），再写 migration。业务实体表若尚未存在，须在 Text2SQL **表白名单** 中 **暂缓暴露** 或先建 **最小演示表**，否则闸门无的放矢。 |
| **2** | 分级优先、登录先极简 | **同意。** 首期登录 = **`Authorization: Bearer` + DB 存 `key_hash` 的常量时间比对**；token 行携带 **`access_level`（0=Super / 1=Admin / 2=终端用户）**；**L2 须** `subject_user_id`（与 `chatbi_user_portrait.user_id` 对齐）。**「对称」**指共享秘密型 API key + `hmac.compare_digest`。**管道 A** 可后置 **P5**；**P1～P4 可不建 `login_exchange`**。 |
| **3** | 在最高优先级 SPEC 下任务怎么排 | 以 **§5.2 分阶段** 为执行序；**先落地能阻断越权的最小表（P1）+ Bearer 鉴权（P2），立刻接 Text2SQL 闸门（P3）**。 |

### 5.1 最小逻辑表清单（草 · 表名实现可改）

> **说明**：下列为 **最少原则**；可与主规 **`temp_admin_keys` 并为一张**（增加 `level` / `subject_user_id`），避免两套 Bearer 校验链。

| 序号 | 对象 | 职责（一句话） |
|------|------|----------------|
| **T1** | `chatbi_access_tokens` | 手工插入：**`key_hash`**、**`access_level`（0/1/2）**、**L2 必填 `subject_user_id`**、可选 `expires_at` / `revoked_at` / `label`；**禁止存明文 token** |
| **T2** | `chatbi_sql_table_policy` 或 YAML | 各表 **min_select / min_insert / min_update / min_delete**；**肖像表**对 L2 的 `min_insert` 应为 **NULL** |
| **T3** | `chatbi_user_portrait` | **L2 写路径主表**（习惯 / 长久 Prompt）；DDL：`chatbi_04_user_portrait.sql` |
| **T4**（可选） | 审计表 | 若不用 **`CHATBI_JSON_LOG`** 覆盖闸门事件，可再建表；**优先**走 §1.6 日志 |
| **—** | 业务数据表 | 不计入权限子系统张数；Admin/Super 操作业务表须 **表白名单 + policy** |

**首期若不启用 `auth.users`**：`subject_user_id` 为 **逻辑用户主键** 字符串，与 **`chatbi_user_portrait.user_id`** 一致。

### 5.2 分阶段任务流（建议按序串行）

| 阶段 | 名称 | 产出物 | 备注 |
|------|------|--------|------|
| **P0** | 口径冻结 | **§1.4 已拍板** 写入代码/YAML 注释；序列图须含 **前闸 + 后闸**（§1.5） | 与 **§1.6** 日志字段草案一致 |
| **P1** | Schema / migration | **T1～T3** SQL 已备：`chatbi_01`～`chatbi_04` | 执行顺序见任务单 |
| **P2** | Bearer 鉴权 | 注入 **`ChatBiPrincipal`**：`principal_kind`（`super`/`admin`/`end_user`）+ `access_level` + `subject_user_id?` + `token_id` | 与 §1.2 slug 对齐 |
| **P3** | Text2SQL 分级闸门 | **后闸**：AST + 表白名单 + **L2 禁 JOIN / 禁 INSERT / 肖像表列白名单**；**前闸**：schema 裁剪 | Admin **禁物理删**、**允许软删**；**双闸都开** |
| **P4** | RAG 对接面 | 检索入口增加 **只读** `effective_level`（及可选 scope）参数，默认 **no-op** | 仅占位与类型签名，权限真值仍来自 **P2** |
| **P5** | 登录加固 | 主规 **管道 A**、`login_exchange`、吊销 UI、限流、`CHATBI_JSON_LOG` 字段对齐 | 不阻塞 P1～P4 |

**依赖**：P3 依赖 P1、P2；P4 依赖 P2；P5 可与 P1～P4 **并行** 但 **不得**反向阻塞 P3。

### 5.3 实施任务单与图谱落盘（建议）

- 在 `ai-ink-brain-api-python/docs/tasks/` 新建任务单（例：[`docs/tasks/active/task_chatbi_level_gate_v1.md`](../../tasks/active/task_chatbi_level_gate_v1.md)）：验收 `- [ ]` **按 P0～P4 拆分**。  
- `docs/text2sql/v1/sql/chatbi_01_*.sql`～`chatbi_04_*.sql`：Supabase **可复制执行**（见任务单 **§Supabase SQL 执行顺序**）。  
- `_tech_graph/` 增量：**鉴权依赖 → Text2SQL 闸门** 子流程（与主仓图谱规范一致即可）。

---

## 六、关联

- [`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md)  
- [`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md)  
- [`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md)（SQL AST / 表白名单）  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

---

## 七、修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-12 | 初版：收录 **一** 数据域 + L0–L2 Text2SQL 草案及待补全；**二** 企业命名映射；**三** 个人项目不做注册、管道 A + Bearer 拍板及与主规差异表；**四** 占位 |
| 2026-05-12 | **§五.3**：落实任务单 [`docs/tasks/active/task_chatbi_level_gate_v1.md`](../../tasks/active/task_chatbi_level_gate_v1.md) 与 `docs/text2sql/v1/sql/chatbi_0*.sql` |
| 2026-05-12 | **§一** 大补：Super/Admin/L2、`chatbi_user_portrait`、软删、L2 禁 JOIN/INSERT、双闸 **§1.5**、日志 **§1.6**；**§二** slug 映射；**§五** T1～T3 与 P0～P3 措辞；**chatbi_04** DDL |
