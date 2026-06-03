from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from tech_graph_ci_stderr import CiIssue, print_ci_failure

API_DIR = REPO_ROOT / "api"
SQL_DIR = REPO_ROOT / "supabase" / "sql"
DEFAULT_BACKEND_MANIFEST = REPO_ROOT / "docs" / "_tech_graph" / "_manifest.json"

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
    "SYNC_ADMIN_SECRET",
    "NODE_ENV",
    "CONTENT_ROOT",
    "CONTENT_DEFAULT_YEAR",
    "EMBEDDING_DIM",
    "MAX_X_SOURCES_HEADER_CHARS",
}

FRONTEND_KEY_ENV_PREFIX = (
    "NEXT_PUBLIC_",
    "SUPABASE_",
    "SILICONFLOW_",
    "RAG_",
    "EMBEDDING_",
    "DASHSCOPE_",
)
FRONTEND_KEY_ENV_EXACT = {
    "NODE_ENV",
    "PY_API_URL",
    "CHAT_API_SECRET",
    "EMBEDDING_PROVIDER",
    "EMBEDDING_DIM",
}

HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")


@dataclass(frozen=True)
class EndpointTruth:
    method: str
    path: str
    handler: str
    line: int


@dataclass(frozen=True)
class RouteTruth:
    method: str
    path: str


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


def _filter_key_envs(envs: Iterable[str], *, exact: set[str], prefixes: tuple[str, ...]) -> set[str]:
    out: set[str] = set()
    for e in envs:
        if e in exact:
            out.add(e)
            continue
        if any(e.startswith(p) for p in prefixes):
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


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing manifest: {path}")
    raw = _read_text(path)
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


def _expect_routes(obj: dict[str, Any]) -> list[dict[str, Any]]:
    routes = obj.get("routes")
    if not isinstance(routes, list) or not all(isinstance(x, dict) for x in routes):
        raise TypeError("manifest.routes must be list[object]")
    for i, r in enumerate(routes):
        if not isinstance(r.get("method"), str) or not isinstance(r.get("path"), str):
            raise TypeError(f"manifest.routes[{i}] method/path must be string")
    return routes


def _set_diff(*, truth: set[str], declared: set[str]) -> dict[str, list[str]]:
    missing = sorted([x for x in truth if x not in declared])
    extra = sorted([x for x in declared if x not in truth])
    return {"missing": missing, "extra": extra}


def _summarize_items(items: list[str], *, limit: int = 8) -> str:
    if not items:
        return "（无）"
    head = ", ".join(items[:limit])
    if len(items) > limit:
        return f"{head} … 共 {len(items)} 项"
    return head


def _set_diff_issues(*, location: str, d: dict[str, list[str]]) -> list[CiIssue]:
    issues: list[CiIssue] = []
    if d["missing"]:
        issues.append(
            CiIssue(
                location=location,
                declared=f"manifest 未声明: {_summarize_items(d['missing'])}",
                actual=f"代码/SQL truth 存在: {_summarize_items(d['missing'])}",
            )
        )
    if d["extra"]:
        issues.append(
            CiIssue(
                location=location,
                declared=f"manifest 多余声明: {_summarize_items(d['extra'])}",
                actual=f"代码/SQL truth 不存在上述项",
            )
        )
    return issues


def _endpoint_key(method: str, path: str) -> str:
    return f"{method.upper()} {path}"


def _endpoint_diff(truth: list[EndpointTruth], declared: list[dict[str, Any]]) -> list[CiIssue]:
    truth_map = {_endpoint_key(e.method, e.path): e for e in truth}
    declared_map: dict[str, dict[str, Any]] = {}
    for e in declared:
        k = _endpoint_key(str(e.get("method", "")).upper(), str(e.get("path", "")))
        declared_map[k] = e

    issues: list[CiIssue] = []
    for k in sorted([k for k in truth_map.keys() if k not in declared_map]):
        te = truth_map[k]
        issues.append(
            CiIssue(
                location=f"manifest.endpoints · {k}",
                declared="manifest 未声明此 HTTP 路由",
                actual=f"api/index.py handler={te.handler!r} @ L{te.line}",
            )
        )
    for k in sorted([k for k in declared_map.keys() if k not in truth_map]):
        handler = declared_map[k].get("handler", "?")
        issues.append(
            CiIssue(
                location=f"manifest.endpoints · {k}",
                declared=f"manifest handler={handler!r}",
                actual="api/index.py 无对应路由装饰器",
            )
        )
    for k, te in truth_map.items():
        de = declared_map.get(k)
        if not de:
            continue
        handler = de.get("handler")
        if isinstance(handler, str) and handler != te.handler:
            issues.append(
                CiIssue(
                    location=f"manifest.endpoints · {k}",
                    declared=f"manifest handler={handler!r}",
                    actual=f"api/index.py handler={te.handler!r} @ L{te.line}",
                )
            )
    return issues


