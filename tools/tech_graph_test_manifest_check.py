from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "docs" / "_tech_graph" / "_test_manifest.json"
API_DIR = REPO_ROOT / "api"
TESTS_DIR = REPO_ROOT / "tests"

REQUIRED_ENTRY_KEYS = {"id", "error_codes", "test_paths"}
OPTIONAL_ENTRY_KEYS = {"failure_path_ref", "pytest_markers", "graph_nodes_optional", "notes"}

_FAILURE_SECTION_RE = re.compile(
    r"(?m)^#{2,3}\s+(?:失败路径|failure_paths)\s*$",
    re.IGNORECASE,
)
_TABLE_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|")
_BACKTICK_CODE_RE = re.compile(r"`([^`]+)`")
_MANIFEST_EXEMPT_RE = re.compile(r"manifest_exempt", re.IGNORECASE)


@dataclass(frozen=True)
class FailurePathRow:
    row_id: str
    line: str
    error_codes: frozenset[str]


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing manifest: {path}")
    raw = _read_text(path)
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise TypeError("manifest root must be an object")
    return obj


def _parse_failure_path_ref(ref: str) -> tuple[Path, str]:
    text = ref.strip()
    if "#" in text:
        path_part, anchor = text.split("#", 1)
    else:
        path_part, anchor = text, "failure_paths"
    return (REPO_ROOT / path_part.strip()).resolve(), anchor.strip().lower()


def _extract_failure_paths_section(task_text: str) -> str | None:
    match = _FAILURE_SECTION_RE.search(task_text)
    if not match:
        return None
    start = match.end()
    rest = task_text[start:]
    lines: list[str] = []
    for line in rest.splitlines():
        if line.startswith("#") and lines:
            break
        if line.strip():
            lines.append(line)
        elif lines and not line.strip():
            # 允许表后空行；遇第二个空块且已有表则停
            if any(l.startswith("|") for l in lines):
                break
    body = "\n".join(lines).strip()
    return body if body else None


def _parse_failure_path_rows(section: str) -> list[FailurePathRow]:
    rows: list[FailurePathRow] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        if first.lower() in {"#", "id", "---", "----"}:
            continue
        if set(first) <= {"-", ":"}:
            continue
        row_id = first
        behavior = cells[2] if len(cells) > 2 else " ".join(cells[1:])
        codes = _extract_error_codes_from_text(behavior)
        rows.append(
            FailurePathRow(
                row_id=row_id,
                line=line,
                error_codes=frozenset(codes),
            )
        )
    return rows


def _extract_error_codes_from_text(text: str) -> set[str]:
    codes: set[str] = set()
    for match in _BACKTICK_CODE_RE.finditer(text):
        token = match.group(1).strip()
        if not token or len(token) > 120:
            continue
        if "=" in token and not token.startswith("HTTP"):
            continue
        if _looks_like_error_code(token):
            codes.add(token)
    for token in re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text):
        if _looks_like_error_code(token):
            codes.add(token)
    return codes


def _looks_like_error_code(token: str) -> bool:
    if token.lower() in {"http", "sse", "api", "sql", "fts", "rpc", "json"}:
        return False
    if token.endswith("Denied") or token.endswith("Error") or token.endswith("Exception"):
        return True
    if "_" in token and token.isupper():
        return True
    if " " in token and len(token) <= 80:
        return True
    if token in {
        "Invalid JSON",
        "Invalid ingest type",
        "Missing required field: query",
        "Client Closed Request",
        "Connection reset by peer",
        "Invalid token id",
        "Invalid access_level in token row",
    }:
        return True
    return False


def _collect_all_test_files() -> list[Path]:
    return sorted([p for p in TESTS_DIR.rglob("*.py") if p.is_file()])


