from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "docs" / "_tech_graph" / "_test_manifest.json"
API_DIR = REPO_ROOT / "api"
TESTS_DIR = REPO_ROOT / "tests"

REQUIRED_ENTRY_KEYS = {"id", "error_codes", "test_paths"}
OPTIONAL_ENTRY_KEYS = {"failure_path_ref", "pytest_markers", "graph_nodes_optional", "notes"}


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
                        problems.append(f"entries[{i}].test_paths[{j}] must start with 'tests/': {tp!r}")

        pytest_markers = entry.get("pytest_markers")
        if pytest_markers is not None:
            if not isinstance(pytest_markers, list) or not all(isinstance(x, str) for x in pytest_markers):
                problems.append(f"entries[{i}].pytest_markers must be list[str]")

        graph_nodes = entry.get("graph_nodes_optional")
        if graph_nodes is not None:
            if not isinstance(graph_nodes, list) or not all(isinstance(x, str) for x in graph_nodes):
                problems.append(f"entries[{i}].graph_nodes_optional must be list[str]")

    return problems


def _collect_all_test_files() -> list[Path]:
    return sorted([p for p in TESTS_DIR.rglob("*.py") if p.is_file()])


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


def _collect_api_text() -> str:
    texts: list[str] = []
    for py in sorted(API_DIR.rglob("*.py")):
        if py.is_file():
            texts.append(_read_text(py))
    return "\n".join(texts)


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

    if args.strict:
        api_text = _collect_api_text()
        problems += _validate_error_codes_strict(entries, api_text)

    if problems:
        print("FAIL: test manifest validation errors detected.\n")
        for msg in problems:
            print(f"  - {msg}")
        return 1

    strict_note = " + strict error_code scan" if args.strict else ""
    print(
        f"OK: test manifest valid ({len(entries)} entries, test_paths globs resolved){strict_note}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
