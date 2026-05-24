# SKILL：Harness 元复检（独立 · 通用）

> **SKILL ID**：`harness-meta-reinspect`  
> **适用阶段**：50 帽之后、或 PR 合并后审计；**非**替代首轮 `50`，而是 **流程合规 + 对拍** 增强。  
> **来源**：`task_chatbi_v3_p2_resilience_v1` 全预批 + `semi_auto` 关账试验；元复检报告见 [`../reinspect_results/reinspect_chatbi_v3_p2_resilience_20260524_meta_v1.md`](../reinspect_results/reinspect_chatbi_v3_p2_resilience_20260524_meta_v1.md)。  
> **Cursor 项目 skill**：[`.cursor/skills/harness-meta-reinspect/SKILL.md`](../../../.cursor/skills/harness-meta-reinspect/SKILL.md)（仅 Cursor 自动发现；**其它 Agent 读本文件**）。

---

## 跨 Agent 如何读到本 SKILL？

| 平台 | 推荐读法 |
|------|----------|
| **Cursor** | `@docs/tasks/skills/SKILL-harness-meta-reinspect.md` 或 `@.cursor/skills/harness-meta-reinspect` |
| **Claude Code** | 读 `AGENTS.md` → 本路径；新会话粘贴「执行 SKILL-harness-meta-reinspect」+ task/分支 |
| **Kimi Code / 其它** | 将本文件全文或 §可复制 Prompt 放入上下文；**无** `.cursor/skills` 自动加载 |
| **人 / CI** | Git 跟踪 `docs/tasks/skills/`；PR review checklist 可链本文 |

**原则**：凡需 **审计 Harness 流程** 的场景，以 **Git 内 `docs/tasks/skills/SKILL-harness-meta-reinspect.md`** 为便携真值；`.cursor/skills/` 为 Cursor 快捷入口，二者须同步修订。

---

## 触发场景

- task 含 `semi_auto: true` 且走完 **30→40→50→关账**
- `human_gate` 含 `HG-REINSPECT` / `HG-GLOBAL-SIGNOFF`，或 kickoff **全预批** 试验
- 首轮 `reinspect_*.md` 由**同会话** Agent 产出，需第三方 **零上下文** 复核
- 合并后复盘：验证「声称未改 gate」是否与 `git log -p` 一致

---

## 身份与输入隔离

你是 **独立元复检 Agent**：假定**未参与**实现与首轮 50。

| 允许作证据 | 禁止作证据 |
|------------|------------|
| `git diff` / `git log -p` / `git blame` | 上一 Agent 对话摘要 |
| task / invoke / review / reinspect **文件正文** | 首轮 reinspect 的结论（仅可对拍） |
| **自行重跑**的 pytest 原始输出 | 「应该已经测过」 |

---

## 硬约束

1. **禁止**修改 `human_gate`、业务代码、CI；**禁止** `git add -A`
2. **禁止**仅读 task 终态即断言「未改写 gate」——须 **commit-level diff**
3. **禁止**因 `HG-*` 已为 `approved` 而跳过流程审查
4. 落盘路径：`docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_meta_vN.md`（`meta` 与首轮 `reinspect` 区分版本号）

---

## 执行步骤（通用）

### 0. 收集锚点

| 项 | 填写 |
|----|------|
| task 路径 | `docs/tasks/done/` 或 `active/` |
| git 分支 | `task/<slug>` |
| diff 基线 | `main...HEAD` 或 `origin/main...HEAD` |
| 首轮 50 报告 | `docs/tasks/reinspect_results/reinspect_*`（对拍用） |
| invoke 链 | `docs/harness/invokes/invoke_*_{30,40,50}_*.md` |
| 合并前命令 | 本仓默认：`pytest tests -m "not intent_eval and not intent_benchmark"` |

### 1. 命令（必须自行执行）

```bash
git branch --show-current
git log --oneline <base>..HEAD
git diff --name-only <base>...HEAD
git diff --stat <base>...HEAD
git log -p <base>..HEAD -- <task_path>
pytest tests -m "not intent_eval and not intent_benchmark"
```

### 2. 审查维度 A — Task 内容