def _route_diff(truth: list[RouteTruth], declared: list[dict[str, Any]]) -> list[CiIssue]:
    truth_keys = {_endpoint_key(r.method, r.path) for r in truth}
    declared_keys = {
        _endpoint_key(str(r.get("method", "")).upper(), str(r.get("path", ""))) for r in declared
    }
    issues: list[CiIssue] = []
    for k in sorted([k for k in truth_keys if k not in declared_keys]):
        issues.append(
            CiIssue(
                location=f"manifest.routes · {k}",
                declared="manifest 未声明此 Next route",
                actual="app/ 存在对应 route.ts",
            )
        )
    for k in sorted([k for k in declared_keys if k not in truth_keys]):
        issues.append(
            CiIssue(
                location=f"manifest.routes · {k}",
                declared="manifest 声明了此 route",
                actual="app/ 无对应 route.ts",
            )
        )
    return issues


def _is_route_group_segment(segment: str) -> bool:
    return segment.startswith("(") and segment.endswith(")")


def _page_path_to_url(page_tsx: Path, app_dir: Path) -> str:
    rel = page_tsx.relative_to(app_dir)
    segments = [s for s in rel.parts[:-1] if not _is_route_group_segment(s)]
    if not segments:
        return "/"
    return "/" + "/".join(segments)


def _route_file_to_url(route_ts: Path, app_dir: Path) -> str:
    rel = route_ts.relative_to(app_dir)
    if len(rel.parts) < 3 or rel.parts[0] != "api" or rel.parts[-1] != "route.ts":
        raise ValueError(f"unexpected route file layout: {route_ts}")
    segments = [s for s in rel.parts[1:-1] if not _is_route_group_segment(s)]
    return "/api/" + "/".join(segments)


def _extract_http_methods_from_route(text: str) -> list[str]:
    methods: list[str] = []
    pat = re.compile(
        r"(?m)^export\s+(?:async\s+)?function\s+(GET|POST|PUT|PATCH|DELETE)\b",
    )
    for m in pat.finditer(text):
        methods.append(m.group(1).upper())
    return methods


def _extract_frontend_pages(app_dir: Path) -> set[str]:
    pages: set[str] = set()
    for page in sorted(app_dir.rglob("page.tsx")):
        if not page.is_file():
            continue
        pages.add(_page_path_to_url(page, app_dir))
    return pages


def _extract_frontend_routes(app_dir: Path) -> list[RouteTruth]:
    api_dir = app_dir / "api"
    if not api_dir.is_dir():
        return []
    out: list[RouteTruth] = []
    for route_file in sorted(api_dir.rglob("route.ts")):
        text = _read_text(route_file)
        url = _route_file_to_url(route_file, app_dir)
        for method in _extract_http_methods_from_route(text):
            out.append(RouteTruth(method=method, path=url))
    out.sort(key=lambda r: (r.path, r.method))
    return out


def _extract_frontend_env_names(repo_root: Path) -> set[str]:
    names: set[str] = set()
    scan_roots = [repo_root / "lib", repo_root / "app" / "api"]
    dot_pat = re.compile(r"process\.env\.([A-Z][A-Z0-9_]*)")
    bracket_pat = re.compile(r'process\.env\[["\']([A-Z][A-Z0-9_]*)["\']\]')
    must_get_pat = re.compile(r'mustGetEnv\(["\']([A-Z][A-Z0-9_]*)["\']\)')
    for root in scan_roots:
        if not root.is_dir():
            continue
        for ts in sorted(root.rglob("*.ts")) + sorted(root.rglob("*.tsx")):
            if not ts.is_file():
                continue
            text = _read_text(ts)
            names |= set(dot_pat.findall(text))
            names |= set(bracket_pat.findall(text))
            names |= set(must_get_pat.findall(text))
    return _filter_key_envs(
        names,
        exact=FRONTEND_KEY_ENV_EXACT,
        prefixes=FRONTEND_KEY_ENV_PREFIX,
    )


