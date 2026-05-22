# Verification CI 模式（Harness V2 · P2 项 5）

> **状态**：指南 + 可选 workflow 落盘（与 [`HARNESS_V2_PLAN.md`](HARNESS_V2_PLAN.md) **§4 P2 项 5**、**§7** 一致）。  
> **真值**：合并前命令与 **Required checks** 以根 [`AGENTS.md`](../AGENTS.md) **§8** 与 [`HARNESS_V2_P0_ACCEPTANCE.md`](HARNESS_V2_P0_ACCEPTANCE.md) **§3** 为准；本文 **不** 定义第二套 pytest / pnpm 命令真值。

---

## 1. 目标

- **组织层面**：可选地把「仅测试 + 静态分析」做成 **独立 workflow 名称 / job**，便于分支保护、CODEOWNERS、或「写代码 Agent」与「只读复检」流程在 **纪律上** 对齐（见 [`prompts/50-independent-reinspect.md`](prompts/50-independent-reinspect.md)）。  
- **技术层面**：**不**替代 [`ai-ink-brain-api-python/.github/workflows/tech-graph.yml`](../../ai-ink-brain-api-python/.github/workflows/tech-graph.yml) / `tech-graph-contract.yml` 等契约门禁；**不**改变现有 `quality` / `pytest` 的 marker 与 CI `env` 语义。

---

## 2. 与现有 workflow 对照

| 资产 | 仓库 | 职责摘要 | 是否「合并前必绿」真值（默认） |
|------|------|-----------|-------------------------------|
| `quality.yml`（`name: quality`） | `ai-ink-brain` | install → lint → **test** → build | **是**（见 `AGENTS.md` §8） |
| `pytest.yml`（`name: pytest`） | `ai-ink-brain-api-python` | pytest + CI dummy `env` | **是** |
| `tech-graph*.yml` | `ai-ink-brain-api-python` | 图谱 / 契约 | **是**（与 `pytest` 并行；真值以各 workflow 为准） |
| `verify-fast.yml`（`name: verify-fast`） | 两仓各一 | 前端：lint + test，**无 build**；后端：与 `pytest.yml` **相同** marker / `env` / 命令 | **否（可选）**；见下文「并行与计费」 |

---

## 3. 形态 A — 并行轻量 `verify-fast`（YAML 已落盘）

**适用**：需要在 GitHub **Branch rules** 里增加一条 **独立 check 名称**（例如只把「测试 + lint」设为必需，而把 `build` 或图谱交给另一条规则）；或未来为不同 GitHub Environment / 权限模型预留同名 job。

**本仓库行为**：

- 前端：[`ai-ink-brain/.github/workflows/verify-fast.yml`](../../ai-ink-brain/.github/workflows/verify-fast.yml) — 触发条件与 `quality` 对齐；**不跑 `pnpm build`**。  
- 后端：[`ai-ink-brain-api-python/.github/workflows/verify-fast.yml`](../../ai-ink-brain-api-python/.github/workflows/verify-fast.yml) — `pytest` 命令与 **`pytest.yml` 中 `Run pytest` 一步逐字一致**，`env` 块与 `pytest.yml` **对齐**，避免行为分叉。

### 3.1 并行与计费（避免「双跑同一套测试」）

若 **同时** 将 `quality` 与 `verify-fast`（前端）或 `pytest` 与 `verify-fast`（后端）设为 **Required**，同一 PR 会在 runner 上 **重复执行** 相同或子集测试，分钟数与队列占用近似翻倍。

**推荐策略（选一）**：

1. **默认**：Required 仍只勾 **`quality`** / **`pytest`**（+ 图谱类）；`verify-fast` 保留在 Actions 中跑绿、**不作为 Required**，供团队观望或后续迁移。  
2. **迁移期**：若组织坚持「verify 名称」为唯一必需，须在规则里 **取消** 对重叠步骤的另一条的 Required，并书面约定真值（回写 `AGENTS.md` §8）。  
3. **收窄触发**：可按需在 `verify-fast.yml` 增加 `paths` / `paths-ignore`（本 v1 未默认启用，避免误伤全仓 PR）。

官方参考：[About branch rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rules-for-repositories/about-branch-rules) · [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

## 4. 形态 B — 仅流程与复检（不新增 YAML）

**适用**：小团队、单套 CI 已足够；P2 项 5 的「权限分离」通过 **复检帽输入裁剪**（diff + 日志 + 验收表）与 **CODEOWNERS / 人工合并** 完成。

与 [`prompts/README.md`](prompts/README.md) 中复检帽一致即可，无需第二套 workflow。

---

## 5. 本任务选用结论（混合）

- **YAML**：已按形态 **A** 落盘 `verify-fast.yml`（两子仓），便于「可启用路径」与验收中的 **首跑验证**（见任务单 **实现备忘**）。  
- **真值**：**合并前必绿**仍以 **`quality`** + **`pytest`**（及图谱 workflow）为准，直至维护者在 **Branch protection** 中显式改 Required 列表。  
- **未**将 `verify-fast` 默认写为必绿，是为避免与 §3.1 冲突；若全量 Required 两套，须在团队内先达成计费与命名共识。

### 5.1 团队选用结论（2026-05-14）

- **已采用**上文 **推荐策略 1**：**Required** 仅 **`quality`**（前端仓）+ **`pytest`**（后端仓）及既有图谱类 workflow；**`verify-fast` 不设为 Required**。  
- 书面验收与勾选见 [`HARNESS_V2_P0_ACCEPTANCE.md`](HARNESS_V2_P0_ACCEPTANCE.md) §6.1。

---

## 6. 首跑与本地等价

- **GitHub**：合并含 workflow 的 PR 后，在 **Actions** 页选择 **`verify-fast`**，确认对新 PR 出现绿色 check。  
- **本地等价**（非 `act` 强依赖）：  
  - 前端：`pnpm install --frozen-lockfile` → `pnpm lint` → `pnpm test`  
  - 后端：`pytest tests -m "not intent_eval and not intent_benchmark"`（与 `pytest.yml` 一致）；**`env` 须与 `pytest.yml` / `verify-fast.yml` 一致**（例如 `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=false`、dummy Key 等），否则结果可能与 CI 分叉。

---

## 7. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | 增补 **§5.1** 团队选用结论（`verify-fast` 不设 Required；与 P0 验收单 §6.1 对齐） |

---

## 8. 给 Cursor

`Harness`、`Verify`、`verification`、`workflow`、`verify-fast`、`quality`、`pytest`、`分支保护`、`HARNESS_V2_PLAN` §4 P2、`docs/harness/tasks`
