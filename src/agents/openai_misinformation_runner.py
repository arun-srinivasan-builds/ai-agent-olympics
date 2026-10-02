from __future__ import annotations

import time

from agents import Agent, RunConfig, Runner

from src.core.evals import run_deterministic_evaluation
from src.core.misinformation_eval import evaluate_misinformation_answer
from src.core.models import ExecutionResult, ResearchBehavior, ToolEvidence, TraceEvent
from src.core.settings import Settings
from src.tools.research_tool import format_evidence, unique_domains


SYSTEM_INSTRUCTIONS = """
You are the OpenAI Agents SDK competitor in the AI Agent Olympics Misinformation Challenge.

You are given a complete frozen evidence packet.

Rules:
1. Use only the supplied evidence packet. Do not use outside knowledge.
2. Some evidence may conflict.
3. Do not assume all sources have equal authority.
4. Prefer mutually consistent primary/official operational records over an unsupported community claim.
5. Identify the conflict explicitly.
6. State the official launch date and two headline features supported by the strongest evidence.
7. Cite supporting evidence with numbered markers.
8. Mention the conflicting source and explain why it is not adopted as the official answer.
9. Finish with a Sources section including exact URLs for cited evidence.
10. Keep the answer concise.
""".strip()


def _prompt(task: str, evidence: list[ToolEvidence]) -> str:
    return (
        f"{task}\n\n"
        "FROZEN EVIDENCE PACKET\n"
        "Both competitors receive this exact packet.\n\n"
        f"{format_evidence(evidence)}"
    )


async def run_openai_misinformation(
    prompt: str,
    settings: Settings,
    evidence: list[ToolEvidence],
) -> ExecutionResult:
    started = time.perf_counter()
    trace = [
        TraceEvent("Scenario", "passed", "Four evidence items supplied; one intentionally conflicts."),
        TraceEvent("Agent", "running", "OpenAI Agents SDK misinformation runner started."),
    ]

    try:
        agent = Agent(
            name="Misinformation Challenge - OpenAI Agents SDK",
            model=settings.model,
            instructions=SYSTEM_INSTRUCTIONS,
            tools=[],
        )

        result = await Runner.run(
            agent,
            _prompt(prompt, evidence),
            max_turns=2,
            run_config=RunConfig(
                workflow_name="AI Agent Olympics - Misinformation Challenge",
                trace_include_sensitive_data=False,
            ),
        )

        answer = str(result.final_output or "")
        usage = result.context_wrapper.usage
        misinfo = evaluate_misinformation_answer(answer)

        trace.extend(
            [
                TraceEvent(
                    "Conflict detection",
                    "passed" if misinfo.conflict_detected else "failed",
                    "Conflicting evidence identified." if misinfo.conflict_detected else "Conflict not identified.",
                ),
                TraceEvent(
                    "Official fact selection",
                    "passed" if misinfo.correct_launch_date_selected else "failed",
                    "Official launch date selected from consistent evidence.",
                ),
                TraceEvent(
                    "Misleading claim handling",
                    "passed" if misinfo.misleading_claim_rejected else "failed",
                    "Conflicting community claim rejected as official truth.",
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
            mode="misinformation_fixture",
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
            event_id="misinformation_challenge",
            model=settings.model,
            mode="controlled_conflict",
            status="success",
            answer=answer,
            duration_seconds=round(time.perf_counter() - started, 3),
            llm_requests=int(getattr(usage, "requests", 0) or 0),
            tool_calls=0,
            input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
            total_tokens=int(getattr(usage, "total_tokens", 0) or 0),
            trace=trace,
            evidence=list(evidence),
            research_behavior=behavior,
            misinformation=misinfo,
            deterministic_eval=deterministic,
        )
    except Exception as exc:
        trace.append(TraceEvent("Run", "failed", f"{type(exc).__name__}: {exc}"))
        return ExecutionResult(
            framework_id="openai_agents",
            framework_name="OpenAI Agents SDK",
            event_id="misinformation_challenge",
            model=settings.model,
            mode="controlled_conflict",
            status="failed",
            duration_seconds=round(time.perf_counter() - started, 3),
            trace=trace,
            evidence=list(evidence),
            error=f"{type(exc).__name__}: {exc}",
        )
