"""Doc Review lab · 请求/响应 Pydantic 模型（task-audit profile 首版）。"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

DocReviewProfile = Literal["task-audit", "spec-audit"]
FindingSeverity = Literal["error", "warn", "info"]


class DocReviewRequest(BaseModel):
    """审查输入：本地读 path 或 paste 正文（线上 paste / GitHub path）。"""

    profile: DocReviewProfile = "task-audit"
    target_path: str | None = Field(
        default=None,
        description="仓库相对路径，如 docs/harness/tasks/active/task_xxx.md",
    )
    content: str | None = Field(
        default=None,
        description="直接粘贴 Markdown 正文（线上 OL-1 首选）",
    )

    @model_validator(mode="after")
    def require_path_or_content(self) -> DocReviewRequest:
        has_path = bool((self.target_path or "").strip())
        has_content = bool((self.content or "").strip())
        if not has_path and not has_content:
            raise ValueError("target_path 与 content 至少提供一个")
        return self


class DocReviewFinding(BaseModel):
    rule_id: str
    severity: FindingSeverity
    message: str
    section: str | None = None


class DocReviewResult(BaseModel):
    profile: DocReviewProfile
    target_path: str | None
    findings: list[DocReviewFinding] = Field(default_factory=list)
    review_md: str = ""
    ok: bool = True
    stub: bool = Field(
        default=True,
        description="true 表示尚未接入 Agently Flow，仅占位响应",
    )
