from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
API_DIR = REPO_ROOT / "api"
SQL_DIR = REPO_ROOT / "supabase" / "sql"
MANIFEST_PATH = REPO_ROOT / "docs" / "_tech_graph" / "_manifest.json"


KEY_ENV_PREFIX = (
    "NEXT_PUBLIC_SUPABASE_",
    "SUPABASE_",
    "SILICONFLOW_",
    "RAG_",
    "DEBUG_",
    "TEXT2SQL_",
)
KEY_ENV_EXACT = {
    "API_KEY",
    "CHAT_API_SECRET",
    "NEXT_PUBLIC_ADMIN_SECRET",
    "NODE_ENV",
    "CONTENT_ROOT",
    "CONTENT_DEFAULT_YEAR",
    "EMBEDDING_DIM",
    "MAX_X_SOURCES_HEADER_CHARS",
}


@dataclass(frozen=True)
class EndpointTruth:
    method: str
    path: str
    handler: str
    line: int


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _iter_py_files() -> list[Path]:
    return sorted([p for p in API_DIR.glob("*.py") if p.is_file()])


def _iter_sql_files() -> list[Path]:
    return sorted([p for p in SQL_DIR.glob("*.sql") if p.is_file()])


def _find_def_line(text: str, symbol: str) -> int | None:
    # def foo( / class Foo(
    pat = re.compile(rf"(?m)^(?:async\s+def|def|class)\s+{re.escape(symbol)}\b")
    m = pat.search(text)
    if not m:
        return None
    return text[: m.start()].count("\n") + 1


def _extract_endpoints_from_index(index_text: str) -> list[EndpointTruth]:
    # Pattern: @app.get("/api/py/x")\n... def handler(
    # We keep it strict to avoid false positives.
    out: list[EndpointTruth] = []
    deco_pat = re.compile(r'(?m)^@app\.(get|post)\("(/api/py/[^"]+)"\)\s*$')
    for m in deco_pat.finditer(index_text):
        method = m.group(1).upper()
        path = m.group(2)
        after = index_text[m.end() :]
        def_m = re.search(r"(?m)^(?:async\s+def|def)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", after)
        if not def_m:
            continue
        handler = def_m.group(1)
        line = index_text[: m.start()].count("\n") + 1
        out.append(EndpointTruth(method=method, path=path, handler=handler, line=line))
    out.sort(key=lambda e: (e.path, e.method, e.handler))
    return out


def _extract_env_names_from_text(py_text: str) -> set[str]:
    # os.getenv("FOO") / os.getenv("FOO", "default")
    return set(re.findall(r'os\.getenv\("([A-Z0-9_]+)"', py_text))


def _filter_key_envs(envs: Iterable[str]) -> set[str]:
    out: set[str] = set()
    for e in envs:
        if e in KEY_ENV_EXACT:
            out.add(e)
            continue
        if any(e.startswith(p) for p in KEY_ENV_PREFIX):
            out.add(e)
    return out


def _extract_rpc_names_from_text(py_text: str) -> set[str]:
    # sb.rpc("keyword_documents", {...})
    return set(re.findall(r'\.rpc\("([A-Za-z0-9_]+)"\s*,', py_text))


def _extract_table_names_from_text(py_text: str) -> set[str]:
    # sb.table("documents")
    return set(re.findall(r'\.table\("([A-Za-z0-9_]+)"\)', py_text))


def _extract_sql_tables(sql_text: str) -> set[str]:
    # create table if not exists public.documents (
    # create table public.foo (
    pat = re.compile(r"(?im)^\s*create\s+table\s+(?:if\s+not\s+exists\s+)?public\.([a-z0-9_]+)\b")
    return set([m.group(1) for m in pat.finditer(sql_text)])


def _extract_sql_public_functions(sql_text: str) -> set[str]:
    # create or replace function public.match_documents(
    pat = re.compile(
        r"(?im)^\s*create\s+or\s+replace\s+function\s+public\.([a-z0-9_]+)\s*\(",
    )
    return set([m.group(1) for m in pat.finditer(sql_text)])


