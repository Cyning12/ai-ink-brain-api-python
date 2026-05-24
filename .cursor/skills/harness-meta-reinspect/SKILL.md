---
name: harness-meta-reinspect
description: >-
  Performs independent Harness meta-reinspect after semi_auto chains (30→40→50→close):
  zero chat context, git diff human_gate audit, re-run pytest, compare prior reinspect.
  Use when user requests third-party review, meta reinspect, semi_auto trial audit,
  or post-merge Harness process validation.
disable-model-invocation: true
---

# Harness 元复检（独立 · 零对话上下文）

> **便携真值（跨 Agent）**：[`docs/tasks/skills/SKILL-harness-meta-reinspect.md`](../../../docs/tasks/skills/SKILL-harness-meta-reinspect.md)  
> **范例报告**：[`docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_resilience_20260524_meta_v1.md`](../../../docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_resilience_20260524_meta_v1.md)

## 何时使用

- `semi_auto: true` 关账后，需**第三方**审计流程（非仅 task 内容）
- 首轮 `50` 与执行链**同会话**，怀疑「状态快照陷阱」
- 人声称「全预批」但需验证 **git 轨迹** 是否合规

## 硬约束（违反则只输出阻塞清单）

1. **禁止**用上一段对话当证据；**禁止**把既有 `reinspect_*.md` 当真值（须对拍）
2. **必须**自行重跑 task 所列合并前命令（本仓默认：`pytest tests -m "not intent_eval and not intent_benchmark"`）
3. **必须**对 `human_gate` 表做 **commit-level diff**（`git log -p` / `git diff <base>..HEAD -- <task>`），追溯 author
4. **禁止**改 gate、改业务代码；仅新增 `docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_meta_vN.md`

## 最小命令集

```bash
git branch --show-current
git log --oneline <base>..HEAD
git diff --name-only <base>...HEAD
git log -p <base>..HEAD -- <task_path>   # 查 human_gate 行变更
pytest tests -m "not intent_eval and not intent_benchmark"
```

## 必审三轴

| 轴 | 要点 |
|----|------|
| **A 内容** | 对照 task 验收项；证据须 `路径:行` / 测试名 / 命令输出 |
| **B 流程** | invoke 30/40/50 是否落盘；40 与 pytest 是否一致；CLOSE_TRACE 是否在 PR/审查中 |
| **C gate** | `pending→approved` 是否由 **人单独 commit**；Agent 代填须有对话授权 + commit message 注明 |

## 同会话偏差

若 30/40/50 同一会话：报告须含 **「流程元复检（同会话偏差披露）」**，并说明 50 非严格独立。

## 输出

- 落盘：`docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_meta_vN.md`（结构见 `docs/harness/ACCEPTANCE_LANDING.md`）
- 结论：`建议合并` / `建议合并（附形式瑕疵记录）` / `不建议合并` / `证据不足待补`
- 与首轮 reinspect **分歧表**（若无写「无实质分歧」）

## 规范引用

- `docs/harness/prompts/50-independent-reinspect.md`
- `docs/harness/prompts/HANDOFF_SEMI_AUTO.md` §2.3（human_gate）
- `docs/harness/prompts/HANDOFF_CLOSE_TRACE.md`
