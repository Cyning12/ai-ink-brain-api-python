"""Ops Desk GitHub → Supabase 同步（P0-2）+ 手动触发（P2-3）。"""

from .dispatch import (
    DISPATCH_REPO_NAME,
    DISPATCH_REPO_OWNER,
    DISPATCH_WORKFLOW_FILE,
    GitHubDispatchError,
    dispatch_sync_workflow,
)
from .router import router
from .runner import SyncRunResult, run_sync

__all__ = [
    "SyncRunResult",
    "run_sync",
    "router",
    "dispatch_sync_workflow",
    "GitHubDispatchError",
    "DISPATCH_REPO_OWNER",
    "DISPATCH_REPO_NAME",
    "DISPATCH_WORKFLOW_FILE",
]
