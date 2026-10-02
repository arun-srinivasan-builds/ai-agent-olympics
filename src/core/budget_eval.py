from __future__ import annotations

import re

from src.core.models import BudgetMetrics
from src.tools.budget_fixture import GROUND_TRUTH


# Standard token pricing as verified for gpt-4.1-mini on 2026-10-02.
# Keep pricing model-specific so changing AI_MODEL does not silently create
# a misleading cost estimate.
MODEL_PRICING_USD_PER_1M = {
    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60,
    },
    "gpt-4.1-mini-2025-04-14": {
        "input": 0.40,
        "output": 1.60,
    },
}


def substantive_text(answer: str) -> str:
    """
    Exclude the Sources section from the word-budget calculation.
    """
    text = answer or ""
    parts = re.split(r"(?im)^\s*(?:#{1,6}\s*)?sources\s*:?\s*$", text, maxsplit=1)
    return parts[0].strip()


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text or ""))


def estimate_model_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> tuple[float, bool]:
    price = MODEL_PRICING_USD_PER_1M.get(model)
    if not price:
        return 0.0, False

    cost = (
        (input_tokens / 1_000_000) * price["input"]
        + (output_tokens / 1_000_000) * price["output"]
    )
    return round(cost, 8), True


def evaluate_budget_answer(
    answer: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> BudgetMetrics:
    text = (answer or "").lower()
    core = substantive_text(answer)
    words = count_words(core)

    correct_decision = (
        "no-go" in text
        or "no go" in text
        or "do not proceed" in text
        or "release should not proceed" in text
    )

    primary_risk_present = (
        "payment timeout" in text
        and (
            "duplicate" in text
            or "pending" in text
            or "risk" in text
        )
    )

    rollback_condition_present = (
        "rollback" in text
        and "2" in text
        and "five" in text
        and "minute" in text
        and ("v8.3" in text or "8.3" in text)
    )

    next_action_present = (
        "rerun" in text
        and "payment regression" in text
        and ("fix" in text or "defect" in text)
    )

    deadline_present = (
        "14:00 utc" in text
        or "14.00 utc" in text
        or "1400 utc" in text
    )

    within_word_budget = words <= GROUND_TRUTH.max_words

    cost, pricing_available = estimate_model_cost_usd(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )

    return BudgetMetrics(
        correct_decision=correct_decision,
        primary_risk_present=primary_risk_present,
        rollback_condition_present=rollback_condition_present,
        next_action_present=next_action_present,
        deadline_present=deadline_present,
        within_word_budget=within_word_budget,
        substantive_word_count=words,
        estimated_model_cost_usd=cost,
        pricing_available=pricing_available,
    )
