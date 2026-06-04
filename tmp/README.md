# tmp/（本机-only · 不纳入 Git）

> 仓库根 `tmp/` 由 `.gitignore` 整目录忽略。  
> **`docs/`** 下仅跟踪长期真值；易过时产物请落本目录或下列 **docs 黑名单** 路径（同样不提交）。

## 建议子目录

| 路径 | 用途 |
|------|------|
| `tmp/diary/` | 草稿、排期对比、未冻结评价稿；**ChatBI 访客 token 脚本** `local_chatbi_access_token_gen.py`（pointer：`docs/diary/POINTER_local_chatbi_access_token_gen.md`） |
| `tmp/jsonPKmermaid-runs/` | **新** jsonPKmermaid 批跑输出（旧路径见下） |
| `tmp/staging/` | Rubric 演示、一次性 JSON/脚本试验 |
| `tmp/portfolio-rag-demo/` | Portfolio W5 留证 · R7 脚本 [`portfolio-rag-demo/run-r7-backend-curl.sh`](portfolio-rag-demo/run-r7-backend-curl.sh) · [`R7-backend-curl-README.md`](portfolio-rag-demo/R7-backend-curl-README.md) |
| `tmp/delivery/` | 本地 SDD/TDD 交付包副本（可选） |

## 与 `docs/` 黑名单的关系

以下路径**仍在仓库内但 Git 不跟踪**（历史 task 可能引用只读路径字符串）：

- `docs/diary/jsonPKmermaid/runs/` — 闸口 batch / raw（已自索引移除）
- `docs/diary/test/` — A/B 实验草稿
- `docs/_staging/` — 历史 staging
- `docs/delivery/` — 本地交付树

复现闸口：读 `docs/diary/jsonPKmermaid/fixtures/` + `reports/`（**在 Git 中**）；runs 在本机重跑或从备份恢复。

## Agent

- **禁止**默认 `glob` / 遍历 `tmp/`（与 `.cursorignore` 一致）。
- 仅当用户 `@tmp/…` 或 task 显式路径时打开。
