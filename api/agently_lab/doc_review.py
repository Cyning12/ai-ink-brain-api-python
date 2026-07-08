"""文档审查业务入口（D3+ 接入 Agently TriggerFlow）。"""

from __future__ import annotations

from pathlib import Path

from api.agently_lab.schemas import DocReviewFinding, DocReviewRequest, DocReviewResult

# 本地读 path 时的前缀白名单（与 RUNTIME_agently_parallel_learning_track §4.5 一致）
_ALLOWED_PATH_PREFIXES = (
    "docs/harness/",
    "docs/tasks/",
    "content/tasks/",
    "docs/spec/",
)


def _normalize_repo_relative_path(raw: str) -> str:
    path = raw.strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    path = path.lstrip("/")
    if ".." in path.split("/"):
        raise ValueError("path 不允许包含 ..")
    return path


def assert_path_allowed(repo_relative: str) -> None:
    if not any(repo_relative.startswith(prefix) for prefix in _ALLOWED_PATH_PREFIXES):
        allowed = ", ".join(_ALLOWED_PATH_PREFIXES)
        raise ValueError(f"path 不在白名单内，允许前缀: {allowed}")


def load_markdown_for_review(*, repo_root: Path, request: DocReviewRequest) -> tuple[str, str | None]:
    """返回 (markdown_text, resolved_path)。"""
    if (request.content or "").strip():
        return request.content.strip(), request.target_path

    if not request.target_path:
        raise ValueError("target_path 与 content 至少提供一个")

    rel = _normalize_repo_relative_path(request.target_path)
    assert_path_allowed(rel)
    abs_path = (repo_root / rel).resolve()
    if not abs_path.is_file():
        raise FileNotFoundError(f"文件不存在: {rel}")
    return abs_path.read_text(encoding="utf-8"), rel


def run_doc_review_stub(
    *,
    request: DocReviewRequest,
    repo_root: Path,
) -> DocReviewResult:
    """占位实现：读入文档并返回最小 findings，供 D3 前联调路由与 schema。"""
    markdown, resolved_path = load_markdown_for_review(repo_root=repo_root, request=request)
    line_count = len(markdown.splitlines())
    findings = [
        DocReviewFinding(
            rule_id="LAB-STUB-001",
            severity="info",
            message=f"Agently Flow 未接入；已读取 {line_count} 行 Markdown，profile={request.profile}",
            section=None,
        ),
    ]
    review_md = (
        f"# Doc Review（stub）\n\n"
        f"- **profile**: `{request.profile}`\n"
        f"- **path**: `{resolved_path or '(paste)'}`\n"
        f"- **lines**: {line_count}\n\n"
        f"> 在 `api/agently_lab/doc_review.py` 接入 Agently TriggerFlow。\n"
    )
    return DocReviewResult(
        profile=request.profile,
        target_path=resolved_path,
        findings=findings,
        review_md=review_md,
        ok=True,
        stub=True,
    )