表头：`验收项 | pass/fail | 独立证据 | 与首轮 reinspect 一致? | 备注`

覆盖：拆单/子 task 字段、非范围（如无 `api/`）、Overview 索引、pytest 与 40 自检一致性。

### 3. 审查维度 B — Harness 流程（重点）

表头：`流程检查项 | pass/fail | 证据 | 风险(L/M/H) | 备注`

**至少**包含：

| # | 检查项 |
|---|--------|
| B1 | 30/40/50 invoke 是否落盘且与 commit 对应 |
| B2 | 40 `### 自检结论` 是否与独立 pytest 一致 |
| B3 | 50 是否披露 **同会话** 偏差（若 30/40/50 同会话） |
| B4 | 50 是否对 **diff** 审查（非仅终态快照） |
| B5 | 关账：`done` + `git mv` + `_views` + Overview 是否同逻辑批次 |
| B6 | **`human_gate` 行**：`git log -p` 是否出现 Agent author 的 `pending→approved` |
| B7 | commit 是否避免 `git add -A` 扫入杂项 |
| B8 | PR / 关账是否含 **HANDOFF_CLOSE_TRACE** 结构化回溯 |

### 4. `human_gate` 专审（状态快照陷阱）

```bash
# 示例：找出 task 历史上 gate 表变更
git log -p <first_task_commit>..HEAD -- docs/tasks/**/task_<slug>.md
```

判定口径（与 `HANDOFF_SEMI_AUTO.md` §2.3 对齐）：

| 情形 | 判定 |
|------|------|
| 人 **单独 commit** 改 `approved` | 形式合规 |
| 人口头预批，Agent 在 **业务 commit** 内改 gate | **形式瑕疵**（内容可能对）；须在报告中写明 author |
| Agent 改 gate 且无对话授权记录 | **流程 fail**（高） |
| 首轮 50 写「未改写 gate」但 diff 显示改写 | 首轮 50 **fail**（元复检须披露） |

### 5. 审查维度 C — 子 task 抽检（若适用）

抽检 3～5 条：验收是否可执行（命令/断言）、`test_strategy: required`、非范围是否防耦合。

### 6. 落盘结构（`ACCEPTANCE_LANDING.md` + 扩展）

1. 元信息（task、branch、commit range、日期）  
2. 独立 pytest 结果  
3. 维度 A / B / C 表  
4. **流程元复检（同会话偏差披露）**  
5. 阻塞项 / 结论 / 与首轮 reinspect 分歧表  
6. 修订记录  

---

## 结论用语（统一）

| 用语 | 含义 |
|------|------|
| **建议合并** | 内容与流程均无阻塞 |
| **建议合并（附形式瑕疵记录）** | 业务可合并；gate author / CLOSE_TRACE 等有形式问题 |
| **不建议合并** | 内容或流程存在实质阻塞 |
| **证据不足待补** | 缺 diff、缺 pytest、缺 invoke 等 |

---

## 可复制 Prompt（给新会话 · 任意 Agent）

```text
你未参与本 task 实现。请严格按 docs/tasks/skills/SKILL-harness-meta-reinspect.md 执行元复检：
- 零对话上下文；自行 git diff + git log -p 审查 human_gate；自行重跑 pytest
- 对拍首轮 docs/tasks/reinspect_results/reinspect_<slug>_*.md（非真值）
- 落盘 docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_meta_vN.md
- task: <TASK_PATH>
- 分支: <BRANCH>
- 基线: main...HEAD
```

---

## 与 Harness 真值的关系

| 文档 | 关系 |
|------|------|
| `50-independent-reinspect.md` | 首轮 50 内容验收；本 SKILL **叠加**流程元复检 |
| `HANDOFF_SEMI_AUTO.md` | gate / semi_auto 规则来源 |
| `HANDOFF_CLOSE_TRACE.md` | 关账回溯格式 |
| `ACCEPTANCE_LANDING.md` | reinspect 落盘最小结构 |

后续若更新 `HANDOFF_SEMI_AUTO` / `50-independent-reinspect`，须与本 SKILL **语义一致**（gate diff、人单独 commit 优先）。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-24 | 初版：P2-1 元复检蒸馏；双轨 Cursor + docs/tasks/skills |
