"""Print concrete client configuration; never change the user's settings."""

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("client", choices=["codex", "claude"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    python = root / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if not python.exists():
        parser.error("Project environment missing. Run uv sync --locked first.")
    # Use the venv path itself, not its symlink target (which would lose installed packages).
    command = str(python)
    if args.client == "codex":
        print('[mcp_servers.workshop-mcp]')
        print(f"command = {json.dumps(command)}")
        print('args = ["-m", "workshop_mcp"]')
    else:
        print(json.dumps({"mcpServers": {"workshop-mcp": {
            "command": command, "args": ["-m", "workshop_mcp"]
        }}}, indent=2))


if __name__ == "__main__":
    main()
