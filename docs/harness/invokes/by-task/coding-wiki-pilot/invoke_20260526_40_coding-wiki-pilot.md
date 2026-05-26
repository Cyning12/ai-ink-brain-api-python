# Invoke 快照 · 40 自检 · coding-wiki-pilot

| 字段 | 值 |
|------|-----|
| **task_slug** | `coding-wiki-pilot` |
| **task_path** | `docs/tasks/active/task_coding_wiki_pilot_v1.md` |
| **git_branch** | `task/coding-wiki-pilot-v1` |
| **帽** | 40 |
| **日期** | 2026-05-26 |

## 验证命令（纯文档）

```bash
cd ai-ink-brain-api-python
test -f docs/coding_wiki/CODING_WIKI.md
test -f docs/coding_wiki/index.md
test -f docs/coding_wiki/log.md
grep -q '2026-05-26' docs/coding_wiki/log.md
grep -q ingest docs/coding_wiki/log.md
test $(find docs/coding_wiki/syntheses -name '*.md' | wc -l) -ge 2
git diff --quiet docs/harness/prompts/
```

结论见 task `### 自检结论（执行者）`。
