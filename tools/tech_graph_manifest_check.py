from __future__ import annotations

import argparse
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
    "SSE_",
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

FRONTEND_ENV_PREFIX = (
    "NEXT_PUBLIC_",
    "SUPABASE_",
    "SILICONFLOW_",
    "RAG_",
    "EMBEDDING_",
    "DASHSCOPE_",
)
FRONTEND_ENV_EXACT = {
    "NODE_ENV",
    "PY_API_URL",
    "CHAT_API_SECRET",
}

ROUTE_HANDLER_PAT = re.compile(
    r"(?m)^export\s+(?:async\s+)?function\s+(GET|POST|PUT|PATCH|DELETE)\b",
)


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
    pat = re.compile(rf"(?m)^(?:async\s+def|def|class)\s+{re.escape(symbol)}\b")
    m = pat.search(text)
    if not m:
        return None
    return text[: m.start()].count("\n") + 1


def _extract_endpoints_from_index(index_text: str) -> list[EndpointTruth]:
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
    return set(re.findall(r'\.rpc\("([A-Za-z0-9_]+)"\s*,', py_text))


def _extract_table_names_from_text(py_text: str) -> set[str]:
    return set(re.findall(r'\.table\("([A-Za-z0-9_]+)"\)', py_text))


def _extract_sql_tables(sql_text: str) -> set[str]:
    pat = re.compile(r"(?im)^\s*create\s+table\s+(?:if\s+not\s+exists\s+)?public\.([a-z0-9_]+)\b")
    return set([m.group(1) for m in pat.finditer(sql_text)])


def _extract_sql_public_functions(sql_text: str) -> set[str]:
    pat = re.compile(
        r"(?im)^\s*create\s+or\s+replace\s+function\s+public\.([a-z0-9_]+)\s*\(",
    )
    return set([m.group(1) for m in pat.finditer(sql_text)])


def _load_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    raw = _read_text(manifest_path)
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise TypeError("manifest root must be an object")
    return obj


def _is_route_group_segment(segment: str) -> bool:
    return segment.startswith("(") and segment.endswith(")")


def _page_url_from_page_file(repo_root: Path, page_file: Path) -> str:
    rel = page_file.relative_to(repo_root / "app")
    parts = [p for p in rel.parts if p != "page.tsx" and not _is_route_group_segment(p)]
    if not parts:
        return "/"
    return "/" + "/".join(parts)


def _api_url_from_route_file(repo_root: Path, route_file: Path) -> str:
    rel = route_file.relative_to(repo_root / "app" / "api")
    parts = [p for p in rel.parts if p != "route.ts" and not _is_route_group_segment(p)]
    return "/api/" + "/".join(parts)


def _extract_route_methods_from_text(route_text: str) -> list[str]:
    return sorted({m.group(1).upper() for m in ROUTE_HANDLER_PAT.finditer(route_text)})


def _collect_frontend_pages_truth(repo_root: Path) -> set[str]:
    app_dir = repo_root / "app"
    if not app_dir.is_dir():
        raise FileNotFoundError(f"missing app dir: {app_dir}")
    pages: set[str] = set()
    for page_file in sorted(app_dir.glob("**/page.tsx")):
        pages.add(_page_url_from_page_file(repo_root, page_file))
    return pages


def _collect_frontend_routes_truth(repo_root: Path) -> set[str]:
    api_dir = repo_root / "app" / "api"
    if not api_dir.is_dir():
        raise FileNotFoundError(f"missing app/api dir: {api_dir}")
    routes: set[str] = set()
    for route_file in sorted(api_dir.glob("**/route.ts")):
        url = _api_url_from_route_file(repo_root, route_file)
        text = _read_text(route_file)
        for method in _extract_route_methods_from_text(text):
            routes.add(_endpoint_key(method, url))
    return routes


def _iter_frontend_scan_files(repo_root: Path) -> list[Path]:
    roots = [repo_root / "lib", repo_root / "app" / "api"]
    out: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for pattern in ("**/*.ts", "**/*.tsx"):
            out.extend(root.glob(pattern))
    return sorted({p for p in out if p.is_file()})


def _extract_frontend_env_names_from_text(text: str) -> set[str]:
    names = set(re.findall(r"process\.env\.([A-Z0-9_]+)", text))
    names |= set(re.findall(r'process\.env\["([A-Z0-9_]+)"\]', text))
    names |= set(re.findall(r"process\.env\['([A-Z0-9_]+)'\]", text))
    names |= set(re.findall(r'mustGetEnv\("([A-Z0-9_]+)"\)', text))
    return names


def _filter_frontend_envs(envs: Iterable[str]) -> set[str]:
    out: set[str] = set()
    for e in envs:
        if e in FRONTEND_ENV_EXACT:
            out.add(e)
            continue
        if any(e.startswith(p) for p in FRONTEND_ENV_PREFIX):
            out.add(e)
    return out


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


def _expect_frontend_pages(obj: dict[str, Any]) -> list[str]:
    pages = obj.get("pages")
    if not isinstance(pages, list) or not all(isinstance(x, str) for x in pages):
        raise TypeError("manifest.pages must be list[str]")
    return pages


def _expect_frontend_routes(obj: dict[str, Any]) -> list[dict[str, Any]]:
    routes = obj.get("routes")
    if not isinstance(routes, list) or not all(isinstance(x, dict) for x in routes):
        raise TypeError("manifest.routes must be list[object]")
    required = {"method", "path"}
    for i, r in enumerate(routes):
        missing = required - set(r.keys())
        if missing:
            raise TypeError(f"manifest.routes[{i}] missing keys: {sorted(missing)}")
        if not isinstance(r.get("method"), str) or not isinstance(r.get("path"), str):
            raise TypeError(f"manifest.routes[{i}] method/path must be string")
    return routes


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


