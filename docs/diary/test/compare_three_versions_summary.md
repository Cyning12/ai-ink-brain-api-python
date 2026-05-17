# 三版本演进总结：从「全量深读」到「索引导航」再到「混合交付」

> 记录日期：2026-04-28  
> 实验背景：围绕「新 Agent / 新人冷启动理解当前项目」这一工程问题，先后进行了三轮对比实验，逐步收敛出可复用的工作流。  
> 输出目录：`docs/diary/test/`

---

## 实验设计速览

| 轮次 | 方案 A（无技术图谱·全量查询） | 方案 B（技术图谱主导·索引导航） | 核心改进方向 |
|------|------------------------------|--------------------------------|-------------|
| **V1** | 禁用图谱，直接通读代码/SQL/tests | 强制先读图谱，再抽样核验代码 | 建立基线：两种极端路径的产出差异 |
| **V2** | 同 V1，统一 token/时间计量口径 | 同 V1，统一计量口径 | 解决 V1 计量混乱问题，使对比可量化 |
| **V3** | 禁用图谱正文，但放行 `manifest.json`/`contract_manifest.json` 作为门禁真值 | 强制走图谱索引，增加「图谱 vs 代码」一致性核验 | 引入 KPI 权重（易交接>可靠性>省钱>省时），补齐 A 的门禁闭环 |
| **Patch** | V3 基础上，强制配方卡包含 manifest/contract/CI | V3 基础上，subagent 逐项核验代码/SQL/CI | 让 A/B 在「门禁必做」上收敛，对比聚焦「信息形态差异」 |
| **Hybrid V1** | — | — | 取 A/B 之长，形成单一推荐 Prompt，取代对抗式二选一 |

---

## 第一轮（V1）：建立基线，发现计量问题

### 对比方向
- **A（无技术图谱·全量查询）**：通读 28 个核心文件（含 tests），产出「实现讲义」风格文档，行级锚点密集，适合直接改代码。
- **B（技术图谱主导·索引导航）**：先读 20+ 图谱文件建立心智地图，再抽样核验 20+ 代码/SQL 文件，产出「索引 + 契约」风格文档，适合快速定位边界。

### 关键发现
| 维度 | 结果 |
|------|------|
| 时间 | A 自报 ~47s（明显失真），B 自报 ~32min；时间统计口径不一致，**不可直接比较** |
| Token | A ~114k，B ~97.8k；但输出 token 换算系数不一致（A 用 ×1.2/字符，B 用 /4），**不可直接比较** |
| 可审计性 | B 更强（图谱锚点 + SQL 行号）；A 结论更丰富但存在「未读文件却给细节」的风险 |
| 核心差异 | A 偏「实现导向通读」，B 偏「索引导向抽样」 |

### 改进方向
- **统一计量口径**：输入统一「每行 12 tokens」，输出统一「4 字符 ≈ 1 token」。
- **统一时间统计**：用外部墙钟计时（Prompt 开始 → 结果落盘）。
- **统一阅读深度约束**：关键函数必须读全，禁止「只读前 150 行」导致后半段行为未确认。

---

## 第二轮（V2）：统一口径，量化成本差异

### 对比方向
- 在 V1 基础上，强制 A/B 使用同一套 token/时间估算公式，使对比具备统计学意义。

### 关键发现
| 维度 | 结果 |
|------|------|
| Token | A ~75k，B ~68.5k；**B 节省约 8.7%**（主要来自不读 tests + 图谱内容更浓缩） |
| 时间 | A ~28min，B ~36min；**B 并未更快**（读图谱 ~8min 为刚性成本，与代码核验叠加） |
| 质量 | A 含 tests 作为行为契约证据，更适合「准备动刀」；B 的 manifest/contract/CI 视角更强，更适合「长期维护」 |
| 核心差异 | **省 token ≠ 省时间**；B 的 time 优势需要进一步收敛代码核验范围才能体现 |

### 改进方向
- **引入 KPI 权重**：不再单纯比较成本，而是按「易交接 > 可靠性 > 省钱 > 省时」加权评分。
- **补齐 A 的门禁短板**：A 的产出容易漏掉 manifest/contract/CI 闸门，需在 Prompt 中强制要求。
- **收敛 B 的代码核验范围**：B 若「又读图谱又读大段代码」，时间优势会被抵消；需严格按图谱锚点只读关键函数。

---

## 第三轮（V3 + Patch）：KPI 加权 + 门禁收敛 + 最终合并

### 对比方向
- **A（Patch 版）**：禁用图谱正文，但强制放行 `manifest.json`/`contract_manifest.json` 作为门禁真值；配方卡必须包含 manifest/contract/CI 动作。
- **B（Patch 版）**：强制走图谱索引，增加 subagent 逐项核验；同样强制配方卡包含门禁动作。

