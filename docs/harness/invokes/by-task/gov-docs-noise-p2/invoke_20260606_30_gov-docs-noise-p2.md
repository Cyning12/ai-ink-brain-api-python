# Invoke · 30 · T2c · gov-docs-noise-p2

> **Round**：T2c
> **Hat**：30-docs
> **Branch**：`task/gov-docs-noise-p2-v1`
> **Date**：2026-06-06

---

## 输入

- task: `docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md`
- SPEC §8.3
- explore: `docs/harness/invokes/by-task/gov-docs-noise-p2/explore_P2_diff_20260606.md`

## 强制注入

- PROMPT §5.1：禁止 git log/blame/考古 · 禁止读 task 范围外路径 · docs-only >10min 须停并向 Lead 汇报

## 交付

- **P2-1**：PROJECT_CONFIG §A/B `.cursorrules` → 已移除；真值 `.cursor/rules/*.mdc`
- **P2-2**：AGENTS.md 与 docs/README.md §1 canonical 子集对齐 + 双向互链；保留扩展导航条
- **P2-3**：根 README.md Unified Chat 端点 pointer（或 PROJECT_CONFIG §F pointer）
- **P2-4**：legacy 6 文件消化（git mv done/ 或补 archived + pointer）+ _views/done.md 更新

## 回填

- task `### 自检结论（执行者）`

## 禁止

- 删 invoke/review 历史
- 改 legacy 正文全文
- 无证据判定 b2_v2 为 done
- 改 api/、tests/、.github/workflows/

## 下一棒

harness-40-check
