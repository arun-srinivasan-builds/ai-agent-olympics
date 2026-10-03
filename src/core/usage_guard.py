from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from threading import Lock
import time
from typing import MutableMapping


SESSION_RUN_LIMIT = 5
GLOBAL_RUN_LIMIT_PER_HOUR = 40
COOLDOWN_SECONDS = 15
WINDOW_SECONDS = 60 * 60

_SESSION_COUNT_KEY = "_public_live_run_count"
_SESSION_LAST_RUN_KEY = "_public_live_last_run_at"

_GLOBAL_RUN_TIMESTAMPS: deque[float] = deque()
_GLOBAL_LOCK = Lock()


@dataclass(frozen=True)
class UsageDecision:
    allowed: bool
    message: str = ""
    session_used: int = 0
    session_limit: int = SESSION_RUN_LIMIT
    global_used: int = 0
    global_limit: int = GLOBAL_RUN_LIMIT_PER_HOUR
    retry_after_seconds: int = 0


def _prune_global(now: float) -> None:
    cutoff = now - WINDOW_SECONDS
    while _GLOBAL_RUN_TIMESTAMPS and _GLOBAL_RUN_TIMESTAMPS[0] <= cutoff:
        _GLOBAL_RUN_TIMESTAMPS.popleft()


def check_and_reserve_public_run(
    session_state: MutableMapping,
    *,
    units: int = 1,
    now: float | None = None,
) -> UsageDecision:
    if units < 1:
        raise ValueError("units must be at least 1")

    current_time = time.time() if now is None else float(now)
    session_used = int(session_state.get(_SESSION_COUNT_KEY, 0) or 0)
    last_run = session_state.get(_SESSION_LAST_RUN_KEY)

    if session_used + units > SESSION_RUN_LIMIT:
        return UsageDecision(
            allowed=False,
            message=(
                "Public demo limit reached for this browser session. "
                f"Up to {SESSION_RUN_LIMIT} live Olympic event executions are available per session."
            ),
            session_used=session_used,
        )

    if last_run is not None:
        elapsed = max(0.0, current_time - float(last_run))
        if elapsed < COOLDOWN_SECONDS:
            retry_after = max(1, int(COOLDOWN_SECONDS - elapsed + 0.999))
            return UsageDecision(
                allowed=False,
                message=(
                    "Please wait a few seconds before starting another live experiment. "
                    f"Try again in about {retry_after} seconds."
                ),
                session_used=session_used,
                retry_after_seconds=retry_after,
            )

    with _GLOBAL_LOCK:
        _prune_global(current_time)
        global_used = len(_GLOBAL_RUN_TIMESTAMPS)

        if global_used + units > GLOBAL_RUN_LIMIT_PER_HOUR:
            return UsageDecision(
                allowed=False,
                message=(
                    "The public demo has reached its shared hourly live-run capacity. "
                    "Please try again later."
                ),
                session_used=session_used,
                global_used=global_used,
            )

        for _ in range(units):
            _GLOBAL_RUN_TIMESTAMPS.append(current_time)

        global_used = len(_GLOBAL_RUN_TIMESTAMPS)

    session_state[_SESSION_COUNT_KEY] = session_used + units
    session_state[_SESSION_LAST_RUN_KEY] = current_time

    return UsageDecision(
        allowed=True,
        session_used=session_used + units,
        global_used=global_used,
    )


def get_public_run_usage(session_state: MutableMapping) -> tuple[int, int]:
    used = int(session_state.get(_SESSION_COUNT_KEY, 0) or 0)
    return used, max(0, SESSION_RUN_LIMIT - used)


def _reset_global_usage_for_tests() -> None:
    with _GLOBAL_LOCK:
        _GLOBAL_RUN_TIMESTAMPS.clear()
