# Verification record

## SAAF maintenance check — 2026-11-23

macOS arm64, CPython 3.12.13, uv 0.11.28; the existing `uv.lock` and
SDK 2.2.0 reference pin are unchanged. A fresh official reference clone verified
commit `9972c21aa42054fb1450c5fc614761ed11847ec6`; the four listed examples were
read. `uv sync --locked` installed successfully.

- 25 tests pass: the 12 existing tests plus 13 boundary/protocol cases.
- Real local stdio initialize/tools-list succeeds with zero tools; a synthetic
  unregistered tool returns an error without registering any tool.
- Bundle source selection rejects symlinked source roots, nested directories and
  files before an installer runs. Missing/empty source is rejected. Non-Python
  local data and caches remain outside the source selection.
- Bootstrap rejects a symlink at `.references` or its clone path before Git runs.
- Ruff passes. No live connector, model provider, graphical installation or full
  bundle rebuild was performed in this maintenance round.
- Proposed PR CI runs the same suite and smoke checks on Linux 3.11/3.12 and
  Windows 3.12 and validates the manifest with a pinned existing Living Map
  checker. Check the exact PR commit's job outcomes; the workflow file alone is
  not proof that these platform checks ran.

The source-selection checks assume a trusted, quiescent checkout. They do not
scan Python for hardcoded secrets or defend against concurrent replacement.
No new tool or external access was added. Named ownership remains unaccepted.
The uv runtime/test lock is preserved; the separately pinned Hatchling build
backend can still resolve its own transitive build dependencies during sync.

## Historical evidence from the original contributors

The records below are retained as earlier reported checks, not re-run claims.

Checked on 2026-09-12 on macOS arm64, CPython 3.14.5.

## Current maintenance checks

After neutralizing the starter naming and adding use-case configuration:

- `uv sync --locked` installed the renamed project successfully.
- `uv run pytest`: 12 tests passed, including invalid/missing names and a real
  stdio connection using generated configuration that reports `invoice-search`.
- `uv run python scripts/smoke_test.py`: connected; zero tools as expected.
- `uv run ruff check .`: passed.
- Existing pinned SDK clone verified; the four listed examples were read.
- Client GUI installation and bundle rebuild were not repeated for this change.

## Earlier baseline checks (before the package rename)

- `uv sync --locked`: installs the project and locked MCP SDK 2.2.0.
- `pytest -q`: 10 tests passed, including a real subprocess MCP initialize and
  tools/list round trip with zero tools.
- `ruff check .`: no findings.
- Bootstrap: actual first-time GitHub clone from the pinned tag in a fresh folder,
  plus verification/reuse of the existing clean reference clone. Both resolve to
  `9972c21aa42054fb1450c5fc614761ed11847ec6`.
- Bootstrap failure behavior: automated tests for missing Git/uv, clone failure,
  unexpected origin/revision and local reference changes.
- Clean installation: fresh source copy in a path containing spaces, new `.venv`,
  locked sync, then a successful real stdio smoke test.
- Codex TOML and Claude JSON output parse correctly and point to the existing
  project virtual environment, preserving spaces in paths.
- Bundle: built with locked, hash-verified dependency wheels for macOS arm64 /
  Python 3.14. Archive inspected for excluded local-data folders/files.
- Both the editable manifest and built manifest pass the official
  `@anthropic-ai/mcpb validate` command.
- Extracted bundle: real initialize and empty tools/list succeeded using a
  system Python with `-I`, outside the project's virtual environment.

## Guidance review

Reviewed the three scenarios in scenarios.md against AGENTS.md: public read API,
authenticated API with missing access, and database writes/deletions. The workflow
requires reference preparation, bounded intake, access verification, explicit
write-scope agreement, and separate confirmation for destructive execution. It
explicitly distinguishes mocks from verified live access and requires a handoff.
This was an instruction walkthrough, not an automated coding-agent evaluation.

## Not verified here

- Windows execution, other CPU architectures, or Python 3.11–3.13.
- Graphical installation in Codex, Claude Code, or Claude Desktop. Configuration
  and bundle checks do not prove an installed client accepts or runs them.
- External API, database, scraping or OAuth behavior: no such implementation is
  present by design. Each user's integration needs its own tests.
- Write enforcement in a future integration: the starter exposes no write tools;
  the guide specifies the controls the implementing agent must add and test.

Git was not initialized and nothing was published. Before relying on an integration, run one
full user exercise in your intended app and on the users' OS.
