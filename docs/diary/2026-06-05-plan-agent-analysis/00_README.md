# Plan Agent 对比实验 · 文档索引

> **日期**：2026-06-05  
> **项目**：`ai-ink-brain-api-python`  
> **触发命令**：「启动 Plan Agent，制定升级计划」  
> **模型**：Claude Code 与 Kimi Code 均使用 `kimi-for-coding`

---

## 1. 背景（发生了什么）

在本项目启动后，Claude Code 与 Kimi Code 分别尝试读取项目概况与任务排期，并调用 **Plan Agent** 制定升级计划。两者使用**相同模型、相同项目、相近命令**，结果却出现明显差距：

| 工具 | Plan Agent 结果 | 根 Agent 补救 |
|------|----------------|---------------|
| **Claude Code** | ✅ 成功（约 30.3k tokens，37 次工具调用） | 无需补救 |
| **Kimi Code** | ❌ 300s 超时失败 | 根 Agent 手写 `artifacts/kimi/upgrade_plan_fallback.md` |

差距不在项目文档缺失，而在 **子 Agent 如何发现与继承项目导航上下文**：

- Claude Code：自动按 `AGENTS.md` → `.cursor/rules/` → `_tech_graph/` → `tasks/` 分层读取
- Kimi Code Plan Agent：零上下文启动，按平铺文件列表深读 V3 SPEC 与巨型源码，跳过图谱与规则

本目录完整留证上述对比过程、阅读路径、根因分析与对外 Issue 草稿。

---

## 2. 目录结构

```
2026-06-05-plan-agent-analysis/
├── 00_README.md                 ← 本索引
├── artifacts/                   ← 两侧实际产出（客观证据）
│   ├── claude/                  ← Claude Code 成功路径产出
│   │   ├── project_reading_path.md
│   │   ├── explore_codebase_structure.md
│   │   └── upgrade_plan.md
│   └── kimi/                    ← Kimi Code 超时后的补救产出
│       └── upgrade_plan_fallback.md
├── analysis/                    ← 对比分析与根因
│   ├── 01_root_cause_and_paths.md
│   ├── 02_agent_design_comparison.md
│   ├── 03_reading_path_comparison.md
│   └── 04_issue_reply_analysis.md
└── outbound/                    ← 对外提交材料
    └── kimi_code_issue_draft.md
```

---

## 3. 推荐阅读顺序

| 顺序 | 文件 | 用途 |
|------|------|------|
| 1 | 本文件 | 建立全局上下文 |
| 2 | `artifacts/claude/project_reading_path.md` | Claude Code 的 6 层阅读策略（对照基准） |
| 3 | `analysis/01_root_cause_and_paths.md` | Kimi Plan Agent 实际读了什么、漏了什么 |
| 4 | `analysis/03_reading_path_comparison.md` | 两侧阅读路径逐项对比表 |
| 5 | `analysis/02_agent_design_comparison.md` | 子 Agent 零上下文 vs Claude 自动注入 |
| 6 | `artifacts/claude/upgrade_plan.md` vs `artifacts/kimi/upgrade_plan_fallback.md` | 成功计划 vs 补救计划的内容差异 |
| 7 | `outbound/kimi_code_issue_draft.md` | 提交 Kimi 官方的 Issue 草稿 |
| 8 | `analysis/04_issue_reply_analysis.md` | Issue #489 第三方回复（AgentRelay）解读 |

---

## 4. 核心结论（TL;DR）

1. **项目侧无责**：`AGENTS.md`、`.cursor/rules/`、`docs/_tech_graph/` 导航体系完备。
2. **Kimi 侧双重因素**：
   - **产品机制**：`Agent` 工具子 Agent 零上下文，不自动注入 `AGENTS.md` / `.cursor/rules/`
   - **Prompt 质量**：根 Agent 给子 Agent 的文件列表平铺、未禁读 SPEC、未强制图谱优先
3. **Claude Code 优势**：子 Agent 能感知项目导航与工程约束，形成 6 层递进阅读，Plan 任务一次成功。
4. **短期 workaround**：在 `Agent(...)` 的 prompt 中显式写明导航顺序与禁止项（见 `analysis/02` §5、`outbound/` 草稿）。
5. **长期建议**：Kimi Code 产品侧增加子 Agent 自动注入 `AGENTS.md` + `.cursor/rules/`（Issue 草稿已写）。

---

## 5. 两份升级计划的差异说明

| 维度 | Claude 版 | Kimi 补救版 |
|------|-----------|-------------|
| 路径 | `artifacts/claude/upgrade_plan.md` | `artifacts/kimi/upgrade_plan_fallback.md` |
| 来源 | Plan Agent 成功产出 | 子 Agent 超时后根 Agent 基于排期手写 |
| 结构 | 5 阶段（P0–P4）：加固 → 解耦 → 性能 → 测试 → DX | 5 Phase：债务清偿 → 架构演进 → …（对齐 `RECENT_TASK_SCHEDULE`） |
| 侧重点 | 工程现代化（路由拆分、服务层、OTel、Redis 限流） | 任务驱动关账（active task 进 `done/`、Intent/Graph 演进） |

两者互补：Claude 版偏架构与工程体验；Kimi 版更贴本仓 Harness 任务排期。**均非 L0 真值**，实施前须对照 `docs/tasks/` 与 `docs/_tech_graph/`。

---

## 6. 关联链接

- Kimi 官方 Issue：https://github.com/MoonshotAI/kimi-code/issues/489
- 项目导航真值：`AGENTS.md`、`docs/_tech_graph/00_main.md`

---


---

## 6.1 落盘位置

- **草稿轨（本机）**：`tmp/diary/2026-06-05-plan-agent-analysis/`（Git 不跟踪）
- **留证轨（可提交）**：`docs/diary/2026-06-05-plan-agent-analysis/`（与 tmp 内容同步，2026-06-06 整理后镜像）

## 7. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-05 | 初稿：Plan Agent 超时分析与 Kimi vs Claude 对比 |
| 2026-06-06 | 整理目录：按 artifacts / analysis / outbound 分层，重写本索引 |
