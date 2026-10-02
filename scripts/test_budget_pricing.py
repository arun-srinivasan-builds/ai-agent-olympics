from pathlib import Path
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.budget_eval import estimate_model_cost_usd

cost, available = estimate_model_cost_usd(
    "gpt-4.1-mini",
    input_tokens=1_000_000,
    output_tokens=1_000_000,
)

assert available is True
assert math.isclose(cost, 2.0, rel_tol=0, abs_tol=1e-9)

cost, available = estimate_model_cost_usd(
    "unknown-model",
    input_tokens=1_000_000,
    output_tokens=1_000_000,
)

assert available is False
assert cost == 0.0

print("BUDGET PRICING TEST: PASS")
print("gpt-4.1-mini pricing calculation = $0.40 input + $1.60 output per 1M.")
print("Unknown models correctly report pricing unavailable.")