def _run_backend_check(*, manifest_path: Path) -> int:
    try:
        manifest = _load_manifest(manifest_path)
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
        env_truth = _filter_key_envs(
            _extract_env_names_from_text(py_text_all),
            exact=KEY_ENV_EXACT,
            prefixes=KEY_ENV_PREFIX,
        )
        rpc_truth = _extract_rpc_names_from_text(py_text_all)
        table_truth = _extract_table_names_from_text(py_text_all)

        sql_text_all = "\n".join([_read_text(p) for p in _iter_sql_files()])
        sql_tables = _extract_sql_tables(sql_text_all)
        sql_funcs = _extract_sql_public_functions(sql_text_all)

        tables_truth = set(sorted(table_truth | sql_tables))
        rpc_truth2 = set(sorted(rpc_truth | sql_funcs))

        issues: list[CiIssue] = []
        issues += _endpoint_diff(endpoint_truth, manifest_endpoints)

        d_tables = _set_diff(truth=tables_truth, declared=manifest_tables_set)
        issues += _set_diff_issues(location="manifest.supabase.tables", d=d_tables)

        d_rpc = _set_diff(truth=rpc_truth2, declared=manifest_rpc_set)
        issues += _set_diff_issues(location="manifest.supabase.rpc", d=d_rpc)

        d_env = _set_diff(truth=env_truth, declared=manifest_env)
        issues += _set_diff_issues(location="manifest.env", d=d_env)

        anchors = manifest.get("anchors")
        if not isinstance(anchors, list) or not all(isinstance(x, dict) for x in anchors):
            issues.append(
                CiIssue(
                    location="manifest.anchors",
                    declared="anchors 须为 list[object]",
                    actual=f"当前类型: {type(anchors).__name__}",
                )
            )
        else:
            for i, a in enumerate(anchors):
                p = a.get("path")
                sym = a.get("symbol")
                if not isinstance(p, str) or not isinstance(sym, str) or not p or not sym:
                    issues.append(
                        CiIssue(
                            location=f"manifest.anchors[{i}]",
                            declared="path + symbol 字符串",
                            actual=f"path={p!r} symbol={sym!r}",
                        )
                    )
                    break
                abs_p = (REPO_ROOT / p).resolve()
                if not abs_p.exists():
                    issues.append(
                        CiIssue(
                            location=f"manifest.anchors[{i}] · {p}::{sym}",
                            declared=f"锚点文件 {p}",
                            actual="文件不存在",
                        )
                    )
                    break
                try:
                    ln = _find_def_line(_read_text(abs_p), sym)
                except Exception:  # noqa: BLE001
                    ln = None
                if ln is None:
                    issues.append(
                        CiIssue(
                            location=f"manifest.anchors[{i}] · {p}::{sym}",
                            declared=f"symbol {sym!r}",
                            actual=f"{p} 中未找到 def/class {sym!r}",
                        )
                    )
                    break

        if issues:
            print_ci_failure(
                title="合并被阻塞：manifest 锚点与代码不一致",
                check_name="tech_graph_manifest_check",
                local_command="python tools/tech_graph_manifest_check.py",
                issues=issues,
            )
            return 1

        ai_main = REPO_ROOT / "docs" / "_tech_graph" / "00_main.ai.md"
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


def _run_frontend_check(*, repo_root: Path, manifest_path: Path) -> int:
    try:
        manifest = _load_manifest(manifest_path)
        schema = manifest.get("schema_version")
        if schema != "tech_graph_manifest_v1":
            raise TypeError(f"manifest.schema_version must be tech_graph_manifest_v1, got {schema!r}")

        manifest_pages = set(_expect_list_str(manifest, "pages"))
        manifest_routes = _expect_routes(manifest)
        manifest_env = set(_expect_list_str(manifest, "env"))

        app_dir = repo_root / "app"
        if not app_dir.is_dir():
            print(f"FAIL: missing app directory under repo root: {app_dir}")
            return 2

        pages_truth = _extract_frontend_pages(app_dir)
        routes_truth = _extract_frontend_routes(app_dir)
        env_truth = _extract_frontend_env_names(repo_root)

        issues: list[CiIssue] = []

        d_pages = _set_diff(truth=pages_truth, declared=manifest_pages)
        issues += _set_diff_issues(location="manifest.pages", d=d_pages)

        issues += _route_diff(routes_truth, manifest_routes)

        d_env = _set_diff(truth=env_truth, declared=manifest_env)
        issues += _set_diff_issues(location="manifest.env", d=d_env)

        if issues:
            print_ci_failure(
                title="合并被阻塞：frontend manifest 与代码不一致",
                check_name="tech_graph_manifest_check --repo frontend",
                local_command=(
                    "python tools/tech_graph_manifest_check.py "
                    "--repo frontend --repo-root <frontend-checkout>"
                ),
                issues=issues,
            )
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


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tech graph manifest drift check (backend or frontend).")
    parser.add_argument(
        "--repo",
        choices=("frontend",),
        default=None,
        help="Profile: frontend Next.js repo (requires --repo-root and --manifest).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root for --repo frontend (e.g. ai-ink-brain checkout).",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to _manifest.json (default: backend docs/_tech_graph/_manifest.json).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        if args.repo == "frontend":
            if args.repo_root is None:
                print("ERROR: --repo frontend requires --repo-root")
                return 2
            manifest_path = args.manifest
            if manifest_path is None:
                manifest_path = args.repo_root / "docs" / "_tech_graph" / "_manifest.json"
            return _run_frontend_check(repo_root=args.repo_root.resolve(), manifest_path=manifest_path.resolve())

        manifest_path = args.manifest if args.manifest is not None else DEFAULT_BACKEND_MANIFEST
        return _run_backend_check(manifest_path=manifest_path.resolve())

    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: unexpected: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
