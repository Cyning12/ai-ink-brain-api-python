#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3：gate_ctx_ab_v1 最小 S0 — 对 T001 跑 CTX_JSON / CTX_MERMAID 各 1 次。

落盘：docs/diary/jsonPKmermaid/runs/<run_id>/raw/{arm}_{task_id}_S0.jsonl
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
PAYLOADS = FIXTURE_ROOT / "payloads"
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.rubric_review.llm_backends import _extract_json_object  # noqa: E402

REQUIRED_KEYS = ("entrypoints", "impacts", "evidence", "unknowns")


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _build_user_message(*, arm: str, main_label: str, main_text: str, manifest: str, contract: str, task_prompt: str) -> str:
    return f"""## 实验分支
{arm}（主载荷：{main_label}）

## 主载荷
{main_text}

## manifest（附件）
{manifest}

## contract manifest（附件）
{contract}

## 题目
{task_prompt}

## 输出要求
只输出一个 JSON 对象（不要 markdown 围栏），必须包含字段：entrypoints、impacts、evidence、unknowns。
entrypoints/impacts 为数组；evidence 每条含 ref 与 note；无法判断的写入 unknowns。
"""


def _call_chat_json(
    *,
    system: str,
    user: str,
    model: str,
    api_key: str,
    base_url: str,
    max_tokens: int,
    temperature: float,
    max_retries: int = 5,
) -> tuple[dict[str, Any], dict[str, Any]]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url.rstrip("/"), timeout=300.0)
    last_exc: BaseException | None = None
    for attempt in range(max_retries):
        try:
            t0 = time.perf_counter()
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            wall = time.perf_counter() - t0
            raw = resp.choices[0].message.content or ""
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = _extract_json_object(raw)
            usage = resp.usage
            meta = {
                "wall_total_s": round(wall, 3),
                "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
                "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
                "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
            }
            return parsed, meta
        except Exception as e:  # noqa: BLE001
            last_exc = e
            err = str(e).lower()
            if "response_format" in err or "json_object" in err:
                # 降级：无 response_format 再试一次
                t0 = time.perf_counter()
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                wall = time.perf_counter() - t0
                raw = resp.choices[0].message.content or ""
                parsed = _extract_json_object(raw)
                usage = resp.usage
                meta = {
                    "wall_total_s": round(wall, 3),
                    "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
                    "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
                    "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
                }
                return parsed, meta
            if attempt < max_retries - 1:
                time.sleep(1.5 * (2**attempt))
            else:
                raise
    assert last_exc
    raise last_exc


def _validate_response(obj: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED_KEYS:
        if k not in obj:
            errs.append(f"missing:{k}")
    for k in REQUIRED_KEYS:
        if k in obj and not isinstance(obj[k], list):
            errs.append(f"not_list:{k}")
    return errs


def main() -> int:
    from tools.rubric_review.config import ReviewRuntimeConfig

    tasks = json.loads((FIXTURE_ROOT / "tasks.json").read_text(encoding="utf-8"))
    task = tasks["tasks"][0]
    task_id = task["task_id"]
    system = _load_text(FIXTURE_ROOT / "system.md")

    cfg = ReviewRuntimeConfig.from_env()
    if cfg.backend != "siliconflow":
        print("本最小脚本仅验证 siliconflow；请设置 RUBRIC_REVIEW_BACKEND=siliconflow", file=sys.stderr)
        return 2
    api_key = cfg.siliconflow_api_key
    if not api_key:
        print("缺少 SILICONFLOW_API_KEY", file=sys.stderr)
        return 2
    base_url = cfg.siliconflow_base_url
    model = "deepseek-ai/DeepSeek-V4-Flash"
    temperature = 0.2
    max_tokens = 4096

    manifest = _load_text(PAYLOADS / "_shared" / "_manifest.json")
    contract = _load_text(PAYLOADS / "_shared" / "_contract_manifest.json")

    arms = [
        (
            "CTX_JSON",
            "graph.json（代号 A）",
            _load_text(PAYLOADS / "CTX_JSON" / "main.graph.json"),
        ),
        (
            "CTX_MERMAID",
            "Mermaid 语料总串（代号 B）",
            _load_text(PAYLOADS / "CTX_MERMAID" / "main.mermaid_corpus.txt"),
        ),
    ]

    run_id = f"gate_ctx_ab_v1_minimal_s0_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    run_dir = RUNS_ROOT / run_id
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, Any]] = []

    for arm, main_label, main_text in arms:
        user = _build_user_message(
            arm=arm,
            main_label=main_label,
            main_text=main_text,
            manifest=manifest,
            contract=contract,
            task_prompt=task["prompt_zh"],
        )
        print(f"调用 {arm} …", flush=True)
        try:
            response, usage_meta = _call_chat_json(
                system=system,
                user=user,
                model=model,
                api_key=api_key,
                base_url=base_url,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            val_errs = _validate_response(response)
            parse_ok = len(val_errs) == 0
            status = "ok" if parse_ok else "invalid_schema"
        except Exception as e:  # noqa: BLE001
            response = {"error": str(e)}
            usage_meta = {"wall_total_s": None, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            val_errs = [f"api_error:{e}"]
            parse_ok = False
            status = "error"

        record = {
            "schema": "gate_ctx_ab_s0_record_v1",
            "run_id": run_id,
            "arm": arm,
            "task_id": task_id,
            "segment": "S0",
            "protocol_version": "v1-minimal-s0",
            "model": model,
            "provider": cfg.backend,
            "status": status,
            "parse_ok": parse_ok,
            "validation_errors": val_errs,
            "usage": usage_meta,
            "response": response,
        }
        out_path = raw_dir / f"{arm}_{task_id}_S0.jsonl"
        out_path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
        summary_rows.append(
            {
                "arm": arm,
                "status": status,
                "parse_ok": parse_ok,
                "prompt_tokens": usage_meta.get("prompt_tokens"),
                "completion_tokens": usage_meta.get("completion_tokens"),
                "wall_total_s": usage_meta.get("wall_total_s"),
                "file": out_path.name,
            }
        )
        print(f"  -> {status} tokens={usage_meta.get('total_tokens')} wall={usage_meta.get('wall_total_s')}s")

    index = {
        "schema": "gate_ctx_ab_run_index_v1",
        "run_id": run_id,
        "task_id": task_id,
        "segment": "S0",
        "model": model,
        "freeze_id": "TECH_GRAPH_S1_FREEZE_20260514_V1_1_3",
        "arms": summary_rows,
        "note": "LLM 行为向 token；轴 II 静态字节见 payloads/materialize_report.json",
    }
    (run_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        f"# gate_ctx_ab_v1 minimal S0 — `{run_id}`",
        "",
        "| arm | status | parse_ok | prompt_tokens | completion_tokens | wall_s | raw |",
        "| --- | --- | --- | ---:| ---:| ---:| --- |",
    ]
    for r in summary_rows:
        md_lines.append(
            f"| `{r['arm']}` | {r['status']} | {r['parse_ok']} | {r['prompt_tokens']} | "
            f"{r['completion_tokens']} | {r['wall_total_s']} | `{r['file']}` |"
        )
    (run_dir / "README.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"OK: {run_dir}")
    return 0 if all(r["parse_ok"] for r in summary_rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
