from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


def test_admin_ingest_type_code(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    # 避免 import 时加载真实 .env 影响（仍允许 dotenv 存在）
    index = importlib.import_module("api.index")
    importlib.reload(index)

    called: dict[str, object] = {}

    def fake_process_code_files(repo_root):
        called["repo_root"] = repo_root
        return {"filesScanned": 1, "chunksTotal": 2, "chunksInserted": 2, "rowsDeleted": 0}

    monkeypatch.setattr(index, "process_code_files", fake_process_code_files)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/admin/ingest?type=code",
        headers={"Authorization": "Bearer secret-token-1234567890"},
        json={},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["filesScanned"] == 1
    assert called["repo_root"] is None


def test_admin_ingest_type_code_repo_path(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    index = importlib.import_module("api.index")
    importlib.reload(index)

    called: dict[str, object] = {}

    def fake_process_code_files(repo_root):
        called["repo_root"] = repo_root
        return {"filesScanned": 1, "chunksTotal": 1, "chunksInserted": 1, "rowsDeleted": 0}

    monkeypatch.setattr(index, "process_code_files", fake_process_code_files)

    client = TestClient(index.app)
    res = client.post(
        f"/api/py/admin/ingest?type=code&repo_path={tmp_path}",
        headers={"Authorization": "Bearer secret-token-1234567890"},
        json={},
    )
    assert res.status_code == 200
    assert called["repo_root"] == tmp_path.resolve()
