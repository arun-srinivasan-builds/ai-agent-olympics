import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
            :root {
                --navy: #0B1739;
                --blue: #2563EB;
                --blue-soft: #EEF4FF;
                --gold: #B8892D;
                --gold-soft: #FFF8E7;
                --green: #0F8A5F;
                --green-soft: #EAF8F2;
                --amber: #B7791F;
                --amber-soft: #FFF8E8;
                --red: #B42318;
                --red-soft: #FFF0EF;
                --slate-900: #182230;
                --slate-700: #344054;
                --slate-600: #475467;
                --slate-500: #667085;
                --slate-400: #98A2B3;
                --slate-300: #D0D5DD;
                --slate-200: #EAECF0;
                --slate-100: #F2F4F7;
                --slate-50: #F8FAFC;
                --white: #FFFFFF;
            }

            .stApp {
                background: #F6F8FB;
            }

            .block-container {
                max-width: 1440px;
                padding-top: 1.3rem;
                padding-bottom: 3rem;
            }

            header[data-testid="stHeader"] {
                background: rgba(246, 248, 251, 0.88);
                backdrop-filter: blur(10px);
            }

            #MainMenu, footer {
                visibility: hidden;
            }

            h1, h2, h3, h4, p, div, span, button {
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            .brand-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                margin-bottom: 10px;
            }

            .brand-left {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .brand-mark {
                width: 42px;
                height: 42px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(145deg, #0B1739, #1F3A70);
                color: white;
                font-size: 22px;
                box-shadow: 0 10px 30px rgba(11, 23, 57, 0.18);
            }

            .brand-title {
                color: var(--navy);
                font-size: 19px;
                font-weight: 800;
                letter-spacing: -0.02em;
            }

            .brand-subtitle {
                color: var(--slate-500);
                font-size: 12px;
                margin-top: 2px;
            }

            .live-badge {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                border: 1px solid #B7E4D3;
                background: var(--green-soft);
                color: #087454;
                border-radius: 999px;
                padding: 7px 11px;
                font-size: 12px;
                font-weight: 700;
            }

            .live-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #12B76A;
                display: inline-block;
            }

            .hero {
                border: 1px solid #D7DEE8;
                background:
                    radial-gradient(circle at 86% 18%, rgba(184,137,45,0.14), transparent 24%),
                    radial-gradient(circle at 65% 90%, rgba(37,99,235,0.12), transparent 32%),
                    linear-gradient(135deg, #FFFFFF 0%, #FBFCFE 100%);
                border-radius: 22px;
                padding: 30px 32px;
                box-shadow: 0 16px 42px rgba(16, 24, 40, 0.06);
                margin: 12px 0 18px 0;
            }

            .eyebrow {
                color: var(--blue);
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 0.09em;
                text-transform: uppercase;
                margin-bottom: 9px;
            }

            .hero h1 {
                margin: 0;
                color: var(--navy);
                font-size: clamp(30px, 4vw, 46px);
                line-height: 1.04;
                letter-spacing: -0.04em;
            }

            .hero p {
                color: var(--slate-600);
                font-size: 16px;
                line-height: 1.6;
                max-width: 850px;
                margin: 14px 0 18px 0;
            }

            .hero-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 16px;
            }

            .hero-tag {
                background: white;
                border: 1px solid var(--slate-200);
                border-radius: 999px;
                color: var(--slate-700);
                padding: 7px 10px;
                font-size: 12px;
                font-weight: 650;
            }

            .section-title {
                margin: 24px 0 12px 0;
            }

            .section-title h2 {
                color: var(--navy);
                font-size: 23px;
                margin: 0;
                letter-spacing: -0.025em;
            }

            .section-title p {
                color: var(--slate-500);
                font-size: 13px;
                margin: 4px 0 0 0;
            }

            .metric-card {
                background: white;
                border: 1px solid var(--slate-200);
                border-radius: 16px;
                padding: 17px 18px;
                box-shadow: 0 6px 18px rgba(16, 24, 40, 0.04);
                min-height: 118px;
            }

            .metric-label {
                color: var(--slate-500);
                font-size: 12px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .metric-value {
                color: var(--navy);
                font-size: 28px;
                font-weight: 800;
                margin-top: 8px;
                letter-spacing: -0.03em;
            }

            .metric-note {
                color: var(--slate-500);
                font-size: 12px;
                margin-top: 6px;
                line-height: 1.4;
            }

            .status-chip {
                display: inline-flex;
                align-items: center;
                border-radius: 999px;
                padding: 5px 9px;
                font-size: 11px;
                font-weight: 700;
                border: 1px solid var(--slate-200);
                background: var(--slate-50);
                color: var(--slate-600);
            }

            .status-ready {
                background: var(--blue-soft);
                color: #1D4ED8;
                border-color: #BFDBFE;
            }

            .status-pending {
                background: var(--amber-soft);
                color: #95650E;
                border-color: #F4D69A;
            }

            .competitor-card {
                background: white;
                border: 1px solid var(--slate-200);
                border-radius: 18px;
                padding: 20px;
                min-height: 170px;
                box-shadow: 0 8px 24px rgba(16, 24, 40, 0.045);
            }

            .competitor-kicker {
                color: var(--slate-500);
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.07em;
                font-weight: 800;
            }

            .competitor-name {
                color: var(--navy);
                font-size: 21px;
                font-weight: 800;
                margin-top: 7px;
            }

            .competitor-desc {
                color: var(--slate-600);
                font-size: 13px;
                line-height: 1.5;
                margin: 8px 0 16px 0;
            }

            .event-card {
                background: white;
                border: 1px solid var(--slate-200);
                border-radius: 18px;
                padding: 18px 20px;
                margin-bottom: 12px;
                box-shadow: 0 6px 20px rgba(16, 24, 40, 0.035);
            }

            .event-top {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 12px;
            }

            .event-title-row {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .event-number {
                color: var(--slate-400);
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 0.07em;
            }

            .event-icon {
                width: 38px;
                height: 38px;
                border-radius: 11px;
                background: var(--slate-50);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 19px;
                border: 1px solid var(--slate-200);
            }

            .event-name {
                color: var(--navy);
                font-size: 17px;
                font-weight: 800;
            }

            .event-question {
                color: var(--slate-600);
                font-size: 13px;
                margin-top: 4px;
                line-height: 1.45;
            }

            .event-business {
                background: #FAFBFC;
                border: 1px solid var(--slate-200);
                border-radius: 12px;
                padding: 12px 13px;
                color: var(--slate-600);
                font-size: 12px;
                line-height: 1.5;
                margin-top: 13px;
            }

            .focus-row {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-top: 12px;
            }

            .focus-pill {
                border: 1px solid #D9E2F1;
                background: #F7FAFF;
                color: #35588A;
                border-radius: 999px;
                padding: 5px 8px;
                font-size: 11px;
                font-weight: 650;
            }

            .empty-result {
                border: 1px dashed #CBD5E1;
                background: rgba(255,255,255,0.72);
                border-radius: 18px;
                padding: 26px;
                text-align: center;
                color: var(--slate-500);
            }

            .empty-result strong {
                display: block;
                color: var(--slate-700);
                font-size: 16px;
                margin-bottom: 5px;
            }

            .rule-card {
                background: white;
                border: 1px solid var(--slate-200);
                border-radius: 16px;
                padding: 18px;
            }

            .rule-item {
                display: flex;
                align-items: center;
                gap: 9px;
                color: var(--slate-600);
                font-size: 13px;
                padding: 8px 0;
                border-bottom: 1px solid #F2F4F7;
            }

            .rule-item:last-child {
                border-bottom: none;
            }

            .rule-check {
                color: var(--green);
                font-weight: 900;
            }

            .method-note {
                border-left: 3px solid var(--gold);
                background: var(--gold-soft);
                padding: 14px 16px;
                border-radius: 0 12px 12px 0;
                color: #684F1F;
                font-size: 13px;
                line-height: 1.55;
            }

            div[data-testid="stHorizontalBlock"] {
                gap: 0.8rem;
            }

            div[data-testid="stButton"] button {
                border-radius: 10px;
                font-weight: 750;
                min-height: 40px;
            }

            div[data-testid="stButton"] button[kind="primary"] {
                background: var(--blue);
                border-color: var(--blue);
            }

            div[data-testid="stRadio"] > div {
                background: white;
                border: 1px solid var(--slate-200);
                padding: 5px;
                border-radius: 12px;
                width: fit-content;
            }

            div[data-testid="stRadio"] label {
                padding: 4px 8px;
            }

            @media (max-width: 700px) {
                .hero {
                    padding: 23px 20px;
                }

                .hero h1 {
                    font-size: 32px;
                }

                .brand-subtitle {
                    display: none;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def competitor_card(name: str, status: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="competitor-card">
            <div class="competitor-kicker">Competitor</div>
            <div class="competitor-name">{name}</div>
            <div class="competitor-desc">{description}</div>
            <span class="status-chip status-pending">{status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def event_card(event: dict) -> None:
    focus = "".join(
        f'<span class="focus-pill">{item}</span>' for item in event["technical_focus"]
    )
    st.markdown(
        f"""
        <div class="event-card">
            <div class="event-top">
                <div class="event-title-row">
                    <span class="event-icon">{event["icon"]}</span>
                    <div>
                        <div class="event-number">EVENT {event["number"]}</div>
                        <div class="event-name">{event["name"]}</div>
                        <div class="event-question">{event["question"]}</div>
                    </div>
                </div>
                <span class="status-chip status-ready">{event["status"]}</span>
            </div>
            <div class="event-business"><strong>Why it matters:</strong> {event["business_value"]}</div>
            <div class="focus-row">{focus}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_result(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="empty-result">
            <strong>{title}</strong>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
