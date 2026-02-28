# ============================================================
# AgriAssist AI — components.py
# All UI rendering functions: sidebar, hero, chat, footer
# ============================================================

import streamlit as st
from config import LANGUAGES, TOPICS, FAQS, FOOTER_LINKS
from session import clear_chat


# ─────────────────────────────────────────────
# CSS LOADER
# ─────────────────────────────────────────────
def inject_css():
    """Read styles.css and inject it into the Streamlit page."""
    try:
        with open("styles.css", "r") as f:
            css = f.read()
    except FileNotFoundError:
        css = ""  # Graceful fallback if CSS file is missing
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    """Render the full sidebar: branding, language, topics, offline toggle, clear."""
    with st.sidebar:
        # Branding
        st.markdown('<div class="sidebar-title">🌾 AgriAssist AI</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-info">'
            'Your intelligent farming companion — ask about crops, pests, '
            'fertilizers, and government schemes in your own language.'
            '</div>',
            unsafe_allow_html=True
        )
        st.divider()

        # Language selector
        st.markdown("**🗣️ Select Language**")
        st.session_state.selected_language = st.selectbox(
            "Language", LANGUAGES,
            index=LANGUAGES.index(st.session_state.selected_language),
            label_visibility="collapsed"
        )
        st.divider()

        # Quick topic buttons
        st.markdown("**📌 Quick Topics**")
        for label, (topic_name, starter_prompt) in TOPICS.items():
            if st.button(label, key=f"topic_{topic_name}"):
                st.session_state.selected_topic = topic_name
                st.session_state.prefill_query = starter_prompt
        st.divider()

        # Offline mode toggle
        st.markdown("**📡 Connectivity**")
        st.session_state.offline_mode = st.toggle(
            "Offline Mode",
            value=st.session_state.offline_mode,
            help="When ON, uses cached answers instead of calling the AI API."
        )
        if st.session_state.offline_mode:
            st.markdown(
                '<div class="offline-warn">📦 Offline Mode active. Showing cached responses only.</div>',
                unsafe_allow_html=True
            )
        st.divider()

        # Clear chat
        if st.button("🗑️ Clear Chat History"):
            clear_chat()
            st.rerun()

        # Stats footer
        msg_count = len(st.session_state.messages)
        lang = st.session_state.selected_language
        st.markdown(
            f"<div style='font-size:0.78rem;color:#95D5B2;text-align:center;margin-top:10px;'>"
            f"💬 {msg_count} messages · {lang}</div>",
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
def render_hero():
    """Render the top hero banner with title and tagline."""
    st.markdown("""
    <div class="hero-banner">
        <div style="font-size:3.5rem;line-height:1;">🌾</div>
        <div>
            <p class="hero-title">AgriAssist AI</p>
            <p class="hero-sub">Your AI farming companion — ask anything, anytime, in your language</p>
        </div>
        <div style="margin-left:auto;font-size:2.5rem;opacity:0.6;">🧑‍🌾</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
def render_chat_history():
    """Render all messages from session state as chat bubbles."""
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;color:#A0AEC0;">
            <div style="font-size:3rem;margin-bottom:12px;">🌱</div>
            <p style="font-size:1.1rem;font-weight:600;color:#2D6A4F;">Welcome to AgriAssist!</p>
            <p style="font-size:0.92rem;">
                Ask me anything about your farm — crops, pests, fertilizers, or government schemes.<br>
                Use the <strong>topic buttons</strong> on the left to get started quickly.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍🌾"):
                topic = msg.get("topic", "")
                badge = f'<span class="badge-topic">{topic}</span>' if topic else ""
                st.markdown(f'{msg["content"]}{badge}', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="chat-meta">{msg.get("timestamp", "")}</div>',
                    unsafe_allow_html=True
                )
        else:
            with st.chat_message("assistant", avatar="🤖"):
                if msg.get("cached"):
                    st.markdown(
                        '<span class="badge-cached">📦 Cached Response</span>',
                        unsafe_allow_html=True
                    )
                st.markdown(msg["content"])
                st.markdown(
                    f'<div class="chat-meta">{msg.get("timestamp", "")}</div>',
                    unsafe_allow_html=True
                )
                with st.expander("📋 Copy / View Raw"):
                    st.code(msg["content"], language=None)


# ─────────────────────────────────────────────
# OFFLINE FAQ FALLBACK
# ─────────────────────────────────────────────
def render_offline_fallback():
    """Show when offline mode is ON and no cache match is found."""
    st.markdown(
        '<div class="offline-warn">🔌 <strong>Offline Mode:</strong> '
        'No cached answer found. Try one of these common questions:</div>',
        unsafe_allow_html=True
    )
    for faq in FAQS:
        if st.button(f"❓ {faq}", key=f"faq_{faq}"):
            st.session_state.prefill_query = faq
            st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
def render_footer():
    """Render the disclaimer and resource links footer."""
    links_html = " ".join(
        f'<a href="{url}" target="_blank">{label}</a>'
        for label, url in FOOTER_LINKS
    )
    st.markdown(f"""
    <div class="footer">
        <p>⚠️ <strong>Disclaimer:</strong> AgriAssist provides general agricultural guidance.
        Consult your local <strong>Krishi Vigyan Kendra (KVK)</strong> for field-specific advice.</p>
        <p>{links_html}</p>
    </div>
    """, unsafe_allow_html=True)