def _load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"missing manifest: {MANIFEST_PATH}")
    raw = _read_text(MANIFEST_PATH)
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise TypeError("manifest root must be an object")
    return obj


def _expect_list_str(obj: dict[str, Any], key: str) -> list[str]:
    v = obj.get(key)
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise TypeError(f"manifest.{key} must be list[str]")
    return v


def _expect_supabase(obj: dict[str, Any]) -> tuple[list[str], list[str]]:
    sb = obj.get("supabase")
    if not isinstance(sb, dict):
        raise TypeError("manifest.supabase must be an object")
    tables = sb.get("tables")
    rpc = sb.get("rpc")
    if not isinstance(tables, list) or not all(isinstance(x, str) for x in tables):
        raise TypeError("manifest.supabase.tables must be list[str]")
    if not isinstance(rpc, list) or not all(isinstance(x, str) for x in rpc):
        raise TypeError("manifest.supabase.rpc must be list[str]")
    return tables, rpc


def _expect_endpoints(obj: dict[str, Any]) -> list[dict[str, Any]]:
    eps = obj.get("endpoints")
    if not isinstance(eps, list) or not all(isinstance(x, dict) for x in eps):
        raise TypeError("manifest.endpoints must be list[object]")
    required = {"method", "path", "handler"}
    for i, e in enumerate(eps):
        missing = required - set(e.keys())
        if missing:
            raise TypeError(f"manifest.endpoints[{i}] missing keys: {sorted(missing)}")
        if not isinstance(e.get("method"), str) or not isinstance(e.get("path"), str) or not isinstance(
            e.get("handler"), str
        ):
            raise TypeError(f"manifest.endpoints[{i}] method/path/handler must be string")
    return eps


def _set_diff(*, truth: set[str], declared: set[str]) -> dict[str, list[str]]:
    missing = sorted([x for x in truth if x not in declared])
    extra = sorted([x for x in declared if x not in truth])
    return {"missing": missing, "extra": extra}


def _format_diff(title: str, d: dict[str, list[str]]) -> str:
    parts: list[str] = []
    if d["missing"]:
        parts.append("  缺失（truth->manifest）：")
        for x in d["missing"][:60]:
            parts.append(f"    - {x}")
        if len(d["missing"]) > 60:
            parts.append(f"    ... and {len(d['missing']) - 60} more")
    if d["extra"]:
        parts.append("  多余（manifest->truth）：")
        for x in d["extra"][:60]:
            parts.append(f"    - {x}")
        if len(d["extra"]) > 60:
            parts.append(f"    ... and {len(d['extra']) - 60} more")
    if not parts:
        return f"{title}: OK"
    return "\n".join([f"{title}: FAIL"] + parts)


def _endpoint_key(method: str, path: str) -> str:
    return f"{method.upper()} {path}"


def _endpoint_diff(truth: list[EndpointTruth], declared: list[dict[str, Any]]) -> list[str]:
    truth_map = {_endpoint_key(e.method, e.path): e for e in truth}
    declared_map: dict[str, dict[str, Any]] = {}
    for e in declared:
        k = _endpoint_key(str(e.get("method", "")).upper(), str(e.get("path", "")))
        declared_map[k] = e

    missing = sorted([k for k in truth_map.keys() if k not in declared_map])
    extra = sorted([k for k in declared_map.keys() if k not in truth_map])
    changed: list[str] = []
    for k, te in truth_map.items():
        de = declared_map.get(k)
        if not de:
            continue
        handler = de.get("handler")
        if isinstance(handler, str) and handler != te.handler:
            changed.append(f"{k}: handler truth={te.handler!r} manifest={handler!r}")

    msgs: list[str] = []
    if missing:
        msgs.append("Endpoints 缺失（truth->manifest）：\n" + "\n".join([f"  - {x}" for x in missing]))
    if extra:
        msgs.append("Endpoints 多余（manifest->truth）：\n" + "\n".join([f"  - {x}" for x in extra]))
    if changed:
        msgs.append("Endpoints 不一致（同 method+path）：\n" + "\n".join([f"  - {x}" for x in changed]))
    return msgs


