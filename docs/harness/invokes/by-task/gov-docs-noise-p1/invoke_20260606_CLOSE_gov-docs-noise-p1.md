# Invoke · CLOSE · T2b · gov-docs-noise-p1

> **Round**：T2b
> **Hat**：Lead CLOSE
> **Branch**：`task/gov-docs-noise-p1-v1`
> **Date**：2026-06-06

---

## 前置

- 40 结论：建议 CLOSE + PR
- merge_policy: `docs_only_ci_green_merge`
- close_action: `merge`

## 动作

1. `gh pr create` — docs-only PR
2. CI watch — Required checks 全绿
3. `gh pr merge --squash`（close_action 授权）
4. `git mv task` → `done/` + 更新 `_views/done.md`
5. HANDOFF_CLOSE_TRACE

## 验收

- [ ] P1-1: delivery README archived 横幅
- [ ] P1-2: flows/README.md 新建
- [ ] CI Required 全绿
- [ ] PR merged

## 下一棒

无（P1 完成）
