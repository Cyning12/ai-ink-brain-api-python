#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0-B：gate_ctx_ab_v1 三段协议 S0→S1→S2（同线程、每题×每 arm）。

- 策略 β（默认）：S0 全量主载荷；S1/S2 增量摘要 + manifest/contract。
- S2：按 user_scripts.json 插入另外两题题面（topic_id 与主题题不同）。

落盘：runs/<run_id>/
  raw/{arm}_{primary_task_id}_S0.jsonl
  raw/{arm}_{primary_task_id}_S1_{01..03}.jsonl
  raw/{arm}_{primary_task_id}_S2_{01..02}.jsonl
  session_index.json

用法：
  python …/run_s1_s2.py --all-tasks
  python …/run_s1_s2.py --task-id T002_unified_sse_chain_contract
  python …/run_s1_s2.py --all-tasks --arms json   # 仅 CTX_JSON
"""

from __future__ import annotations

import argparse
import importlib.util
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
PROTOCOL_PATH = FIXTURE_ROOT / "protocol_version.yaml"
USER_SCRIPTS_PATH = FIXTURE_ROOT / "user_scripts.json"
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"

OUTPUT_SUFFIX = (
    "只输出一个 JSON 对象（不要 markdown 围栏），必须包含字段："
    "entrypoints、impacts、evidence、unknowns。"
)


def _load_s0_module():
    path = _REPO.parent / "run_s0_minimal.py"
    spec = importlib.util.spec_from_file_location("gate_ctx_s0_minimal", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_user_scripts(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _call_chat_messages(
    *,
    messages: list[dict[str, str]],
    model: str,
    api_key: str,
    base_url: str,
    max_tokens: int,
    temperature: float,
    request_timeout: float,
    max_retries: int = 5,
) -> tuple[dict[str, Any], dict[str, Any], str, str | None]:
    """返回 (parsed, usage_meta, assistant_raw, model_returned)。"""
    from openai import OpenAI

    from tools.rubric_review.llm_backends import _extract_json_object

    client = OpenAI(api_key=api_key, base_url=base_url.rstrip("/"), timeout=request_timeout)
    last_exc: BaseException | None = None
    returned_model: str | None = None

    for attempt in range(max_retries):
        try:
            t0 = time.perf_counter()
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
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
            return parsed, meta, raw, returned_model
        except Exception as e:  # noqa: BLE001
            last_exc = e
            err = str(e).lower()
            if "response_format" in err or "json_object" in err:
                t0 = time.perf_counter()
                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
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
                return parsed, meta, raw, returned_model
            if attempt < max_retries - 1:
                time.sleep(1.5 * (2**attempt))
            else:
                raise
    assert last_exc
    raise last_exc


def _build_digest(*, primary_task_id: str, topic_id: str, last_response: dict[str, Any]) -> str:
    eps = [e for e in (last_response.get("entrypoints") or []) if isinstance(e, dict)]
    paths = [str(e.get("path") or "") for e in eps if e.get("path")]
    sym = [str(e.get("symbol") or "") for e in eps if e.get("symbol")]
    head_paths = ", ".join(paths[:6]) or "（无 path）"
    head_sym = ", ".join(sym[:6]) or "（无 symbol）"
    return (
        f"## 上下文摘要（策略 β · 主题题 `{primary_task_id}` · topic `{topic_id}`）\n"
        f"- 上轮入口约 {len(eps)} 条；path 示例：{head_paths}\n"
        f"- symbol 示例：{head_sym}\n"
        f"- 请勿要求重贴全量 graph/Mermaid 主载荷；沿用本线程已有分析。\n"
    )


def _build_s0_user(s0: Any, *, arm: str, main_label: str, main_text: str, manifest: str, contract: str, task_prompt: str) -> str:
    return s0._build_user_message(
        arm=arm,
        main_label=main_label,
        main_text=main_text,
        manifest=manifest,
        contract=contract,
        task_prompt=task_prompt,
    )


def _build_followup_user(
    *,
    digest: str,
    manifest: str,
    contract: str,
    segment: str,
    round_index: int,
    prompt_zh: str,
    extra_note: str = "",
) -> str:
    note_block = f"\n{extra_note}\n" if extra_note else ""
    return f"""{digest}

