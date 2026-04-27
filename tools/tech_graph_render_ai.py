from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "docs" / "_tech_graph" / "_manifest.json"
AI_MAIN_PATH = REPO_ROOT / "docs" / "_tech_graph" / "00_main.ai.md"

AUTO_BEGIN = "<!-- AUTO:ENDPOINTS_AND_ANCHORS BEGIN -->"
AUTO_END = "<!-- AUTO:ENDPOINTS_AND_ANCHORS END -->"


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _write_text_if_changed(p: Path, new_text: str) -> bool:
    old = _read_text(p) if p.exists() else ""
    if old == new_text:
        return False
    p.write_text(new_text, encoding="utf-8")
    return True


def _load_manifest() -> dict[str, Any]:
    raw = _read_text(MANIFEST_PATH)
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise TypeError("manifest root must be an object")
    return obj


def _fmt_endpoint(e: dict[str, Any]) -> str:
    method = str(e.get("method", "")).upper()
    path = str(e.get("path", ""))
    handler = str(e.get("handler", ""))
    anchor = e.get("anchor")
    if isinstance(anchor, dict):
        ap = str(anchor.get("path", "")).strip()
        sym = str(anchor.get("symbol", "")).strip()
        if ap and sym:
            return f"- `{method} {path}` → `{handler}`  // → `{ap}::{sym}`"
    return f"- `{method} {path}` → `{handler}`"


def _render_auto_block(manifest: dict[str, Any]) -> str:
    endpoints = manifest.get("endpoints")
    anchors = manifest.get("anchors")
    if not isinstance(endpoints, list) or not all(isinstance(x, dict) for x in endpoints):
        raise TypeError("manifest.endpoints must be list[object]")
    if not isinstance(anchors, list) or not all(isinstance(x, dict) for x in anchors):
        raise TypeError("manifest.anchors must be list[object]")

    endpoints_sorted = sorted(
        endpoints,
        key=lambda x: (str(x.get("path", "")), str(x.get("method", "")).upper(), str(x.get("handler", ""))),
    )

    anchor_pairs: list[tuple[str, str]] = []
    for a in anchors:
        p = str(a.get("path", "")).strip()
        sym = str(a.get("symbol", "")).strip()
        if p and sym:
            anchor_pairs.append((p, sym))
    anchors_sorted = sorted(set(anchor_pairs), key=lambda t: (t[0], t[1]))

    lines: list[str] = []
    lines.append("<!-- This block is auto-generated from docs/_tech_graph/_manifest.json. Do not edit manually. -->")
    lines.append("")
    lines.append("#### Endpoints（from manifest）")
    for e in endpoints_sorted:
        lines.append(_fmt_endpoint(e))
    lines.append("")
    lines.append("#### Anchors（from manifest）")
    for p, sym in anchors_sorted:
        lines.append(f"- `{p}::{sym}`")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _replace_auto_block(*, text: str, block_body: str) -> str:
    if AUTO_BEGIN not in text or AUTO_END not in text:
        # If the file doesn't have the markers, append a fresh block at EOF.
        if not text.endswith("\n"):
            text += "\n"
        return (
            text
            + "\n"
            + AUTO_BEGIN
            + "\n"
            + block_body
            + AUTO_END
            + "\n"
        )

    before, rest = text.split(AUTO_BEGIN, 1)
    _, after = rest.split(AUTO_END, 1)

    # Keep markers in place and replace only inner content.
    if not before.endswith("\n"):
        before += "\n"
    if not after.startswith("\n"):
        after = "\n" + after
    return before + AUTO_BEGIN + "\n" + block_body + AUTO_END + after


def main() -> int:
    manifest = _load_manifest()
    src = _read_text(AI_MAIN_PATH)
    block = _render_auto_block(manifest)
    out = _replace_auto_block(text=src, block_body=block)
    changed = _write_text_if_changed(AI_MAIN_PATH, out)
    if changed:
        print(f"UPDATED: {AI_MAIN_PATH.relative_to(REPO_ROOT)}")
    else:
        print(f"OK (no changes): {AI_MAIN_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

