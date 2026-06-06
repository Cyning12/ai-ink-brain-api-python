# Plan Agent 超时 · 根因与阅读路径

> **日期**：2026-06-05  
> **所属**：`analysis/01` · 完整索引见 [`00_README.md`](../00_README.md)

> **事件**：Plan Agent（`Create upgrade plan`）执行超时（300s）失败  
> **分析目标**：记录完整读取路径、改动路径、根因定位

---

## 1. 本次会话中 Plan Agent 实际读取的文件路径（完整）

Plan Agent 在超时前读取了以下文件（按工具调用顺序）：


| #   | 文件路径                                                   | 类型   | 说明                    |
| --- | ------------------------------------------------------ | ---- | --------------------- |
| 1   | `AGENTS.md`                                            | 导航   | Agent 指引（正确）          |
| 2   | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`  | 配置   | 环境变量/契约真值（正确）         |
| 3   | `docs/tasks/RECENT_TASK_SCHEDULE.md`                   | 排期   | 任务状态与优先级（正确）          |
| 4   | `docs/harness/README.md`                               | 流程   | Harness 关账流程（正确）      |
| 5   | `docs/coding_wiki/index.md`                            | 索引   | Coding Wiki L2 导航（正确） |
| 6   | `main.py`                                              | 源码   | 入口转发（正确）              |
| 7   | `api/index.py`                                         | 源码   | 主 FastAPI 应用（正确）      |
| 8   | `api/unified_chat.py`                                  | 源码   | Unified Chat 实现（正确）   |
| 9   | `requirements.txt`                                     | 配置   | 依赖列表（正确）              |
| 10  | `pytest.ini`                                           | 配置   | 测试配置（正确）              |
| 11  | `docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md`  | SPEC | **V3 实现细节**（过度深入）     |
| 12  | `docs/spec/v3-agent/SPEC-ChatBI-V3-Evaluation.md`      | SPEC | **V3 实现细节**（过度深入）     |
| 13  | `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md`        | SPEC | **V3 实现细节**（过度深入）     |
| 14  | `docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access.md` | SPEC | **V3 实现细节**（过度深入）     |


**未读取的关键文件**（项目图谱入口，本应先读）：

- ❌ `docs/_tech_graph/00_main.md` — 架构总览 Mermaid
- ❌ `docs/_tech_graph/99_spec.md` — 规格总索引
- ❌ `docs/_tech_graph/_manifest.json` — 图谱 manifest
- ❌ `docs/_tech_graph/graph.json` — 机器可读图谱

---

## 2. 本次会话中产生的改动文件路径（完整）

> **注（2026-06-06 整理）**：下表为当时会话落盘路径；整理后统一迁入本目录子树，见 [`00_README.md`](../00_README.md) §2。



| #   | 文件路径                                                     | 操作       | 说明                                |
| --- | -------------------------------------------------------- | -------- | --------------------------------- |
| 1   | `artifacts/kimi/upgrade_plan_fallback.md`                             | **新建**   | Plan Agent 失败后，由根 Agent 手动制定的升级计划 |
| 2   | `artifacts/kimi/`                                            | **新建目录** | 存放升级计划                            |
| 3   | `00_README.md` | **新建**   | 本分析落盘文件                           |
| 4   | `analysis/`             | **新建目录** | 分析落盘目录                            |


---

## 3. 根因：Prompt 设计问题归属

### 3.1 结论：**Kimi Code 侧（我）的 Prompt 设计问题**，不是项目的问题


| 维度            | 项目侧                                              | Kimi Code 侧（我）                          |
| ------------- | ------------------------------------------------ | --------------------------------------- |
| 知识组织          | ✅ 已建立完整图谱体系（`_tech_graph/`、`AGENTS.md` 导航）       | —                                       |
| 读取指引          | ✅ `AGENTS.md` 明确写了"必读按顺序"，第 3 条就是 `_tech_graph/` | —                                       |
| 快速入口          | ✅ `00_main.md` 一张图展示全架构                          | —                                       |
| **Prompt 约束** | —                                                | ❌ **未在 prompt 中强制要求按 `AGENTS.md` 顺序读取** |
| **深度控制**      | —                                                | ❌ **未禁止读取 `docs/spec/v3-agent/` 细节**    |
| **路径白名单**     | —                                                | ❌ **未指定"先读图谱，再读排期，最后读源码"的优先级**          |


### 3.2 具体错误

我发给 Plan Agent 的 prompt 是：

> "请读以下关键文件... 1. `AGENTS.md` ... 7. `main.py`, `api/index.py`, `api/unified_chat.py` ..."

**问题**：

1. **列表式平铺，无优先级分层** — 所有文件同等重要，Agent 会按顺序逐个深读
2. **未引用 `_tech_graph/`** — 完全遗漏了项目设计的"快速通道"
3. **未设边界** — 没有说"不要读 SPEC 细节"，Agent 自行决定深入 V3 SPEC
4. **任务描述模糊** — "制定升级计划"没有定义"升级"的范围边界，Agent 试图全面理解所有 V3 功能

### 3.3 正确的 Prompt 应该怎么写

```
你是 plan mode。请按以下**严格顺序**读取文件，**不要跳过步骤**：

