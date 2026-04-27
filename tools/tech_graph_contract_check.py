from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = REPO_ROOT / "docs" / "_tech_graph" / "_contract_manifest.json"
BACKEND_UNIFIED_CHAT = REPO_ROOT / "api" / "unified_chat.py"


@dataclass(frozen=True)
class Diff:
    missing: list[str]
    extra: list[str]


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _load_json(p: Path) -> dict[str, Any]:
    raw = _read_text(p)
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise TypeError(f"{p} root must be an object")
    return obj


def _diff_set(*, truth: set[str], declared: set[str]) -> Diff:
    missing = sorted([x for x in declared if x not in truth])
    extra = sorted([x for x in truth if x not in declared])
    return Diff(missing=missing, extra=extra)


def _fmt_diff(title: str, d: Diff) -> str:
    lines: list[str] = []
    if d.missing:
        lines.append(f"{title}: MISSING (contract -> truth)")
        for x in d.missing[:80]:
            lines.append(f"  - {x}")
    if d.extra:
        lines.append(f"{title}: EXTRA (truth -> contract)")
        for x in d.extra[:80]:
            lines.append(f"  - {x}")
    return "\n".join(lines).strip()


def _extract_string_keys_from_dict_literal(text: str) -> set[str]:
    # Very lightweight: only "key": ... (string keys)
    return set(re.findall(r'(?s)"([A-Za-z0-9_]+)"\s*:', text))


def _slice_balanced_braces(text: str, *, start_idx: int) -> str | None:
    """Return substring from start_idx starting with '{' until matching '}' (inclusive)."""
    if start_idx < 0 or start_idx >= len(text) or text[start_idx] != "{":
        return None
    depth = 0
    for i in range(start_idx, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start_idx : i + 1]
    return None


def _backend_truth_from_unified_chat(py_text: str) -> dict[str, Any]:
    # 1) SSE event names used by backend
    # allow multiline formatting: _sse(\n  "done", {...})
    backend_events = set(re.findall(r'_sse\(\s*"([A-Za-z0-9_]+)"\s*,', py_text))

    # 2) chain.type values from _event(typ="...") + meta first packet
    chain_types = set(re.findall(r'typ="([A-Za-z0-9_.-]+)"', py_text))
    chain_types |= set(re.findall(r'"type"\s*:\s*"([A-Za-z0-9_.-]+)"', py_text))

    # 3) per-type payload keys (only for dict-literal payload= {...} within the same _event call)
    payload_keys_by_type: dict[str, set[str]] = {}
    event_starts = [m.start() for m in re.finditer(r"_event\(", py_text)]
    event_starts.append(len(py_text))
    for i in range(len(event_starts) - 1):
        seg = py_text[event_starts[i] : event_starts[i + 1]]
        tm = re.search(r'typ="([A-Za-z0-9_.-]+)"', seg)
        if not tm:
            continue
        typ = tm.group(1)
        pm = re.search(r"payload\s*=\s*\{", seg)
        if not pm:
            continue
        brace_pos = seg.find("{", pm.start())
        block = _slice_balanced_braces(seg, start_idx=brace_pos) if brace_pos >= 0 else None
        if not block:
            continue
        keys = _extract_string_keys_from_dict_literal(block)
        if keys:
            payload_keys_by_type.setdefault(typ, set()).update(keys)

    # 4) rag.sources payload structure from _build_rag_sources_event return dict
    rag_sources_payload_keys: set[str] = set()
    rag_sources_retrieval_keys: set[str] = set()
    rag_sources_item_keys: set[str] = set()
    fn_m = re.search(r"def\s+_build_rag_sources_event\([\s\S]*?\n\s*return\s+\{", py_text)
    if fn_m:
        brace_pos = py_text.find("{", fn_m.end() - 1)
        block = _slice_balanced_braces(py_text, start_idx=brace_pos) if brace_pos >= 0 else None
        if block:
            rag_sources_payload_keys = _extract_string_keys_from_dict_literal(block)
            # retrieval nested keys
            r_m = re.search(r'"retrieval"\s*:\s*\{', block)
            if r_m:
                r_brace_pos = block.find("{", r_m.end() - 1)
                r_block = _slice_balanced_braces(block, start_idx=r_brace_pos) if r_brace_pos >= 0 else None
                if r_block:
                    rag_sources_retrieval_keys = _extract_string_keys_from_dict_literal(r_block)

    # item keys from packed.append({ ... })
    # (We only need the first packed.append literal; keys should be stable.)
    pa_m = re.search(r"packed\.append\(\s*\{", py_text)
    if pa_m:
        brace_pos = py_text.find("{", pa_m.end() - 1)
        block = _slice_balanced_braces(py_text, start_idx=brace_pos) if brace_pos >= 0 else None
        if block:
            rag_sources_item_keys = _extract_string_keys_from_dict_literal(block)

    # 5) done data keys from yield _sse("done", {...})
    done_keys: set[str] = set()
    done_m = re.search(r'yield\s+_sse\(\s*"done"\s*,', py_text)
    if done_m:
        brace_pos = py_text.find("{", done_m.end())
        block = _slice_balanced_braces(py_text, start_idx=brace_pos) if brace_pos >= 0 else None
        if block:
            done_keys = _extract_string_keys_from_dict_literal(block)

    # 6) meta payload keys from first yield _sse("chain", {"type":"meta", ... "payload": {...}})
    meta_payload_keys: set[str] = set()
    meta_m = re.search(r'yield\s+_sse\("chain"\s*,\s*\{', py_text)
    if meta_m:
        brace_pos = py_text.find("{", meta_m.end() - 1)
        block = _slice_balanced_braces(py_text, start_idx=brace_pos) if brace_pos >= 0 else None
        if block and '"type"' in block and '"meta"' in block:
            pm = re.search(r'"payload"\s*:\s*\{', block)
            if pm:
                p_brace = block.find("{", pm.end() - 1)
                p_block = _slice_balanced_braces(block, start_idx=p_brace) if p_brace >= 0 else None
                if p_block:
                    meta_payload_keys = _extract_string_keys_from_dict_literal(p_block)

    return {
        "backend_events": backend_events,
        "chain_types": chain_types,
        "payload_keys_by_type": payload_keys_by_type,
        "rag_sources_payload_keys": rag_sources_payload_keys,
        "rag_sources_retrieval_keys": rag_sources_retrieval_keys,
        "rag_sources_item_keys": rag_sources_item_keys,
        "done_keys": done_keys,
        "meta_payload_keys": meta_payload_keys,
    }


