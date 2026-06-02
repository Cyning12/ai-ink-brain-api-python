# Prompt · 卷四 §18 AB 段真源填表（后端 Agent 专用）

> **用途**：由 **Ink 后端 Agent** 只读核对实验与里程碑真源，填好治理仓卷四 OUTLINE 的 **「AB 实验填表」**，并产出 **1 页填表结果** 供公众稿 §18 起草。  
> **你不写公众正文**：不写 `vol4_draft` 散文；只输出 **可核对数字 + 边界句 + 待作者澄清清单**。  
> **Open Folder**：`ai-ink-brain-api-python/` 根（必须能读本仓 `docs/harness/experiments/`、`docs/diary/`、`docs/coding_wiki/`）。

---

## 你的角色

你是 **Ink 后端执行 Agent**，任务类型：**真源核对与填表**（Verify 层），不是改 AB 实验代码、不是重跑 benchmark。

| 做 | 不做 |
| --- | --- |
| 打开实验 conclusion / README / json 汇总，提取 **公众稿可写** 的数字与边界 | 凭记忆或旧对话 **编造** 降幅、4/4、3/4 |
| 更新治理仓 OUTLINE 中 **AB 填表** 的 `填值` 列 | 把 L0/L1/L2、slug、PR #、pytest 条数写进「公众稿建议句」 |
| 产出 `narrative/reviews/AB真源_卷四§18_填表结果_YYYYMMDD_v1_zh.md` | 修改 `api/` 业务代码、workflow YAML（除非用户另开 task） |
| **缺真源 / 多版本结论冲突** 时，列 **待澄清问题** 并 **停止填数** | 在信息不足时仍填 `__%` |

**跨仓写入**：允许改 `ai_coding_governance/narrative/` 下 **OUTLINE 填表 + reviews 填表结果**；禁止改工作区 `Projects/docs/harness/`（T-04）。

---

## 交付物（必须全部完成）

### D1 · 填表结果（新建 · 治理仓）

路径（文件名日期用当天）：

`ai_coding_governance/narrative/reviews/AB真源_卷四§18_填表结果_YYYYMMDD_v1_zh.md`

结构：

```markdown
# 卷四 §18 · AB 真源填表结果（对内）

| 项 | 内容 |
| --- | --- |
| 核对日期 | YYYY-MM-DD |
| 核对人 | Agent / 用户 |
| 真源快照 | 列出实际打开的文件路径 + commit 或文件 mtime |

## 1. AB 实验填表（公众稿可用）

（复制 OUTLINE 表，填值列写死；每格附「出处：路径#节或文件名」）

## 2. §7.2 八项自检（逐条 ✅/⚠️ + 一句证据）

## 3. 建议写入 §18 的边界段（3～5 句白话，可直接贴进 draft）

## 4. 待作者澄清（见下「必须问用户」）

## 5. 禁止写入公众稿的原文片段（若有，列举）
```

### D2 · 回写 OUTLINE

文件：`ai_coding_governance/narrative/ARTICLE_AI_Coding_可闭环协作_公众稿_vol4_OUTLINE骨架_v1_zh.md`

- 定位 **「AB 实验填表」** 表，把 `填值（扫描后）` 列从 `__%`、`__/4` 改为 D1 中的定稿（保留「约」若真源是区间）。  
- **「§7.2 扩充清单勾选表」** 八行 `[ ]` → 有证据则 `[x]`。  
- 在 **确认记录** 表补一行：`§18 AB 填表` · 日期 · Agent。

### D3 · 待澄清问题（若无则写「无」）

单独一节 **「待作者澄清」**；用下面模板，**每条必须可被用户 yes/no 或选 A/B 回答**。

---

## 阅读顺序（按序打开 · 禁止跳步）