def _route_diff(truth: set[str], declared_routes: list[dict[str, Any]]) -> list[str]:
    declared_map = {
        _endpoint_key(str(r.get("method", "")).upper(), str(r.get("path", ""))): r
        for r in declared_routes
    }
    missing = sorted([k for k in truth if k not in declared_map])
    extra = sorted([k for k in declared_map.keys() if k not in truth])
    msgs: list[str] = []
    if missing:
        msgs.append("Routes 缺失（truth->manifest）：\n" + "\n".join([f"  - {x}" for x in missing]))
    if extra:
        msgs.append("Routes 多余（manifest->truth）：\n" + "\n".join([f"  - {x}" for x in extra]))
    return msgs


def _page_diff(truth: set[str], declared_pages: list[str]) -> list[str]:
    declared_set = set(declared_pages)
    d = _set_diff(truth=truth, declared=declared_set)
    if not d["missing"] and not d["extra"]:
        return []
    return [_format_diff("Pages", d)]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tech graph manifest drift check (api-python or frontend).")
    parser.add_argument(
        "--repo",
        choices=["frontend"],
        default=None,
        help="Repository profile. Default: api-python (unchanged legacy behavior).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root. Default: script parent dir (api-python) or required for --repo frontend.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to _manifest.json. Default: docs/_tech_graph/_manifest.json under repo-root.",
    )
    return parser.parse_args()


def _check_api_python(*, repo_root: Path, manifest_path: Path) -> int:
    api_dir = repo_root / "api"
    sql_dir = repo_root / "supabase" / "sql"
    try:
        manifest = _load_manifest(manifest_path)
        manifest_env = set(_expect_list_str(manifest, "env"))
        manifest_tables, manifest_rpc = _expect_supabase(manifest)
        manifest_tables_set = set(manifest_tables)
        manifest_rpc_set = set(manifest_rpc)
        manifest_endpoints = _expect_endpoints(manifest)

        index_path = api_dir / "index.py"
        if not index_path.exists():
            print("FAIL: missing api/index.py")
            return 2

        index_text = _read_text(index_path)
        endpoint_truth = _extract_endpoints_from_index(index_text)

        py_files = sorted([p for p in api_dir.glob("*.py") if p.is_file()]) if api_dir.is_dir() else []
        py_text_all = "\n".join([_read_text(p) for p in py_files])
        env_truth = _filter_key_envs(_extract_env_names_from_text(py_text_all))
        rpc_truth = _extract_rpc_names_from_text(py_text_all)
        table_truth = _extract_table_names_from_text(py_text_all)

        sql_files = (
            sorted([p for p in sql_dir.glob("*.sql") if p.is_file()]) if sql_dir.is_dir() else []
        )
        sql_text_all = "\n".join([_read_text(p) for p in sql_files])
        sql_tables = _extract_sql_tables(sql_text_all)
        sql_funcs = _extract_sql_public_functions(sql_text_all)

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
                abs_p = (repo_root / p).resolve()
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

        ai_main = repo_root / "docs" / "_tech_graph" / "00_main.ai.md"
        if ai_main.exists():
            t = _read_text(ai_main)
            if "<!-- AUTO:ENDPOINTS_AND_ANCHORS BEGIN -->" in t and "<!-- AUTO:ENDPOINTS_AND_ANCHORS END -->" in t:
                print("OK: manifest matches code/SQL truth (endpoints/rpc/tables/env + anchors resolvable).")
                print("TIP: 若 `docs/_tech_graph/00_main.ai.md` 的 auto 区块未同步，可运行：python tools/tech_graph_render_ai.py")
                return 0

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


def _check_frontend(*, repo_root: Path, manifest_path: Path) -> int:
    try:
        manifest = _load_manifest(manifest_path)
        if manifest.get("repo") != "ai-ink-brain":
            print('WARN: manifest.repo is not "ai-ink-brain" (frontend profile)')

        manifest_pages = _expect_frontend_pages(manifest)
        manifest_routes = _expect_frontend_routes(manifest)
        manifest_env = set(_expect_list_str(manifest, "env"))

        pages_truth = _collect_frontend_pages_truth(repo_root)
        routes_truth = _collect_frontend_routes_truth(repo_root)
        scan_text = "\n".join([_read_text(p) for p in _iter_frontend_scan_files(repo_root)])
        env_truth = _filter_frontend_envs(_extract_frontend_env_names_from_text(scan_text))

        problems: list[str] = []
        problems += _page_diff(pages_truth, manifest_pages)
        problems += _route_diff(routes_truth, manifest_routes)

        d_env = _set_diff(truth=env_truth, declared=manifest_env)
        if d_env["missing"] or d_env["extra"]:
            problems.append(_format_diff("Key env vars", d_env))

        if problems:
            print("FAIL: frontend manifest drift detected.\n")
            for msg in problems:
                print(msg)
                print()
            return 1

        print(
            "OK: frontend manifest matches code truth "
            f"(pages={len(pages_truth)}, routes={len(routes_truth)}, env={len(env_truth)})."
        )
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


def main() -> int:
    args = _parse_args()
    if args.repo == "frontend":
        repo_root = (args.repo_root or Path.cwd()).resolve()
        manifest_path = (args.manifest or (repo_root / "docs" / "_tech_graph" / "_manifest.json")).resolve()
        return _check_frontend(repo_root=repo_root, manifest_path=manifest_path)

    repo_root = (args.repo_root or REPO_ROOT).resolve()
    manifest_path = (args.manifest or MANIFEST_PATH).resolve()
    return _check_api_python(repo_root=repo_root, manifest_path=manifest_path)


if __name__ == "__main__":
    raise SystemExit(main())
