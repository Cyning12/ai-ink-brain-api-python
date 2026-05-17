# Phase·P1 — 双人盲审（gate_ctx_ab）

> **前置**：Phase·P0 已闭环（见 [`reports/conclusion_gate_ctx_ab_final_zh.md`](./reports/conclusion_gate_ctx_ab_final_zh.md) · `accepted`）  
> **符号**：[NOTATION_zh.md](./NOTATION_zh.md)（Reviewer·R1/R2 ≠ Rule·R1–R6）

## 目标

对 **6 条段·S0** 结构化输出（3 题 × 2 arm）做 **KPI·P1 / P2** 双人盲审，补强启发式 F1；**不**再跑 LLM。

## 目录

```
fixtures/gate_ctx_ab_v1/p1/
  rubric_v1.yaml          # 子项与 0–2 档位说明
  blind/                  # 评审只看此目录（无 arm）
  admin/sample_manifest.json  # ⚠️ 仅汇总/仲裁前打开（含真实 arm）
  scores/
    score_template.csv
    reviewer_R1.csv       # 由你填写（可复制 template）
    reviewer_R2.csv
    aggregate_p1.md       # aggregate_p1_scores.py 生成
```

## 步骤

### 1. 生成盲审包（已完成可跳过）

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/prepare_p1_blind_pack.py
```

数据来源：[`runs/gate_ctx_ab_v1_s1s2_20260516_152126/`](./runs/gate_ctx_ab_v1_s1s2_20260516_152126/) 内 6×`*_S0.jsonl`。

### 2. 双人打分（盲审）

1. 评审员 **只** 打开 `p1/blind/P1-*.json` + `rubric_v1.yaml`。  
2. 每人复制 `scores/score_template.csv` → `reviewer_R1.csv` / `reviewer_R2.csv`。  
3. 填 `p1_total`、`p2_total`（0–100）；`notes` 可写 evidence 条目 id。  
4. **禁止** 在打分前查看 `admin/sample_manifest.json`。

### 3. 汇总与仲裁

```bash
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/aggregate_p1_scores.py
```

若 `aggregate_p1.md` 标「需仲裁」：第三人打开 manifest + 争议样本，填 `reviewer_R3_arbitration.csv`（可选，格式同 R1）。

### 4. 回写定稿文

将 P1 胜负（按 arm 聚合均值）写入 `conclusion_gate_ctx_ab_final_zh.md` **§6 附录**；**不**自动改写 Rule·R1–R6 硬门槛，除非团队决议调整 charter。

## 验收（P1 完成）

- [ ] `reviewer_R1.csv` + `reviewer_R2.csv` 6 行齐全  
- [ ] `aggregate_p1.md` 已生成；仲裁项有 R3 终值或记录「保留 F1」  
- [ ] 定稿文 §6 增加「P1 盲审摘要」一段
