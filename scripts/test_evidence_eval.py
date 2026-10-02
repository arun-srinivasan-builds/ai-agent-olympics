from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.evals import run_deterministic_evaluation
from src.core.models import ToolEvidence


evidence = [
    ToolEvidence(1, "Source 1", "https://example.com/1", "Evidence one"),
    ToolEvidence(2, "Source 2", "https://example.com/2", "Evidence two"),
    ToolEvidence(3, "Source 3", "https://example.com/3", "Evidence three"),
]

good_answer = """
Claim one is supported [1]. Claim two is supported [2].

Sources:
https://example.com/1
https://example.com/2
""".strip()

good = run_deterministic_evaluation(
    answer=good_answer,
    tool_calls=1,
    evidence=evidence,
)

assert good.answer_present is True
assert good.research_accessed is True
assert good.citation_marker_present is True
assert good.citation_numbers_valid is True
assert good.cited_urls_listed is True
assert good.passed_checks == 5

broken_source_list = """
The main claim uses evidence [3].

Sources:
https://example.com/1
https://example.com/2
""".strip()

broken = run_deterministic_evaluation(
    answer=broken_source_list,
    tool_calls=1,
    evidence=evidence,
)

assert broken.citation_numbers_valid is True
assert broken.cited_urls_listed is False

invalid_number = """
This cites evidence that was never captured [8].

Sources:
https://example.com/8
""".strip()

invalid = run_deterministic_evaluation(
    answer=invalid_number,
    tool_calls=1,
    evidence=evidence,
)

assert invalid.citation_numbers_valid is False
assert invalid.cited_urls_listed is False

print("EVIDENCE EVAL TEST: PASS")
print("Valid citation mapping detected correctly.")
print("Missing cited URL detected correctly.")
print("Out-of-range citation detected correctly.")
