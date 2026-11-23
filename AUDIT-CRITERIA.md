# Python MCP Starter — candidate technical criteria

Reviewed 2026-11-23. These component criteria supplement SAAF's existing nine
standards; they are not a new organizational norm or a production certification.
Named maintainer acceptance remains open (`confirmed: false`). Record exact
commit, uv.lock revision, Python/OS, command, date and outcome with each check.
Missing execution or evaluation remains **not assessed**.

| ID | Type | Criterion | Evidence |
|---|---|---|---|
| MCP-001 | [code] | The real local stdio server initializes and lists zero tools; a synthetic unregistered tool is refused. | `test_real_stdio_initialization_and_empty_tools`, `test_unknown_tool_is_refused_by_real_stdio_server`; manual `scripts/smoke_test.py --expect-empty` |
| MCP-002 | [code] | Client configurations parse, retain the actual venv executable and supplied identity, and reject absent/invalid names. The helper prints rather than installs settings. | `test_config_is_parseable_and_uses_existing_venv`, `test_generated_config_reports_use_case_identity`, `test_config_requires_valid_use_case_name` |
| MCP-003 | [code] | Reference preparation verifies origin, clean tree, pinned revision and required examples; rejects mismatches/failed clone and symlinked reference locations without overwriting an existing checkout. | `tests/test_bootstrap.py`, `test_bootstrap_rejects_reference_symlinks_without_git`; actual bootstrap is a separate network check |
| MCP-004 | [code] | Bundling selects regular Python files only; local data, caches and symlinks are excluded or rejected. Missing/empty source is rejected before installation. | `test_bundle_allowlist_excludes_local_data`, `test_bundle_rejects_symlinked_source_before_install`, `test_bundle_rejects_missing_or_empty_source`, `test_bundle_sources_remain_sorted_and_exclude_non_sources` |
| MCP-005 | [code] | Blank environment names fail before creating a server. | `test_empty_environment_identity_is_rejected` |
| MCP-006 | [code] | A clean job installs the committed dependency lock, then runs the local tests, lint and real stdio smoke test with no credential input. Manifest validation uses the pinned existing Living Map checker. | `.github/workflows/ci.yml`; job outcome and uploaded JUnit tied to the commit |
| MCP-007 | [llm] | A coding agent follows the intake guide, preserves scopes and obtains meaningful approval for consequential integrations. | Not assessed: prose scenarios are not agent evaluations; needs an approved evaluation set and budget |

The starter deliberately contains no business tools, model calls or customer
records. An empty tool list proves the current registration state, not the safety
of future tools. Protocol success is separate from client GUI installation;
source-selection tests are separate from a full platform-specific bundle build.
A locked dependency set aids reproducibility but is not a vulnerability assessment.
See [verification](docs/verification.md) for scope and remaining checks.
