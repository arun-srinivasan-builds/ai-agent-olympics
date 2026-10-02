import asyncio

import streamlit as st

from config.events import (
    BROKEN_TOOL_PREFETCH_QUERY,
    BROKEN_TOOL_PROMPT,
    COMPETITORS,
    DEFAULT_RESEARCH_PROMPT,
    EVENTS,
    FAIR_TEST_RULES,
    RESEARCH_MODES,
)
from src.core.experiment_runner import (
    run_broken_tool_relay,
    run_research_sprint,
)
from src.core.guardrails import InputGuardrailError
from src.core.settings import get_settings
from src.ui import (
    competitor_card,
    config_status,
    event_card,
    inject_global_css,
    metric_card,
    render_recovery_result,
    render_result,
    section_title,
)


def run_async(coro):
    loop = st.session_state.get("_async_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state["_async_loop"] = loop

    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def as_text(value):
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


st.set_page_config(
    page_title="AI Agent Olympics",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()
settings = get_settings()

st.session_state.setdefault("research_comparison", None)
st.session_state.setdefault("relay_comparison", None)

st.markdown(
    """
    <div class="brand-row">
        <div class="brand-left">
            <div class="brand-mark">🏅</div>
            <div>
                <div class="brand-title">AI Agent Olympics</div>
                <div class="brand-subtitle">Enterprise Agent Reliability & Efficiency Lab</div>
            </div>
        </div>
        <div class="lab-badge"><span class="lab-dot"></span> EVENT 02 LIVE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.radio(
    "Navigation",
    ["Overview", "Live Arena", "Events", "Results", "Learnings"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "Overview":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">AI Agents Under Pressure</div>
            <h1>What happens when the tool an AI agent depends on suddenly fails?</h1>
            <p>
                Research Sprint is validated. Broken Tool Relay now injects the same controlled
                transient failure into both competitors and measures whether they detect it,
                retry, recover, and finish without unnecessary orchestration.
            </p>
            <div class="hero-tags">
                <span class="hero-tag">Same Model</span>
                <span class="hero-tag">Same Evidence</span>
                <span class="hero-tag">Same Injected 503</span>
                <span class="hero-tag">Retry Tracking</span>
                <span class="hero-tag">Recovery Evals</span>
                <span class="hero-tag">Recovery Overhead</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    with cols[0]:
        metric_card("Events configured", "5 / 5", "Olympic event catalogue.")
    with cols[1]:
        metric_card("Events validated", "1 / 5", "Research Sprint complete.")
    with cols[2]:
        metric_card("Current event", "02", "Broken Tool Relay.")
    with cols[3]:
        metric_card("Failure pattern", "503 → Retry", "First tool call fails by design.")

    config_status(settings.ready, settings.model, settings.eval_model)

    section_title("Competitors", "Both face exactly the same fault-injection scenario.")
    cols = st.columns(2)
    for index, competitor in enumerate(COMPETITORS):
        with cols[index]:
            competitor_card(
                competitor["name"],
                competitor["status"],
                competitor["description"],
            )

    section_title("Olympic Events", "Research Sprint complete; Broken Tool Relay is live.")
    for event in EVENTS:
        event_card(event)

    section_title("Broken Tool Relay — Fair Test", "Failure and recovery path are controlled.")
    left, right = st.columns([1.05, 1])
    with left:
        rules = "".join(
            f'<div class="rule-item"><span class="rule-check">✓</span>{rule}</div>'
            for rule in FAIR_TEST_RULES
        )
        st.markdown(f'<div class="rule-card">{rules}</div>', unsafe_allow_html=True)
    with right:
        st.markdown(
            """
            <div class="method-note">
                <strong>Controller:</strong> fetches one evidence packet.<br><br>
                <strong>Call 1:</strong> tool returns simulated HTTP 503.<br><br>
                <strong>Call 2:</strong> same tool returns the frozen evidence.<br><br>
                The minimum clean recovery path is therefore exactly <strong>2 tool calls</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )

elif page == "Live Arena":
    section_title(
        "Live Arena",
        "Choose an event. Research Sprint remains available; Broken Tool Relay is the current event.",
    )
    config_status(settings.ready, settings.model, settings.eval_model)

    selected_event = st.selectbox(
        "Olympic event",
        ["broken_tool_relay", "research_sprint"],
        format_func=lambda event_id: (
            "🔌 Broken Tool Relay — LIVE"
            if event_id == "broken_tool_relay"
            else "🔎 Research Sprint — COMPLETE"
        ),
    )

    if selected_event == "broken_tool_relay":
        st.markdown(
            """
            <div class="event-card">
                <div class="event-title-row">
                    <span class="event-icon">🔌</span>
                    <div>
                        <div class="event-number">EVENT 02 • LIVE</div>
                        <div class="event-name">Broken Tool Relay</div>
                        <div class="event-question">
                            First tool call fails with a controlled 503. Can the agent recover?
                        </div>
                    </div>
                </div>
                <div class="event-business">
                    <strong>Failure contract:</strong> both competitors receive the same frozen
                    evidence. Their first tool call fails. The next call succeeds.
                    Minimum clean recovery path = 2 tool calls.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        prompt = st.text_area(
            "Relay task",
            value=BROKEN_TOOL_PROMPT,
            height=110,
        )

        semantic_eval_enabled = st.checkbox(
            "Run semantic evidence evaluator after successful recovery",
            value=True,
            key="relay_semantic",
        )

        if st.button(
            "🔌 Run Broken Tool Relay",
            type="primary",
            disabled=not settings.ready,
        ):
            try:
                with st.status("Running Broken Tool Relay...", expanded=True) as status:
                    st.write("0/4 — Controller fetches one shared evidence packet")
                    st.write("1/4 — OpenAI Agents SDK receives simulated 503")
                    st.write("2/4 — AutoGen receives the same simulated 503")
                    st.write("3/4 — Measuring retry, recovery and overhead")
                    if semantic_eval_enabled:
                        st.write("4/4 — Evaluating final evidence-grounded answers")

                    comparison = run_async(
                        run_broken_tool_relay(
                            prompt=prompt,
                            settings=settings,
                            shared_search_query=BROKEN_TOOL_PREFETCH_QUERY,
                            semantic_eval_enabled=semantic_eval_enabled,
                        )
                    )
                    st.session_state.relay_comparison = comparison
                    status.update(
                        label="Broken Tool Relay completed",
                        state="complete",
                        expanded=False,
                    )
            except InputGuardrailError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Event controller failed: {type(exc).__name__}: {exc}")

        comparison = st.session_state.relay_comparison
        if comparison:
            st.success(
                f"Fault-injection evidence prepared once: "
                f"{len(comparison.shared_evidence)} shared evidence items • "
                f"{comparison.shared_external_search_calls} controller search."
            )

            tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
            with tabs[0]:
                render_recovery_result(comparison.openai_agents)
            with tabs[1]:
                render_recovery_result(comparison.autogen)

            section_title(
                "Side-by-Side Recovery Metrics",
                "Descriptive measurements from this controlled failure event.",
            )

            oa = comparison.openai_agents
            ag = comparison.autogen

            st.table(
                {
                    "Metric": [
                        "Run status",
                        "Failure injected",
                        "Retry attempted",
                        "Recovered",
                        "Tool calls",
                        "Minimum clean path",
                        "Unnecessary extra calls",
                        "LLM requests",
                        "Input tokens",
                        "Output tokens",
                        "Total tokens",
                        "Duration (seconds)",
                        "Deterministic checks",
                        "Evidence support",
                    ],
                    "OpenAI Agents SDK": [
                        as_text(oa.status),
                        as_text(oa.recovery.failure_injected),
                        as_text(oa.recovery.retry_attempted),
                        as_text(oa.recovery.recovered),
                        as_text(oa.tool_calls),
                        as_text(oa.recovery.expected_minimum_tool_calls),
                        as_text(oa.recovery.unnecessary_extra_calls),
                        as_text(oa.llm_requests),
                        as_text(oa.input_tokens),
                        as_text(oa.output_tokens),
                        as_text(oa.total_tokens),
                        as_text(oa.duration_seconds),
                        f"{oa.deterministic_eval.passed_checks}/{oa.deterministic_eval.total_checks}",
                        as_text(oa.semantic_eval.evidence_support),
                    ],
                    "Microsoft AutoGen": [
                        as_text(ag.status),
                        as_text(ag.recovery.failure_injected),
                        as_text(ag.recovery.retry_attempted),
                        as_text(ag.recovery.recovered),
                        as_text(ag.tool_calls),
                        as_text(ag.recovery.expected_minimum_tool_calls),
                        as_text(ag.recovery.unnecessary_extra_calls),
                        as_text(ag.llm_requests),
                        as_text(ag.input_tokens),
                        as_text(ag.output_tokens),
                        as_text(ag.total_tokens),
                        as_text(ag.duration_seconds),
                        f"{ag.deterministic_eval.passed_checks}/{ag.deterministic_eval.total_checks}",
                        as_text(ag.semantic_eval.evidence_support),
                    ],
                }
            )

    else:
        mode = st.radio(
            "Research mode",
            options=["autonomous", "controlled"],
            format_func=lambda key: RESEARCH_MODES[key]["label"],
            horizontal=True,
        )

        prompt = st.text_area(
            "Research question",
            value=DEFAULT_RESEARCH_PROMPT,
            height=110,
        )

        semantic_eval_enabled = st.checkbox(
            "Run semantic evidence evaluator",
            value=True,
            key="research_semantic",
        )

        if st.button(
            "🏁 Run Research Sprint",
            type="primary",
            disabled=not settings.ready,
        ):
            try:
                comparison = run_async(
                    run_research_sprint(
                        prompt=prompt,
                        settings=settings,
                        mode=mode,
                        semantic_eval_enabled=semantic_eval_enabled,
                    )
                )
                st.session_state.research_comparison = comparison
            except Exception as exc:
                st.error(f"Research Sprint failed: {type(exc).__name__}: {exc}")

        comparison = st.session_state.research_comparison
        if comparison:
            tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
            with tabs[0]:
                render_result(comparison.openai_agents)
            with tabs[1]:
                render_result(comparison.autogen)

elif page == "Events":
    section_title(
        "Event Catalogue",
        "Each event isolates a different production concern.",
    )
    for event in EVENTS:
        event_card(event)

elif page == "Results":
    section_title(
        "Results",
        "View the latest measured session result for each validated/live event.",
    )

    result_event = st.selectbox(
        "Result set",
        ["broken_tool_relay", "research_sprint"],
        format_func=lambda value: (
            "🔌 Broken Tool Relay" if value == "broken_tool_relay"
            else "🔎 Research Sprint"
        ),
    )

    if result_event == "broken_tool_relay":
        comparison = st.session_state.relay_comparison
        if not comparison:
            st.info("Run Broken Tool Relay from Live Arena first.")
        else:
            oa = comparison.openai_agents
            ag = comparison.autogen
            cols = st.columns(4)
            with cols[0]:
                metric_card(
                    "Recovered systems",
                    str(sum([oa.recovery.recovered, ag.recovery.recovered])),
                    "Out of two competitors.",
                )
            with cols[1]:
                metric_card(
                    "Total tool calls",
                    str(oa.tool_calls + ag.tool_calls),
                    "Includes failure + retry calls.",
                )
            with cols[2]:
                metric_card(
                    "Extra retry calls",
                    str(
                        oa.recovery.unnecessary_extra_calls
                        + ag.recovery.unnecessary_extra_calls
                    ),
                    "Beyond the minimum clean recovery path.",
                )
            with cols[3]:
                metric_card(
                    "Competitor tokens",
                    f"{oa.total_tokens + ag.total_tokens:,}",
                    "Evaluator usage excluded.",
                )
    else:
        st.info(
            "Research Sprint final findings are documented in "
            "docs/RESEARCH-SPRINT-FINDINGS.md. "
            "You can also rerun it from Live Arena."
        )

elif page == "Learnings":
    section_title(
        "Learning Log",
        "Validated findings plus the current resilience experiment.",
    )

    st.markdown(
        """
        <div class="rule-card">
            <div class="rule-item"><span class="rule-check">✓</span>
                Research Sprint: same model + same tool can still produce different evidence.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Controlled Evidence: outputs converged when both frameworks received the same packet.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Evidence-aware evals caught gaps that simple citation-format checks missed.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Broken Tool Relay now isolates transient-failure recovery using the same evidence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Current question")
    st.write(
        "After a transient tool failure, does each agent retry exactly enough to recover, "
        "or does it stop too early / keep calling the tool unnecessarily?"
    )
