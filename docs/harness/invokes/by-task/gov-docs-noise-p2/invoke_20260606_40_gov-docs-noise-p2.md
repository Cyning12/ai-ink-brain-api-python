# Invoke · 40 · T2c · gov-docs-noise-p2

> **Round**：T2c
> **Hat**：40-check
> **Branch**：`task/gov-docs-noise-p2-v1`
> **Date**：2026-06-06

---

## 输入

- task: `docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md`
- 30 交付：PROJECT_CONFIG + AGENTS + docs/README + 根 README + legacy 6 文件

## 验证

| 命令 | 结果 |
|------|------|
| `rg -n '\.cursorrules.*当前\|仍.*保留\|仍常保留' docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 无命中（`NO_MATCH`） |
| `rg -n 'AGENTS\.md\|docs/README\.md' AGENTS.md docs/README.md` | AGENTS.md L18 → docs/README.md §1；docs/README.md L6 → AGENTS.md；双向互链存在 |
| `rg -n 'unified/chat\|PROJECT_CONFIG.*§F' README.md` | L12 `POST /api/py/unified/chat`；L13 `POST /api/py/unified/chat/stream`；L15 pointer 至 PROJECT_CONFIG §F |
| `git diff --stat HEAD -- api/ tests/ .github/workflows/` | 无输出（未改动受限路径） |
| `ls docs/tasks/legacy/` | 空（legacy 已消化） |
| `rg -n 'task_rag_b\|task_03\|Task 04' docs/tasks/_views/done.md` | 6 条新条目均命中 |

## 交付

- 回填 task `### 自检结论（40 帽回填 · T2c 后）`：6 项检查全绿
- 建议 **CLOSE + PR / merge**：无阻塞

## 下一棒

Lead CLOSE
