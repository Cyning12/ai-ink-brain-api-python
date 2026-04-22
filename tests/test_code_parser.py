from __future__ import annotations

from pathlib import Path

import pytest


def _write(tmp_path: Path, rel: str, content: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def test_parse_simple_function(tmp_path: Path):
    from api.code_parser import parse_python_file

    repo = tmp_path
    fp = _write(
        tmp_path,
        "api/demo.py",
        "def foo():\n    pass\n",
    )
    chunks = parse_python_file(fp, repo_root=repo)
    assert any(c.chunk_type == "function" and c.name == "foo" for c in chunks)


def test_parse_class_and_method(tmp_path: Path):
    from api.code_parser import parse_python_file

    repo = tmp_path
    fp = _write(
        tmp_path,
        "api/demo2.py",
        "class A:\n    \"\"\"doc\"\"\"\n\n    def bar(self):\n        pass\n",
    )
    chunks = parse_python_file(fp, repo_root=repo)
    assert any(c.chunk_type == "class" and c.name == "A" for c in chunks)
    assert any(c.chunk_type == "method" and c.name == "A.bar" for c in chunks)


def test_parse_async_function_signature_contains_async(tmp_path: Path):
    from api.code_parser import parse_python_file

    repo = tmp_path
    fp = _write(tmp_path, "api/demo3.py", "async def baz():\n    return 1\n")
    chunks = parse_python_file(fp, repo_root=repo)
    baz = [c for c in chunks if c.name == "baz" and c.chunk_type == "function"]
    assert baz, "baz chunk not found"
    assert "async def" in baz[0].signature


def test_parse_decorated_function_signature_keeps_decorator(tmp_path: Path):
    from api.code_parser import parse_python_file

    repo = tmp_path
    fp = _write(
        tmp_path,
        "api/demo4.py",
        "@app.get(\"/\")\n"
        "def home():\n"
        "    return \"ok\"\n",
    )
    chunks = parse_python_file(fp, repo_root=repo)
    home = [c for c in chunks if c.name == "home" and c.chunk_type == "function"]
    assert home, "home chunk not found"
    assert "@app.get" in home[0].signature


def test_parse_module_docstring_chunk(tmp_path: Path):
    from api.code_parser import parse_python_file

    repo = tmp_path
    fp = _write(
        tmp_path,
        "api/demo5.py",
        "\"\"\"module doc\"\"\"\n\ndef foo():\n    pass\n",
    )
    chunks = parse_python_file(fp, repo_root=repo)
    assert any(c.chunk_type == "module_doc" for c in chunks)


def test_parse_syntax_error_raises(tmp_path: Path):
    from api.code_parser import parse_python_file

    repo = tmp_path
    fp = _write(tmp_path, "api/bad.py", "def foo(\n")
    with pytest.raises(SyntaxError):
        parse_python_file(fp, repo_root=repo)

