"""
brand.py
Shared brand constants + CSS for The Passive-Aggressive Corporate Emailer.

Extracted from app.py so the Red Team Lab and Security Dashboard pages can
reuse the exact same look without duplicating the stylesheet.
"""

import streamlit as st

NAVY = "#0D1B2A"
GOLD = "#E0A96D"
ELECTRIC_BLUE = "#1F6FEB"


def inject_css():
    st.markdown(
        f"""
        <style>

        /* =========================================================
           MAIN APP
           ========================================================= */

        .stApp {{
        background-color: {NAVY};
        color: #FFFFFF;
    }}

    /* Remove Streamlit top white header (keep it in the layout so the
       sidebar expand/collapse button inside it still works) */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        box-shadow: none !important;
    }}

    /* The "reopen sidebar" arrow lives inside that header. Streamlit's
       default icon color is dark (meant for a light background), so on
       our navy background it's invisible even though it's clickable.
       Force it visible. */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stExpandSidebarButton"] span {{
        color: {GOLD} !important;
    }}
    [data-testid="stExpandSidebarButton"] {{
        background-color: {NAVY} !important;
        border: 1px solid {GOLD} !important;
        border-radius: 6px !important;
    }}

    [data-testid="stAppViewContainer"] {{
        padding-top: 0 !important;
    }}

    .block-container {{
        padding-top: 0 !important;
    }}


    /* Main headings */
    h1, h2, h3, h4 {{
        color: {GOLD} !important;
    }}

        /* Normal text */
        p {{
            color: #FFFFFF;
        }}


        /* =========================================================
           SIDEBAR
           ========================================================= */

        [data-testid="stSidebar"] {{
            background-color: {NAVY};
            border-right: 1px solid {GOLD};
        }}

        /* Sidebar normal text */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {{
            color: #FFFFFF !important;
        }}

        /* Sidebar headings */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {{
            color: {GOLD} !important;
        }}

        /* Sidebar radio buttons */
        [data-testid="stSidebar"] [data-testid="stRadio"] label {{
            color: #FFFFFF !important;
        }}

        /* Radio button text */
        [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {{
            color: #FFFFFF !important;
        }}

        /* Selectbox label */
        [data-testid="stSidebar"] [data-testid="stSelectbox"] label {{
            color: #FFFFFF !important;
        }}

        /* Slider label */
        [data-testid="stSidebar"] [data-testid="stSlider"] label {{
            color: #FFFFFF !important;
        }}

        /* Toggle label */
        [data-testid="stSidebar"] [data-testid="stToggle"] label {{
            color: #FFFFFF !important;
        }}

        /* Sidebar captions/help text */
        [data-testid="stSidebar"] small,
        [data-testid="stSidebar"] .stCaption {{
            color: #D9E2EC !important;
        }}


        /* =========================================================
           INPUTS / SELECTBOXES
           ========================================================= */

        /* Text area */
        textarea {{
            background-color: #142236 !important;
            color: #FFFFFF !important;
            border: 1px solid {GOLD} !important;
        }}

        textarea::placeholder {{
            color: #AAB7C4 !important;
        }}

        /* Selectbox */
        [data-baseweb="select"] > div {{
            background-color: #142236 !important;
            color: #FFFFFF !important;
            border-color: {GOLD} !important;
        }}

        [data-baseweb="select"] input {{
            color: #FFFFFF !important;
        }}

        /* Selectbox selected text */
        [data-baseweb="select"] span {{
            color: #FFFFFF !important;
        }}


        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button {{
            background-color: {ELECTRIC_BLUE};
            color: #FFFFFF !important;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            padding: 0.5em 1.2em;
        }}

        .stButton > button:hover {{
            background-color: {GOLD};
            color: {NAVY} !important;
        }}


        /* =========================================================
           REPLY BOX
           ========================================================= */

        .reply-box {{
            background-color: #142236;
            border: 1px solid {GOLD};
            border-radius: 10px;
            padding: 1.2em;
            margin-top: 1em;
            color: #FFFFFF;
        }}


        /* =========================================================
           WARNING
           ========================================================= */

        .leak-warning {{
            background-color: #3a1414;
            border: 1px solid #d94f4f;
            border-radius: 10px;
            padding: 1em;
            margin-top: 0.8em;
            color: #ffb3b3;
        }}


        /* =========================================================
           SAFE / RISKY BADGES
           ========================================================= */

        .safe-badge {{
            display: inline-block;
            background-color: {ELECTRIC_BLUE};
            color: #FFFFFF !important;
            border-radius: 20px;
            padding: 0.2em 0.9em;
            font-size: 0.85em;
            font-weight: 600;
        }}

        .risky-badge {{
            display: inline-block;
            background-color: #d94f4f;
            color: #FFFFFF !important;
            border-radius: 20px;
            padding: 0.2em 0.9em;
            font-size: 0.85em;
            font-weight: 600;
        }}

        /* =========================================================
           SAFETY SHIELD (risk scan panel)
           ========================================================= */

        .shield-low {{
            background-color: #14321f;
            border: 1px solid #3fb56f;
            border-radius: 10px;
            padding: 1em;
            margin-top: 0.8em;
            color: #b6f0cb;
        }}

        .shield-review {{
            background-color: #3a2f14;
            border: 1px solid {GOLD};
            border-radius: 10px;
            padding: 1em;
            margin-top: 0.8em;
            color: #ffe1b3;
        }}

        .shield-blocked {{
            background-color: #3a1414;
            border: 1px solid #d94f4f;
            border-radius: 10px;
            padding: 1em;
            margin-top: 0.8em;
            color: #ffb3b3;
        }}

        [data-testid="stMetric"] {{
            background-color: #142236;
            border: 1px solid {GOLD};
            border-radius: 10px;
            padding: 0.6em;
        }}

        [data-testid="stMetricLabel"] {{
            color: #D9E2EC !important;
        }}


        /* =========================================================
           DIVIDERS
           ========================================================= */

        hr {{
            border-color: rgba(224, 169, 109, 0.35) !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
