from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tools.budget_fixture import GROUND_TRUTH, get_budget_evidence

evidence = get_budget_evidence()

assert len(evidence) == 4
assert "NO-GO" in evidence[0].snippet
assert "payment timeout" in evidence[1].snippet.lower()
assert "2.0%" in evidence[2].snippet
assert "14:00 UTC" in evidence[3].snippet
assert GROUND_TRUTH.max_words == 180

print("BUDGET FIXTURE TEST: PASS")
print("Four deterministic change-governance evidence items validated.")
