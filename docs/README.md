# docs/（ai-ink-brain-api-python）文档导航

> 本 README 是 `docs/` 的入口与分类说明。  
> **`docs/tasks/` v1 目录规整**已落地（见 [`docs/tasks/done/task_docs_tasks_reorg_move_v1.md`](tasks/done/task_docs_tasks_reorg_move_v1.md)）；状态视图入口 [`docs/tasks/_views/`](tasks/_views/)。  
> `docs/_tech_graph/` 为本仓技术图谱单一事实来源，不参与 tasks 规整，但在导航中引用。

---

## 1. 你应该从哪里开始读

- **如果你要改代码/环境变量/接口边界**：先读 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
- **如果你要做任务实现/验收**：从 [`docs/tasks/_views/`](tasks/_views/) 按状态进入，或直接在 `docs/tasks/active/`、`docs/tasks/done/` 找 `task_*.md`（每个 Task 需要写明 `状态`）
- **如果你要理解“端到端怎么跑”**：读 `docs/flows/` 的版本化流程快照
- **如果你要做 UI 协议对齐（SSE、events、timeline）**：读 `docs/UI/`
- **如果你要做 Text2SQL**：读 `docs/text2sql/`
- **如果你要做可复现交付（SDD/TDD/Harness）**：读 [`docs/harness/README.md`](harness/README.md) → [`docs/harness/ACCEPTANCE_LANDING.md`](harness/ACCEPTANCE_LANDING.md)（含 **50 三方复检** 落盘 `docs/tasks/reinspect_results/`），辅以 `docs/delivery/`
- **如果你要查跨 task 蒸馏知识（Coding Wiki / L2）**：读 [`docs/coding_wiki/index.md`](coding_wiki/index.md) → [`docs/coding_wiki/CODING_WIKI.md`](coding_wiki/CODING_WIKI.md)
- **如果你要写总结**：读 `docs/diary/DIARY_GUIDE.md` 并按规范产出

---

## 2. docs/ 的“类型”划分（现状 → 规整目标）

> 原则：按“文档用途/读者/生命周期”分类型，而不是按时间或作者随意堆叠。

### 2.1 `meta/`（真值表 / 项目配置 / 边界）

