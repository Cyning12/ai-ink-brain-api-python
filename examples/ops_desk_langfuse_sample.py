#!/usr/bin/env python3
"""Langfuse @observe 最小示例（via api.ops.tracing traceable shim）。

运行：
  export LANGFUSE_TRACING=true LANGFUSE_PUBLIC_KEY=... LANGFUSE_SECRET_KEY=...
  python examples/ops_desk_langfuse_sample.py

说明：Sample 使用 OpenAI 兼容 API；未配置 Key 时仅打印结构不调用 LLM。
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api.ops.tracing import flush_traces, traceable, tracing_provider


@traceable
def format_prompt(subject: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"What's a good name for a store that sells {subject}?"},
    ]


@traceable(run_type="llm")
def invoke_llm(messages: list[dict[str, str]]) -> str:
    key = (os.getenv("SILICONFLOW_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
    if not key:
        return "[dry-run] no LLM key; trace span still created if LANGFUSE_TRACING=true"
    import requests

    base = (os.getenv("OPS_LLM_BASE") or "https://api.siliconflow.cn/v1").rstrip("/")
    model = os.getenv("OPS_LLM_MODEL") or "Qwen/Qwen2.5-72B-Instruct"
    resp = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": 0},
        timeout=60,
    )
    resp.raise_for_status()
    return str(resp.json()["choices"][0]["message"]["content"])


@traceable
def parse_output(response: str) -> str:
    return response.strip()


@traceable
def run_pipeline(subject: str = "colorful socks") -> str:
    messages = format_prompt(subject)
    response = invoke_llm(messages)
    return parse_output(response)


def main() -> None:
    if tracing_provider() == "none":
        print(
            "提示：设置 LANGFUSE_TRACING=true 与 LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY "
            "后可在 Langfuse UI 看到 trace"
        )
    out = run_pipeline()
    print(out)
    flush_traces()


if __name__ == "__main__":
    main()
