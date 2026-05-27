# SPEC — 治理：图谱 L2 工具链 · 锚点与测试 Manifest（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **freeze_id** | `GOV-L2-ANCHOR-TEST-MANIFEST@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.1 **P2 · L2 工具链** |
| **姊妹 SPEC** | [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)（Wiki↔图谱 · T4） |
| **L0 真值** | [`docs/_tech_graph/99_spec.md`](../../_tech_graph/99_spec.md) · [`_manifest.json`](../../_tech_graph/_manifest.json) |
| **Wiki 测试档案** | [`docs/coding_wiki/CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §8（**叙事**；本 SPEC 管 **机器校验**） |

> **命名澄清**：本 SPEC 的 **「L2 工具链」** = 治理方法论中的 **锚点 / 测试 manifest / CI 门禁** 层，**不是** [`CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) 所称 **L2 编译层**（`docs/coding_wiki/` 目录）。

---

## 0. 完成态（一句话）

建立 **可 CI 执行** 的锚点与测试相关清单纪律：`_manifest.json` / `99_spec` 锚点与源码一致；关键 `ERR_*` / `failure_paths` 与 **测试 manifest 文档** 可互查；Wiki 仅存档 **测试变更叙事**，**不** 充当 coverage 真值。

---

## 1. 背景与目标

| 痛点 | 本 SPEC 应对 |
| --- | --- |
| 图谱锚点漂移、静默过期 | 已有 `manifest_check`、`drift_check`；本 SPEC **收敛验收口径** |
| 测试意图只在 pytest 文件里 | 文档化 **`_test_manifest` 草案** + 与 task `failure_paths` 对齐 |
| 治理仓 L2-1/L2-2 未在本仓落地 | 本仓 **Executable 子集** + 链向治理仓（不双真值） |

**外部参考**（**非**本仓正文真值）：治理仓 `11_REVIEW_L3_L2理论层缺口分析`、方法论 **L2-1 / L2-2**（锚点校验、测试↔ERR manifest）。

---

## 2. 三层分工（锚点 vs 测试 vs Wiki）

| 层 | 载体 | 职责 |
| --- | --- | --- |
| **L0 锚点** | `_manifest.json` `anchors`、`.ai.md` 注释锚点、`99_spec` drift 字面量 | 端点/RPC/env/表/关键 DEBUG 与文档 **覆盖** |
| **L1 测试 manifest（本 SPEC）** | `docs/_tech_graph/_test_manifest.json`（**拟新增**）或 `docs/spec/governance/manifests/` | **ERR 分支 / 关键 pytest 路径 / failure_path id** 映射（机器可读） |
| **L2 Wiki 叙事** | `coding_wiki` §8、`decisions/` | **为何这样测**；pointer 到 L1 task / L0 ERR |

```text
改 api/ 行为 → 更新 _manifest +（若涉 ERR）_test_manifest → 按需 pytest
关账 task   → Wiki §测试变更（可选）→ 不替代 pytest 绿
```

---

## 3. 锚点纪律（L2-1 本仓落地）

### 3.1 已有工具（须保持 CI Required）

| 工具 | 用途 |
| --- | --- |
| `python tools/tech_graph_manifest_check.py` | manifest vs 源码 / SQL |
| `python tools/tech_graph_drift_check.py` | 端点/RPC/env/表名在 `_tech_graph` 文本覆盖 |
| `python tools/tech_graph_contract_check.py` | 跨端契约 |
| `python tools/tech_graph_graph_export.py --check` | `.ai.md` ↔ `graph.json` |

### 3.2 锚点格式（与 P0_1 done 对齐）

| 类型 | 要求 |
| --- | --- |
| **manifest `anchors`** | `path` + `kind` + 可选 `line`；与 `api/*.py` handler 一致 |
| **Mermaid 注释锚点** | `// → path#Ln` 独立行（`99_mermaid_protocol.md`） |
| **drift 字面量** | `99_spec` 所列 `DEBUG_*` 等 **禁止删**（除非同步改 `drift_check` 与代码） |

