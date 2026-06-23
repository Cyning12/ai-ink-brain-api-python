"""GitHub workflow_dispatch 客户端：手动触发 sync GHA。"""

from __future__ import annotations

import os
from typing import Any

import httpx


class GitHubDispatchError(Exception):
    """GitHub dispatch 不可恢复错误。"""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


DISPATCH_REPO_OWNER = "Cyning12"
DISPATCH_REPO_NAME = "ai-ink-brain-api-python"
DISPATCH_WORKFLOW_FILE = "ops_sync_kimi_code.yml"
DISPATCH_REF = "main"


def _auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def has_active_sync_workflow_run(*, token: str) -> bool:
    """GHA 侧是否已有 queued / in_progress 的 ops-sync-kimi-code run。"""
    base = (
        f"https://api.github.com/repos/{DISPATCH_REPO_OWNER}/{DISPATCH_REPO_NAME}"
        f"/actions/workflows/{DISPATCH_WORKFLOW_FILE}/runs"
    )
    headers = _auth_headers(token)
    try:
        with httpx.Client(timeout=30) as client:
            for status in ("in_progress", "queued"):
                resp = client.get(f"{base}?status={status}&per_page=1", headers=headers)
                if resp.status_code != 200:
                    body = (resp.text or "")[:300]
                    raise GitHubDispatchError(
                        f"GitHub runs 查询失败 {resp.status_code}: {body}",
                        status_code=resp.status_code,
                    )
                data = resp.json()
                total = data.get("total_count", 0) if isinstance(data, dict) else 0
                if isinstance(total, int) and total > 0:
                    return True
    except httpx.HTTPError as exc:
        raise GitHubDispatchError(f"GitHub 网络错误: {exc}", status_code=None) from exc
    return False


def dispatch_sync_workflow(*, token: str | None = None) -> dict[str, Any]:
    """触发 workflow_dispatch；返回 GitHub API 响应体。"""
    resolved = (token or os.getenv("OPS_GITHUB_DISPATCH_TOKEN") or "").strip()
    if not resolved:
        raise GitHubDispatchError("缺少 OPS_GITHUB_DISPATCH_TOKEN", status_code=None)

    url = (
        f"https://api.github.com/repos/{DISPATCH_REPO_OWNER}/{DISPATCH_REPO_NAME}"
        f"/actions/workflows/{DISPATCH_WORKFLOW_FILE}/dispatches"
    )
    headers = _auth_headers(resolved)
    payload = {"ref": DISPATCH_REF}

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, json=payload)
    except httpx.HTTPError as exc:
        raise GitHubDispatchError(f"GitHub 网络错误: {exc}", status_code=None) from exc

    if resp.status_code == 204:
        return {"dispatched": True}

    # 403/422 等结构化错误
    body = (resp.text or "")[:500]
    raise GitHubDispatchError(
        f"GitHub dispatch 失败 {resp.status_code}: {body}",
        status_code=resp.status_code,
    )
