# ChatBI V3 P2-1b 限流 · 10 帽启动

> **task**：`docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md`  
> **task_slug**：`chatbi-v3-p2-1b-rate-limit`  
> **分支**：`task/chatbi-v3-p2-1b-rate-limit`  
> **worktree**：主仓 `ai-ink-brain-api-python/`（与 Wiki 轨并行，勿混切分支）

---

## 执行前（分支 / worktree）

分支与 worktree **已创建**；开帽前确认：

```bash
cd ai-ink-brain-api-python
git branch --show-current   # 期望 task/chatbi-v3-p2-1b-rate-limit
git worktree list           # 主仓 = 本分支；Wiki 轨在 ../ai-ink-brain-api-python-wt-wiki-accept

python tools/harness_human_gate_check.py \
  --task docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md
```

`HG-TASK-DRAFT` 未 `approved` → **硬停**（须人改 task 头 `human_gate` 后再开 30）。

---

## §3 可复制 Prompt 正文（10-requirements · 开帽）

```text
你正在扮演本仓 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/harness/prompts/templates/TEMPLATE-requirements-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

【目标与上下文】
启动 ChatBI V3 **P2-1b 高消耗端点限流** 实现链：在既有 task 与 SPEC 基础上，确认验收/failure_paths/必读列表可执行，补齐缺口后输出下一棒 A（22）/ B（30）双 Prompt 供人择一。
约束：test_strategy **required** · semi_auto **true** · 分支 **task/chatbi-v3-p2-1b-rate-limit** · 与 Wiki 验收扩充轨并行（勿改 RECENT 除非 task 明确要求）。

【已有材料路径】
docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md
docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md
docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md
docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md §2.1
docs/tasks/RECENT_TASK_SCHEDULE.md §1.1 #0b · §1.2
api/index.py
api/unified_chat.py
docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md（限流 env 落点）

【是否按任务审核文档回填】
无

【SDD 三轮状态】
不涉及新 SPEC（§3 省略）

【是否新建或重大修订 SPEC】
否

你必须完成（TEMPLATE §3 全文纪律）：
0. **Invoke 快照**：将本消息全文落盘 docs/harness/invokes/by-task/chatbi-v3-p2-1b-rate-limit/invoke_YYYYMMDD_10_chatbi-v3-p2-1b-rate-limit.md（元数据表 + 快照 fenced code）。
1. 扫描 task **human_gate**；列出阻塞帽。
2. 对照 SPEC §2 与母单 P2-1b 行：输出结构化块（背景/范围/非范围/依赖/验收/failure_paths/必读）；矛盾单独小节。
3. 若 task 缺项（如 VERIFY 命令块、env 名草案、429 body 字段表）：在对话给出 **段落级补丁建议**；用户授权后再写入 task。
4. **禁止**：写 api/ 实现；改 CI；代填 human_gate approved。
5. **下一棒双 Prompt（硬）**：
   - 推荐判定：本 task 为 test_strategy required + post_close → **默认推荐 A（22）**；若 task 已人扫且 HG-TASK-DRAFT approved 且无验收缺口，可说明选 B 的条件与风险。
   - 路径 A：TEMPLATE-task-audit-invoke §3 全文（{{TASK_PATH}} = 上列 active task；R1 落盘 docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/）。
   - 路径 B：TEMPLATE-execute-invoke §3 全文（30 须先跑 graph_query 影响面：unified chat stream + /api/py/chat）。
6. 回复末尾 **📋 Harness 状态栏（版本 B）**（HANDOFF_SEMI_AUTO §3.4）。
7. invoke（+ 若授权改 task）按 HANDOFF_AUTO_COMMIT 分仓 commit；用户说「不要 commit」则跳过。

P2-1b 实现要点（供 10 分析引用，非本帽实现）：
- 端点：/api/py/unified/chat/stream · /api/py/chat
- 429 结构化 body：error_code · 可选 retry_after
- 粒度：IP 或 API Key（与现有鉴权对齐）
- 非范围：/live /ready（P2-1a）· 熔断（P2-1c）· WAF
```

---

## 落盘约定

| 帽 | 路径模式 |
|----|----------|
| 10 | `docs/harness/invokes/by-task/chatbi-v3-p2-1b-rate-limit/invoke_*_10_*` |
| 22 | `docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/review_*_22_*` |
| 30 | `docs/harness/invokes/by-task/chatbi-v3-p2-1b-rate-limit/invoke_*_30_*` |
| 40 | `docs/harness/invokes/by-task/chatbi-v3-p2-1b-rate-limit/invoke_*_40_*` |
| 50 | `docs/tasks/reinspect_results/reinspect_chatbi-v3-p2-1b-rate-limit_*` |

关账链（semi_auto）：**30 → 40 → 50（required）→ PR → git mv done/**。
