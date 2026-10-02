from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tools.research_tool import AutonomousResearchTool


tool = AutonomousResearchTool(api_key="TEST_ONLY")

a = tool._register_result("A", "https://example.com/a", "one")
b = tool._register_result("B", "https://example.com/b", "two")
a_repeat = tool._register_result("A newer title", "https://example.com/a", "repeat")
c = tool._register_result("C", "https://example.com/c", "three")

assert a.position == 1
assert b.position == 2
assert a_repeat.position == 1
assert c.position == 3
assert len(tool.evidence) == 3

print("EVIDENCE REGISTRY TEST: PASS")
print("Stable citation IDs preserved across repeated search results.")
print("Duplicate URLs do not create duplicate evidence records.")
