# Agent 执行任务 KPI 评分规则（v1.2）

> **状态**：`active`（2026-05-31 定稿）  
> **用途**：00 总调度帽、关账轮、维护者抽检时，对 **HatInstance（帽实例）** 打分并汇总 **Task KPI%**。  
> **落盘**：task 正文 **`### KPI（00）`** 表；公式与细则 **以本文件为真值**（不写死在 00 对话行）。  
> **关联**：[`../prompts/00-orchestrator.md`](../prompts/00-orchestrator.md)、[`../HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) §5.7–§5.8、[`../prompts/HANDOFF_CLOSE_TRACE.md`](../prompts/HANDOFF_CLOSE_TRACE.md)。

---

## 1. 术语表

| 术语 | 含义 |
|------|------|
| **hat_code** | Harness 帽编号：`00` 总调度；`10` 需求；`20` 规格短评；`22` 任务审核；`30` 执行；`40` 自检；`50` 独立复检/全局验收；`CLOSE` 关账 |
| **round** | 同帽多轮：`R1`、`R2`、`close` 等 |
| **agent_mode** | `main_chat`（总 Chat / 00）\| `task_subagent`（Cursor `Task` 派发） |
| **HatInstance** | 本 task 上某帽的 **一次执行**（KPI 表一行） |
| **50** | **帽子** `50-independent-reinspect`（独立复检），**不是**测试套件编号 |
| **返工** | **外部打回**：22 要求 R+1、50 fail 打回 30、人明确要求返工；**不含** 30 内自我修正且未落审查/复检 |
| **CI 绿** | 仅 task 列出的 **关联子仓** + workflow（对齐根 `AGENTS.md` §8） |
| **J-exp** | `experience_capture` 档位判断是否合理 |
| **J-gate** | `human_gate` / 阻塞判断 |
| **J-scope** | 范围、`freeze_id`、静默扩 scope |
| **J-evidence** | 无证据却 pass |
| **J-refuse** | 该拒开工未拒 / 该停未停 |
| **judgment_notes** | 任一大维或 J 为 warn/fail 时 **必填** 的原因说明 |

---

## 2. 大维权重（v1.2 · 合计 100%）

| 大维 | 权重 | 聚合方式（Task 级） |
|------|------|---------------------|
| **D1** 交付 | 20% | 各帽实例 **算术平均** |
| **D2** 判断 | 30% | 各帽实例 **最小值（min）** |
| **D3** 上下文 | 15% | **平均** |
| **D4** 合规 | 15% | **min** |
| **D5** 结果 | 20% | **min** |

**D2 子项权重（合成单帽 D2 前，各子项 100/60/0）**

| 子项 | 占 Task 总权重 |
|------|----------------|
| J-exp | 4% |
| J-gate | 5% |
| J-scope | 5% |
| J-evidence | 6% |
| J-refuse | 10% |

**单帽 D2 规则**：任一 J 子项 **fail** → 该帽 **D2 = fail（0）**；否则按子项加权平均后映射：≥85→pass(100)；60–84→warn(60)；<60→fail(0)。

---

## 3. 评分规则表（pass=100 · warn=60 · fail=0）

### D1 交付（20%）

| 等级 | 条件 |
|------|------|
| pass | 下列 checklist **全部满足**（仅勾选本 task **已执行** 的帽所要求项） |
| warn | **缺 1 项** |
| fail | **缺 ≥2 项** |

**checklist**

- [ ] task 路径有效，验收节可读  
- [ ] 若走过 **40**：`### 自检结论（执行者）` 已回填  
- [ ] 若走过 **22**：`reviews/task_*_audit_*.md` 存在  
- [ ] 若走过 **50**：`reinspect_results/` 或 50 报告路径存在  
- [ ] 该帽若要求 invoke：对应 `invokes/...` 已落盘  

### D2 判断（30%）

| 等级 | 条件 |
|------|------|
| pass | J 子项 **无 fail**；warn ≤1 |
| warn | 无 fail；warn **2 项** |
| fail | **任一** J fail **或** warn ≥3 |

**J 子项判定要点（附录 A）**

| 子项 | pass | warn | fail |
|------|------|------|------|
| J-exp | 与 task 档位一致 | 建议升级/降级但理由弱 | 明显应 `required` 仍 n/a 或相反 |
| J-gate | 闸状态判断正确 | 漏标建议闸 | 代签 approved / 误闯 pending 闸 |
| J-scope | 未静默扩 scope | 边界模糊已提示 | 明显扩 scope 或漏升 freeze |
| J-evidence | 证据可定位 | 证据偏弱但已声明 | 无证据却 pass |
| J-refuse | 拒/停正确 | — | 该拒未拒或该停未停 |

### D3 上下文（15%）

| 等级 | 条件 |
|------|------|
| pass | 三项全满足 |
| warn | **1 项**不满足 |
| fail | **≥2 项**不满足 |

1. 父→子 Handoff（00→Task）正文 **≤500 字**（路径列表不计入）  
2. **未**粘贴总 Chat / 30 执行过程长文  
3. `worktree_root` / cwd 与 task、invoke **一致**（若已声明 worktree）  

### D4 合规（15%）

| 等级 | 条件 |
|------|------|
| pass | 无严重违规；须 `approved` 的 gate 已 approved |
| warn | **1 处**轻微违规（缺 invoke 元信息、commit 未含 slug 等） |
| fail | **代签 approved**、跳过 pending 闸开工、在 `main` 上 `semi_auto` 链式提交 |

### D5 结果（20%）

| 等级 | 条件 |
|------|------|
| pass | 返工 **0**；关联子仓 **必绿 CI 全绿**；若已跑 **50**：建议合并且无阻塞 |
| warn | 返工 **1**；或 CI 有 **与本 task 无关** 的失败（须在 notes 注明） |
| fail | 返工 **≥2**；或 **本 task 关键** CI 红；或 **50 阻塞合并** |

**未跑 50 的帽实例**：D5 填 **`—`**，不参与该帽 D5；Task 级 D5 仅对已有 D5 分数的帽取 min。

---

## 4. Task 汇总

### 4.1 公式

```text
Task_KPI% = D1×20% + D2×30% + D3×15% + D4×15% + D5×20%
（各大维得分已按 §2 聚合）
```

### 4.2 状态（语义）

| 状态 | 规则 |
|------|------|
| **blocked** | **任一** HatInstance 的 **D2=fail** 或 **D5=fail**（v1.2 收紧；覆盖 KPI%） |
| **pass** | 非 blocked 且 KPI% **≥ 80** |
| **warn** | 非 blocked 且 **60 ≤ KPI% < 80** |
| **fail** | 非 blocked 且 KPI% **< 60** |

**关账硬规则（并行）**：`human_gate` pending、50 书面阻塞、必绿 CI 红 → **不得关账**，即使 KPI%≥80。

### 4.3 task 落盘表（模板）

```markdown
### KPI（00）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: {KPI%} · **状态**: pass|warn|fail|blocked · **帽**: …

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
|----------|-------|------------|----|----|----|----|-----|----------------|
| … | … | … | … | … | … | … | … | … |

**blocked 原因**：（若有）
```

**judgment_notes**：任一大维或 J 为 warn/fail → **必填**。

---

## 5. 版本迁移（v1.1 → v1.2）

| 变更项 | v1.1 | v1.2 |
|--------|------|------|
| D1 / D5 权重 | 25% / 15% | **20% / 20%** |
| D2 子项 | 均分 6% | **J-refuse 10%**，其余见 §2 |
| blocked | 仅 22/50 的 D2/D5 fail | **任一帽** D2 或 D5 fail |
| Task 维聚合 | 全算术平均 | **D2/D4/D5=min**；D1/D3=平均 |
| Task 状态阈值 | 仅 blocked 覆盖 | **+ pass≥80 / warn 60–79 / fail<60** |
| 经验归纳 | 未纳入 | **`experience_capture`** + Judgment（**无 60 帽**） |

**存量 task 适配（1 条）**

- **已关账、无 `### KPI（00）`**：**不强制重算**；新关账或 **`00` 复盘中** 的任务从 v1.2 起算。  
- **进行中 task**：在下次 **50 或 CLOSE** 前补写 KPI 表；`rubric` 标 `KPI_RUBRIC_v1_2`。  
- 若需对比历史，在 notes 注明「按 v1.1 估算，仅供参考」，**勿**与 v1.2 百分比直接排名。

---

## 6. 完整计算示例（虚构 task · 含 30/40/50）

**背景**：`task_demo_api_fix_v1` · 已跑 30→40→50 · 50 建议合并，J-exp 建议升 `experience_capture: required`。

### 6.1 HatInstance 得分

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
|----------|-------|------------|----|----|----|----|-----|----------------|
| 30 | R1 | task_subagent | 100 | 100 | 100 | 100 | — | — |
| 40 | R1 | task_subagent | 100 | 100 | 100 | 100 | — | — |
| 50 | close | task_subagent | 100 | 60 | 100 | 100 | 100 | J-exp warn: 同类排障将复现，建议 task 升 required；见 reinspect §3 |

**50 的 D2=60 推导**：J-exp warn（+ 其余 J pass）→ D2 整体 warn → 60。

### 6.2 Task 各大维聚合

| 大维 | 计算 | 得分 |
|------|------|------|
| D1 | avg(100,100,100) | **100** |
| D2 | min(100,100,60) | **60** |
| D3 | avg(100,100,100) | **100** |
| D4 | min(100,100,100) | **100** |
| D5 | min(—,—,100) → 仅 50 有分 | **100** |

### 6.3 Task_KPI% 与状态

```text
Task_KPI% = 100×20% + 60×30% + 100×15% + 100×15% + 100×20%
          = 20 + 18 + 15 + 15 + 20 = 88%

blocked：无（50 的 D2 为 warn 非 fail）
状态：pass（88 ≥ 80）
```

### 6.4 与 `experience_capture` 联动

- task 原为 `recommended` → 50 + Judgment 建议升 **required** → **22 或人** 改 task 元信息后再关账；CLOSE 核对 [`HANDOFF_CLOSE_TRACE.md`](../prompts/HANDOFF_CLOSE_TRACE.md) §6。

### 6.5 反例（blocked）

若 50 的 **D5=fail**（阻塞合并）：

```text
blocked = 是（50 · D5 fail）
→ 忽略 KPI%，不得关账，须回 30
```

---

## 7. 维护者 rsync（子仓执行真值）

工作区改本文件及 `00` / 模板后，在 **`Projects/` 根** 按需同步至 `ai-ink-brain-api-python/docs/harness/`（**禁止**整目录覆盖）。清单见 [`RSYNC_PROMPTS_TO_API_PYTHON.md`](RSYNC_PROMPTS_TO_API_PYTHON.md)。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v1.2：初版定稿 + §6 演算示例 + §5 迁移 |

## 给 Cursor

`KPI_RUBRIC_v1_2`、`00-orchestrator`、`HatInstance`、`judgment_notes`、`blocked`、`experience_capture`、`D1`、`D2`、`J-exp`、`J-refuse`
