from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.budget_eval import evaluate_budget_answer


good = """
Decision: NO-GO [1].

Primary risk: the Payment Timeout Recovery defect can leave sessions pending and
cause duplicate customer retries [2].

Rollback condition: if production error rate exceeds 2.0% for five consecutive
minutes during rollout, rollback to Checkout API v8.3 [3].

Next action: fix the defect and rerun the payment regression suite. Updated
evidence is due by 14:00 UTC [4].

Sources:
[1] https://evidence.local/change/readiness-gate
[2] https://evidence.local/change/risk-register
[3] https://evidence.local/change/rollback-standard
[4] https://evidence.local/change/action-record
"""

result = evaluate_budget_answer(
    answer=good,
    model="gpt-4.1-mini",
    input_tokens=1000,
    output_tokens=200,
)

assert result.correct_decision
assert result.primary_risk_present
assert result.rollback_condition_present
assert result.next_action_present
assert result.deadline_present
assert result.within_word_budget
assert result.quality_gate_passed
assert result.pricing_available

bad = """
Decision: GO.
The release looks mostly ready.
"""

result = evaluate_budget_answer(
    answer=bad,
    model="gpt-4.1-mini",
    input_tokens=100,
    output_tokens=20,
)

assert result.quality_gate_passed is False

print("BUDGET EVAL TEST: PASS")
print("Complete concise answer passes 6/6.")
print("Cheap but incomplete answer fails the quality gate.")
