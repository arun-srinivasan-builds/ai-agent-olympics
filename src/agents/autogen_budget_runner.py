from __future__ import annotations

import time

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.core.budget_eval import evaluate_budget_answer
from src.core.evals import run_deterministic_evaluation
from src.core.models import ExecutionResult, ResearchBehavior, ToolEvidence, TraceEvent
from src.core.settings import Settings
from src.tools.research_tool import format_evidence, unique_domains


SYSTEM_INSTRUCTIONS = """
You are the Microsoft AutoGen competitor in the AI Agent Olympics Budget Marathon.

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


def _usage_from_messages(messages: list) -> tuple[int, int, int]:
    requests = 0
    input_tokens = 0
    output_tokens = 0

    for message in messages:
        usage = getattr(message, "models_usage", None)
        if usage is None:
            continue
        requests += 1
        input_tokens += int(getattr(usage, "prompt_tokens", 0) or 0)
        output_tokens += int(getattr(usage, "completion_tokens", 0) or 0)

    return requests, input_tokens, output_tokens


def _prompt(task: str, evidence: list[ToolEvidence]) -> str:
    return (
        f"{task}\n\n"
        "FROZEN CHANGE-GOVERNANCE EVIDENCE\n"
        "Use only this packet.\n\n"
        f"{format_evidence(evidence)}"
    )


async def run_autogen_budget_marathon(
    prompt: str,
    settings: Settings,
    evidence: list[ToolEvidence],
) -> ExecutionResult:
    started = time.perf_counter()
    model_client = None
    trace = [
        TraceEvent("Quality contract", "passed", "Six answer-quality requirements fixed before execution."),
        TraceEvent("Evidence", "passed", f"{len(evidence)} identical evidence items supplied."),
        TraceEvent("Agent", "running", "AutoGen Budget Marathon runner started."),
    ]

    try:
        model_client = OpenAIChatCompletionClient(
            model=settings.model,
            api_key=settings.openai_api_key,
        )

        agent = AssistantAgent(
            name="budget_marathon_autogen",
            model_client=model_client,
            tools=[],
            system_message=SYSTEM_INSTRUCTIONS,
            reflect_on_tool_use=False,
        )

        result = await agent.run(task=_prompt(prompt, evidence))
        messages = list(result.messages)
        final_message = messages[-1] if messages else None
        answer = str(getattr(final_message, "content", "") or "")

        llm_requests, input_tokens, output_tokens = _usage_from_messages(messages)
        total_tokens = input_tokens + output_tokens

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
            framework_id="autogen",
            framework_name="Microsoft AutoGen",
            event_id="budget_marathon",
            model=settings.model,
            mode="controlled_budget",
            status="success",
            answer=answer,
            duration_seconds=round(time.perf_counter() - started, 3),
            llm_requests=llm_requests,
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
            framework_id="autogen",
            framework_name="Microsoft AutoGen",
            event_id="budget_marathon",
            model=settings.model,
            mode="controlled_budget",
            status="failed",
            duration_seconds=round(time.perf_counter() - started, 3),
            trace=trace,
            evidence=list(evidence),
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        if model_client is not None:
            await model_client.close()
