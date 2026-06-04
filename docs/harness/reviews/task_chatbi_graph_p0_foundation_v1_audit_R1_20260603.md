# 任务审核：ChatBI Graph P0 地基 — R1

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_path** | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |
| **audit_round** | R1（首轮 · `post_close` 闸 1） |
| **关联上一轮** | 无 |
| **关联 SPEC** | `docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md` · `docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md` · `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` · `docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md` |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/invoke_20260603_22_chatbi-graph-p0-foundation-v1.md` |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **test_strategy** | `required` |
| **audit_profile** | `post_close` |
| **reviewer** | Agent（22 帽） |
| **date** | 2026-06-03 |
| **机械校验** | `python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` → **exit 1** · `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` → **FAIL** |

---

## 审查结论摘要

task 草案与 Plan SPEC **§4A** / 冻结决策 **D-1～D-5** 在背景、五步范围、非范围、P0 硬约束上 **语义对齐**；`test_strategy: required` 与涉 `api/` 新路由匹配；FP-1～4 四条失败语义 **内容可操作**，但 **Harness 机械校验未过**；**SDD §10 待确认清单未清零**（含 P0 必冻 **Q-8**）；**HG-TASK-DRAFT** 仍为 `pending`。

**结论：有阻塞 — 不可进入 30 执行帽**；须 **10 需求帽** 按下方清单回填 task 后，人签 `HG-TASK-DRAFT` → **22 R2** 复审。

---

## 理论对齐检查表（P0）

### §3.1 任务单最小字段

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 头部 `test_strategy` 三选一 | ☑ `required` |
| 2 | `not_applicable` 时 `test_strategy_note` | N/A |
| 3 | `failure_paths` ≥1 行（机械 validate） | ☐ **FAIL** — 小节标题为 `failure_paths`，validate 期望 **`失败路径`** 且表格式 |
| 4 | **非范围** 独立小节非空 | ☑ §3 |
| 5 | 验收含 **合并前必绿** pytest | ☐ **部分** — §6 有条目但缺 **PR workflow** 表述；validate 因标题非精确 `验收标准` 未识别 |
| 6 | `semi_auto` + `audit_profile` | ☑ |

### §3.2 合并前 CI 验收条

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | PR pytest workflow 全绿 + 本地等价命令 | ☐ 本地命令在 §6/§4 有述；**缺**「PR 上 pytest workflow 全绿」于 **验收标准** 小节 |
| 2 | 40 自检 / PR 链接可核对（终轮） | ☐ 待 30/40（本 R1 不阻塞终轮 alone） |

### §Blocking · 高敏须人判断

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 触达 `api/` + 新 HTTP 路由 | ☑ task 已声明；**50 关账必须**（`test_strategy_note` 已写） |
| 2 | `_manifest` 端点登记 | ☑ 验收 §6 已列；依赖 Q-8 冻结 |

### §3.3 独立复检（50）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `required` + 涉 `api/`/契约 | ☑ 50 **必须** |
| 2 | 关账前 50 落盘 | ☐ 待 30 后（预期） |

### OpenSpec × TDD（`harness_task_validate.py`）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型一致 | ☑ |
| 2 | §行为变更 Delta 已填或显式「无」 | ☐ **缺失** — 触达 `api/`；须 ADDED/MODIFIED 或经人确认后写「无」 |
| 3 | `failure_paths` 含 **Scenario ID** 列 | ☐ 现为 FP-1～4 子标题表，**无** validate 可扫的 ID 列 |
| 4 | 验收含 pytest 表述（validate 可扫） | ☐ 标题须对齐 **`## 验收标准`** |

---

## 阻塞项

| ID | 说明 | 建议回填位置 |
|----|------|--------------|
| **B-1** | **`HG-TASK-DRAFT` = `pending`**（`blocks_hats`: 22-R1, 30）；`harness_human_gate_check.py` **exit 1** | 人确认草案方向后改 **`approved`**（建议单独 commit） |
| **B-2** | **SDD §10 待确认清单未清零**：§10 末行「均已人确认 · YYYY-MM-DD」仍为「（待填写）」；**Q-8**（Graph 路由 path · P0 须冻结）未拍板；项 3/4/5 未确认 | §10 表 + 确认行；与 `gates_before_code`「Q-8 已人确认」对齐 |
| **B-3** | **`harness_task_validate.py` FAIL**（`FAILURE-PATHS-EMPTY` · `TEST-STRATEGY-REQUIRED-PYTEST`）— 小节标题与模板/validate 不对齐 | 将 **`## 7. failure_paths`** 改为 **`## 失败路径`**（或增 **`## 失败路径`** 汇总表）；**`## 6. 验收标准`** 改为精确 **`## 验收标准`**（子标题可另起） |
| **B-4** | **缺 §行为变更（Delta）** — 涉 `api/` 模块抽取 + 新路由 | 新增 **`## 行为变更（Delta）`**：`### ADDED`（新模块/路由/manifest 节点）· `### MODIFIED`（`agent.py` import 边界）· 或人确认后显式「无」并说明理由 |

---

## 非阻塞项

