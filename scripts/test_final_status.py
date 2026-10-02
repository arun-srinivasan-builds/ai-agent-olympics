from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from config.events import EVENTS
lookup={e["id"]:e for e in EVENTS}
for event_id in ["research_sprint","broken_tool_relay","misinformation_challenge","prompt_injection_hurdle","budget_marathon"]:
    assert lookup[event_id]["status"] == "Complete"
print("FINAL EVENT STATUS TEST: PASS")
print("All 5 Olympic events = Complete")