## manifest（附件）
{manifest}

## contract manifest（附件）
{contract}

## 本轮（{segment} · 第 {round_index} 轮）
{prompt_zh}
{note_block}
## 输出要求
{OUTPUT_SUFFIX}
"""


def _gold_path_set(task: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    gold = task.get("gold") or {}
    for key in ("entrypoints", "impacts"):
        for item in gold.get(key) or []:
            if isinstance(item, dict) and item.get("path"):
                paths.add(str(item["path"]).replace("\\", "/").strip())
    return paths


def _response_path_mentions(response: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    blob = json.dumps(response, ensure_ascii=False)
    # 粗匹配 tasks gold 常见 path 前缀
    for prefix in (
        "api/",
        "docs/_tech_graph/",
        "tools/",
        "supabase/sql",
        ".github/workflows",
    ):
        if prefix in blob:
            found.add(prefix)
    for key in ("entrypoints", "impacts"):
        for item in response.get(key) or []:
            if not isinstance(item, dict):
                continue
            p = item.get("path")
            if p:
                found.add(str(p).replace("\\", "/").strip())
            desc = item.get("description") or ""
            for token in ("api/", "docs/_tech_graph/", "supabase/sql", "tools/"):
                if token in str(desc):
                    found.add(token)
    return found


def _count_leakage(
    response: dict[str, Any],
    *,
    current_paths: set[str],
    prior_paths: set[str],
) -> int:
    """前序题 gold 路径出现在本轮且不属于当前题 gold 的条数（启发式）。"""
    mentions = _response_path_mentions(response)
    leak = 0
    for p in prior_paths:
        if p in current_paths:
            continue
        # 目录级：若 mention 含 prior 的 path 子串
        for m in mentions:
            if p in m or m in p:
                leak += 1
                break
    return leak


def _write_record(path: Path, record: dict[str, Any]) -> None:
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")


def _make_record(
    *,
    schema_segment: str,
    run_id: str,
    arm: str,
    primary_task_id: str,
    topic_id: str,
    segment: str,
    round_index: int,
    protocol_version: str,
    model_requested: str,
    model_returned: str | None,
    provider: str,
    status: str,
    parse_ok: bool,
    validation_errors: list[str],
    usage: dict[str, Any],
    response: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "schema": "gate_ctx_ab_s1s2_record_v1",
        "run_id": run_id,
        "arm": arm,
        "primary_task_id": primary_task_id,
        "topic_id": topic_id,
        "segment": segment,
        "round_index": round_index,
        "protocol_version": protocol_version,
        "model_requested": model_requested,
        "model_returned": model_returned,
        "provider": provider,
        "status": status,
        "parse_ok": parse_ok,
        "validation_errors": validation_errors,
        "usage": usage,
        "response": response,
    }
    if extra:
        rec.update(extra)
    return rec


def execute_s1_s2_session(
    *,
    run_dir: Path,
    primary_task: dict[str, Any],
    arm: str,
    s0: Any,
    tasks_by_id: dict[str, dict[str, Any]],
    user_scripts: dict[str, Any],
    protocol: dict[str, Any],
    context_strategy: str,
    model: str,
    api_key: str,
    base_url: str,
    max_tokens: int,
    temperature: float,
    request_timeout: float,
    quiet: bool = False,
) -> tuple[dict[str, Any], int]:
    from tools.rubric_review.config import ReviewRuntimeConfig

    primary_task_id = primary_task["task_id"]
    topic_id = primary_task.get("topic_id") or ""
    protocol_version = str(protocol.get("protocol_version") or "unknown")
    freeze_id = str(protocol.get("freeze_id") or "")

    if arm not in s0.ARM_SPECS:
        raise RuntimeError(f"未配置载荷：{arm}")
    main_label, main_path = s0.ARM_SPECS[arm]
    main_text = s0._load_text(main_path)
    manifest = s0._load_text(PAYLOADS / "_shared" / "_manifest.json")
    contract = s0._load_text(PAYLOADS / "_shared" / "_contract_manifest.json")
    system = s0._load_text(FIXTURE_ROOT / "system.md")

    cfg = ReviewRuntimeConfig.from_env()
    provider = cfg.backend

    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    messages: list[dict[str, str]] = [{"role": "system", "content": system}]
    summaries: list[dict[str, Any]] = []
    cumulative_tokens = 0

    current_gold_paths = _gold_path_set(primary_task)
    prior_gold_paths: set[str] = set()
    for tid, t in tasks_by_id.items():
        if tid != primary_task_id:
            prior_gold_paths |= _gold_path_set(t)

    def _one_round(
        *,
        segment: str,
        round_index: int,
        user_content: str,
        file_name: str,
        extra_fields: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        nonlocal cumulative_tokens
        messages.append({"role": "user", "content": user_content})
        try:
            parsed, usage, assistant_raw, returned_model = _call_chat_messages(
                messages=messages,
                model=model,
                api_key=api_key,
                base_url=base_url,
                max_tokens=max_tokens,
                temperature=temperature,
                request_timeout=request_timeout,
            )
            val_errs = s0._validate_response(parsed)
            parse_ok = len(val_errs) == 0
            status = "ok" if parse_ok else "invalid_schema"
            messages.append({"role": "assistant", "content": assistant_raw})
        except Exception as e:  # noqa: BLE001
            parsed = {"error": str(e)}
            usage = {
                "wall_total_s": None,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }
            val_errs = [f"api_error:{e}"]
            parse_ok = False
            status = "error"
            returned_model = None
            assistant_raw = json.dumps(parsed, ensure_ascii=False)

        cumulative_tokens += int(usage.get("total_tokens") or 0)
        record = _make_record(
            run_id=run_dir.name,
            arm=arm,
            primary_task_id=primary_task_id,
            topic_id=topic_id,
            segment=segment,
            round_index=round_index,
            protocol_version=protocol_version,
            model_requested=model,
            model_returned=returned_model,
            provider=provider,
            status=status,
            parse_ok=parse_ok,
            validation_errors=val_errs,
            usage=usage,
            response=parsed,
            extra=extra_fields,
        )
        _write_record(raw_dir / file_name, record)
        row = {
            "segment": segment,
            "round_index": round_index,
            "arm": arm,
            "status": status,
            "parse_ok": parse_ok,
            "file": file_name,
            **usage,
            "cumulative_tokens": cumulative_tokens,
        }
        if extra_fields:
            row.update(extra_fields)
        summaries.append(row)
        if not quiet:
            print(
                f"    {segment} r{round_index} -> {status} wall={usage.get('wall_total_s')}s "
                f"cum_tokens={cumulative_tokens}",
                flush=True,
            )
        return parsed

    # --- S0 ---
    if not quiet:
        print(f"  [{arm}] S0 …", flush=True)
    s0_user = _build_s0_user(
        s0,
        arm=arm,
        main_label=main_label,
        main_text=main_text,
        manifest=manifest,
        contract=contract,
        task_prompt=primary_task["prompt_zh"],
    )
    last_response = _one_round(
        segment="S0",
        round_index=0,
        user_content=s0_user,
        file_name=f"{arm}_{primary_task_id}_S0.jsonl",
        extra_fields={"context_strategy": context_strategy, "freeze_id": freeze_id},
    )

    digest = _build_digest(
        primary_task_id=primary_task_id,
        topic_id=topic_id,
        last_response=last_response if isinstance(last_response, dict) else {},
    )

    # --- S1 ---
    s1_prompts = list((user_scripts.get("s1") or {}).get("prompts") or [])
    for i, prompt in enumerate(s1_prompts, start=1):
        if context_strategy == "alpha":
            user = _build_s0_user(
                s0,
                arm=arm,
                main_label=main_label,
                main_text=main_text,
                manifest=manifest,
                contract=contract,
                task_prompt=f"{primary_task['prompt_zh']}\n\n【S1 追问】{prompt}",
            )
        else:
            user = _build_followup_user(
                digest=digest,
                manifest=manifest,
                contract=contract,
                segment="S1",
                round_index=i,
                prompt_zh=prompt,
            )
        last_response = _one_round(
            segment="S1",
            round_index=i,
            user_content=user,
            file_name=f"{arm}_{primary_task_id}_S1_{i:02d}.jsonl",
            extra_fields={"context_strategy": context_strategy},
        )
        if isinstance(last_response, dict):
            digest = _build_digest(
                primary_task_id=primary_task_id,
                topic_id=topic_id,
                last_response=last_response,
            )

    # --- S2 ---
    s2_order = list(
        ((user_scripts.get("s2") or {}).get("order_by_primary") or {}).get(primary_task_id) or []
    )
    for j, other_id in enumerate(s2_order, start=1):
        other_task = tasks_by_id.get(other_id)
        if not other_task:
            raise RuntimeError(f"S2 未知 task_id：{other_id}")
        other_topic = other_task.get("topic_id") or ""
        note = (
            f"【S2 换题】本题 topic_id=`{other_topic}`，与主题题 `{topic_id}` 不同。"
            f"仅回答本题面，避免串题引用无关路径。"
        )
        if context_strategy == "alpha":
            user = _build_s0_user(
                s0,
                arm=arm,
                main_label=main_label,
                main_text=main_text,
                manifest=manifest,
                contract=contract,
                task_prompt=f"{other_task['prompt_zh']}\n\n{note}",
            )
        else:
            user = _build_followup_user(
                digest=digest,
                manifest=manifest,
                contract=contract,
                segment="S2",
                round_index=j,
                prompt_zh=other_task["prompt_zh"],
                extra_note=note,
            )
        s2_file = f"{arm}_{primary_task_id}_S2_{j:02d}.jsonl"
        last_response = _one_round(
            segment="S2",
            round_index=j,
            user_content=user,
            file_name=s2_file,
            extra_fields={
                "context_strategy": context_strategy,
                "s2_task_id": other_id,
                "s2_topic_id": other_topic,
            },
        )
        if isinstance(last_response, dict):
            leak = _count_leakage(
                last_response,
                current_paths=_gold_path_set(other_task),
                prior_paths=(current_gold_paths | prior_gold_paths) - _gold_path_set(other_task),
            )
            summaries[-1]["leakage_count_heuristic"] = leak
            s2_path = raw_dir / s2_file
            patched = json.loads(s2_path.read_text(encoding="utf-8"))
            patched["leakage_count_heuristic"] = leak
            _write_record(s2_path, patched)

    session_index = {
        "schema": "gate_ctx_ab_s1s2_session_v1",
        "run_id": run_dir.name,
        "primary_task_id": primary_task_id,
        "topic_id": topic_id,
        "arm": arm,
        "context_strategy": context_strategy,
        "rounds": summaries,
        "cumulative_tokens_final": cumulative_tokens,
        "freeze_id": freeze_id,
        "model_requested": model,
    }
    return session_index, 0 if all(s.get("parse_ok") for s in summaries) else 1


def _tasks_for_run(tasks_doc: dict[str, Any], task_ids: list[str] | None) -> list[dict[str, Any]]:
    all_tasks = tasks_doc.get("tasks") or []
    if not task_ids:
        out = []
        for t in all_tasks:
            scope = t.get("segment_scope") or ["S0"]
            if "S1" in scope or "S2" in scope:
                out.append(t)
        return out
    id_set = set(task_ids)
    return [t for t in all_tasks if t["task_id"] in id_set]


def main() -> int:
    p = argparse.ArgumentParser(description="gate_ctx_ab_v1 S0→S1→S2（三题通用）")
    p.add_argument("--all-tasks", action="store_true", help="跑 segment_scope 含 S1/S2 的全部题（默认）")
    p.add_argument("--task-id", action="append", default=[], help="可多次指定；缺省等同 --all-tasks")
    p.add_argument("--arms", default="mermaid,json", help="逗号分隔 arm，默认两分支都跑")
    p.add_argument("--context-strategy", choices=("alpha", "beta"), default="beta")
    p.add_argument("--model", default=None)
    p.add_argument("--request-timeout", type=float, default=300.0)
    p.add_argument("--pause-between-sessions", type=float, default=5.0)
    args = p.parse_args()

    s0 = _load_s0_module()
    protocol = s0.load_protocol(PROTOCOL_PATH)
    user_scripts = _load_user_scripts(USER_SCRIPTS_PATH)
    tasks_doc = json.loads((FIXTURE_ROOT / "tasks.json").read_text(encoding="utf-8"))
    tasks_by_id = {t["task_id"]: t for t in tasks_doc.get("tasks", [])}

    task_ids = args.task_id if args.task_id else None
    if not args.all_tasks and not task_ids:
        args.all_tasks = True
    tasks = _tasks_for_run(tasks_doc, task_ids)
    if not tasks:
        print("无匹配任务", file=sys.stderr)
        return 2

    arm_tokens = [s0.resolve_arm_id(x.strip()) for x in args.arms.split(",") if x.strip()]

    from tools.rubric_review.config import ReviewRuntimeConfig

    cfg = ReviewRuntimeConfig.from_env()
    if cfg.backend != "siliconflow":
        raise RuntimeError("本脚本仅验证 siliconflow")
    api_key = cfg.siliconflow_api_key
    if not api_key:
        raise RuntimeError("缺少 SILICONFLOW_API_KEY")

    model = (args.model or protocol.get("model") or "").strip()
    if not model:
        raise RuntimeError("缺少 model")
    temperature = float(protocol.get("temperature") or 0.2)
    max_tokens = int(protocol.get("max_tokens") or 4096)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    parent = RUNS_ROOT / f"gate_ctx_ab_v1_s1s2_{ts}"
    parent.mkdir(parents=True, exist_ok=True)

    print(
        f"parent={parent} tasks={len(tasks)} arms={arm_tokens} strategy={args.context_strategy}",
        flush=True,
    )

    all_sessions: list[dict[str, Any]] = []
    exit_code = 0

    for task in tasks:
        tid = task["task_id"]
        task_dir = parent / tid
        task_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== 主题题 {tid} ===", flush=True)
        for arm in arm_tokens:
            session_dir = task_dir / arm
            session_dir.mkdir(parents=True, exist_ok=True)
            try:
                index, code = execute_s1_s2_session(
                    run_dir=session_dir,
                    primary_task=task,
                    arm=arm,
                    s0=s0,
                    tasks_by_id=tasks_by_id,
                    user_scripts=user_scripts,
                    protocol=protocol,
                    context_strategy=args.context_strategy,
                    model=model,
                    api_key=api_key,
                    base_url=cfg.siliconflow_base_url,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    request_timeout=args.request_timeout,
                )
                index["exit_code"] = code
                all_sessions.append(index)
                (session_dir / "session_index.json").write_text(
                    json.dumps(index, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                exit_code = max(exit_code, code)
            except Exception as e:  # noqa: BLE001
                print(f"  [{arm}] 失败: {e}", file=sys.stderr)
                exit_code = 2
            if args.pause_between_sessions > 0:
                time.sleep(args.pause_between_sessions)

    (parent / "batch_index.json").write_text(
        json.dumps(
            {
                "schema": "gate_ctx_ab_s1s2_batch_v1",
                "parent_run_id": parent.name,
                "context_strategy": args.context_strategy,
                "tasks": [t["task_id"] for t in tasks],
                "arms": arm_tokens,
                "sessions": all_sessions,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nOK: {parent}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
