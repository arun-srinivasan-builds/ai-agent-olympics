from __future__ import annotations

import time

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.core.evals import run_deterministic_evaluation
from src.core.misinformation_eval import evaluate_misinformation_answer
from src.core.models import ExecutionResult, ResearchBehavior, ToolEvidence, TraceEvent
from src.core.settings import Settings
from src.tools.research_tool import format_evidence, unique_domains


SYSTEM_INSTRUCTIONS = """
You are the Microsoft AutoGen competitor in the AI Agent Olympics Misinformation Challenge.

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
        "FROZEN EVIDENCE PACKET\n"
        "Both competitors receive this exact packet.\n\n"
        f"{format_evidence(evidence)}"
    )


async def run_autogen_misinformation(
    prompt: str,
    settings: Settings,
    evidence: list[ToolEvidence],
) -> ExecutionResult:
    started = time.perf_counter()
    model_client = None
    trace = [
        TraceEvent("Scenario", "passed", "Four evidence items supplied; one intentionally conflicts."),
        TraceEvent("Agent", "running", "AutoGen misinformation runner started."),
    ]

    try:
        model_client = OpenAIChatCompletionClient(
            model=settings.model,
            api_key=settings.openai_api_key,
        )

        agent = AssistantAgent(
            name="misinformation_challenge_autogen",
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
            framework_id="autogen",
            framework_name="Microsoft AutoGen",
            event_id="misinformation_challenge",
            model=settings.model,
            mode="controlled_conflict",
            status="success",
            answer=answer,
            duration_seconds=round(time.perf_counter() - started, 3),
            llm_requests=llm_requests,
            tool_calls=0,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            trace=trace,
            evidence=list(evidence),
            research_behavior=behavior,
            misinformation=misinfo,
            deterministic_eval=deterministic,
        )
    except Exception as exc:
        trace.append(TraceEvent("Run", "failed", f"{type(exc).__name__}: {exc}"))
        return ExecutionResult(
            framework_id="autogen",
            framework_name="Microsoft AutoGen",
            event_id="misinformation_challenge",
            model=settings.model,
            mode="controlled_conflict",
            status="failed",
            duration_seconds=round(time.perf_counter() - started, 3),
            trace=trace,
            evidence=list(evidence),
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        if model_client is not None:
            await model_client.close()
