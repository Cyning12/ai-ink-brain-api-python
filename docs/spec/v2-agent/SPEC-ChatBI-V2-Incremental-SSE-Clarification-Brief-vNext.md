# ChatBI V2 增量 SSE / Timeline（vNext）— 不明确点澄清简报（吸收索引）

> **状态**：**已吸收**（2026-05-08 二稿）。本文件为 **回溯索引**：原「未锁定」项均已落盘到主 SPEC / Events / 任务单 / manifest 注释；**实现真值**以 **`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md`** + **`SPEC-ChatBI-V2-Events.md` §8** + **`docs/_tech_graph/_contract_manifest.json`**（与代码 **同 PR** 更新枚举）为准。  
> **日期**：2026-05-08  
> **依赖**：`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md`、`SPEC-ChatBI-V2-Events.md`、`docs/tasks/active/task_chatbi_v2_incremental_sse_backend_v1.md`、`ai-ink-brain/content/tasks/task_chatbi_v2_incremental_sse_timeline_frontend_v1.md`、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`  
> **用途**：给审阅者 **10 分钟内** 对照「原七类问题 + §8 补充」与 **主文档节号**；**实现前优先读主 SPEC §0**，本简报 **仅作索引**。剩余主要是 **§8.8 DB 关联**（非阻断）、**manifest 与代码同 PR**、以及任务单 **实现备忘** 中的落地填空。

---

## 0. 执行顺序（与主 SPEC 对齐）

与 **`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` §0** 一致：**契约（§5 + Events §8）→ 验收（§7）→ 降级矩阵（§9）→ 任务单填空**；manifest **禁止**先于 `unified_chat.py` 空转（见 manifest `_note`）。

---

## 1. 原 §1 契约二选一 → 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| `token` vs `chain` 唯一真值 | Timeline **§5.1**；Events **§8.1** | **仅 `chain` + `agent.llm.*`** 承载子步 LLM 增量；Unified 增量路径 **禁止** 顶层 `event: token` 传子步。 |
| Legacy `token` 硬区分 | Events **§8.1** 表 | **HTTP 路径** + **`X-ChatBI-Sse-Contract: 2`**；不靠 `scope` 推断 Legacy。 |
| manifest 与 TS | Timeline §5 脚注；manifest **`_note`** | 枚举 **`type_values`** 与代码 **同一 PR**；当前仅 `_note` 预告 `agent.llm.*`。 |

---

## 2. 原 §2 payload 形状 → 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| 嵌套 vs 兄弟 `chain` | Timeline **§5.1** | **`agent.llm.delta` 多条兄弟 `chain`**，深度 **1**，与 `ChainEventCard` 一一对应。 |
| `think` vs delta | Timeline **§5.1**、**§5.3**；Events **§8.6** | **`agent.think` 仅在 `agent.llm.end` 后**；仅摘要；全文真相源见 **Timeline §8.4**。 |
| 最小样例 + 坏例 | Timeline **§5.4**；Events **§8.5** | 好例 JSON 行序列 + 缺 `text` 策略 B。 |

---

## 3. 原 §3 Feature flag / 持久化 → 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| query / localStorage / 默认 | Timeline **§6**；前端任务单 | **`?single_panel=1`**；**`localStorage`** 键 **`ink-brain.chatbi.unified.singlePanel`**；**默认双栏**；**无 `NEXT_PUBLIC_*`** 布局开关。 |
| ~~`stream_panel`~~ | — | **废止**该命名；以 **`single_panel`** 为准。 |
| 后端是否感知布局 | Timeline **§9.3**；前端任务单 | **布局纯前端**；后端感知的是 **`X-ChatBI-Sse-Contract`** 与 **`CHATBI_SSE_INCREMENTAL`**（流式时序），非单双栏。 |

---

## 4. 原 §4 时间 / 「有意义」→ 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| CI 不测 wall-clock 1s | Timeline **§7.1–7.2** | mock / 顺序 / tick；**≤1s** 仅 **staging 手测**。 |
| 白名单 | Timeline **§7.3**；Events **§8.3** | `router.decision` 等；注释行 / 坏 JSON **不算**。 |
| keepalive | Timeline **§7.4** | **`: ...` 注释行** 不计入 data 帧。 |

---

## 5. 原 §5 可选能力细节 → 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| `step_id` 聚合 | Timeline **§6**；前端任务单 | **v1 不做** 聚合卡片。 |
| 坏帧计数对用户可见 | Timeline **§5.4** | **默认不可见**；`console.debug`；`meta.debug` **可选**。 |
| 方案 B + 移动 | Timeline **§2.2 / §3.2**；前端任务单 | **本版不验收移动端**；将来产品可单栏+抽屉（任务单备注，非交付）。 |

---

## 6. 原 §6 联调节奏 → 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| 前置任务未勾完能否开工 | 前后端任务单 **「开工门槛」** | **最小子集**可并行；合并前须可联调。 |
| mock vs 真实 LLM | Timeline **§7.5**；前后端任务单 | **CI = mock/stub**；**真实 LLM = release checklist**（唯一口径）。 |

---

## 7. 原 §7 降级与旧客户端 → 已锁定

| 原问题 | 落盘位置 | 结论 |
|--------|----------|------|
| 旧客户端识别 | Timeline **§9.2** | 缺 **`X-ChatBI-Sse-Contract: 2`** 或 **`0`/`1`** → **批量 replay**。 |
| env 矩阵 | Timeline **§9**；`PROJECT_CONFIG` **`CHATBI_SSE_INCREMENTAL`** | `USE_AGENT` × `SSE_INCREMENTAL` × 协商头；见主表。 |

---

## 8. 原补充 §8.1–8.7 → 已锁定

| 子项 | 落盘位置 |
|------|----------|
| 8.1 run_id / step_id / 重连 | Timeline **§8.1** |
| 8.2 并发与到达序 | Timeline **§8.2** |
| 8.3 中途失败与 `done` | Timeline **§8.3** |
| 8.4 真相源 | Timeline **§8.4** |
| 8.5 背压字段名 | Timeline **§4.3**、**§5.2**（`agent.llm.truncated`） |
| 8.6 日志与隐私 | Timeline **§8.6** |
| 8.7 版本协商 | Timeline **§8.7**；与 **`X-ChatBI-Sse-Contract: 2`** 绑定 |

### 8.8 仍属「实现 PR 填空」、非契约阻断（简报 + 任务备忘）

- **`conversation_id` / `message_id` 与 `step_id` 的 DB 关系**：SSE 语义已在主 SPEC **§8.1** 规定；若 ingest / 表结构要强绑定，由 **实现 PR** 对照 **`PROJECT_CONFIG`** 与 SQL **另补一行**，**不阻塞**当前门禁。  
- **`_contract_manifest.json` 的 `type_values`**：简报 §9 与任务单已写明 **与代码同一 PR** 落地；当前 manifest **可能仍只有 `_note` 预告** — 正常，直至实现合并。  
- **任务单「实现备忘」**：前端/后端 **`______`**（修改文件列表、单栏 UI 入口、`assistant.message` 失败时选 **空 / 部分 / 错误全文** 等）属 **落地选型**，**不是** SPEC 缺口。

---

## 9. 文件清单（吸收状态）

| 文件 | 状态 |
|------|------|
| `SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` | **已终稿**：§0–§9、§5.4 JSON、§7 可测化、§8.1–8.7 |
| `SPEC-ChatBI-V2-Events.md` | **已终稿**：**§8** vNext；§2.2 增补 `agent.llm.*`；§6 规则同 PR |
| `docs/_tech_graph/_contract_manifest.json` | **`_note` 已更新**；`type_values` **待实现 PR** |
| `docs/tasks/active/task_chatbi_v2_incremental_sse_backend_v1.md` | **契约与流程已填**（G2、§9 矩阵、mock/LLM、门槛）；**实现备忘** 仍为落地 PR 填空（见该节说明） |
| `ai-ink-brain/content/tasks/task_chatbi_v2_incremental_sse_timeline_frontend_v1.md` | **同上**（协商头、query/LS、聚合 v1 不做）；**实现备忘** 为落地 PR 填空 |
| `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | **已增** `CHATBI_SSE_INCREMENTAL` |

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-08（末） | §8.8 改为「实现 PR 填空 / 非阻断」三句定稿；§9 任务行区分 **契约已填** vs **实现备忘**；用途段补 **结论口径**；主 SPEC 文首已与「终稿」对齐 |
| 2026-05-08（晚） | **二稿**：全文改为「吸收索引」；各节映射主 SPEC / Events 节号；废止 `stream_panel`；增 **§8.8**；文件清单改状态列 |
| 2026-05-08 | 初稿：合并前端 Agent 七类问题 + §8 补充项 + 文件清单 |
