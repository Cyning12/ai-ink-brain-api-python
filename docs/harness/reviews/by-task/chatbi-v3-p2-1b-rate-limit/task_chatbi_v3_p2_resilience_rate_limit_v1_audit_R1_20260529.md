# 任务审核：ChatBI V3 P2-1b 高消耗端点限流 — R1

## 元信息

| 字段 | 值 |
|------|-----|
| 审查轮次 | **R1**（首轮 · `post_close` 闸 1） |
| 关联上一轮 | **无** |
| 待审 task | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md` |
| 关联 SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md` · `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` §2.1 |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/chatbi-v3-p2-1b-rate-limit/invoke_20260529_22_chatbi-v3-p2-1b-rate-limit.md` |
| **git_branch** | `task/chatbi-v3-p2-1b-rate-limit` |
| **worktree_root** | 主仓 `ai-ink-brain-api-python/` |
| **freeze_id** | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11`（与 task 头部一致） |
| **test_strategy** | `required` |
| **audit_profile** | `post_close` |
| 门禁 | `python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md` → **exit 0** |
| 规划对齐 | `docs/harness/HARNESS_V2_PLAN.md` **§5** |
| 落盘日期 | 2026-05-29 |

---

## 审查结论摘要

1. **Harness 字段**：`test_strategy: required`、`freeze_id`、`gates_before_code`（`failure_paths` / `验收标准` / `必读列表`）、`semi_auto`、`audit_profile: post_close`、`git_branch` 齐全；与母单 P2-1 拆单及 P2-1a **done**（PR #52）依赖关系在 task 头部可追溯。  
2. **SPEC 对齐**：`SPEC-ChatBI-V3-Resilience-Ops.md` **§2**（粒度、路径、`429` + 结构化 body、env 禁硬编码）与 task **范围 / 非范围** 一致；**非范围** 正确排除 P2-1a 探针与 P2-1c 熔断。  
3. **failure_paths**：F1（超阈值 `429`）、F3（双端点覆盖缺口 → 复检 fail）可观测、可写 pytest；F2（env 缺失/非法）语义在 task 层 **略歧义**（见非阻塞 NB-2），不单独构成 22 拒开工。  
4. **验收可观测性**：四条 `- [ ]` 均可核对；与 sibling `task_chatbi_v3_p2_resilience_health_ready_v1` 相比，**未预钉 pytest 模块名**（见 NB-1），在 `required` 下由 **30 帽** 以「先红后绿」落地并回填自检，符合 `post_close` 最小 R1。  
5. **必读列表**：覆盖 task、母单、Resilience SPEC、`api/index.py` + `api/unified_chat.py`；10 帽 kickoff 已提示 `PROJECT_CONFIG` env 落点，**建议** 30 实施时写入必读（NB-3），非 R1 硬阻塞。  
6. **现网差距（文档层）**：仓库内 **尚无** 限流 middleware / `429` 实现（符合 `in_progress`）；实现归属 30，与本帽停于 task 合同层一致。

---

## 阻塞项

- **无**。

---

## 非阻塞项

| ID | 说明 | 建议落点 |
|----|------|----------|
| NB-1 | 验收第 1 条写「`hey` 或 pytest 并发桩」，未像 P2-1a 那样钉死 `tests/test_*.py` | 30 在 PR 中新增专用 pytest（建议命名 `tests/test_rate_limit_routes.py` 或等价），自检结论写清命令；可选由 10 帽在 R2 前补一句 task 验收 |
| NB-2 | F2「启动期报错 **或** 回退默认值并告警」二选一未在 task 冻结 | 30 择一并写入 `PROJECT_CONFIG` + 实现备忘；若与 SPEC 冲突则走变更请求 |
| NB-3 | 必读未列 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 30 必读自扩；关账前 env 表须有阈值项 |
| NB-4 | 粒度「IP 或 access token」未指定 MVP 优先 | SPEC §2 要求「至少支持」其一；建议初版 **每客户端 IP**（与现有 Bearer 鉴权并存），API Key 分桶可 follow-up |
| NB-5 | task 无 `human_gate` 表，而 `PROMPT_TASK_10_kickoff` 提及 `HG-TASK-DRAFT` | 机器门禁已通过（无 `pending` 行）；`post_close` 关账前仍建议人签终轮闸（与 P2-1a 流程一致） |
| NB-6 | `error_code` 未给字面量 | 30 须与现网 JSON 错误 envelope 对齐（参考 P1-2 guard / unified 错误体），pytest 断言 `error_code` 字段存在 |

