#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3：gate_ctx_ab_v1 最小 S0 — 对 T001 跑 CTX_JSON / CTX_MERMAID 各 1 次。

落盘：docs/diary/jsonPKmermaid/runs/<run_id>/raw/{arm}_{task_id}_S0.jsonl

用法：
  python …/run_s0_minimal.py
  python …/run_s0_minimal.py --arms-order mermaid,json
  python …/run_s0_minimal.py --model deepseek-ai/DeepSeek-V4-Flash
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
PAYLOADS = FIXTURE_ROOT / "payloads"
PROTOCOL_PATH = FIXTURE_ROOT / "protocol_version.yaml"
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.rubric_review.llm_backends import _extract_json_object  # noqa: E402

REQUIRED_KEYS = ("entrypoints", "impacts", "evidence", "unknowns")

ARM_ALIASES: dict[str, str] = {
    "json": "CTX_JSON",
    "a": "CTX_JSON",
    "ctx_json": "CTX_JSON",
    "CTX_JSON": "CTX_JSON",
    "mermaid": "CTX_MERMAID",
    "b": "CTX_MERMAID",
    "ctx_mermaid": "CTX_MERMAID",
    "CTX_MERMAID": "CTX_MERMAID",
}

ARM_SPECS: dict[str, tuple[str, Path]] = {
    "CTX_JSON": (
        "graph.json（代号 A）",
        PAYLOADS / "CTX_JSON" / "main.graph.json",
    ),
    "CTX_MERMAID": (
        "Mermaid 语料总串（代号 B）",
        PAYLOADS / "CTX_MERMAID" / "main.mermaid_corpus.txt",
    ),
}


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_yaml_comment(value: str) -> str:
    if "#" in value:
        value = value.split("#", 1)[0]
    return value.strip().strip('"').strip("'")


def load_protocol(path: Path) -> dict[str, Any]:
    """轻量读取 protocol_version.yaml（不依赖 PyYAML）。"""
    data: dict[str, Any] = {}
    arms: list[str] = []
    s0_arms_order: list[str] = []
    mode: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "arms:":
            mode = "arms"
            continue
        if line == "s0_arms_order:":
            mode = "s0_arms_order"
            continue
        if line.startswith("- ") and mode in ("arms", "s0_arms_order"):
            item = _strip_yaml_comment(line[2:].strip())
            if mode == "arms":
                arms.append(item)
            else:
                s0_arms_order.append(item)
            continue
        if ":" in line and not line.startswith("-"):
            mode = None
            key, val = line.split(":", 1)
            data[key.strip()] = _strip_yaml_comment(val)

    data["arms"] = arms
    if s0_arms_order:
        data["s0_arms_order"] = s0_arms_order
    return data


def resolve_arm_id(token: str) -> str:
    key = token.strip()
    if key not in ARM_ALIASES:
        raise ValueError(f"未知 arm：{token!r}；可用：{', '.join(sorted(set(ARM_ALIASES)))}")
    return ARM_ALIASES[key]


def resolve_arms_order(order_arg: str | None, protocol: dict[str, Any]) -> list[str]:
    if order_arg:
        parts = [p.strip() for p in order_arg.split(",") if p.strip()]
    elif protocol.get("s0_arms_order"):
        parts = list(protocol["s0_arms_order"])
    else:
        parts = list(protocol.get("arms") or ["CTX_JSON", "CTX_MERMAID"])
    return [resolve_arm_id(p) for p in parts]


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
    request_timeout: float,
    max_retries: int = 5,
) -> tuple[dict[str, Any], dict[str, Any], str | None]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url.rstrip("/"), timeout=request_timeout)
    last_exc: BaseException | None = None
    returned_model: str | None = None

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
            returned_model = getattr(resp, "model", None) or model
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
            return parsed, meta, returned_model
        except Exception as e:  # noqa: BLE001
            last_exc = e
            err = str(e).lower()
            if "response_format" in err or "json_object" in err:
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
                returned_model = getattr(resp, "model", None) or model
                raw = resp.choices[0].message.content or ""
                parsed = _extract_json_object(raw)
                usage = resp.usage
                meta = {
                    "wall_total_s": round(wall, 3),
                    "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
                    "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
                    "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
                }
                return parsed, meta, returned_model
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


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="gate_ctx_ab_v1 minimal S0 双分支调用")
    p.add_argument(
        "--arms-order",
        default=None,
        help="逗号分隔，如 mermaid,json 或 CTX_MERMAID,CTX_JSON；默认读 protocol s0_arms_order",
    )
    p.add_argument("--model", default=None, help="覆盖 protocol_version.yaml 中的 model")
    p.add_argument("--protocol", type=Path, default=PROTOCOL_PATH, help="protocol_version.yaml 路径")
    p.add_argument("--request-timeout", type=float, default=300.0, help="单次 HTTP 超时（秒）")
    p.add_argument("--task-id", default=None, help="tasks.json 中的 task_id，默认第一条")
    p.add_argument(
        "--parallel",
        action="store_true",
        help="两分支同时发起 HTTP 请求，削弱「串行时仅首轮吃冷启动」的顺序偏差",
    )
    return p.parse_args()


