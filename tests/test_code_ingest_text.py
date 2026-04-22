from __future__ import annotations

from pathlib import Path


def test_build_enhanced_code_text_contains_required_fields(tmp_path: Path):
    from api.code_ingest import build_enhanced_code_text, get_all_code_chunks

    # 构造一个最小 repo：写入一个 .py 文件
    repo = tmp_path
    p = repo / "api" / "demo.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        '"""module doc"""\n\n'
        "def foo(a: int) -> str:\n"
        '    """doc"""\n'
        "    return str(a)\n",
        encoding="utf-8",
    )

    chunks = get_all_code_chunks(repo_root=repo)
    assert chunks, "expected at least one chunk"

    # 找一个 function chunk
    fn = None
    for c in chunks:
        md = c.metadata
        if getattr(md, "chunk_type", "") == "function" and getattr(md, "name", "") == "foo":
            fn = c
            break
    assert fn is not None, "foo function chunk not found"

    text = build_enhanced_code_text(fn)
    assert "[Code Context]" in text
    assert "File:" in text
    assert "Module:" in text
    assert "Lines:" in text
    assert "Type:" in text
    assert "Name:" in text
    assert "Signature:" in text
    assert "---" in text
    assert "Content:" in text
    assert "def foo" in text

