# Task Audit · R1 · `kimi_harness_pilot_recentsync_v1`

> **帽**: 22-task-audit · **AUDIT_ROUND**: R1 · **日期**: 2026-06-08
> **task_path**: `docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md`
> **explore_snapshot**: `docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md`

---

## 元信息表

| 字段 | 值 |
| --- | --- |
| **task_slug** | `kimi_harness_pilot_recentsync_v1` |
| **orchestration** | Kimi Code · Lead 主会话 + 串行 `Agent()` |
| **test_strategy** | `not_applicable` |
| **audit_profile** | `post_close` |
| **human_gate** | HG-TASK-DRAFT: `approved` · HG-KIMI-PILOT-EXEC: `approved` |
| **harness_human_gate_check** | `exit 0` |
| **harness_task_validate** | `OK` |

---

## 审查结论摘要

- **HG-TASK-DRAFT**: ✅ `approved`（task 正文 + PROMPT 已人扫）
- **HG-KIMI-PILOT-EXEC**: ✅ `approved`（T1 执行链开干前人签）
- **范围核对（A/B）**: ✅ A 段 5 项清晰；B 段上限 10 文件约束明确
- **failure_paths F1–F4**: ✅ 均含 Scenario ID，通过 `harness_task_validate`
- **OpenSpec×TDD 机械校验**: ✅ `OK`
- **阻塞项**: 无
- **结论**: **建议 30 开工**

---

## 范围核对（A/B）

### A 段 · RECENT §1.2 同步（必做）

| ID | 交付 | 核对 | 说明 |
| --- | --- | --- | --- |
| A-1 | MANIFEST 链至 `done/` | ✅ | explore 确认 RECENT L147 仍写 `active/`，须改 `done/` |
| A-2 | P0–P3 子批表：状态 done + PR 号 | ✅ | RECENT L153–155 过期；P1「脚手架」/P2P3「pending」须更新 |
| A-3 | 执行器行注明治理线 CLOSE | ✅ | RECENT L148 未反映 P1–P3 已完成 |
| A-4 | 删除过期表述 | ✅ | 「分支已开 / pending」等须删 |
| A-5 | §1.2 段首注明 docs-noise CLOSE | ✅ | 当前段首无 CLOSE 声明 |

**A 段清晰度**: 5 项均指向单一文件 `docs/tasks/RECENT_TASK_SCHEDULE.md`，改动点明确，无歧义。

### B 段 · done/ 状态卫生（有条件 · 上限 10 文件）

| ID | 交付 | 核对 | 说明 |
| --- | --- | --- | --- |
| B-1 | explore 用 `rg` 扫描候选 | ✅ | explore 报告已产出完整清单 |
| B-2 | 优先 5 个 gov-docs-noise 文件格式统一 | ✅ | 清单固定：P0/P1/P2/P3/MANIFEST |
| B-3 | 其余候选最多再修 5 个；无合格则跳过 | ✅ | 明确上限 10 文件；explore 发现 11 候选，须按优先级取舍 |

**B 段上限检查**: B-2 固定 5 文件 + B-3 最多 5 文件 = **≤10 文件**。explore 报告建议 legacy 6 个中选 0~5 个，不超限。

**B 段清晰度**: ✅ 范围清晰、可执行、有明确停止条件。

---

## failure_paths 检查（F1–F4）

| # | Scenario ID | 触发 | 行为 | validate |
| --- | --- | --- | --- | --- |
| F1 | `fp-kimi-pilot-scope-drift` | 深读 `docs/spec/v3-agent/**` 或改 `api/` | 禁止；explore/30 须停并回报 Lead | ✅ |
| F2 | `fp-kimi-pilot-readorder` | RECENT 与 MANIFEST 仍指向 `active/` 路径 | 30 帽必须修正为 `done/` | ✅ |
| F3 | `fp-kimi-pilot-over-edit` | B 段修改超过 10 个 `done/` 文件 | 禁止；仅 explore 清单内文件 | ✅ |
| F4 | `fp-kimi-subagent-git` | subagent 尝试 `git commit` | 禁止；仅 Lead commit | ✅ |

- **Scenario ID**: 4 条均含唯一 Scenario ID，符合 `harness_task_validate` 要求。
- **触发→行为→可重试→用户可见**: 触发与行为均明确；F1/F3/F4 为硬禁止（不可重试），F2 为修正指令（可重试）。
- **与 explore 对照**: F2 直接对应 explore 发现的 A-1 问题（MANIFEST 链 `active/`），闭环一致。

