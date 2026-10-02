from __future__ import annotations

import time

from agents import Agent, RunConfig, Runner
from agents.decorators import tool

from src.core.evals import run_deterministic_evaluation
from src.core.models import ExecutionResult, ToolEvidence, TraceEvent
from src.core.settings import Settings
from src.tools.fault_injection_tool import FaultInjectedEvidenceTool


SYSTEM_INSTRUCTIONS = """
You are the OpenAI Agents SDK competitor in the AI Agent Olympics Broken Tool Relay.

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


async def run_openai_broken_tool_relay(
    prompt: str,
    settings: Settings,
    shared_evidence: list[ToolEvidence],
) -> ExecutionResult:
    tracker = FaultInjectedEvidenceTool(shared_evidence)
    started = time.perf_counter()

    trace = [
        TraceEvent("Scenario", "passed", "First evidence-tool call will return simulated HTTP 503."),
        TraceEvent("Agent", "running", "OpenAI Agents SDK relay runner started."),
    ]

    @tool
    async def resilient_research(query: str) -> str:
        """Retrieve evidence. A transient first-call failure may occur.

        Args:
            query: The research query to use for this task.
        """
        return await tracker.retrieve(query)

    try:
        agent = Agent(
            name="Broken Tool Relay - OpenAI Agents SDK",
            model=settings.model,
            instructions=SYSTEM_INSTRUCTIONS,
            tools=[resilient_research],
        )

        result = await Runner.run(
            agent,
            prompt,
            max_turns=6,
            run_config=RunConfig(
                workflow_name="AI Agent Olympics - Broken Tool Relay",
                trace_include_sensitive_data=False,
            ),
        )

        answer = str(result.final_output or "")
        usage = result.context_wrapper.usage
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
            framework_id="openai_agents",
            framework_name="OpenAI Agents SDK",
            event_id="broken_tool_relay",
            model=settings.model,
            mode="fault_injection",
            status="success",
            answer=answer,
            duration_seconds=round(time.perf_counter() - started, 3),
            llm_requests=int(getattr(usage, "requests", 0) or 0),
            tool_calls=tracker.call_count,
            input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
            total_tokens=int(getattr(usage, "total_tokens", 0) or 0),
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
            framework_id="openai_agents",
            framework_name="OpenAI Agents SDK",
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