### 关键发现
| KPI | 权重 | 胜者 | 依据 |
|------|------|------|------|
| P1 易交接 | 40% | **平局/依场景分裂** | A 更适合「改后端实现」（行级锚点、Legacy 细节）；B 更适合「维护图谱与跨端契约」（SSE 配方、CI 索引） |
| P2 可靠性 | 35% | **B 略胜** | B 显式标出「PROJECT_CONFIG 与 workflows 矛盾」「图谱 RPC 缩写与 SQL 全名差异」等漂移 |
| P3 省钱 | 15% | **B 胜** | A ~92.9k tokens，B ~67.4k tokens；B 的图谱先行策略在同等产出质量下更省 |
| P4 省时 | 10% | **A 胜** | A ~33min，B ~60min；读图谱 ~25min 为显式增量 |

### Patch 的核心效果
- **A 已补齐门禁叙事**：manifest/contract/manifest_check/contract_check 已写进接手清单与配方卡，与 B 在「门禁必做」上收敛。
- **差异转向信息形态**：A 偏「实现讲义」（行级锚点、踩坑细节），B 偏「索引 + 元层防漂移」（图谱—manifest—契约—CI 一条龙）。

### 改进方向 → Hybrid V1
- **不再对抗式二选一**：日常默认执行「混合方案」——以 B 为导航与漂移提示，以 A 为深读与改码手册。
- **沉淀为单一 Prompt**：将 A 的行级锚点、B 的图谱索引、Patch 的门禁共识合并为 `prompt_AB_hybrid_v1.md`。
- **四张配方卡固定化**：新增端点（manifest）、检索策略（RRF/threshold）、ingest（维度/fts_tokens）、SSE 契约（contract）——覆盖后端改动 80% 场景。

---

## 三版本演进脉络图

```
V1（基线）          V2（量化）           V3（加权）           Patch（收敛）         Hybrid V1（合并）
  │                   │                   │                    │                    │
  ├─ 计量混乱          ├─ 统一口径          ├─ 引入 KPI           ├─ A 补齐门禁          ├─ 单一推荐 Prompt
  ├─ 时间失真          ├─ token 可比较       ├─ 可靠性优先         ├─ B subagent 核验      ├─ 四张配方卡固定
  ├─ 输出系数不一       ├─ 发现「省 token      ├─ A 强制 manifest    ├─ 差异转向形态         ├─ 取代对抗式 A/B
  │                   │   ≠ 省时间」        │   /contract         │   （讲义 vs 索引）     │
  └─ 结论：不可比      └─ 结论：B 省 8.7%    └─ 结论：B 加权胜       └─ 结论：合并最优        └─ 结论：可复用资产
                      token，但不省时间                         （日常默认 Hybrid）
```

---

## 可复用资产清单

| 资产类型 | 文件路径 | 用途 |
|---------|---------|------|
| 混合方案 Prompt | `docs/diary/test/prompt_AB_hybrid_v1.md` | 团队默认 onboarding Prompt |
| 混合方案执行结果 | `docs/diary/test/result_AB_hybrid_v1.md` | 参考产出模板 |
| 实验协议 | `docs/diary/test/experiment_hybrid_v1_protocol.md` | Hybrid 定位与落盘路径说明 |
| 三版本对比总结 | `docs/diary/test/compare_three_versions_summary.md` | 本文件，演进脉络与决策依据 |
| V1 对比 | `docs/diary/test/compare_core_A_vs_B.md` | 基线对比（计量混乱版） |
| V2 对比 | `docs/diary/test/compare_core_A_vs_B_v2.md` | 统一口径版 |
| V3 对比 | `docs/diary/test/compare_core_A_vs_B_v3.md` | KPI 加权版 |
| V3 Patch 对比 | `docs/diary/test/compare_core_A_vs_B_v3_patch.md` | 门禁收敛版 |
| 门禁脚本 | `tools/tech_graph_manifest_check.py` | 端点/RPC/表/env/anchors 校验 |
| 门禁脚本 | `tools/tech_graph_contract_check.py` | SSE 后端 truth vs contract vs 前端消费 |
| 门禁脚本 | `tools/tech_graph_drift_check.py` | 代码真值 vs 图谱覆盖度校验 |
| CI Workflow | `.github/workflows/tech-graph.yml` | manifest_check CI |
| CI Workflow | `.github/workflows/tech-graph-contract.yml` | contract_check CI（跨仓） |

---

## 下一步（务实，已落地）

1. ✅ **日常接手**：默认执行 Hybrid V1（已产出 `prompt_AB_hybrid_v1.md` + `result_AB_hybrid_v1.md`）。
2. ✅ **文档治理**：漂移防线中显式标注了 `PROJECT_CONFIG` 与 `.github/workflows/` 的矛盾、`99_spec.md` 对 `.cursorrules` 的过时引用——可作为下一轮文档修复的 TODO。
3. ⏳ **深度重构**：以 Unified Chat 为基准，逐步收敛 Legacy `/api/py/chat` 的重复逻辑（`_parse_match_threshold`、embedding 降级、keyword fallback 等）——这是代码层面的后续工作，不在本次文档实验范围内。
4. ✅ **资产沉淀**：所有对比文件、Prompt、协议、结果均已落盘 `docs/diary/test/`，可直接用于团队 Wiki 或 onboarding 手册。