def _frontend_expect_from_files(*, sse_consumer_files: list[Path]) -> dict[str, Any]:
    # Only parse SSE consumer files for "frontend expect".
    # Next BFF proxy files are transport-only; avoid mixing in HTTP error JSON keys.
    handled_events_required: set[str] = set()
    handled_events_optional: set[str] = set()
    chain_data_keys_used: set[str] = set()
    done_data_keys_used: set[str] = set()
    payload_keys_used: set[str] = set()
    output_keys_used: set[str] = set()
    router_decision_payload_keys_used: set[str] = set()
    source_item_keys_used: set[str] = set()

    for p in sse_consumer_files:
        t = _read_text(p)

        # Event handling branches: if (b.event === "chain") ...
        ev_vals = set(re.findall(r'\.event\s*===\s*"([A-Za-z0-9_]+)"', t))
        # Required: chain/done branches exist and are used; token/message treated as optional.
        if "chain" in ev_vals:
            handled_events_required.add("chain")
        if "done" in ev_vals:
            handled_events_required.add("done")
        for v in sorted(ev_vals):
            if v not in ("chain", "done"):
                handled_events_optional.add(v)

        # Keys accessed on SSE JSON object parsed as `obj`
        obj_keys = set(re.findall(r"\bobj\.([A-Za-z_][A-Za-z0-9_]*)\b", t))
        chain_data_keys_used |= obj_keys
        done_data_keys_used |= obj_keys

        # payload reading: payload.text / payload.answer / payload.output / output.answer
        payload_keys_used |= set(re.findall(r"\bpayload\.([A-Za-z_][A-Za-z0-9_]*)\b", t))
        output_keys_used |= set(re.findall(r"\boutput\.([A-Za-z_][A-Za-z0-9_]*)\b", t))

        # router decision payload keys: obj.prefer, obj.final_mode, ...
        router_decision_payload_keys_used |= set(re.findall(r"\bobj\.([A-Za-z_][A-Za-z0-9_]*)\b", t))

        # sources item keys: detect map((x)=> ...) variable and then x.foo
        for mm in re.finditer(r"\.map\(\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*=>", t):
            var = mm.group(1)
            source_item_keys_used |= set(re.findall(rf"\b{re.escape(var)}\.([A-Za-z_][A-Za-z0-9_]*)\b", t))

    # Heuristic cleanup: keep only likely contract keys (snake_case + common ones)
    # We intentionally keep a broad set to catch forbidden keys.
    return {
        "handled_events_required": handled_events_required,
        "handled_events_optional": handled_events_optional,
        "chain_obj_keys_used": chain_data_keys_used,
        "done_obj_keys_used": done_data_keys_used,
        "payload_keys_used": payload_keys_used,
        "output_keys_used": output_keys_used,
        "router_decision_payload_keys_used": router_decision_payload_keys_used,
        "source_item_keys_used": source_item_keys_used,
    }


