# PROMPT · P2 改稿 + 脚手架（Claude Code Lead · pre-T2c）

> **用途**：整文件 `@` 给 Claude Code Lead；**§1–§4 全部必做**，不得只做部分就停。  
> **输入审核真值**：[`reviews/by-task/gov-docs-noise-p2/task_gov_docs_noise_p2_readorder_v1_audit_R1_20260606.md`](../reviews/by-task/gov-docs-noise-p2/task_gov_docs_noise_p2_readorder_v1_audit_R1_20260606.md)  
> **task**：[`docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md`](../../tasks/active/task_gov_docs_noise_p2_readorder_v1.md)  
> **git_branch**：`task/gov-docs-noise-p2-v1`  
> **slug**：`gov-docs-noise-p2`  
> **性质**：**改 task 草案 + 建 PROMPT/MANIFEST** — **非 T2c 执行**（不改 PROJECT_CONFIG/AGENTS 业务交付）

---

## §0 · 开跑前

    git checkout main && git pull
    git checkout task/gov-docs-noise-p2-v1 || git checkout -b task/gov-docs-noise-p2-v1

| 纪律 | 说明 |
| --- | --- |
| **禁止** | 代签 `human_gate` · 执行 P2-1～P2-4 实现 · 改 api/tests/workflows |
| **禁止** | git log / blame 考古（改稿只读 task 列路径 + SPEC §8.3） |
| **必须** | 每步 commit（`HANDOFF_AUTO_COMMIT.md`）· 落盘 invoke |
| **invoke** | `docs/harness/invokes/by-task/gov-docs-noise-p2/invoke_YYYYMMDD_pre_exec_amendments.md` |

---

## §1 · 改 task 正文（`task_gov_docs_noise_p2_readorder_v1.md`）

### §1.1 背景 bullets（替换 L45–47）

**原（删）**：

    - C5/C6：`AGENTS.md` 与 `docs/README.md` 读序表述不一致；根 `README.md` Unified Chat 端点缺失

**新（写）**：

    - **C4**：`PROJECT_CONFIG` 仍提 `.cursorrules`（已不存在）→ P2-1
    - **C5**：根 `README.md` Unified Chat 端点 / 关键 env 不完整 → P2-3
    - **C2 复核**（P0 已修 flows 降级）：P2-2 补 AGENTS ↔ `docs/README` **互链**与 **canonical 读序子集**对齐（不要求 docs/README 全节逐步一致）
    - **C6**（`HARNESS_V2_PLAN` vs `AGENTS` 权威链）：**本批非范围**，留 P3 或单独小修
    - `docs/tasks/legacy/` 6 份缺状态 / 未入 `_views/` → P2-4

（L45 C4 行若与上重复，合并为一段，避免 C4 写两次。）

### §1.2 完成态第二 bullet（替换 L52）

**新**：

    - `AGENTS.md` 与 `docs/README.md` §1 **canonical 子集**一致、**双向互链**；docs/README 保留 UI/text2sql/diary 等扩展导航条

### §1.3 P2-2 内容要求（替换 L74–81 整段）

**新**：

### P2-2 内容要求（SPEC §8.3 · 子集对齐）

**角色区分**：

- `AGENTS.md` = Agent **最小读序地图**（7 步，含 `.mdc` / harness / Wiki / 跨仓）
- `docs/README.md` §1 = **docs 分类导航**（可含扩展条目）；**不要求**与 AGENTS 逐步完全一致

**Canonical 子集**（须与 SPEC §7 / 导图 §5 一致，且在两文件 **§1 前 5 条**对齐）：

1. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
2. `docs/_tech_graph/`（`graph_query` 按需）
3. `docs/tasks/RECENT_TASK_SCHEDULE.md` → `active/task_*.md`（docs/README 可写 `_views/` 入口，语义等价）
4. 涉 ChatBI → `docs/spec/v3-agent/`（docs/README 扩展条可保留）
5. 关账回顾 → `docs/coding_wiki/`（AGENTS 写 `index.md` / syntheses 指针）

**AGENTS.md 必做**：

- 保持现有 7 步地图；在「必读」节末或「非必读」节前增加显式互链：`docs/README.md` §1
- 可选：增加一行 pointer 至 SPEC §7 canonical（导图或正文）

**docs/README.md §1 必做**：

- **前 3–5 条**按上表 canonical 子集重写/排序（PROJECT_CONFIG → `_tech_graph` → tasks 入口）
- `docs/flows/` 保持 **Legacy · 非 L0**（P0 已降级，勿改回「当前入口」）
- 在 §1 末或文首增加显式互链：`AGENTS.md`
- **保留** UI / text2sql / diary / PR spec 等扩展条（不删）

### §1.4 验收标准 P2-2（替换原两条 `- [ ] P2-2`）

**新**：

    - [ ] P2-2：`AGENTS.md` 与 `docs/README.md` §1 **canonical 子集**（前 3–5 条）与 SPEC §7 一致
    - [ ] P2-2：`AGENTS.md` ↔ `docs/README.md` **双向互链**存在；docs/README 扩展导航条保留

### §1.5 Delta ADDED 第一条（替换 L128–129）

**新**：

    - **Requirement**：`AGENTS.md` 与 `docs/README.md` 须 **双向互链**，且 **canonical 读序子集**一致
      - **Scenario**：`sc-p2-agents-docs-readme-link` — GIVEN Agent 打开 AGENTS.md WHEN 读「必读」节 THEN 看到指向 docs/README §1 的互链；打开 docs/README §1 THEN 看到指向 AGENTS.md 的互链；且两文件前 5 条与 SPEC §7 子集一致

