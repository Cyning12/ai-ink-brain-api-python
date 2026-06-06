# Kimi Code vs Claude Code · 阅读路径对比分析

> **日期**: 2026-06-05  
> **数据来源**: Claude Code CLI 生成的 `artifacts/claude/project_reading_path.md`  
> **对比对象**: Kimi Code Plan Agent（agent-1/agent-2）vs Claude Code（同一模型 kimi-for-coding）

---

## 1. Claude Code 的阅读路径（来自实际记录）

### 分层递进策略（6 层）

```
L1: 入口与导航（必读）
    ├── CLAUDE.md → @AGENTS.md
    └── AGENTS.md（核心导航，含 .cursor/rules/ 索引）

L2: 配置与契约（必读）
    ├── PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
    └── .cursor/rules/*.mdc（12 个规则文件，含 10-tech-graph.mdc）

L3: 架构与技术图谱（必读）
    ├── docs/_tech_graph/（架构真值）
    ├── docs/tasks/RECENT_TASK_SCHEDULE.md → active/
    └── docs/harness/README.md

L4: 编码维基与回顾（按需）
    ├── docs/coding_wiki/index.md
    ├── docs/diary/（默认不读）
    └── docs/spec/（按需）

L5: 代码实现（改代码时必读）
    ├── api/index.py, ingest_pipeline.py, unified_chat.py, rag_recall_tools.py
    └── 子系统按需：intent_*, code_*, text2sql_*, chatbi_*, graph/

L6: 测试与工具（辅助）
    ├── tests/
    └── tools/
```

### 关键特征


