# Payload · H-full（P1 对照臂 · 模板）

> **含义**：模拟「扫 by-task 目录读全过程」— 载荷尽量大。  
> **使用**：复制本文件为 `H-full_{{TASK_SLUG}}.md`，按下方清单 **内联全文** 或 **逐文件路径列表**（二选一，但 P1 跑分须固定一种并记入 `scorecard`）。

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-full` |
| **task_slug** | `{{TASK_SLUG}}` |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |

---

## Agent 约束（实验 Prompt 附件首段）

```text
你只能依据下文「载荷正文」作答。禁止读取未列出的路径。
若载荷中无信息，回答「载荷未提供」而非猜测。
```

---

## 1. 必须纳入的文件清单（{{TASK_SLUG}} · 请勾选已内联）

### 1.1 invokes（by-task 下 **全部**）

| # | 相对路径（本仓根） | 已内联 |
| --- | --- | --- |
| 1 | `docs/harness/invokes/by-task/{{TASK_SLUG}}/invoke_*.md` | [ ] |

**实例（harness-p1-docs-consolidation）**：

- `docs/harness/invokes/by-task/harness-p1-docs-consolidation/invoke_20260523_10_harness-p1-docs-consolidation.md`
- `docs/harness/invokes/by-task/harness-p1-docs-consolidation/invoke_20260523_30_harness-p1-docs-consolidation.md`
- `docs/harness/invokes/by-task/harness-p1-docs-consolidation/invoke_20260523_40_harness-p1-docs-consolidation.md`
- `docs/harness/invokes/by-task/harness-p1-docs-consolidation/invoke_20260523_50_harness-p1-docs-consolidation.md`

### 1.2 reviews（同 slug 下 **全部** · 若有）

| # | 相对路径 | 已内联 |
| --- | --- | --- |
| 1 | `docs/harness/reviews/by-task/{{TASK_SLUG}}/task_*_audit_*.md` | [ ] |

> 本 slug 若无 review 子目录，在 scorecard 注明「reviews=0」。

### 1.3 done task 全文

| # | 相对路径 | 已内联 |
| --- | --- | --- |
| 1 | `docs/tasks/done/{{DONE_TASK_FILENAME}}` | [ ] |

**实例**：`docs/tasks/done/task_harness_p1_docs_consolidation_v1.md`

---

## 2. 载荷正文（内联区）

> 将 §1 中文件 **按顺序** 粘贴于下。每个文件前加一行 `--- FILE: <path> ---` 便于计数。

```text
（在此粘贴 invoke / review / done task 全文）
```

---

## 3. 物化后统计（必填）

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | |
| `file_count` | |
| `notes` | 是否含 review；是否用路径列表代替内联 |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：H-full 模板 |