### §1.6 非范围（在 L117 后追加）

    - **不** 在本批解决 **C6**（`HARNESS_V2_PLAN.md` vs `AGENTS.md` 权威链互链 — 留 P3 或单独 task）
    - **不** 要求 `docs/README.md` §1 与 `AGENTS.md` **逐步完全一致**（扩展导航条保留）

### §1.7 P2-1 范围补充（在 P2-1 内容要求末追加一条）

    - 同步更新 `PROJECT_CONFIG` **§A L17**（若仍写 `.cursorrules` 为兼容/历史参考，改为「已移除；真值 `.cursor/rules/*.mdc`」）

### §1.8 规划摘要 Approach（替换 L206）

**新**：

    - **Approach**：四核心 README 最小扰动（PROJECT_CONFIG §A/B、AGENTS、docs/README、根 README）+ legacy 6 文件索引迁移 + `_views/done.md` 更新（diff 大于 P1，30 帽禁止改 legacy 正文全文）

### §1.9 关账验收追加（在验收列表末、CI 条目前插入）

    - [ ] 关账时更新 [`docs/spec/governance/docs-noise-inventory/README.md`](../../spec/governance/docs-noise-inventory/README.md) 冲突寄存器 **C4、C5** 为 `done`（C6 不改）

### §1.10 P2-4 explore 门禁（在 P2-4 判定表前追加）

    > **explore 必做**：`task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` 须 `rg rag_fts_alias supabase/`（或等价）判定 done vs archived；**禁止** 30 帽无证据 `git mv`。

### §1.11 修订记录

追加一行：`2026-06-06 | R1 改稿：P2-2 子集对齐 · C4/C5/C6 映射 · 关账 C4/C5`

---

## §2 · 验证改稿

    python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md

须 **OK**。失败则修 task 后重跑。

---

## §3 · 新建 PROMPT 实例（照 P1 模板 · 改 P2 占位）

### §3.1 新建 `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`

对照：[`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md`](PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md)

替换占位：

| 占位 | P2 值 |
| --- | --- |
| Round | T0（本文件用途：复核/微调 task，若 task 已存在则 **改稿确认** 而非重写） |
| slug | `gov-docs-noise-p2` |
| git_branch | `task/gov-docs-noise-p2-v1` |
| task | `task_gov_docs_noise_p2_readorder_v1.md` |
| SPEC | §8.3 |
| gates | `HG-TASK-DRAFT` / `HG-GOV-P2-EXEC` |
| T2 下一棒 | 指向 T2c PROMPT 路径 |

### §3.2 新建 `PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`

对照：[`PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`](PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md)

须含：

| 节 | 内容 |
| --- | --- |
| gates | `HG-TASK-DRAFT` + `HG-GOV-P2-EXEC` approved |
| 帽链 | explore → 22 → 30 → 40 → CLOSE（跳过 50） |
| explore | 允许读：PROJECT_CONFIG §A/B 前 30 行 · AGENTS 必读节 · docs/README §1 · 根 README Endpoints/env · `ls legacy/` · **W1** b2_v2 的 `rg supabase/` |
| 30 spawn 注入 | PROMPT **§5.1** 三条 + 「禁止 git log 考古 · >10min 停」 |
| 30 交付 | P2-1～P2-4 按改稿后 task |
| 40 验证 | 使用 task 内 40 表命令 |
| CLOSE | C4/C5 寄存器 + HANDOFF_CLOSE_TRACE |

### §3.3 更新 task 依赖表 L150

将 `（**尚未创建**）` 改为相对链至上述两文件（改稿完成后路径须存在）。

---

## §4 · 更新 MANIFEST 与导图

### §4.1 `task_governance_docs_noise_line_manifest_v1.md`

| 字段 | 新值 |
| --- | --- |
| P2 行 task | `active/task_gov_docs_noise_p2_readorder_v1.md` |
| P2 状态 | `draft`（T0 改稿完成 · 待人签 gate） |
| git_branch | `task/gov-docs-noise-p2-v1` |
| Round 表 T2c | 链至 `PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md` |
| Round 表 T0 P2 | 链至 `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`（或注明 P2 task 已由 T0 产出，本批为改稿） |

### §4.2 `docs/spec/governance/docs-noise-inventory/README.md` §6

- **当前下一棒** → **P2 · T2c**（task 已建 · 待人签 `HG-GOV-P2-EXEC`）
- 增链：P2 T0 / T2c PROMPT 路径

### §4.3 `docs/harness/prompts/README.md`

文件列表增：

- `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`
- `PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`
- `PROMPT_claude_P2_pre_exec_amendments_zh.md`（本文件）

---

## §5 · commit + 回报人

**建议 commit 分 2 次**：

1. `docs(task): P2 R1 改稿 — 读序子集 · C4/C5/C6 映射`
2. `docs(harness): P2 T0/T2c PROMPT + MANIFEST 脚手架`

**回报（≤15 行）**：

- 改了哪些文件
- `harness_task_validate` 结果
- 仍 **pending** 的 gate_id（须人签）
- T2c 开跑指令：`@PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`（**gate 批准后**）

**禁止**：spawn T2c · 代签 gate · 改 P2 业务文件

---

## §6 · 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1：P2 R1 改稿 + 脚手架 · CC handoff |
