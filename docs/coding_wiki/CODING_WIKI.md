# CODING_WIKI.md — LLM Wiki Schema（本仓）

> **freeze_id**：`CODING-WIKI-PILOT@2026-05-25`  
> **治理 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) · **T4 桥接**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)  
> **指导意见**：工作区 `Projects/docs/harness/guides/GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md`  
> **需求对比（理论 / SPEC / 交付 / 缺口）**：[`WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](WIKI_REQUIREMENTS_COMPARISON_v1_zh.md)

---

## 1. L0 / L1 / L2 分工

| 层 | 载体 | 谁维护 | Agent 何时读 |
|----|------|--------|--------------|
| **L0** | `docs/_tech_graph/`、`graph.json`、`_contract_manifest`、`PROJECT_CONFIG` | 人 + CI | 改接口/表/流程拓扑 |
| **L1** | `docs/tasks/`、`docs/harness/invokes|reviews`、`docs/spec/` | Harness 关账链 | 单 task 执行与验收 |
| **L2** | **本目录** `docs/coding_wiki/` | ingest + lint | 跨 task 概念/综合叙事（**非**第二真值） |

**禁止**：将 Wiki 页标为「当前架构真值」；与 task `freeze_id` 矛盾时以 L0/L1 为准（见 task `failure_paths` F1）。

---

## 2. 目录约定

```text
docs/coding_wiki/
├── CODING_WIKI.md      # 本文件（schema）
├── index.md            # 导航目录
├── log.md              # append-only 时间线
├── concepts/           # 跨 task 概念
├── syntheses/          # 已关账 task 蒸馏（摘要 + 链接）
├── sources/            # SPEC 摘要 stub（可选）
├── entities/           # 模块/表实体 stub（可选）
└── decisions/          # append-only 决策记录（可选）
```

---

## 3. Frontmatter 最小集

每页 YAML 头（`---`）：

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 人读标题 |
| `slug` | 是 | 稳定 ID（kebab-case，与 Wiki-CTX-AB 对齐时可复用） |
| `layer` | 是 | 固定 `L2` |
| `source_task` | syntheses 必填 | 相对子仓根，指向 `docs/tasks/done/...` |
| `closed_date` 或 `freeze_id` | 至少其一 | 关账锚点 |
| `status` | 是 | `compiled` \| `stub` \| `deprecated` |
| `graph_nodes` | 否 | **T4** 可选；`id` + `relation` + 可选 `note` / `manifest_ref`（见 T4 SPEC §3） |

**T4 覆盖（syntheses · 2026-05-29）**：**25/25** 页 frontmatter 均含 `graph_nodes` 键（非空种子 **17** · 纯叙事 `[]` **8**）。机器校验：

```bash
python tools/coding_wiki_graph_nodes_lint.py
pytest tests/test_coding_wiki_graph_nodes_lint.py -q
```

## 4. 三操作

### 4.1 Ingest

1. 仅 **done** task（或已 accepted 的 SPEC 摘要）进入 `syntheses/`。  
2. 每页：**摘要**（背景、决策、验收要点）+ **wikilink** 至 L1；**禁止**复制 review/SPEC 全文。  
3. 更新 `index.md` 与 `log.md`（`YYYY-MM-DD` 前缀行）。  
4. **进行中** task 仅可在 `log.md` 记一行，不写 `syntheses/`。

### 4.2 Query

1. 先读 `index.md` → 按主题打开 1～3 页。  
2. 若 frontmatter 含 `graph_nodes`：记下种子 `id`，对每个 id 执行 `python tools/tech_graph_graph_query.py neighbors <id>`，再按需 `downstream`/`upstream`。  
3. 需影响面/依赖遍历 → **并行** 使用 `graph_query`（L0），不以 Wiki 替代。  
4. 答案可写回 Wiki 时：小改直接编辑；大改走新 task + 再 ingest。

### 4.3 Lint

| 检查 | 动作 |
|------|------|
| 孤儿页（未在 index 登记） | 补 index 或删页 |
| `source_task` 404 | 修正路径或标 `deprecated` |
| 与 `freeze_id` 矛盾 | 标「待人工」，禁止 syntheses 当真值 |
| 复制 Harness `prompts/` 全文 | 删正文，改 pointer |
| `graph_nodes[].id` 不在 graph_v2 | `graph_query neighbors <id>` exit 4 → 修 id 或删项 |
| `graph_nodes[].relation` 非法 | 须在 T4 SPEC §3.1 表内 |
| syntheses 缺 `graph_nodes` 键 | `python tools/coding_wiki_graph_nodes_lint.py` exit 1 |

**VERIFY**：

```bash
python tools/coding_wiki_graph_nodes_lint.py
```

## 5. 链接规则

- **wikilink**：`[[syntheses/harness-p1-docs-consolidation]]`（相对本目录，无扩展名）  
- **pointer**：`→ docs/tasks/done/task_….md` 单行，可带锚点说明  
- **禁止**：绝对本机路径、`file://`、未脱敏密钥

---

## 6. 与 Harness / 图谱边界

| 不进 Wiki | 进 Wiki 方式 |
|-----------|--------------|
| `docs/harness/prompts/` 帽子全文 | `concepts/` 流程概念 + 链 README |
| `reviews/` 全文 | 摘要 + `→ docs/harness/reviews/by-task/...` |
| Mermaid 边 / `graph.json` | prose + 链 `_tech_graph`；影响集用 graph_query |
| `graph_nodes` 机器轨 | frontmatter 种子 + `graph_query`；**禁止** 手改 `graph.json` |

---

## 7. 试点定位（与 Karpathy LLM Wiki 的关系）

本目录是 **工程化裁剪版** LLM Wiki，首要目标是降低 **L1 Harness 历史**（`invokes/`、`reviews/`、长 done task）在 **关账回顾 / 跨 Epic 理解** 时的上下文消耗，**不是**个人知识库式的全量 Raw + 概念网。

| Karpathy 模式 | 本仓试点 |
|---------------|----------|
| Raw 原文库 + 每源改 10～15 页 | **L1 即原文真值**；L2 只 ingest **done** 摘要 |
| 实体/概念织网 | `concepts/`、`entities/` **可选**；表/RPC/依赖以 **L0 图谱** 为准 |
| Wiki 即唯一真值 | **禁止**；与 L0/L1 矛盾时以 L0/L1 为准 |

**读序（关账后默认）**：`index.md` → `syntheses/<slug>.md` → 按需 pointer 打开 L1 → 改代码/拓扑必 L0。  
**Agent 默认读序常模**：见 [`SPEC-Governance-Wiki-Agent-Readorder-v1.md`](../spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md) · `AGENTS.md` 必读链第 5 条。

---

## 8. 测试迭代档案（过程存档 · 非 coverage 真值）

Wiki **不**执行、不替代 pytest / CI / 覆盖率统计，也**不**维护与代码等价的「用例清单真值表」（避免与 `tests/` 漂移）。

**存档对象**：测试覆盖工作的 **变更史、意图、范围边界**，支撑未来对测试做增删改查时的上下文，例如：

| 写入位置 | 内容示例 |
|----------|----------|
| `syntheses/<slug>.md` §测试变更 | 本 Epic **新增/删除/修改** 了哪些测试文件；覆盖了哪些 **failure path**（文字 + pointer） |
| `decisions/`（append-only） | 「删除 flaky 用例 X，原因…」「某 ERR 分支暂不测，欠债单…」 |
| `concepts/` | 跨 Epic 测试策略演进（如 ChatBI 分级闸门、smoke → e2e） |
| `log.md` | `YYYY-MM-DD \| ingest \| <slug> \| 测试 +2 -1` |

**与图谱测评 L2 工具链的关系**：[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) · `_test_manifest.json`、锚点校验等负责 **机器校验**；Wiki 负责 **人/Agent 读懂「为何这样测」** 并 pointer 到 L0 `ERR_*` 与 L1 `failure_paths`。

**ingest 纪律**：仅 **done** 且与测试交付相关的 task 写入 synthesis；进行中调整只记 `log.md` 一行。

### 8.1 `api/` 类 Epic · `test_strategy` ingest（Multi slug B-Q3 纪律）

当 ingest 的 **done** L1 task **曾改 `api/`**（RAG 路由、ingest、unified chat 等）且 L1 头含 **`test_strategy`** 时：

| 检查项 | 要求 |
|--------|------|
| **frontmatter** | `test_strategy: required \| recommended \| not_applicable` — **取值须与 L1 task 头一致** |
| **或摘要** | 摘要或 §测试变更 **内联** 同上取值 + wikilink `[[../concepts/test-strategy-ink-backend]]` |
| **禁止** | 仅写「见 concept / 见 test-strategy」**而不**给出枚举取值（Wiki-only 无法答 B-Q3 类题） |
| **VERIFY** | ingest 关账前：`rg -n test_strategy docs/coding_wiki/syntheses/<slug>.md` 有命中且取值与 L1 一致 |

**示范**：`syntheses/query-rewrite-observability`（A1 · `recommended`，链 [`task_coding_wiki_ingest_test_strategy_v1.md`](../tasks/done/task_coding_wiki_ingest_test_strategy_v1.md)）。

---

## 9. 原文（Raw）与 `sources/` 何时启用

```text
pointer（1 行 → L1）→ synthesis（摘要）→ 按需打开 L1 片段 → 仍过大再写 sources/ stub
```

| 场景 | 动作 |
|------|------|
| 已有结构化 L1（task、SPEC、review by-task） | **不**复制全文进 Wiki；`source_task` + pointer 即可 |
| L1 单文件过大、Agent 仅需结论 | 在 `sources/` 写 **stub 摘要**（可选），正文仍留 L1 |
| 无 L1、仅外部剪报/帖子库 | 参考 Karpathy Raw 库（本仓 **非** 当前试点范围） |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-26 | 试点 v1：目录、frontmatter、ingest/query/lint |
| 2026-05-26 | §7 试点定位；§8 测试迭代档案；§9 Raw/sources 启用条件 |
| 2026-05-26 | 链出 `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` |
| 2026-05-26 | §8.1 `api/` Epic `test_strategy` ingest 纪律（Wiki Loop A2 · `CODING-WIKI-A2-SCHEMA-RULE@2026-05-26`） |
| 2026-05-27 | T4：`graph_nodes` frontmatter · query/lint · 链 Bridge SPEC |
| 2026-05-27 | T4 扩面：3 slug 含 `graph_nodes`（Pilot `query-rewrite-observability` + `chatbi-v3-text2sql-tool-latency-obs` + `tech-graph-gate-d-v2-tasks`）|
| 2026-05-27 | Agent 读序常模：链 Readorder SPEC · `AGENTS.md` 必读第 5 条 |
| 2026-05-29 | T4 运营化：syntheses **25/25** `graph_nodes` 键 · `tools/coding_wiki_graph_nodes_lint.py` |
