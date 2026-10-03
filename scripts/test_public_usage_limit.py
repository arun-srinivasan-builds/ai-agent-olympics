from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.usage_guard import (
    COOLDOWN_SECONDS,
    GLOBAL_RUN_LIMIT_PER_HOUR,
    SESSION_RUN_LIMIT,
    _reset_global_usage_for_tests,
    check_and_reserve_public_run,
    get_public_run_usage,
)


_reset_global_usage_for_tests()

session = {}
decision = check_and_reserve_public_run(session, units=1, now=1000)
assert decision.allowed
assert decision.session_used == 1
assert get_public_run_usage(session) == (1, SESSION_RUN_LIMIT - 1)

decision = check_and_reserve_public_run(session, units=1, now=1001)
assert not decision.allowed
assert decision.retry_after_seconds > 0
assert get_public_run_usage(session)[0] == 1

now = 1000 + COOLDOWN_SECONDS + 1
for expected_used in range(2, SESSION_RUN_LIMIT + 1):
    decision = check_and_reserve_public_run(session, units=1, now=now)
    assert decision.allowed
    assert decision.session_used == expected_used
    now += COOLDOWN_SECONDS + 1

decision = check_and_reserve_public_run(session, units=1, now=now)
assert not decision.allowed
assert "browser session" in decision.message

_reset_global_usage_for_tests()
batch_session = {}
decision = check_and_reserve_public_run(batch_session, units=5, now=5000)
assert decision.allowed
assert decision.session_used == 5
assert get_public_run_usage(batch_session) == (5, 0)

_reset_global_usage_for_tests()
base = 10000
for i in range(GLOBAL_RUN_LIMIT_PER_HOUR):
    separate_session = {}
    decision = check_and_reserve_public_run(
        separate_session,
        units=1,
        now=base + i,
    )
    assert decision.allowed

overflow_session = {}
decision = check_and_reserve_public_run(
    overflow_session,
    units=1,
    now=base + GLOBAL_RUN_LIMIT_PER_HOUR,
)
assert not decision.allowed
assert "shared hourly" in decision.message

decision = check_and_reserve_public_run(
    overflow_session,
    units=1,
    now=base + 3601 + GLOBAL_RUN_LIMIT_PER_HOUR,
)
assert decision.allowed

app = (ROOT / "app.py").read_text(encoding="utf-8")
assert "check_and_reserve_public_run" in app
assert "units=5" in app
assert "units=1" in app
assert "Public demo limits apply" in app

print("PUBLIC USAGE LIMIT TEST: PASS")
print(
    "Public live API execution is protected by a 5-event browser-session cap, "
    "15-second cooldown, and 40-event rolling hourly process-wide cap."
)
