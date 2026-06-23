# Langfuse 快速开始 · Ops Desk

> 规划与排期：工作区 [`GUIDE_ops_desk_langfuse_eval_v1_zh.md`](../../../../docs/harness/guides/GUIDE_ops_desk_langfuse_eval_v1_zh.md)  
> 官方：[Get Started · Python](https://langfuse.com/docs/observability/get-started) · [langfuse-python](https://github.com/langfuse/langfuse-python) · [Local Docker](https://langfuse.com/self-hosting/local)

**两条试用路径不冲突**：同一套 `langfuse-python` + [`api/ops/tracing.py`](../../api/ops/tracing.py)，只改 `LANGFUSE_BASE_URL` 与 key。生产 Python API 部署方式不变。

| 路径 | 适用 | `LANGFUSE_BASE_URL` |
| --- | --- | --- |
| **A · Cloud 免费额度** | 零运维 · 团队共享 UI | `https://cloud.langfuse.com` |
| **B · 本地 Docker** | 熟悉自建 · 数据在本地 | `http://localhost:3000` |

建议 Cloud 与本地 Docker **各建独立 Project**，key 分开，避免 trace 混项目。

---

## 1A. Cloud 试用（免费额度）

1. 打开 [Langfuse Cloud](https://cloud.langfuse.com) 注册
2. 新建 Project（建议 `ops-desk-dev`）
3. **Settings → API Keys** 复制 `Public Key` / `Secret Key`
4. env 模板：[`langfuse.env.example`](./langfuse.env.example)

后续迁自建或换 Cloud 区域，**只改 `LANGFUSE_BASE_URL` + 对应 Project 的 key**，SDK 代码不变。

---

## 1B. 本地 Docker 自建（开发用）

> 官方文档：[Self-Host · Local (docker compose)](https://langfuse.com/self-hosting/local)  
> 栈：Langfuse Web + Worker + PostgreSQL + ClickHouse + Redis（Compose 一键起）

### 前置

- 已安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)（或 Docker Engine + Compose v2）
- 本机可用端口 **3000**（Langfuse UI）

### 启动

```bash
# 任意目录 · 官方最小流程（浅克隆即可）
git clone --depth=1 https://github.com/langfuse/langfuse.git
cd langfuse

# 前台启动（首次会拉镜像，约数分钟）
docker compose up

# 或后台
docker compose up -d
```

浏览器打开 **http://localhost:3000** → 注册本地账号 → 新建 Project（建议 `ops-desk-local`）→ **Settings → API Keys** 复制 key。

### 停止 / 清理

```bash
cd langfuse
docker compose down          # 停容器 · 保留数据卷
docker compose down -v       # 停容器并删数据卷（trace 全清 · 慎用）
```

### 与本机 Python 对接

复制 [`langfuse.env.local.docker.example`](./langfuse.env.local.docker.example) 合并进 `.env` 或 export：

```bash
export LANGFUSE_TRACING=true
export LANGFUSE_PUBLIC_KEY=pk-lf-...
export LANGFUSE_SECRET_KEY=sk-lf-...
export LANGFUSE_BASE_URL=http://localhost:3000

cd ai-ink-brain-api-python
python examples/ops_desk_langfuse_sample.py
```

刷新 **http://localhost:3000** → **Tracing** → 应看到 `run_pipeline` trace。

### 边界（与生产 Python 的关系）

| 场景 | 能否用本地 Docker Langfuse |
| --- | --- |
| 本机跑 `api-python` + sample | ✅ `localhost:3000` |
| 本机跑 Ops Desk 全链路 dev | ✅ 同上 |
| Railway / 云上 **生产** Python | ❌ 连不到你笔记本的 `localhost` → 用 **Cloud** 或 **部署在公网/内网的自建实例** |
| 生产默认 | `LANGFUSE_TRACING=false` · 与是否本地试过 Docker **无关** |

---

## 2. 安装 Python SDK

```bash
cd ai-ink-brain-api-python
pip install -U langfuse
```

可选：已写入 `requirements.txt` 注释行；观测环境再 `pip install langfuse`。

---

## 3. 环境变量（汇总）

| 变量 | 说明 |
| --- | --- |
| `LANGFUSE_TRACING` | `true` 开启 · **生产默认 false** |
| `LANGFUSE_PUBLIC_KEY` | `pk-lf-...` |
| `LANGFUSE_SECRET_KEY` | `sk-lf-...` |
| `LANGFUSE_BASE_URL` | Cloud 或 `http://localhost:3000` |
| `LANGFUSE_TRACING_ENVIRONMENT` | 可选 · `development` / `staging` / `production` |

模板：

- Cloud：[`langfuse.env.example`](./langfuse.env.example)
- 本地 Docker：[`langfuse.env.local.docker.example`](./langfuse.env.local.docker.example)

**Vercel / Railway 等**：变量配在 **跑 Python API 的环境**；Ink 前端一般不必配。

---

## 4. 跑示例

**Cloud：**

```bash
export LANGFUSE_TRACING=true
export LANGFUSE_PUBLIC_KEY=pk-lf-...
export LANGFUSE_SECRET_KEY=sk-lf-...
export LANGFUSE_BASE_URL=https://cloud.langfuse.com

python examples/ops_desk_langfuse_sample.py
```

**本地 Docker：** 见 §1B · 仅 `LANGFUSE_BASE_URL=http://localhost:3000` 不同。

未配置 `SILICONFLOW_API_KEY` / `OPENAI_API_KEY` 时示例为 dry-run，trace 仍会写入。

---

## 5. 代码用法

[`api/ops/tracing.py`](../../api/ops/tracing.py) 提供 Langfuse 优先的 `traceable`：

- 未安装 `langfuse` → 原函数不变
- `LANGFUSE_TRACING=false` → no-op
- `LANGFUSE_TRACING=true` 且 key 齐全 → `@observe` 上报

```python
from api.ops.tracing import traceable, flush_traces

@traceable
def run_deep(...):
    ...

@traceable(run_type="llm")  # 映射为 Langfuse as_type=generation
def chat_completion(messages, temperature=0.3):
    ...

flush_traces()  # 短脚本 / serverless 结束前
```

关联 `ops_runs.id`（P2-5a 接线时）：

```python
from langfuse import get_client

langfuse = get_client()
with langfuse.start_as_current_observation(
    name="ops_run",
    metadata={"ops_run_id": run_id, "route": "deep"},
):
    ...
```

---

## 6. 与 LangSmith 并存

| 开关 | 后端 |
| --- | --- |
| `LANGFUSE_TRACING=true` + keys | **Langfuse**（优先） |
| 仅 `LANGSMITH_TRACING=true` | LangSmith（遗留） |

新接入请只用 Langfuse；LangSmith 见 [`LANGSMITH_QUICKSTART_zh.md`](./LANGSMITH_QUICKSTART_zh.md)。

---

## 7. 可视化

SDK 只负责上报；**Dashboard** 在 Langfuse Cloud 或本地 **http://localhost:3000** 查看 trace 树、token、延迟、metadata。

产品侧用户可见时间线仍为 Supabase `ops_run_events`；Langfuse 为维护者/debug 轨。

---

## 8. 后续：生产自建全链（预留）

本地 Docker 验证满意后，可将同一 [`langfuse/langfuse`](https://github.com/langfuse/langfuse) 栈部署到 VM / Railway / K8s（见 [Self-Hosting 文档](https://langfuse.com/self-hosting)），staging 生产 Python 只改：

```bash
LANGFUSE_BASE_URL=https://langfuse.your-domain.example
# + 该实例上新建的 Project keys
```

无需改 `tracing.py` 或 Orchestrator 装饰器写法。