| 特征                 | Claude Code 行为             |
| ------------------ | -------------------------- |
| **AGENTS.md 优先级**  | ✅ 第二层就读取，作为导航核心            |
| **.cursor/rules/** | ✅ 完整读取 12 个 .mdc 文件，获取工程约束 |
| **_tech_graph/**   | ✅ 第三层就读取，作为架构真值            |
| **docs/spec/**     | ✅ 标记为"按需"，默认不读             |
| **docs/diary/**    | ✅ 明确标记"默认不读"               |
| **代码读取**           | ✅ 分层按需，不直接遍历源码             |
| **阅读策略**           | 6 层递进，每层有明确的"必读/按需"标记      |


---

## 2. Kimi Code Plan Agent 的阅读路径（实际发生）

### 实际读取顺序（14 个文件）

```
1. AGENTS.md                    ← 正确
2. PROJECT_CONFIG...            ← 正确
3. RECENT_TASK_SCHEDULE.md      ← 正确
4. docs/harness/README.md       ← 正确
5. docs/coding_wiki/index.md    ← 正确
6. main.py                      ← 过早读源码
7. api/index.py                 ← 过早读源码（1163 行）
8. api/unified_chat.py          ← 过早读源码（3217 行）
9. requirements.txt             ← 正确
10. pytest.ini                  ← 正确
11. SPEC-ChatBI-V3-Resilience-Ops.md     ← ❌ 过度深入 SPEC
12. SPEC-ChatBI-V3-Evaluation.md         ← ❌ 过度深入 SPEC
13. SPEC-ChatBI-V3-Security.md           ← ❌ 过度深入 SPEC
14. SPEC-ChatBI-V3-Identity-Access.md    ← ❌ 过度深入 SPEC
```

### 关键缺失


| 缺失项                                 | 影响                                   |
| ----------------------------------- | ------------------------------------ |
| ❌ `.cursor/rules/*.mdc`             | 未获取工程约束（如 10-tech-graph.mdc 的图谱优先规则） |
| ❌ `docs/_tech_graph/00_main.md`     | 未读架构总览，直接跳源码                         |
| ❌ `docs/_tech_graph/99_spec.md`     | 未读规格索引                               |
| ❌ `docs/_tech_graph/_manifest.json` | 未读契约清单                               |


---

## 3. 核心差异对比表


| 维度                    | Claude Code       | Kimi Code Plan Agent  |
| --------------------- | ----------------- | --------------------- |
| **AGENTS.md 利用**      | ✅ 作为导航核心，指引后续读取顺序 | ⚠️ 读了但只作为列表项之一，未按指引执行 |
| **.cursor/rules/ 读取** | ✅ 完整读取 12 个 .mdc  | ❌ 完全未读                |
| **_tech_graph/ 读取**   | ✅ 第三层必读           | ❌ 完全未读                |
| **SPEC 读取**           | ✅ 标记为"按需"，默认不读    | ❌ 读了 4 份 V3 SPEC 细节   |
| **源码读取时机**            | ✅ L5（改代码时）        | ❌ L1-L2 阶段就读了 3 个源码文件 |
| **阅读策略**              | 6 层递进，每层有约束       | 平铺列表，无分层概念            |
| **结果**                | ✅ 成功              | ❌ 超时失败（300s）          |


---

## 4. 根因定位：为什么 Claude Code 能做到分层递进？

### 假设验证


| 假设                                       | 验证       | 结论                                                              |
| ---------------------------------------- | -------- | --------------------------------------------------------------- |
| H1: Claude Code 自动注入 AGENTS.md           | 可能       | AGENTS.md 中明确写了 .cursor/rules/ 索引，Claude Code 读了 .cursor/rules/ |
| H2: Claude Code 自动注入 .cursor/rules/*.mdc | **高度可能** | 10-tech-graph.mdc 明确指引 _tech_graph/，Claude Code 读了 _tech_graph/ |
| H3: Claude Code 的 Plan 模式有内置模板           | 可能       | "6 层递进"结构非常规范，像内置模板                                             |
| H4: 用户命令不同                               | 已排除      | 用户确认命令相同                                                        |


### 关键证据

Claude Code 生成的阅读路径中：

```markdown
## 第二层：配置与契约（必读）
### 4. Cursor 规则（.cursor/rules/*.mdc）
按主题分类的工程约束，共 12 个规则文件：
```

**这 12 个 .mdc 文件是我（Kimi Code 根 Agent）都没有完整读过的**，但 Claude Code 的子 Agent 读了。这说明：

> **Claude Code 有某种机制让子 Agent 自动感知并读取 `.cursor/rules/*.mdc`**

而 Kimi Code 的 `Agent` 工具明确声明：

> "The subagent starts with **zero context**"

---

## 5. 这是 Bug 还是设计差异？

### 5.1 严格定义


| 判断维度         | 分析                                                  |
| ------------ | --------------------------------------------------- |
| **是否符合文档**   | ✅ Kimi Code 的 Agent 工具文档明确说 "zero context"，实际行为符合文档 |
| **是否与竞品一致**  | ❌ Claude Code 明显有不同的行为（自动项目感知）                      |
| **是否影响用户体验** | ❌ 严重影响：同样的命令，Claude Code 成功，Kimi Code 失败            |
| **是否可预期**    | ❌ 不可预期：用户无法知道子 Agent 不会自动读 AGENTS.md                |


### 5.2 结论：设计差异，但用户体验是缺陷

不是 bug（符合文档），但是**产品竞争力缺陷**。

---

## 6. 建议：Issue vs PR

### 6.1 不建议做 PR 的原因


| 原因                  | 说明                           |
| ------------------- | ---------------------------- |
| **Kimi Code 是闭源产品** | 无法直接修改代码提 PR                 |
| **涉及核心架构决策**        | 子 Agent 上下文隔离是设计意图，改动需产品团队决策 |
| **需要多方案评估**         | 自动注入 vs 可选继承 vs 模板化，需产品团队权衡  |


### 6.2 建议：给 Kimi 官方提 Issue

**Issue 标题建议**：

> `Agent 工具子 Agent 无法自动感知项目导航文件（AGENTS.md / .cursor/rules/），导致与 Claude Code 相比用户体验差距`

**Issue 内容要点**：

```markdown
## 问题描述
使用同样的模型（kimi-for-coding）、同样的项目、同样的命令：
- Claude Code：成功完成 plan 任务，自动按 AGENTS.md → .cursor/rules/ → _tech_graph/ 分层读取
- Kimi Code：子 Agent 超时失败，因为零上下文启动，未读 .cursor/rules/ 和 _tech_graph/

## 复现步骤
1. 项目根有 AGENTS.md、.cursor/rules/*.mdc、docs/_tech_graph/
2. 调用 Agent 工具：Agent(description="Create upgrade plan", prompt="...")
3. 子 Agent 未自动读取 AGENTS.md 和 .cursor/rules/

## 期望行为
子 Agent 自动注入项目导航文件（类似 Claude Code 的行为），或提供机制让用户选择继承上下文

## 实际行为
子 Agent 零上下文启动，完全依赖用户手动在 prompt 中传递所有导航规则

## 对比证据
- Claude Code 阅读路径：artifacts/claude/project_reading_path.md（6 层递进，读了 12 个 .mdc + _tech_graph/）
- Kimi Code 阅读路径：读了 4 份 V3 SPEC + 源码，未读 .cursor/rules/ 和 _tech_graph/

## 建议方案
1. P1: 子 Agent 自动注入 AGENTS.md（如果项目根存在）
2. P1: 子 Agent 自动注入 .cursor/rules/*.mdc
3. P2: Agent 工具增加 inherit_context 参数
4. P2: Plan/explore 类型 Agent 内置"导航优先"模板
```

### 6.3 Issue 的价值


| 价值            | 说明                                        |
| ------------- | ----------------------------------------- |
| **有实际对比数据**   | Claude Code vs Kimi Code 的同一项目、同一模型的对比    |
| **有完整阅读路径记录** | `artifacts/claude/project_reading_path.md` 是客观证据 |
| **影响可量化**     | 同样的任务：Claude Code 成功 vs Kimi Code 超时失败    |
| **有具体改进建议**   | 4 个方案，从 P1 到 P2                           |


---

## 7. 当前 Workaround（用户侧）

在 Kimi Code 修复前，调用 Agent 时必须：

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

---

## 8. 结论


| 问题             | 答案                                      |
| -------------- | --------------------------------------- |
| 是 Bug 吗？       | ❌ 不是，符合 Kimi Code 文档的 "zero context" 设计 |
| 是设计差异吗？        | ✅ 是，Claude Code 自动注入 vs Kimi Code 零上下文  |
| 是产品竞争力缺陷吗？     | ✅ 是，同样的任务 Claude Code 成功，Kimi Code 失败   |
| 值得提 Issue 吗？   | ✅ **非常值得**，有完整对比数据和改进建议                 |
| 能做 PR 吗？       | ❌ 不能，Kimi Code 是闭源产品                    |
| 短期 workaround？ | ✅ 在 prompt 中显式写明导航规则和禁止项                |


---

## 9. 修订记录


| 日期         | 说明                                                     |
| ---------- | ------------------------------------------------------ |
| 2026-06-05 | 初稿：基于 Claude Code 实际阅读路径记录，对比分析 Kimi Code 的 Agent 行为差异 |


