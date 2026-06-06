# SPEC — 治理：docs/ 噪音 / 重复 / 冲突 · 全量盘点与需求总纲（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **freeze_id** | `GOV-DOCS-NOISE-INVENTORY@2026-06-06` |
| **性质** | **需求总纲 / 盘点 SPEC**；本文 **不** 替代 L0 架构真值，**不** 要求一次性删改过程工件 |
| **盘点基线** | 2026-06-06 · 本仓 `ai-ink-brain-api-python` · Agent 只读分析会话产出 |
| **导图（默认入口）** | [`README.md`](./README.md) — 日常 **只读导图**；本文为正文 SPEC |
| **关联** | [`docs/coding_wiki/CODING_WIKI.md`](../../../coding_wiki/CODING_WIKI.md) §1 L0/L1/L2 · [`docs/README.md`](../../../README.md) · [`AGENTS.md`](../../../../AGENTS.md) · [`.cursor/rules/08-docs-diary.mdc`](../../../../.cursor/rules/08-docs-diary.mdc) |
| **执行 task** | **待开** · 建议 slug：`task_governance_docs_noise_cleanup_v1`（按本文 §8 分批） |

---

## 0. 完成态（一句话）

将本仓 `docs/` 的 **体量分布、分层边界、真冲突清单、历史遗留与治理优先级** 冻结为 **单一 SPEC**；后续细节治理 task **按 P0→P3 分批** 执行，**禁止** 以 diary / Wiki / flows 替代 L0，**禁止** 默认 glob 全量 `docs/harness/invokes/`。

---

## 1. 背景与目标

### 1.1 背景

Harness V2 落地后，本仓 `docs/` 体量显著膨胀（约 **1095** 个 Markdown 文件）。其中大量为 **有意分层** 的过程工件（invoke / review / reinspect / diary），但对 Agent 与人类新人而言，存在：

- **导航入口不一致**（`AGENTS.md` vs `docs/README.md` vs 根 `README.md`）
- **少数过时指针**（如 `invokes/README` 称 `reviews/` 已移除）
- **目录名易混**（`docs/tech_graph/` vs `docs/_tech_graph/`）
- **历史快照与 L0 真值并存**（`flows/`、`delivery/v0.2.0-code-rag/`）

### 1.2 目标

| # | 目标 |
| --- | --- |
| G1 | 冻结 **2026-06-06 基线盘点**（体量、分层、冲突寄存器） |
| G2 | 给出 **可验收的分批治理计划**（P0～P3），供后续 task 引用 |
| G3 | 统一 **Agent 最小无噪音读序** 表述，供 AGENTS / docs/README 对齐 |
| G4 | 明确 **非目标**，避免误删 Harness 审计链 |

### 1.3 非目标

- **不** 删除 `docs/harness/invokes/`、`reviews/`、`reinspect_results/` 历史全文（审计链保留）
- **不** 合并或重写 `docs/tasks/done/` 113 份 task 正文
- **不** 在本 SPEC 内直接修改 `api/` 或 CI
- **不** 将 `docs/showcase/` 对外叙事稿纳入实现真值
- **不** 一次性收敛全部 20 份 `spec/governance/` Wiki 批次文档（留 P3）

---

## 2. 体量基线（2026-06-06）

### 2.1 `docs/` 子目录文件数

| 目录 | 文件数 | 性质 |
| --- | ---: | --- |
| `docs/harness/` | **512** | 过程工件（invoke / review / experiment / prompts） |
| `docs/diary/` | **257** | 非必读、易过时留证 |
| `docs/tasks/` | **206** | 任务单 + review / reinspect 落盘 |
| `docs/spec/` | **80** | SDD 规格 + 治理 SPEC |
| `docs/showcase/` | **41** | 对外展示 / 叙事稿 |
| `docs/coding_wiki/` | **33** | L2 蒸馏 Wiki |
| `docs/text2sql/` | **25** | Text2SQL 专题 |
| `docs/delivery/` | **23** | 早期交付框架 |
| `docs/_tech_graph/` | **23** | **L0 架构真值** |
| `docs/UI/` | **4** | 前后端协议 |
| `docs/tech_graph/` | **2** | **遗留**闸口留痕（非 L0 目录） |
| `docs/flows/` | **1** | 端到端快照 |
| `docs/chatbi/` | **1** | 专题 pointer |
| `docs/meta/` | **1** | PROJECT_CONFIG 真值表 |

