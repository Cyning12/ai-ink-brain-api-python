# Payload · H-lean（P1 基线臂 · 模板）

> **含义**：**纪律消费** — 只读 README + done task + 排期相关行；**禁止** invoke/review 全文。  
> **使用**：复制为 `H-lean_{{TASK_SLUG}}.md`，替换占位符并粘贴摘录。

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `{{TASK_SLUG}}` |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |

---

## Agent 约束（实验 Prompt 附件首段）

```text
你只能依据下文「载荷正文」作答。
禁止打开 docs/harness/invokes/by-task/ 下任意 invoke 全文或 reviews 全文。
若载荷中无信息，回答「载荷未提供」而非猜测。
```

---

## 1. 允许的文件清单（固定 · 不得追加 invoke/review 全文）

| # | 相对路径 | 内容要求 |
| --- | --- | --- |
| 1 | `docs/harness/README.md` | 仅 §1「日常读什么」+ §2.1「落盘 taxonomy」全文摘录 |
| 2 | `docs/harness/invokes/README.md` | 仅「命名建议」+「何时必须写」两节摘录（各 ≤40 行） |
| 3 | `docs/tasks/done/{{DONE_TASK_FILENAME}}` | **全文**（done task 视为关账摘要真值） |
| 4 | `docs/tasks/RECENT_TASK_SCHEDULE.md` | 仅含 **P1-2 / P1-3 / harness-p1** 关键词的段落（§0.4 表 + 本 Epic 相关 1 段） |

**禁止清单**

- `docs/harness/invokes/by-task/{{TASK_SLUG}}/*`
- `docs/harness/reviews/by-task/{{TASK_SLUG}}/*`
- `docs/coding_wiki/*`（P1 不用 Wiki）

---

## 2. 载荷正文（内联区）

### 2.1 docs/harness/README.md（摘录）

```text
（粘贴 §1 + §2.1）
```

### 2.2 docs/harness/invokes/README.md（摘录）

```text
（粘贴命名 + 何时必须写）
```

### 2.3 docs/tasks/done/{{DONE_TASK_FILENAME}}（全文）

```text
（粘贴 done task 全文）
```

### 2.4 RECENT_TASK_SCHEDULE 摘录

```text
（粘贴 §0.4 P1-2/P1-3 表行 + 指向 task_harness_p1_docs_consolidation 的一句）
```

---

## 3. 物化后统计（必填）

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | |
| `file_count` | 应为 4 |
| `notes` | |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：H-lean 模板 |
