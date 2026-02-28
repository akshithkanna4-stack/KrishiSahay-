# ============================================================
# AgriAssist AI — session.py
# Streamlit session state initialization and management
# ============================================================

import streamlit as st


def init_session():
    """
    Initialize all required Streamlit session state variables.
    Safe to call multiple times — only sets defaults on first run.
    """
    defaults = {
        "messages":          [],       # List of chat message dicts
        "offline_cache":     {},       # Dict of {query: ai_response} for offline use
        "selected_language": "English",
        "selected_topic":    "General",
        "offline_mode":      False,
        "prefill_query":     "",       # Pre-filled query from topic button clicks
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_message(role: str, content: str, timestamp: str,
                topic: str = "", language: str = "", cached: bool = False):
    """
    Append a message to the session chat history.

    Args:
        role      : 'user' or 'assistant'
        content   : Message text (markdown)
        timestamp : Human-readable datetime string
        topic     : Farming topic category (for user messages)
        language  : Selected language (for user messages)
        cached    : True if this is a cached offline response
    """
    st.session_state.messages.append({
        "role":      role,
        "content":   content,
        "timestamp": timestamp,
        "topic":     topic,
        "language":  language,
        "cached":    cached,
    })


def cache_response(query: str, response: str):
    """Save a query-response pair to the offline cache."""
    st.session_state.offline_cache[query] = response


def clear_chat():
    """Clear all chat messages and reset prefill."""
    st.session_state.messages = []
    st.session_state.prefill_query = ""
