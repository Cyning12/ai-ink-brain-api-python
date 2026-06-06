# explore 帽 · P1 差分报告 — gov-docs-noise-p1

> **hat**: explore · **round**: R1 · **date**: 2026-06-06
> **task**: `gov_docs_noise_p1_archived_v1`
> **freeze_id**: `GOV-DOCS-NOISE-INVENTORY@2026-06-06`

---

## 1. 变更范围确认

仅两文件，无 api/tests/workflows 触及：

| 文件 | 动作 | 说明 |
|------|------|------|
| `docs/delivery/v0.2.0-code-rag/README.md` | **修改**（文首插入横幅） | 保留全文，仅加 archived 标记 |
| `docs/flows/README.md` | **新建** | 索引 / POINTER，不替代子文件 |

---

## 2. P1-1 现状 vs 期望

### 2.1 现状（`docs/delivery/v0.2.0-code-rag/README.md` 文首）

```markdown
# v0.2.0-code-rag 交付清单

> 为 ai-ink-brain-api-python 增加代码语义检索能力。
> 支持自然语言查询项目 Python 代码，返回精确到函数/类级别的代码片段。
```

- 当前文首无 archived / superseded 标记。
- 正文 106 行完整保留交付清单、SDD/TDD/Harness 表格、技术决策、部署记录、验收标准、前置条件、后续演进。

### 2.2 期望（须添加的 archived 横幅建议文案）

在 `# v0.2.0-code-rag 交付清单` 之前（文件最顶部）插入：

```markdown
> **ARCHIVED** — 本交付包为历史快照，已被 `docs/spec/`（当前 SDD 真值）与 `docs/harness/`（Harness 过程库）supersede。
> - 当前规格见 [`docs/spec/`](../../../spec/)
> - 当前 Harness 入口见 [`docs/harness/README.md`](../../../harness/README.md)

---
```

**约束**：
- 横幅位置必须在文首（第 1 行之前）。
- 不删除正文其余任何段落（SPEC §8.2 明确要求）。
- 链接使用相对路径：`../../../spec/`、`../../../harness/README.md`（从 `docs/delivery/v0.2.0-code-rag/` 出发）。

---

## 3. P1-2 现状 vs 期望

### 3.1 现状（`docs/flows/` 目录）

```
docs/flows/
  rag-chat/
    v1_2026-04-16_rag_chat_end_to_end.md
```

- 目录仅 1 个子目录 `rag-chat/`，内含 1 个快照文件。
- **无 `README.md`**。
- 快照内容：Legacy `/api/py/chat` 端到端流程（Mermaid sequenceDiagram），落后于当前 Unified/ChatBI。

### 3.2 期望（须新建的 `docs/flows/README.md` 大纲）

```markdown
# docs/flows — Legacy Chat 流程快照

> **FREEZE DATE**: `2026-04-16`
> **性质**: 本目录为 **Legacy chat** 端到端流程快照，落后于当前 Unified Chat / ChatBI 实现。
> **当前真值**: 端到端架构与流程已迁移至 [`docs/_tech_graph/`](../_tech_graph/)；入口见 [`docs/_tech_graph/00_main.md`](../_tech_graph/00_main.md)。

---

## 目录内容

| 文件 | 说明 |
|------|------|
| [`rag-chat/v1_2026-04-16_rag_chat_end_to_end.md`](rag-chat/v1_2026-04-16_rag_chat_end_to_end.md) | 2026-04-16 快照 · `/api/py/chat` 旧链路 |

---

> 本 README 仅为索引 / POINTER，不替代子文件内容。
```

**约束**：
- freeze 日期必须为 `2026-04-16`（与快照文件名一致）。
- 须说明 Legacy chat 性质、superseded by `_tech_graph`。
- 须链至 `docs/_tech_graph/00_main.md` 或 `docs/_tech_graph/README.md`。
- 明确本 README 仅作索引 / POINTER，不替代子文件。

---

## 4. 自检清单（供 40 帽引用）

| 检查项 | 命令 / 方法 | 期望结果 |
|--------|-------------|----------|
| delivery README 含 ARCHIVED 横幅 | `rg -n 'ARCHIVED' docs/delivery/v0.2.0-code-rag/README.md` | 命中且行号 < 5 |
| delivery README 链至 harness | `rg -n 'harness/README' docs/delivery/v0.2.0-code-rag/README.md` | 命中 |
| delivery README 链至 spec | `rg -n 'docs/spec' docs/delivery/v0.2.0-code-rag/README.md` | 命中 |
| flows README 已新建 | `test -f docs/flows/README.md` | exit 0 |
| flows README 含 freeze 日期 | `rg -n '2026-04-16' docs/flows/README.md` | 命中 |
| flows README 含 Legacy 说明 | `rg -n -i 'legacy' docs/flows/README.md` | 命中 |
| flows README 链至 _tech_graph | `rg -n '_tech_graph' docs/flows/README.md` | 命中 |
| 未改 api/tests/workflows | `git diff --stat` | 仅 docs/ 下两文件 |
| 未删历史文件 | `git status --short` | 无 `D` 状态 |

---

## 5. 结论

- **现状与期望 gap 明确**：两文件均符合 SPEC §8.2 描述，无歧义。
- **变更范围极小**：一文首插入、一新建 POINTER，零代码/零测试/零 CI workflow 触及。
- **无 blockers**：可直接进入 22 审核 → 30 执行 → 40 自检链。
