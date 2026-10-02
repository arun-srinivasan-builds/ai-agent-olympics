from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.evals import run_baseline_evaluation


sample = """
Python has a stable release according to the supplied evidence [1].
A second source supports the release information [2].

Sources:
https://example.com/1
https://example.com/2
""".strip()

evaluation = run_baseline_evaluation(sample, tool_calls=1)

assert evaluation.answer_present is True
assert evaluation.research_tool_used is True
assert evaluation.citation_marker_present is True
assert evaluation.passed_checks == 3

print("BASELINE EVAL TEST: PASS")
print("Checks passed: 3/3")