【步骤 1：导航与架构（必读，不超过 5 分钟）】
1. AGENTS.md — 获取项目导航规则
2. docs/_tech_graph/00_main.md — 架构总览（一张 Mermaid 图）
3. docs/_tech_graph/99_spec.md — 规格索引

【步骤 2：任务状态（必读，不超过 3 分钟）】
4. docs/tasks/RECENT_TASK_SCHEDULE.md — 当前排期与 active 任务

【步骤 3：边界与配置（选读，不超过 3 分钟）】
5. docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md — 环境变量与契约

【禁止读取】
- docs/spec/v3-agent/ 下的任何 SPEC 文件（这些是实现细节，非计划所需）
- 任何源码文件超过前 50 行（除非图谱明确指向）

基于以上信息，制定宏观升级计划，写入 artifacts/kimi/upgrade_plan_fallback.md。
```

---

## 4. 项目文档体系的验证

为验证"项目侧无问题"，检查项目已有的导航设计：


| 检查项                                | 结果  | 证据                                              |
| ---------------------------------- | --- | ----------------------------------------------- |
| `AGENTS.md` 是否指引 `_tech_graph/`？   | ✅ 是 | AGENTS.md 第 1 条："3. `docs/_tech_graph/` — 架构真值" |
| `_tech_graph/00_main.md` 是否存在？     | ✅ 是 | 61 行，含完整 Mermaid 架构图                            |
| `_tech_graph/` 是否有机器轨？             | ✅ 是 | `graph.json`（61KB）+ `_manifest.json`            |
| `RECENT_TASK_SCHEDULE.md` 是否含升级线索？ | ✅ 是 | §4.2 "纯后端线" 已给出执行顺序                             |
| 是否有规则禁止 Agent 乱读？                  | ✅ 是 | `.cursor/rules/00-core.mdc` 含"修改前确认"约束          |


**结论**：项目已经建立了"图谱优先 → 任务驱动 → 源码实现"的三层知识架构，且文档完备。Plan Agent 的失败纯粹是因为我的 prompt 没有利用这个体系。

---

## 5. 改进建议（Kimi Code 侧）

1. **Plan Agent 的默认 prompt 模板应强制引用 `AGENTS.md`**
2. **增加"项目图谱优先"的元规则** — 类似 `tree-sitter` 的符号索引，Agent 应先查图谱再读源码
3. **支持读取路径白名单/黑名单** — 如 `DO_NOT_READ: docs/spec/v3-agent/`*
4. **Plan Agent 应限制单文件读取深度** — 默认只读前 N 行，除非显式需要全文

---

## 6. 修订记录


| 日期         | 说明                           |
| ---------- | ---------------------------- |
| 2026-06-05 | 初稿：分析 Plan Agent 超时根因，落盘完整路径 |


