from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.events import EVENTS

lookup = {event["id"]: event for event in EVENTS}

assert lookup["research_sprint"]["status"] == "Complete"
assert lookup["broken_tool_relay"]["status"] == "Live"

print("EVENT STATUS TEST: PASS")
print("Research Sprint = Complete")
print("Broken Tool Relay = Live")
