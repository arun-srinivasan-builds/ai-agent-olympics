import asyncio

import streamlit as st

from config.events import (
    COMPETITORS,
    DEFAULT_RESEARCH_PROMPT,
    EVENTS,
    FAIR_TEST_RULES,
    RESEARCH_MODES,
)
from src.core.experiment_runner import run_research_sprint
from src.core.guardrails import InputGuardrailError
from src.core.settings import get_settings
from src.ui import (
    competitor_card,
    config_status,
    event_card,
    inject_global_css,
    metric_card,
    render_result,
    section_title,
)


def run_async(coro):
    """
    Execute async work on one persistent event loop for this Streamlit session.
    This avoids closing the SDK transport loop between button-click reruns.
    """
    loop = st.session_state.get("_async_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state["_async_loop"] = loop

    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def as_text(value):
    """Return type-stable table values for Streamlit/PyArrow."""
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

if "comparison" not in st.session_state:
    st.session_state.comparison = None

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
        <div class="lab-badge"><span class="lab-dot"></span> RESEARCH SPRINT 2.1</div>
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
            <div class="eyebrow">Controlled AI Agent Evaluation</div>
            <h1>Same question. Two research strategies. Evidence you can inspect.</h1>
            <p>
                Research Sprint now separates search behaviour from evidence interpretation.
                Run agents autonomously, or freeze one evidence packet and make both interpret
                exactly the same information.
            </p>
            <div class="hero-tags">
                <span class="hero-tag">Autonomous Research</span>
                <span class="hero-tag">Controlled Evidence</span>
                <span class="hero-tag">Citation Integrity</span>
                <span class="hero-tag">Requirement Coverage</span>
                <span class="hero-tag">Real Usage Metrics</span>
                <span class="hero-tag">Evaluation Cost Separated</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    comparison = st.session_state.comparison
    successful_runs = 0
    if comparison:
        successful_runs = sum(
            result.status == "success"
            for result in [comparison.openai_agents, comparison.autogen]
        )

    cols = st.columns(4)
    with cols[0]:
        metric_card("Events configured", "5 / 5", "Five Olympic events defined.")
    with cols[1]:
        metric_card("Research modes", "2", "Autonomous + Controlled Evidence.")
    with cols[2]:
        metric_card("Latest agent runs", str(successful_runs), "Successful current-session runs.")
    with cols[3]:
        metric_card("Evaluation layer", "2-stage", "Deterministic + semantic evidence checks.")

    config_status(settings.ready, settings.model, settings.eval_model)

    section_title(
        "Competitors",
        "Both use the same configured model; framework orchestration remains native.",
    )
    cols = st.columns(2)
    for i, competitor in enumerate(COMPETITORS):
        with cols[i]:
            competitor_card(
                competitor["name"],
                competitor["status"],
                competitor["description"],
            )

    section_title(
        "What changed after our first live run?",
        "The first experiment showed that a format-level PASS can still hide answer-quality problems.",
    )
    st.markdown(
        """
        <div class="quality-callout">
            <strong>Simple eval:</strong> Did it answer? Did it search? Did it cite?<br><br>
            <strong>Evidence-aware eval:</strong> Do citations map correctly? Are cited URLs actually
            listed? Does the evidence support the claims? Was every user requirement answered?
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_title("Olympic Events", "Research Sprint is live with evidence-aware evaluation.")
    for event in EVENTS:
        event_card(event)

    section_title("Fair Test Protocol", "Controls defined before interpreting results.")
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
                <strong>Autonomous mode</strong> intentionally allows different evidence because
                search strategy is part of the agent behaviour.<br><br>
                <strong>Controlled mode</strong> removes that variable by sharing one evidence packet.
            </div>
            """,
            unsafe_allow_html=True,
        )

elif page == "Live Arena":
    section_title(
        "Live Arena — Research Sprint",
        "Choose whether you want to test research strategy or evidence interpretation.",
    )
    config_status(settings.ready, settings.model, settings.eval_model)

    mode_label = st.radio(
        "Research mode",
        options=["autonomous", "controlled"],
        format_func=lambda key: RESEARCH_MODES[key]["label"],
        horizontal=True,
    )
    mode = mode_label

    st.markdown(
        f"""
        <div class="mode-card">
            <strong>{RESEARCH_MODES[mode]["label"]}</strong><br>
            {RESEARCH_MODES[mode]["description"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    prompt = st.text_area(
        "Research question",
        value=DEFAULT_RESEARCH_PROMPT,
        height=110,
        help="The exact same user question is passed to both competitors.",
    )

    semantic_eval_enabled = st.checkbox(
        "Run semantic evidence evaluator (adds 2 shared judge model calls)",
        value=True,
        help=(
            "Evaluator usage is recorded separately and is never added to either "
            "competitor's token/call metrics."
        ),
    )

    run_clicked = st.button(
        "🏁 Run Research Sprint",
        type="primary",
        disabled=not settings.ready,
    )

    if run_clicked:
        try:
            with st.status("Running controlled comparison...", expanded=True) as status:
                if mode == "controlled":
                    st.write("0/3 — Fetching one shared evidence packet")
                st.write("1/3 — Running OpenAI Agents SDK")
                st.write("2/3 — Running Microsoft AutoGen")
                if semantic_eval_enabled:
                    st.write("3/3 — Applying the same evidence evaluator to both answers")

                comparison = run_async(
                    run_research_sprint(
                        prompt=prompt,
                        settings=settings,
                        mode=mode,
                        semantic_eval_enabled=semantic_eval_enabled,
                    )
                )
                st.session_state.comparison = comparison
                status.update(
                    label="Research Sprint completed",
                    state="complete",
                    expanded=False,
                )
        except InputGuardrailError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Experiment controller failed: {type(exc).__name__}: {exc}")

    comparison = st.session_state.comparison

    if comparison:
        mode_name = RESEARCH_MODES[comparison.mode]["label"]
        st.caption(
            f"Mode: {mode_name} • Model: {comparison.model} • "
            f"Evidence run: {comparison.created_at_utc}"
        )

        if comparison.mode == "controlled":
            st.success(
                f"Controlled Evidence active: one shared external search produced "
                f"{len(comparison.shared_evidence)} evidence items. "
                "Both competitors received this exact packet."
            )

        tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
        with tabs[0]:
            render_result(comparison.openai_agents)
        with tabs[1]:
            render_result(comparison.autogen)

        section_title(
            "Side-by-Side Measured Metrics",
            "Descriptive measurements only — no universal framework winner is declared.",
        )

        oa = comparison.openai_agents
        ag = comparison.autogen
        st.table(
            {
                "Metric": [
                    "Run status",
                    "LLM requests",
                    "Evidence tool calls",
                    "External searches",
                    "Input tokens",
                    "Output tokens",
                    "Total tokens",
                    "Duration (seconds)",
                    "Deterministic checks",
                    "Evidence support",
                    "Incomplete requirements",
                ],
                "OpenAI Agents SDK": [
                    as_text(oa.status),
                    as_text(oa.llm_requests),
                    as_text(oa.tool_calls),
                    as_text(oa.research_behavior.external_search_calls),
                    as_text(oa.input_tokens),
                    as_text(oa.output_tokens),
                    as_text(oa.total_tokens),
                    as_text(oa.duration_seconds),
                    f"{oa.deterministic_eval.passed_checks}/{oa.deterministic_eval.total_checks}",
                    as_text(oa.semantic_eval.evidence_support),
                    as_text(len(oa.semantic_eval.incomplete_requirements)),
                ],
                "Microsoft AutoGen": [
                    as_text(ag.status),
                    as_text(ag.llm_requests),
                    as_text(ag.tool_calls),
                    as_text(ag.research_behavior.external_search_calls),
                    as_text(ag.input_tokens),
                    as_text(ag.output_tokens),
                    as_text(ag.total_tokens),
                    as_text(ag.duration_seconds),
                    f"{ag.deterministic_eval.passed_checks}/{ag.deterministic_eval.total_checks}",
                    as_text(ag.semantic_eval.evidence_support),
                    as_text(len(ag.semantic_eval.incomplete_requirements)),
                ],
            }
        )

        if semantic_eval_enabled:
            eval_calls = (
                oa.semantic_eval.judge_requests
                + ag.semantic_eval.judge_requests
            )
            eval_tokens = (
                oa.semantic_eval.judge_input_tokens
                + oa.semantic_eval.judge_output_tokens
                + ag.semantic_eval.judge_input_tokens
                + ag.semantic_eval.judge_output_tokens
            )
            st.caption(
                f"Evaluation overhead kept separate: {eval_calls} judge model calls, "
                f"{eval_tokens:,} judge tokens."
            )
    else:
        st.info("No Research Sprint has been run in this browser session yet.")

elif page == "Events":
    section_title(
        "Event Catalogue",
        "Research Sprint now has two experimental modes and an evidence-aware evaluator.",
    )
    for event in EVENTS:
        event_card(event)

elif page == "Results":
    section_title(
        "Experiment Results",
        "Measured agent behaviour and answer-quality evidence from the latest session run.",
    )

    comparison = st.session_state.comparison
    if not comparison:
        st.info("Run Research Sprint from Live Arena first.")
    else:
        oa = comparison.openai_agents
        ag = comparison.autogen

        cols = st.columns(4)
        with cols[0]:
            metric_card(
                "Mode",
                "Controlled" if comparison.mode == "controlled" else "Autonomous",
                "What variable this run isolates.",
            )
        with cols[1]:
            metric_card(
                "Competitor LLM calls",
                str(oa.llm_requests + ag.llm_requests),
                "Does not include evaluator calls.",
            )
        with cols[2]:
            competitor_searches = (
                oa.research_behavior.external_search_calls
                + ag.research_behavior.external_search_calls
            )
            total_searches = competitor_searches + comparison.shared_external_search_calls
            metric_card(
                "External searches",
                str(total_searches),
                "Includes shared prefetch when controlled.",
            )
        with cols[3]:
            metric_card(
                "Competitor tokens",
                f"{oa.total_tokens + ag.total_tokens:,}",
                "Evaluator tokens excluded.",
            )

        st.markdown(
            """
            <div class="quality-callout">
                <strong>Why the old 3/3 could mislead:</strong><br>
                Format-level checks can confirm that an answer exists, a tool was used and
                citation syntax is present. They cannot by themselves prove that the cited
                evidence supports the claim or that every requested detail was answered.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Evidence quality")
        st.table(
            {
                "Check": [
                    "Citation numbers valid",
                    "Cited URLs listed",
                    "Evidence support",
                    "Incomplete requirements",
                    "Unsupported claims",
                    "Contradictions",
                ],
                "OpenAI Agents SDK": [
                    as_text(oa.deterministic_eval.citation_numbers_valid),
                    as_text(oa.deterministic_eval.cited_urls_listed),
                    as_text(oa.semantic_eval.evidence_support),
                    as_text(len(oa.semantic_eval.incomplete_requirements)),
                    as_text(len(oa.semantic_eval.unsupported_claims)),
                    as_text(len(oa.semantic_eval.contradictions)),
                ],
                "Microsoft AutoGen": [
                    as_text(ag.deterministic_eval.citation_numbers_valid),
                    as_text(ag.deterministic_eval.cited_urls_listed),
                    as_text(ag.semantic_eval.evidence_support),
                    as_text(len(ag.semantic_eval.incomplete_requirements)),
                    as_text(len(ag.semantic_eval.unsupported_claims)),
                    as_text(len(ag.semantic_eval.contradictions)),
                ],
            }
        )

elif page == "Learnings":
    section_title(
        "Learning Log",
        "What the experiment design itself has taught us so far.",
    )

    st.markdown(
        """
        <div class="rule-card">
            <div class="rule-item"><span class="rule-check">✓</span>
                Same tool does not automatically mean same evidence.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                An agent can search successfully and still stop before every requirement is resolved.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Citation syntax is not the same thing as citation integrity.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Controlled Evidence isolates interpretation; Autonomous Research tests the complete strategy.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Evaluation overhead must be measured separately from competitor efficiency.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Next milestone")
    st.write(
        "Broken Tool Relay: inject a controlled research-tool failure, measure detection, "
        "retry/fallback behaviour and the extra model/tool cost of recovery."
    )
