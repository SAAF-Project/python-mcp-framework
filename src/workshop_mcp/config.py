"""Non-secret settings; add integration-specific settings after intake."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    name: str = "Workshop MCP"

    @classmethod
    def from_environment(cls) -> "Settings":
        name = os.environ.get("WORKSHOP_MCP_NAME", "Workshop MCP").strip()
        if not name:
            raise ValueError("WORKSHOP_MCP_NAME must not be empty")
        return cls(name=name)
