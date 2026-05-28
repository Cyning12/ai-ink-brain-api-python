from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import tech_graph_test_manifest_check as manifest_check
from tools.tech_graph_test_manifest_check import main


def _make_manifest(entries: list[dict]) -> dict:
    return {
        "version": 1,
        "freeze_id": "TEST@2026-05-27",
        "entries": entries,
    }


def _write_manifest(tmp_path: Path, obj: dict) -> Path:
    p = tmp_path / "_test_manifest.json"
    p.write_text(json.dumps(obj), encoding="utf-8")
    return p


class TestValidManifest:
    def test_valid_manifest_passes(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-001",
                "error_codes": ["Invalid JSON"],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 0

    def test_multiple_entries_pass(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-001",
                "error_codes": ["Invalid JSON"],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
                "pytest_markers": ["unit"],
                "graph_nodes_optional": ["C1"],
                "notes": "test note",
            },
            {
                "id": "FP-TEST-002",
                "error_codes": ["Unauthorized"],
                "test_paths": ["tests/test_code_api_routes.py"],
            },
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 0


class TestBadGlob:
    def test_glob_matches_zero_files_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-BAD-GLOB",
                "error_codes": ["Invalid JSON"],
                "test_paths": ["tests/test_nonexistent_*.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1

    def test_glob_missing_tests_prefix_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-BAD-PREFIX",
                "error_codes": ["Invalid JSON"],
                "test_paths": ["test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1


class TestMissingRequiredField:
    def test_missing_id_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "error_codes": ["Invalid JSON"],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1

    def test_missing_error_codes_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-NO-CODES",
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1

    def test_missing_test_paths_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-NO-PATHS",
                "error_codes": ["Invalid JSON"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1


class TestStrictMode:
    def test_strict_missing_error_code_in_api_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-STRICT",
                "error_codes": ["THIS_ERROR_DOES_NOT_EXIST_IN_API"],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path), "--strict"])
        assert rc == 1

    def test_strict_existing_error_code_passes(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-STRICT-OK",
                "error_codes": ["Invalid JSON"],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path), "--strict"])
        assert rc == 0


class TestFailurePathsMode:
    def _write_task(self, tmp_path: Path, rel: str, body: str) -> None:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")

    def _patch_repo_root(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(manifest_check, "REPO_ROOT", tmp_path)
        monkeypatch.setattr(manifest_check, "TESTS_DIR", tmp_path / "tests")
        monkeypatch.setattr(manifest_check, "API_DIR", tmp_path / "api")
        (tmp_path / "api").mkdir(parents=True, exist_ok=True)

    def test_failure_paths_mode_passes(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        self._patch_repo_root(tmp_path, monkeypatch)
        task_rel = "docs/tasks/done/task_fp_sample.md"
        self._write_task(
            tmp_path,
            task_rel,
            """# Sample

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | DB down | returns `DATABASE_DISCONNECT` | 是 |
""",
        )
        test_py = tmp_path / "tests" / "test_fp_sample.py"
        test_py.parent.mkdir(parents=True, exist_ok=True)
        test_py.write_text("# stub\n", encoding="utf-8")
        manifest = _make_manifest([
            {
                "id": "FP-SAMPLE-DB",
                "failure_path_ref": f"{task_rel}#failure_paths",
                "error_codes": ["DATABASE_DISCONNECT"],
                "test_paths": ["tests/test_fp_sample.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path), "--check-failure-paths"])
        assert rc == 0

    def test_failure_paths_missing_task_file_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        self._patch_repo_root(tmp_path, monkeypatch)
        test_py = tmp_path / "tests" / "test_fp_sample.py"
        test_py.parent.mkdir(parents=True, exist_ok=True)
        test_py.write_text("# stub\n", encoding="utf-8")
        manifest = _make_manifest([
            {
                "id": "FP-MISSING-TASK",
                "failure_path_ref": "docs/tasks/done/task_does_not_exist.md#failure_paths",
                "error_codes": ["DATABASE_DISCONNECT"],
                "test_paths": ["tests/test_fp_sample.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path), "--check-failure-paths"])
        assert rc == 1

    def test_failure_paths_unknown_error_code_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        self._patch_repo_root(tmp_path, monkeypatch)
        task_rel = "docs/tasks/done/task_fp_bad_code.md"
        self._write_task(
            tmp_path,
            task_rel,
            """# Bad

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | x | no codes here | 是 |
""",
        )
        test_py = tmp_path / "tests" / "test_fp_bad.py"
        test_py.parent.mkdir(parents=True, exist_ok=True)
        test_py.write_text("# stub\n", encoding="utf-8")
        manifest = _make_manifest([
            {
                "id": "FP-BAD-CODE",
                "failure_path_ref": f"{task_rel}#failure_paths",
                "error_codes": ["TOTALLY_FAKE_ERROR_CODE_XYZ"],
                "test_paths": ["tests/test_fp_bad.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path), "--check-failure-paths"])
        assert rc == 1

    def test_production_manifest_failure_paths_passes(self) -> None:
        manifest = Path("docs/_tech_graph/_test_manifest.json")
        rc = main(["--manifest", str(manifest.resolve()), "--check-failure-paths"])
        assert rc == 0


class TestSchemaErrors:
    def test_empty_error_codes_list_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-EMPTY-CODES",
                "error_codes": [],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1

    def test_empty_test_paths_list_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-EMPTY-PATHS",
                "error_codes": ["Invalid JSON"],
                "test_paths": [],
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1

    def test_unknown_key_fails(self, tmp_path: Path) -> None:
        manifest = _make_manifest([
            {
                "id": "FP-TEST-UNKNOWN",
                "error_codes": ["Invalid JSON"],
                "test_paths": ["tests/test_unified_chat_backend_v1.py"],
                "extra_field": "should fail",
            }
        ])
        path = _write_manifest(tmp_path, manifest)
        rc = main(["--manifest", str(path)])
        assert rc == 1
