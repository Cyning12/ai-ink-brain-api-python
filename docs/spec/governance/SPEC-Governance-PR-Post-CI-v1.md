# SPEC — PR 后 CI 监听、说明同步与条件自动合并（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-PR-POST-CI@2026-05-26` |
| **适用范围** | 本仓 `ai-ink-brain-api-python`；前端 `ai-ink-brain` **另仓** 须镜像 SPEC（检查名不同） |
| **实现** | [`.github/workflows/pr-post-ci.yml`](../../../.github/workflows/pr-post-ci.yml) · [`.mergify.yml`](../../../.mergify.yml) · [`docs/tasks/skills/SKILL-pr-post-ci.md`](../../tasks/skills/SKILL-pr-post-ci.md) |

---

## 0. 背景与问题

| 现象 | 影响 |
| --- | --- |
| PR 创建后继续 push，**body / Test plan 不自动更新** | 审查人与合并后审计误解范围（例：PR #54） |
| CI 绿后仍须人工改勾选、合并 | 纯文档 PR 成本高 |
| squash 多主题进一支 PR | 标题与 diff 不一致时，**自动 merge 风险高** |

**目标**：CI Required 全绿后 **自动刷新 PR 元数据**；在 **白名单** 下 **自动 squash merge**；其余交 Agent SKILL + 人审。

---

## 1. 三层分工（方案 C）

| 层 | 载体 | 职责 |
| --- | --- | --- |
| **L0** | `.cursor/rules/09-pr-post-ci.mdc` | 开 PR / push 后须同步 body；禁止未绿 merge |
| **L1** | `SKILL-pr-post-ci.md` | Agent：监听、`gh pr edit`、多主题 Summary、冲突与评论 |
| **L2a** | `pr-post-ci.yml` | Bot：CI 完成后追加 **CI 状态**、勾选 Test plan 模板项 |
| **L2b** | `.mergify.yml` | Bot：`label:automerge` + 路径白名单 + checks 绿 → squash merge |

---

## 2. 为何「docs 更合适」、前后端有何风险

### 2.1 本后端仓（api-python）

| 维度 | 纯 docs / 治理 PR | 含 `api/` / 契约 / CI 变更 |
| --- | --- | --- |
| **回归信号** | pytest 仍跑，但 diff 常不触业务路径 | pytest + contract/图谱 失败即真回归 |
| **自动改 body** | 脚本按路径统计即可，误判成本低 | 须人写 Summary（行为、回滚、Env） |
| **自动 merge** | 可启用 `automerge` 标签 | **默认禁止**；须人 merge |
| **典型风险** | 漏写同批并入主题（#54） | 线上 API、迁移、密钥 |

### 2.2 前端仓（ai-ink-brain）

| 维度 | 说明 |
| --- | --- |
| **检查集不同** | `pnpm lint` / `pnpm test` / `pnpm build`（见工作区 `AGENTS.md` §8） |
| **不可照搬 yaml** | `check-success` 名称、Required 列表须按该仓 branch protection 配置 |
| **UI/契约** | 改 BFF、SSE、env 示例 → **禁止** docs 白名单 automerge |
| **建议** | 复用本 SPEC **语义**；复制 workflow + mergify 时 **改检查名与 paths** |

### 2.3 结论（裁决）

- **pr-post-ci.yml**：全仓 PR 均可跑 **CI 状态追加 + Test plan 勾选**（无路径歧视）。  
- **Mergify automerge**：**仅** `label:automerge` + **非 api/tests 变更**（见 §3.2）。  
- **前后端「有风险」** 指 **自动 merge**，不是指 **自动更新 PR 说明**。

---

## 3. 行为规约

### 3.1 `pr-post-ci.yml`（CI 完成后）

**触发**：`workflow_run`（pytest / tech-graph / tech-graph-contract / verify-fast 完成）及 `pull_request` `synchronize`。

**动作**（PR 仍 open 时）：

1. 汇总 Required 类 checks（见 workflow 内 `REQUIRED_CHECKS` 列表）。  
2. 若 **全部 success**：  
   - 在 PR body 追加或更新 `## CI 状态（自动 · pr-post-ci）` 表（时间、check、conclusion）。  
   - 将 `## Test plan` 下与模板匹配的 `- [ ]` 改为 `- [x]`（不删除人工条目）。  
   - 追加 `## 变更范围（自动统计）`：`git diff --name-only` 按顶层目录计数。  
3. 若 **未全绿**：仅更新 CI 状态表为失败/进行中，**不** 勾选 Test plan，**不** merge。

**不做什么**：不用 LLM 重写 Summary；多主题 PR 的叙述性 Summary 由 **SKILL / 人** 补。

### 3.2 `.mergify.yml`（条件自动合并）

**同时满足** 方可 squash merge：

| # | 条件 |
| --- | --- |
| M1 | label 含 **`automerge`** |
| M2 | base = `main` |
| M3 | checks：`pytest`、`manifest_check`、`contract_check` 为 success |
| M4 | **无** `api/**` 变更（`files` 规则） |
| M5 | **无** `tests/**` 变更 |
| M6 | **无** `.github/workflows/**` 变更（防 CI 自改自通过） |
| M7 | 非 draft |

**显式禁止 automerge**（须人 merge）：`supabase/sql/**`、`requirements.txt`、`.env.example` 变更 — 在 mergify 用 `-files~=` 或扩展规则。

### 3.3 Agent SKILL

见 [`SKILL-pr-post-ci.md`](../../tasks/skills/SKILL-pr-post-ci.md)：开 PR 首写 body、push 后 diff 对账、#54 类多主题分节、是否打 `automerge` 标签。

---

## 4. 人工闸与标签

| 标签 | 谁打 | 含义 |
| --- | --- | --- |
| `automerge` | **人** | 允许 Mergify 在 M1–M7 满足时自动 squash |
| `no-automerge` | **人** | 禁止自动合并（覆盖 automerge） |

**禁止** Agent 自行打 `automerge`，除非用户明文授权且 diff 通过 §3.2 路径自检。

---

## 5. 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | Required check 失败 | 只更新 CI 表；不勾选 Test plan |
| F2 | 路径含 `api/` 但带 `automerge` | Mergify 不合并；comment 提示移除标签或拆 PR |
| F3 | bot 改 body 失败（权限） | workflow 失败；人用手动 `gh pr edit` |
| F4 | 多主题 squash 仅依赖 bot Summary | **不允许**；人须补 Summary（SKILL） |

---

## 6. 验收标准

- [ ] `pr-post-ci.yml` 在 PR 上 green 后追加 `## CI 状态（自动 · pr-post-ci）`。  
- [ ] `tools/pr_post_ci_update_body.py` 可在本地 `python tools/pr_post_ci_update_body.py --pr N` 复现。  
- [ ] `.mergify.yml` 在 Mergify 启用后：仅 docs PR + `automerge` 自动合并。  
- [ ] `SKILL-pr-post-ci.md` 与 `.cursor/rules/09-pr-post-ci.mdc` 已链入 `docs/tasks/skills/README.md`。  
- [ ] 前端仓镜像前须更新 `REQUIRED_CHECKS` 与 paths（§2.2）。

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：方案 C（workflow + Mergify + SKILL）；#54 教训 |
