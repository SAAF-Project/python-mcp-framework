import asyncio
import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_real_stdio_initialization_and_empty_tools():
    smoke = load_script("smoke_test")
    assert asyncio.run(smoke.check(sys.executable, ["-m", "workshop_mcp"], True)) == []


def test_config_is_parseable_and_uses_existing_venv():
    for client in ("codex", "claude"):
        output = subprocess.check_output(
            [sys.executable, str(ROOT / "scripts/client_config.py"), client], text=True
        )
        if client == "codex":
            config = tomllib.loads(output)["mcp_servers"]["workshop-mcp"]
        else:
            config = json.loads(output)["mcpServers"]["workshop-mcp"]
        assert Path(config["command"]).is_file()
        assert ".venv" in Path(config["command"]).parts
        assert config["args"] == ["-m", "workshop_mcp"]


def test_bundle_allowlist_excludes_local_data(tmp_path):
    bundle = load_script("build_bundle")
    package = tmp_path / "src/workshop_mcp"
    package.mkdir(parents=True)
    (package / "server.py").write_text("# server")
    (package / ".env").write_text("SECRET=do-not-ship")
    (tmp_path / ".env").write_text("SECRET=do-not-ship")
    (package / "notes.json").write_text("{}")
    assert bundle.source_files(tmp_path) == [package / "server.py"]
