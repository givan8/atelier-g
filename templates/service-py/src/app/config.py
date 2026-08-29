"""Configuration, read from the environment and validated once at startup.

House rule 6: fail loudly. A missing or malformed variable stops the process here
rather than producing a confusing failure somewhere later.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when the environment does not describe a runnable service."""


def required(name: str, env: dict[str, str] | None = None) -> str:
    source = os.environ if env is None else env
    value = source.get(name, "")
    if not value:
        raise ConfigError(f"missing required environment variable: {name}")
    return value


def parse_port(raw: str) -> int:
    try:
        port = int(raw)
    except ValueError:
        raise ConfigError(f"PORT must be an integer, got {raw!r}") from None
    if not 1 <= port <= 65535:
        raise ConfigError(f"PORT must be between 1 and 65535, got {port}")
    return port


@dataclass(frozen=True, slots=True)
class Config:
    port: int
    log_level: str

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> Config:
        source = dict(os.environ) if env is None else env
        return cls(
            port=parse_port(source.get("PORT", "8080")),
            log_level=source.get("LOG_LEVEL", "info"),
        )
