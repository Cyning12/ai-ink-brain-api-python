# docs/tasks/skills/ — 蒸馏 SKILL 索引

> **用途**：为新建 task 提供 **高频场景预填片段**，与 [`../templates/TASK_TEMPLATE.md`](../templates/TASK_TEMPLATE.md) 骨架叠加；降低 Harness 扩展字段（`test_strategy`、`failure_paths`、`human_gate` 等）填写成本。  
> **真值层级**：类型清单与关账蒸馏口径以 [`docs/diary/2026-05-22-harness-evaluation-improvement-response.md`](../../diary/2026-05-22-harness-evaluation-improvement-response.md) **§三 3.1**（已接受 P1 规格）为准；字段语义与 [`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) **§5** 对齐。  
> **非目标**：本目录 **不替代** task 正文；具体业务仍须在 `active/task_*.md` 中微调。  
> **跨 Agent**：本目录为 **Git 便携真值**；Cursor 另维护 [`.cursor/skills/README.md`](../../.cursor/skills/README.md)（项目 skill 入口，Claude Code / Kimi **默认不自动读取**）。

---

## 如何使用

```text
1. 人/Agent 识别任务类型 → 选下表 SKILL ID
2. 按该类型的「范围 / 非范围 / failure_paths / 验收 / Harness 默认值」预填 task
3. 复制 TASK_TEMPLATE 骨架 → 叠加 SKILL 片段 → 微调业务内容
4. 关账后（可选）按「关账蒸馏」节萃取共性，更新 SKILL 正文（须人审）
```

**CLI 生成脚本**：P1 可选，非阻塞；当前可先 `cp` 模板 + 手工改字段。

---

## 六类 SKILL 一览

| SKILL ID | 适用阶段 | 输入 | 输出（task 预填重点） |
|----------|----------|------|------------------------|
| [`api-endpoint`](SKILL-api-endpoint.md) | 30 执行前 | 路由契约、`_contract_manifest` 切片、关联 SPEC | 范围：路由 + handler + 测试 + 契约同步；`test_strategy: required` |
| [`bug-fix`](SKILL-bug-fix.md) | 30 执行前 | 复现步骤、日志/失败测试 | 范围：根因 + 最小修复 + 回归测试；禁止顺带重构 |
| [`refactor-module`](SKILL-refactor-module.md) | 10 / 22 规划 | 模块边界、调用点清单 | 范围：迁移 + 测试适配；非范围：业务逻辑/API 契约变更；`test_strategy: recommended` |
| [`docs-governance`](SKILL-docs-governance.md) | 10 / 30 | 目录/索引变更范围 | 范围：文档移动 + 链接修复；非范围：代码/CI；`test_strategy: not_applicable` + note |
| [`tech-graph-update`](SKILL-tech-graph-update.md) | 30 执行前 | 受影响 `.ai.md`、manifest/contract | 范围：维护轨 + 机器轨导出；验收含 `tech_graph_*_check` |
| [`harness-task`](SKILL-harness-task.md) | 10 需求帽 | prompts/模板/rules 变更点 | 范围：Harness 工件；非范围：业务代码；**`audit_profile: full`** |
| [`harness-meta-reinspect`](SKILL-harness-meta-reinspect.md) | 50 后 / 合并后 | 首轮 reinspect + git 历史 + invoke 链 | **零上下文**流程元复检：`human_gate` commit diff、同会话偏差、对拍首轮 50；落盘 `reinspect_*_meta_vN.md` |
| [`pr-post-ci`](SKILL-pr-post-ci.md) | 开 PR / push 后 | PR 号、是否 docs-only | CI 监听、body/Test plan 同步、`automerge` 白名单；见 `SPEC-Governance-PR-Post-CI-v1` |

各类型详细预填段落见同目录 `SKILL-<id>.md`（随关账蒸馏增量维护；初版可与本表语义一致即可）。

---

## 关账蒸馏与人审口径

> **来源**：评价改进回复 **§三 3.1**「关账后蒸馏 + **人审后合并**」— ✅ 已接受。

### 触发条件

- task 验收通过：头部 `done（YYYY-MM-DD …）` + `git mv` 至 `docs/tasks/done/`（见 [`../README.md`](../README.md) 归档流程）
- 关账链路完整：`40` 自检回填、`50` 复检（若 task 要求）、`HANDOFF_CLOSE_TRACE`（若 semi_auto 关账）

### 蒸馏动作

1. 对比 task **初稿**（10 帽或首 commit）与 **done 终稿**
2. 提取高频共用段落：范围 / 非范围 / `failure_paths` / 验收项中重复模式
3. 若某模式在同类型 task 中重复出现（建议阈值：**≥2 次**），起草 `SKILL-<type>.md` 更新
4. 产出为 **建议草案**，**禁止** Agent 自动合并入主分支 SKILL 正文

### 人审合并

| 步骤 | 谁 | 做什么 |
|------|-----|--------|
| 1 | Agent / 人 | 关账后提交 SKILL 更新 PR 或 patch，标注来源 task |
| 2 | **人** | 审阅是否过拟合单一历史 task、是否与 HARNESS_V2 §5 字段冲突 |
| 3 | **人** | 合并 SKILL 正文；必要时回流更新本 README 一览表 |
| 4 | （可选） | 在来源 task 或 review 中留一行「已蒸馏至 SKILL-xxx」 |

**禁止**：蒸馏产物自动写入 `approved` 态 `human_gate`；蒸馏 **不替代** 22/50 审查职责。

---

## 目录结构（目标态）

```text
docs/tasks/skills/
  README.md                  # 本文件：索引 + 使用 + 关账蒸馏
  SKILL-api-endpoint.md
  SKILL-bug-fix.md
  SKILL-refactor-module.md
  SKILL-docs-governance.md
  SKILL-tech-graph-update.md
  SKILL-harness-task.md
  SKILL-harness-meta-reinspect.md
  SKILL-pr-post-ci.md
```

初版可仅维护 **README + 本表**；各 `SKILL-*.md` 随首个同类型 task 关账后按需增补。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-23 | P1-2 初版：6 类 SKILL 索引 + 关账蒸馏/人审口径（`task_harness_p1_docs_consolidation_v1`） |
| 2026-05-24 | 新增 `harness-meta-reinspect`；双轨 `.cursor/skills/` 说明（P2-1 元复检蒸馏） |
