# invoke_20260608_CLOSE_chatbi-intent-retry-u1.5-chain

> **帽**：CLOSE  
> **round**：T1  
> **task_slug**：`chatbi_intent_llm_retry_u1_5_v1`  
> **task_path**：`docs/tasks/done/task_chatbi_intent_llm_retry_u1_5_v1.md`  
> **git_branch**：`task/chatbi-intent-llm-retry-u1.5-chain-v1`  
> **merge_policy**：`docs_only_ci_green_merge`  
> **Epic**：`GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08` · G2

---

## §3 Prompt（CLOSE 帽 · 全文）

```text
【角色】Harness CLOSE · T1 B 轨 · ChatBI Intent U1.5 链式补关账

【前置】
- 50 reinspect 已落盘 · pytest 全集绿 · task_validate OK
- human_gate 均已 approved

【必须完成】
1. task git mv → docs/tasks/done/（若尚未）
2. 更新 docs/tasks/_views/done.md
3. 更新 RECENT §1.3（G2 done · MANIFEST → done/）
4. MANIFEST Epic 标 done · A+B 齐 CLOSE
5. PR #137/#138 merge · 删已合并分支

【禁止】改 api/ · 扩 scope

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 关账摘要（落盘时填写）

| 项 | 值 |
| --- | --- |
| **PR** | #137（T1 链）· #138（关账收尾） |
| **代码** | 已在 main（PR #110 · `9a01ebd`）· 本链为 Harness 补关账 |
| **50** | `reinspect_chatbi_intent_llm_retry_u1_5_20260608_v1.md` |
| **Epic** | G1 + G2 done → **semi_auto 全面废弃** 条件满足 |
