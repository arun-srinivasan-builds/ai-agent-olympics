from __future__ import annotations

import time

from agents import Agent, RunConfig, Runner

from src.core.budget_eval import evaluate_budget_answer
from src.core.evals import run_deterministic_evaluation
from src.core.models import ExecutionResult, ResearchBehavior, ToolEvidence, TraceEvent
from src.core.settings import Settings
from src.tools.research_tool import format_evidence, unique_domains


SYSTEM_INSTRUCTIONS = """
You are the OpenAI Agents SDK competitor in the AI Agent Olympics Budget Marathon.

This event measures efficiency only after answer quality is satisfied.

Rules:
1. Use only the supplied evidence packet.
2. Complete every requested element: decision, primary risk, rollback condition,
   next operational action, and deadline.
3. Cite evidence using numbered markers such as [1].
4. Finish with a Sources section containing exact URLs for every citation used.
5. Keep the substantive answer at or below 180 words, excluding Sources.
6. Do not add unnecessary background, repetition, or generic advice.
7. Do not mention the benchmark or your token budget.
""".strip()


def _prompt(task: str, evidence: list[ToolEvidence]) -> str:
    return (
        f"{task}\n\n"
        "FROZEN CHANGE-GOVERNANCE EVIDENCE\n"
        "Use only this packet.\n\n"
        f"{format_evidence(evidence)}"
    )


async def run_openai_budget_marathon(
    prompt: str,
    settings: Settings,
    evidence: list[ToolEvidence],
) -> ExecutionResult:
    started = time.perf_counter()
    trace = [
        TraceEvent("Quality contract", "passed", "Six answer-quality requirements fixed before execution."),
        TraceEvent("Evidence", "passed", f"{len(evidence)} identical evidence items supplied."),
        TraceEvent("Agent", "running", "OpenAI Agents SDK Budget Marathon runner started."),
    ]

    try:
        agent = Agent(
            name="Budget Marathon - OpenAI Agents SDK",
            model=settings.model,
            instructions=SYSTEM_INSTRUCTIONS,
            tools=[],
        )

        result = await Runner.run(
            agent,
            _prompt(prompt, evidence),
            max_turns=2,
            run_config=RunConfig(
                workflow_name="AI Agent Olympics - Budget Marathon",
                trace_include_sensitive_data=False,
            ),
        )

        answer = str(result.final_output or "")
        usage = result.context_wrapper.usage

        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        total_tokens = int(getattr(usage, "total_tokens", 0) or 0)

        budget = evaluate_budget_answer(
            answer=answer,
            model=settings.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        trace.extend(
            [
                TraceEvent(
                    "Quality gate",
                    "passed" if budget.quality_gate_passed else "failed",
                    f"{budget.quality_checks_passed}/{budget.quality_checks_total} quality checks passed.",
                ),
                TraceEvent(
                    "Word budget",
                    "passed" if budget.within_word_budget else "failed",
                    f"{budget.substantive_word_count}/180 substantive words.",
                ),
                TraceEvent(
                    "Cost estimate",
                    "passed" if budget.pricing_available else "warning",
                    (
                        f"Estimated competitor model cost: ${budget.estimated_model_cost_usd:.8f}"
                        if budget.pricing_available
                        else f"No pricing configured for model {settings.model}."
                    ),
                ),
                TraceEvent("Final response", "passed", "Agent completed the task."),
            ]
        )

        deterministic = run_deterministic_evaluation(
            answer=answer,
            tool_calls=0,
            evidence=evidence,
            evidence_supplied=True,
        )

        behavior = ResearchBehavior(
            mode="budget_fixture",
            queries_generated=[],
            tool_calls=0,
            external_search_calls=0,
            source_count=len(evidence),
            unique_domains=unique_domains(evidence),
            follow_up_search=False,
        )

        return ExecutionResult(
            framework_id="openai_agents",
            framework_name="OpenAI Agents SDK",
            event_id="budget_marathon",
            model=settings.model,
            mode="controlled_budget",
            status="success",
            answer=answer,
            duration_seconds=round(time.perf_counter() - started, 3),
            llm_requests=int(getattr(usage, "requests", 0) or 0),
            tool_calls=0,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            trace=trace,
            evidence=list(evidence),
            research_behavior=behavior,
            budget=budget,
            deterministic_eval=deterministic,
        )
    except Exception as exc:
        trace.append(TraceEvent("Run", "failed", f"{type(exc).__name__}: {exc}"))
        return ExecutionResult(
            framework_id="openai_agents",
            framework_name="OpenAI Agents SDK",
            event_id="budget_marathon",
            model=settings.model,
            mode="controlled_budget",
            status="failed",
            duration_seconds=round(time.perf_counter() - started, 3),
            trace=trace,
            evidence=list(evidence),
            error=f"{type(exc).__name__}: {exc}",
        )
