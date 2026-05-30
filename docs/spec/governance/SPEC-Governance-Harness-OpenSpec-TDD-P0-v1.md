# SPEC — 治理：Harness OpenSpec 写法 × TDD 纪律 · P0 执行安排

| 项 | 内容 |
| --- | --- |
| **状态** | `active`（Loop R1–R3 执行中 · Step 0 模板 done） |
| **freeze_id** | `GOV-HARNESS-OPENSPEC-TDD-P0@2026-05-30` |
| **排期** | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) **§0.6** |
| **Loop 母单** | [`docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md`](../../tasks/active/task_harness_p0_openspec_tdd_loop_v1.md) |
| **Manifest** | [`docs/harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md`](../../harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md) |
| **分支** | `task/harness-p0-openspec-tdd`（单 PR） |

> **背景**：OpenSpec / Harness 对比分析与 TDD 架构评估；**不**引入 `openspec/` 目录、不全员 strict TDD。  
> **原则**：OpenSpec **写法 P0** 与 TDD **纪律 P0** **合并 Sprint A**（同一 `task_validate` + 22/40 补丁），不拆两波 PR。

---

## 1. O1～O3 是否完成态？

**结论：模板级 ✅ 完成；全仓 adoption ❌ 未做。**

| ID | 内容 | 完成度 | 说明 |
|----|------|--------|------|
| **O1** | task §行为变更 Delta（ADDED/MODIFIED/REMOVED） | **✅ 模板完成** | [`docs/tasks/templates/TASK_TEMPLATE.md`](../../tasks/templates/TASK_TEMPLATE.md) L63–80 |
| **O2** | failure_paths + **Scenario ID** 列 | **✅ 模板完成** | 同文件 L95–106 |
| **O3** | 大 task §规划 artifact（proposal/design/tasks 等价） | **✅ 模板完成** | 同文件 L129–147 |
| — | README / HARNESS_V2 指针 | **✅ 文档完成** | [`docs/tasks/README.md`](../../tasks/README.md)、[`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) §5.1 |

**尚未完成（不算 O1–O3 闭环）**：

- [ ] 存量 `docs/tasks/active/*.md` **未回填** Delta/Scenario  
- [ ] 22 帽 **未**增格式勾选项  
- [ ] **无** `task_validate` 机械校验  
- [ ] 关账合并 Delta → `docs/spec/` 的 checklist **未**写进 50/关账流  

**因此**：对新 task Copy 模板即完成 Step 0；全仓 **Step 1–3** 由 Loop **R1–R3** 交付。

---

## 2. 总览：P0 项状态表

### 2.1 OpenSpec 借鉴（写法 + 工具）

| ID | 项 | 状态 | Loop |
|----|-----|------|------|
| O1 | Delta Spec 小节 | ✅ 模板 | — |
| O2 | Scenario ID | ✅ 模板 | — |
| O3 | 规划 artifact 分节 | ✅ 模板 | — |
| O4 | `tools/harness_task_validate.py` | ⬜ 待做 | **R1** |
| O5 | `tools/harness_change_status.py`（`--json`） | ⬜ 待做 | **R3** |
| O6 | `.cursor/commands/harness-*.md` | ⬜ 待做 | **R3** |

### 2.2 TDD 纪律 P0

| ID | 项 | 状态 | Loop |
|----|-----|------|------|
| T1 | 22 帽：`api/` 禁滥用 `not_applicable` | ⬜ 待做 | **R2** |
| T2 | 22 帽：Scenario / test_strategy 勾选项 | ⬜ 待做 | **R2** |
| T3 | 40 帽：Completeness/Correctness/Coherence 三维提示 | ⬜ 待做 | **R2** |
| T4 | `task_validate` 内嵌 test_strategy 规则 | ⬜ 待做 | **R1**（与 O4 合并） |
| T5 | 存量 active task 抽样回填 | ⬜ 可选 | Sprint C |

### 2.3 重叠说明

- **O2 ≡ TDD Scenario 命名** → 模板一次写完，勿重复做。  
- **O4 + T4** → **同一个脚本**，一次读取 task 校 Delta + Scenario + test_strategy。

---

## 3. 执行顺序（冻结 · Loop 映射）

```text
已完成（Step 0）──► Loop R1（validate · O4+T4）
                      │
                      ▼
                   Loop R2（22/40 帽 · T1–T3）
                      │
                      ▼
                   Loop R3（status + cursor · O5+O6）
                      │
                      ▼
                   META 关账 + REPORT_completion_*
                      │
                      ▼
                   Sprint C（可选 · 存量回填）
```

| 历史 Sprint 名 | Loop round | task |
|----------------|------------|------|
| Sprint A（validate） | **R1** | `task_harness_p0_task_validate_v1.md` |
| Sprint A（22/40） | **R2** | `task_harness_p0_audit_selfcheck_v1.md` |
| Sprint B | **R3** | `task_harness_p0_status_cursor_v1.md` |

**不做**：先只做 OpenSpec 再做 TDD 的两波 PR。  
**不做**：等 universal `harness-spec` 库再落地 R1（本仓 `tools/` 先 dogfood）。

---

## 4. R1 交付清单（`harness_task_validate.py`）

### 4.1 规则（草案）

| 规则 | 来源 | 严重级别 |
|------|------|----------|
| Harness 元信息表存在 | 原有 | error |
| `not_applicable` ⇒ 须 `test_strategy_note` | 原有 | error |
| 失败路径表 ≥1 行 | 原有 | error |
| `test_strategy: required` ⇒ 验收含 pytest 类表述 | TDD | warn/error |
| 变更触达 `api/`（启发：范围/实现备忘/图谱）⇒ 禁 `not_applicable` | TDD | error |
| §行为变更：有 API 变更时不得仅写「无」 | O1 | warn |
| Delta 节含 ADDED/MODIFIED/REMOVED 之一或显式「无」 | O1 | warn |
| failure_paths 含 Scenario ID 列非空 | O2 | warn |
| `semi_auto: true` ⇒ `git_branch` 非 main | 原有 | error |
| human_gate 表格式 | 原有 | error |

CLI：

```bash
python tools/harness_task_validate.py docs/tasks/active/task_foo.md
python tools/harness_task_validate.py --all-active
python tools/harness_task_validate.py --json docs/tasks/active/task_foo.md
```

### 4.2 R2：22 帽增补（T1+T2）

在 `22-task-audit.md` 或 reviews 模板增勾选：

- [ ] `test_strategy` 与变更类型一致（`api/` 非 `not_applicable`）  
- [ ] §行为变更 Delta 已填或明确「无」  
- [ ] failure_paths 含 Scenario ID  
- [ ] 验收含合并前 pytest 条（模板已有则核对）  

### 4.3 R2：40 帽增补（T3）

在 `40-self-check.md` 增可选自检表：

| 维度 | 自问 |
|------|------|
| Completeness | 每个 Scenario / F# 有测例或命令证据？ |
| Correctness | 错误码/边界与 task 一致？ |
| Coherence | 实现与 Delta / SPEC 无 silent drift？ |

---

## 5. R3 交付清单

| 项 | 交付 |
|----|------|
| O5 | `harness_change_status.py`：读 task + reviews + human_gate → JSON（下一 hat、pending gates） |
| O6 | `.cursor/commands/harness-validate.md`、`harness-status.md`（薄封装，指向 tools + 真值路径） |

**依赖**：R1 的 validate 规则稳定后，status JSON 可复用同一解析器。

---

## 6. Sprint C（可选 · 非 P0 阻塞）

- 选 2～3 个 **active 且触达 api/** 的 task 手工回填 Delta + Scenario  
- 22 季度抽检与 T1 合并执行  
- CI 是否加 `harness_task_validate --all-active`：**R1 合并后**再议（先本地 + 22 人工）

---

## 7. 日常纪律（现在就能做 · 无需等 R1）

1. **新建 task** 一律从最新 `TASK_TEMPLATE.md` 复制（含 O1–O3）。  
2. 触达 `api/` → 默认 `test_strategy: recommended` 或 `required`。  
3. 纯文档 task → `not_applicable` + 一行 note。  

---

## 8. 与后续「通用 harness-spec 库」关系

| 阶段 | 关系 |
|------|------|
| R1–R3 | 在本仓 `tools/` 验证规则与 UX |
| 未来库化 | 将 validate/status 迁入 `ink-harness` core；本仓改 pip 依赖 |

分析稿（非 Git · `docs/diary/tmp/`）：`2026-05-30-InkHarness-universal-library-feasibility-v2.md`。

---

## 9. 关联文档

| 文档 | 路径 |
|------|------|
| OpenSpec vs Harness 差异 + O 清单 | `docs/diary/tmp/2026-05-30-Harness-vs-OpenSpec-diff-and-optimization.md`（tmp） |
| TDD 架构评估 | `docs/diary/tmp/2026-05-30-backend-TDD-architecture-assessment.md`（tmp） |
| 通用库 v2 | `docs/diary/tmp/2026-05-30-InkHarness-universal-library-feasibility-v2.md`（tmp） |
| Task 模板（O1–O3 真值） | [`docs/tasks/templates/TASK_TEMPLATE.md`](../../tasks/templates/TASK_TEMPLATE.md) |
| TDD 口径（README） | [`docs/tasks/README.md`](../../tasks/README.md) §本仓 TDD 实践口径 |

---

## 10. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-30 | 初版：O1–O3 完成态；Sprint A/B/C；O4 与 TDD P0 合并 |
| 2026-05-30 | 自 `docs/diary/tmp/` 迁入 `docs/spec/governance/`；对齐 Loop R1–R3 与 RECENT §0.6 |