**结论**：约 **70%** 文档为 Harness 执行链产物与 diary 留证；对日常改代码 Agent，**禁止默认 glob 全树**（规则已存在于 `AGENTS.md`、`.cursor/rules/08-docs-diary.mdc`）。

### 2.2 Harness 细分

| 路径 | 文件数 | 说明 |
| --- | ---: | --- |
| `docs/harness/invokes/` | 359 | 含 `by-task/<slug>/`（41 个 task 目录）+ 根目录遗留 1 个 README |
| `docs/harness/reviews/` | 66 | **22 帽**任务审核 |
| `docs/harness/experiments/` | 52 | Wiki-CTX-AB 等实验 |
| `docs/harness/prompts/` | 24 | 帽子 / 模板真值 |
| `docs/harness/guides/` | 6 | RUNBOOK / KPI |
| `docs/harness/linters/` | 1 | — |

### 2.3 Tasks 细分

| 路径 | 数量 | 说明 |
| --- | ---: | --- |
| `docs/tasks/active/` | 11 | 进行中 |
| `docs/tasks/done/` | 113 | 已完成 |
| `docs/tasks/legacy/` | 6 | 历史命名 / 缺 `状态` |
| `docs/tasks/specs/` | 4 | `SPEC-*.md` |
| `docs/tasks/review_results/` | 3 | **20 帽**短评 |
| `docs/tasks/reinspect_results/` | 55 | **50 帽**三方复检 |

### 2.4 Diary 细分

| 路径 | 数量 | 说明 |
| --- | ---: | --- |
| `docs/diary/` 根目录 `*.md` | 34 | 日期总结 / 主题稿 |
| `docs/diary/jsonPKmermaid/` | 94 | 图谱行为实验轨 · **非必读** |
| `docs/diary/harness-archive/` | 63 | 迁移的旧 invoke / review |

### 2.5 重复 basename（模板化落盘 · 非内容重复）

| basename | 出现次数 | 说明 |
| --- | ---: | --- |
| `README.md` | 54 | 各子目录索引 |
| `scorecard.md` | 8 | Loop 评分卡 |
| `LOOP_MANIFEST.md` | 8 | Loop 清单 |
| `PROMPT_LOOP_22_to_CLOSE_v1.md` | 8 | Loop 模板复制 |
| `PROMPT_TASK_22_to_CLOSE_v1.md` | 8 | Loop 模板复制 |
| `PROMPT_START_full_chain_v1.md` | 7 | Loop 模板复制 |

→ 全文搜索易命中「假重复」；**不**视为需合并的正文冲突。

---

## 3. 文档分层（设计如此 · 非 bug）

项目已明确 **L0 / L1 / L2** 分工（[`CODING_WIKI.md`](../../../coding_wiki/CODING_WIKI.md) §1）：

```text
L0 真值    → docs/_tech_graph/、graph.json、_contract_manifest、PROJECT_CONFIG
L1 执行    → docs/tasks/、docs/harness/、docs/spec/
L2 回顾    → docs/coding_wiki/（明确「不得替代 L0」）
非必读     → docs/diary/、jsonPKmermaid 实验轨
```

### 3.1 看似重复 · 实际分工

| 内容 | 多处出现 | 关系 |
| --- | --- | --- |
| RAG 流程 | `_tech_graph/10_flow_*.ai.md` + `flows/rag-chat/` + Wiki syntheses | **部分重叠** · flows 为快照 · 见 §4.2 |
| ChatBI 规格 | `spec/v3-agent/`（主）+ `spec/v2-agent/`（冻结参考） | **有意并存** |
| 任务状态 | `tasks/done/` 全文 + Wiki `syntheses/` 摘要 | **L1 + L2** |
| Agent 入口 | `AGENTS.md` + `docs/README.md` + 12×`.mdc` | **导航重复** · 见 §4.1 |
| Harness 规划 | 本仓 `HARNESS_V2_PLAN.md` + 工作区 `Projects/AGENTS.md` §8 | **跨仓镜像** · 有漂移风险 |

