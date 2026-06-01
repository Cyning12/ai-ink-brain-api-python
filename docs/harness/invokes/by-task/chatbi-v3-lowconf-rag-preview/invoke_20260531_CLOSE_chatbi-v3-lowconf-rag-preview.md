# Invoke 快照 · CLOSE · chatbi-v3-lowconf-rag-preview

| 字段 | 值 |
|------|-----|
| hat_id | CLOSE |
| task_slug | chatbi-v3-lowconf-rag-preview |
| task_path | docs/tasks/done/task_chatbi_v3_lowconf_rag_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-rag-preview |
| freeze_id | CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31 |
| date | 20260531 |

---

## 执行路线与 Commit 回溯

**结论**：HG-REINSPECT 人签放行；50 复检 + KPI 100% pass；G8/G9/G10 · diary 索引 · task → `done/`。

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | commit |
|------|-------------|----------|----------|--------|
| 1 | 00 | 开帽 22→30→40 | `invoke_*_00_*` | `dafda18` |
| 2 | gate | HG-DRAFT / HG-AUDIT-R1 | task human_gate | `b540fa3` |
| 3 | 22 R1 | 零阻塞 · C1 | `reviews/.../audit_R1_20260531.md` | （本 CLOSE commit） |
| 4 | 30 | G1–G7 RAG preview + token | `api/*` · tests | `b297c94` |
| 5 | 40 | 自检 §10 | task §10 | `b297c94` |
| 6 | 50 v1 | 关账轮复检 | `reinspect_*_20260531_v1.md` | （本 CLOSE commit） |
| 7 | CLOSE | KPI · G8/G9 · done | task `done/` · 母单 · SPEC | （本 CLOSE commit） |

### api-python 分仓索引（新→旧）

```text
- （CLOSE）docs: KPI · 母单 5-3 · SPEC §6 · reinspect · diary · git mv done
- b297c94 feat(chatbi): 低置信 RAG 方案预览与 plan token 放行（5-3）
- b540fa3 docs(task): 人签 HG-TASK-DRAFT / HG-AUDIT-R1
- dafda18 docs(harness): 00 开帽
- 89ba341 docs(task): 草案 §5-3
```

---

## §3 调用体（快照）

```text
00/CLOSE：关账已人签；KPI 100% pass；无下一棒。
```
