# ChatBI Intent 站点上下文配置（intent_hints）— SPEC 目录

> **性质**：L0 总览 + 分步 L1 子规 + YAML Schema；**行为规格**（SDD），实现前须开 task 并走 Harness。  
> **状态**：`draft`（2026-06-04 · 分支 `task/chatbi-graph-harness-showcase-v1`）  
> **freeze_id（建议）**：`CHATBI-INTENT-HINTS@2026-06-09`（Step 1 合入后可人审冻结）  
> **SDD 过程**：[`../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md)

---

## 0. 一句话

为 Unified Chat **Intent 识别**增加外置 **`intent_hints.yaml`**（仿 `value_hints.yaml`），分 **三步（C-lite → C-mid → C-full）** 解决 Portfolio 演示站 **Q4 / 人名 / 个人经历** 等高置信误路由 `direct_answer` 问题；**6/9 前至少交付 Step 1**。

---

## 文档地图（大纲 · 勿合并为单文件）

| 序号 | 文件 | 层级 | 读谁 |
| --- | --- | --- | --- |
| **0** | 本 README | 索引 | 所有人 |
| **1** | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) | **L0 总览** | 立项、排期、Harness 10 帽 |
| **2** | [`SPEC-ChatBI-Intent-Hints-Analysis-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Analysis-v1_zh.md) | L1 问题分析 | 22 审核、50 复检、实现前必读 |
| **3** | [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) | L1 配置契约 | 30 实现 · YAML 作者 |
| **4** | [`SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md) | L1 **Step 1** | 6/9 硬门槛 · 首 PR |
| **5** | [`SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md) | L1 **Step 2** | 6/9 有余力 · 第二 PR |
| **6** | [`SPEC-ChatBI-Intent-Hints-Step3-C-Full-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Step3-C-Full-v1_zh.md) | L1 **Step 3** | 6/9 后 · Graph 对接 |

---

## 阅读顺序

1. **Overview** §0～§3（背景、目标、三步边界）  
2. **Analysis**（根因、Timeline 证据、与 A/B 旧方案关系）  
3. **Schema**（YAML 字段、env、加载语义）  
4. 按排期打开 **Step 1 → 2 → 3** 对应验收表  

---

## 关联真值（只链、不复制）

| 项 | 路径 |
| --- | --- |
| Portfolio 五问 / ingest | [`../governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) |
| 投递冲刺 | [`../governance/投递冲刺_20260609_v1_zh.md`](../governance/投递冲刺_20260609_v1_zh.md) §2 |
| Intent V2 现行 | [`../v2-agent/SPEC-ChatBI-V2-Intent.md`](../v2-agent/SPEC-ChatBI-V2-Intent.md) |
| Intent 技术债母单 | [`../../tasks/active/task_chatbi_v3_intent_classification_debt_v1.md`](../../tasks/active/task_chatbi_v3_intent_classification_debt_v1.md) |
| value_hints 参照实现 | `api/text2sql_value_hints.py` · `docs/text2sql/v1/value_hints.yaml` |
| Graph P0 / 路线图 | [`../research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) |
| PR #106 / #107 | 已合 `main` · 见 Overview §5 |

---

## 实现落盘位置（代码 · 规划）

| 阶段 | 新增/修改（概要） |
| --- | --- |
| Step 1 | `docs/chatbi/v1/intent_hints.yaml` · `api/intent_hints.py` · `api/intent_agent.py` · 测试 |
| Step 2 | `api/intent_router.py` · 可选 `api/agent.py` 仲裁 · 测试 |
| Step 3 | `PROJECT_CONFIG` · `.env.example` · Graph route 共用 · RUNBOOK 一句 |

> **非范围**：`api/graph/*` 行为变更（Step 3 仅 **预留** 注入点）；`unified_chat_graph.py` stub 不在本 Epic 修 Portfolio。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版：目录 + L0/L1 六文 · 三步 C-lite/mid/full |
