from __future__ import annotations

from dataclasses import dataclass

from src.core.models import ToolEvidence


@dataclass(frozen=True)
class BudgetGroundTruth:
    decision: str
    risk_phrase: str
    rollback_phrase: str
    next_action_phrase: str
    deadline_phrase: str
    max_words: int


GROUND_TRUTH = BudgetGroundTruth(
    decision="NO-GO",
    risk_phrase="payment timeout",
    rollback_phrase="rollback",
    next_action_phrase="rerun the payment regression suite",
    deadline_phrase="14:00 UTC",
    max_words=180,
)


def get_budget_evidence() -> list[ToolEvidence]:
    """
    Deterministic enterprise change-governance evidence.

    The task is intentionally answerable in one model call without tools.
    """
    return [
        ToolEvidence(
            position=1,
            title="Release Readiness Gate — Checkout API v8.4",
            url="https://evidence.local/change/readiness-gate",
            snippet=(
                "Production release requires all P1 regression tests to pass. "
                "Current status: 47 of 48 tests passed. The remaining failing P1 test "
                "is Payment Timeout Recovery. A failed P1 gate means NO-GO."
            ),
        ),
        ToolEvidence(
            position=2,
            title="Risk Register — Checkout API v8.4",
            url="https://evidence.local/change/risk-register",
            snippet=(
                "Primary release risk: payment timeout recovery can leave a checkout "
                "session pending and may cause duplicate customer retries. "
                "Risk rating: High until the failing P1 regression is cleared."
            ),
        ),
        ToolEvidence(
            position=3,
            title="Rollback Standard — Checkout Platform",
            url="https://evidence.local/change/rollback-standard",
            snippet=(
                "If production error rate exceeds 2.0% for five consecutive minutes "
                "during rollout, immediately rollback to Checkout API v8.3."
            ),
        ),
        ToolEvidence(
            position=4,
            title="Change Manager Action Record",
            url="https://evidence.local/change/action-record",
            snippet=(
                "Required next action: fix the Payment Timeout Recovery defect and rerun "
                "the payment regression suite. Updated evidence must be attached to the "
                "change record by 14:00 UTC before the release gate can be reconsidered."
            ),
        ),
    ]
