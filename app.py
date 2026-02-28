# ============================================================
# AgriAssist AI — app.py  (MAIN ENTRY POINT)
# ============================================================
# SETUP:
#   pip install streamlit anthropic
#   export ANTHROPIC_API_KEY=your_key_here
#   streamlit run app.py
# ============================================================

import streamlit as st
from datetime import datetime

from config import PAGE_CONFIG
from session import init_session, add_message, cache_response
from ai_engine import get_ai_response, search_cache
from components import (
    inject_css,
    render_sidebar,
    render_hero,
    render_chat_history,
    render_offline_fallback,
    render_footer,
)

# ── Page config (must be first Streamlit call) ──
st.set_page_config(**PAGE_CONFIG)


def main():
    # 1. Inject CSS theme
    inject_css()

    # 2. Initialize session state
    init_session()

    # 3. Render sidebar (language, topics, offline toggle, clear)
    render_sidebar()

    # 4. Render hero banner
    render_hero()

    # 5. Render existing chat history
    render_chat_history()

    # 6. Chat input box
    placeholder = (
        st.session_state.prefill_query
        or "Ask your farming question here... (e.g. My tomato leaves are turning yellow)"
    )
    user_input = st.chat_input(placeholder)

    # 7. Handle user input
    if user_input:
        query     = user_input.strip()
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        topic     = st.session_state.selected_topic
        language  = st.session_state.selected_language

        # Save user message to session
        add_message("user", query, timestamp, topic=topic, language=language)
        st.session_state.prefill_query = ""  # clear any pre-fill

        # ── OFFLINE MODE ──
        if st.session_state.offline_mode:
            cached_response = search_cache(query, st.session_state.offline_cache)
            if cached_response:
                add_message("assistant", cached_response, timestamp, cached=True)
            else:
                # Show FAQ fallback inline (not saved to history so user can retry)
                with st.chat_message("assistant", avatar="🤖"):
                    render_offline_fallback()
            st.rerun()

        # ── ONLINE MODE ──
        else:
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🌾 AgriAssist is thinking..."):
                    # Exclude the just-added user message from history context
                    history = st.session_state.messages[:-1]
                    response = get_ai_response(query, language, topic, history)
                st.markdown(response)
                with st.expander("📋 Copy / View Raw"):
                    st.code(response, language=None)

            # Save AI response and update offline cache
            ai_timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
            add_message("assistant", response, ai_timestamp)
            cache_response(query, response)
            st.rerun()

    # 8. Render footer
    render_footer()


if __name__ == "__main__":
    main()
