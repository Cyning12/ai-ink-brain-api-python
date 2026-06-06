# Kimi Code vs Claude Code · AGENTS.md 读取行为对比分析

> **日期**：2026-06-05  
> **背景**：用户反馈"用 Claude Code 同样的模型、同样的命令，完全没有读错"，质疑 Kimi Code 是否存在设计缺陷

---

## 1. 关键发现：`CLAUDE.md` 的内容

```bash
$ cat CLAUDE.md
@AGENTS.md
```

**只有 11 字节**：一个指向 `AGENTS.md` 的引用。

这意味着 Claude Code 和 Kimi Code 在**项目文件层面**的输入是完全相同的：
- 都有 `AGENTS.md`
- 都有 `.cursor/rules/*.mdc`（含 `10-tech-graph.mdc` 明确指引 `_tech_graph/`）
- 都有 `docs/_tech_graph/00_main.md` 等图谱文件

**所以差异不在项目文件，而在 Agent 的行为设计。**

---

## 2. 对比假设

| 维度 | Claude Code（用户反馈） | Kimi Code（实际发生） |
|------|------------------------|----------------------|
| 用户命令 | "启动一个 plan Agent 制定升级计划" | 相同 |
| 模型 | 相同（用户确认） | 相同 |
| 项目文件 | 相同（`AGENTS.md`、`CLAUDE.md`、`.cursor/rules/`） | 相同 |
| **Agent 行为** | ✅ 正确读取 `_tech_graph/` → `RECENT_TASK_SCHEDULE.md` → 制定计划 | ❌ 读了 4 份 V3 SPEC + 源码，超时失败 |
| **结果** | 成功 | 失败（300s 超时） |

---

## 3. 根因分析：Kimi Code 的 Agent 工具设计问题

### 3.1 核心问题：Agent 的 Prompt 中没有自动注入 `AGENTS.md`

从系统指令中可以看到：

> "`AGENTS.md` files can appear at any level of the project directory tree... When multiple `AGENTS.md` files apply to a file you are modifying, instructions in deeper directories take precedence..."

**这是给根 Agent（我）的指令，不是给子 Agent 的。**

当我调用 `Agent` 工具创建子 Agent 时：

```
agent_id: agent-1
actual_subagent_type: plan
prompt: "You are in plan mode. Please read the following key files..."
```

**子 Agent 的 prompt 是全新上下文，不包含：**
- 根 Agent 已读取的 `AGENTS.md` 内容
- `.cursor/rules/*.mdc` 的约束
- 系统指令中关于 "先读图谱" 的约定

子 Agent 看到的只有我给它的 prompt：
> "请读以下关键文件... 1. `AGENTS.md` ... 7. `main.py`, `api/index.py`, `api/unified_chat.py`"

**这是一个平铺的列表，Agent 按顺序逐个读，没有优先级概念。**

### 3.2 为什么 Claude Code 没有这个问题？

可能的解释（基于用户反馈推断）：

| 假设 | 说明 |
|------|------|
| **H1: Claude Code 自动注入项目上下文** | Claude Code 可能在创建子 Agent 时，自动将 `AGENTS.md`、`.cursorrules`、`.cursor/rules/*.mdc` 注入到子 Agent 的 system prompt 中 |
| **H2: Claude Code 的 Plan Agent 模板更智能** | Claude Code 的 "plan" 模式可能有内置的"先读项目导航文件"的默认行为 |
| **H3: Claude Code 的上下文继承** | Claude Code 的子 Agent 可能继承父 Agent 已读取的文件内容 |
| **H4: 用户在使用 Claude Code 时用了不同的命令** | 可能 Claude Code 的命令更具体，如 "先读 AGENTS.md 和 _tech_graph" |

**最可能的是 H1 或 H2**：Claude Code 有某种机制让子 Agent "感知"到项目导航规则。

### 3.3 Kimi Code 的具体缺陷

| 缺陷 | 说明 |
|------|------|
| **子 Agent 零上下文启动** | `Agent` 工具的 prompt 参数是子 Agent 的**唯一**输入，不继承父 Agent 的任何读取历史 |
| **无自动 AGENTS.md 注入** | 系统没有自动将项目根目录的 `AGENTS.md` 作为子 Agent 的 system prompt 前缀 |
| **无 `.cursor/rules/` 感知** | `.cursor/rules/*.mdc` 文件对子 Agent 完全不可见 |
| **Prompt 设计责任完全下放给用户** | 用户必须手动在 prompt 中写明"先读 AGENTS.md"、"不要读 SPEC"等约束 |

