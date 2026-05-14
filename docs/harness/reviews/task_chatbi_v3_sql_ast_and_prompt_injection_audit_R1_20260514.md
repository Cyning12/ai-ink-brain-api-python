# 任务审核 · ChatBI V3 P1-1 / P1-2（合并 R1）

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `docs/tasks/active/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（P1-1）<br>`docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（P1-2） |
| **关联 L1 SPEC / 总规** | `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` §2、§3<br>`docs/spec/v3-agent/SPEC-ChatBI-V3-Logging-Trace.md`<br>日志键与 OpenItems：`docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` **§1.6**（`### 1.6 结构化日志`） |
| **轮次** | **R1**（首轮） |
| **审查日期** | 2026-05-14 |
| **上一轮审查** | 无 |
| **CI 对齐（执行 / 自检）** | `pytest tests -m "not intent_eval and not intent_benchmark"`（与 `.github/workflows/pytest.yml` 一致） |

---

## 审查结论摘要

两条 task 头部均具备 **`test_strategy: required`** 及 **`test_strategy_note`**（与工作区 [`HARNESS_V2_PLAN.md`](../../../../docs/harness/HARNESS_V2_PLAN.md) **§5.1** 精神一致：关键语义须由 **可失败** 的 `pytest` 钉住，并与 PR 可复现顺序/负例叙述一致）、**`freeze_id`**、**`gates_before_code`**、**`failure_paths`** 表、**必读列表**、**拒开工条件**与 **§验收标准** 中的 **可命令断言**（`pytest`、`CHATBI_JSON_LOG=1` 下 JSON 结构、顺序、正/负例数量下限等）。对照 L1：`SPEC-ChatBI-V3-Security.md` §2/§3 与 Identity-Access-OpenItems §1.6 中 `sql_gate_deny` / `rule` 等表述，与 P1-1 日志验收、P1-2 新增 `prompt_guard_*` 键的「不打架」要求 **可核对**，无文档层硬冲突。

**总判**：从 **Harness 任务单可执行性** 维度，**本轮无阻塞项**；允许进入 **执行帽** 开工（仍须遵守各 task **拒开工条件** 与 `gates_before_code`）。

---

## 阻塞项

（本轮 **无**。）

---

## 非阻塞建议（任务帽 / 执行帽可选优化）

1. **P1-1 · `### 给执行帽的必读列表` 第 3 条**：现写「`SPEC-ChatBI-V3-Logging-Trace.md` + OpenItems **§1.6**」未给出 OpenItems **文件路径**；建议与 **P1-2** 对齐，显式写 `docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` **`### 1.6`**，减少执行帽误读为其他 OpenItems。
2. **P1-1 · `### failure_paths`（FP-C）与 `## 5. 验收标准`**：FP-C（闸内未捕获错误 → **5xx**、不执行 SQL）在验收勾选表中 **未**要求专用 pytest；若希望与 FP-A/B 对称钉死，可在 **§5** 增一条可选验收或注明「由现有全局异常处理 + 抽检覆盖」。
3. **P1-2 · `### 待确认问题`**：golden JSON 路径由执行 PR 在 **§5 实现备忘** 写死即可；任务帽若希望减少执行期往返，可预先在备忘表留 **占位键**（仍属优化，非必须）。

---

## 需任务帽回填清单

（**无强制回填**；若采纳上文非阻塞建议，请按下表位置增量编辑。）

| # | 建议动作 | 目标 task / 小节标题 |
|---|----------|----------------------|
| S1 | 在必读列表第 3 条补全 OpenItems **文件相对路径**及小节锚点 | P1-1 → **`### 给执行帽的必读列表`** |
| S2 | （可选）为 FP-C 增加验收勾选或「非本 task 专测」说明 | P1-1 → **`## 5. 验收标准`** 或 **`### failure_paths`** 脚注 |

---

## 是否建议执行帽开工

**建议开工**：两条 task 的 **`failure_paths`**、**`test_strategy`（required）**、**验收标准** 与 **CI 命令** 已形成可观测、可机械验证闭环；**禁止**在仍有 **本文档级阻塞** 时强推编码的前提已满足。

**给下一棒（文内副本）**：无阻塞 → 可交 **执行帽**；合并前跑通 `pytest tests -m "not intent_eval and not intent_benchmark"`；遵守 **`gates_before_code`**（`failure_paths`、`freeze_id`、必读列表）；`required` 语义下关键用例须在 PR 中满足 **可失败复现**（见各 task **`test_strategy_note`**）。

---

## 签收 / 关闭

本轮为 **R1 契约审查**，**不对** implementation 终态签收，**不**将 task 头部 `状态` 视为可改为 `done`。任务正式 **签收 / 关闭** 须在 **终轮审查文档（如 R2+）** 与 **自检帽回填**、**代码合并** 完成后，由后续轮次 **任务审核** 落盘声明，并与 task **`done`** 对齐。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | R1：合并审查 P1-1 SQL AST gate + P1-2 Prompt guard PoC；无阻塞；建议可选文档对齐 |
