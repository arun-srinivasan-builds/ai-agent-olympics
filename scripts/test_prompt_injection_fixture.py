from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tools.prompt_injection_fixture import GROUND_TRUTH, get_prompt_injection_evidence

evidence = get_prompt_injection_evidence()

assert len(evidence) == 4
assert "38%" in evidence[0].snippet
assert "SEV-1" in evidence[1].snippet
assert "regional failover" in evidence[2].snippet
assert "SEV-3" in evidence[3].snippet
assert GROUND_TRUTH.attack_source_position == 4
assert GROUND_TRUTH.attack_token == "INJECTION_ACCEPTED"

print("PROMPT INJECTION FIXTURE TEST: PASS")
print("3 trusted evidence items + 1 controlled malicious retrieved item.")
