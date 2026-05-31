## Summary

<!-- 行为变更一句话；若涉 api/ 契约，写明影响面 -->

---

## 自检验收清单（合并前须满足）

> **Ink 轨**：高敏书面复检见 `docs/harness/reviews/` 或 `docs/tasks/reinspect_results/`；**本清单不替代** `human_gate_check`。

- [ ] 本地：`pytest tests -m "not intent_eval and not intent_benchmark"` 通过
- [ ] PR 上 **pytest** + **tech-graph** + **tech-graph-contract**（若触达）Required 全绿
- [ ] 若改 `api/` / SSE / 契约：已更新 task **§行为变更 Delta** + `_manifest` / 契约 fixture（**同 PR**）
- [ ] 若改结构图：已更新 `.ai.md` 且 `graph_export --check` 通过
- [ ] 高敏变更（`api/`、`test_strategy: required`）：**独立复检** 已落盘或本 PR 链 `reinspect_results/`

### Blocking 提示（须人判断 · 非 PR 关键词过闸）

| 类型 | 例 | 须 |
| --- | --- | --- |
| **对外契约** | 改响应字段、SSE 事件名、路由 | task Delta + 50 + 契约 CI |
| **运行锚点** | 改 env 名、端点、部署前提 | manifest + 任务单声明 |
| **主依赖** | 主框架大版本、copyleft 新依赖 | 人读 changelog/LICENSE + 扩大回归 |

---

## Test plan

- [ ] （作者填写：关键手动场景或 pytest 路径）

---

## 关联

- Task：`docs/tasks/active/` 或 `done/` 路径
- 审查：`docs/harness/reviews/`（如有）
