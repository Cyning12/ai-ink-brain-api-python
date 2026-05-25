# 任务审核：ChatBI V3 · Prompt 注入防护 PoC（P1-2）— CLOSE

## 元信息

| 字段 | 值 |
|------|-----|
| 审查轮次 | **CLOSE**（R4 复审签收 · 关账） |
| 关联上一轮 | **R4**：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_R4_20260514.md` |
| 待审 task | `ai-ink-brain-api-python/docs/tasks/done/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（关账后路径） |
| 关联 SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_22_chatbi-v3-prompt-injection-closeout-audit.md` |
| **git_branch** | `task/chatbi-v3-prompt-injection-closeout-v1` |
| **human_gate** | **`approved`**（22 帽终轮签收；无待回填） |
| 规划对齐 | `docs/harness/HARNESS_V2_PLAN.md` **§5**；`docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md` **INK-P3 / §3 B3** |
| 落盘日期 | 2026-05-20 |

---

## 审查结论摘要

1. **pytest（本帽复跑）**：于分支 `task/chatbi-v3-prompt-injection-closeout-v1`、子仓根执行 `pytest tests -m "not intent_eval and not intent_benchmark"` → **退出码 0**，**199 passed**，1 skipped，2 deselected（约 100s）；与 CI `pytest.yml` 门禁一致。  
2. **§4 验收**：task 正文 `- [x]` 全勾选；含 **SSE v1** `test_sse_v1_prompt_guard_short_circuits_before_decide_intent`（相对 R4 文档项 NB-3 已随实现闭合）。  
3. **failure_paths / §5**：FP-1～FP-4 与 `api/chatbi_prompt_guard.py`、`api/unified_chat.py`、golden `tests/fixtures/chatbi/prompt_guard_fp1_unified_chat_error_envelope.json` 及 `tests/test_chatbi_prompt_guard_fp1_envelope_contract.py` 一致；**fail-closed** + `internal_error` 在 warn 下同等短路有 pytest `test_scan_fail_closed_internal`。  
4. **freeze_id**：`SPEC-SEC-2026-05-13-§3` 于 SPEC **§6** 无漂移。  
5. **文档项（R4 复检项）**：`PROJECT_CONFIG` **§C** 含 `CHATBI_PROMPT_GUARD_MODE`（默认 `off`）；SPEC **§3.1**「首期 PoC（已合并代码）」+ **§6** 2026-05-14 修订 — **pass**。

---

## 阻塞项

- **无**。

---

## 非阻塞项

| ID | 说明 |
|----|------|
| NB-scope | **历史块 / rewrite 出口** 仍仅扫用户 `query`（task「已知未测」与 SPEC §3.1 非范围一致）；不阻塞 P1-2 关账。 |

---

## 需任务帽回填清单

- [x] task 头部 **状态** → `done（2026-05-20 · 22 帽 CLOSE 签收）`  
- [x] `git mv` `active/` → `done/`  
- [x] `docs/tasks/_views/done.md` 索引  
- [x] `PRIORITY_ROADMAP` **INK-P3 / §3 B3** → `done（2026-05-20）`（工作区根，§0）

---

## 是否建议执行帽开工

| 结论 |
|------|
| **否**（P1-2 PoC 已交付；无待修阻塞）。 |

---

## 签收 / 关闭

- **结论**：**approved** — P1-2 Prompt guard PoC **Harness 书面闭环**；task 可 **`done`** 归档。  
- **与 R4 关系**：R4 零阻塞 + 待关账 checklist 已由本轮 **22 帽** 在 closeout 分支完成；R4 中「下一棒需求帽」动作并入本 CLOSE 关账提交。  
- **human_gate**：`approved`（本文件元信息；无 `pending` 待人改项）。

---

## 执行路线与 Commit 回溯

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | `10` 需求 | P1-2 task + failure_paths | `docs/tasks/…/task_chatbi_v3_prompt_injection_guard_poc_v1.md` | `54826c3` |
| 2 | `30` 执行 | JSON Unified guard | `api/chatbi_prompt_guard.py` 等 | `fba40f2` |
| 3 | `30` 执行 | SSE 短路扩展 | `api/unified_chat.py` | `029b290` |
| 4 | `40` 自检 | §4 勾选 + pytest 摘要 | task 自检小节 | `4080e36` |
| 5 | `22` R4 | 文档层终审（零阻塞） | `…_audit_R4_20260514.md` | `398f777` |
| 6 | `22` CLOSE | 关账 + 路线图 + 本文件 | task→`done/`、PRIORITY_ROADMAP | *本轮 closeout commit* |

### api-python（ai-ink-brain-api-python）

- `029b290` feat(chatbi): extend prompt guard PoC to Unified SSE path  
- `398f777` docs(harness): add task audit R4 for ChatBI prompt guard PoC (P1-2)  
- `4080e36` docs(task): refresh self-check section for prompt injection guard PoC  
- `fba40f2` feat(chatbi): P1-2 prompt guard PoC on unified JSON path  
- *本轮* `docs(harness): 22 CLOSE ChatBI P1-2 prompt guard 签收关账` — 见对话末尾 short-hash  

### Projects（工作区根）

- *本轮* `docs(roadmap): INK-P3/B3 Prompt 注入 PoC done（2026-05-20）` — 见对话末尾 short-hash  

---

## 给 Cursor

`Harness`、`任务审核`、`CLOSE`、`approved`、`P1-2`、`prompt_guard`、`INK-P3`、`B3`、`HANDOFF_CLOSE_TRACE`