### 3.4 验证：子 Agent 的 prompt 确实没有继承

从 tool 调用记录看：

```
Agent(description="Create upgrade plan", prompt="You are in plan mode. Please read...")
```

子 Agent 的 prompt 中：
- ✅ 有 `AGENTS.md`（我显式写的第 1 项）
- ❌ 没有 `_tech_graph/` 的指引（我没写）
- ❌ 没有 `.cursor/rules/10-tech-graph.mdc` 的约束（子 Agent 看不到）
- ❌ 没有 "不要读 SPEC" 的边界（我没写）

**结论：子 Agent 的行为完全取决于我写的 prompt。我写得不好，子 Agent 就表现差。**

---

## 4. 这是 Kimi Code 的设计问题吗？

### 4.1 严格来说：**是设计差异，不是 bug**

Kimi Code 的 `Agent` 工具文档明确写了：

> "The subagent starts with zero context — it has not seen this conversation. Brief it like a colleague who just walked into the room"

这是**设计意图**：子 Agent 是干净的、独立的。好处是：
- 避免上下文污染
- 明确的输入输出边界
- 可控的 token 消耗

代价是：
- 用户必须手动传递所有必要上下文
- 容易遗漏项目导航规则

### 4.2 但与 Claude Code 相比，**用户体验确实有差距**

| 方面 | Claude Code（推断） | Kimi Code |
|------|---------------------|-----------|
| 项目导航 | 自动感知 `AGENTS.md` / `.cursorrules` | 完全依赖用户手动传递 |
| 子 Agent 上下文 | 可能继承或自动注入 | 零上下文，完全隔离 |
| 学习曲线 | 低（"像同事一样说话"就行） | 高（必须显式写明所有约束） |
| 一致性 | 高（不同用户得到相似行为） | 低（完全取决于 prompt 质量） |

### 4.3 改进建议（给 Kimi Code 产品侧）

| 优先级 | 建议 | 说明 |
|--------|------|------|
| P1 | **子 Agent 自动注入 `AGENTS.md`** | 如果项目根有 `AGENTS.md`，自动作为子 Agent system prompt 前缀 |
| P1 | **子 Agent 自动注入 `.cursor/rules/*.mdc`** | 类似 Cursor 的规则注入机制 |
| P2 | **父 Agent 上下文可选继承** | `Agent` 工具增加 `inherit_context: true` 参数 |
| P2 | **Plan Agent 专用模板** | 内置 "先读导航 → 再读图谱 → 最后读源码" 的默认行为 |
| P3 | **项目导航文件索引** | 自动发现 `AGENTS.md`、`.kimi-code/`、`CLAUDE.md` 等导航文件 |

---

## 5. 当前 workaround（用户侧）

在 Kimi Code 修复之前，调用 `Agent` 工具时必须：

```python
Agent(
    description="Create upgrade plan",
    prompt="""
【项目导航规则 - 必须先读】
1. 读取项目根目录的 AGENTS.md，获取导航指引
2. 按 AGENTS.md 的"必读（按顺序）"列表读取文件
3. 优先使用 docs/_tech_graph/ 图谱了解架构，不要直接遍历源码

【禁止读取】
- docs/spec/v3-agent/ 下的 SPEC 文件（除非 task 明确指向）
- 任何超过 100 行的源码文件（除非图谱明确需要）

【任务】
制定升级计划...
"""
)
```

---

## 6. 结论

| 问题 | 答案 |
|------|------|
| 是模型问题吗？ | ❌ 不是，同样的模型 Claude Code 表现更好 |
| 是项目文件问题吗？ | ❌ 不是，`AGENTS.md`、`.cursor/rules/` 都完备 |
| 是 Kimi Code 设计问题吗？ | ⚠️ **是设计差异**：子 Agent 零上下文隔离 vs Claude Code 的自动项目感知 |
| 是我的 prompt 问题吗？ | ✅ **也是**：我没有显式约束读取路径和边界 |
| 如何修复？ | 短期：改进 prompt；长期：Kimi Code 产品侧增加自动导航注入 |

---

## 7. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-05 | 初稿：对比分析 Kimi Code 与 Claude Code 的 Agent 行为差异 |
