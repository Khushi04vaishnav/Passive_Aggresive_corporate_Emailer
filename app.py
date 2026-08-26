"""
app.py
The Passive-Aggressive Corporate Emailer — Streamlit UI

Layout, branded styling, buttons, and page logic live here.
All reply-generation logic lives in generator.py (kept UI-free on purpose).
"""

import html

import streamlit as st
from generator import (
    generate_reply,
    HONESTY_LEVELS,
    SENDER_TYPES,
    DEMO_SCENARIOS,
)
from brand import NAVY, GOLD, ELECTRIC_BLUE, inject_css
from core.models import RiskLevel
from core.risk import assess_risk, SAFE_ALTERNATIVE

st.set_page_config(
    page_title="The Passive-Aggressive Corporate Emailer",
    page_icon="assets/logo.jpeg",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Brand CSS
# ---------------------------------------------------------------------------
inject_css()

# ---------------------------------------------------------------------------
# Sidebar — logo + controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("assets/logo.jpeg", width=90)
    st.markdown(f"<h3 style='color:{GOLD};'>Control Panel</h3>", unsafe_allow_html=True)

    mode = st.radio("Mode", ["Free Input Mode", "Live Demo Scenarios Mode"])

    st.markdown("---")
    sender_type = st.selectbox("Message is from:", SENDER_TYPES)

    honesty_level = st.slider(
        "Corporate Honesty Level",
        min_value=1, max_value=5, value=2,
        help="1 = mildly petty, 5 = HR-will-be-involved",
    )
    st.caption(HONESTY_LEVELS[honesty_level])

    st.markdown("---")
    auto_send = st.toggle("⚠️ Auto-Send Mode", value=False)
    if auto_send:
        st.markdown("<span class='risky-badge'>RISKY MODE — no human review</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='safe-badge'>SAFE MODE — review before sending</span>", unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🔑 Gemini API Key (optional)"):
        st.caption(
            "Set GEMINI_API_KEY in `.streamlit/secrets.toml` or as an environment "
            "variable to use live Gemini generation. Without it, the app falls back "
            "to local templates automatically — the demo still works either way."
        )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.jpeg", width=64)
with col2:
    st.markdown(f"<h1 style='margin-bottom:0;'>The Passive-Aggressive Corporate Emailer</h1>", unsafe_allow_html=True)
    st.caption("The AI Product Roast & Pivot Challenge — Team 1")

st.write(
    "Reads a message someone sent you and writes a reply — but instead of being "
    "polite, it uses fake-polite, passive-aggressive 'corporate honesty' language."
)

# session state for the current reply so Safe Mode review/edit/delete works
if "current_reply" not in st.session_state:
    st.session_state.current_reply = None
if "current_leaked" not in st.session_state:
    st.session_state.current_leaked = False
if "current_risk" not in st.session_state:
    st.session_state.current_risk = None

# ---------------------------------------------------------------------------
# Free Input Mode
# ---------------------------------------------------------------------------
if mode == "Free Input Mode":
    message = st.text_area("Message you received:", height=120, placeholder="e.g. Hey, just checking in on that report...")

    if st.button("Generate Reply"):
        if message.strip():
            with st.spinner("Drafting a reply..."):
                result = generate_reply(message, sender_type, honesty_level, auto_send)
            st.session_state.current_reply = result["reply"]
            st.session_state.current_leaked = result["leaked"]
            st.session_state.source = result["source"]
            st.session_state.current_risk = assess_risk(message, result["reply"])
        else:
            st.warning("Type a message first.")

# ---------------------------------------------------------------------------
# Live Demo Scenarios Mode
# ---------------------------------------------------------------------------
else:
    scenario_names = [s["name"] for s in DEMO_SCENARIOS]
    chosen_name = st.selectbox("Pick a scripted scenario:", scenario_names)
    scenario = next(s for s in DEMO_SCENARIOS if s["name"] == chosen_name)

    st.info(f"**Incoming message** ({scenario['sender_type']}):\n\n> {scenario['message']}")
    st.caption(scenario["note"])

    if st.button("Run Scenario"):
        with st.spinner("Drafting a reply..."):
            result = generate_reply(
                scenario["message"],
                scenario["sender_type"],
                scenario["honesty_level"],
                auto_send,
            )
        st.session_state.current_reply = result["reply"]
        st.session_state.current_leaked = result["leaked"]
        st.session_state.source = result["source"]
        st.session_state.current_risk = assess_risk(scenario["message"], result["reply"])

# ---------------------------------------------------------------------------
# Output — Safe Mode (review/edit/delete) vs Risky Mode (fires immediately)
# ---------------------------------------------------------------------------
if st.session_state.current_reply:
    st.markdown("---")

    if st.session_state.current_leaked:
        st.markdown(
            "<div class='leak-warning'>🚨 <b>Data-leak flaw triggered:</b> this reply to an "
            "External Client contains an internal-only detail that should never have been sent.</div>",
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # Safety Shield — deterministic scan of the message + generated reply
    # -----------------------------------------------------------------------
    risk = st.session_state.current_risk
    blocked = risk is not None and risk.risk_level == RiskLevel.BLOCKED
    if risk is not None:
        st.markdown(f"<h4>🛡️ Safety Shield</h4>", unsafe_allow_html=True)

        shield_rows = [
            ("Toxicity", risk.toxicity_detected),
            ("Confidential Data", risk.confidential_data_detected),
            ("Prompt Injection", risk.prompt_injection_detected),
            ("Unsafe Request", risk.unsafe_request_detected),
        ]
        cols = st.columns(len(shield_rows))
        for col, (label, detected) in zip(cols, shield_rows):
            with col:
                st.metric(
                    label,
                    "DETECTED" if detected else "NONE",
                    delta="🚨 Risk" if detected else "✓ Safe",
                    delta_color="inverse" if detected else "normal",
                )

        if risk.risk_level == RiskLevel.BLOCKED:
            reasons_html = "".join(f"<li>{html.escape(r)}</li>" for r in risk.reasons)
            st.markdown(
                f"<div class='shield-blocked'>🚫 <b>RESPONSE BLOCKED</b><ul>{reasons_html}</ul>"
                f"<b>Suggested alternative:</b> {html.escape(SAFE_ALTERNATIVE)}</div>",
                unsafe_allow_html=True,
            )
        elif risk.risk_level == RiskLevel.REVIEW:
            st.markdown(
                "<div class='shield-review'>⚠️ <b>REVIEW REQUIRED</b> — flagged for a closer look before sending.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='shield-low'>🟢 <b>LOW RISK</b> — safe to review.</div>",
                unsafe_allow_html=True,
            )

    if blocked:
        st.caption(f"Generated via: {st.session_state.get('source', 'template')}")
    elif not auto_send:
        st.markdown(f"<h4>Safe Mode — Review before sending</h4>", unsafe_allow_html=True)
        edited = st.text_area("Edit the reply if needed:", value=st.session_state.current_reply, height=300)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Send"):
                st.success("Reply sent (simulated).")
        with c2:
            if st.button("🗑️ Delete"):
                st.session_state.current_reply = None
                st.session_state.current_risk = None
                st.rerun()
        st.caption(f"Generated via: {st.session_state.get('source', 'template')}")
    else:
        st.markdown(f"<h4>⚡ Auto-Sent — no review step</h4>", unsafe_allow_html=True)
        st.markdown(f"<div class='reply-box'>{st.session_state.current_reply}</div>", unsafe_allow_html=True)
        st.caption(f"Generated via: {st.session_state.get('source', 'template')}")

# ---------------------------------------------------------------------------
# Risk Notes footer
# ---------------------------------------------------------------------------
with st.expander("📋 Risk Notes — What we tell judges & the red team"):
    st.markdown(
        """
- **No human-in-the-loop:** Auto-Send fires replies with zero review.
- **Context bleed:** the bot can pull internal-only details into a message sent to the wrong audience.
- **Tone misjudgment:** "unfiltered honesty" can read as savage humor internally but as a fireable offense externally.

**A safer version of this product would need:**
- A mandatory review/approval step before sending, especially to external or senior contacts.
- Strict separation between an "internal humor mode" and any real send channel.
- Confidential-data detection and redaction before a reply is drafted.
- Recipient-aware tone limits — no savage mode for clients or leadership.
        """
    )

st.markdown(
    f"<p style='text-align:center; color:{GOLD}; margin-top:2em;'>"
    "Built for The AI Product Roast & Pivot Challenge — Team 1</p>",
    unsafe_allow_html=True,
)
