# Invoke · 40 · T2b · gov-docs-noise-p1

> **Round**：T2b
> **Hat**：40-check
> **Branch**：`task/gov-docs-noise-p1-v1`
> **Date**：2026-06-06

---

## 输入

- task: `docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md`
- 30 交付：delivery README + flows README

## 验证

- `test -f docs/flows/README.md`
- `rg -n 'ARCHIVED|archived' docs/delivery/v0.2.0-code-rag/README.md`
- `git diff --stat` 确认仅 docs/ 变更
- `git diff --name-only | grep -E 'api/|tests/|.github/workflows/'` 应为空

## 交付

- 回填 task `### 自检结论（40 帽回填 · T2b 后）`
- 建议 CLOSE + PR / 或列出阻塞

## 下一棒

Lead CLOSE