### 3.3 新增/变更锚点时

1. 改代码 / SQL  
2. 改 `.ai.md` + `_manifest.json`  
3. 跑 §3.1 四脚本（或 CI 绿）  
4. **禁止** 仅在 Wiki 写锚点而不更新 L0  

---

## 4. 测试 Manifest（L2-2 本仓落地）

### 4.1 文件位置（草案）

```text
docs/_tech_graph/_test_manifest.json    # 首选：与 _manifest 并列，便于 CI 同 workflow
```

#### 4.1.1 与现有图谱 CI 的互操作（防误检）

| 脚本 | 输入范围 | 对 `_test_manifest.json` |
| --- | --- | --- |
| `tech_graph_graph_export.py --check` | 仅 `docs/_tech_graph/*.ai.md` → 比对 **`graph.json`** | **不读取**；新增 JSON **不会** 触发 FP-2 |
| `tech_graph_drift_check.py` | 仅 `docs/_tech_graph/*.md` 文本 | **不读取** |
| `tech_graph_manifest_check.py` | 固定 **`_manifest.json`** 路径 | **不读取** |
| `tech_graph_contract_check.py` | 固定 **`_contract_manifest.json`** | **不读取** |
| `tech_graph_test_manifest_check.py`（Phase B） | **仅** `_test_manifest.json` + `tests/` + `api/` | **专责**；**禁止** 写入或合并进 `graph.json` |

**落盘纪律**：`_test_manifest.json` 与 `graph.json` / `_manifest.json` / `_contract_manifest.json` **并列**；**不得** 手改 `graph.json` 以「塞进」测试条目。若未来某 workflow 对 `_tech_graph/*.json` 做全目录扫描，须在 workflow 中 **显式排除** `_test_manifest.json`（白名单仅 `graph.json`、`_manifest.json`、`_contract_manifest.json`）。

**Schema（v1 最小）**：

```json
{
  "version": 1,
  "freeze_id": "GOV-L2-ANCHOR-TEST-MANIFEST@2026-05-27",
  "entries": [
    {
      "id": "FP-RAG-DB-DISCONNECT",
      "failure_path_ref": "docs/tasks/templates/TASK_TEMPLATE.md#failure_paths",
      "error_codes": ["DATABASE_DISCONNECT"],
      "pytest_markers": ["integration"],
      "test_paths": ["tests/test_rag_*.py"],
      "graph_nodes_optional": ["rag-supabase-client"]
    }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `id` | 稳定 failure path 标识（可与 task 表内 F1/F2 对齐） |
| `error_codes` | 对外结构化 `code` / HTTP 语义 |
| `test_paths` | **仅 glob**（见下表）；相对**仓库根**；**不要求** 行级覆盖 |

**`test_paths` 格式（v1 写死 · 降低 Phase B 解析复杂度）**：

| 规则 | 说明 |
| --- | --- |
| **仅 glob** | 每条为 **fnmatch 模式**（Python `fnmatch`）；**禁止**「精确路径与 glob 混用」双模式 |
| **前缀** | 必须以 `tests/` 开头 |
| **示例** | `tests/test_rag_*.py`、`tests/test_*health*.py` |
| **单文件** | 须写成退化 glob：`tests/test_foo.py`（无 `*` 亦视为合法 glob） |
| **禁止** | `test_rag_*.py`（缺 `tests/`）、`**/tests/**`、仓库外路径 |
| `graph_nodes_optional` | 可选；链 T4 `graph_nodes` / `graph_query` |
| `notes` | 人读；不进 CI 解析亦可 |

### 4.2 与 Wiki §8 边界（重申）

| Wiki **做** | Wiki **不做** |
| --- | --- |
| 记录删/增哪些测试、原因 | 替代 `_test_manifest` 做 CI gate |
| pointer 到 task `failure_paths` | 维护 100% 覆盖列表 |
| `test_strategy` 取值 ingest | 映射 pytest marker 到 CI Required |

见 [`CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §8、§8.1。

### 4.3 CI 演进（分阶段）

| 阶段 | 行为 |
| --- | --- |
| **Phase A（本 SPEC 最小）** | `_test_manifest.json` **文档化存在** + 人工 REVIEW；**不** 阻塞 merge |
| **Phase B（可选 follow-up）** | 新增 `tools/tech_graph_test_manifest_check.py`：ERR 在代码中出现则 manifest 须有项；对每条 `test_paths` 用 `fnmatch` 在仓库根展开，**至少匹配一个** `tests/**/*.py` |
| **Phase C** | **设计已落盘** · 见 **§4.4**；自动化实现 **另 task**（`test_strategy: required`） |

### 4.4 Phase C（design · `GOV-L2-PHASE-C-DESIGN@2026-05-27`）

> **状态**：**design only**（P2 Loop R2）· Phase B CI **done** · **禁止** 在本节承诺已实现双向校验脚本。

#### 4.4.1 目标

| 方向 | 规则 |
| --- | --- |
| **task → manifest** | 每个 `failure_paths` 行 `F#` 在关账前 **应** 有 `_test_manifest.entries[].id` 或显式 `manifest_exempt` 理由（实现期校验） |
| **manifest → task** | 每个 `entries[].id` **应** 有 `failure_path_ref` 指向含对应 `F#` 的 task 锚点（或 Epic 级汇总 task） |
| **命名** | 推荐 `FP-<EPIC>-<SHORT>`；task 表内 `F1` 与 manifest `id` **禁止** 仅同名不同义 |

