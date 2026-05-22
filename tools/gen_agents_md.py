#!/usr/bin/env python3
"""Generate AGENTS.md rules section from .cursor/rules/*.mdc files.

Reads all .mdc rule files, strips YAML frontmatter, and writes the
concatenated result into AGENTS.md after the ``<!-- RULES_AUTO_GENERATED -->``
marker.  The hand-maintained header above the marker is preserved unchanged.

Usage::

    python tools/gen_agents_md.py           # regenerate
    python tools/gen_agents_md.py --check   # CI: exit 1 if AGENTS.md is stale
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / ".cursor" / "rules"
AGENTS_MD = ROOT / "AGENTS.md"
MARKER = "<!-- RULES_AUTO_GENERATED -->"


def _parse_frontmatter(text: str) -> tuple[str, dict[str, str]]:
    """Return (body, frontmatter_dict)."""
    if not text.startswith("---"):
        return text, {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text, {}
    fm: dict[str, str] = {}
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return parts[2].strip(), fm


def _section_name(stem: str) -> str:
    """Derive a readable section title from the filename stem.

    ``00-core`` → ``Core``, ``10-tech-graph`` → ``Tech Graph``.
    """
    # Strip numeric prefix
    name = re.sub(r"^\d{2,}-", "", stem)
    # Replace hyphens/underscores with spaces, title-case each word
    words = re.split(r"[-_]", name)
    return " ".join(w.capitalize() for w in words)


def generate() -> str:
    """Return the full AGENTS.md content (header + marker + rules)."""
    if not RULES_DIR.is_dir():
        sys.exit(f"Rules directory not found: {RULES_DIR}")

    # Read existing header (everything before the marker)
    header = ""
    if AGENTS_MD.exists():
        existing = AGENTS_MD.read_text(encoding="utf-8")
        if MARKER in existing:
            header = existing.split(MARKER)[0].rstrip()
        else:
            # No marker yet — treat whole file as header
            header = existing.rstrip()

    # Collect .mdc files in sorted order
    mdc_files = sorted(RULES_DIR.glob("*.mdc"))
    if not mdc_files:
        sys.exit(f"No .mdc files found in {RULES_DIR}")

    sections: list[str] = []
    for mdc in mdc_files:
        body, fm = _parse_frontmatter(mdc.read_text(encoding="utf-8"))
        title = _section_name(mdc.stem)
        desc = fm.get("description", "")
        heading = f"## {title}"
        if desc:
            heading += f"\n\n> {desc}"
        sections.append(f"{heading}\n\n{body}")

    generated = "\n\n---\n\n".join(sections)

    return f"{header}\n\n{MARKER}\n\n{generated}\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AGENTS.md from .mdc rules")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if AGENTS.md differs from generated content (CI mode)",
    )
    args = parser.parse_args()

    new_content = generate()

    if args.check:
        if not AGENTS_MD.exists():
            print("AGENTS.md does not exist — run without --check first")
            sys.exit(1)
        current = AGENTS_MD.read_text(encoding="utf-8")
        if current != new_content:
            print("AGENTS.md is stale. Run: python tools/gen_agents_md.py")
            sys.exit(1)
        print("AGENTS.md is up-to-date.")
        return

    AGENTS_MD.write_text(new_content, encoding="utf-8")
    mdc_count = len(list(RULES_DIR.glob("*.mdc")))
    print(f"AGENTS.md regenerated from {mdc_count} .mdc files")


if __name__ == "__main__":
    main()