| ID | 说明 |
|----|------|
| NB-1 | **Q-7** defer P1 — task 已声明，不阻塞 P0 |
| NB-2 | **Q-4** `ChatBIState` 路径 — 建议默认 **A** `api/graph/state.py`；30 可据 A 实施 |
| NB-3 | **`freeze_id`** 引用 research SPEC 而非单行 ID — P0 无新 L1 SPEC，可接受 |
| NB-4 | 10 帽 invoke `invoke_20260603_10_requirements.md` **未落盘** — 不影响 R1 合同审查，建议 10 回填时补链 |
| NB-5 | **`HG-AUDIT-R1` = pending** — 预期；R2 零阻塞后由 **人** 改 `approved` 再开 30 |

---

## 需任务帽回填清单

- [ ] **B-1**：人将 `HG-TASK-DRAFT` → `approved`（或明示授权 Agent 代填并单独 commit）
- [ ] **B-2**：§10 待确认清单 — **至少冻结 Q-8**（路由 path）；项 3/4/5 拍板；表后写 **「均已人确认 · YYYY-MM-DD」**（Q-7 可注明 defer P1）
- [ ] **B-3**：对齐 validate — 小节 **`## 失败路径`** + 表头含 **Scenario ID**（FP-1～4 映射）；**`## 验收标准`** 精确标题 + 增 `- [ ] PR 上 pytest workflow 全绿` 与本地 `pytest tests -m "not intent_eval and not intent_benchmark"`
- [ ] **B-4**：补 **`## 行为变更（Delta）`**（ADDED/MODIFIED 或经人确认的「无」）
- [ ] （建议）§6 验收钉明 **边表单测 + runner smoke** 模块级期望（`required` red-green 口径）
- [ ] 回填后运行：`python tools/harness_task_validate.py docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` → **OK**

**按审查 R1 回填** → 触发 **22 R2**（`task_chatbi_graph_p0_foundation_v1_audit_R2_YYYYMMDD.md`）。

---

## 是否建议执行帽开工

| 结论 |
|------|
| **否** — B-1～B-4 未闭合；**禁止** 30 帽写 `api/` 实现。下一棒：**10 需求帽** 回填 task。 |

---

## 签收 / 关闭

- **R1 结论**：**未签收** — task 合同层 **尚不可执行**。
- **须继续的条件**：上表回填清单全闭合 · `harness_task_validate.py` OK · 人签 `HG-TASK-DRAFT` → 22 **R2** 零阻塞 → 人签 `HG-AUDIT-R1` → 30 → 40 → CI → **50**（`required` + `api/`）→ `post_close` 终轮 22。
- **本 task 未关闭**（`active` 维持）。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md（**SDD 三轮** · §4 待确认清单 · §5 完成后下一棒）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
按 22 帽 R1 审查清单回填 `task_chatbi_graph_p0_foundation_v1`：对齐 Harness validate、清零 SDD §10 待确认（至少 Q-8 Graph 路由 path），补 §行为变更 Delta；不扩 scope、不写业务代码。回填完成后输出路径 A（22 R2）与路径 B（仅当人已预批且清单已清零时）两条下一棒 Prompt。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md
ai-ink-brain-api-python/docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md
ai-ink-brain-api-python/docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md
ai-ink-brain-api-python/docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md
ai-ink-brain-api-python/docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md

【SDD 三轮状态】（§2 合法取值之一）
轮0+1+2 已完成，清单有待确认项

【是否新建或重大修订 SPEC】
否

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 docs/harness/invokes/README.md 落盘到 docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. **SDD 纪律（硬）**：
   - 若 `{{NEW_OR_MAJOR_SPEC}}` = **是**：须遵守三轮模型（§1）；**禁止** 在本帽一次生成整本 L1 SPEC。
   - 若 SDD 状态含 **「清单有待确认项」**：下一棒 **只许推荐路径 A** 或输出阻塞清单，**禁止** 推荐路径 B。
   - 当状态 = **`轮0+1+2 已完成，清单已人确认`**：可据 §下一棒 A/B 规则推荐 A 或 B；**三轮完成 ≠ 自动跳过 22**（见 SPEC §5）。
   - 本轮回填：**否** 新 SPEC · 须逐条闭合 R1「需任务帽回填清单」B-1～B-4。
2. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
3. 按审查 R1 回填清单逐条映射到 task 小节；文末注明「按审查 R1 回填」。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值。
5. 对话回复 — **下一棒须输出两条 Prompt（由人择一执行，不可只给一条）**：
   - 先输出 **推荐判定**（1～3 行）：本轮回填后 **推荐路径 A（22 R2）**；清单未清零前 **禁止** 推荐 B。
   - **路径 A · 22 任务审核 R2**：标题 `### 下一棒 A：22 任务审核 R2（推荐）`；正文 = TEMPLATE-task-audit-invoke §3 全文（`PREV_REVIEW_PATH` 指向 R1 审查 md）。
   - **路径 B · 30 执行（跳过 22）**：标题 `### 下一棒 B：30 执行（跳过 22）`；**不推荐**；若人强制选 B 须在 task 写明事后补 22。
6. 回复末尾输出 HANDOFF_SEMI_AUTO.md §3.4 `📋 Harness 状态栏（版本 B）`；**不得** 代填 `human_gate: approved`（除非人二次确认授权）。
7. **自动 commit**：若本轮已落盘 invoke 或已按用户授权写入 task，按 HANDOFF_AUTO_COMMIT.md 分仓 commit（仅本轮路径；对话报 short-hash）。用户写明「不要 commit」则跳过。
```
