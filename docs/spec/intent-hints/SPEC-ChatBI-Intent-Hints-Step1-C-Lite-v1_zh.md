# SPEC — ChatBI Intent Hints · Step 1（C-lite）（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **阶段** | **Step 1 / 3** · 6/9 **硬门槛** |
| **上级** | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| **Schema** | [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) |

---

## 1. 目标

外置 **`intent_hints.yaml`** + loader + **仅 Prompt 注入**，使 Portfolio **Q4** 与 **刘新宁/经历/成果** 问句在 `prefer=auto` 下稳定 **`rag_search`**，**不** 改 V1 router、**不** 改 Graph、**不** 改 `unified_chat.py` 行为。

---

## 2. 范围

### 2.1 在范围

| # | 交付 |
| --- | --- |
| S1-1 | `docs/chatbi/v1/intent_hints.yaml`（Portfolio 默认稿 · 见 Schema §5） |
| S1-2 | `api/intent_hints.py`：`load_resolved_hints()` · `build_intent_hints_prompt_block()` |
| S1-3 | `api/intent_agent.py`：`_llm_decide_v2` 注入配置块 |
| S1-4 | `tests/test_intent_hints_loader.py`（或等价）· 加载/缺失/禁用 |
| S1-5 | `tests/test_intent_agent_accuracy.py`：**追加** 2～4 条 Portfolio `IntentCase`（stub 路径可断言） |
| S1-6 | `.env.example` 注释 · `INTENT_HINTS_*`（实现 PR 同步 PROJECT_CONFIG） |

### 2.2 非范围

- `api/intent_router.py` 改动（留 Step 2）  
- `api/agent.py` 仲裁（留 Step 2）  
- `api/tools.py` · `direct_answer` system prompt（可选后续）  
- `api/graph/*` · `unified_chat_graph.py`  
- 跑生产 sync / 改前端 content  

---

## 3. 实现要点

### 3.1 `intent_hints.py`（仿 value_hints）

```text
_resolve_hints_path() → Path | None
load_hints(path) → dict | None
load_resolved_hints() → dict | None
build_intent_hints_prompt_block(hints) → str   # 空则 ""
```

### 3.2 `intent_agent.py`

- 在构建 `prompt` 时：`hints_block = build_intent_hints_prompt_block(load_resolved_hints())`  
- 插入位置：`## 总原则` 与 `## 「通用知识」vs「须查资料」` 之间（或紧接总原则后）  
- **不** 改变 JSON 输出 schema  

### 3.3 可选（同 PR 内小改）

- `api/tools.py` · `rag_search.description` 增半句 Portfolio 语料说明（与 YAML 一致，防 registry 漂移）

---

## 4. 验收标准

### 4.1 功能

- [ ] Q4 逐字句 · Timeline `final_mode=rag` · 有 `rag.sources` · 主 category `resume`  
- [ ] 「刘新宁…优势/看法」· 同上 · 回答含简历要点（百果园/Cursor/Ink 等至少一项）  
- [ ] 「解释一下量子计算，用通俗语言」· 仍 `direct_answer`  
- [ ] YAML 删除或 `INTENT_HINTS_ENABLED=0` · 行为回退现行（降级不 crash）  

### 4.2 工程

- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿  
- [ ] 新增 loader 单测全绿  
- [ ] diff **不含** `api/graph/*`  

### 4.3 可选（本地）

- [ ] `pytest -m intent_eval` 前后 macro-F1 / Portfolio 条目不回归（ diary 留证）  

---

## 5. 建议 task / PR

| 项 | 建议 |
| --- | --- |
| **task_slug** | `chatbi_intent_hints_step1_v1` |
| **分支** | 从 `main` 拉 `task/chatbi-intent-hints-step1-v1`（或续用 showcase 分支若人定） |
| **test_strategy** | `required` |
| **PR 标题** | `feat(chatbi): intent_hints Step1 — YAML 注入 Portfolio Intent` |

---

## 6. 失败路径

| # | 触发 | 系统行为 | 用户可见 |
| --- | --- | --- | --- |
| F1 | YAML 损坏 | 不注入 · 等同现行 | 可能仍误路由 · 日志可选 |
| F2 | Intent LLM 仍判 direct | Step 1 未 100% · Step 2 仲裁补位 | 通史/不知道人名 |
| F3 | 向量库无 resume | rag 空 · 非 Step 1 范围 | 检索空 · 查 ingest |

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版 Step 1 范围与验收 |
