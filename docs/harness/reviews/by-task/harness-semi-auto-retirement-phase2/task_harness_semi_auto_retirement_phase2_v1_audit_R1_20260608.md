# 22 R1 · Task Audit · `harness_semi_auto_retirement_phase2_v1`

> **日期**：2026-06-08  
> **审查者**：Harness 22 · harness-22-audit  
> **task_path**：[`docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md`](../../../tasks/active/task_harness_semi_auto_retirement_phase2_v1.md)  
> **task_slug**：`harness-semi-auto-retirement-phase2`  
> **Round**：T1 · R1  
> **audit_profile**：`post_close`（R1 放行 30；终轮签收在 40 + CLOSE 后）  
> **invoke_snapshot**：[`explore_semi_auto_retirement_phase2_gap.md`](../../invokes/by-task/harness-semi-auto-retirement-phase2/explore_semi_auto_retirement_phase2_gap.md)

---

## 审查结论摘要

**R1 PASS · 零阻塞**。`human_gate` 双闸已批；`harness_task_validate.py` **OK**。P2-1～P2-8 范围清晰、与 explore 差分一致（均未交付属预期）；deprecated 策略（横幅 + pointer、不删全文）可执行。**建议 30 帽开工**。

---

## 理论对齐检查表（P0 · 已核对）

### §3.1 任务单最小字段

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 头部 Harness 元信息表：`test_strategy` 三选一 | ✅ `not_applicable` |
| 2 | `not_applicable` 时 `test_strategy_note` 非空 | ✅ |
| 3 | `failure_paths` ≥1 行（含 Scenario ID） | ✅ F1–F4 |
| 4 | 非范围独立小节非空 | ✅ |
| 5 | 验收含合并前必绿条 | ✅ 「单 PR docs-only · CI Required 全绿」 |
| 6 | `semi_auto` + `audit_profile` 已填 | ✅ `false` · `post_close` |

### §3.2 合并前 CI 验收条

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 验收含 PR CI 全绿 | ✅ docs-only · 40 跳过 pytest |
| 2 | 40 自检 / PR 可核对 | ⏳ 关账前 40 落盘 |

### §Blocking · 高敏须人判断

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 触达 Blocking 行 | ✅ 未触达 `api/` / manifest env |

### §3.3 独立复检（50）触发

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型匹配 | ✅ 纯 docs · `not_applicable` |
| 2 | `required` 且涉 api/ → 50 | N/A · task/PROMPT 明示跳过 50 |

### OpenSpec × TDD（机械校验）

```bash
python tools/harness_human_gate_check.py --task docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md  # OK
python tools/harness_task_validate.py docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md          # OK
```

---

## 范围核对表（P2-1～P2-8）

| ID | 交付目标 | 目标文件 | 当前态（explore） | R1 判定 |
| --- | --- | --- | --- | --- |
| **P2-1** | SPEC 状态 → **全面生效**；§0/§1 完成态（A+B 已 CLOSE） | `docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md` | 状态行仍「待 B 轨」；§0/§1 缺口段过时 | ✅ 范围明确 · 30 执行 |
| **P2-2** | `HARNESS_V2_PLAN` §5.6 + 关账常模：`semi_auto` **deprecated** | `docs/harness/HARNESS_V2_PLAN.md` | §5.6 为「过渡/废弃」无 deprecated 关键字；§0.2 仍链 semi_auto | ✅ 范围明确 · 见注① |
| **P2-3** | `HANDOFF_SEMI_AUTO` 文首 **DEPRECATED** + 链式替代读序 | `docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md` | 无 DEPRECATED · 无 chain PROMPT pointer | ✅ 范围明确 · 30 执行 |
| **P2-4** | `05` deprecated；`06` 默认读链式规则 | `.cursor/rules/05-harness-semi-auto.mdc` · `06-harness-in-repo.mdc` | `05` alwaysApply 无 deprecated；`06` 仍链 05 为细则 | ✅ 范围明确 · 保留文件+横幅 |
| **P2-5** | `TASK_TEMPLATE`：`semi_auto` deprecated；新建须 `orchestration` + PROMPT | `docs/tasks/templates/TASK_TEMPLATE.md` | G1 部分完成（orchestration 已有；semi_auto 未标 deprecated） | ✅ 增量小 |
| **P2-6** | README · AGENTS · RECENT §0.0 + §1.4 同步 | 多文件 + `RECENT_TASK_SCHEDULE.md` | §1.4 结构 OK；§0.0 仍锚 `semi_auto: true` 常模 | ✅ 范围明确 · RECENT 为 §0.0 真值 |
| **P2-7** | governance / prompts README Phase 2 索引 | 两 README | 骨架有 · 关账态缺 | ✅ 范围明确 |
| **P2-8** | MANIFEST Phase 2 → done（**CLOSE 后**） | `docs/tasks/done/task_harness_semi_auto_retirement_manifest_v1.md` | `in_progress` · 关账前预期 | ✅ 须 40 后 CLOSE 写入 |