#### 4.4.2 字段对照（最小）

| task `failure_paths` 列 | `_test_manifest.entries[]` | 一致性 |
| --- | --- | --- |
| 触发条件 | `notes`（人读） + 可选 `graph_nodes_optional` | 语义等价 |
| 系统行为 / `error_codes` | `error_codes[]` | **必须** 集合相等（实现期） |
| 可重试 | `notes` 或扩展字段（Phase C 实现） | 建议一致 |
| — | `test_paths[]` | task **不** 替代；manifest 专责 pytest glob |

#### 4.4.3 示例映射（2～3 条 · 摘自 Phase B manifest）

| task `F#` / 锚点 | manifest `id` | `error_codes` |
| --- | --- | --- |
| `task_05` … F1（DB 不可用） | `FP-RAG-DB-DISCONNECT` | `DATABASE_DISCONNECT` |
| `task_chatbi_v3_sql_ast` … F1 | `FP-SQL-GATE-DENIED` | `ChatBiSqlGateDenied` |
| `task_chatbi_v3_p2_resilience` … F2 | `FP-CODE-RETRIEVAL-UNAUTHORIZED` | `Unauthorized` |

#### 4.4.4 未来实现 task 验收口径（草案）

| # | 项 | pass |
| --- | --- | --- |
| C1 | `tech_graph_test_manifest_check.py` 增 **双向** 模式（`--check-failure-paths` 或等价） | exit 0 |
| C2 | 抽样 ≥3 Epic task 与 manifest 行 **一一对应** | 人工 + 脚本 |
| C3 | 不改 Wiki coverage 真值边界（§4.2） | 审查 |

**非范围（实现 task）**：全仓一次性扫所有历史 task；改 Harness 帽子正文。

#### 4.4.5 Loop 链出