def _resolve_test_glob_files(patterns: list[str]) -> list[Path]:
    all_test_files = _collect_all_test_files()
    matched: list[Path] = []
    for pattern in patterns:
        if not isinstance(pattern, str):
            continue
        for p in all_test_files:
            rel = str(p.relative_to(REPO_ROOT))
            if fnmatch.fnmatch(rel, pattern):
                matched.append(p)
    return matched


def _collect_api_text() -> str:
    texts: list[str] = []
    for py in sorted(API_DIR.rglob("*.py")):
        if py.is_file():
            texts.append(_read_text(py))
    return "\n".join(texts)


def _entry_corpus_text(entry: dict[str, Any], api_text: str) -> str:
    chunks: list[str] = [api_text]
    notes = entry.get("notes")
    if isinstance(notes, str):
        chunks.append(notes)
    test_paths = entry.get("test_paths")
    if isinstance(test_paths, list):
        for p in _resolve_test_glob_files(test_paths):
            chunks.append(_read_text(p))
    ref = entry.get("failure_path_ref")
    if isinstance(ref, str):
        task_path, _ = _parse_failure_path_ref(ref)
        if task_path.is_file():
            chunks.append(_read_text(task_path))
    return "\n".join(chunks)


def _validate_schema(obj: dict[str, Any]) -> list[str]:
    problems: list[str] = []

    if "version" not in obj:
        problems.append("manifest missing 'version'")
    elif not isinstance(obj["version"], int):
        problems.append("manifest.version must be int")

    if "freeze_id" not in obj:
        problems.append("manifest missing 'freeze_id'")
    elif not isinstance(obj["freeze_id"], str):
        problems.append("manifest.freeze_id must be str")

    entries = obj.get("entries")
    if not isinstance(entries, list):
        problems.append("manifest.entries must be a list")
        return problems

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"entries[{i}] must be an object")
            continue

        missing = REQUIRED_ENTRY_KEYS - set(entry.keys())
        if missing:
            problems.append(f"entries[{i}] missing required keys: {sorted(missing)}")

        extra = set(entry.keys()) - REQUIRED_ENTRY_KEYS - OPTIONAL_ENTRY_KEYS
        if extra:
            problems.append(f"entries[{i}] unknown keys: {sorted(extra)}")

        entry_id = entry.get("id")
        if isinstance(entry_id, str) and not entry_id:
            problems.append(f"entries[{i}].id must be non-empty string")

        error_codes = entry.get("error_codes")
        if error_codes is not None:
            if not isinstance(error_codes, list) or not all(isinstance(x, str) for x in error_codes):
                problems.append(f"entries[{i}].error_codes must be list[str]")
            elif not error_codes:
                problems.append(f"entries[{i}].error_codes must not be empty")

        test_paths = entry.get("test_paths")
        if test_paths is not None:
            if not isinstance(test_paths, list) or not all(isinstance(x, str) for x in test_paths):
                problems.append(f"entries[{i}].test_paths must be list[str]")
            elif not test_paths:
                problems.append(f"entries[{i}].test_paths must not be empty")
            else:
                for j, tp in enumerate(test_paths):
                    if not tp.startswith("tests/"):
                        problems.append(
                            f"entries[{i}].test_paths[{j}] must start with 'tests/': {tp!r}"
                        )

        pytest_markers = entry.get("pytest_markers")
        if pytest_markers is not None:
            if not isinstance(pytest_markers, list) or not all(
                isinstance(x, str) for x in pytest_markers
            ):
                problems.append(f"entries[{i}].pytest_markers must be list[str]")

        graph_nodes = entry.get("graph_nodes_optional")
        if graph_nodes is not None:
            if not isinstance(graph_nodes, list) or not all(isinstance(x, str) for x in graph_nodes):
                problems.append(f"entries[{i}].graph_nodes_optional must be list[str]")

    return problems