### 3.2 审查落盘四目录（易混 · 非互斥）

| 路径 | 帽 | 文件量 | 职责 |
| --- | --- | ---: | --- |
| `docs/harness/reviews/` | **22** | 66 | 任务审核书面结论 |
| `docs/tasks/review_results/` | **20** | 3 | SPEC/task 短评 |
| `docs/tasks/reinspect_results/` | **50** | 55 | 三方复检 |
| task 正文 | 30/40 | — | 结论回填 |

---

## 4. 真冲突与导航不一致（冲突寄存器）

> **维护**：后续治理 task 关闭项时，在本表更新「状态」列。

| ID | 严重度 | 现象 | 真值 / 期望 | 建议修复 | 状态 |
| --- | --- | --- | --- | --- | --- |
| **C1** | **高** | `docs/harness/invokes/README.md` 写「**不使用已移除的** `harness/reviews/`」 | `reviews/` **仍存在** 66 文件；`reviews/README.md` 定义 **22 帽**落盘；`HARNESS_V2_PLAN.md` 仍引用 | 更正 invokes/README 表述为「22→reviews/；20→review_results/；50→reinspect_results/」 | `open` |
| **C2** | **中高** | `docs/README.md` §1 建议理解端到端读 **`docs/flows/`** | `AGENTS.md` 改拓扑读 **`docs/_tech_graph/`**；flows 仅 **2026-04-16** Legacy chat 快照 | docs/README 改为：端到端 **优先 L0**；flows **仅历史快照** | `open` |
| **C3** | **中** | `docs/tech_graph/`（2 文件）与 `docs/_tech_graph/`（L0）目录名易混 | L0 唯一目录为 **`docs/_tech_graph/`** | 在 `docs/tech_graph/README.md` 加 POINTER → `_tech_graph` + gate 留痕说明 | `open` |
| **C4** | **中** | `PROJECT_CONFIG` 描述 **`.cursorrules` 为历史/兼容** | 仓库 **已无** `.cursorrules` | PROJECT_CONFIG 更新为「已移除；真值仅 `.mdc`」 | `open` |
| **C5** | **低中** | 根 `README.md` 环境变量 / 端点列表不完整 | 缺 Unified Chat 等新端点；完整表在 PROJECT_CONFIG | 根 README 加 pointer 或补 1 行 Unified 入口 | `open` |
| **C6** | **低** | `HARNESS_V2_PLAN.md` 写真值「本文件 + AGENTS」；`AGENTS` 写细则在 `harness/README` | 实际：**task + spec + harness prompts** 为执行真值 | 三份互链「读序索引」；不在 SPEC 内争权威 | `open` |

### 4.1 导航层重复（可接受 · 需对齐读序）

当前 Agent 可能接触 **4+ 层入口**：

```text
根 README.md          → 开发者快速上手（英文 · 偏部署）
AGENTS.md             → Agent 导航（中文 · 7 步读序）
docs/README.md        → docs 分类地图（中文 · 含规整 TODO）
.cursor/rules/*.mdc   → 12 条强制规则（与 AGENTS 规则索引重复摘要）
用户 Cursor rules     → 执行报告等（部分与 01-agent-observability 重叠）
Projects/AGENTS.md    → 工作区跨仓调度（Open 子仓时可能注入）
```

**重复类型**：

- **AGENTS ↔ .mdc**：`RULES_AUTO_GENERATED` 表与 12 个 `.mdc` 一一对应 — 索引重复，正文在 mdc
- **AGENTS ↔ docs/README**：读序 **不完全一致**（flows vs _tech_graph）→ 见 **C2**
- **CLAUDE.md**：仅 `@AGENTS.md` — 无额外噪音

