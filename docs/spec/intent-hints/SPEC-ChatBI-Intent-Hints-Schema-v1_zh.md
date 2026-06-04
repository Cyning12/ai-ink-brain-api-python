# SPEC — ChatBI Intent Hints · YAML Schema 与加载契约（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **上级** | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| **参照实现（规划）** | `api/intent_hints.py`（待建）· 语义对齐 `api/text2sql_value_hints.py` |

---

## 1. 文件位置

| 项 | 真值 |
| --- | --- |
| **默认路径** | `docs/chatbi/v1/intent_hints.yaml`（相对仓库根） |
| **env 覆盖** | `INTENT_HINTS_PATH`（绝对或相对仓库根） |
| **开关** | `INTENT_HINTS_ENABLED` · 默认 **开启**；`0/false/no/off` 关闭 |
| **缺失文件** | loader 返回 `None` · **不抛错** · Intent 行为 = 现行 |

---

## 2. 环境变量（实现 PR 须写入 PROJECT_CONFIG）

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `INTENT_HINTS_ENABLED` | `true`（未设视为开） | 关闭则不读文件、不注入 |
| `INTENT_HINTS_PATH` | （空 → 默认路径） | 覆盖 YAML 位置 |

与现有 Intent env **正交**：`CHATBI_V2_INTENT_LLM`、`INTENT_LLM_MODEL`、`CHATBI_V2_INTENT_TIMEOUT_S`、`INTENT_MIN_CONFIDENCE`。

---

## 3. 加载语义

| 规则 | 说明 |
| --- | --- |
| 编码 | UTF-8 · 允许 UTF-8 BOM（`utf-8-sig`） |
| 解析 | `yaml.safe_load` · 根须为 `dict` |
| 缓存 | 进程内按 **文件 mtime** 缓存（对齐 value_hints） |
| 失败 | YAML 语法错误 / 非 dict → 视为无配置 + 可选 debug 日志 |
| 注入 | 仅 **`build_intent_hints_prompt_block()`** 产出 Markdown 文本块，由 `_llm_decide_v2` 插入 |

---

## 4. YAML Schema（v1）

### 4.1 顶层字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `version` | int | 是 | 当前 **1** |
| `site_mode` | string | 否 | `portfolio` \| `blog` \| `default` · 注入 Prompt 说明 |
| `product_summary` | string | 否 | 多行 · 站点一句话（Portfolio 演示 / content 三类） |
| `persons` | list | 否 | 人名与 RAG 触发语义 · Step 1 起用 |
| `rag_signals` | object | 否 | keywords / regex · **Step 2** 起 router 共用 |
| `direct_answer_exceptions` | list[string] | 否 | 反例说明 · 仅 Prompt 叙述 |
| `few_shots` | list | 否 | 额外 few-shot · 注入 Prompt |
| `arbitration` | object | 否 | **Step 2** · LLM/direct 与 config 冲突时行为 |

### 4.2 `persons[]`

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | 是 | 主显示名 · 如 `刘新宁` |
| `aliases` | list[string] | 否 | 别名 |
| `rag_triggers` | list[string] | 否 | 与 name 共现时倾向 RAG 的动词/名词 · 如 `优势`、`看法`、`经历` |
| `corpus_hint` | string | 否 | 人类可读 · 如 `content/resume/cv-online.md` |

### 4.3 `rag_signals`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `keywords` | list[string] | 并入 V1 `_rag_rule_hits`（Step 2） |
| `regex` | list[object] | `{ pattern, hint }` · Python `re.search` |

### 4.4 `few_shots[]`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `query` | string | 用户问句 |
| `tool` | string | `rag_search` \| `text2sql_query` \| `direct_answer` |
| `reasoning` | string | 1～2 句 |
| `confidence` | float | 可选 · 默认 0.9 |

### 4.5 `arbitration`（Step 2）

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `enabled` | bool | `true` | env `INTENT_HINTS_ARBITRATION` 可覆盖 |
| `on_person_match_force_rag` | bool | `true` | 人名 + trigger 命中 · LLM 选 direct → 改 rag |
| `on_career_span_force_rag` | bool | `true` | `\d+年.*经历` 等 · 同上 |

---

## 5. Portfolio 默认稿（Step 1 随仓提交 · 示例）

```yaml
version: 1
site_mode: portfolio

product_summary: |
  本 Unified Chat 服务 Portfolio 演示站：用户关于个人履历、项目成果、方法论与证据卡的问题，
  应优先检索 content/ 下 methodology、resume、evidence 文稿（已 ingest 至向量库），
  而非通用百科或行业通史。未明确要求「只要通识、不要站内文档」时，选 rag_search。

persons:
  - name: 刘新宁
    aliases: []
    rag_triggers:
      - 看法
      - 优势
      - 评价
      - 经历
      - 成果
    corpus_hint: content/resume/cv-online.md

rag_signals:
  keywords:
    - 经历
    - 履历
    - 简历
    - 11 年
    - AI Coding
    - 混合检索
    - 冷/温/热
  regex:
    - pattern: "\\d+\\s*年.*经历"
      hint: career_span

direct_answer_exceptions:
  - 与项目无关的通识解释（如量子计算通俗解释）
  - 明确不要查站内文档的行业史

few_shots:
  - query: "11 年经历里 AI Coding 相关成果？"
    tool: rag_search
    reasoning: "Portfolio 简历与项目文稿，须检索 resume/*"
    confidence: 0.92
  - query: "聊聊刘新宁在 AI coding 岗位有什么优势"
    tool: rag_search
    reasoning: "问站点演示者个人能力与履历，应查 resume 文稿"
    confidence: 0.91
  - query: "解释一下量子计算，用通俗语言"
    tool: direct_answer
    reasoning: "与站内语料无关的通识"
    confidence: 0.88
```

---

## 6. Prompt 注入块格式（实现约定）

`_llm_decide_v2` 在 `## 总原则` 之后插入：

```markdown
## 站点上下文（配置 · intent_hints.yaml）

{product_summary 段落}

### 须走 rag_search 的 Portfolio 场景
- 问个人经历、履历、成果、评价、优势、看法（尤其涉及下列人物：…）
- …

### 配置 few-shot 补充
…
```

**禁止**在注入块中包含密钥或 `.env` 内容。

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版 schema · env · Portfolio 默认稿 |