def main() -> int:
    try:
        contract = _load_json(CONTRACT_PATH)
        sse = contract.get("sse")
        if not isinstance(sse, dict):
            raise TypeError("contract.sse must be an object")

        allowed_events = set(sse.get("allowed_events") or [])
        chain = sse.get("chain")
        done = sse.get("done")
        if not isinstance(chain, dict) or not isinstance(done, dict):
            raise TypeError("contract.sse.chain/done must be objects")

        chain_data_keys = set(chain.get("data_keys") or [])
        chain_opt_data_keys = set(chain.get("frontend_optional_chain_data_keys") or [])
        chain_type_values = set(chain.get("type_values") or [])
        done_data_keys = set(done.get("data_keys") or [])

        pkbt = chain.get("payload_min_keys_by_type")
        if not isinstance(pkbt, dict):
            raise TypeError("contract.sse.chain.payload_min_keys_by_type must be an object")

        # Contract self-validation (P6): make sure the manifest itself contains the minimal promised keys.
        must_allowed_events = {"chain", "done"}
        must_chain_data = {"type", "ts", "step_id", "payload"}
        must_done_data = {"ok", "mode", "run_id", "session_id", "request_id"}
        must_types = {"rag.sources", "sql.result"}
        missing_contract: list[str] = []
        if not must_allowed_events.issubset(allowed_events):
            missing_contract.append("contract.sse.allowed_events must include: chain, done")
        if not must_chain_data.issubset(chain_data_keys):
            missing_contract.append("contract.sse.chain.data_keys must include: type, ts, step_id, payload")
        if not must_done_data.issubset(done_data_keys):
            missing_contract.append("contract.sse.done.data_keys must include: ok, mode, run_id, session_id, request_id")
        if not must_types.issubset(set(pkbt.keys())):
            missing_contract.append("contract.sse.chain.payload_min_keys_by_type must include: rag.sources, sql.result")
        if missing_contract:
            print("FAIL: contract manifest incomplete.\n")
            for x in missing_contract:
                print(f"- {x}")
            return 1

        # Load backend truth
        if not BACKEND_UNIFIED_CHAT.exists():
            print(f"ERROR: backend file missing: {BACKEND_UNIFIED_CHAT}")
            return 2
        backend_text = _read_text(BACKEND_UNIFIED_CHAT)
        bt = _backend_truth_from_unified_chat(backend_text)

        problems: list[str] = []

        # backend_truth ⊇ contract
        d_ev = _diff_set(truth=set(bt["backend_events"]), declared=allowed_events)
        if d_ev.missing:
            problems.append(_fmt_diff("Backend SSE allowed events", d_ev))

        d_types = _diff_set(truth=set(bt["chain_types"]), declared=chain_type_values)
        if d_types.missing:
            problems.append(_fmt_diff("Backend chain.type values", d_types))

        d_done = _diff_set(truth=set(bt["done_keys"]), declared=done_data_keys)
        if d_done.missing:
            problems.append(_fmt_diff("Backend done.data keys", d_done))

        # payload keys: only check what we can statically extract
        payload_keys_by_type: dict[str, set[str]] = bt["payload_keys_by_type"]
        for typ, required in pkbt.items():
            if typ == "meta":
                if isinstance(required, list):
                    req = set([x for x in required if isinstance(x, str)])
                    d_meta = _diff_set(truth=set(bt["meta_payload_keys"]), declared=req)
                    if d_meta.missing:
                        problems.append(_fmt_diff("Backend payload keys for meta", d_meta))
                continue
            if typ == "rag.sources":
                if not isinstance(required, dict):
                    continue
                req_payload_keys = set(required.get("payload_keys") or [])
                req_item_keys = set(required.get("source_item_keys") or [])
                req_ret_keys = set(required.get("retrieval_keys") or [])

                d_rag_payload = _diff_set(truth=set(bt["rag_sources_payload_keys"]), declared=req_payload_keys)
                if d_rag_payload.missing:
                    problems.append(_fmt_diff("Backend rag.sources payload keys", d_rag_payload))
                d_rag_items = _diff_set(truth=set(bt["rag_sources_item_keys"]), declared=req_item_keys)
                if d_rag_items.missing:
                    problems.append(_fmt_diff("Backend rag.sources.source item keys", d_rag_items))
                d_rag_ret = _diff_set(truth=set(bt["rag_sources_retrieval_keys"]), declared=req_ret_keys)
                if d_rag_ret.missing:
                    problems.append(_fmt_diff("Backend rag.sources.retrieval keys", d_rag_ret))
                continue

            if isinstance(required, list):
                req = set([x for x in required if isinstance(x, str)])
            else:
                continue
            truth = payload_keys_by_type.get(typ)
            if not truth:
                problems.append(f"Backend payload keys for type {typ!r}: MISSING (cannot find dict-literal payload)")
                continue
            d = _diff_set(truth=set(truth), declared=req)
            if d.missing:
                problems.append(_fmt_diff(f"Backend payload keys for {typ}", d))

        # frontend_expect ⊆ contract
        fa = contract.get("frontend_anchors")
        if not isinstance(fa, dict):
            raise TypeError("contract.frontend_anchors must be an object")
        sse_files_raw = fa.get("sse_consumer_files") or []
        bff_files_raw = fa.get("next_bff_proxy_files") or []
        if not isinstance(sse_files_raw, list) or not all(isinstance(x, str) for x in sse_files_raw):
            raise TypeError("contract.frontend_anchors.sse_consumer_files must be list[str]")
        if not isinstance(bff_files_raw, list) or not all(isinstance(x, str) for x in bff_files_raw):
            raise TypeError("contract.frontend_anchors.next_bff_proxy_files must be list[str]")

        sse_files = [Path(REPO_ROOT / x).resolve() for x in sse_files_raw]
        bff_files = [Path(REPO_ROOT / x).resolve() for x in bff_files_raw]

        missing_files = [str(p) for p in (sse_files + bff_files) if not p.exists()]
        if missing_files:
            print("ERROR: frontend anchor file(s) not found:")
            for p in missing_files:
                print(f"  - {p}")
            return 2

        fe = _frontend_expect_from_files(sse_consumer_files=sse_files)

        # Required handled events must be subset of allowed_events
        d_fe_events = _diff_set(truth=allowed_events, declared=set(fe["handled_events_required"]))
        if d_fe_events.missing:
            problems.append(_fmt_diff("Frontend handled events (required)", d_fe_events))

        # Keys used by frontend must be subset of contract (very lightweight)
        contract_key_union: set[str] = set()
        contract_key_union |= {"event", "data"}
        contract_key_union |= chain_data_keys
        contract_key_union |= chain_opt_data_keys
        contract_key_union |= done_data_keys
        contract_key_union |= chain_type_values
        # payload keys union
        for v in pkbt.values():
            if isinstance(v, list):
                contract_key_union |= set([x for x in v if isinstance(x, str)])
            elif isinstance(v, dict):
                contract_key_union |= set([x for x in (v.get("payload_keys") or []) if isinstance(x, str)])
                contract_key_union |= set([x for x in (v.get("source_item_keys") or []) if isinstance(x, str)])
                contract_key_union |= set([x for x in (v.get("retrieval_keys") or []) if isinstance(x, str)])

        # Used keys collected
        used_union: set[str] = set()
        used_union |= set([x for x in fe["chain_obj_keys_used"] if isinstance(x, str)])
        used_union |= set([x for x in fe["payload_keys_used"] if isinstance(x, str)])
        used_union |= set([x for x in fe["output_keys_used"] if isinstance(x, str)])
        used_union |= set([x for x in fe["router_decision_payload_keys_used"] if isinstance(x, str)])
        used_union |= set([x for x in fe["source_item_keys_used"] if isinstance(x, str)])

        # Ignore known non-contract keys from TS runtime
        ignore = {
            "length",
            "trim",
            "map",
            "filter",
            "sort",
            "at",
            "now",
            "isFinite",
            "parse",
            "stringify",
            "body",
            "headers",
            "status",
            "text",
            "answer",
            "detail",
            "startsWith",
        }
        used_union = set([x for x in used_union if x not in ignore])

        forbidden = sorted([x for x in used_union if x not in contract_key_union])
        if forbidden:
            problems.append("Frontend forbidden keys (expect -> not in contract):\n" + "\n".join([f"  - {x}" for x in forbidden[:120]]))

        if problems:
            print("FAIL: cross-repo contract drift detected.\n")
            for msg in problems:
                if msg.strip():
                    print(msg)
                    print()
            # Optional info
            opt = sorted(list(fe["handled_events_optional"]))
            if opt:
                print("INFO: frontend also handles optional event names (not enforced):")
                for x in opt[:50]:
                    print(f"  - {x}")
                print()
            return 1

        print("OK: cross-repo contract check passed (backend truth covers contract; frontend reads within contract).")
        opt = sorted(list(fe["handled_events_optional"]))
        if opt:
            print("INFO: frontend also handles optional event names (not enforced): " + ", ".join(opt[:20]))
        return 0

    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 2
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"ERROR: contract invalid: {exc}")
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: unexpected: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

