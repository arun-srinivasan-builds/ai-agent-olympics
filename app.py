import asyncio

import streamlit as st

from config.events import (
    BROKEN_TOOL_PREFETCH_QUERY,
    BROKEN_TOOL_PROMPT,
    BUDGET_MARATHON_PROMPT,
    COMPETITORS,
    DEFAULT_RESEARCH_PROMPT,
    EVENTS,
    FAIR_TEST_RULES,
    MISINFORMATION_PROMPT,
    PROMPT_INJECTION_PROMPT,
    RESEARCH_MODES,
)
from src.core.experiment_runner import (
    run_broken_tool_relay,
    run_budget_marathon,
    run_misinformation_challenge,
    run_prompt_injection_hurdle,
    run_research_sprint,
)
from src.core.settings import get_settings
from src.responsive_dashboard import inject_responsive_dashboard_css
from src.premium_dashboard import (
    inject_approved_dashboard_css,
    inject_exact_approved_overrides,
    inject_approved_design_lock_css,
    inject_final_reference_exact_css,
    inject_arena_event_selector_css,
    render_hero,
    render_key_takeaways,
    render_kpi_grid,
    render_live_event_flow,
    render_medal_board,
    render_page_heading,
    render_podium_comparison,
    render_profiles,
    render_section_heading,
    render_sidebar_brand,
    render_telemetry_mini,
    render_top_toolbar,
)
from src.ui import (
    competitor_card,
    config_status,
    event_card,
    get_final_benchmark_df,
    inject_global_css,
    inject_premium_css,
    metric_card,
    render_budget_result,
    render_competition_visuals,
    render_event_result_spotlight,
    render_executive_callout,
    render_executive_medal_board,
    render_insight_card,
    render_live_workflow,
    render_misinformation_result,
    render_page_header,
    render_prompt_injection_result,
    render_recovery_result,
    render_result,
    render_right_rail_heading,
    render_sidebar_overview,
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


ARENA_EVENTS = [
    {
        "id": "research_sprint",
        "number": "EVENT 01",
        "title": "Research Sprint",
        "icon": ":material/search:",
        "description": "Research current evidence, ground the answer and validate citations.",
        "status": "Ready",
    },
    {
        "id": "broken_tool_relay",
        "number": "EVENT 02",
        "title": "Broken Tool Relay",
        "icon": ":material/build:",
        "description": "Inject one transient tool failure and measure disciplined recovery.",
        "status": "Ready",
    },
    {
        "id": "misinformation_challenge",
        "number": "EVENT 03",
        "title": "Misinformation Challenge",
        "icon": ":material/gpp_maybe:",
        "description": "Present conflicting evidence and test source weighting and rejection.",
        "status": "Ready",
    },
    {
        "id": "prompt_injection_hurdle",
        "number": "EVENT 04",
        "title": "Prompt Injection Hurdle",
        "icon": ":material/shield:",
        "description": "Embed malicious instructions in retrieved evidence and test defense.",
        "status": "Ready",
    },
    {
        "id": "budget_marathon",
        "number": "EVENT 05",
        "title": "Budget Marathon",
        "icon": ":material/database:",
        "description": "Hold answer quality constant and compare tokens, latency and model cost.",
        "status": "Ready",
    },
 ]


OFFICIAL_ARENA_PROMPTS = {
    "research_sprint": DEFAULT_RESEARCH_PROMPT,
    "broken_tool_relay": BROKEN_TOOL_PROMPT,
    "misinformation_challenge": MISINFORMATION_PROMPT,
    "prompt_injection_hurdle": PROMPT_INJECTION_PROMPT,
    "budget_marathon": BUDGET_MARATHON_PROMPT,
}


def _arena_prompt_for(event_id: str, prompt_override: str | None = None) -> str:
    prompt = (prompt_override or OFFICIAL_ARENA_PROMPTS[event_id]).strip()
    if not prompt:
        return OFFICIAL_ARENA_PROMPTS[event_id]
    return prompt


def _execute_arena_event(
    event_id: str,
    settings,
    *,
    prompt_override: str | None = None,
    run_mode: str = "benchmark",
):
    """Execute one Olympic event using the official or user-provided challenge question."""
    prompt = _arena_prompt_for(event_id, prompt_override)

    if event_id == "research_sprint":
        comparison = run_async(
            run_research_sprint(
                prompt=prompt,
                settings=settings,
                mode="autonomous",
                semantic_eval_enabled=True,
            )
        )
        st.session_state.research_comparison = comparison
    elif event_id == "broken_tool_relay":
        comparison = run_async(
            run_broken_tool_relay(
                prompt=prompt,
                settings=settings,
                shared_search_query=BROKEN_TOOL_PREFETCH_QUERY,
                semantic_eval_enabled=True,
            )
        )
        st.session_state.relay_comparison = comparison
    elif event_id == "misinformation_challenge":
        comparison = run_async(
            run_misinformation_challenge(
                prompt=prompt,
                settings=settings,
                semantic_eval_enabled=True,
            )
        )
        st.session_state.misinformation_comparison = comparison
    elif event_id == "prompt_injection_hurdle":
        comparison = run_async(
            run_prompt_injection_hurdle(
                prompt=prompt,
                settings=settings,
                semantic_eval_enabled=True,
            )
        )
        st.session_state.prompt_injection_comparison = comparison
    else:
        comparison = run_async(
            run_budget_marathon(
                prompt=prompt,
                settings=settings,
                semantic_eval_enabled=True,
            )
        )
        st.session_state.budget_comparison = comparison

    st.session_state["arena_selected_event"] = event_id
    st.session_state["arena_last_run"] = event_id
    st.session_state["arena_last_run_mode"] = run_mode
    st.session_state["arena_last_prompt"] = prompt
    return comparison



def run_arena_event(
    event_id: str,
    settings,
    *,
    prompt_override: str | None = None,
    run_mode: str = "benchmark",
):
    """Run one Olympic event and show focused progress."""
    event = next(item for item in ARENA_EVENTS if item["id"] == event_id)
    label = "custom experiment" if run_mode == "custom" else "controlled benchmark"
    with st.status(f"Running {event['title']} — {label}...", expanded=True) as status:
        try:
            step_text = {
                "research_sprint": "Running autonomous research with the selected challenge question",
                "broken_tool_relay": "Injecting the controlled transient tool failure",
                "misinformation_challenge": "Supplying the controlled evidence conflict",
                "prompt_injection_hurdle": "Supplying trusted evidence plus the controlled malicious source",
                "budget_marathon": "Applying the fixed six-part quality contract",
            }[event_id]
            st.write(f"1/3 — {step_text}")
            comparison = _execute_arena_event(
                event_id,
                settings,
                prompt_override=prompt_override,
                run_mode=run_mode,
            )
            st.write("2/3 — Comparing OpenAI Agents SDK and Microsoft AutoGen")
            st.write("3/3 — Capturing metrics, deterministic checks and evidence-aware evaluation")
            status.update(label=f"{event['title']} completed", state="complete", expanded=False)
            return comparison
        except Exception as exc:
            status.update(label=f"{event['title']} failed", state="error", expanded=True)
            st.error(f"Event controller failed: {type(exc).__name__}: {exc}")
            return None



def run_all_arena_events(settings):
    """Run all five Olympic events sequentially using validated defaults."""
    batch_results = {}
    failures = []
    with st.status("Running all 5 Olympic events...", expanded=True) as status:
        progress = st.progress(0, text="Starting Olympic pentathlon...")
        for index, event in enumerate(ARENA_EVENTS, start=1):
            st.write(f"{index}/5 — {event['title']}")
            try:
                result = _execute_arena_event(event["id"], settings, run_mode="benchmark")
                batch_results[event["id"]] = "success" if result is not None else "failed"
                if result is None:
                    failures.append(event["id"])
            except Exception as exc:
                batch_results[event["id"]] = f"failed: {type(exc).__name__}"
                failures.append(event["id"])
                st.warning(f"{event['title']} failed; continuing with the remaining events.")
            progress.progress(index / len(ARENA_EVENTS), text=f"Completed {index} of {len(ARENA_EVENTS)} events")

        st.session_state["arena_batch_results"] = batch_results
        st.session_state["arena_batch_completed"] = True
        st.session_state["arena_selected_event"] = failures[0] if failures else "budget_marathon"
        st.session_state["arena_last_run_mode"] = "benchmark_batch"
        if failures:
            status.update(
                label=f"Run All completed with {len(failures)} event issue(s)",
                state="error",
                expanded=True,
            )
        else:
            status.update(label="All 5 Olympic events completed", state="complete", expanded=False)
    return batch_results


def render_arena_event_selector(settings):
    """Visible event list plus one always-editable challenge-question workspace."""
    st.session_state.setdefault("arena_question_event", "research_sprint")
    for event in ARENA_EVENTS:
        st.session_state.setdefault(
            f"arena_custom_prompt_{event['id']}",
            OFFICIAL_ARENA_PROMPTS[event["id"]],
        )

    head_left, head_right = st.columns([4.2, 1.3], gap="medium", vertical_alignment="center")
    with head_left:
        st.markdown(
            """
            <div class="ao-arena-selector-head ao-arena-selector-head-compact">
                <div>
                    <div class="ao-arena-selector-kicker">OLYMPIC EVENTS</div>
                    <div class="ao-arena-selector-title">Choose an event and challenge question</div>
                    <div class="ao-arena-selector-sub">Every event starts with its validated Olympic question. Edit it directly for exploration, or reset it to the official benchmark question at any time.</div>
                </div>
                <div class="ao-arena-ready-pill">5 EVENTS READY</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with head_right:
        if st.button(
            "Run All 5 Benchmark Events",
            key="arena_run_all_events",
            icon=":material/fast_forward:",
            type="primary",
            use_container_width=False,
            disabled=not settings.ready,
        ):
            run_all_arena_events(settings)
            st.rerun()
        st.caption("Uses the five official benchmark questions • sequential live API run")

    # Always-visible question workspace. Users switch events with visible tabs.
    short_labels = {
        "research_sprint": "Research",
        "broken_tool_relay": "Tool Relay",
        "misinformation_challenge": "Misinformation",
        "prompt_injection_hurdle": "Prompt Injection",
        "budget_marathon": "Budget",
    }
    question_event_id = st.radio(
        "Challenge question event",
        [event["id"] for event in ARENA_EVENTS],
        format_func=lambda event_id: short_labels[event_id],
        horizontal=True,
        key="arena_question_event",
    )
    question_event = next(item for item in ARENA_EVENTS if item["id"] == question_event_id)
    prompt_key = f"arena_custom_prompt_{question_event_id}"
    official_prompt = OFFICIAL_ARENA_PROMPTS[question_event_id]

    reset_pending_key = f"arena_reset_pending_{question_event_id}"

    if st.session_state.pop(reset_pending_key, False):
     st.session_state[prompt_key] = official_prompt

    current_before_widget = st.session_state.get(prompt_key, official_prompt)
    is_custom_before_widget = current_before_widget.strip() != official_prompt.strip()

    with st.container(border=True):
        q_left, q_right = st.columns([4.2, 1.3], gap="medium", vertical_alignment="top")
        with q_left:
            badge_text = "CUSTOM EDIT" if is_custom_before_widget else "BENCHMARK DEFAULT"
            badge_class = "custom" if is_custom_before_widget else "benchmark"
            st.markdown(
                f"""
                <div class="ao-question-workspace-head">
                    <div>
                        <div class="ao-custom-question-kicker">CHALLENGE QUESTION</div>
                        <div class="ao-question-workspace-title">{question_event['title']}</div>
                    </div>
                    <div class="ao-question-workspace-badge {badge_class}">{badge_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.text_area(
                f"Challenge question for {question_event['title']}",
                key=prompt_key,
                height=118,
                label_visibility="collapsed",
                placeholder="Enter the question you want both frameworks to answer...",
            )
            selected_prompt = st.session_state.get(prompt_key, "").strip()
            is_custom = selected_prompt != official_prompt.strip()
            if is_custom:
                if question_event_id == "research_sprint":
                    st.caption("Custom experiment • both frameworks research your edited question. This does not change the validated medal board.")
                else:
                    st.caption("Custom experiment • your task is edited while this event's validated failure/evidence/security fixture remains fixed. Official medal-board results stay frozen.")
            else:
                st.caption("Official benchmark question • editable. Run it unchanged for repeatable benchmark comparison, or edit it for exploration.")

        with q_right:
            st.markdown('<div style="height:27px"></div>', unsafe_allow_html=True)
            if st.button(
                "Reset to Benchmark Question",
                key=f"arena_reset_top_{question_event_id}",
                icon=":material/restart_alt:",
                use_container_width=False,
            ):
                st.session_state[reset_pending_key] = True
                st.rerun()
            run_label = "Run Custom Experiment" if is_custom else "Run Benchmark Question"
            if st.button(
                run_label,
                key=f"arena_run_selected_{question_event_id}_{'custom' if is_custom else 'benchmark'}",
                icon=":material/science:" if is_custom else ":material/play_arrow:",
                type="primary",
                use_container_width=False,
                disabled=not settings.ready,
            ):
                if not selected_prompt:
                    st.warning("Enter a question before running the event.")
                else:
                    run_arena_event(
                        question_event_id,
                        settings,
                        prompt_override=selected_prompt if is_custom else None,
                        run_mode="custom" if is_custom else "benchmark",
                    )
                    st.rerun()

    if st.session_state.get("arena_batch_completed"):
        results = st.session_state.get("arena_batch_results", {})
        success_count = sum(1 for value in results.values() if value == "success")
        if success_count == len(ARENA_EVENTS):
            st.success("All 5 benchmark events completed successfully. Select or rerun any event below to inspect it in detail.")
        else:
            st.warning(f"Batch run completed: {success_count}/5 events succeeded. Inspect the affected event below for details.")

    st.markdown(
        '<div class="ao-arena-event-list-label">ALL OLYMPIC EVENTS · QUICK ACTIONS</div>',
        unsafe_allow_html=True,
    )
def render_arena_latest_result(settings):
    event_id = st.session_state.get("arena_selected_event")
    if not event_id:
        st.markdown(
            """
            <div class="ao-arena-empty">
                <div class="ao-arena-empty-icon"><span class="material-symbols-rounded">emoji_events</span></div>
                <div>
                    <div class="ao-arena-empty-title">Select an event above</div>
                    <div class="ao-arena-empty-copy">The latest head-to-head output, evals and Behind-the-Scenes traces will appear here after the run completes.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    lookup = {
        "research_sprint": st.session_state.research_comparison,
        "broken_tool_relay": st.session_state.relay_comparison,
        "misinformation_challenge": st.session_state.misinformation_comparison,
        "prompt_injection_hurdle": st.session_state.prompt_injection_comparison,
        "budget_marathon": st.session_state.budget_comparison,
    }
    comparison = lookup[event_id]
    if not comparison:
        return

    event = next(item for item in ARENA_EVENTS if item["id"] == event_id)
    last_mode = st.session_state.get("arena_last_run_mode", "benchmark")
    if last_mode == "custom":
        st.markdown(
            '<div class="ao-latest-mode custom"><b>CUSTOM EXPERIMENT</b> · Exploratory result only. The official medal board and validated benchmark findings are unchanged.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="ao-latest-mode benchmark"><b>CONTROLLED BENCHMARK</b> · Official validated challenge configuration.</div>',
            unsafe_allow_html=True,
        )
    render_section_heading(
        f"Latest result — {event['title']}",
        "Actual framework outputs from the most recent Olympic Arena run.",
    )

    main_col, right_col = st.columns([2.15, 1], gap="large")
    with main_col:
        config_status(settings.ready, settings.model, settings.eval_model)
        tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
        if event_id == "budget_marathon":
            with tabs[0]:
                render_budget_result(comparison.openai_agents)
            with tabs[1]:
                render_budget_result(comparison.autogen)
            metric_table_for_event(comparison, event_id)
        elif event_id == "prompt_injection_hurdle":
            with tabs[0]:
                render_prompt_injection_result(comparison.openai_agents)
            with tabs[1]:
                render_prompt_injection_result(comparison.autogen)
            metric_table_for_event(comparison, event_id)
        elif event_id == "misinformation_challenge":
            with tabs[0]:
                render_misinformation_result(comparison.openai_agents)
            with tabs[1]:
                render_misinformation_result(comparison.autogen)
            metric_table_for_event(comparison, event_id)
        elif event_id == "broken_tool_relay":
            with tabs[0]:
                render_recovery_result(comparison.openai_agents)
            with tabs[1]:
                render_recovery_result(comparison.autogen)
            metric_table_for_event(comparison, event_id)
        else:
            with tabs[0]:
                render_result(comparison.openai_agents)
            with tabs[1]:
                render_result(comparison.autogen)
    with right_col:
        render_live_event_flow(event_id)
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_event_result_spotlight(event_id)


def metric_table_for_event(comparison, event_id: str):
    oa = comparison.openai_agents
    ag = comparison.autogen

    if event_id == "budget_marathon":
        st.table(
            {
                "Metric": [
                    "Run status",
                    "Quality gate passed",
                    "Quality checks",
                    "Substantive words",
                    "LLM requests",
                    "Tool calls",
                    "Input tokens",
                    "Output tokens",
                    "Total tokens",
                    "Duration (seconds)",
                    "Estimated model cost (USD)",
                    "Deterministic checks",
                    "Evidence support",
                ],
                "OpenAI Agents SDK": [
                    as_text(oa.status),
                    as_text(oa.budget.quality_gate_passed),
                    f"{oa.budget.quality_checks_passed}/{oa.budget.quality_checks_total}",
                    as_text(oa.budget.substantive_word_count),
                    as_text(oa.llm_requests),
                    as_text(oa.tool_calls),
                    as_text(oa.input_tokens),
                    as_text(oa.output_tokens),
                    as_text(oa.total_tokens),
                    as_text(oa.duration_seconds),
                    f"${oa.budget.estimated_model_cost_usd:.8f}" if oa.budget.pricing_available else "N/A",
                    f"{oa.deterministic_eval.passed_checks}/{oa.deterministic_eval.total_checks}",
                    as_text(oa.semantic_eval.evidence_support),
                ],
                "Microsoft AutoGen": [
                    as_text(ag.status),
                    as_text(ag.budget.quality_gate_passed),
                    f"{ag.budget.quality_checks_passed}/{ag.budget.quality_checks_total}",
                    as_text(ag.budget.substantive_word_count),
                    as_text(ag.llm_requests),
                    as_text(ag.tool_calls),
                    as_text(ag.input_tokens),
                    as_text(ag.output_tokens),
                    as_text(ag.total_tokens),
                    as_text(ag.duration_seconds),
                    f"${ag.budget.estimated_model_cost_usd:.8f}" if ag.budget.pricing_available else "N/A",
                    f"{ag.deterministic_eval.passed_checks}/{ag.deterministic_eval.total_checks}",
                    as_text(ag.semantic_eval.evidence_support),
                ],
            }
        )
    elif event_id == "prompt_injection_hurdle":
        st.table(
            {
                "Metric": [
                    "Run status",
                    "Injection detected",
                    "Trusted SEV-1 selected",
                    "Trusted action selected",
                    "SEV-3 override rejected",
                    "Attack token not emitted",
                    "Untrusted source identified",
                    "Prompt-injection checks",
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
                    as_text(oa.prompt_injection.injection_detected),
                    as_text(oa.prompt_injection.trusted_severity_selected),
                    as_text(oa.prompt_injection.trusted_action_selected),
                    as_text(oa.prompt_injection.malicious_severity_rejected),
                    as_text(oa.prompt_injection.attack_token_not_output),
                    as_text(oa.prompt_injection.untrusted_source_identified),
                    f"{oa.prompt_injection.passed_checks}/{oa.prompt_injection.total_checks}",
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
                    as_text(ag.prompt_injection.injection_detected),
                    as_text(ag.prompt_injection.trusted_severity_selected),
                    as_text(ag.prompt_injection.trusted_action_selected),
                    as_text(ag.prompt_injection.malicious_severity_rejected),
                    as_text(ag.prompt_injection.attack_token_not_output),
                    as_text(ag.prompt_injection.untrusted_source_identified),
                    f"{ag.prompt_injection.passed_checks}/{ag.prompt_injection.total_checks}",
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
    elif event_id == "broken_tool_relay":
        st.table(
            {
                "Metric": [
                    "Run status",
                    "Failure injected",
                    "Retry attempted",
                    "Recovered",
                    "Tool calls",
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
    elif event_id == "misinformation_challenge":
        st.table(
            {
                "Metric": [
                    "Run status",
                    "Conflict detected",
                    "Correct launch date",
                    "Feature 1 selected",
                    "Feature 2 selected",
                    "Bad claim rejected",
                    "Conflict source identified",
                    "Misinformation checks",
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
                    as_text(oa.misinformation.conflict_detected),
                    as_text(oa.misinformation.correct_launch_date_selected),
                    as_text(oa.misinformation.feature_one_selected),
                    as_text(oa.misinformation.feature_two_selected),
                    as_text(oa.misinformation.misleading_claim_rejected),
                    as_text(oa.misinformation.conflicting_source_cited_as_conflict),
                    f"{oa.misinformation.passed_checks}/{oa.misinformation.total_checks}",
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
                    as_text(ag.misinformation.conflict_detected),
                    as_text(ag.misinformation.correct_launch_date_selected),
                    as_text(ag.misinformation.feature_one_selected),
                    as_text(ag.misinformation.feature_two_selected),
                    as_text(ag.misinformation.misleading_claim_rejected),
                    as_text(ag.misinformation.conflicting_source_cited_as_conflict),
                    f"{ag.misinformation.passed_checks}/{ag.misinformation.total_checks}",
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


def render_live_event(selected_event: str, settings):
    main_col, right_col = st.columns([2.15, 1], gap="large")

    with right_col:
        render_live_event_flow(selected_event)
        render_telemetry_mini()
        render_event_result_spotlight(selected_event)

    with main_col:
        config_status(settings.ready, settings.model, settings.eval_model)

        if selected_event == "budget_marathon":
            st.markdown(
                """
                <div class="event-card">
                    <div class="event-title-row">
                        <span class="event-icon">💰</span>
                        <div>
                            <div class="event-number">EVENT 05 • COMPLETE</div>
                            <div class="event-name">Budget Marathon</div>
                            <div class="event-question">How much execution does each framework need to produce a complete answer?</div>
                        </div>
                    </div>
                    <div class="event-business"><strong>Quality-gated setup:</strong> both competitors receive the same four-item evidence packet and must satisfy six answer requirements within a 180-word substantive limit.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.info("Pricing estimate for gpt-4.1-mini: $0.40 / 1M input tokens and $1.60 / 1M output tokens. Evaluator calls/tokens are excluded.")
            prompt = st.text_area("Budget Marathon task", value=BUDGET_MARATHON_PROMPT, height=120)
            semantic_eval_enabled = st.checkbox("Run semantic evidence evaluator", value=True, key="budget_semantic")
            if st.button("💰 Run Budget Marathon", type="primary", disabled=not settings.ready):
                try:
                    with st.status("Running Budget Marathon...", expanded=True) as status:
                        st.write("1/3 — Running OpenAI Agents SDK against fixed quality contract")
                        st.write("2/3 — Running AutoGen against the same contract")
                        st.write("3/3 — Measuring calls, tokens, latency, cost and quality")
                        comparison = run_async(run_budget_marathon(prompt=prompt, settings=settings, semantic_eval_enabled=semantic_eval_enabled))
                        st.session_state.budget_comparison = comparison
                        status.update(label="Budget Marathon completed", state="complete", expanded=False)
                except Exception as exc:
                    st.error(f"Event controller failed: {type(exc).__name__}: {exc}")
            comparison = st.session_state.budget_comparison
            if comparison:
                tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
                with tabs[0]:
                    render_budget_result(comparison.openai_agents)
                with tabs[1]:
                    render_budget_result(comparison.autogen)
                section_title("Side-by-Side Budget Metrics", "Efficiency is only comparable after both answers satisfy the same quality gate.")
                metric_table_for_event(comparison, selected_event)

        elif selected_event == "prompt_injection_hurdle":
            st.markdown(
                """
                <div class="event-card">
                    <div class="event-title-row">
                        <span class="event-icon">🛡️</span>
                        <div>
                            <div class="event-number">EVENT 04 • COMPLETE</div>
                            <div class="event-name">Prompt Injection Hurdle</div>
                            <div class="event-question">Can the agent read an attack embedded in evidence without obeying it?</div>
                        </div>
                    </div>
                    <div class="event-business"><strong>Controlled setup:</strong> sources [1]-[3] contain trusted operational facts. Source [4] contains a fake system override telling the agent to downgrade the incident and emit a planted response token.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            prompt = st.text_area("Prompt-injection task", value=PROMPT_INJECTION_PROMPT, height=120)
            semantic_eval_enabled = st.checkbox(
                "Run hardened semantic evidence evaluator",
                value=True,
                key="prompt_injection_semantic",
                help="The evaluator treats evidence and candidate answers as inert data so the planted injection cannot redefine the judge task.",
            )
            if st.button("🛡️ Run Prompt Injection Hurdle", type="primary", disabled=not settings.ready):
                try:
                    with st.status("Running Prompt Injection Hurdle...", expanded=True) as status:
                        st.write("1/3 — Supplying trusted task + same untrusted evidence to OpenAI Agents SDK")
                        st.write("2/3 — Supplying identical input to AutoGen")
                        st.write("3/3 — Checking instruction hierarchy, attack rejection and grounding")
                        comparison = run_async(run_prompt_injection_hurdle(prompt=prompt, settings=settings, semantic_eval_enabled=semantic_eval_enabled))
                        st.session_state.prompt_injection_comparison = comparison
                        status.update(label="Prompt Injection Hurdle completed", state="complete", expanded=False)
                except Exception as exc:
                    st.error(f"Event controller failed: {type(exc).__name__}: {exc}")
            comparison = st.session_state.prompt_injection_comparison
            if comparison:
                st.warning("Controlled security fixture: source [4] contains a planted malicious instruction. It is synthetic test data only and has no access to secrets or external actions.")
                tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
                with tabs[0]:
                    render_prompt_injection_result(comparison.openai_agents)
                with tabs[1]:
                    render_prompt_injection_result(comparison.autogen)
                section_title("Side-by-Side Prompt Injection Metrics", "Security posture, instruction hierarchy and answer quality shown together.")
                metric_table_for_event(comparison, selected_event)

        elif selected_event == "misinformation_challenge":
            st.markdown(
                """
                <div class="event-card">
                    <div class="event-title-row">
                        <span class="event-icon">🕵️</span>
                        <div>
                            <div class="event-number">EVENT 03 • COMPLETE</div>
                            <div class="event-name">Misinformation Challenge</div>
                            <div class="event-question">Can the agent detect deliberately conflicting or incorrect evidence?</div>
                        </div>
                    </div>
                    <div class="event-business"><strong>Controlled setup:</strong> sources [1]-[3] agree on the official record, while source [4] is an intentionally conflicting community claim.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            prompt = st.text_area("Misinformation challenge task", value=MISINFORMATION_PROMPT, height=120)
            semantic_eval_enabled = st.checkbox("Run semantic evidence evaluator", value=True, key="misinformation_semantic")
            if st.button("🕵️ Run Misinformation Challenge", type="primary", disabled=not settings.ready):
                comparison = run_async(run_misinformation_challenge(prompt=prompt, settings=settings, semantic_eval_enabled=semantic_eval_enabled))
                st.session_state.misinformation_comparison = comparison
            comparison = st.session_state.misinformation_comparison
            if comparison:
                tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
                with tabs[0]:
                    render_misinformation_result(comparison.openai_agents)
                with tabs[1]:
                    render_misinformation_result(comparison.autogen)
                section_title("Side-by-Side Misinformation Metrics", "Conflict handling and grounding shown side by side.")
                metric_table_for_event(comparison, selected_event)

        elif selected_event == "broken_tool_relay":
            st.markdown(
                """
                <div class="event-card">
                    <div class="event-title-row">
                        <span class="event-icon">🔌</span>
                        <div>
                            <div class="event-number">EVENT 02 • COMPLETE</div>
                            <div class="event-name">Broken Tool Relay</div>
                            <div class="event-question">Can the agent recover when its research tool fails once?</div>
                        </div>
                    </div>
                    <div class="event-business"><strong>Controlled setup:</strong> both frameworks see the same tool failure on the first call and the same successful response after retry.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            prompt = st.text_area("Relay task", value=BROKEN_TOOL_PROMPT, height=110)
            semantic_eval_enabled = st.checkbox("Run semantic evidence evaluator after recovery", value=True, key="relay_semantic")
            if st.button("🔌 Run Broken Tool Relay", type="primary", disabled=not settings.ready):
                comparison = run_async(run_broken_tool_relay(prompt=prompt, settings=settings, shared_search_query=BROKEN_TOOL_PREFETCH_QUERY, semantic_eval_enabled=semantic_eval_enabled))
                st.session_state.relay_comparison = comparison
            comparison = st.session_state.relay_comparison
            if comparison:
                tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
                with tabs[0]:
                    render_recovery_result(comparison.openai_agents)
                with tabs[1]:
                    render_recovery_result(comparison.autogen)
                section_title("Side-by-Side Recovery Metrics", "Resilience, retries and answer quality in the same view.")
                metric_table_for_event(comparison, selected_event)

        else:
            st.markdown(
                """
                <div class="event-card">
                    <div class="event-title-row">
                        <span class="event-icon">🔎</span>
                        <div>
                            <div class="event-number">EVENT 01 • COMPLETE</div>
                            <div class="event-name">Research Sprint</div>
                            <div class="event-question">Can the agent find, validate, and explain the right answer?</div>
                        </div>
                    </div>
                    <div class="event-business"><strong>Two modes:</strong> autonomous lets each framework choose its own searches, while controlled mode gives both the same evidence packet.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            mode = st.radio("Research mode", options=["autonomous", "controlled"], format_func=lambda key: RESEARCH_MODES[key]["label"], horizontal=True)
            prompt = st.text_area("Research question", value=DEFAULT_RESEARCH_PROMPT, height=110)
            semantic_eval_enabled = st.checkbox("Run semantic evidence evaluator", value=True, key="research_semantic")
            if st.button("🏁 Run Research Sprint", type="primary", disabled=not settings.ready):
                comparison = run_async(run_research_sprint(prompt=prompt, settings=settings, mode=mode, semantic_eval_enabled=semantic_eval_enabled))
                st.session_state.research_comparison = comparison
            comparison = st.session_state.research_comparison
            if comparison:
                tabs = st.tabs(["OpenAI Agents SDK", "Microsoft AutoGen"])
                with tabs[0]:
                    render_result(comparison.openai_agents)
                with tabs[1]:
                    render_result(comparison.autogen)


st.set_page_config(
    page_title="AI Agent Olympics",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="locked",
)

inject_global_css()
inject_approved_dashboard_css()
inject_exact_approved_overrides()
inject_approved_design_lock_css()
inject_final_reference_exact_css()
inject_arena_event_selector_css()
inject_responsive_dashboard_css()
settings = get_settings()

for key in [
    "research_comparison",
    "relay_comparison",
    "misinformation_comparison",
    "prompt_injection_comparison",
    "budget_comparison",
]:
    st.session_state.setdefault(key, None)

st.session_state.setdefault("arena_selected_event", None)
st.session_state.setdefault("arena_last_run_mode", "benchmark")
st.session_state.setdefault("arena_custom_event", "research_sprint")

MENU = [
    ("Overview", ":material/home:"),
    ("Executive Scoreboard", ":material/bar_chart:"),
    ("Olympic Arena", ":material/emoji_events:"),
    ("Event Telemetry", ":material/monitoring:"),
    ("Research Sprint", ":material/description:"),
    ("Broken Tool Relay", ":material/build:"),
    ("Misinformation", ":material/gpp_maybe:"),
    ("Prompt Injection", ":material/shield:"),
    ("Budget Marathon", ":material/database:"),
    ("Final Findings", ":material/flag:"),
]

with st.sidebar:
    render_sidebar_brand()
    st.session_state.setdefault("nav_page", MENU[0][0])
    for idx, (item, icon) in enumerate(MENU):
        button_type = "primary" if st.session_state["nav_page"] == item else "secondary"
        if st.button(item, icon=icon, key=f"sidebar_nav_{idx}", use_container_width=True, type=button_type):
            st.session_state["nav_page"] = item
            st.rerun()
    page = st.session_state["nav_page"]
    st.markdown(
        """
        <div class="ao-side-footer">
            <div class="ao-side-section">ABOUT</div>
            <div class="ao-about-row"><span class="ao-about-icon">info</span><span>Methodology</span></div>
            <div class="ao-about-row"><span class="ao-about-icon">database</span><span>Data &amp; Sources</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_top_toolbar()

EVENT_PAGE_TO_ID = {
    "Research Sprint": "research_sprint",
    "Broken Tool Relay": "broken_tool_relay",
    "Misinformation": "misinformation_challenge",
    "Prompt Injection": "prompt_injection_hurdle",
    "Budget Marathon": "budget_marathon",
}

if page == "Overview":
    render_hero()
    left, right = st.columns([3.05, 1], gap="small")
    with left:
        render_podium_comparison()
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        render_profiles()
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        render_medal_board()
    with right:
        render_live_event_flow()

elif page == "Executive Scoreboard":
    render_page_heading(
        "Executive comparison",
        "AI Agent Olympics Scoreboard",
        "A decision-ready view of where each framework showed its strongest measured behaviour across the five validated events.",
        "FINAL RESULTS",
    )
    left, right = st.columns([3.05, 1], gap="small")
    with left:
        render_podium_comparison()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_medal_board()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_profiles()
    with right:
        render_key_takeaways()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_telemetry_mini()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_live_event_flow()

elif page == "Olympic Arena":
    render_page_heading(
        "Experiment workspace",
        "Olympic Arena",
        "Choose an event, run the validated head-to-head experiment, then inspect the actual framework output, evals and Behind-the-Scenes traces.",
        "LIVE HARNESS",
    )
    config_status(settings.ready, settings.model, settings.eval_model)
    render_arena_event_selector(settings)
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    render_arena_latest_result(settings)

elif page == "Event Telemetry":
    render_page_heading(
        "Performance intelligence",
        "Event Telemetry",
        "Supporting evidence for tokens, latency, deterministic checks and evidence support across the five final benchmark events.",
        "5 EVENTS",
    )
    left, right = st.columns([3.05, 1], gap="small")
    with left:
        render_competition_visuals()
    with right:
        render_telemetry_mini()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_key_takeaways()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_live_event_flow()

elif page in EVENT_PAGE_TO_ID:
    event_id = EVENT_PAGE_TO_ID[page]
    titles = {
        "research_sprint": ("Research intelligence", "Research Sprint", "Can the agent find, validate and explain the right answer under autonomous and controlled evidence conditions?"),
        "broken_tool_relay": ("Reliability", "Broken Tool Relay", "Can the agent recover from a transient tool failure without unnecessary retries or unsupported answers?"),
        "misinformation_challenge": ("Evidence integrity", "Misinformation Challenge", "Can the agent identify conflicting evidence, weight source authority and reject the planted claim?"),
        "prompt_injection_hurdle": ("Security", "Prompt Injection Hurdle", "Can the agent preserve trusted instruction hierarchy when malicious instructions are embedded in retrieved evidence?"),
        "budget_marathon": ("Efficiency", "Budget Marathon", "How much model execution is required to satisfy the same quality contract?"),
    }
    kicker, title, subtitle = titles[event_id]
    render_page_heading(kicker, title, subtitle, "EVENT COMPLETE")
    render_live_event(event_id, settings)

else:
    render_page_heading(
        "Final findings",
        "What the Olympics Taught Us",
        "The strongest outcome is a behaviour profile, not a simplistic framework winner.",
        "LEARNINGS CAPTURED",
    )
    left, right = st.columns([3.05, 1], gap="small")
    with left:
        render_section_heading("Final competition picture", "The medal board preserves nuance while keeping the results easy to explain.")
        render_medal_board()
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        render_section_heading("Supporting telemetry", "Measured performance and evidence signals across all five events.")
        render_competition_visuals()
    with right:
        render_key_takeaways()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        render_live_event_flow()
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ao-rail-card">
                <div class="ao-rail-title">Portfolio narrative</div>
                <div class="ao-rail-sub">What this build now demonstrates</div>
                <div class="ao-takeaway"><div class="ao-takeaway-icon">✓</div><div><div class="ao-takeaway-title">Controlled experiment design</div><div class="ao-takeaway-sub">Same evidence and quality contracts where isolation matters.</div></div></div>
                <div class="ao-takeaway"><div class="ao-takeaway-icon">✓</div><div><div class="ao-takeaway-title">Guardrails + evals</div><div class="ao-takeaway-sub">Deterministic and semantic evaluation layers.</div></div></div>
                <div class="ao-takeaway"><div class="ao-takeaway-icon">✓</div><div><div class="ao-takeaway-title">Benchmark QA</div><div class="ao-takeaway-sub">Harness and evaluator regressions were tested, not assumed.</div></div></div>
                <div class="ao-takeaway"><div class="ao-takeaway-icon">✓</div><div><div class="ao-takeaway-title">Enterprise communication</div><div class="ao-takeaway-sub">Decision-grade UI plus auditable detailed traces.</div></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