> **注①**：task P2-2 写「§0.0 关账常模表」物理落点在 **RECENT §0.0**（explore 已确认）；P2-6 覆盖 RECENT 改写。30 须同时改 `HARNESS_V2_PLAN` §5.6/§0.2 与 RECENT §0.0，**非阻塞歧义**。

---

## failure_paths F1–F4 可执行性

| ID | Scenario ID | 触发 | 行为 | 可执行性 | 40/30 验证手段 |
| --- | --- | --- | --- | --- | --- |
| **F1** | `fp-p2-scope-drift` | 30 改 `api/` 或 workflow | **禁止** | ✅ | PROMPT §4 forbidden；非范围；PR diff 目检 |
| **F2** | `fp-p2-delete-semi-auto-history` | 未留 deprecated 即删 semi_auto / HANDOFF 全文 | **禁止** | ✅ | 40 `rg DEPRECATED` + 文件仍存在 |
| **F3** | `fp-p2-premature-rule-removal` | 未更新链式读序即移除 `05` | **禁止**；须 deprecated + pointer | ✅ | 40 查 `05`/`06` 横幅与链 SPEC/PROMPT 链 |
| **F4** | `fp-p2-spec-stale-gate` | SPEC 仍写「待 B 轨 CLOSE」 | 40 **fail** | ✅ | PROMPT §5：`rg '待 B 轨' SPEC` 应无匹配 |

**结论**：四路径均有明确触发、行为与验证命令；与 PROMPT §4–§5、T1 纪律 §6 对齐，**可执行**。

---

## deprecated 策略可执行性

| 策略要素 | task / PROMPT 要求 | R1 判定 |
| --- | --- | --- |
| 不删历史 | 非范围禁止删 invokes/reviews/done；F2/F3 硬禁 | ✅ |
| DEPRECATED 横幅 | HANDOFF + `05` 文首可见说明 | ✅ 文案方向明确 |
| 链式替代 pointer | `PROMPT_*_chain_serial_*` · `HANDOFF_CLOSE_TRACE` · Chain SPEC | ✅ SPEC §4 已有索引 |
| 保留对照表 | HARNESS_V2_PLAN §5.6 不删历史正文 | ✅ 与 A 轨一致 |
| Cursor 注入 | `05` 可保留 `alwaysApply` 但须 deprecated 声明（explore 建议降权；task 未强制移除） | ✅ 30 酌情：文首 deprecated ≥ 移除 alwaysApply |

---

## 阻塞 / 非阻塞

### 阻塞项

**无**。

### 非阻塞建议（交 30，不必回填 task）

