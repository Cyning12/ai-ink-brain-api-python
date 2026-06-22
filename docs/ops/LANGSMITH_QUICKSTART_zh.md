# LangSmith · Ops Desk 快速上手（api-python）

> 规划与排期：工作区 [`GUIDE_ops_desk_langsmith_eval_v1_zh.md`](../../../../docs/harness/guides/GUIDE_ops_desk_langsmith_eval_v1_zh.md)  
> 官方文档：[Custom instrumentation · @traceable](https://docs.langchain.com/langsmith/annotate-code)

---

## 1. 安装

```bash
pip install -U langsmith
```

可选：已写入 `requirements.txt` 注释行；评测/观测环境再 `pip install langsmith`。

---

## 2. 环境变量

复制 [`langsmith.env.example`](./langsmith.env.example) 中所需行合并进 `.env`：

```bash
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxx
LANGSMITH_PROJECT=ops-desk-dev

# LLM（deep 路径已有）
SILICONFLOW_API_KEY=sk-...
# 或 OPENAI_API_KEY=sk-...
```

| 变量 | 说明 |
| --- | --- |
| `LANGSMITH_TRACING` | `true` 开启 · **`false` 时不发 trace、@traceable 等价 no-op** |
| `LANGSMITH_PROJECT` | UI 中项目名 · 建议 dev/staging/prod 分开 |

**生产**：默认 `LANGSMITH_TRACING=false` · 仅在排障窗口短期打开。

---

## 3. 运行示例

```bash
cd ai-ink-brain-api-python
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=...
python examples/ops_desk_langsmith_sample.py
```

在 [smith.langchain.com](https://smith.langchain.com) → Project `ops-desk-dev`（或你配置的名称）查看 trace 树。

---

## 4. 在 Ops 代码中使用（薄封装）

[`api/ops/tracing.py`](../../api/ops/tracing.py) 提供与官方兼容的 `traceable`：

- 未安装 `langsmith` → 原函数不变
- `LANGSMITH_TRACING` 未开启 → 原函数不变
- 开启后 → 行为同官方 `@traceable`

```python
from api.ops.tracing import traceable

@traceable(run_type="llm")
def chat_completion(messages: list[dict[str, str]], temperature: float = 0.3) -> str:
    ...

@traceable
def run_deep(...):
    ...
```

LLM 调用建议使用 `run_type="llm"`，便于 UI 统计 token 与延迟。

---

## 5. 与 ops_run_events 的关系

| 系统 | 受众 | 真值 |
| --- | --- | --- |
| `ops_run_events` | 产品 UI · 断联续看 | **是** |
| LangSmith | 维护者 · 评测 · 调试 | 否（镜像 span） |

推荐在 deep 路径把 `ops_runs.id` 写入 trace metadata：

```python
my_fn(..., langsmith_extra={"metadata": {"ops_run_id": run_id}})
```

---

## 6. 进程退出前 flush（脚本/CI）

LangSmith 后台线程上报 trace。短脚本需：

```python
from langsmith import Client

client = Client()
try:
    run_pipeline()
finally:
    client.flush()
```

示例见 [`examples/ops_desk_langsmith_sample.py`](../../examples/ops_desk_langsmith_sample.py)。

---

## 7. 下一步（task P2-5 · 未开工）

1. `chat_completion` / `run_deep` / `analyze_issue` 接线 `@traceable`
2. staging 默认 `LANGSMITH_TRACING=true` 验证 D4
3. Dataset + Evaluator 对齐 Review V1–V4