def _validate_test_paths(entries: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    all_test_files = _collect_all_test_files()
    all_test_rel_paths = [str(p.relative_to(REPO_ROOT)) for p in all_test_files]

    for i, entry in enumerate(entries):
        test_paths = entry.get("test_paths")
        if not isinstance(test_paths, list):
            continue

        entry_id = entry.get("id", f"entries[{i}]")
        for j, pattern in enumerate(test_paths):
            if not isinstance(pattern, str):
                continue
            matched = any(fnmatch.fnmatch(rel, pattern) for rel in all_test_rel_paths)
            if not matched:
                problems.append(
                    f"{entry_id}.test_paths[{j}] glob '{pattern}' matched 0 files under tests/"
                )

    return problems


def _validate_error_codes_strict(entries: list[dict[str, Any]], api_text: str) -> list[str]:
    problems: list[str] = []
    for i, entry in enumerate(entries):
        error_codes = entry.get("error_codes")
        if not isinstance(error_codes, list):
            continue

        entry_id = entry.get("id", f"entries[{i}]")
        for code in error_codes:
            if not isinstance(code, str):
                continue
            if code not in api_text:
                problems.append(
                    f"{entry_id} error_code '{code}' not found in api/*.py (strict mode)"
                )
    return problems


def _find_matching_row(
    rows: list[FailurePathRow],
    entry_id: str,
    manifest_codes: set[str],
) -> FailurePathRow | None:
    for row in rows:
        if row.row_id == entry_id:
            return row
    for row in rows:
        if entry_id in row.line:
            return row
    best: FailurePathRow | None = None
    best_overlap = 0
    for row in rows:
        overlap = len(row.error_codes & manifest_codes)
        if overlap > best_overlap:
            best_overlap = overlap
            best = row
    return best if best_overlap > 0 else None


def _validate_failure_paths(entries: list[dict[str, Any]], api_text: str) -> list[str]:
    problems: list[str] = []
    task_cache: dict[Path, tuple[str, list[FailurePathRow]]] = {}

    for i, entry in enumerate(entries):
        entry_id = entry.get("id", f"entries[{i}]")
        ref = entry.get("failure_path_ref")
        if not isinstance(ref, str) or not ref.strip():
            problems.append(f"{entry_id} missing failure_path_ref (--check-failure-paths)")
            continue

        error_codes = entry.get("error_codes")
        if not isinstance(error_codes, list):
            continue
        manifest_codes = {c for c in error_codes if isinstance(c, str)}

        try:
            task_path, _anchor = _parse_failure_path_ref(ref)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{entry_id} invalid failure_path_ref {ref!r}: {exc}")
            continue

        if not task_path.is_file():
            problems.append(f"{entry_id} failure_path_ref file not found: {task_path}")
            continue

        if task_path not in task_cache:
            task_text = _read_text(task_path)
            section = _extract_failure_paths_section(task_text)
            if section is None:
                task_cache[task_path] = (task_text, [])
                problems.append(
                    f"{entry_id} failure_paths section not found in {task_path.relative_to(REPO_ROOT)}"
                )
            else:
                task_cache[task_path] = (task_text, _parse_failure_path_rows(section))

        task_text, rows = task_cache[task_path]
        corpus = _entry_corpus_text(entry, api_text)

        for code in manifest_codes:
            if code not in corpus:
                problems.append(
                    f"{entry_id} error_code '{code}' not found in task/api/tests corpus"
                )

        task_linked = entry_id in task_text or any(c in task_text for c in manifest_codes)
        if not task_linked and not all(c in corpus for c in manifest_codes):
            problems.append(
                f"{entry_id} neither id nor error_codes appear in task file "
                f"{task_path.relative_to(REPO_ROOT)} and not all codes in api/tests corpus"
            )

        matched_row = _find_matching_row(rows, str(entry_id), manifest_codes)
        if matched_row is not None and matched_row.error_codes:
            if not manifest_codes <= matched_row.error_codes:
                problems.append(
                    f"{entry_id} error_codes {sorted(manifest_codes)} not subset of task row "
                    f"{matched_row.row_id} codes {sorted(matched_row.error_codes)}"
                )

    # task → manifest：仅检查被 manifest 引用的 task
    entries_by_task: dict[Path, list[dict[str, Any]]] = {}
    for entry in entries:
        ref = entry.get("failure_path_ref")
        if not isinstance(ref, str):
            continue
        task_path, _ = _parse_failure_path_ref(ref)
        entries_by_task.setdefault(task_path, []).append(entry)

    for task_path, task_entries in entries_by_task.items():
        if task_path not in task_cache:
            continue
        _task_text, rows = task_cache[task_path]
        if not rows:
            continue

        all_manifest_codes: set[str] = set()
        for entry in task_entries:
            ec = entry.get("error_codes")
            if isinstance(ec, list):
                all_manifest_codes.update(c for c in ec if isinstance(c, str))

        for row in rows:
            if _MANIFEST_EXEMPT_RE.search(row.line):
                continue
            if re.match(r"^FP-\d+$", row.row_id):
                continue
            if not row.error_codes and not row.row_id.startswith("FP-"):
                continue

            covered = False
            for entry in task_entries:
                eid = entry.get("id")
                ec = entry.get("error_codes")
                if not isinstance(eid, str) or not isinstance(ec, list):
                    continue
                codes = {c for c in ec if isinstance(c, str)}
                if row.row_id == eid or eid in row.line:
                    covered = True
                    if row.error_codes and not codes <= row.error_codes:
                        problems.append(
                            f"{task_path.relative_to(REPO_ROOT)} row {row.row_id} codes "
                            f"{sorted(row.error_codes)} missing manifest {eid} codes {sorted(codes)}"
                        )
                    break
                if row.error_codes and (row.error_codes & codes):
                    covered = True
                    break

            if not covered and row.error_codes and not (row.error_codes & all_manifest_codes):
                problems.append(
                    f"{task_path.relative_to(REPO_ROOT)} row {row.row_id} "
                    f"(codes {sorted(row.error_codes)}) has no matching manifest entry"
                )
            if (
                not covered
                and row.row_id.startswith("FP-")
                and row.row_id.count("-") >= 2
                and row.row_id not in {e.get("id") for e in task_entries if isinstance(e.get("id"), str)}
            ):
                problems.append(
                    f"{task_path.relative_to(REPO_ROOT)} row {row.row_id} "
                    "has no manifest entry with matching id"
                )

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tech Graph _test_manifest.json validator.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to _test_manifest.json (default: docs/_tech_graph/_test_manifest.json).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also verify that every error_code appears as a substring in api/*.py.",
    )
    parser.add_argument(
        "--check-failure-paths",
        action="store_true",
        help="Phase C: bidirectional task <-> manifest failure_path_ref checks.",
    )
    args = parser.parse_args(argv)

    manifest_path: Path = args.manifest.resolve()

    try:
        manifest = _load_manifest(manifest_path)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: manifest invalid JSON: {exc}")
        return 2
    except TypeError as exc:
        print(f"ERROR: manifest invalid: {exc}")
        return 2

    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        print("ERROR: manifest.entries must be a list")
        return 2

    problems: list[str] = []
    problems += _validate_schema(manifest)
    problems += _validate_test_paths(entries)

    api_text = _collect_api_text()

    if args.strict:
        problems += _validate_error_codes_strict(entries, api_text)

    if args.check_failure_paths:
        problems += _validate_failure_paths(entries, api_text)

    if problems:
        print("FAIL: test manifest validation errors detected.\n")
        for msg in problems:
            print(f"  - {msg}")
        return 1

    modes: list[str] = []
    if args.check_failure_paths:
        modes.append("failure-paths")
    if args.strict:
        modes.append("strict")
    mode_note = f" [{', '.join(modes)}]" if modes else ""
    print(
        f"OK: test manifest valid ({len(entries)} entries, test_paths globs resolved){mode_note}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