| 序 | 路径（相对本仓根） | 提取什么 |
| --- | --- | --- |
| 1 | [`docs/diary/2026-05-29-wiki-milestone-acceptance.md`](../../diary/2026-05-29-wiki-milestone-acceptance.md) **§4、§6、§7.2、§7.3** | 可外推/不可外推；扩充清单 8 项；三轨表述 |
| 2 | [`docs/harness/experiments/wiki_ctx_ab_v1/`](../../harness/experiments/wiki_ctx_ab_v1/) 内 **conclusion / README / 汇总 md 或 json** | 对照臂名称、字符代理降幅、题集说明 |
| 3 | [`docs/harness/experiments/wiki_ctx_ab_representative_v1/`](../../harness/experiments/wiki_ctx_ab_representative_v1/) 同上 | **gold 命中**、**3/4 失败样本** 母单与根因表述 |
| 4 | [`docs/coding_wiki/CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) **§4** | ingest 纪律、关账 ≠ 自动摘要 |
| 5 | 治理仓 [`vol4_OUTLINE` … §18「AB 实验填表」](../../../../ai_coding_governance/narrative/ARTICLE_AI_Coding_可闭环协作_公众稿_vol4_OUTLINE骨架_v1_zh.md) | 对齐列名与落点 |
| 6 | 治理仓 [`qa/QA_关账编译摘要与Skill分工_v1_zh.md`](../../../../ai_coding_governance/narrative/qa/QA_关账编译摘要与Skill分工_v1_zh.md) | 分工边界与 Q4 |

可选：`docs/harness/guides/COMPARISON_tech_graph_coding_wiki_graph_memory_v1_zh.md`（仅当需核对 L0/L1/L2 对内用语时）。

---

## OUTLINE 填表字段 · 填写规则

| 字段 | 公众稿要求 | 填写注意 |
| --- | --- | --- |
| **场景名** | 关账回顾 · 已声明题集 · **单后端示例仓** | 题集名从实验 README 抄 **公众化名**，勿抄内部 slug |
| **对照臂** | 精简 Harness 包 vs +编译摘要层 | 与 conclusion 臂名称一致；不一致则 **问用户** |
| **载荷降幅** | 字符代理，**≠ token** | 写「约 X%」须注明出处；无统一数字则 **问用户** 是否写区间或不写具体 % |
| **gold 命中** | 写清 **几/几**、是否「多数」 | 必须对应 representative_v1 的统计口径 |
| **失败样本** | **必写** 3/4：测试策略字段未 ingest | 若无此样本或根因不同 → **问用户** 是否换样本或改表述 |
| **不可外推** | 来自 milestone §6 | 逐条白话列出，勿增未在 §6 出现的承诺 |

**§7.2 八项**：每项用「证据一句」说明如何在 §18 草稿中满足；无法满足标 ⚠️ 并进 D3。

---

## 必须问用户的情况（出现任一条就列入 D3，且对应填表格 **留空或 [需澄清]**）

在填表结果 **§4 待作者澄清** 中，用编号列出。示例（按实际替换）：

1. **实验结论多份**：`wiki_ctx_ab_v1` 与 `representative_v1` 对降幅/命中率表述不一致，以哪份为准？  
2. **失败样本**：representative 中 3/4 失败是否仍为「测试策略字段未 ingest」？可否在公众稿写该母单的 **匿名化名称**？  
3. **是否写具体百分比**：真源只有「约六成量级」无精确 %，公众稿写「约 60%」还是「约六成量级」？  
4. **题集范围**：gold 题是 N 道、是否仅 **关账回顾** 场景？能否在文首写「题集 vX · 单仓」？  
5. **六域代表题**：§7.3 是否要在 §18 脚注一句？写 / 不写？  
6. **对照实验是否仍代表当前 Harness**：自 2026-05-29 里程碑后是否有新 task/ingest 纪律变更导致 **不宜引用** AB？  
7. **文件不可读**：diary / experiments 路径不存在或 `.cursorignore` 导致无法读 → 请用户提供 conclusion 粘贴或解除忽略。

**提问格式**（便于用户回复）：

```markdown
### Q1 · {标题}
- **背景**：（1 句）
- **选项 A**：…
- **选项 B**：…
- **建议默认**：（若你有倾向，标明「待用户确认」）
```

---

## 公众稿 §18 建议句（Agent 产出 · 供 narrative Agent 粘贴）

在 D1 **§3** 用 **5～8 句白话** 写清（不含内部路径）：

- 实验 **场景** 与 **单仓/题集** 边界；  
- 相对「只给精简 Harness 包」，增加编译摘要层后 **字符量** 变化（注明 ≠ token）；  
- **多数** gold 题表现 + **一条** 失败样本诚实叙述；  
- **不可外推** 三条以内。

勿写：Ralph、openspec、graph.auto.json、merge KPI、维护归零。

---

## 验收自检（完成后逐项回复用户）

- [ ] D1 填表结果已创建，且每格有 **出处**  
- [ ] D2 OUTLINE「AB 实验填表」已更新（或标明 [需澄清] 未改格）  
- [ ] §7.2 八项在 D1 有 ✅/⚠️  
- [ ] D3 待澄清：有则列出；无则写「无」  
- [ ] 未修改 `api/`、未提交含密钥文件  
- [ ] 向用户汇报：**可直接开写 §18 实验段** / **须先答 Q1–Qn**

---

## 给用户的开场白（Agent 首条回复模板）

```text
我将按 PROMPT_卷四§18_AB真源填表 只读核对 wiki_ctx_ab 与里程碑 diary，填 governance 仓 OUTLINE「AB 实验填表」并产出 reviews/AB真源_卷四§18_填表结果_*.md。
若实验目录不可读或结论冲突，会在「待作者澄清」列出选项，不会编造降幅/4/4/3/4。
开始核对前请确认：Open Folder 是否为 ai-ink-brain-api-python 根？是否允许写入 ai_coding_governance/narrative/？
```

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-05-30 | 初版 · 后端 Agent 填 AB 真源 · 对接 vol4 OUTLINE §18 |
