import streamlit as st

from config.events import COMPETITORS, EVENTS, FAIR_TEST_RULES
from src.ui import (
    competitor_card,
    empty_result,
    event_card,
    inject_global_css,
    metric_card,
    section_title,
)

st.set_page_config(
    page_title="AI Agent Olympics",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()

if "selected_event" not in st.session_state:
    st.session_state.selected_event = EVENTS[0]["id"]

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
        <div class="live-badge"><span class="live-dot"></span> LAB READY</div>
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
            <h1>What happens when AI agents face the problems demos usually hide?</h1>
            <p>
                Two agent architectures will face the same tasks, tools, evidence and evaluation rules.
                The goal is not to crown a universal winner. It is to understand how each architecture
                behaves under realistic operating pressure.
            </p>
            <div class="hero-tags">
                <span class="hero-tag">Same Task</span>
                <span class="hero-tag">Same Model</span>
                <span class="hero-tag">Equivalent Tools</span>
                <span class="hero-tag">Measured Recovery</span>
                <span class="hero-tag">Guardrails + Evals</span>
                <span class="hero-tag">API Efficiency</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4)
    with metric_cols[0]:
        metric_card("Events configured", "5 / 5", "Experiment definitions are ready.")
    with metric_cols[1]:
        metric_card("Events executed", "0 / 5", "No live benchmark has been run yet.")
    with metric_cols[2]:
        metric_card("Agent runs", "0", "Framework integration begins in Milestone 2.")
    with metric_cols[3]:
        metric_card("Results status", "Not Run", "No synthetic scores are displayed.")

    section_title(
        "Competitors",
        "Both implementations will be evaluated through the same event harness.",
    )
    comp_cols = st.columns(2)
    for index, competitor in enumerate(COMPETITORS):
        with comp_cols[index]:
            competitor_card(
                competitor["name"],
                competitor["status"],
                competitor["description"],
            )

    section_title(
        "Olympic Events",
        "Five tests covering usefulness, resilience, safety, evidence quality and efficiency.",
    )
    for event in EVENTS:
        event_card(event)

    section_title(
        "Fair Test Protocol",
        "Controls designed to reduce accidental bias between the two implementations.",
    )
    left, right = st.columns([1.05, 1])
    with left:
        rules_html = "".join(
            f'<div class="rule-item"><span class="rule-check">✓</span>{rule}</div>'
            for rule in FAIR_TEST_RULES
        )
        st.markdown(f'<div class="rule-card">{rules_html}</div>', unsafe_allow_html=True)
    with right:
        st.markdown(
            """
            <div class="method-note">
                <strong>Important:</strong> this project reports measured behavior from these controlled
                experiments. It will not claim that one framework is universally better than another.
                Differences in orchestration, retries, handoffs and tool usage will be shown as evidence.
            </div>
            """,
            unsafe_allow_html=True,
        )

elif page == "Live Arena":
    section_title(
        "Live Arena",
        "This view will stream one controlled experiment side-by-side once the agent runners are connected.",
    )

    event_lookup = {event["id"]: event for event in EVENTS}
    selected_name = st.selectbox(
        "Choose an event",
        options=[event["id"] for event in EVENTS],
        format_func=lambda event_id: f'{event_lookup[event_id]["icon"]}  {event_lookup[event_id]["name"]}',
    )
    st.session_state.selected_event = selected_name
    selected = event_lookup[selected_name]

    st.markdown(
        f"""
        <div class="event-card">
            <div class="event-title-row">
                <span class="event-icon">{selected["icon"]}</span>
                <div>
                    <div class="event-number">SELECTED EVENT {selected["number"]}</div>
                    <div class="event-name">{selected["name"]}</div>
                    <div class="event-question">{selected["question"]}</div>
                </div>
            </div>
            <div class="event-business"><strong>Why it matters:</strong> {selected["business_value"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    arena_cols = st.columns(2)
    with arena_cols[0]:
        st.markdown("### OpenAI Agents SDK")
        empty_result(
            "Waiting for agent runner",
            "Execution trace, tool activity, guardrails and metrics will appear here.",
        )
    with arena_cols[1]:
        st.markdown("### Microsoft AutoGen")
        empty_result(
            "Waiting for agent runner",
            "Execution trace, tool activity, guardrails and metrics will appear here.",
        )

    st.info(
        "Milestone 1 intentionally does not simulate results. "
        "The Run Event control will be activated when both real framework runners are connected."
    )

elif page == "Events":
    section_title(
        "Event Catalogue",
        "Each event has a plain-English purpose and a measurable engineering objective.",
    )

    for event in EVENTS:
        event_card(event)
        with st.expander(f'What will we measure in {event["name"]}?'):
            if event["id"] == "research_sprint":
                st.write(
                    "Task completion, source validation, citation correctness, groundedness, "
                    "tool calls, LLM calls and estimated cost."
                )
            elif event["id"] == "broken_tool_relay":
                st.write(
                    "Failure detection, recovery attempt count, fallback selection, successful completion, "
                    "extra tool/LLM calls and cost introduced by recovery."
                )
            elif event["id"] == "misinformation_challenge":
                st.write(
                    "Conflict detection, evidence comparison, uncertainty handling, unsupported claims, "
                    "groundedness and final-answer quality."
                )
            elif event["id"] == "prompt_injection_hurdle":
                st.write(
                    "Injection detection, instruction integrity, unsafe tool behavior, output validation "
                    "and whether untrusted content changes the intended task."
                )
            elif event["id"] == "budget_marathon":
                st.write(
                    "Task completion within a controlled budget, LLM calls, tool calls, token usage, "
                    "estimated cost and duplicate/unnecessary work."
                )

elif page == "Results":
    section_title(
        "Experiment Results",
        "Only evidence generated by real event executions will be shown here.",
    )

    result_cols = st.columns(4)
    with result_cols[0]:
        metric_card("Completed comparisons", "0", "Waiting for live execution.")
    with result_cols[1]:
        metric_card("Guardrail checks", "0", "No benchmark data yet.")
    with result_cols[2]:
        metric_card("Evaluation records", "0", "No benchmark data yet.")
    with result_cols[3]:
        metric_card("Measured cost", "$0.00", "No API calls have been made.")

    empty_result(
        "No experiment results yet",
        "After Milestone 2, each event will produce framework-specific traces, metrics and evaluation evidence.",
    )

elif page == "Learnings":
    section_title(
        "Learning Log",
        "Engineering conclusions will be added only after a measured experiment supports them.",
    )

    st.markdown(
        """
        <div class="rule-card">
            <div class="rule-item"><span class="rule-check">✓</span>
                Experiment framing completed: compare behavior, not marketing claims.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Five event categories defined: research, resilience, misinformation, security and efficiency.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Dashboard avoids fake benchmark scores before real execution.
            </div>
            <div class="rule-item"><span class="rule-check">✓</span>
                Fair-test protocol defined before framework implementation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Next engineering milestone")
    st.write(
        "Connect the first real competitors, establish a common result schema, "
        "and run a baseline task through both frameworks."
    )