def main() -> int:
    try:
        manifest = _load_manifest()
        manifest_env = set(_expect_list_str(manifest, "env"))
        manifest_tables, manifest_rpc = _expect_supabase(manifest)
        manifest_tables_set = set(manifest_tables)
        manifest_rpc_set = set(manifest_rpc)
        manifest_endpoints = _expect_endpoints(manifest)

        index_path = API_DIR / "index.py"
        if not index_path.exists():
            print("FAIL: missing api/index.py")
            return 2

        index_text = _read_text(index_path)
        endpoint_truth = _extract_endpoints_from_index(index_text)

        py_text_all = "\n".join([_read_text(p) for p in _iter_py_files()])
        env_truth = _filter_key_envs(_extract_env_names_from_text(py_text_all))
        rpc_truth = _extract_rpc_names_from_text(py_text_all)
        table_truth = _extract_table_names_from_text(py_text_all)

        sql_text_all = "\n".join([_read_text(p) for p in _iter_sql_files()])
        sql_tables = _extract_sql_tables(sql_text_all)
        sql_funcs = _extract_sql_public_functions(sql_text_all)

        # 将“代码调用 + SQL 定义”合并为 truth（manifest 必须覆盖）
        tables_truth = set(sorted(table_truth | sql_tables))
        rpc_truth2 = set(sorted(rpc_truth | sql_funcs))

        problems: list[str] = []
        problems += _endpoint_diff(endpoint_truth, manifest_endpoints)

        d_tables = _set_diff(truth=tables_truth, declared=manifest_tables_set)
        if d_tables["missing"] or d_tables["extra"]:
            problems.append(_format_diff("Supabase tables", d_tables))

        d_rpc = _set_diff(truth=rpc_truth2, declared=manifest_rpc_set)
        if d_rpc["missing"] or d_rpc["extra"]:
            problems.append(_format_diff("Supabase RPC (public functions)", d_rpc))

        d_env = _set_diff(truth=env_truth, declared=manifest_env)
        if d_env["missing"] or d_env["extra"]:
            problems.append(_format_diff("Key env vars", d_env))

        # anchors：只做结构校验 + symbol 可定位（避免把“锚点清单”做成强耦合）
        anchors = manifest.get("anchors")
        if not isinstance(anchors, list) or not all(isinstance(x, dict) for x in anchors):
            problems.append("Anchors: FAIL\n  manifest.anchors must be list[object]")
        else:
            for i, a in enumerate(anchors):
                p = a.get("path")
                sym = a.get("symbol")
                if not isinstance(p, str) or not isinstance(sym, str) or not p or not sym:
                    problems.append(f"Anchors: FAIL\n  anchors[{i}] requires path/symbol string")
                    break
                abs_p = (REPO_ROOT / p).resolve()
                if not abs_p.exists():
                    problems.append(f"Anchors: FAIL\n  anchors[{i}] path not found: {p}")
                    break
                try:
                    ln = _find_def_line(_read_text(abs_p), sym)
                except Exception:  # noqa: BLE001
                    ln = None
                if ln is None:
                    problems.append(f"Anchors: FAIL\n  anchors[{i}] symbol not found: {p}::{sym}")
                    break

        if problems:
            print("FAIL: manifest drift detected.\n")
            for msg in problems:
                print(msg)
                print()
            return 1

        print("OK: manifest matches code/SQL truth (endpoints/rpc/tables/env + anchors resolvable).")
        return 0

    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 2
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"ERROR: manifest invalid: {exc}")
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: unexpected: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

