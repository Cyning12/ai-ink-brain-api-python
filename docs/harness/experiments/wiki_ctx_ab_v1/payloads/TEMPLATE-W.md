# Payload · W（P2 · Wiki 臂 · 模板）

> **含义**：**仅 Coding Wiki（L2）** — `index.md` + 同 slug 的 `syntheses/` 页；**禁止** Harness README、done task 全文、invoke/review。  
> **使用**：复制为 `W_{{TASK_SLUG}}.md`，或运行 `python tools/wiki_ctx_ab_materialize_w.py --slug {{TASK_SLUG}}`。

| 元信息 | 值 |
| --- | --- |
| **arm** | `W` |
| **task_slug** | `{{TASK_SLUG}}` |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **T1b 依赖** | `docs/coding_wiki/syntheses/{{TASK_SLUG}}.md` 须存在 |

---

## Agent 约束（实验 Prompt 附件首段）

```text
你只能依据下文「载荷正文」作答。
禁止打开 docs/harness/、docs/tasks/done/ 全文、invoke/review。
若载荷中无信息，回答「载荷未提供」而非猜测。
```

---

## 1. 允许的文件清单（固定 · 不得追加）

| # | 相对路径 | 内容要求 |
| --- | --- | --- |
| 1 | `docs/coding_wiki/index.md` | **全文**（含 syntheses 表行） |
| 2 | `docs/coding_wiki/syntheses/{{TASK_SLUG}}.md` | **全文** |

**禁止清单**

- `docs/coding_wiki/CODING_WIKI.md`（除非人审显式扩 scope）
- `docs/harness/**`、`docs/tasks/done/**` 全文
- 其它 slug 的 syntheses

---

## 2. 载荷正文（内联区 · 物化脚本填充）

```text
（--- FILE: ... --- 分隔的多文件正文）
```

---

## 3. 物化后统计（必填）

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | |
| `file_count` | 应为 2 |
| `notes` | |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：P2 W 臂模板（README 占位） |
| 2026-05-26 | v1.1：对齐 T1b 物化脚本与两文件清单 |
