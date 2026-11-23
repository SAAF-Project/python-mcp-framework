"""Offline filesystem boundaries and real stdio refusal; no external tools."""

import asyncio
import json
import sys

import pytest
from test_starter import load_script


@pytest.mark.parametrize("location", ["src", "package", "nested", "file"])
def test_bundle_rejects_symlinked_source_before_install(tmp_path, monkeypatch, location):
    bundle = load_script("build_bundle")
    root = tmp_path / "project"
    package = root / "src/usecase_mcp"
    package.mkdir(parents=True)
    (package / "server.py").write_text("# synthetic source")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "private.py").write_text("# synthetic, not for distribution")
    if location == "src":
        (package / "server.py").unlink()
        package.rmdir()
        (root / "src").rmdir()
        target, destination = root / "src", outside
    elif location == "package":
        (package / "server.py").unlink()
        package.rmdir()
        target, destination = package, outside
    elif location == "nested":
        target, destination = package / "nested", outside
    else:
        target, destination = package / "linked.py", outside / "private.py"
    target.symlink_to(destination, target_is_directory=location != "file")

    def no_process(*args, **kwargs):
        pytest.fail("A rejected source tree must not start an installer")

    monkeypatch.setattr(bundle.subprocess, "run", no_process)
    with pytest.raises(RuntimeError, match="symlink"):
        bundle.build_bundle(root)
    assert not (root / "dist").exists()


@pytest.mark.parametrize("exists", [False, True])
def test_bundle_rejects_missing_or_empty_source(tmp_path, exists):
    if exists:
        (tmp_path / "src/usecase_mcp").mkdir(parents=True)
    with pytest.raises(RuntimeError, match="missing|no Python source"):
        load_script("build_bundle").source_files(tmp_path)


def test_bundle_sources_remain_sorted_and_exclude_non_sources(tmp_path):
    package = tmp_path / "src/usecase_mcp"
    package.mkdir(parents=True)
    for name in ("z.py", "a.py", "notes.json", ".env"):
        (package / name).write_text("# synthetic")
    (package / "directory.py").mkdir()
    cache = package / "__pycache__"
    cache.mkdir()
    (cache / "cached.py").write_text("# not source")
    assert load_script("build_bundle").source_files(tmp_path) == [
        package / "a.py", package / "z.py",
    ]


@pytest.mark.parametrize("location", ["parent", "clone"])
def test_bootstrap_rejects_reference_symlinks_without_git(tmp_path, monkeypatch, location):
    bootstrap = load_script("bootstrap")
    (tmp_path / "reference.json").write_text(json.dumps({"url": "unused"}))
    outside = tmp_path / "outside"
    outside.mkdir()
    references = tmp_path / ".references"
    target = references
    if location == "clone":
        references.mkdir()
        target = references / "python-sdk"
    target.symlink_to(outside, target_is_directory=True)

    def no_process(*args, **kwargs):
        pytest.fail("A reference symlink must be rejected before running git")

    monkeypatch.setattr(bootstrap, "run", no_process)
    with pytest.raises(RuntimeError, match="symlink"):
        bootstrap.ensure_reference(tmp_path)
    assert list(outside.iterdir()) == []


@pytest.mark.parametrize("name", ["", " ", "\t\n"])
def test_empty_environment_identity_is_rejected(monkeypatch, name):
    from usecase_mcp.config import Settings

    monkeypatch.setenv("MCP_SERVER_NAME", name)
    with pytest.raises(ValueError, match="must not be empty"):
        Settings.from_environment()


def test_unknown_tool_is_refused_by_real_stdio_server():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def connect():
        async with asyncio.timeout(20):
            async with stdio_client(StdioServerParameters(
                command=sys.executable, args=["-m", "usecase_mcp"],
            )) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool("synthetic_unregistered_tool", {})
                    assert result.is_error
                    assert (await session.list_tools()).tools == []

    asyncio.run(connect())
