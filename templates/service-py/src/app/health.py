from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

_STARTED_AT = time.monotonic()


@dataclass(frozen=True, slots=True)
class Health:
    status: str
    uptime_seconds: int


def health(now: Callable[[], float] = time.monotonic, started_at: float = _STARTED_AT) -> Health:
    return Health(status="ok", uptime_seconds=int(now() - started_at))