---

## 需任务帽回填清单

- [ ] **无**（R1 不强制 10 帽改 task；NB-1～NB-6 可在 30/40 自检与 `PROJECT_CONFIG` 中闭合）。

---

## 是否建议执行帽开工

| 结论 |
|------|
| **是** — 在分支 `task/chatbi-v3-p2-1b-rate-limit`、worktree 主仓内可进入 **30 执行编码帽**；须遵守 `test_strategy: required`（先可失败 pytest 再实现）。 |

---

## 签收 / 关闭

- **结论**：**22-R1 approved（零阻塞）** — task 合同层 **可执行**；**不等同** task `done`（仍须 30→40→CI→50 + `post_close` 终轮 22 签收）。  
- **须继续的条件**：双高消耗路径可稳定 `429`、env 可调、全量 pytest 门禁绿、50 复检 pass 后归档 `done/`。  
- **与母单**：`blocked_by` P2-1a 已满足；本单不挡 P2-1c 立项，但实现顺序仍建议先完成 P2-1b 再开熔断子单。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/hats/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8（合并前必绿命令真值，若与本条 VERIFY 冲突以 task + 子仓 workflow 为准）

输入（已由人工替换占位符；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致，见 docs/harness/README.md「并行分支与 Git worktree」）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/task_chatbi_v3_p2_resilience_rate_limit_v1_audit_R1_20260529.md
- 关联 SPEC / 总规（无则「无」）：
ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md
ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 `human_gate`（见 docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md）。若任一对 **本帽（30）** 为 `pending` → 仅输出须人改的 `gate_id` 与路径，**拒开工**；禁止代填 `approved`。**例外**：若 invoke 声明 gate 已「人 kickoff 预批」但文件仍为 `pending`，Agent 须向用户二次确认（见 HANDOFF_SEMI_AUTO.md §2.3 预批与二次确认），获得明确文字授权后方可代填，且须在 commit message 注明 `human_gate 由 Agent 按人授权代填`。
1. 通读 task 全文：头部 `gates_before_code`、`audit_profile`、`semi_auto`、`test_strategy` / `test_strategy_note`、`freeze_id`、`failure_paths`、拒开工条件、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足（缺 failure_paths 可操作性、缺验收命令、必读未覆盖等）→ **仅输出 Markdown 阻塞清单**（缺什么、建议回填的小节标题、推荐下一棒角色），**不写**业务实现代码。
3. `test_strategy: required` 时：先增加或调整 **可失败** 的自动化测试（或与实现同 PR 且满足 task 所述 red-green / 可复现失败语义），再改实现；禁止「只写实现、后补测」绕过 task 约定。
4. 在 `ai-ink-brain-api-python` 内按 task 范围改代码/配置（**禁止**在并行另一 worktree/checkout 改同一子仓）；禁止静默扩大 scope；SPEC/task 矛盾走变更请求或交回需求帽，不擅自调和为代码假设。
5. 在 `ai-ink-brain-api-python` 执行 `pytest tests -m "not intent_eval and not intent_benchmark"`（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 `hats/40-self-check.md` 将结论与命令摘要 **回填** 至 task 正文 **`### 自检结论（执行者）`**（无则新增该小节）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
9. **半自动下一棒（可选）**：若 task `semi_auto: true` 且下一棒（如 40）无 `human_gate` 阻塞：先将 **下一棒 §3 全文** 落盘新 invoke 并 commit，再切换角色执行；规则见 HANDOFF_SEMI_AUTO.md §3。否则仅输出下一棒 Prompt 供人开新会话。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出。

【22-R1 审查约束（须一并遵守）】
- 覆盖 `/api/py/unified/chat/stream` 与 `/api/py/chat`；触发限流时 HTTP 429 + 结构化 body（含 `error_code`，可选 `retry_after`）。
- 阈值经 env 配置并写入 PROJECT_CONFIG；闭合 NB-2（F2 启动期行为二选一）、NB-4（建议 MVP 每 IP）。
- 参考审查非阻塞表：ai-ink-brain-api-python/docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/task_chatbi_v3_p2_resilience_rate_limit_v1_audit_R1_20260529.md
```

---

## 给 Cursor

`Harness`、`任务审核`、`R1`、`零阻塞`、`chatbi-v3-p2-1b-rate-limit`、`P2-1b`、`rate_limit`、`post_close`、`30-execute`
