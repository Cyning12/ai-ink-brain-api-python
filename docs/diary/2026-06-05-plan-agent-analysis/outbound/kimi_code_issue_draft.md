### 问题描述

使用**同样的模型**（kimi-for-coding）、**同样的项目**、**同样的命令**：

- **Claude Code**: 成功完成 plan 任务，自动按 `AGENTS.md` → `.cursor/rules/` → `_tech_graph/` 分层读取
- **Kimi Code**: 子 Agent 超时失败（300s），因为零上下文启动，未读 `.cursor/rules/` 和 `_tech_graph/`，反而读了 4 份 V3 SPEC 细节文件

### 环境信息

- **Kimi Code 版本**: （请填写 `kimi --version`）
- **模型**: `kimi-for-coding`
- **项目**: `ai-ink-brain-api-python`（FastAPI + Supabase + SiliconFlow RAG 后端）
- **项目导航文件**:
  - `AGENTS.md`（根目录，含必读顺序和 `.cursor/rules/` 索引）
  - `CLAUDE.md`（11 字节，仅 `@AGENTS.md`）
  - `.cursor/rules/*.mdc`（12 个规则文件，含 `10-tech-graph.mdc` 指引 `_tech_graph/`）
  - `docs/_tech_graph/`（架构真值，含 `00_main.md`、`graph.json` 等）

### 复现步骤

1. 项目根有 `AGENTS.md`、`.cursor/rules/*.mdc`、`docs/_tech_graph/`
2. 在 Kimi Code 中调用 Agent 工具:
   ```
   Agent(description="Create upgrade plan", prompt="You are in plan mode...")
   ```
3. 子 Agent 未自动读取 `AGENTS.md` 的导航指引
4. 子 Agent 未读取 `.cursor/rules/*.mdc` 的工程约束
5. 子 Agent 未读取 `docs/_tech_graph/` 的架构图谱
6. 子 Agent 自行深入 `docs/spec/v3-agent/` 下的 SPEC 文件，最终超时失败

### 期望行为

子 Agent 应自动感知项目导航文件，类似 Claude Code 的行为：
1. 自动读取 `AGENTS.md` 作为导航核心
2. 自动读取 `.cursor/rules/*.mdc` 获取工程约束
3. 按分层策略读取：`AGENTS.md` → `.cursor/rules/` → `_tech_graph/` → `tasks/` → 源码

### 实际行为

子 Agent 零上下文启动，完全依赖用户手动在 prompt 中传递所有导航规则。由于 prompt 中未显式写明"读 `.cursor/rules/`"和"禁止读 SPEC"，子 Agent：
- ❌ 未读 `.cursor/rules/*.mdc`（12 个文件）
- ❌ 未读 `docs/_tech_graph/`（架构真值）
- ❌ 读了 4 份 `docs/spec/v3-agent/` 下的 SPEC 细节文件
- ❌ 过早读取源码文件（`api/index.py` 1163 行、`api/unified_chat.py` 3217 行）
- ❌ 最终超时失败（300s）

### 对比证据

**Claude Code 阅读路径**（同一项目、同一模型，成功）:
```
L1: CLAUDE.md → AGENTS.md
L2: PROJECT_CONFIG + .cursor/rules/*.mdc（12 个文件全部读取）
L3: _tech_graph/ + tasks/ + harness/
L4: coding_wiki/ + diary/（按需）+ spec/（按需）
L5: 源码（改代码时）
L6: tests/ + tools/
```

完整记录见: `artifacts/claude/project_reading_path.md`

**Kimi Code Plan Agent 阅读路径**（失败）:
```
1. AGENTS.md
2. PROJECT_CONFIG
3. RECENT_TASK_SCHEDULE
4. harness/README
5. coding_wiki/index
6. main.py（源码）
7. api/index.py（源码，1163 行）
8. api/unified_chat.py（源码，3217 行）
9. requirements.txt
10. pytest.ini
11-14. 4 份 V3 SPEC（过度深入）
→ 超时失败
```

### 根因分析

Kimi Code 的 `Agent` 工具文档明确:
> "The subagent starts with **zero context** — it has not seen this conversation."

这是**有意的设计**（避免污染、控制 token），但代价是:
- 用户必须手动传递**所有**项目导航规则
- 容易遗漏（如本次遗漏了 `.cursor/rules/` 和 `_tech_graph/`）
- 与 Claude Code 相比，同样的命令得到完全不同的结果

### 建议方案

#### P1: 子 Agent 自动注入项目导航文件

如果项目根存在以下文件，自动作为子 Agent system prompt 前缀:
- `AGENTS.md`
- `.cursorrules`
- `.cursor/rules/*.mdc`

#### P1: 子 Agent 自动注入 `.cursor/rules/*.mdc`

类似 Cursor IDE 的规则注入机制，让子 Agent 感知工程约束。

#### P2: Agent 工具增加 `inherit_context` 参数

```python
Agent(
    description="Create upgrade plan",
    prompt="...",
    inherit_context=True  # 继承父 Agent 已读取的 AGENTS.md 等导航文件
)
```

#### P2: Plan/Explore 类型 Agent 内置"导航优先"模板

内置分层读取策略:
1. 先读 `AGENTS.md` 获取导航
2. 读 `.cursor/rules/*.mdc` 获取约束
3. 读 `_tech_graph/` 获取架构
4. 读 `tasks/` 获取排期
5. 最后按需读源码

### 当前 Workaround

在 Kimi Code 修复前，用户必须在 prompt 中显式写明:

```python
Agent(
    description="Create upgrade plan",
    prompt="""
【强制导航规则 - 子 Agent 必须先执行】
1. 读取项目根目录 AGENTS.md，按其中"必读（按顺序）"列表读取
2. 读取 .cursor/rules/*.mdc（尤其是 10-tech-graph.mdc、11-coding-wiki-readorder.mdc）
3. 优先使用 docs/_tech_graph/ 了解架构（00_main.md、99_spec.md）
4. 禁止默认读取 docs/spec/v3-agent/ 下的 SPEC 文件
5. 禁止默认读取超过 100 行的源码文件

【任务】
...
"""
)
```

### 附件

- `artifacts/claude/project_reading_path.md` — Claude Code 完整阅读路径记录
- `00_README.md` — 本次事件分析
- `analysis/02_agent_design_comparison.md` — 对比分析
- `analysis/03_reading_path_comparison.md` — 详细对比