---

## 5. 历史遗留 / 低维护噪音

| 路径 | 问题 | 建议认知 | 治理动作 |
| --- | --- | --- | --- |
| `docs/delivery/v0.2.0-code-rag/` | 早期 SDD+TDD+Harness 交付包 | 已被 `docs/spec/` + `docs/harness/` supersede | P1 文首标 `archived` |
| `docs/flows/rag-chat/v1_2026-04-16_*.md` | 仅 1 个快照 | Legacy `/api/py/chat`；落后于 Unified/ChatBI | P1 加 superseded 说明 |
| `docs/tasks/legacy/` | 6 个旧命名 task | 待消化（`docs/README.md` §4 TODO） | P2 规范化 `状态` 或归档 pointer |
| `docs/tasks/done/` | 113 文件 | 体量大但合理 | 靠 `_views/done.md` + Wiki syntheses |
| `docs/diary/jsonPKmermaid/` | 94 文件 | 实验轨 · 规则已标非必读 | 不删 · 不默认遍历 |
| `docs/showcase/` | 41 文件 | 对外叙事 · **非实现真值** | 不纳入 Agent 必读 |
| `docs/spec/governance/` | 20 文件 | Wiki/Harness 治理线膨胀 | P3 收敛为 roadmap + changelog |

---

## 6. 总体判断矩阵

| 类别 | 严重程度 | 说明 |
| --- | --- | --- |
| Harness invoke/review/diary 体量 | 中（噪音） | 设计如此；应禁止默认 glob |
| L0/L1/L2 多层 | 低 | 有 SPEC 约束；Wiki 非第二真值 |
| 导航入口不一致 | **中高** | C1/C2 需优先修 |
| `docs/tech_graph/` 遗留 | 中 | C3 命名易混 |
| `delivery/v0.2.0` | 低 | 历史包 |
| 治理 SPEC 膨胀 | 中 | P3 长期 |
| 根 README 过时 | 低中 | C5 |

**一句话**：项目 **不是**「文档混乱到无法维护」，而是 **Harness V2 + Wiki 试点 + diary 留证** 叠加的高体积过程库；需警惕 **少数过时指针** 与 **多入口读序不一致**。

---

## 7. Agent 最小无噪音读序（canonical · 待写入 AGENTS / docs/README）

改代码 / 改契约时 **仅** 读：

```text
1. docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
2. docs/_tech_graph/（python tools/tech_graph_graph_query.py 按需）
3. docs/tasks/RECENT_TASK_SCHEDULE.md → active/task_*.md
4. 涉 ChatBI → docs/spec/v3-agent/
5. 关账回顾 → docs/coding_wiki/syntheses/<slug>.md
```

**刻意不读**（除非 task / 用户 `@` 路径）：

- `docs/diary/` 全树
- `docs/harness/invokes/` 全量 glob
- `docs/showcase/`
- `docs/delivery/`（除非 task 指向）
- `docs/flows/`（除非做历史对比）

---

## 8. 分批治理计划（供后续 task 引用）

### 8.1 P0 — 修真冲突指针（最小扰动 · 建议首个 task）

| # | 交付 | 文件 | 验收 |
| --- | --- | --- | --- |
| P0-1 | 更正 reviews 表述 | `docs/harness/invokes/README.md` | 全文无「reviews 已移除」；分工表与 `reviews/README` 一致 |
| P0-2 | 对齐端到端读序 | `docs/README.md` §1 | flows 降为「历史快照」；L0 `_tech_graph` 优先 |
| P0-3 | tech_graph 遗留 POINTER | 新建 `docs/tech_graph/README.md` | 链至 `_tech_graph`；说明 2 份 gate 为留痕 |

**建议 `test_strategy`**：`not_applicable`（纯 docs；无 api 变更）

### 8.2 P1 — 标 archived / superseded