- P2 编排：[`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](./SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) §2 R2  
- 母单：[`task_harness_wiki_loop_p2_followup_v1.md`](../../tasks/active/task_harness_wiki_loop_p2_followup_v1.md)

---

## 5. 范围 / 非范围

### 5.1 范围

- [ ] 本 SPEC `draft` → `active`。  
- [ ] 落盘 `_test_manifest.json` **v1 草案**（≥5 条 **真实** 条目，来自现有 `api/` ERR 与 `tests/`）。  
- [ ] `99_spec.md` 增 **「测试 manifest」** 小节（链本 SPEC + 脚本表）。  
- [ ] 文档化 VERIFY（§7）；CI 仍跑现有 `tech-graph*.yml`。  
- [ ] （可选）`tools/tech_graph_test_manifest_check.py` 骨架 + workflow 非 Required job。  

### 5.2 非范围

- 用 Wiki 替代 pytest / coverage 真值。  
- 修改 Harness 帽子 prompts。  
- 全仓一次性补全所有 Epic 的 failure_path 映射（**分批**）。  
- 替代 ChatBI V3 业务 SPEC（`docs/spec/v3-agent/*`）。  

---

## 6. Agent 使用说明

| 场景 | 动作 |
| --- | --- |
| 新 task 定义 `failure_paths` | 参考 `_test_manifest` 已有 `id`；新 id 命名带 Epic 前缀 |
| 改 ERR 响应 | 同步 manifest + 测一条 pytest；task 表 F 行与 manifest `id` **一致** |
| 关账 docs task | Wiki 可写 §测试变更；**50 仍跑** pytest（若 `test_strategy: required`） |
| 影响分析 | 仍 **graph_query** 优先；manifest 仅清单 |

---

## 7. 验收标准（VERIFY）

```bash
# 锚点 / 图谱 CI（合并前必绿 · 现有）
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check

# 测试 manifest 草案存在且可解析
test -f docs/_tech_graph/_test_manifest.json
python -c "import json; json.load(open('docs/_tech_graph/_test_manifest.json'))"

# 可选：草案条目数
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5"
```

| # | 验收项 | 通过条件 |
| --- | --- | --- |
| B1 | SPEC 冻结 | `active` 或 task 含 `GOV-L2-ANCHOR-TEST-MANIFEST@*` |
| B2 | manifest 文件 | `_test_manifest.json` 合法 JSON + ≥5 entries |
| B3 | 99_spec 链 | `99_spec` 含测试 manifest 指针 |
| B4 | 图谱 CI | 上表四脚本 exit 0 |
| B5 | Wiki 边界 | `CODING_WIKI` §8 已链本 SPEC（一行即可） |

---

## 8. 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
| --- | --- | --- | --- |
| F1 | 仅改 Wiki 不写 manifest/pytest | 50 **fail**（测试意图不可验证） | 补 manifest 或 pytest |
| F2 | `_test_manifest` 引用的 pytest 路径不存在 | Phase B 脚本 **fail**；v1 人工 REVIEW catch | 修路径 |
| F3 | 删 `99_spec` drift 字面量未改代码 | `drift_check` **fail** | 恢复或更新脚本 |
| F4 | 将 coverage % 写入 Wiki 当真值 | lint **拒绝**；违反 §8 | 删/wiki 改 pointer |

---

## 9. 与 T4 / Loop / Harness 的关系

| 项 | 约定 |
| --- | --- |
| **T4** | `_test_manifest.entries[].graph_nodes_optional` 可引用 T4 `graph_nodes.id`；**无硬依赖** |
| **Loop Batch** | 建议 **独立子 round**（R3：manifest 草案；R4：可选脚本）；母单 docs-only，`test_strategy: not_applicable` 除非 R4 |
| **test_strategy: required** | 仅当子 round **改 api/ 或 tests/** 时启用 |

---

## 10. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1 草案：锚点纪律 · `_test_manifest` schema · Phase A/B/C · VERIFY |
| 2026-05-27 | v1.1：§4.1.1 图谱 CI 互操作 · `test_paths` 仅 glob |
| 2026-05-27 | v1.2：§4.4 Phase C **design**（P2 Loop R2 · `GOV-L2-PHASE-C-DESIGN`） |

---

## 给 Cursor

`GOV-L2-ANCHOR-TEST-MANIFEST`、L2 工具链、_test_manifest、manifest_check、drift_check、failure_paths、ERR_、锚点、非 coding_wiki L2 层
