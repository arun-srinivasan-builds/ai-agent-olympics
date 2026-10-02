from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from src.agents.autogen_runner import run_autogen_research
from src.agents.autogen_broken_tool_runner import run_autogen_broken_tool_relay
from src.agents.autogen_misinformation_runner import run_autogen_misinformation
from src.agents.autogen_prompt_injection_runner import run_autogen_prompt_injection
from src.agents.autogen_budget_runner import run_autogen_budget_marathon
from src.agents.openai_runner import run_openai_research
from src.agents.openai_broken_tool_runner import run_openai_broken_tool_relay
from src.agents.openai_misinformation_runner import run_openai_misinformation
from src.agents.openai_prompt_injection_runner import run_openai_prompt_injection
from src.agents.openai_budget_runner import run_openai_budget_marathon
from src.core.guardrails import validate_research_prompt
from src.core.models import ComparisonResult
from src.core.semantic_eval import run_semantic_evaluation
from src.core.settings import Settings
from src.tools.research_tool import prefetch_shared_evidence
from src.tools.misinformation_fixture import get_misinformation_evidence
from src.tools.prompt_injection_fixture import get_prompt_injection_evidence
from src.tools.budget_fixture import get_budget_evidence


async def run_research_sprint(
    prompt: str,
    settings: Settings,
    mode: str = "autonomous",
    semantic_eval_enabled: bool = True,
) -> ComparisonResult:
    clean_prompt = validate_research_prompt(prompt)

    if mode not in {"autonomous", "controlled"}:
        raise ValueError("Research mode must be 'autonomous' or 'controlled'.")

    shared_evidence = []
    shared_external_search_calls = 0

    if mode == "controlled":
        (
            shared_evidence,
            shared_external_search_calls,
        ) = await prefetch_shared_evidence(
            question=clean_prompt,
            api_key=settings.serper_api_key,
        )

    openai_result = await run_openai_research(
        clean_prompt,
        settings,
        mode,
        shared_evidence,
    )
    autogen_result = await run_autogen_research(
        clean_prompt,
        settings,
        mode,
        shared_evidence,
    )

    if semantic_eval_enabled:
        if openai_result.status == "success":
            openai_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=openai_result.answer,
                evidence=openai_result.evidence,
                settings=settings,
            )
        if autogen_result.status == "success":
            autogen_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=autogen_result.answer,
                evidence=autogen_result.evidence,
                settings=settings,
            )

    comparison = ComparisonResult(
        event_id="research_sprint",
        prompt=clean_prompt,
        model=settings.model,
        mode=mode,
        openai_agents=openai_result,
        autogen=autogen_result,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        shared_external_search_calls=shared_external_search_calls,
        shared_evidence=shared_evidence,
        semantic_eval_enabled=semantic_eval_enabled,
    )

    _persist_comparison(comparison)
    return comparison



async def run_broken_tool_relay(
    prompt: str,
    settings: Settings,
    shared_search_query: str,
    semantic_eval_enabled: bool = True,
) -> ComparisonResult:
    clean_prompt = validate_research_prompt(prompt)

    shared_evidence, shared_external_search_calls = await prefetch_shared_evidence(
        question=shared_search_query,
        api_key=settings.serper_api_key,
    )

    openai_result = await run_openai_broken_tool_relay(
        clean_prompt,
        settings,
        shared_evidence,
    )
    autogen_result = await run_autogen_broken_tool_relay(
        clean_prompt,
        settings,
        shared_evidence,
    )

    if semantic_eval_enabled:
        if openai_result.status == "success" and openai_result.recovery.recovered:
            openai_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=openai_result.answer,
                evidence=openai_result.evidence,
                settings=settings,
            )
        if autogen_result.status == "success" and autogen_result.recovery.recovered:
            autogen_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=autogen_result.answer,
                evidence=autogen_result.evidence,
                settings=settings,
            )

    comparison = ComparisonResult(
        event_id="broken_tool_relay",
        prompt=clean_prompt,
        model=settings.model,
        mode="fault_injection",
        openai_agents=openai_result,
        autogen=autogen_result,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        shared_external_search_calls=shared_external_search_calls,
        shared_evidence=shared_evidence,
        semantic_eval_enabled=semantic_eval_enabled,
    )

    _persist_comparison(comparison)
    return comparison



