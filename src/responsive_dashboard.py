"""Responsive hardening for AI Agent Olympics.

The approved >=1500px desktop design is intentionally untouched.
All overrides are scoped to smaller viewport media queries.
"""

import streamlit as st


def inject_responsive_dashboard_css() -> None:
    st.markdown(
        """
        <style>
        /* ------------------------------------------------------------
           AI Agent Olympics responsive hardening
           Desktop baseline >= 1500px remains unchanged.
           ------------------------------------------------------------ */

        /* Large / common laptops: 1280-1499px */
        @media (max-width: 1499px) {
            html, body, .stApp{
                overflow-x:hidden !important;
            }
            section[data-testid="stSidebar"]{
                width:230px !important;
                min-width:230px !important;
                max-width:230px !important;
            }
            section[data-testid="stSidebar"] > div{
                width:230px !important;
            }
            .ao-sidebar-brand{padding:18px 10px 10px !important;gap:10px !important;}
            .ao-trophy{width:50px !important;height:50px !important;font-size:31px !important;}
            .ao-sidebar-title{font-size:20px !important;}
            .ao-sidebar-sub{font-size:9px !important;margin:2px 10px 14px !important;}
            section[data-testid="stSidebar"] div[data-testid="stButton"]{
                width:100% !important;
                max-width:100% !important;
                box-sizing:border-box !important;
                overflow:hidden !important;
            }
            section[data-testid="stSidebar"] div[data-testid="stButton"] button{
                width:100% !important;
                max-width:100% !important;
                min-height:42px !important;
                padding:0 10px !important;
                margin:0 !important;
                box-sizing:border-box !important;
            }
            section[data-testid="stSidebar"] div[data-testid="stButton"] button p{
                font-size:13px !important;
            }

            .block-container{padding:0 14px 30px 14px !important;}
            .ao-topbar-approved{
                margin:0 -14px !important;
                padding:0 14px !important;
            }
            .ao-topbar-brandline{gap:18px !important;}
            .ao-topbar-context{font-size:9.5px !important;letter-spacing:.09em !important;}
            .ao-topbar-date{font-size:11px !important;}

            .ao-hero-approved{
                min-height:184px !important;
                padding:15px 18px 14px !important;
            }
            .ao-hero-approved .ao-hero-content{width:75% !important;}
            .ao-hero-approved .ao-hero-title{
                font-size:40px !important;
                line-height:1.04 !important;
            }
            .ao-hero-approved .ao-hero-subtitle{
                font-size:27px !important;
                line-height:1.08 !important;
            }
            .ao-hero-approved::after{width:48% !important;}

            .ao-podium-row-approved{
                grid-template-columns:minmax(0,1fr) 170px minmax(0,1fr) !important;
                min-height:204px !important;
            }
            .ao-competitor-panel{
                height:204px !important;
                padding:22px 15px !important;
            }
            .ao-competitor-inner{grid-template-columns:92px 1fr !important;gap:10px !important;}
            .ao-competitor-inner.autogen{grid-template-columns:100px 1fr !important;}
            .ao-approved-avatar{width:88px !important;height:88px !important;}
            .ao-approved-team-avatar{width:98px !important;height:90px !important;}
            .ao-comp-name-approved{font-size:19px !important;}
            .ao-comp-tagline{font-size:11px !important;margin-top:12px !important;}
            .ao-approved-podium-wrap{height:204px !important;}
            .ao-approved-podium-img{width:190px !important;height:168px !important;}

            .ao-profile-approved{padding:15px 16px !important;}
            .ao-profile-approved .ao-profile-list li{font-size:12px !important;}
            .ao-medal-board-approved .ao-medal-table th,
            .ao-medal-board-approved .ao-medal-table td{
                padding-left:7px !important;
                padding-right:7px !important;
            }

            div[data-testid="stHorizontalBlock"]{gap:.6rem !important;}
            section[data-testid="stMain"] [data-testid="stColumn"]{min-width:0 !important;}
        }

        /* Small laptops / landscape tablets */
        @media (max-width: 1280px) {
            section[data-testid="stSidebar"]{
                width:200px !important;
                min-width:200px !important;
                max-width:200px !important;
            }
            section[data-testid="stSidebar"] > div{width:200px !important;}
            .ao-sidebar-title{font-size:18px !important;}
            section[data-testid="stSidebar"] div[data-testid="stButton"] button p{
                font-size:12px !important;
            }

            .ao-topbar-context{display:none !important;}
            .ao-topbar-date{font-size:10px !important;}

            .ao-hero-approved{
                min-height:170px !important;
                padding:14px 16px !important;
            }
            .ao-hero-approved .ao-hero-content{width:84% !important;}
            .ao-hero-approved .ao-hero-title{font-size:34px !important;}
            .ao-hero-approved .ao-hero-subtitle{font-size:23px !important;}
            .ao-hero-approved::after{width:42% !important;opacity:.72 !important;}
            .ao-hero-approved .ao-hero-fade{left:47% !important;width:30% !important;}

            /* Stack Streamlit content columns so the right rail never crushes the main workspace. */
            section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]{
                flex-direction:column !important;
                align-items:stretch !important;
                gap:.75rem !important;
            }
            section[data-testid="stMain"] div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{
                width:100% !important;
                flex:1 1 100% !important;
                min-width:100% !important;
            }

            /*
               At 1280px the outer Streamlit columns stack, giving the benchmark
               card the full content width. Keep the approved three-way competitor
               row compact instead of stacking OpenAI / podium / AutoGen vertically.
            */
            .ao-podium-row-approved{
                grid-template-columns:minmax(0,1fr) 155px minmax(0,1fr) !important;
                min-height:190px !important;
                height:auto !important;
            }
            .ao-competitor-panel{
                height:190px !important;
                min-height:190px !important;
                padding:18px 14px !important;
            }
            .ao-competitor-inner{
                grid-template-columns:82px minmax(0,1fr) !important;
                gap:9px !important;
                max-width:none !important;
                margin:0 !important;
            }
            .ao-competitor-inner.autogen{
                grid-template-columns:88px minmax(0,1fr) !important;
                gap:9px !important;
                max-width:none !important;
                margin:0 !important;
            }
            .ao-approved-avatar{
                width:78px !important;
                height:78px !important;
            }
            .ao-approved-team-avatar{
                width:86px !important;
                height:80px !important;
            }
            .ao-comp-name-approved{
                font-size:17px !important;
                line-height:1.04 !important;
            }
            .ao-comp-mode{
                font-size:8px !important;
                margin-top:6px !important;
            }
            .ao-comp-tagline{
                font-size:10px !important;
                line-height:1.25 !important;
                margin-top:10px !important;
            }
            .ao-approved-podium-wrap{
                height:190px !important;
                min-height:190px !important;
                padding:0 !important;
                align-items:flex-end !important;
            }
            .ao-approved-podium-img{
                width:155px !important;
                height:150px !important;
                max-height:150px !important;
                transform:none !important;
            }

            .ao-metric-strip,
            .ao-metric-strip-approved{grid-template-columns:repeat(4,1fr) !important;}
            .ao-profile-grid,
            .ao-profile-grid-approved{grid-template-columns:1fr !important;}
            .ao-kpi-grid{grid-template-columns:repeat(2,1fr) !important;}

            .ao-medal-board{overflow-x:auto !important;}
            .ao-medal-table{min-width:720px !important;}
            .ao-flow-stages{overflow-x:auto !important;padding-bottom:4px !important;}

            section[data-testid="stMain"] div[data-testid="stButton"] button{
                white-space:normal !important;
                height:auto !important;
                min-height:34px !important;
            }
        }

        /* Narrow screens: keep the experience usable rather than desktop-perfect. */
        @media (max-width: 800px) {
            section[data-testid="stSidebar"]{
                width:180px !important;
                min-width:180px !important;
                max-width:180px !important;
            }
            section[data-testid="stSidebar"] > div{width:180px !important;}
            .ao-trophy{width:42px !important;height:42px !important;}
            .ao-sidebar-title{font-size:16px !important;}
            .ao-sidebar-sub{display:none !important;}
            .ao-side-footer{display:none !important;}

            .block-container{padding:0 10px 24px 10px !important;}
            .ao-topbar-approved{
                margin:0 -10px !important;
                height:42px !important;
                padding:0 10px !important;
            }
            .ao-topbar-app{font-size:15px !important;}
            .ao-topbar-date{display:none !important;}

            .ao-hero-approved{
                min-height:160px !important;
                margin-bottom:10px !important;
                padding:14px !important;
            }
            .ao-hero-approved .ao-hero-content{
                width:100% !important;
                padding-left:10px !important;
            }
            .ao-hero-approved .ao-hero-title{font-size:29px !important;}
            .ao-hero-approved .ao-hero-subtitle{
                font-size:19px !important;
                max-width:90% !important;
            }
            .ao-hero-approved::after{width:52% !important;opacity:.20 !important;}
            .ao-hero-approved .ao-hero-fade{
                left:20% !important;
                width:60% !important;
            }

            .ao-metric-strip,
            .ao-metric-strip-approved{grid-template-columns:repeat(2,1fr) !important;}
            .ao-kpi-grid{grid-template-columns:1fr !important;}

            .ao-card-head,
            .ao-medal-head,
            .ao-page-head{
                flex-direction:column !important;
                align-items:flex-start !important;
                gap:8px !important;
            }
            .ao-page-title{font-size:27px !important;}
            .ao-page-status{align-self:flex-start !important;}

            .ao-competitor-inner,
            .ao-competitor-inner.autogen{
                grid-template-columns:78px 1fr !important;
            }
            .ao-approved-avatar{width:74px !important;height:74px !important;}
            .ao-approved-team-avatar{width:78px !important;height:74px !important;}
            .ao-comp-name-approved{font-size:17px !important;}

            div[data-testid="stTabs"] [role="tablist"]{
                overflow-x:auto !important;
                flex-wrap:nowrap !important;
            }
            div[data-testid="stTabs"] button{white-space:nowrap !important;}
        }
        
        /* Final deterministic sidebar button containment for narrow laptop widths. */
        @media (min-width: 801px) and (max-width: 1280px) {
            section[data-testid="stSidebar"] div[data-testid="stButton"]{
                width:184px !important;
                max-width:184px !important;
                min-width:184px !important;
                margin-left:auto !important;
                margin-right:auto !important;
                overflow:hidden !important;
                box-sizing:border-box !important;
            }
            section[data-testid="stSidebar"] div[data-testid="stButton"] button{
                width:100% !important;
                max-width:100% !important;
                min-width:0 !important;
                margin:0 !important;
                box-sizing:border-box !important;
            }
        }

        @media (max-width: 800px) {
            section[data-testid="stSidebar"] div[data-testid="stButton"]{
                width:164px !important;
                max-width:164px !important;
                min-width:164px !important;
                margin-left:auto !important;
                margin-right:auto !important;
                overflow:hidden !important;
                box-sizing:border-box !important;
            }
            section[data-testid="stSidebar"] div[data-testid="stButton"] button{
                width:100% !important;
                max-width:100% !important;
                min-width:0 !important;
                margin:0 !important;
                box-sizing:border-box !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
