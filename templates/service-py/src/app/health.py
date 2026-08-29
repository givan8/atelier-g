from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

_STARTED_AT = time.monotonic()


@dataclass(frozen=True, slots=True)
class Health:
    status: str
    uptime_seconds: int


def health(now: Callable[[], float] = time.monotonic, started_at: float = _STARTED_AT) -> Health:
    return Health(status="ok", uptime_seconds=int(now() - started_at))
