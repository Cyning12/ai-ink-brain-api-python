---

## Tech Graph 工程落地记录（已完成任务）

- **P0（可接手性补强）**：入口锚点到 handler/行号、Struct 标注 required/optional、最小漂移检测脚本落地（commit：`adf06d6`）。
- **P1（方案A最小闭环）**：引入 `_manifest.json` + 强校验脚本，支持“制造漂移→明确报错”回归（commit：`a3673bf`）。
- **P2（排障视角）**：新增运行/事件总览图，并在 RAG/Text2SQL/FTS/RPC `.ai.md` 补齐失败路径；`tools/tech_graph_manifest_check.py` 仍为 `OK`（待合并提交）。

---

## 1) 今日关键目标
- 让新 Agent **只读图谱即可开工**（入口可定位到代码锚点）
- 让图谱 **不再静默过期**（manifest 作为真值 + 校验脚本）
- 让排障 **有最短路径**（失败分支、降级、重试、事件契约）

## 2) 关键产出 / 决策（Why + What）
- **产出 1：P0（内容层补强）**
  - **Why**：仅有“主链路图”不足以让新 Agent 快速定位入口与依赖。
  - **What**：`00_main(.ai).md` 增加端点与 handler 锚点；`01_struct.md` 标注 `(req)/(opt)`；提供最小漂移检测脚本。

- **产出 2：P1（机制层闭环）**
  - **Why**：纯手工维护图谱会漂移，且难以发现遗漏。
  - **What**：`docs/_tech_graph/_manifest.json` 做机器可读真值；`tools/tech_graph_manifest_check.py` 做严格一致性校验（端点/RPC/表/env/anchors）。

- **产出 3：P2（运行层/失败路径视角）**
  - **Why**：排障最常见的问题不在 happy path，而在错误分支与降级策略。
  - **What**：新增 `14_runtime_observability(.ai).md`，并在核心子流程 `.ai.md` 中补齐 `[err]` / `?>` / `[retry=N]` 等失败路径。

## 3) 风险与坑位（含排障线索）
- **负向测试后要恢复真值**：对 `_manifest.json` 做“制造漂移→应失败”的回归时，务必恢复原文件再复跑校验。
- **校验脚本是门禁，不是装饰**：端点/RPC/表/env 任何新增/改名，必须先更新 manifest 再更新图谱。

## 4) 明日计划
- [ ] 将校验脚本接入 CI（PR/commit 自动跑 `python tools/tech_graph_manifest_check.py`）
- [ ] 开始端到端边界图（跨仓契约）：Frontend SSE / Content / Backend / Supabase（按需加载）
