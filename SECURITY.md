# Security policy

Use the [SAAF organization security reporting guidance](https://github.com/SAAF-Project/SAAF-Project/security/policy).
Do not put credentials, private endpoints, customer records or exploit payloads
containing real data in public issues. A named repository maintainer, response
SLA and supported-release policy have not yet been accepted.

The current starter exposes zero tools over local stdio. It has no model client,
network listener, authentication service or external data connector. Local code
and its dependencies run with the launching user's permissions; this is not a
sandbox. A client connection is not authorization to an external service.

Read [access and safety](docs/security.md) before adding an integration. The
manifest is a declaration, not an enforcement engine. Source, reference and
packaging files must be trusted and unchanged during checks/builds. The source
allowlist rejects symlinks and omits non-Python data, but cannot identify secrets
hardcoded in Python or defend against a concurrent filesystem attacker. Review
all source and bundle contents before sharing. Existing output archives are not
removed by a failed build; check its exit status before using an archive.

Preparation and package installation use GitHub/PyPI. Runtime protocol tests use
local subprocesses and synthetic values; they do not verify any API credentials,
provider processing region, desktop client installation or future write tool.
