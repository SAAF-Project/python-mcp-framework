# Install locally

First run `uv sync --locked` and the smoke test. The client starts the server;
you do not need a separate terminal server or a public URL. Keep the project in
its permanent location: moving it invalidates its environment and stored paths.

## Codex

Run `uv run python scripts/client_config.py codex`. It prints an actual TOML
configuration with the absolute project Python path. Add that server section to
your existing `~/.codex/config.toml` (Windows: under your user home `.codex`).
Merge it without replacing other settings; if `workshop-mcp` already exists,
choose a distinct name or deliberately update that entry.

Alternatively register with the CLI, replacing `ABSOLUTE-VENV-PYTHON` with the
printed command path, including quotes when the path has spaces:

```sh
codex mcp add workshop-mcp -- "ABSOLUTE-VENV-PYTHON" -m workshop_mcp
codex mcp list
```

Restart/reconnect the app and inspect its MCP tools. Remove with
`codex mcp remove workshop-mcp` or remove only that TOML section.

## Claude Code

Run `uv run python scripts/client_config.py claude`. Merge the printed JSON into
the project `.mcp.json` without losing existing servers, or register via:

```sh
claude mcp add --transport stdio --scope local workshop-mcp -- "ABSOLUTE-VENV-PYTHON" -m workshop_mcp
claude mcp list
```

`--scope local` keeps this registration local to you for this project. In Claude
Code, use `/mcp` to inspect the connection. Accept any client trust prompt yourself.
Remove it with `claude mcp remove workshop-mcp` for CLI registration, or remove
the entry from `.mcp.json` for file registration. Reconnect/restart afterwards.

## Credentials and checks

The generated starter configurations contain no credentials. The guide must adapt
the chosen client's environment/private storage setup for the finished integration.
Do not paste tokens into command examples. A GUI app may not inherit variables
from your terminal. Verify availability without printing the value.

The initial server has zero tools; some clients flag that as an empty server.
After implementation, verify the expected tools appear and try one bounded read.
Record the actual result. Registration alone is not an end-to-end test.

If startup fails, rerun `uv sync --locked`, regenerate the path and run
`uv run python scripts/smoke_test.py`. Check that the interpreter is inside
`.venv`, dependencies are installed, logs go to stderr, and credentials are
available to the client process. Stop a client-managed server by disabling or
removing it and reconnecting the client. Stop a manually run process with Ctrl+C.

For Claude Desktop's optional installable file, see [Bundles](bundles.md).

Sources: [Codex](https://developers.openai.com/codex/mcp),
[Claude Code](https://code.claude.com/docs/en/mcp).