def _execute_arm(
    *,
    call_index: int,
    arm: str,
    main_label: str,
    main_text: str,
    manifest: str,
    contract: str,
    task_prompt: str,
    system: str,
    model: str,
    api_key: str,
    base_url: str,
    max_tokens: int,
    temperature: float,
    request_timeout: float,
    run_id: str,
    arm_ids: list[str],
    task_id: str,
    protocol_version: str,
    provider: str,
    execution_mode: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """返回 (record, summary_row)。"""
    user = _build_user_message(
        arm=arm,
        main_label=main_label,
        main_text=main_text,
        manifest=manifest,
        contract=contract,
        task_prompt=task_prompt,
    )
    returned_model: str | None = None
    try:
        response, usage_meta, returned_model = _call_chat_json(
            system=system,
            user=user,
            model=model,
            api_key=api_key,
            base_url=base_url,
            max_tokens=max_tokens,
            temperature=temperature,
            request_timeout=request_timeout,
        )
        val_errs = _validate_response(response)
        parse_ok = len(val_errs) == 0
        status = "ok" if parse_ok else "invalid_schema"
    except Exception as e:  # noqa: BLE001
        response = {"error": str(e)}
        usage_meta = {
            "wall_total_s": None,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        val_errs = [f"api_error:{e}"]
        parse_ok = False
        status = "error"

    record = {
        "schema": "gate_ctx_ab_s0_record_v1",
        "run_id": run_id,
        "arm": arm,
        "call_index": call_index,
        "arms_order": arm_ids,
        "execution_mode": execution_mode,
        "task_id": task_id,
        "segment": "S0",
        "protocol_version": protocol_version,
        "model_requested": model,
        "model_returned": returned_model,
        "provider": provider,
        "status": status,
        "parse_ok": parse_ok,
        "validation_errors": val_errs,
        "usage": usage_meta,
        "response": response,
    }
    summary = {
        "call_index": call_index,
        "arm": arm,
        "status": status,
        "parse_ok": parse_ok,
        "prompt_tokens": usage_meta.get("prompt_tokens"),
        "completion_tokens": usage_meta.get("completion_tokens"),
        "wall_total_s": usage_meta.get("wall_total_s"),
        "model_returned": returned_model,
        "file": f"{arm}_{task_id}_S0.jsonl",
    }
    return record, summary


def execute_s0_round(
    *,
    run_dir: Path,
    parallel: bool = False,
    arms_order: str | None = None,
    model: str | None = None,
    protocol_path: Path = PROTOCOL_PATH,
    request_timeout: float = 300.0,
    task_id_arg: str | None = None,
    batch_id: str | None = None,
    batch_round: int | None = None,
    quiet: bool = False,
) -> tuple[Path, dict[str, Any], int]:
    """执行一轮 S0，写入 run_dir，返回 (run_dir, index, exit_code)。"""
    from tools.rubric_review.config import ReviewRuntimeConfig

    protocol = load_protocol(protocol_path)
    tasks_doc = json.loads((FIXTURE_ROOT / "tasks.json").read_text(encoding="utf-8"))
    if task_id_arg:
        task = next(t for t in tasks_doc["tasks"] if t["task_id"] == task_id_arg)
    else:
        task = tasks_doc["tasks"][0]
    task_id = task["task_id"]
    system = _load_text(FIXTURE_ROOT / "system.md")

    cfg = ReviewRuntimeConfig.from_env()
    if cfg.backend != "siliconflow":
        raise RuntimeError("本最小脚本仅验证 siliconflow；请设置 RUBRIC_REVIEW_BACKEND=siliconflow")
    api_key = cfg.siliconflow_api_key
    if not api_key:
        raise RuntimeError("缺少 SILICONFLOW_API_KEY")
    base_url = cfg.siliconflow_base_url

    model_resolved = (model or protocol.get("model") or "").strip()
    if not model_resolved:
        raise RuntimeError("protocol 中缺少 model，请用 --model 指定")
    temperature = float(protocol.get("temperature") or 0.2)
    max_tokens = int(protocol.get("max_tokens") or 4096)
    protocol_version = str(protocol.get("protocol_version") or "unknown")
    freeze_id = str(protocol.get("freeze_id") or "")

    arm_ids = resolve_arms_order(arms_order, protocol)

    manifest = _load_text(PAYLOADS / "_shared" / "_manifest.json")
    contract = _load_text(PAYLOADS / "_shared" / "_contract_manifest.json")

    arms: list[tuple[str, str, str]] = []
    for arm_id in arm_ids:
        if arm_id not in ARM_SPECS:
            raise RuntimeError(f"未配置载荷：{arm_id}")
        label, path = ARM_SPECS[arm_id]
        arms.append((arm_id, label, _load_text(path)))

    run_id = run_dir.name
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    execution_mode = "parallel" if parallel else "sequential"
    if not quiet:
        print(
            f"model={model_resolved} mode={execution_mode} arms_order={','.join(arm_ids)} "
            f"timeout={request_timeout}s -> {run_dir}",
            flush=True,
        )

    arm_index = {arm_id: i + 1 for i, arm_id in enumerate(arm_ids)}
    common_kw = {
        "manifest": manifest,
        "contract": contract,
        "task_prompt": task["prompt_zh"],
        "system": system,
        "model": model_resolved,
        "api_key": api_key,
        "base_url": base_url,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "request_timeout": request_timeout,
        "run_id": run_id,
        "arm_ids": arm_ids,
        "task_id": task_id,
        "protocol_version": protocol_version,
        "provider": cfg.backend,
        "execution_mode": execution_mode,
    }

    results_by_arm: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    batch_wall_s: float | None = None

    if parallel:
        if not quiet:
            print(f"并行发起 {len(arms)} 个请求 …", flush=True)
        batch_t0 = time.perf_counter()

        def _job(item: tuple[str, str, str]) -> tuple[str, dict[str, Any], dict[str, Any]]:
            arm, label, text = item
            rec, summ = _execute_arm(
                call_index=arm_index[arm],
                arm=arm,
                main_label=label,
                main_text=text,
                **common_kw,
            )
            return arm, rec, summ

        with ThreadPoolExecutor(max_workers=len(arms)) as pool:
            futures = [pool.submit(_job, item) for item in arms]
            for fut in as_completed(futures):
                arm, record, summary = fut.result()
                results_by_arm[arm] = (record, summary)
                if not quiet:
                    print(
                        f"  完成 {arm} -> {summary['status']} wall={summary['wall_total_s']}s",
                        flush=True,
                    )
        batch_wall_s = round(time.perf_counter() - batch_t0, 3)
        if not quiet:
            print(f"并行批次总墙钟 batch_wall_total_s={batch_wall_s}", flush=True)
    else:
        for arm, main_label, main_text in arms:
            idx = arm_index[arm]
            if not quiet:
                print(f"[{idx}/{len(arms)}] 调用 {arm} …", flush=True)
            record, summary = _execute_arm(
                call_index=idx,
                arm=arm,
                main_label=main_label,
                main_text=main_text,
                **common_kw,
            )
            results_by_arm[arm] = (record, summary)
            if not quiet:
                print(
                    f"  -> {summary['status']} model_returned={summary['model_returned']} "
                    f"tokens={(summary.get('prompt_tokens') or 0) + (summary.get('completion_tokens') or 0)} "
                    f"wall={summary['wall_total_s']}s",
                    flush=True,
                )

    summary_rows: list[dict[str, Any]] = []
    for arm_id in arm_ids:
        record, summary = results_by_arm[arm_id]
        out_path = raw_dir / summary["file"]
        out_path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
        summary_rows.append(summary)

    index: dict[str, Any] = {
        "schema": "gate_ctx_ab_run_index_v1",
        "run_id": run_id,
        "task_id": task_id,
        "segment": "S0",
        "protocol_version": protocol_version,
        "model_requested": model_resolved,
        "arms_order": arm_ids,
        "execution_mode": execution_mode,
        "batch_wall_total_s": batch_wall_s,
        "freeze_id": freeze_id,
        "request_timeout_s": request_timeout,
        "arms": summary_rows,
        "note": "LLM 行为向 token；轴 II 静态字节见 payloads/materialize_report.json",
    }
    if batch_id is not None:
        index["parent_batch_id"] = batch_id
    if batch_round is not None:
        index["batch_round"] = batch_round

    (run_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        f"# gate_ctx_ab_v1 minimal S0 — `{run_id}`",
        "",
        f"- **model**：`{model_resolved}`",
        f"- **arms_order**：`{','.join(arm_ids)}`",
        f"- **execution_mode**：`{execution_mode}`"
        + (f" · batch_wall_total_s={batch_wall_s}" if batch_wall_s is not None else ""),
        "",
        "| # | arm | status | parse_ok | prompt | completion | wall_s | model_returned | raw |",
        "| ---:| --- | --- | --- | ---:| ---:| ---:| --- | --- |",
    ]
    for r in summary_rows:
        md_lines.append(
            f"| {r['call_index']} | `{r['arm']}` | {r['status']} | {r['parse_ok']} | {r['prompt_tokens']} | "
            f"{r['completion_tokens']} | {r['wall_total_s']} | `{r.get('model_returned')}` | `{r['file']}` |"
        )
    (run_dir / "README.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if not quiet:
        print(f"OK: {run_dir}")
    code = 0 if all(r["parse_ok"] for r in summary_rows) else 1
    return run_dir, index, code


def main() -> int:
    args = _parse_args()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = RUNS_ROOT / f"gate_ctx_ab_v1_minimal_s0_{ts}"
    try:
        _, _, code = execute_s0_round(
            run_dir=run_dir,
            parallel=args.parallel,
            arms_order=args.arms_order,
            model=args.model,
            protocol_path=args.protocol,
            request_timeout=args.request_timeout,
            task_id_arg=args.task_id,
        )
        return code
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
