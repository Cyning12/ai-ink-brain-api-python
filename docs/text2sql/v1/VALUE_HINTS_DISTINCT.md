# Text2SQL 值域：YAML 与 DISTINCT 探针（防漂移）

## 行为摘要

- **YAML**：人工维护的 `values`（库内枚举真值）与 `synonyms`（口语 → 真值）。
- **DISTINCT 探针**（`TEXT2SQL_DISTINCT_PROBE=1` 且配置 `TEXT2SQL_DISTINCT_COLUMNS`）：对 allowlist 列执行只读 `SELECT DISTINCT ... LIMIT N`，与 YAML 的 `values` 做**并集去重**，再按字典序写入 prompt。
- **同义词**始终只来自 YAML；模型应把「库内取值」理解为 **字典 ∪ 采样** 的并集，**不是**闭集（受 `LIMIT` 约束）。
- **探针失败**（超时、权限、无 `TEXT2SQL_DATABASE_URL` 等）：该列**降级为仅 YAML**，不阻断 Text2SQL。
- **库侧新增枚举**：会经 DISTINCT 进入并集；新口语仍靠 YAML 或人工补同义词。

## 环境变量

见 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 中 `TEXT2SQL_DISTINCT_*` 与 `.env.example` 占位。
