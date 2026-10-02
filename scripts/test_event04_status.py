from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.events import EVENTS

lookup = {event["id"]: event for event in EVENTS}

assert lookup["research_sprint"]["status"] == "Complete"
assert lookup["broken_tool_relay"]["status"] == "Complete"
assert lookup["misinformation_challenge"]["status"] == "Complete"
assert lookup["prompt_injection_hurdle"]["status"] == "Live"
assert lookup["budget_marathon"]["status"] == "Next"

print("EVENT 04 STATUS TEST: PASS")
print("Events 01-03 = Complete")
print("Event 04 = Live")
print("Event 05 = Next")
