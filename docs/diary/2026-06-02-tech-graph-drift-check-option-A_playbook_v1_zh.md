# 技术图谱 · 叙述层漂移检查（方案 A）操作指引

| 项 | 内容 |
| --- | --- |
| **版本** | v1.0 |
| **日期** | 2026-06-02 |
| **决策** | **方案 A**：`drift_check` 并入 `tech-graph` CI（**fail**，与 manifest / export 并列必绿） |
| **关联审计** | [`2026-06-02-tech-graph-full-capability-audit_v1_zh.md`](./2026-06-02-tech-graph-full-capability-audit_v1_zh.md) §F P1-1 · §K |
| **脚本** | `tools/tech_graph_drift_check.py` |
| **CI** | `.github/workflows/tech-graph.yml` → step `Tech graph docs literal drift check` |

---

## 1. 两种「漂移」（必分清）

| 俗称 | 工具 | 查什么 | CI |
| --- | --- | --- | --- |
| **机器轨** | `tech_graph_graph_export.py --check` | `.ai.md` 导出结果 vs 已提交 `graph.json` | **是** |
| **门牌号轨** | `tech_graph_manifest_check.py` | `_manifest.json` vs `api/*.py` / SQL | **是** |
| **叙述轨** | `tech_graph_drift_check.py` | 端点/RPC/表/关键 env **字符串** 是否出现在 `docs/_tech_graph/*.md` | **是（方案 A）** |

**典型漏洞（方案 B 时）**：`/api/py/live`、`/api/py/ready` 已在 `_manifest.json`，但 **人读 `.md` 搜不到** → Agent 排障漏入口。

---

## 2. 方案 A · 代价与兜底

### 2.1 代价（本仓量级）

| 类型 | 内容 |
| --- | --- |
| **一次性** | 清 FAIL 清单（见 §4）；集中在 `99_spec` 索引段 + `14_runtime_observability` + `01_struct` |
| **每 PR** | 动路由 / 新表 / 新关键 env → `_manifest.json` + **某篇** `_tech_graph/*.md` 出现相同字面量 |
| **写胖风险** | env 优先写入 `99_spec.md`「drift_check 叙述层索引」 |

### 2.2 谁修复

| 角色 | 职责 |
| --- | --- |
| **同 PR 作者 / Agent** | 改代码 + manifest + 补 md 字面量（§3） |
| **人审** | 字面量落在正确文档 |
| **CI** | 只报 FAIL，不自动改 md |

### 2.3 兜底

1. manifest / export **仍独立**——A 是「人读能搜到」第三层。  
2. 子图拓扑 **不自动** 随路由更新。  
3. env 过多时收窄 `drift_check.py` 的 `key_env_prefix` 或只扩 `99_spec` 索引。

---

## 3. 同 PR 标准作业（与审计 §K.2）

```text
① graph_query / 任务单图谱入口
② 改 api + *.ai.md + _manifest.json +（SSE）_contract_manifest.json
③ render_ai.py → graph_export.py
④ manifest_check → test_manifest_check [--check-failure-paths]
   → export --check → drift_check → equivalence_check
⑤ 人审 → CI tech-graph + tech-graph-contract + pytest
```

---

## 4. 还债：本地检查

```bash
python tools/tech_graph_drift_check.py
```

| 类别 | 曾缺失（2026-06-02） | 落盘 |
| --- | --- | --- |
| Endpoints | `/api/py/live` `/api/py/ready` | `14_runtime_observability.md` + `99_spec` 索引 |
| Tables | `chatbi_access_tokens` | `01_struct.md` + `99_spec` 索引 |
| Key env | SUPABASE_HTTP_* / INSERT_* / TEXT2SQL_DISTINCT_* 等 | `99_spec` 索引段 |

---

## 5. 新增路由 / 表 / env（Agent 清单）

| 变更 | 必做 |
| --- | --- |
| 新 `/api/py/...` | manifest + md 中出现 **完整路径** |
| 新 `sb.table("x")` | `01_struct` 或索引段写 `x` |
| 新关键 env | `99_spec` 索引或 Env 图写变量名 |

---

## 6. P1 并行项

| ID | 状态 |
| --- | --- |
| P1-1 叙述轨 CI | **A · 已接入** |
| P1-3 render_ai `--dry-run` | 待做 |
| P1-4 示范性 PR 索引 | 待做 |
| P1-2 路由→子图自动 | 不做 |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-02 | 方案 A 拍板；playbook + CI |
