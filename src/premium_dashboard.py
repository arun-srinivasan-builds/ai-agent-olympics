from __future__ import annotations

import base64
import html
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from src.ui import get_final_benchmark_df


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "ui"


def _data_uri(filename: str, mime: str | None = None) -> str:
    path = ASSET_DIR / filename
    if mime is None:
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def inject_approved_dashboard_css() -> None:
    st.markdown(
        """
        <style>
        @import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700;800&display=swap");
        :root{
            --ao-bg:#F4F7FB;
            --ao-sidebar:#0E2548;
            --ao-sidebar-deep:#0A1D39;
            --ao-sidebar-soft:#18365F;
            --ao-blue:#2468F2;
            --ao-blue-soft:#EAF1FF;
            --ao-purple:#6D4BF6;
            --ao-purple-soft:#F0ECFF;
            --ao-navy:#102857;
            --ao-text:#1C2E50;
            --ao-muted:#6A7B99;
            --ao-border:#DCE5F1;
            --ao-card:#FFFFFF;
            --ao-green:#13A66B;
            --ao-green-soft:#E8F8F1;
            --ao-gold:#EFAF16;
            --ao-gold-soft:#FFF6D7;
            --ao-silver:#98A8BF;
            --ao-bronze:#C2773C;
            --ao-amber:#F59E0B;
            --ao-red:#E5484D;
        }

        html, body, [class*="css"], .stApp,
        p,div,span,label,button,input,textarea,select{
            font-family:"Manrope", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }
        h1,h2,h3,h4,h5,h6{
            font-family:"Instrument Serif", Georgia, serif !important;
            font-weight:400 !important;
            letter-spacing:-.02em;
        }
        code,pre,kbd,samp,.ao-search-shortcut,.ao-kpi-value,.ao-metric-main,.ao-framework-badge,.ao-profile-badge{
            font-family:"IBM Plex Mono", "SFMono-Regular", Consolas, monospace !important;
        }
        [data-testid="stIconMaterial"], .material-symbols-rounded, .material-symbols-outlined{
            font-family:"Material Symbols Rounded" !important;
        }

        .stApp{ background:var(--ao-bg); color:var(--ao-text); }
        #MainMenu, footer{ visibility:hidden !important; }
        header[data-testid="stHeader"]{ display:none !important; }
        [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"]{ display:none !important; }

        /* fixed sidebar - never collapses */
        section[data-testid="stSidebar"]{
            width:240px !important;
            min-width:240px !important;
            max-width:240px !important;
            background:linear-gradient(180deg,var(--ao-sidebar) 0%, var(--ao-sidebar-deep) 100%);
            border-right:1px solid #18345C;
        }
        section[data-testid="stSidebar"] > div{
            width:240px !important;
            padding:0 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{
            padding:0 10px 16px !important;
        }
        section[data-testid="stSidebar"] *{ color:#E5ECF8; }
        section[data-testid="stSidebar"] hr{ border-color:#25466D !important; opacity:.7; }

        .block-container{
            max-width:none !important;
            padding:0 18px 36px 18px !important;
        }

        /* sidebar brand */
        .ao-sidebar-brand{
            display:flex; gap:12px; align-items:center; padding:18px 10px 14px;
        }
        .ao-trophy{
            width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center;
            color:#F8D56A; font-size:28px; background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
        }
        .ao-sidebar-title{ color:#FFF; font-size:17px; font-weight:800; line-height:1.06; letter-spacing:-.01em; }
        .ao-sidebar-sub{ color:#92A7C8; font-size:9px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin:0 10px 14px; }
        .ao-side-section{ color:#AFC2DD !important; font-size:10px; font-weight:850; letter-spacing:.12em; text-transform:uppercase; margin:14px 9px 6px; }
        .ao-side-footer{ margin:20px 10px 0; padding-top:14px; border-top:1px solid #35547C; color:#D7E3F4 !important; font-size:11.5px; font-weight:600; line-height:1.95; }
        .ao-side-footer div{ color:#D7E3F4 !important; opacity:1 !important; }

        section[data-testid="stSidebar"] div[data-testid="stRadio"]{
            background:transparent !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stRadio"] > div{
            gap:3px !important;
            background:transparent !important;
            border:0 !important;
            box-shadow:none !important;
            padding:0 !important;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]{
            min-height:42px; border-radius:8px; padding:9px 10px !important; margin:1px 0;
            transition:.15s ease; width:100%; background:transparent !important; opacity:1 !important;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child{ display:none !important; }
        section[data-testid="stSidebar"] label[data-baseweb="radio"] p,
        section[data-testid="stSidebar"] label[data-baseweb="radio"] span{
            color:#F3F7FD !important; font-size:13px !important; font-weight:650 !important;
            line-height:1.25 !important; opacity:1 !important;
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover{ background:#193B66 !important; }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover p,
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover span{ color:#FFFFFF !important; }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked){
            background:#1F66F2 !important; box-shadow:0 5px 14px rgba(31,102,242,.28);
        }
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p,
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) span{
            color:#FFFFFF !important; font-weight:800 !important;
        }

        /* app top bar */
        .ao-topbar{
            height:50px; display:flex; align-items:center; justify-content:space-between;
            background:#FFF; border-bottom:1px solid var(--ao-border); margin:0 -18px 0 -18px; padding:0 22px;
            box-shadow:0 1px 3px rgba(17,38,78,.035); position:sticky; top:0; z-index:40;
        }
        .ao-search{
            width:470px; height:34px; border:1px solid #D9E3F0; border-radius:8px; background:#F8FAFD;
            display:flex; align-items:center; gap:9px; padding:0 12px; color:#8394AF; font-size:11px;
        }
        .ao-search-shortcut{ margin-left:auto; padding:2px 6px; border-radius:5px; background:#EEF3F9; color:#9AA8BB; font-size:9px; }
        .ao-top-actions{ display:flex; align-items:center; gap:8px; }
        .ao-top-pill{ height:34px; border:1px solid #D9E3F0; background:#FFF; border-radius:8px; padding:0 10px; display:flex; align-items:center; gap:7px; color:#4C6285; font-size:10.5px; font-weight:600; }
        .ao-top-circle{ width:27px; height:27px; border-radius:50%; background:#14366E; color:#FFF; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:800; }

        /* hero */
        .ao-hero{
            position:relative; min-height:196px; overflow:hidden; margin:0 -18px 12px -18px; padding:24px 28px 20px;
            background:linear-gradient(100deg,#F7FBFF 0%,#F8FBFF 44%,#EAF3FF 100%); border-bottom:1px solid #DCE5F1;
        }
        .ao-hero::after{
            content:""; position:absolute; inset:0 0 0 auto; width:48%; background-image:var(--ao-hero-image);
            background-size:cover; background-position:right center; opacity:.96; pointer-events:none;
        }
        .ao-hero-fade{ position:absolute; top:0; bottom:0; left:38%; width:38%; z-index:1; background:linear-gradient(90deg,#F8FBFF 0%,rgba(248,251,255,.96) 34%,rgba(248,251,255,0) 100%); }
        .ao-hero-content{ position:relative; z-index:2; width:67%; }
        .ao-hero-kicker{ color:#1B4D9B; font-size:10px; font-weight:800; letter-spacing:.09em; text-transform:uppercase; margin-bottom:8px; }
        .ao-hero-title{ color:#0D2A5F; font-family:"Instrument Serif", Georgia, serif !important; font-size:39px; line-height:1.02; font-weight:400; letter-spacing:-.025em; margin-bottom:6px; }
        .ao-hero-subtitle{ color:#546D96; font-size:19px; line-height:1.18; font-weight:700; letter-spacing:-.01em; margin-bottom:8px; }
        .ao-hero-copy{ color:#5F7394; font-size:12.5px; line-height:1.48; max-width:760px; }
        .ao-hero-chip{ position:absolute; z-index:3; top:16px; right:26px; color:#3F5E8E; background:rgba(255,255,255,.78); border:1px solid #D7E4F2; border-radius:8px; padding:6px 10px; font-size:9.5px; font-weight:800; letter-spacing:.03em; }

        .ao-grid-main{ display:grid; grid-template-columns:minmax(0,3.05fr) minmax(310px,1fr); gap:12px; align-items:start; }
        .ao-stack{ display:flex; flex-direction:column; gap:10px; }

        /* cards */
        .ao-card{ background:#FFF; border:1px solid var(--ao-border); border-radius:10px; box-shadow:0 3px 10px rgba(19,49,95,.035); }
        .ao-card-head{ display:flex; justify-content:space-between; align-items:flex-start; padding:14px 16px 9px; }
        .ao-card-title{ color:#153368; font-family:"Instrument Serif", Georgia, serif !important; font-size:19px; font-weight:400; letter-spacing:-.01em; }
        .ao-card-sub{ color:#7586A2; font-size:10.5px; margin-top:3px; line-height:1.4; }

        /* podium */
        .ao-podium-card{ background:#FFF; border:1px solid var(--ao-border); border-radius:10px; overflow:hidden; box-shadow:0 3px 10px rgba(19,49,95,.04); }
        .ao-podium-row{ display:grid; grid-template-columns:1fr 250px 1fr; align-items:center; min-height:175px; padding:14px 18px 4px; gap:12px; }
        .ao-competitor{ display:grid; grid-template-columns:84px 1fr; align-items:center; gap:12px; position:relative; }
        .ao-competitor.right{ grid-template-columns:1fr 96px; text-align:left; }
        .ao-competitor.right .ao-avatar{ order:2; }
        .ao-avatar{ width:86px; height:92px; object-fit:cover; border-radius:50%; background:#EEF4FF; }
        .ao-team-avatar{ width:102px; height:92px; object-fit:cover; border-radius:50%; background:#EEF4FF; }
        .ao-framework-badge{ position:absolute; top:-4px; left:-2px; min-width:48px; height:24px; padding:0 8px; border-radius:999px; display:flex; align-items:center; justify-content:center; font-size:8px; letter-spacing:.06em; font-weight:850; background:#EAF1FF; color:#245FBF; border:1px solid #CFE0FF; box-shadow:0 2px 6px rgba(36,104,242,.08); }
        .ao-competitor.right .ao-framework-badge{ left:auto; right:0; background:#F1ECFF; color:#6D4BF6; border-color:#DDD3FF; box-shadow:0 2px 6px rgba(109,75,246,.08); }
        .ao-headtohead{ width:220px; height:142px; margin:auto; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:16px; border:1px solid #E2EAF5; background:linear-gradient(180deg,#FFFFFF 0%,#F7FAFF 100%); box-shadow:inset 0 0 0 1px rgba(255,255,255,.8),0 5px 16px rgba(25,58,107,.05); }
        .ao-headtohead-laurel{ color:#E8AE22; font-size:26px; line-height:1; }
        .ao-headtohead-title{ color:#12326B; font-size:14px; font-weight:900; letter-spacing:.08em; margin-top:8px; }
        .ao-headtohead-sub{ color:#7586A2; font-size:9px; margin-top:4px; }
        .ao-headtohead-pair{ display:grid; grid-template-columns:1fr 1fr; gap:6px; width:84%; margin-top:11px; }
        .ao-headtohead-pair span{ border:1px solid #DDE6F3; border-radius:7px; padding:5px 4px; font-size:8px; font-weight:800; text-align:center; color:#496486; background:#FFF; }
        /* neutral dual podium: equal competitor plinths, no first/second ranking */
        .ao-dual-podium{ position:relative; height:142px; display:flex; align-items:flex-end; justify-content:center; gap:8px; padding:26px 8px 10px; }
        .ao-dual-podium::before{ content:""; position:absolute; left:50%; bottom:20px; width:150px; height:86px; transform:translateX(-50%); background:radial-gradient(circle at 50% 16%,rgba(239,175,22,.25),rgba(239,175,22,0) 70%); pointer-events:none; }
        .ao-podium-torch{ position:absolute; top:0; left:50%; transform:translateX(-50%); display:flex; flex-direction:column; align-items:center; z-index:4; }
        .ao-podium-flame{ font-size:31px; line-height:1; filter:drop-shadow(0 4px 7px rgba(239,175,22,.26)); }
        .ao-podium-event-label{ margin-top:2px; padding:3px 8px; border-radius:999px; background:#FFF8E2; border:1px solid #F2D987; color:#8A6300; font-size:7.5px; font-weight:850; letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }
        .ao-podium-base{ position:absolute; bottom:5px; left:50%; transform:translateX(-50%); width:230px; height:14px; border-radius:6px 6px 3px 3px; background:linear-gradient(180deg,#DCE5F2 0%,#B9C9DE 100%); box-shadow:0 5px 12px rgba(16,40,87,.10); z-index:1; }
        .ao-podium-plinth{ position:relative; z-index:2; width:102px; height:72px; border:1px solid #D8E2F0; border-bottom:3px solid #BFCDE1; border-radius:9px 9px 4px 4px; background:linear-gradient(180deg,#FFFFFF 0%,#F2F6FC 100%); box-shadow:0 8px 18px rgba(16,40,87,.08),inset 0 1px 0 #FFF; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:8px 6px; }
        .ao-podium-plinth.openai{ border-top:4px solid #2D6DF6; }
        .ao-podium-plinth.autogen{ border-top:4px solid #6D4BF6; }
        .ao-podium-type{ font-family:"IBM Plex Mono",monospace !important; font-size:7.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:#7184A5; }
        .ao-podium-name{ margin-top:4px; color:#17376E; font-size:10px; font-weight:850; line-height:1.15; }
        .ao-podium-caption{ position:absolute; bottom:-13px; left:50%; transform:translateX(-50%); color:#657A9B; font-size:7.5px; font-weight:700; white-space:nowrap; }
        .ao-comp-name{ font-family:"Instrument Serif", Georgia, serif !important; color:#102C63; font-size:18px; line-height:1.03; font-weight:850; letter-spacing:-.02em; }
        .ao-comp-mode{ color:#5871A0; font-size:9px; font-weight:800; letter-spacing:.05em; text-transform:uppercase; margin-top:8px; }
        .ao-comp-tagline{ color:#415C89; font-size:11px; margin-top:9px; }
        .ao-podium-img{ width:220px; height:150px; object-fit:contain; display:block; margin:auto; }
        .ao-metric-strip{ display:grid; grid-template-columns:repeat(8,1fr); border-top:1px solid #E6EDF6; background:#FBFCFE; }
        .ao-metric{ padding:10px 11px; min-height:62px; border-right:1px solid #E9EFF7; }
        .ao-metric:last-child{ border-right:none; }
        .ao-metric-main{ color:#153A7A; font-size:13px; font-weight:800; }
        .ao-metric-label{ color:#8290A9; font-size:8.5px; text-transform:uppercase; letter-spacing:.05em; margin-top:3px; }

        /* profiles */
        .ao-profile-grid{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }
        .ao-profile{ background:#FFF; border:1px solid var(--ao-border); border-radius:10px; padding:14px 16px; min-height:175px; position:relative; }
        .ao-profile-badge{ position:absolute; right:12px; top:11px; min-width:58px; height:24px; padding:0 8px; border-radius:999px; display:flex; align-items:center; justify-content:center; font-size:8px; letter-spacing:.05em; font-weight:850; color:#245FBF; background:#EAF1FF; border:1px solid #CFE0FF; }
        .ao-profile-badge.silver{ color:#6D4BF6; background:#F1ECFF; border-color:#DDD3FF; }
        .ao-profile-title{ font-family:"Instrument Serif", Georgia, serif !important; color:#12326B; font-size:15px; font-weight:800; }
        .ao-profile-sub{ color:#667A9D; font-size:10.5px; line-height:1.45; margin-top:4px; margin-bottom:9px; max-width:88%; }
        .ao-profile-list{ list-style:none; margin:0; padding:0; display:grid; gap:7px; }
        .ao-profile-list li{ color:#35527F; font-size:11.5px; display:flex; gap:8px; align-items:center; }
        .ao-profile-icon{ color:#245FBE; font-size:15px; width:18px; text-align:center; }

        /* medal board */
        .ao-medal-board{ background:#FFF; border:1px solid var(--ao-border); border-radius:10px; overflow:hidden; }
        .ao-medal-head{ display:flex; justify-content:space-between; align-items:center; padding:11px 14px 8px; }
        .ao-medal-title{ color:#153368; font-size:15px; font-weight:800; }
        .ao-medal-title span{ color:#EAA713; margin-right:7px; }
        .ao-medal-sub{ color:#788AA7; font-size:9.8px; margin-top:2px; }
        .ao-medal-legend{ display:flex; gap:10px; color:#687B9B; font-size:9px; align-items:center; }
        .ao-medal-dot{ width:18px; height:18px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; color:#FFF; font-size:9px; font-weight:800; margin-right:4px; }
        .ao-medal-dot.gold{ background:#ECAF12; } .ao-medal-dot.silver{ background:#99A8BD; } .ao-medal-dot.bronze{ background:#C17A40; }
        .ao-medal-table{ width:100%; border-collapse:collapse; }
        .ao-medal-table th{ background:#F3F6FB; color:#183A70; font-size:10px; text-align:left; padding:6px 9px; border-top:1px solid #E6ECF4; border-bottom:1px solid #E6ECF4; }
        .ao-medal-table th:not(:first-child), .ao-medal-table td:not(:first-child){ text-align:center; }
        .ao-medal-table td{ color:#385477; font-size:10.5px; padding:6px 9px; border-bottom:1px solid #EEF2F7; }
        .ao-medal-table tr:last-child td{ border-bottom:none; }
        .ao-medal-chip{ display:inline-flex; align-items:center; gap:5px; border-radius:999px; padding:3px 7px; font-size:9px; font-weight:700; background:#F7F9FC; border:1px solid #E2E8F0; }
        .ao-medal-chip.gold{ color:#8A6500; background:#FFF7D9; border-color:#F3D46C; }
        .ao-medal-chip.shared{ color:#1D5B8E; background:#EEF6FF; border-color:#C8DFF8; }

        /* right rail */
        .ao-rail-card{ background:#FFF; border:1px solid var(--ao-border); border-radius:10px; padding:13px 14px; box-shadow:0 3px 10px rgba(19,49,95,.035); }
        .ao-rail-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:2px; }
        .ao-rail-title{ font-family:"Instrument Serif", Georgia, serif !important; color:#153368; font-size:16px; font-weight:800; }
        .ao-live-pill{ color:#0C8E5D; background:#E9F8F2; border-radius:8px; padding:5px 9px; font-size:9px; font-weight:800; }
        .ao-rail-sub{ color:#7C8CA7; font-size:10px; margin-bottom:8px; }
        .ao-flow-item{ display:grid; grid-template-columns:30px 1fr auto; gap:8px; align-items:center; padding:8px 4px; border-top:1px solid #EDF2F7; }
        .ao-flow-item:first-of-type{ border-top:none; }
        .ao-flow-icon{ width:28px; height:28px; border-radius:7px; display:flex; align-items:center; justify-content:center; background:#EEF4FF; color:#2468F2; font-size:15px; }
        .ao-flow-icon.purple{ background:#F1ECFF; color:#7A43EA; } .ao-flow-icon.red{ background:#FFF0F1; color:#E5484D; } .ao-flow-icon.amber{ background:#FFF5DE; color:#E79A12; } .ao-flow-icon.green{ background:#E9F8F2; color:#12A16F; }
        .ao-flow-name{ color:#18386D; font-size:10.5px; font-weight:750; }
        .ao-flow-nodes{ display:flex; align-items:center; gap:4px; margin-top:5px; }
        .ao-node{ width:8px; height:8px; border-radius:50%; background:#D4DFF0; border:2px solid #EDF3FB; box-shadow:0 0 0 1px #D7E2F3; }
        .ao-node.on{ background:#2D6DF6; box-shadow:0 0 0 1px #BFD3FF; }
        .ao-line{ width:14px; height:1px; background:#C8D5E8; }
        .ao-flow-status{ border-radius:7px; padding:4px 7px; font-size:8.5px; font-weight:800; color:#14845F; background:#EAF8F2; }

        .ao-takeaway{ display:grid; grid-template-columns:26px 1fr; gap:8px; align-items:flex-start; padding:8px 3px; border-top:1px solid #EDF2F7; }
        .ao-takeaway:first-of-type{ border-top:none; }
        .ao-takeaway-icon{ font-size:18px; color:#2D6DF6; }
        .ao-takeaway-title{ color:#1A386C; font-size:10.5px; font-weight:750; }
        .ao-takeaway-sub{ color:#7A8BA8; font-size:9px; margin-top:1px; line-height:1.35; }

        /* event pages */
        .ao-page-head{ display:flex; justify-content:space-between; align-items:flex-end; gap:16px; margin:14px 0 12px; }
        .ao-page-kicker{ color:#245FBF; font-size:9px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
        .ao-page-title{ color:#102C63; font-family:"Instrument Serif", Georgia, serif !important; font-size:31px; font-weight:400; line-height:1.03; margin-top:4px; }
        .ao-page-sub{ color:#6A7B99; font-size:11.5px; margin-top:5px; max-width:820px; line-height:1.45; }
        .ao-page-status{ color:#245FBF; background:#EDF3FF; border:1px solid #D1E0FF; border-radius:7px; padding:6px 8px; font-size:8.5px; font-weight:800; }

        .ao-kpi-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }
        .ao-kpi{ background:#FFF; border:1px solid var(--ao-border); border-radius:9px; padding:10px 12px; min-height:78px; }
        .ao-kpi-label{ color:#7585A0; font-size:8.5px; font-weight:800; letter-spacing:.05em; text-transform:uppercase; }
        .ao-kpi-value{ color:#153A7A; font-size:22px; font-weight:850; margin-top:6px; }
        .ao-kpi-note{ color:#8794A8; font-size:8.5px; margin-top:2px; }

        .ao-section-title{ color:#153368; font-family:"Instrument Serif", Georgia, serif !important; font-size:22px; font-weight:400; margin:18px 0 3px; }
        .ao-section-sub{ color:#7A8BA6; font-size:10px; margin-bottom:8px; }

        /* native streamlit components */
        div[data-testid="stButton"] button{ border-radius:8px !important; font-size:11px !important; font-weight:750 !important; min-height:34px !important; height:34px !important; padding:0 14px !important; }
        div[data-testid="stButton"] button[kind="primary"]{ background:#2468F2 !important; border-color:#2468F2 !important; }
        /* Arena/main workspace actions stay compact; sidebar keeps its own approved sizing below. */
        section[data-testid="stMain"] div[data-testid="stButton"]{ width:max-content !important; max-width:100% !important; }
        section[data-testid="stMain"] div[data-testid="stButton"] button{ width:auto !important; min-width:0 !important; white-space:nowrap !important; }
        div[data-testid="stTextArea"] textarea, div[data-baseweb="input"] input{ border-radius:8px !important; border-color:#D9E2EE !important; font-size:11px !important; }
        div[data-testid="stExpander"]{ border:1px solid #DDE5EF !important; border-radius:8px !important; background:#FFF !important; }
        div[data-testid="stTabs"] button{ font-size:11px !important; }
        div[data-testid="stTabs"] button[aria-selected="true"]{ color:#2468F2 !important; border-bottom-color:#2468F2 !important; }
        .stAlert{ border-radius:8px !important; }

        @media(max-width:1200px){
            .ao-grid-main{ grid-template-columns:1fr; }
            .ao-podium-row{ grid-template-columns:1fr; text-align:center; }
            .ao-competitor,.ao-competitor.right{ grid-template-columns:86px 1fr; text-align:left; }
            .ao-competitor.right .ao-avatar{ order:0; }
            .ao-metric-strip{ grid-template-columns:repeat(4,1fr); }
            .ao-hero-content{ width:78%; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def inject_exact_approved_overrides() -> None:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"]{width:290px !important;min-width:290px !important;max-width:290px !important;background:linear-gradient(180deg,#102B55 0%,#092443 100%) !important;}
        section[data-testid="stSidebar"] > div{width:290px !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding:0 8px 18px !important;}
        .block-container{padding:0 16px 34px 16px !important;}
        .ao-sidebar-brand{padding:22px 14px 12px;gap:14px;}
        .ao-trophy{width:64px;height:64px;font-size:38px;border:none;background:transparent;position:relative;}
        .ao-trophy::before{content:"❧";position:absolute;left:-5px;top:12px;color:#F5D25E;font-size:29px;transform:rotate(-35deg);}
        .ao-trophy::after{content:"❧";position:absolute;right:-5px;top:12px;color:#F5D25E;font-size:29px;transform:scaleX(-1) rotate(-35deg);}
        .ao-sidebar-title{font-family:"Manrope",sans-serif !important;font-size:24px;font-weight:800;line-height:1.05;}
        .ao-sidebar-sub{font-size:11px;margin:2px 15px 20px;letter-spacing:.18em;color:#9FB2D0;}
        section[data-testid="stSidebar"] label[data-baseweb="radio"]{min-height:48px;border-radius:7px;padding:11px 13px !important;margin:2px 0;}
        section[data-testid="stSidebar"] label[data-baseweb="radio"] p, section[data-testid="stSidebar"] label[data-baseweb="radio"] span{font-size:15px !important;font-weight:550 !important;color:#E8F0FC !important;}
        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked){background:linear-gradient(90deg,#1877F2,#1764DB) !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"]{margin:2px 0 !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button{width:100% !important;min-height:48px !important;border-radius:7px !important;border:none !important;box-shadow:none !important;padding:0 14px !important;justify-content:flex-start !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]{background:transparent !important;color:#E8F0FC !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover{background:#183B67 !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(90deg,#1877F2,#1764DB) !important;color:#FFF !important;box-shadow:0 5px 14px rgba(31,102,242,.24) !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button p{font-family:"Manrope",sans-serif !important;font-size:15px !important;font-weight:600 !important;text-align:left !important;color:inherit !important;width:100% !important;}
        .ao-side-footer{font-size:13px;line-height:2.35;margin-top:25px;padding-top:18px;}
        .ao-side-section{font-size:10px;margin:14px 0 4px;}
        .ao-topbar-approved{height:44px;margin:0 -16px;padding:0 18px;background:#FFF;border-bottom:1px solid #DCE5F1;box-shadow:none;}
        .ao-topbar-brandline{display:flex;align-items:center;gap:32px;}
        .ao-topbar-app{font-size:18px;font-weight:800;color:#102857;}
        .ao-topbar-context{font-size:11px;letter-spacing:.13em;color:#526D9E;font-weight:650;}
        .ao-topbar-date{font-size:13px;color:#16346B;font-weight:650;}
        .ao-hero-approved{min-height:198px;margin:0 0 16px;padding:16px 22px 15px;border:1px solid #D7E2F0;border-radius:10px;background:linear-gradient(100deg,#F8FBFF 0%,#F4F9FF 47%,#EAF3FF 100%);}
        .ao-hero-approved::after{width:53%;background-position:right center;}
        .ao-hero-approved .ao-hero-fade{left:36%;width:38%;}
        .ao-hero-approved .ao-hero-content{width:72%;padding-left:12px;border-left:4px solid #2472F4;}
        .ao-hero-approved .ao-hero-kicker{font-size:12px;letter-spacing:.13em;margin-bottom:12px;color:#2A4F87;}
        .ao-hero-approved .ao-hero-title{font-family:"Manrope",sans-serif !important;font-size:49px;line-height:1.03;font-weight:800 !important;color:#09285D;letter-spacing:-.035em;margin-bottom:6px;}
        .ao-hero-approved .ao-hero-subtitle{font-family:"Manrope",sans-serif !important;font-size:34px;line-height:1.05;font-weight:800;color:#2667D8;letter-spacing:-.035em;margin:0;}
        .ao-podium-card-approved{border-radius:10px;box-shadow:0 2px 8px rgba(19,49,95,.04);}
        .ao-podium-row-approved{grid-template-columns:minmax(0,1fr) 210px minmax(0,1fr);min-height:222px;padding:0;gap:0;background:#FFF;}
        .ao-competitor-panel{height:222px;padding:28px 22px;display:flex;align-items:center;border-top:5px solid #D6A014;}
        .ao-competitor-panel.autogen{border-top-color:#9AA8B8;}
        .ao-competitor-inner{display:grid;grid-template-columns:120px 1fr;gap:16px;align-items:center;width:100%;}
        .ao-competitor-inner.autogen{grid-template-columns:128px 1fr;}
        .ao-approved-avatar{width:116px;height:116px;border-radius:50%;object-fit:cover;background:#EEF5FF;}
        .ao-approved-team-avatar{width:128px;height:116px;border-radius:50%;object-fit:cover;background:#EEF5FF;}
        .ao-comp-name-approved{font-family:"Manrope",sans-serif !important;font-size:22px;line-height:1.05;font-weight:800;}
        .ao-comp-mode{font-size:10px;margin-top:8px;}
        .ao-comp-tagline{font-size:13px;margin-top:18px;color:#1A3768;}
        .ao-approved-podium-wrap{height:222px;display:flex;align-items:flex-end;justify-content:center;overflow:visible;background:linear-gradient(180deg,#FFFFFF,#FBFCFF);}
        .ao-approved-podium-img{width:230px;height:188px;object-fit:contain;object-position:center bottom;transform:scale(1.05);}
        .ao-metric-strip-approved .ao-metric{min-height:64px;padding:10px 12px;}
        .ao-metric-strip-approved .ao-metric-main{font-size:14px;}
        .ao-metric-strip-approved .ao-metric-label{font-size:8.5px;}
        .ao-profile-grid-approved{gap:14px;}
        .ao-profile-approved{min-height:190px;padding:17px 20px;}
        .ao-profile-approved .ao-profile-title{font-family:"Manrope",sans-serif !important;font-size:18px;font-weight:800;}
        .ao-profile-approved .ao-profile-sub{font-size:12px;max-width:100%;margin:4px 0 12px;}
        .ao-profile-approved .ao-profile-list{gap:10px;}
        .ao-profile-approved .ao-profile-list li{font-size:14px;color:#1F4479;}
        .ao-profile-approved .ao-profile-icon{font-size:17px;}
        .ao-medal-board-approved .ao-medal-head{padding:10px 14px 8px;}
        .ao-medal-board-approved .ao-medal-title{font-size:18px;}
        .ao-medal-board-approved .ao-medal-sub{font-size:11px;}
        .ao-medal-board-approved .ao-medal-legend{font-size:10px;}
        .ao-medal-board-approved .ao-medal-table th{font-size:12px;padding:6px 10px;}
        .ao-medal-board-approved .ao-medal-table td{font-size:12px;padding:5px 10px;}
        .ao-medal-value{display:inline-flex;align-items:center;gap:8px;font-size:12px;color:#19396C;}
        .ao-medal-rank{width:19px;height:19px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:#FFF;font-weight:800;font-size:10px;}
        .ao-medal-rank.gold{background:#E1A800;} .ao-medal-rank.silver{background:#98A7BA;}
        .ao-live-flow-approved{padding:14px 12px 12px;}
        .ao-live-flow-approved .ao-rail-title{font-family:"Manrope",sans-serif !important;font-size:18px;font-weight:800;}
        .ao-live-flow-approved .ao-rail-sub{font-size:11px;margin-top:2px;}
        .ao-live-pill{padding:5px 10px;font-size:10px;}
        .ao-flow-card{border:1px solid #DCE5F0;border-radius:9px;background:#FFF;padding:10px 10px 8px;margin-top:10px;}
        .ao-flow-card-title{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:800;color:#17376E;}
        .ao-flow-card-icon{width:25px;height:25px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;background:#EAF2FF;}
        .ao-flow-ready{margin-left:auto;color:#0D9D68;background:#E8F8F1;border-radius:999px;padding:3px 7px;font-size:8px;}
        .ao-flow-stages{display:flex;align-items:flex-start;justify-content:space-between;margin-top:10px;}
        .ao-flow-stage{display:flex;flex-direction:column;align-items:center;min-width:43px;}
        .ao-flow-stage-icon{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#EDF4FF;color:#2468F2;font-size:17px;font-weight:800;}
        .ao-flow-stage-icon.purple{background:#F0EAFF;color:#7A43EA;} .ao-flow-stage-icon.red{background:#FFF0F2;color:#E5484D;} .ao-flow-stage-icon.amber{background:#FFF5DF;color:#EA9514;} .ao-flow-stage-icon.green{background:#E9F8F2;color:#11A16C;}
        .ao-flow-node-final{background:#19A96B !important;color:#FFF !important;}
        .ao-flow-stage-label{font-size:8.5px;color:#17376E;margin-top:5px;text-align:center;white-space:nowrap;}
        .ao-flow-arrow{color:#7891B6;font-size:17px;margin-top:8px;}
        div[data-testid="stHorizontalBlock"]{gap:.75rem !important;}
        @media(max-width:1200px){.ao-hero-approved .ao-hero-title{font-size:42px}.ao-hero-approved .ao-hero-subtitle{font-size:29px}.ao-podium-row-approved{grid-template-columns:1fr 180px 1fr}.ao-competitor-inner{grid-template-columns:95px 1fr}.ao-approved-avatar{width:92px;height:92px}.ao-approved-team-avatar{width:100px;height:92px}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    st.markdown(
        """
        <div class="ao-sidebar-brand">
            <div class="ao-trophy" aria-hidden="true">
                <svg viewBox="0 0 72 72" width="100%" height="100%" role="img" aria-label="Olympic-style trophy mark">
                    <g fill="none" stroke="#F6D35A" stroke-width="2.6" stroke-linecap="round">
                        <path d="M18 55c-8-8-11-18-9-29"/><path d="M54 55c8-8 11-18 9-29"/>
                        <path d="M13 47l-6-3M11 39l-6-5M11 31l-5-6M14 24l-3-7M18 19l-1-7"/>
                        <path d="M59 47l6-3M61 39l6-5M61 31l5-6M58 24l3-7M54 19l1-7"/>
                    </g>
                    <g fill="#F6D35A">
                        <path d="M25 18h22v5c0 9-4 15-11 18-7-3-11-9-11-18z"/>
                        <rect x="33" y="40" width="6" height="10" rx="1"/>
                        <rect x="27" y="50" width="18" height="4" rx="2"/>
                        <rect x="24" y="55" width="24" height="4" rx="2"/>
                        <path d="M25 22H18c0 7 3 11 9 13v-4c-3-2-4-4-4-6h2zM47 22h7c0 7-3 11-9 13v-4c3-2 4-4 4-6h-2z"/>
                    </g>
                </svg>
            </div>
            <div class="ao-sidebar-title">AI Agent<br>Olympics</div>
        </div>
        <div class="ao-sidebar-sub">EVALUATE · COMPARE · LEARN</div>
        """,
        unsafe_allow_html=True,
    )



def render_top_toolbar() -> None:
    st.markdown(
        '''
        <div class="ao-topbar ao-topbar-approved">
            <div class="ao-topbar-brandline">
                <span class="ao-topbar-app">AI Agent Olympics</span>
                <span class="ao-topbar-context">MULTI-EVENT EVALUATION OF AI AGENT FRAMEWORKS</span>
            </div>
            <div class="ao-topbar-date">● &nbsp; 5 EVENTS COMPLETE</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    scenic = _data_uri("hero_scenic.jpg", "image/jpeg")
    st.markdown(
        f'''
        <div class="ao-hero ao-hero-approved" style="--ao-hero-image:url('{scenic}')">
            <div class="ao-hero-fade"></div>
            <div class="ao-hero-content">
                <div class="ao-hero-kicker">EXECUTIVE INTERPRETATION</div>
                <div class="ao-hero-title">The strongest story is not who ‘won’.</div>
                <div class="ao-hero-subtitle">It is that different framework strengths emerge<br>under different operating pressures.</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_podium_comparison() -> None:
    oa = _data_uri("openai_avatar.png")
    ag = _data_uri("autogen_team.png")
    podium = _data_uri("podium.png")
    st.markdown(
        f'''
        <div class="ao-podium-card ao-podium-card-approved">
            <div class="ao-podium-row ao-podium-row-approved">
                <div class="ao-competitor-panel openai">
                    <div class="ao-competitor-inner">
                        <img class="ao-approved-avatar" src="{oa}" />
                        <div>
                            <div class="ao-comp-name ao-comp-name-approved">OpenAI<br>Agents SDK</div>
                            <div class="ao-comp-mode">SINGLE-AGENT EXECUTION</div>
                            <div class="ao-comp-tagline">Concise. Efficient. Focused.</div>
                        </div>
                    </div>
                </div>
                <div class="ao-approved-podium-wrap">
                    <img class="ao-approved-podium-img" src="{podium}" alt="Olympic-style podium"/>
                </div>
                <div class="ao-competitor-panel autogen">
                    <div class="ao-competitor-inner autogen">
                        <img class="ao-approved-team-avatar" src="{ag}" />
                        <div>
                            <div class="ao-comp-name ao-comp-name-approved">Microsoft<br>AutoGen</div>
                            <div class="ao-comp-mode">MULTI-AGENT ORCHESTRATION</div>
                            <div class="ao-comp-tagline">Autonomous. Collaborative. Resilient.</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="ao-metric-strip ao-metric-strip-approved">
                <div class="ao-metric"><div class="ao-metric-main">⚙ 665</div><div class="ao-metric-label">Total tokens</div></div>
                <div class="ao-metric"><div class="ao-metric-main">$ Lower</div><div class="ao-metric-label">Model cost</div></div>
                <div class="ao-metric"><div class="ao-metric-main">▤ 100 words</div><div class="ao-metric-label">Decision brief</div></div>
                <div class="ao-metric"><div class="ao-metric-main">🛡 6/6</div><div class="ao-metric-label">Security</div></div>
                <div class="ao-metric"><div class="ao-metric-main">⚡ Faster</div><div class="ao-metric-label">Final run time</div></div>
                <div class="ao-metric"><div class="ao-metric-main">▤ Supported</div><div class="ao-metric-label">Evidence</div></div>
                <div class="ao-metric"><div class="ao-metric-main">🛡 5/5</div><div class="ao-metric-label">Citation checks</div></div>
                <div class="ao-metric"><div class="ao-metric-main">🛡 Full pass</div><div class="ao-metric-label">Security</div></div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_profiles() -> None:
    st.markdown(
        '''
        <div class="ao-profile-grid ao-profile-grid-approved">
            <div class="ao-profile ao-profile-approved">
                <div class="ao-profile-title">OpenAI Agents SDK profile</div>
                <div class="ao-profile-sub">Strong concise-execution profile in the final Budget Marathon.</div>
                <ul class="ao-profile-list">
                    <li><span class="ao-profile-icon">▰</span>665 total tokens vs 700</li>
                    <li><span class="ao-profile-icon">●</span>Lower estimated model cost</li>
                    <li><span class="ao-profile-icon">▤</span>100-word decision brief vs 113</li>
                    <li><span class="ao-profile-icon">◆</span>Prompt-injection security: 6/6</li>
                </ul>
            </div>
            <div class="ao-profile ao-profile-approved">
                <div class="ao-profile-title">Microsoft AutoGen profile</div>
                <div class="ao-profile-sub">Strong run-time and autonomous-research profile across the validated events.</div>
                <ul class="ao-profile-list">
                    <li><span class="ao-profile-icon">⚡</span>Faster final run time in all five event comparisons</li>
                    <li><span class="ao-profile-icon">▤</span>Supported evidence in autonomous Research Sprint</li>
                    <li><span class="ao-profile-icon">◆</span>Prompt-injection citation checks: 5/5</li>
                    <li><span class="ao-profile-icon">◆</span>Security and misinformation: full pass</li>
                </ul>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_medal_board() -> None:
    rows = [
        ("📄 Research Sprint", '<span class="ao-medal-rank silver">2</span><span>Silver (2)</span>', '<span class="ao-medal-rank gold">1</span><span>Gold (1)</span>'),
        ("🔧 Broken Tool Relay", '<span class="ao-medal-rank silver">2</span><span>Silver (2)</span>', '<span class="ao-medal-rank gold">1</span><span>Gold (1)</span>'),
        ("🛑 Misinformation", '<span class="ao-medal-rank silver">2</span><span>Silver (2)</span>', '<span class="ao-medal-rank gold">1</span><span>Gold (1)</span>'),
        ("🛡 Prompt Injection", '<span class="ao-medal-rank gold">1</span><span>Gold (1)</span>', '<span class="ao-medal-rank silver">2</span><span>Silver (2)</span>'),
        ("🟢 Budget Marathon", '<span class="ao-medal-rank gold">1</span><span>Gold (1)</span>', '<span class="ao-medal-rank silver">2</span><span>Silver (2)</span>'),
    ]
    body = "".join(f"<tr><td>{event}</td><td><span class='ao-medal-value'>{oa}</span></td><td><span class='ao-medal-value'>{ag}</span></td></tr>" for event, oa, ag in rows)
    st.markdown(
        f'''
        <div class="ao-medal-board ao-medal-board-approved">
            <div class="ao-medal-head">
                <div>
                    <div class="ao-medal-title"><span>🏆</span>Event Medal Board</div>
                    <div class="ao-medal-sub">Comparison across all Olympic events. Different strengths emerge under different operating pressures.</div>
                </div>
                <div class="ao-medal-legend"><span><span class="ao-medal-dot gold">1</span>Best</span><span><span class="ao-medal-dot silver">2</span>Second</span><span><span class="ao-medal-dot bronze">3</span>Third</span></div>
            </div>
            <table class="ao-medal-table">
                <thead><tr><th>Event</th><th>OpenAI Agents SDK</th><th>Microsoft AutoGen</th></tr></thead>
                <tbody>{body}</tbody>
            </table>
        </div>
        ''',
        unsafe_allow_html=True,
    )

def _flow_nodes(active: int = 4) -> str:
    parts = []
    for i in range(4):
        parts.append(f'<span class="ao-node {"on" if i <= active else ""}"></span>')
        if i < 3:
            parts.append('<span class="ao-line"></span>')
    return "".join(parts)



def render_live_event_flow(selected_event: str | None = None) -> None:
    flows = [
        ("research_sprint", "📄", "Research Sprint", [("?","Question"),("⌕","Evidence"),("▤","Answer"),("✓","Eval")], "blue"),
        ("broken_tool_relay", "🔧", "Broken Tool Relay", [("▤","Task"),("⊗","Tool fail"),("↻","Retry"),("⚙","Recovery"),("✓","Eval")], "purple"),
        ("misinformation_challenge", "🛑", "Misinformation", [("▤","Claim"),("⌕","Verify"),("◆","Detect"),("✓","Eval")], "red"),
        ("prompt_injection_hurdle", "🛡", "Prompt Injection", [("▱","User Input"),("◆","Defend"),("▤","Safe Output"),("✓","Eval")], "amber"),
        ("budget_marathon", "🟢", "Budget Marathon", [("▤","Task"),("⚙","Plan"),("▰","Execute"),("✓","Eval")], "green"),
    ]
    cards = []
    for event_id, icon, label, nodes, tone in flows:
        pieces = []
        for i, (symbol, node_label) in enumerate(nodes):
            final_cls = "ao-flow-node-final" if node_label == "Eval" else ""
            pieces.append(f'<div class="ao-flow-stage"><div class="ao-flow-stage-icon {tone} {final_cls}">{symbol}</div><div class="ao-flow-stage-label">{node_label}</div></div>')
            if i < len(nodes) - 1:
                pieces.append('<div class="ao-flow-arrow">→</div>')
        ready_html = '<span class="ao-flow-ready">Live</span>' if selected_event == event_id else ''
        cards.append(
            f'<div class="ao-flow-card"><div class="ao-flow-card-title"><span class="ao-flow-card-icon {tone}">{icon}</span>{html.escape(label)}{ready_html}</div><div class="ao-flow-stages">{"".join(pieces)}</div></div>'
        )
    flow_html = (
        '<div class="ao-rail-card ao-live-flow-approved">'
        '<div class="ao-rail-head"><div><div class="ao-rail-title">Live Event Flow</div><div class="ao-rail-sub">Agent workflows across each Olympic event</div></div><div class="ao-live-pill">● Live</div></div>'
        + ''.join(cards)
        + '</div>'
    )
    st.markdown(flow_html, unsafe_allow_html=True)

def render_telemetry_mini() -> None:
    df = get_final_benchmark_df()
    order = ["Research Sprint", "Broken Tool Relay", "Misinformation Challenge", "Prompt Injection Hurdle", "Budget Marathon"]
    labels = ["Research", "Tool Relay", "Misinformation", "Prompt Inject", "Budget"]
    oa = df[df["framework"] == "OpenAI Agents SDK"].set_index("event").reindex(order)
    ag = df[df["framework"] == "Microsoft AutoGen"].set_index("event").reindex(order)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=labels, y=oa["duration_seconds"], mode="lines+markers", name="OpenAI Agents SDK", line=dict(color="#2468F2", width=2), marker=dict(size=5), fill="tozeroy", fillcolor="rgba(36,104,242,.06)"))
    fig.add_trace(go.Scatter(x=labels, y=ag["duration_seconds"], mode="lines+markers", name="Microsoft AutoGen", line=dict(color="#6D4BF6", width=2), marker=dict(size=5), fill="tozeroy", fillcolor="rgba(109,75,246,.04)"))
    fig.update_layout(
        height=185,
        margin=dict(l=34,r=8,t=18,b=28),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", x=1, xanchor="right", y=1.16, yanchor="bottom", font=dict(size=8)),
        xaxis=dict(title="", tickfont=dict(size=8, color="#8290A9"), showgrid=False, fixedrange=True),
        yaxis=dict(title=dict(text="sec", font=dict(size=8, color="#8290A9")), tickfont=dict(size=8, color="#8290A9"), gridcolor="#EEF2F7", zeroline=False, fixedrange=True),
        font=dict(family="Manrope, Arial, sans-serif", color="#415C89"),
        hovermode="x unified",
    )
    st.markdown('<div class="ao-rail-card"><div class="ao-rail-head"><div class="ao-rail-title">Event Telemetry</div><div style="color:#607A9F">→</div></div><div class="ao-rail-sub">Independent run time across all Olympic events</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


def render_key_takeaways() -> None:
    items = [
        ("🏆", "Different strengths win in different contexts", "No universal framework winner across all events."),
        ("📊", "Trade-offs are clear and measurable", "Speed, cost, evidence and security vary by use case."),
        ("👥", "Both frameworks show production potential", "Choose based on your operating priorities."),
    ]
    rows = "".join(
        f'<div class="ao-takeaway"><div class="ao-takeaway-icon">{icon}</div><div><div class="ao-takeaway-title">{html.escape(title)}</div><div class="ao-takeaway-sub">{html.escape(sub)}</div></div></div>'
        for icon, title, sub in items
    )
    st.markdown(
        f'<div class="ao-rail-card"><div class="ao-rail-head"><div class="ao-rail-title">💡 Key Takeaways</div><div style="color:#607A9F">→</div></div>{rows}</div>',
        unsafe_allow_html=True,
    )


def render_page_heading(kicker: str, title: str, subtitle: str, status: str | None = None) -> None:
    status_html = f'<div class="ao-page-status">{html.escape(status)}</div>' if status else ""
    st.markdown(
        f"""
        <div class="ao-page-head">
            <div><div class="ao-page-kicker">{html.escape(kicker)}</div><div class="ao-page-title">{html.escape(title)}</div><div class="ao-page-sub">{html.escape(subtitle)}</div></div>
            {status_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="ao-section-title">{html.escape(title)}</div><div class="ao-section-sub">{html.escape(subtitle)}</div>', unsafe_allow_html=True)


def render_kpi_grid(items: list[tuple[str,str,str]]) -> None:
    blocks = "".join(f'<div class="ao-kpi"><div class="ao-kpi-label">{html.escape(label)}</div><div class="ao-kpi-value">{html.escape(value)}</div><div class="ao-kpi-note">{html.escape(note)}</div></div>' for label,value,note in items)
    st.markdown(f'<div class="ao-kpi-grid">{blocks}</div>', unsafe_allow_html=True)


def inject_approved_design_lock_css() -> None:
    """Final visual lock based on the approved AI Agent Olympics reference screen.

    This layer intentionally overrides earlier experimental styling. Keep changes here
    narrowly scoped so the approved design remains the visual source of truth.
    """
    st.markdown(
        """
        <style>
        /* APPROVED DESIGN LOCK -------------------------------------------------- */
        :root{
            --approved-sidebar:#0B2A52;
            --approved-sidebar-deep:#082243;
            --approved-active:#1774F1;
            --approved-page:#F5F8FC;
            --approved-card:#FFFFFF;
            --approved-border:#DCE6F1;
            --approved-navy:#0C2A5C;
            --approved-blue:#2468EE;
            --approved-muted:#61779A;
            --approved-gold:#EAAF12;
            --approved-silver:#9BAABC;
            --approved-green:#14A66D;
        }

        /* The approved screen is a sans-serif product UI. Manrope is the visible UI
           font throughout. IBM Plex Mono is reserved for code/trace output only. */
        html, body, [class*="css"], .stApp,
        p, div, span, label, button, input, textarea, select,
        h1, h2, h3, h4, h5, h6,
        .ao-card-title,.ao-page-title,.ao-section-title,.ao-profile-title,.ao-medal-title,
        .ao-rail-title,.ao-hero-title,.ao-hero-subtitle{
            font-family:"Manrope", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }
        code, pre, kbd, samp{
            font-family:"IBM Plex Mono", "SFMono-Regular", Consolas, monospace !important;
        }

        .stApp{background:var(--approved-page) !important;}
        .block-container{max-width:none !important;padding:0 1.05vw 2.2vw !important;}

        /* Persistent sidebar, proportional to the approved reference on wide displays. */
        section[data-testid="stSidebar"]{
            width:17vw !important;
            min-width:272px !important;
            max-width:430px !important;
            background:linear-gradient(180deg,var(--approved-sidebar) 0%,var(--approved-sidebar-deep) 100%) !important;
            border-right:0 !important;
            box-shadow:none !important;
        }
        section[data-testid="stSidebar"] > div{width:17vw !important;min-width:272px !important;max-width:430px !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding:0 1.15vw 1.3vw !important;}
        [data-testid="stSidebarCollapseButton"],[data-testid="collapsedControl"]{display:none !important;}

        .ao-sidebar-brand{padding:2.1vw .75vw .9vw !important;gap:.85vw !important;align-items:center !important;}
        .ao-trophy{
            width:4vw !important;height:4vw !important;min-width:56px !important;min-height:56px !important;
            max-width:76px !important;max-height:76px !important;font-size:2.25vw !important;
            border:none !important;background:transparent !important;color:#F5D45E !important;
        }
        .ao-trophy::before,.ao-trophy::after{display:none !important;content:none !important;}
        .ao-trophy svg{display:block;width:100%;height:100%;}
        .ao-sidebar-title{font-size:clamp(23px,1.45vw,34px) !important;font-weight:800 !important;line-height:1.05 !important;color:#FFF !important;letter-spacing:-.02em !important;}
        .ao-sidebar-sub{font-size:clamp(10px,.58vw,14px) !important;font-weight:650 !important;letter-spacing:.18em !important;color:#A9BBD5 !important;margin:.1vw .8vw 1.25vw !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"]{margin:.22vw 0 !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button{
            width:100% !important;min-height:clamp(48px,2.9vw,62px) !important;border-radius:8px !important;
            padding:0 .95vw !important;justify-content:flex-start !important;border:0 !important;box-shadow:none !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]{background:transparent !important;color:#E9F0FA !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover{background:#153B67 !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]{
            background:linear-gradient(90deg,#1778F5 0%,#1766DE 100%) !important;color:#FFF !important;
            box-shadow:0 7px 18px rgba(15,104,231,.24) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button p{
            font-size:clamp(15px,.78vw,19px) !important;font-weight:550 !important;line-height:1.2 !important;color:inherit !important;text-align:left !important;
        }
        .ao-side-footer{font-size:clamp(12px,.68vw,16px) !important;line-height:2.25 !important;margin:2.2vw .6vw 0 !important;padding-top:1.2vw !important;border-top:1px solid #355277 !important;}
        .ao-side-section{font-size:clamp(9px,.48vw,12px) !important;letter-spacing:.14em !important;color:#9EB1CD !important;margin:0 0 .45vw !important;}

        /* Approved top bar. */
        .ao-topbar-approved{
            height:clamp(52px,3.4vw,68px) !important;margin:0 -1.05vw !important;padding:0 1.45vw !important;
            background:#FFF !important;border-bottom:1px solid var(--approved-border) !important;box-shadow:none !important;
        }
        .ao-topbar-app{font-size:clamp(17px,1vw,24px) !important;font-weight:800 !important;color:var(--approved-navy) !important;}
        .ao-topbar-context{font-size:clamp(10px,.56vw,14px) !important;letter-spacing:.12em !important;color:#5872A0 !important;font-weight:650 !important;}
        .ao-topbar-date{font-size:clamp(12px,.72vw,17px) !important;font-weight:650 !important;color:#17396F !important;}

        /* Hero proportions and typography exactly follow the approved reference. */
        .ao-hero-approved{
            min-height:clamp(210px,12.7vw,330px) !important;margin:.65vw 0 1vw !important;padding:1.3vw 1.55vw !important;
            border:1px solid #D6E2F0 !important;border-radius:10px !important;
            background:linear-gradient(100deg,#F8FBFF 0%,#F4F9FF 45%,#EAF3FF 100%) !important;
        }
        .ao-hero-approved::after{width:54% !important;background-position:right center !important;opacity:1 !important;}
        .ao-hero-approved .ao-hero-fade{left:35% !important;width:39% !important;background:linear-gradient(90deg,#F8FBFF 0%,rgba(248,251,255,.98) 32%,rgba(248,251,255,0) 100%) !important;}
        .ao-hero-approved .ao-hero-content{width:73% !important;padding-left:1vw !important;border-left:4px solid #2472F4 !important;}
        .ao-hero-approved .ao-hero-kicker{font-size:clamp(11px,.62vw,15px) !important;letter-spacing:.13em !important;font-weight:750 !important;margin-bottom:.7vw !important;color:#315282 !important;}
        .ao-hero-approved .ao-hero-title{
            font-size:clamp(48px,3.05vw,74px) !important;line-height:1.02 !important;font-weight:800 !important;
            color:#09285D !important;letter-spacing:-.04em !important;margin-bottom:.3vw !important;
        }
        .ao-hero-approved .ao-hero-subtitle{
            font-size:clamp(30px,2.05vw,50px) !important;line-height:1.03 !important;font-weight:800 !important;
            color:#2465D4 !important;letter-spacing:-.035em !important;margin:0 !important;
        }

        /* Main overview split matches approved central canvas + right workflow rail. */
        div[data-testid="stHorizontalBlock"]{gap:.8vw !important;}

        /* Head-to-head card. */
        .ao-podium-card-approved{border:1px solid var(--approved-border) !important;border-radius:10px !important;background:#FFF !important;overflow:hidden !important;box-shadow:0 2px 8px rgba(21,48,88,.035) !important;}
        .ao-podium-row-approved{
            grid-template-columns:minmax(0,1fr) clamp(250px,15vw,355px) minmax(0,1fr) !important;
            min-height:clamp(250px,15vw,370px) !important;background:#FFF !important;padding:0 !important;gap:0 !important;
        }
        .ao-competitor-panel{height:100% !important;min-height:clamp(250px,15vw,370px) !important;padding:2.15vw 1.55vw !important;display:flex !important;align-items:center !important;border-top:5px solid #D7A018 !important;}
        .ao-competitor-panel.autogen{border-top-color:#9CA9B8 !important;}
        .ao-competitor-inner{grid-template-columns:clamp(116px,7.2vw,170px) 1fr !important;gap:1.15vw !important;}
        .ao-competitor-inner.autogen{grid-template-columns:clamp(128px,7.6vw,185px) 1fr !important;}
        .ao-approved-avatar{width:clamp(112px,7vw,166px) !important;height:clamp(112px,7vw,166px) !important;}
        .ao-approved-team-avatar{width:clamp(125px,7.5vw,180px) !important;height:clamp(112px,7vw,166px) !important;}
        .ao-comp-name-approved{font-size:clamp(23px,1.35vw,32px) !important;line-height:1.03 !important;font-weight:800 !important;color:#0D2E63 !important;letter-spacing:-.025em !important;}
        .ao-comp-mode{font-size:clamp(10px,.57vw,14px) !important;margin-top:.65vw !important;color:#3D5E90 !important;font-weight:700 !important;}
        .ao-comp-tagline{font-size:clamp(13px,.76vw,18px) !important;margin-top:1.35vw !important;color:#17396B !important;}
        .ao-approved-podium-wrap{height:100% !important;min-height:clamp(250px,15vw,370px) !important;display:flex !important;align-items:flex-end !important;justify-content:center !important;background:linear-gradient(180deg,#FFF 0%,#FBFCFF 100%) !important;overflow:visible !important;}
        .ao-approved-podium-img{width:clamp(250px,15vw,350px) !important;height:auto !important;max-height:90% !important;object-fit:contain !important;object-position:center bottom !important;transform:none !important;display:block !important;}

        /* Metrics row. */
        .ao-metric-strip-approved{grid-template-columns:repeat(8,1fr) !important;background:#FFF !important;border-top:1px solid #E5ECF4 !important;}
        .ao-metric-strip-approved .ao-metric{min-height:clamp(66px,4.1vw,92px) !important;padding:.75vw .85vw !important;border-right:1px solid #E8EEF6 !important;}
        .ao-metric-strip-approved .ao-metric:last-child{border-right:0 !important;}
        .ao-metric-strip-approved .ao-metric-main{font-size:clamp(14px,.82vw,20px) !important;font-family:"Manrope",sans-serif !important;font-weight:800 !important;color:#14356B !important;}
        .ao-metric-strip-approved .ao-metric-label{font-size:clamp(8px,.46vw,11px) !important;font-weight:650 !important;color:#7690B5 !important;margin-top:.2vw !important;}

        /* Profiles. */
        .ao-profile-grid-approved{gap:.8vw !important;}
        .ao-profile-approved{min-height:clamp(210px,12.5vw,300px) !important;padding:1.25vw 1.45vw !important;border:1px solid var(--approved-border) !important;border-radius:10px !important;background:#FFF !important;}
        .ao-profile-approved .ao-profile-title{font-size:clamp(19px,1.1vw,27px) !important;font-weight:800 !important;color:#12346D !important;}
        .ao-profile-approved .ao-profile-sub{font-size:clamp(11px,.67vw,16px) !important;line-height:1.35 !important;margin:.35vw 0 .9vw !important;color:#62799D !important;}
        .ao-profile-approved .ao-profile-list{gap:.72vw !important;}
        .ao-profile-approved .ao-profile-list li{font-size:clamp(13px,.8vw,19px) !important;color:#1B477E !important;line-height:1.25 !important;}
        .ao-profile-approved .ao-profile-icon{font-size:clamp(15px,.9vw,21px) !important;width:1.25vw !important;min-width:18px !important;color:#164982 !important;}

        /* Medal board. */
        .ao-medal-board-approved{border:1px solid var(--approved-border) !important;border-radius:10px !important;background:#FFF !important;}
        .ao-medal-board-approved .ao-medal-head{padding:.8vw 1.15vw .55vw !important;}
        .ao-medal-board-approved .ao-medal-title{font-size:clamp(18px,1.05vw,25px) !important;font-weight:800 !important;color:#12346D !important;}
        .ao-medal-board-approved .ao-medal-sub{font-size:clamp(10px,.58vw,14px) !important;color:#657B9D !important;}
        .ao-medal-board-approved .ao-medal-legend{font-size:clamp(9px,.52vw,13px) !important;gap:.7vw !important;}
        .ao-medal-board-approved .ao-medal-table th{font-size:clamp(11px,.64vw,15px) !important;padding:.42vw .8vw !important;background:#F1F5FA !important;color:#17396F !important;}
        .ao-medal-board-approved .ao-medal-table td{font-size:clamp(11px,.64vw,15px) !important;padding:.38vw .8vw !important;color:#244A7C !important;}
        .ao-medal-value{font-size:inherit !important;gap:.45vw !important;}
        .ao-medal-rank{width:clamp(18px,1.05vw,25px) !important;height:clamp(18px,1.05vw,25px) !important;font-size:clamp(9px,.5vw,12px) !important;}

        /* Right rail live flow. */
        .ao-live-flow-approved{padding:1vw .85vw !important;border:1px solid var(--approved-border) !important;border-radius:10px !important;background:#FFF !important;}
        .ao-live-flow-approved .ao-rail-title{font-size:clamp(20px,1.2vw,28px) !important;font-weight:800 !important;color:#0F2F65 !important;}
        .ao-live-flow-approved .ao-rail-sub{font-size:clamp(10px,.58vw,14px) !important;color:#6B80A1 !important;margin-top:.15vw !important;}
        .ao-live-pill{font-size:clamp(9px,.5vw,12px) !important;padding:.32vw .6vw !important;}
        .ao-flow-card{padding:.75vw .75vw .65vw !important;margin-top:.68vw !important;border:1px solid #DCE5F0 !important;border-radius:9px !important;background:#FFF !important;}
        .ao-flow-card-title{font-size:clamp(12px,.72vw,17px) !important;font-weight:800 !important;color:#15376E !important;gap:.5vw !important;}
        .ao-flow-card-icon{width:clamp(26px,1.55vw,36px) !important;height:clamp(26px,1.55vw,36px) !important;font-size:clamp(14px,.82vw,19px) !important;}
        .ao-flow-stages{margin-top:.65vw !important;}
        .ao-flow-stage{min-width:clamp(44px,2.7vw,64px) !important;}
        .ao-flow-stage-icon{width:clamp(36px,2.1vw,50px) !important;height:clamp(36px,2.1vw,50px) !important;font-size:clamp(16px,.95vw,22px) !important;}
        .ao-flow-stage-label{font-size:clamp(8px,.48vw,12px) !important;margin-top:.35vw !important;color:#17396E !important;}
        .ao-flow-arrow{font-size:clamp(16px,.95vw,22px) !important;margin-top:.55vw !important;color:#7892B8 !important;}

        /* All other pages inherit the same approved typography hierarchy. */
        .ao-page-title{font-size:clamp(32px,2.05vw,48px) !important;font-weight:800 !important;color:#0D2D62 !important;letter-spacing:-.03em !important;}
        .ao-section-title{font-size:clamp(22px,1.35vw,31px) !important;font-weight:800 !important;color:#12346D !important;}
        .ao-card-title{font-weight:800 !important;color:#12346D !important;}

        /* Keep the approved layout on desktop; only collapse at true tablet widths. */
        @media(max-width:1100px){
            section[data-testid="stSidebar"],section[data-testid="stSidebar"] > div{width:260px !important;min-width:260px !important;}
            .ao-hero-approved .ao-hero-title{font-size:45px !important;}
            .ao-hero-approved .ao-hero-subtitle{font-size:28px !important;}
            .ao-podium-row-approved{grid-template-columns:1fr 220px 1fr !important;}
            .ao-competitor-inner,.ao-competitor-inner.autogen{grid-template-columns:95px 1fr !important;}
            .ao-approved-avatar,.ao-approved-team-avatar{width:92px !important;height:92px !important;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def inject_final_reference_exact_css() -> None:
    """Final reference lock.

    Fixed-pixel sizing is intentional: typography and component sizes should not
    grow with a wide monitor. This keeps the UI visually aligned with the
    approved reference rather than scaling all controls via viewport units.
    """
    st.markdown(
        """
        <style>
        /* FINAL APPROVED REFERENCE LOCK -------------------------------------- */
        :root{
            --ref-sidebar:#0B2A52;
            --ref-sidebar-deep:#082243;
            --ref-active:#1F73EA;
            --ref-page:#F5F8FC;
            --ref-card:#FFFFFF;
            --ref-border:#DCE6F1;
            --ref-navy:#0C2A5C;
            --ref-blue:#2468EE;
            --ref-muted:#61779A;
        }

        html, body, [class*="css"], .stApp,
        p, div, span, label, button, input, textarea, select,
        h1, h2, h3, h4, h5, h6,
        .ao-card-title,.ao-page-title,.ao-section-title,.ao-profile-title,
        .ao-medal-title,.ao-rail-title,.ao-hero-title,.ao-hero-subtitle{
            font-family:"Manrope", ui-sans-serif, system-ui, -apple-system,
                BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }
        code,pre,kbd,samp{font-family:"IBM Plex Mono","SFMono-Regular",Consolas,monospace !important;}

        .stApp{background:var(--ref-page) !important;}
        .block-container{max-width:none !important;padding:0 14px 28px !important;}

        /* Sidebar — same physical scale as approved reference. */
        section[data-testid="stSidebar"]{
            width:238px !important;min-width:238px !important;max-width:238px !important;
            background:linear-gradient(180deg,var(--ref-sidebar) 0%,var(--ref-sidebar-deep) 100%) !important;
            border-right:0 !important;box-shadow:none !important;
        }
        section[data-testid="stSidebar"] > div{width:238px !important;min-width:238px !important;max-width:238px !important;}
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding:0 10px 15px !important;}
        [data-testid="stSidebarCollapseButton"],[data-testid="collapsedControl"]{display:none !important;}

        .ao-sidebar-brand{padding:18px 10px 10px !important;gap:10px !important;}
        .ao-trophy{width:52px !important;height:52px !important;min-width:52px !important;min-height:52px !important;max-width:52px !important;max-height:52px !important;border:0 !important;background:transparent !important;}
        .ao-sidebar-title{font-size:23px !important;font-weight:800 !important;line-height:1.02 !important;color:#FFF !important;letter-spacing:-.02em !important;}
        .ao-sidebar-sub{font-size:9px !important;font-weight:700 !important;letter-spacing:.17em !important;color:#AABBD5 !important;margin:0 10px 16px !important;}

        section[data-testid="stSidebar"] div[data-testid="stButton"]{margin:2px 0 !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button{
            width:100% !important;min-height:44px !important;height:44px !important;border-radius:7px !important;
            padding:0 12px !important;justify-content:flex-start !important;border:0 !important;box-shadow:none !important;gap:11px !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]{background:transparent !important;color:#E8F0FC !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover{background:#173B67 !important;color:#FFF !important;}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]{
            background:linear-gradient(90deg,#1777F2 0%,#1767DF 100%) !important;color:#FFF !important;
            box-shadow:0 5px 14px rgba(31,102,242,.24) !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] button p{
            font-size:14px !important;font-weight:600 !important;line-height:1.1 !important;color:inherit !important;text-align:left !important;margin:0 !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] [data-testid="stIconMaterial"],
        section[data-testid="stSidebar"] div[data-testid="stButton"] .material-symbols-rounded,
        section[data-testid="stSidebar"] div[data-testid="stButton"] .material-symbols-outlined{
            font-family:"Material Symbols Rounded" !important;font-size:22px !important;line-height:1 !important;
            width:24px !important;min-width:24px !important;height:24px !important;display:inline-flex !important;align-items:center !important;justify-content:center !important;color:inherit !important;
        }
        .ao-side-footer{font-size:12px !important;line-height:2.05 !important;margin:22px 8px 0 !important;padding-top:15px !important;border-top:1px solid #355277 !important;}
        .ao-side-section{font-size:9px !important;letter-spacing:.14em !important;color:#9EB1CD !important;margin:0 0 4px !important;}
        .ao-about-row{display:flex !important;align-items:center !important;gap:10px !important;color:#DDE8F7 !important;font-size:12px !important;line-height:2.2 !important;}
        .ao-about-icon{font-family:"Material Symbols Rounded" !important;font-size:19px !important;width:21px !important;text-align:center !important;color:#DDE8F7 !important;}

        /* Top bar. */
        .ao-topbar-approved{height:44px !important;margin:0 -14px !important;padding:0 16px !important;background:#FFF !important;border-bottom:1px solid var(--ref-border) !important;box-shadow:none !important;}
        .ao-topbar-brandline{gap:28px !important;}
        .ao-topbar-app{font-size:16px !important;font-weight:800 !important;color:var(--ref-navy) !important;}
        .ao-topbar-context{font-size:10px !important;letter-spacing:.12em !important;color:#5872A0 !important;font-weight:650 !important;}
        .ao-topbar-date{font-size:12px !important;font-weight:650 !important;color:#17396F !important;}

        /* Hero. */
        .ao-hero-approved{min-height:190px !important;height:190px !important;margin:10px 0 12px !important;padding:15px 20px !important;border:1px solid #D6E2F0 !important;border-radius:10px !important;}
        .ao-hero-approved::after{width:54% !important;background-position:right center !important;opacity:1 !important;}
        .ao-hero-approved .ao-hero-fade{left:35% !important;width:39% !important;}
        .ao-hero-approved .ao-hero-content{width:72% !important;padding-left:12px !important;border-left:4px solid #2472F4 !important;}
        .ao-hero-approved .ao-hero-kicker{font-size:11px !important;letter-spacing:.13em !important;font-weight:750 !important;margin-bottom:9px !important;color:#315282 !important;}
        .ao-hero-approved .ao-hero-title{font-size:45px !important;line-height:1.01 !important;font-weight:800 !important;color:#09285D !important;letter-spacing:-.038em !important;margin-bottom:4px !important;}
        .ao-hero-approved .ao-hero-subtitle{font-size:29px !important;line-height:1.04 !important;font-weight:800 !important;color:#2465D4 !important;letter-spacing:-.032em !important;margin:0 !important;}

        /* Head-to-head row — fixed height matching approved screen. */
        .ao-podium-card-approved{border:1px solid var(--ref-border) !important;border-radius:10px !important;background:#FFF !important;overflow:hidden !important;box-shadow:0 2px 8px rgba(21,48,88,.035) !important;}
        .ao-podium-row-approved{grid-template-columns:minmax(0,1fr) 210px minmax(0,1fr) !important;min-height:186px !important;height:186px !important;background:#FFF !important;padding:0 !important;gap:0 !important;}
        .ao-competitor-panel{height:186px !important;min-height:186px !important;padding:20px 18px !important;display:flex !important;align-items:center !important;border-top:4px solid #D7A018 !important;}
        .ao-competitor-panel.autogen{border-top-color:#9CA9B8 !important;}
        .ao-competitor-inner{grid-template-columns:98px 1fr !important;gap:14px !important;}
        .ao-competitor-inner.autogen{grid-template-columns:108px 1fr !important;}
        .ao-approved-avatar{width:94px !important;height:94px !important;}
        .ao-approved-team-avatar{width:106px !important;height:94px !important;}
        .ao-comp-name-approved{font-size:20px !important;line-height:1.02 !important;font-weight:800 !important;color:#0D2E63 !important;letter-spacing:-.02em !important;}
        .ao-comp-mode{font-size:9px !important;margin-top:7px !important;color:#3D5E90 !important;font-weight:700 !important;}
        .ao-comp-tagline{font-size:11.5px !important;margin-top:15px !important;color:#17396B !important;}
        .ao-approved-podium-wrap{height:186px !important;min-height:186px !important;display:flex !important;align-items:flex-end !important;justify-content:center !important;background:linear-gradient(180deg,#FFF 0%,#FBFCFF 100%) !important;overflow:hidden !important;}
        .ao-approved-podium-img{width:218px !important;height:174px !important;max-height:174px !important;object-fit:contain !important;object-position:center bottom !important;transform:none !important;display:block !important;}

        /* Metrics strip. */
        .ao-metric-strip-approved{grid-template-columns:repeat(8,1fr) !important;background:#FFF !important;border-top:1px solid #E5ECF4 !important;}
        .ao-metric-strip-approved .ao-metric{min-height:61px !important;height:61px !important;padding:9px 10px !important;border-right:1px solid #E8EEF6 !important;}
        .ao-metric-strip-approved .ao-metric-main{font-size:13px !important;font-family:"Manrope",sans-serif !important;font-weight:800 !important;color:#14356B !important;}
        .ao-metric-strip-approved .ao-metric-label{font-size:7.5px !important;font-weight:650 !important;color:#7690B5 !important;margin-top:2px !important;}

        /* Profiles. */
        .ao-profile-grid-approved{gap:12px !important;}
        .ao-profile-approved{min-height:190px !important;height:auto !important;padding:15px 18px 17px !important;border:1px solid var(--ref-border) !important;border-radius:10px !important;background:#FFF !important;overflow:visible !important;}
        .ao-profile-approved .ao-profile-title{font-size:17px !important;font-weight:800 !important;color:#12346D !important;}
        .ao-profile-approved .ao-profile-sub{font-size:10.5px !important;line-height:1.35 !important;margin:4px 0 10px !important;color:#62799D !important;}
        .ao-profile-approved .ao-profile-list{gap:8px !important;}
        .ao-profile-approved .ao-profile-list li{font-size:12.5px !important;color:#1B477E !important;line-height:1.25 !important;}
        .ao-profile-approved .ao-profile-icon{font-size:15px !important;width:18px !important;min-width:18px !important;color:#164982 !important;}

        /* Medal board. */
        .ao-medal-board-approved{border:1px solid var(--ref-border) !important;border-radius:10px !important;background:#FFF !important;}
        .ao-medal-board-approved .ao-medal-head{padding:9px 13px 7px !important;}
        .ao-medal-board-approved .ao-medal-title{font-size:16px !important;font-weight:800 !important;color:#12346D !important;}
        .ao-medal-board-approved .ao-medal-sub{font-size:9px !important;color:#657B9D !important;}
        .ao-medal-board-approved .ao-medal-legend{font-size:9px !important;gap:7px !important;}
        .ao-medal-board-approved .ao-medal-table th{font-size:10.5px !important;padding:4px 8px !important;background:#F1F5FA !important;color:#17396F !important;}
        .ao-medal-board-approved .ao-medal-table td{font-size:10.5px !important;padding:3px 8px !important;color:#244A7C !important;}
        .ao-medal-value{font-size:10.5px !important;gap:6px !important;}
        .ao-medal-rank{width:17px !important;height:17px !important;font-size:9px !important;}

        /* Live Event Flow rail. */
        .ao-live-flow-approved{padding:13px 11px 11px !important;border:1px solid var(--ref-border) !important;border-radius:10px !important;background:#FFF !important;}
        .ao-live-flow-approved .ao-rail-title{font-size:18px !important;font-weight:800 !important;color:#0F2F65 !important;}
        .ao-live-flow-approved .ao-rail-sub{font-size:9.5px !important;color:#6B80A1 !important;margin-top:2px !important;}
        .ao-live-pill{font-size:9px !important;padding:4px 8px !important;}
        .ao-flow-card{padding:9px 9px 7px !important;margin-top:8px !important;border:1px solid #DCE5F0 !important;border-radius:9px !important;background:#FFF !important;}
        .ao-flow-card-title{font-size:12px !important;font-weight:800 !important;color:#15376E !important;gap:7px !important;}
        .ao-flow-card-icon{width:24px !important;height:24px !important;font-size:13px !important;}
        .ao-flow-stages{margin-top:8px !important;}
        .ao-flow-stage{min-width:40px !important;}
        .ao-flow-stage-icon{width:31px !important;height:31px !important;font-size:15px !important;}
        .ao-flow-stage-label{font-size:7.5px !important;margin-top:4px !important;color:#17396E !important;}
        .ao-flow-arrow{font-size:15px !important;margin-top:7px !important;color:#7892B8 !important;}

        /* Event/secondary pages keep the same scale. */
        .ao-page-title{font-size:30px !important;font-weight:800 !important;color:#0D2D62 !important;letter-spacing:-.025em !important;}
        .ao-section-title{font-size:21px !important;font-weight:800 !important;color:#12346D !important;}
        .ao-card-title{font-weight:800 !important;color:#12346D !important;}

        /* Keep layout intact on desktop, only adjust below tablet widths. */
        @media(max-width:1100px){
            section[data-testid="stSidebar"],section[data-testid="stSidebar"] > div{width:220px !important;min-width:220px !important;max-width:220px !important;}
            .ao-hero-approved .ao-hero-title{font-size:38px !important;}
            .ao-hero-approved .ao-hero-subtitle{font-size:24px !important;}
            .ao-podium-row-approved{grid-template-columns:1fr 180px 1fr !important;}
            .ao-competitor-inner,.ao-competitor-inner.autogen{grid-template-columns:82px 1fr !important;}
            .ao-approved-avatar,.ao-approved-team-avatar{width:80px !important;height:80px !important;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_arena_event_selector_css() -> None:
    """Clear enterprise event-list styling for Olympic Arena."""
    st.markdown(
        """
        <style>
        .ao-arena-selector-head{
            display:flex;align-items:flex-end;justify-content:space-between;gap:20px;
            margin:18px 0 12px;padding:0 2px;
        }
        .ao-arena-selector-kicker{font-size:10px;font-weight:800;letter-spacing:.14em;color:#2E63B8;margin-bottom:4px;}
        .ao-arena-selector-title{font-size:22px;font-weight:800;color:#0D2E63;line-height:1.1;}
        .ao-arena-selector-sub{font-size:12px;line-height:1.55;color:#61779A;max-width:860px;margin-top:5px;}
        .ao-arena-ready-pill{font-size:9px;font-weight:800;letter-spacing:.08em;color:#167657;background:#EAF8F2;border:1px solid #CBEBDD;border-radius:999px;padding:6px 10px;white-space:nowrap;}
        .ao-arena-event-icon{width:42px;height:42px;border-radius:10px;background:#EEF4FC;color:#245FBC;display:flex;align-items:center;justify-content:center;border:1px solid #DCE7F4;}
        .ao-arena-event-icon.selected{background:#E8F1FF;color:#176CE8;border-color:#BDD4FA;}
        .ao-arena-event-icon .material-symbols-rounded{font-family:"Material Symbols Rounded" !important;font-size:22px !important;}
        .ao-arena-event-number{font-size:9px;font-weight:800;letter-spacing:.12em;color:#7890B2;margin-bottom:2px;}
        .ao-arena-event-title{font-size:15px;font-weight:800;color:#12346D;line-height:1.2;}
        .ao-arena-event-copy{font-size:11px;color:#687E9F;line-height:1.45;margin-top:3px;}
        .ao-arena-status{display:inline-flex;align-items:center;justify-content:center;font-size:9px;font-weight:800;letter-spacing:.07em;color:#1B8A65;background:#EDF9F4;border:1px solid #D0EDE2;border-radius:999px;padding:5px 8px;white-space:nowrap;}
        .ao-arena-empty{display:flex;align-items:center;gap:14px;background:#FFF;border:1px dashed #CAD8E8;border-radius:10px;padding:22px 24px;margin-top:4px;}
        .ao-arena-empty-icon{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#F2F6FC;color:#C28B06;}
        .ao-arena-empty-icon .material-symbols-rounded{font-family:"Material Symbols Rounded" !important;font-size:24px !important;}
        .ao-arena-empty-title{font-size:15px;font-weight:800;color:#14356B;}
        .ao-arena-empty-copy{font-size:11px;color:#6D82A1;margin-top:3px;line-height:1.45;}
        .ao-arena-mode-note{margin:8px 0 14px;border-radius:8px;padding:9px 12px;font-size:10.5px;line-height:1.5;border:1px solid #D8E4F2;color:#466386;background:#F8FBFF;}
        .ao-arena-mode-note b{font-size:9.5px;letter-spacing:.08em;color:#194E9D;}
        .ao-arena-mode-note.benchmark{background:#F3FAF7;border-color:#CEEADF;color:#436A5D;}
        .ao-arena-mode-note.benchmark b{color:#14775A;}
        .ao-arena-mode-note.custom{background:#FFF9EB;border-color:#F2DFB6;color:#6F5A32;}
        .ao-arena-mode-note.custom b{color:#9A6700;}
        .ao-custom-question-kicker{font-size:9px;font-weight:850;letter-spacing:.12em;color:#2E63B8;margin:11px 0 6px;}
        .ao-question-workspace-head{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;margin-bottom:7px;}
        .ao-question-workspace-title{font-size:17px;font-weight:800;color:#0D2E63;line-height:1.2;}
        .ao-question-workspace-badge{font-family:"IBM Plex Mono",monospace;font-size:10px;font-weight:700;color:#315EFB;background:#EEF4FF;border:1px solid #D3E1FF;border-radius:999px;padding:5px 9px;}
        .ao-question-workspace-badge.custom{color:#7A4A00;background:#FFF4D8;border-color:#F4D28A;}
        .ao-question-workspace-badge.benchmark{color:#315EFB;background:#EEF4FF;border-color:#D3E1FF;}
        .ao-arena-event-list-label{font-size:9px;font-weight:850;letter-spacing:.13em;color:#7286A5;margin:15px 0 7px;}
        .ao-arena-question-preview{font-size:10px;line-height:1.45;color:#7184A1;margin-top:6px;max-width:940px;}
        .ao-arena-question-preview b{color:#49658C;font-weight:750;}
        .ao-latest-mode{margin:2px 0 10px;border-radius:8px;padding:8px 11px;font-size:10.5px;line-height:1.45;border:1px solid #D8E4F2;background:#F8FBFF;color:#4D668A;}
        .ao-latest-mode b{font-size:9.5px;letter-spacing:.08em;}
        .ao-latest-mode.benchmark{background:#F3FAF7;border-color:#CEEADF;color:#436A5D;}
        .ao-latest-mode.benchmark b{color:#14775A;}
        .ao-latest-mode.custom{background:#FFF9EB;border-color:#F2DFB6;color:#6F5A32;}
        .ao-latest-mode.custom b{color:#9A6700;}
        div[data-testid="stRadio"]:has(input[value="Controlled Benchmark"]) > label{font-size:10px !important;color:#5B7193 !important;margin-bottom:4px !important;}
        div[data-testid="stRadio"]:has(input[value="Controlled Benchmark"]) [role="radiogroup"]{gap:8px !important;}
        div[data-testid="stRadio"]:has(input[value="Controlled Benchmark"]) [role="radiogroup"] label{border:1px solid #D8E4F2;border-radius:8px;padding:7px 10px;background:#FFF;min-height:34px;}
        div[data-testid="stRadio"]:has(input[value="Controlled Benchmark"]) [role="radiogroup"] label:has(input:checked){background:#EEF5FF;border-color:#BCD3F8;}
        div[data-testid="stTextArea"] textarea{border:1px solid #C9D8EB !important;border-radius:8px !important;background:#FCFDFF !important;color:#183665 !important;font-size:12px !important;line-height:1.5 !important;box-shadow:none !important;}
        div[data-testid="stTextArea"] textarea:focus{border-color:#4D8BF5 !important;box-shadow:0 0 0 2px rgba(77,139,245,.10) !important;}
        /* Olympic Arena list containers */
        div[data-testid="stVerticalBlockBorderWrapper"]{border-color:#DDE6F1 !important;border-radius:10px !important;background:#FFF !important;box-shadow:0 1px 4px rgba(20,48,88,.025) !important;}
        
        /* V8 compact action controls — approved UI refinement. */
        section[data-testid="stMain"] div[data-testid="stButton"]{width:max-content !important;max-width:100% !important;}
        section[data-testid="stMain"] div[data-testid="stButton"] button{
            width:auto !important;min-width:0 !important;min-height:34px !important;height:34px !important;
            padding:0 14px !important;border-radius:7px !important;font-size:11px !important;white-space:nowrap !important;
        }
</style>
        """,
        unsafe_allow_html=True,
    )
