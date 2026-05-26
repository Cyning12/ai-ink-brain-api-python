# CODING_WIKI.md — LLM Wiki Schema（本仓）

> **freeze_id**：`CODING-WIKI-PILOT@2026-05-25`  
> **治理 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)  
> **指导意见**：工作区 `Projects/docs/harness/guides/GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md`

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

---

## 4. 三操作

### 4.1 Ingest

1. 仅 **done** task（或已 accepted 的 SPEC 摘要）进入 `syntheses/`。  
2. 每页：**摘要**（背景、决策、验收要点）+ **wikilink** 至 L1；**禁止**复制 review/SPEC 全文。  
3. 更新 `index.md` 与 `log.md`（`YYYY-MM-DD` 前缀行）。  
4. **进行中** task 仅可在 `log.md` 记一行，不写 `syntheses/`。

### 4.2 Query

1. 先读 `index.md` → 按主题打开 1～3 页。  
2. 需影响面/依赖遍历 → **并行** 使用 `python tools/tech_graph_graph_query.py`（L0），不以 Wiki 替代。  
3. 答案可写回 Wiki 时：小改直接编辑；大改走新 task + 再 ingest。

### 4.3 Lint

| 检查 | 动作 |
|------|------|
| 孤儿页（未在 index 登记） | 补 index 或删页 |
| `source_task` 404 | 修正路径或标 `deprecated` |
| 与 `freeze_id` 矛盾 | 标「待人工」，禁止 syntheses 当真值 |
| 复制 Harness `prompts/` 全文 | 删正文，改 pointer |

---

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

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-26 | 试点 v1：目录、frontmatter、ingest/query/lint |
