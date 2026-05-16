# payloads（Step 2 物化）

由 [`../scripts/materialize_payloads.py`](../scripts/materialize_payloads.py) 从 `docs/_tech_graph/` 生成；**勿手改**主载荷（改图谱后重新运行脚本）。

| 路径 | 分支 | 内容 |
|------|------|------|
| [`CTX_JSON/main.graph.json`](./CTX_JSON/main.graph.json) | `CTX_JSON` | 冻结 `graph.json` 全文 |
| [`CTX_MERMAID/main.mermaid_corpus.txt`](./CTX_MERMAID/main.mermaid_corpus.txt) | `CTX_MERMAID` | `*.ai.md` 内 mermaid fence 拼接（跳过 `99_*`） |
| [`_shared/`](./_shared/) | 两分支共用 | `_manifest.json`、`_contract_manifest.json` |
| [`materialize_report.json`](./materialize_report.json) | — | 字节/token 粗估与源文件列表 |

**隔离规则**：`CTX_JSON/` 下无 Markdown 正文；`CTX_MERMAID/` 下无 `graph.json`。

重新生成：

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/materialize_payloads.py
```
