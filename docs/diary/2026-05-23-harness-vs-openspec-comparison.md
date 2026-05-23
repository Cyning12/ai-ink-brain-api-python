# Harness 与 OpenSpec 对照备忘（2026-05-23）

> **性质**：探索性备忘，**非**工程真值；未决是否引入 OpenSpec CLI 或 delta 协议。  
> **真值仍见**：`docs/harness/HARNESS_V2_PLAN.md`、`docs/tasks/`、`docs/_tech_graph/`、工作区 `Projects/AGENTS.md`。

---

## OpenSpec 是什么

[Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)：面向 AI 编码助手的 **Spec-Driven Development（SDD）** 工具链。

典型流程：

```text
/opsx:propose → openspec/changes/<name>/
  ├── proposal.md
  ├── specs/（需求与场景）
  ├── design.md
  └── tasks.md
/opsx:apply → 按 tasks 实现
/opsx:verify → 对照 artifact 验证
/opsx:archive + /opsx:sync → delta 回写 openspec/specs/ 主规格
```

哲学：**fluid not rigid**、轻仪式、brownfield 友好；自比 GitHub Spec Kit 更轻。

---

## 与 Harness 的重叠（同构层）

| 维度 | OpenSpec | 本仓 Harness |
|------|----------|--------------|
| 先对齐再写码 | proposal + specs | 10 帽 task + SPEC + 验收表 |
| 变更包落盘 | `changes/<name>/` | `docs/tasks/active/task_*.md` + invokes/reviews |
| 实现 | `/opsx:apply` | 30 帽 + 自检 |
| 验证 | `/opsx:verify` | `test_strategy` + pytest/CI + 50 reinspect |
| 关账 | archive + sync delta | `done/` + `_views/done.md` |

估计 **SDD 主链概念重叠约 40%～60%**。

---

## Harness 多出的部分（OpenSpec 默认不覆盖）

1. **多帽角色链**：10→22→30→40→50、`semi_auto`、`human_gate`
2. **Verify 背压**：合并前必绿、reinspect 证据表、`test_strategy` 三档
3. **技术图谱机器轨**：`docs/_tech_graph/`、`graph.json`、manifest/contract CI
4. **多子仓调度**：工作区 `Projects/AGENTS.md`、跨仓契约
5. **审计落盘**：`docs/harness/reviews/`、`reinspect_results/`、invoke 快照链
6. **IDE 规则真值**：`.cursor/rules/*.mdc`、`docs/tasks/skills/`

OpenSpec README 将 Spec Kit 标为「阶段闸 rigid」— Harness 仪式更接近 Spec Kit 完整度 + 自研治理层。

---

## 可借鉴、暂不引入工具的部分

| 借鉴点 | 做法（不必装 OpenSpec CLI） |
|--------|---------------------------|
| Delta 写法 | 大 SPEC 变更用 `ADDED/MODIFIED/REMOVED` 小节 |
| sync 语义 | 关账 task 时显式列「更新了哪些 SPEC/图谱段落」 |
| explore 阶段 | 大需求先探索再 10 帽，减少 task 返工 |

**风险**：同时维护 `openspec/changes/` 与 `docs/tasks/` → **双真值**，暂不建议并行引入。

---

## 待决问题（记录占位）

- [ ] 是否在 long SPEC 上试点 delta 段落（无 CLI）
- [ ] Harness 内部是否进一步「减 ceremony」（docs-only 路径 B 已试点）
- [ ] 是否对外写一页「Harness vs OpenSpec」给协作者（非 diary）

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-23 | 初稿：对话备忘，暂无引入决策 |