1. P2-2「§0.0」→ 执行时以 **RECENT §0.0** 为主、`HARNESS_V2_PLAN` §0.2/§5.6 为辅（见范围表注①）。
2. `05-harness-semi-auto.mdc`：优先文首 **DEPRECATED** + 链式 pointer；是否改 `alwaysApply` 由 30 按 Cursor 注入体验决定，**不阻塞 R1**。
3. P2-8 / RECENT §1.4 / task `git mv`：**仅 CLOSE 阶段**（40 通过后），30 单 PR 可不写 MANIFEST done 行。

---

## 30 帽回填清单（逐条可勾选）

- [ ] **P0** P2-1：SPEC 状态改「全面生效」；§0 A+B 已 CLOSE；§1 缺口段更新（消「待 B 轨」「→ B 轨」）
- [ ] **P0** P2-6：RECENT §0.0 关账链改 **`orchestration` 链式常模**；去「`semi_auto: true` 时」表头
- [ ] **P1** P2-3：`HANDOFF_SEMI_AUTO.md` 文首 DEPRECATED + `PROMPT_*_chain_serial_*` / `HANDOFF_CLOSE_TRACE` pointer
- [ ] **P1** P2-4：`05` deprecated 横幅；`06` 默认读 Chain SPEC + `06-harness-in-repo`（非 05 为首选）
- [ ] **P1** P2-2：`HARNESS_V2_PLAN` §5.6 增 **deprecated** 注记；§0.2 链式为默认
- [ ] **P2** P2-5：`TASK_TEMPLATE` `semi_auto` 行标 **deprecated**；真值链改链 PROMPT
- [ ] **P2** P2-6：`AGENTS.md` · `docs/tasks/README.md` Harness 指针去「半自动通则」为默认
- [ ] **P2** P2-7：`docs/spec/governance/README.md` · `docs/harness/prompts/README.md` Phase 2 关账行
- [ ] **P3 CLOSE** P2-8：MANIFEST Phase 2 → done；RECENT §1.4 CLOSE；`git mv` task → `done/`
- [ ] 跑通：`python tools/harness_task_validate.py docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md` → OK

---

## 是否建议执行帽开工

**是**。R1 无阻塞；`HG-TASK-DRAFT` · `HG-CHAIN-P2-EXEC` 均已 `approved`；explore 差分已锁定改动面。

---

## 签收 / 关闭

| 项 | 结论 |
| --- | --- |
| **R1 签收** | **通过** — 30 可执行 P2-1～P2-8（P2-8 关账阶段） |
| **audit_profile `post_close`** | 本文件 **非** task 终轮关闭点；**终轮签收**须在 **40 自检通过 + CLOSE（PR merge + task 归档）** 后由 Lead 更新 task 头 `done` 并对齐 MANIFEST |
| **须继续的条件** | 40 若 F4 触发（SPEC 仍「待 B 轨」）→ 30 回补 SPEC 后重跑 40 |
| **50** | 跳过（`not_applicable` · task/PROMPT 明示） |

---

## 下一棒可复制 Prompt（30 帽）

```text
你 = Harness 30 · 纯 docs · Phase 2 semi_auto 物理退场。

【读序】
1. docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md
2. docs/harness/reviews/by-task/harness-semi-auto-retirement-phase2/task_harness_semi_auto_retirement_phase2_v1_audit_R1_20260608.md
3. docs/harness/invokes/by-task/harness-semi-auto-retirement-phase2/explore_semi_auto_retirement_phase2_gap.md
4. docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_semi-auto-retirement-phase2_zh.md §4

【执行】task §范围 P2-1～P2-7（P2-8 留 CLOSE）；对照 R1「30 帽回填清单」逐条勾选

【forbidden】api/** · tests/** · .github/** · 删 HANDOFF_SEMI_AUTO/05 全文 · 删 invokes/reviews/done 历史 · git commit（Lead 负责）

【必须】DEPRECATED 横幅 + 链式 pointer · SPEC 全面生效 · RECENT §0.0 链式常模 · harness_task_validate → OK

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | R1 · PASS · 零阻塞 · 放行 30 |