| # | 交付 | 验收 |
| --- | --- | --- |
| P1-1 | `docs/delivery/v0.2.0-code-rag/README.md` 文首 archived 横幅 | 链至 `docs/harness/README` + `docs/spec/` |
| P1-2 | `docs/flows/` 索引（新建 `docs/flows/README.md` 或扩展现有） | 写明 freeze 日期 · Legacy chat · superseded by `_tech_graph` |

### 8.3 P2 — 导航收敛

| # | 交付 | 验收 |
| --- | --- | --- |
| P2-1 | `PROJECT_CONFIG` 更新 `.cursorrules` 段落 | 与仓库现状一致 |
| P2-2 | `AGENTS.md` 与 `docs/README.md` 互链 §7 读序 | 两文件读序表述一致 |
| P2-3 | 根 `README.md` Unified Chat pointer | 或明确「完整契约见 PROJECT_CONFIG §F」 |
| P2-4 | 消化 `docs/tasks/legacy/`（6 文件） | `_views/` 无漏网；或移 done + pointer |

### 8.4 P3 — 治理 SPEC 与 showcase 索引（长期）

| # | 交付 | 验收 |
| --- | --- | --- |
| P3-1 | `spec/governance/` Wiki 批次 SPEC 收敛索引 | 单页 roadmap + 各 batch 状态表 |
| P3-2 | `docs/showcase/README.md` | 标明非实现真值 · 链对外 repo |

---

## 9. 建议后续 task 单骨架

> 执行 Agent 开 task 时可复制本节为 `docs/tasks/active/task_governance_docs_noise_cleanup_v1.md` 起点。

```yaml
状态: pending
范围: 仅后端本仓 docs/ 治理（按 SPEC-Governance-Docs-Noise-Inventory-v1_zh.md 分批）
关联 SPEC: docs/spec/governance/docs-noise-inventory/README.md（导图）
关联 SPEC 正文: docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md
关联图谱: （可选）docs/_tech_graph/
test_strategy: not_applicable  # 纯 docs 指针修正；理由：无 api/契约变更
semi_auto: true
human_gate: （按批次定）
```

**验收标准（P0 母单示例）**：

- [ ] C1/C2/C3 冲突寄存器状态改为 `done`
- [ ] §7 canonical 读序写入 `AGENTS.md` 与 `docs/README.md`
- [ ] 无新增「第二 L0」表述（flows/diary/Wiki 不得标为架构真值）
- [ ] `python tools/gen_agents_md.py`（若改 `.mdc`）与规则索引一致

**失败路径**：

| 触发 | 行为 |
| --- | --- |
| 误删 invoke/review 审计链 | **禁止**；仅改 README / POINTER |
| AGENTS 与 docs/README 仍不一致 | 阻塞关账；回滚至 SPEC §7 表述 |

---

## 10. 与 RECENT / Wiki 的关系

| 文档 | 关系 |
| --- | --- |
| [`RECENT_TASK_SCHEDULE.md`](../../../tasks/RECENT_TASK_SCHEDULE.md) | 本治理线 **不** 压过 ChatBI 业务队列；P0 可在空档插入 |
| [`SPEC-Governance-Wiki-Agent-Readorder-v1.md`](../SPEC-Governance-Wiki-Agent-Readorder-v1.md) | §7 读序 **兼容** Wiki L2 规则；改代码仍 L0 |
| [`docs/README.md`](../../../README.md) §4 TODO | 本 SPEC §8 为 **超集**；执行时同步勾选 docs/README TODO |
| [`README.md`](./README.md) | 导图 · Agent 默认入口 |

---

## 11. VERIFY（本 SPEC 自身）

```bash
test -f docs/spec/governance/docs-noise-inventory/README.md
test -f docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md
rg -n 'GOV-DOCS-NOISE-INVENTORY@2026-06-06' docs/spec/governance/docs-noise-inventory/
rg -n 'C1|C2|C3' docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md
```

---

## 12. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1 初版：Agent 全量分析落盘；基线 1095 md；冲突寄存器 C1–C6；P0–P3 治理计划 |
| 2026-06-06 | v1.1：迁入 `docs-noise-inventory/` 独立目录；新增导图 `README.md` |
