# Invoke 快照 · 50 独立复检 · chatbi-v3-lowconf-rag-preview

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| task_slug | chatbi-v3-lowconf-rag-preview |
| task_path | docs/tasks/active/task_chatbi_v3_lowconf_rag_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-rag-preview |
| freeze_id | CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31 |
| fresh_context | **必须** · 新会话 |
| review | docs/harness/reviews/by-task/chatbi-v3-lowconf-rag-preview/task_chatbi_v3_lowconf_rag_preview_v1_audit_R1_20260531.md |
| date | 20260531 |

---

## §3 调用体（快照 · Fresh Context）

```text
【须新会话】你正在扮演 Harness「50 独立复检帽」，严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/templates/TEMPLATE-independent-reinspect-invoke.md §3

输入：
- task：docs/tasks/active/task_chatbi_v3_lowconf_rag_preview_v1.md
- slug：chatbi-v3-lowconf-rag-preview
- SUBPROJECT_ROOT：ai-ink-brain-api-python
- REINSPECT_MODE：独立复检
- DIFF：git diff origin/main...HEAD（本仓 + 提示对照 ai-ink-brain 72f8f0c 契约）
- 审查：docs/harness/reviews/by-task/chatbi-v3-lowconf-rag-preview/task_chatbi_v3_lowconf_rag_preview_v1_audit_R1_20260531.md
- 自检：task §10

禁止：读 30 长聊天史；代签 HG-REINSPECT。

落盘：docs/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview_20260531_v1.md

完成后回报 00 继续 CLOSE（KPI、G8–G10、diary 样本、FE-5 联调口径）。

Judgment（50 · 待填）：
- experience_capture:
- gate/risk:
- hat_self:
```