---

## 理论对齐检查表（P0 · R1 硬门禁）

### §3.1 任务单最小字段

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 头部 Harness 元信息表：`test_strategy` 三选一 | ✅ `not_applicable` |
| 2 | `not_applicable` 时 `test_strategy_note` 非空 | ✅ "纯 docs 排期/元数据；无 `api/` / 契约 / workflow 变更" |
| 3 | `failure_paths` ≥1 行（触发→行为→可重试→用户可见） | ✅ 4 行 |
| 4 | **非范围** 独立小节非空 | ✅ 4 条明确禁止 |
| 5 | **验收标准** 含 **合并前必绿** 条 | ✅ "CI Required 全绿" |
| 6 | （P1 抽检）`semi_auto` + `audit_profile` 已填 | ✅ `false` / `post_close` |

### §3.2 合并前 CI 验收条

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 验收含：`PR 上 pytest workflow 全绿` + 本地等价命令 | ✅ "单 PR · docs-only · CI Required 全绿" |
| 2 | 40 自检 / PR 链接可核对（终轮 22 不得无证明签收） | ⏳ 终轮 CLOSE 时核验 |

### §Blocking · 高敏须人判断

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 若触达 Blocking 任一行 → 上表已核对，缺项 **阻塞** | ✅ 未触达 Blocking（纯 docs，无 api/ 契约变更） |

### §3.3 独立复检（50）触发

| 变更类型 | `test_strategy` | 50 |
|----------|-----------------|-----|
| 纯 `docs/`、索引、无行为 | `not_applicable` | 可选 |

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型匹配 | ✅ |
| 2 | `required` 且涉 `api/`/契约 → 关账前 **50 已落盘** 或显式阻塞 | N/A（`not_applicable`） |

### OpenSpec × TDD 勾选项（P0 · R1）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型一致（触达 `api/` 时 **非** `not_applicable`） | ✅ 纯 docs，未触达 `api/` |
| 2 | §行为变更 Delta 已填 **或** 显式「无」 | ✅ 非范围已声明「无行为变更」 |
| 3 | `failure_paths` 含 **Scenario ID** 列且非空 | ✅ 4 条均含 |
| 4 | 验收含 **合并前 pytest** 条（或 task 模板等价表述） | ✅ "CI Required 全绿" |

---

## 阻塞 / 非阻塞

**无阻塞项**。task 字段完整、范围清晰、failure_paths 合规、human_gate 已批。

---

## 是否建议 30 开工

**建议开工**。

理由：
1. HG-TASK-DRAFT / HG-KIMI-PILOT-EXEC 双闸均 `approved`
2. A/B 范围清晰、可执行、有明确上限
3. failure_paths F1–F4 均含 Scenario ID，通过 `task_validate`
4. 纯 docs 变更，`test_strategy=not_applicable` 合理，不触发 50 强制要求
5. explore 报告已提供完整改动清单，30 可直接执行

---

## 签收 / 关闭

- **R1 状态**: `approved` → 建议进入 30 执行帽
- **终轮条件**: 30 执行完成 + 40 自检全绿 + CI Required 全绿 + diary 落盘后，触发 R2/CLOSE 审查

---

## 下一棒可复制 Prompt

```text
【角色】Harness 30 执行帽 · Kimi Code 试点 T1
【task】docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
【canonical 读序】
1. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
2. docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md
3. docs/harness/reviews/by-task/kimi-harness-recentsync/task_governance_kimi_harness_pilot_recentsync_v1_audit_R1_20250608.md
【forbidden】
docs/spec/v3-agent/** · api/** · tests/** · .github/workflows/** · 改 task 正文 · git commit
【你必须完成】
1. A-1～A-5：修正 RECENT_TASK_SCHEDULE.md §1.2（MANIFEST 链 done/、P0–P3 状态 done+PR、执行器行注明 CLOSE、删过期表述、段首加 CLOSE 标注）
2. B-2：统一 5 个 gov-docs-noise done task 状态行格式（优先简化为 done(YYYY-MM-DD · PR #N @ commit)）
3. B-3：若 legacy 候选有合格项，最多再修 5 个；超出则跳过并在 40 自检说明
4. 总修改文件 ≤10（RECENT 1 个 + done/ 最多 9 个）
5. 回报格式：Status / Deliverables / Blockers / Judgment（各≤10行）
【额外指令】
- 不要 git commit（Lead 负责）
- wall-clock >10 min 须停并向 Lead 汇报
- 禁止贴 subagent 全文
```
