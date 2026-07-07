"""agently_lab 路由与 doc-review stub（需 AGENTLY_LAB_ENABLED）。"""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from api.index import app


@pytest.fixture
def lab_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("AGENTLY_LAB_ENABLED", "1")
    return TestClient(app)


def test_health_when_enabled(lab_client: TestClient) -> None:
    res = lab_client.get("/api/py/agently-lab/health")
    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True
    assert body["service"] == "agently-lab"


def test_doc_review_stub_paste(lab_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    # 本地 dev 无 legacy 秘钥时 deps 放行 maintainer
    monkeypatch.setattr("api.ops.deps.legacy_secret_candidates", lambda: [])
    res = lab_client.post(
        "/api/py/agently-lab/doc-review",
        json={"profile": "task-audit", "content": "# Task\n\n## 验收\n\n- [ ] item\n"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["stub"] is True
    assert body["profile"] == "task-audit"
    assert len(body["findings"]) >= 1


def test_health_disabled_by_default() -> None:
    prev = os.environ.pop("AGENTLY_LAB_ENABLED", None)
    try:
        client = TestClient(app)
        res = client.get("/api/py/agently-lab/health")
        assert res.status_code == 404
    finally:
        if prev is not None:
            os.environ["AGENTLY_LAB_ENABLED"] = prev