async def run_misinformation_challenge(
    prompt: str,
    settings: Settings,
    semantic_eval_enabled: bool = True,
) -> ComparisonResult:
    clean_prompt = validate_research_prompt(prompt)
    evidence = get_misinformation_evidence()

    openai_result = await run_openai_misinformation(
        clean_prompt,
        settings,
        evidence,
    )
    autogen_result = await run_autogen_misinformation(
        clean_prompt,
        settings,
        evidence,
    )

    if semantic_eval_enabled:
        if openai_result.status == "success":
            openai_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=openai_result.answer,
                evidence=openai_result.evidence,
                settings=settings,
            )
        if autogen_result.status == "success":
            autogen_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=autogen_result.answer,
                evidence=autogen_result.evidence,
                settings=settings,
            )

    comparison = ComparisonResult(
        event_id="misinformation_challenge",
        prompt=clean_prompt,
        model=settings.model,
        mode="controlled_conflict",
        openai_agents=openai_result,
        autogen=autogen_result,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        shared_external_search_calls=0,
        shared_evidence=evidence,
        semantic_eval_enabled=semantic_eval_enabled,
    )

    _persist_comparison(comparison)
    return comparison



async def run_prompt_injection_hurdle(
    prompt: str,
    settings: Settings,
    semantic_eval_enabled: bool = True,
) -> ComparisonResult:
    clean_prompt = validate_research_prompt(prompt)
    evidence = get_prompt_injection_evidence()

    openai_result = await run_openai_prompt_injection(clean_prompt, settings, evidence)
    autogen_result = await run_autogen_prompt_injection(clean_prompt, settings, evidence)

    if semantic_eval_enabled:
        if openai_result.status == "success":
            openai_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt, answer=openai_result.answer, evidence=openai_result.evidence, settings=settings
            )
        if autogen_result.status == "success":
            autogen_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt, answer=autogen_result.answer, evidence=autogen_result.evidence, settings=settings
            )

    comparison = ComparisonResult(
        event_id="prompt_injection_hurdle",
        prompt=clean_prompt,
        model=settings.model,
        mode="controlled_prompt_injection",
        openai_agents=openai_result,
        autogen=autogen_result,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        shared_external_search_calls=0,
        shared_evidence=evidence,
        semantic_eval_enabled=semantic_eval_enabled,
    )
    _persist_comparison(comparison)
    return comparison



async def run_budget_marathon(
    prompt: str,
    settings: Settings,
    semantic_eval_enabled: bool = True,
) -> ComparisonResult:
    clean_prompt = validate_research_prompt(prompt)
    evidence = get_budget_evidence()

    openai_result = await run_openai_budget_marathon(
        clean_prompt,
        settings,
        evidence,
    )
    autogen_result = await run_autogen_budget_marathon(
        clean_prompt,
        settings,
        evidence,
    )

    if semantic_eval_enabled:
        if openai_result.status == "success":
            openai_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=openai_result.answer,
                evidence=openai_result.evidence,
                settings=settings,
            )
        if autogen_result.status == "success":
            autogen_result.semantic_eval = await run_semantic_evaluation(
                question=clean_prompt,
                answer=autogen_result.answer,
                evidence=autogen_result.evidence,
                settings=settings,
            )

    comparison = ComparisonResult(
        event_id="budget_marathon",
        prompt=clean_prompt,
        model=settings.model,
        mode="controlled_budget",
        openai_agents=openai_result,
        autogen=autogen_result,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        shared_external_search_calls=0,
        shared_evidence=evidence,
        semantic_eval_enabled=semantic_eval_enabled,
    )

    _persist_comparison(comparison)
    return comparison


def _persist_comparison(comparison: ComparisonResult) -> None:
    output_dir = Path("outputs") / comparison.event_id
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = output_dir / f"{comparison.mode}_{timestamp}.json"
    path.write_text(
        json.dumps(comparison.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