- **定位**：本仓权威配置与边界说明（环境变量、入口文件、对外契约摘要、敏感信息规范）。
- **现有入口**：
  - `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
- **规整目标**：
  - `meta/` 下仅保留“稳定、不频繁改”的真值表类文档
  - 命名建议：`PROJECT_CONFIG_*.md`、`CONTRACT_*.md`、`SECURITY_*.md`

### 2.2 `tasks/`（任务规格 / 验收标准 / 实现回填）

- **定位**：实现与验收的主入口。要求：每个任务必须可落地、可验证、可回填。
- **入口与结构（v1 已落地）**：
  - 视图索引：`docs/tasks/_views/`（按状态聚合）
  - 进行中/待开始/设计中：`docs/tasks/active/`
  - 已完成：`docs/tasks/done/`
  - 规格：`docs/tasks/specs/`（`SPEC-*.md`）
  - 模板：`docs/tasks/templates/`（`TASK_TEMPLATE.md`）
  - 遗留：`docs/tasks/legacy/`（历史命名/缺少 `状态`）
- **规整目标（核心）**：以 `_views` 为入口，逐步消化 `legacy/`，并让新增任务始终落在 `active/` 且具备 `状态` 字段。

**Task 状态（建议扩展集合，向后兼容模板）**

- **设计中**：`design`（等价：`draft`）
- **待开始**：`pending`（等价：`todo`）
- **进行中**：`in_progress`
- **已完成**：`done`
- **已归档**：`archived`（完成后较久、仅供回溯）
- **已取消**：`cancelled`（明确不做/被替代）

**Task 文件头（建议统一字段）**

- `状态`：必须（从上面集合中选一个；允许历史值 `draft/pending/in_progress/done`）
- `范围`：必须（例如“仅后端本仓”）
- `关联图谱`：可选但推荐（指向 `docs/_tech_graph/*`）
- `关联 Issue/PR`：可选
- `前端依赖`：可选（跨仓协作时必须）

**命名规则（建议）**

- 统一采用：`task_<domain>_<topic>_vN.md`
  - 例：`task_unified_chat_backend_v1.md`
- 兼容历史命名：保留不动，但后续新增任务全部按新规范。

**状态视图（本次不建目录，仅定义未来落盘方式）**

> v1 已落地（本次对话已创建文件）

- `docs/tasks/_views/in_progress.md`：进行中任务索引
- `docs/tasks/_views/done.md`：已完成任务索引
- `docs/tasks/_views/design.md`：设计中/草稿任务索引 + 缺少状态字段清单

### 2.3 `diary/`（非长期 / 易过时产物 · **非必读**）

- **定位**：存放 **非长期维护**、**易过时** 的沉淀（验收留证、排障快照、实验报告、阶段性对比等）；**不是**实现与架构真值源。
- **Agent 读取**：**默认不读** `docs/diary/` 全树；仅 task / 用户显式路径需要时打开最小文件集（见 `.cursor/rules/08-docs-diary.mdc`、`AGENTS.md` **非必读**）。
- **实验轨**：`docs/diary/jsonPKmermaid/`（图谱行为实验 / 闸口 fixtures & reports）— **非必读**，非实验复现勿遍历。
- **写作规范**：见 `docs/diary/DIARY_GUIDE.md`（含 `YYYY-MM-DD.md` 后端总结格式）。
- **规整目标（后续）**：长期结论须提炼进 `_tech_graph/`、`tasks/done/`、`docs/spec/` 等；diary 仅留回溯。

### 2.4 `UI/`（前后端协议/交互方案）

- **定位**：用于对齐接口协议（例如 SSE、events 模型）与前端渲染形态（timeline）。
- **现有入口**：`docs/UI/v1/*`
- **规整目标**：
  - 保持版本化：`UI/v{N}/UI-XX-*.md`
  - 与 `tasks/` 相互引用：UI 文档负责“方案与协议”，Task 负责“落地验收”

### 2.5 `flows/`（端到端流程快照 / 可回溯）

- **定位**：把“真实调用链路”版本化固化，适合复盘与对比演进。
- **现有入口**：`docs/flows/rag-chat/*`
- **规整目标**：
  - 保持版本化命名（已在文档内建议）：`v{N}_YYYY-MM-DD_<topic>.md`

### 2.6 `text2sql/`（Text2SQL 方案、任务、样例、SQL）

- **定位**：Text2SQL 的规格、执行清单、样例、初始化 SQL。
- **现有入口**：`docs/text2sql/v1/`
- **规整目标**：
  - 保持 `v1/` 版本边界
  - `spec/` / `task/` / `sql/` 三类职责清晰（现状基本符合）

### 2.7 `delivery/`（交付框架 / 版本化交付包）

- **定位**：SDD + TDD + Harness 的可复现交付流程。
- **现有入口**：`docs/delivery/README.md`、`docs/delivery/v0.2.0-code-rag/*`
- **规整目标**：
  - 保持 SemVer 版本目录
  - Harness 内脚本保持可执行与可复现（与任务/流程互链）

---

## 3. docs 规整进度（摘要）

- **已完成（2026-05-22）**：`docs/tasks/` v1 目录结构、`_views/` 状态索引、SPEC/模板分目录（见 [`task_docs_tasks_reorg_move_v1.md`](tasks/done/task_docs_tasks_reorg_move_v1.md)）。
- **仍不参与**：`docs/_tech_graph/` 内容搬迁。

---

## 4. 下一步整理任务清单（后续单独 task 执行）

> 执行时建议遵循“最小扰动”：先做“索引/视图”，再做“移动/重命名”，最后做“内容纠偏”。

- [ ] **盘点 `docs/diary/` 非日期命名文件**：确认是“主题总结/知识库/个人资料”，决定落入新类型（建议新建 `docs/notes/` 或 `docs/kb/`）
- [ ] **统一 `docs/tasks/` 历史任务头部 `状态`**：将 `legacy/` 与个别 `done/` 漏网项规范化到统一集合（不改变语义）
- [x] **建立 Tasks 状态视图**：
  - [x] `docs/tasks/_views/design.md`
  - [x] `docs/tasks/_views/in_progress.md`
  - [x] `docs/tasks/_views/done.md`
- [ ] **为 `UI/`、`flows/`、`delivery/` 建索引页**（同样只新增入口文件，不移动原文档）
- [ ] **补齐跨仓引用规则**：Task/Flow/UI 文档中引用前端仓文件时，统一写相对仓库路径并避免本地绝对路径

