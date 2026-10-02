from __future__ import annotations

import time

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.core.evals import run_deterministic_evaluation
from src.core.models import ExecutionResult, ToolEvidence, TraceEvent
from src.core.settings import Settings
from src.tools.fault_injection_tool import FaultInjectedEvidenceTool


SYSTEM_INSTRUCTIONS = """
You are the Microsoft AutoGen competitor in the AI Agent Olympics Broken Tool Relay.

The research tool has a controlled transient-failure scenario.

Rules:
1. You MUST call resilient_research before answering.
2. If the tool returns SIMULATED_TRANSIENT_ERROR / HTTP 503, recognize it as transient
   and retry the same research tool.
3. Do not answer from model memory after a tool failure.
4. After evidence is returned, answer from that evidence only.
5. Cite evidence using numbered markers such as [1].
6. Finish with a Sources section containing the exact URL for every citation used.
7. Do not keep retrying after valid evidence has been returned.
8. If recovery never succeeds, state that the task could not be completed safely.
9. Keep the answer concise.
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


async def run_autogen_broken_tool_relay(
    prompt: str,
    settings: Settings,
    shared_evidence: list[ToolEvidence],
) -> ExecutionResult:
    tracker = FaultInjectedEvidenceTool(shared_evidence)
    started = time.perf_counter()
    model_client = None

    trace = [
        TraceEvent("Scenario", "passed", "First evidence-tool call will return simulated HTTP 503."),
        TraceEvent("Agent", "running", "AutoGen relay runner started."),
    ]

    async def resilient_research(query: str) -> str:
        """Retrieve evidence. A transient first-call failure may occur."""
        return await tracker.retrieve(query)

    try:
        model_client = OpenAIChatCompletionClient(
            model=settings.model,
            api_key=settings.openai_api_key,
        )

        agent = AssistantAgent(
            name="broken_tool_relay_autogen",
            model_client=model_client,
            tools=[resilient_research],
            system_message=SYSTEM_INSTRUCTIONS,
            reflect_on_tool_use=True,
            max_tool_iterations=4,
        )

        result = await agent.run(task=prompt)
        messages = list(result.messages)
        final_message = messages[-1] if messages else None
        answer = str(getattr(final_message, "content", "") or "")

        llm_requests, input_tokens, output_tokens = _usage_from_messages(messages)
        recovery = tracker.recovery_metrics()
        behavior = tracker.behavior()

        trace.append(
            TraceEvent(
                "Failure injection",
                "warning" if recovery.failure_injected else "failed",
                f"{recovery.injected_failures} controlled transient failure injected.",
            )
        )
        trace.append(
            TraceEvent(
                "Retry",
                "passed" if recovery.retry_attempted else "failed",
                f"{tracker.call_count} total evidence-tool calls.",
            )
        )
        trace.append(
            TraceEvent(
                "Recovery",
                "passed" if recovery.recovered else "failed",
                (
                    f"Evidence returned after retry; {len(tracker.delivered_evidence)} items delivered."
                    if recovery.recovered
                    else "No valid evidence was delivered after the failure."
                ),
            )
        )
        trace.append(
            TraceEvent(
                "Recovery efficiency",
                "passed" if recovery.unnecessary_extra_calls == 0 else "warning",
                f"{recovery.unnecessary_extra_calls} unnecessary extra tool calls after minimum recovery path.",
            )
        )
        trace.append(TraceEvent("Final response", "passed", "Agent completed the relay."))

        deterministic = run_deterministic_evaluation(
            answer=answer,
            tool_calls=tracker.call_count,
            evidence=tracker.delivered_evidence,
            evidence_supplied=False,
        )

        return ExecutionResult(
            framework_id="autogen",
            framework_name="Microsoft AutoGen",
            event_id="broken_tool_relay",
            model=settings.model,
            mode="fault_injection",
            status="success",
            answer=answer,
            duration_seconds=round(time.perf_counter() - started, 3),
            llm_requests=llm_requests,
            tool_calls=tracker.call_count,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            trace=trace,
            evidence=list(tracker.delivered_evidence),
            research_behavior=behavior,
            recovery=recovery,
            deterministic_eval=deterministic,
        )
    except Exception as exc:
        recovery = tracker.recovery_metrics()
        trace.append(TraceEvent("Run", "failed", f"{type(exc).__name__}: {exc}"))
        return ExecutionResult(
            framework_id="autogen",
            framework_name="Microsoft AutoGen",
            event_id="broken_tool_relay",
            model=settings.model,
            mode="fault_injection",
            status="failed",
            duration_seconds=round(time.perf_counter() - started, 3),
            tool_calls=tracker.call_count,
            trace=trace,
            evidence=list(tracker.delivered_evidence),
            research_behavior=tracker.behavior(),
            recovery=recovery,
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        if model_client is not None:
            await model_client.close()
