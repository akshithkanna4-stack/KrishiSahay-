# ============================================================
# AgriAssist AI — ai_engine.py
# Claude API integration + offline cache search
# ============================================================

import os
import anthropic
import streamlit as st
from config import CLAUDE_MODEL, MAX_TOKENS, HISTORY_WINDOW, CACHE_MATCH_THRESHOLD, SYSTEM_PROMPT_TEMPLATE


def _get_api_key() -> str | None:
    """Retrieve API key from Streamlit secrets or environment variable."""
    try:
        return st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


def get_ai_response(query: str, language: str, topic: str, history: list) -> str:
    """
    Call the Claude API and return a structured AI response string.

    Args:
        query    : The farmer's question.
        language : Preferred response language.
        topic    : Selected farming topic category.
        history  : List of previous message dicts {role, content}.

    Returns:
        AI response text (markdown formatted).
    """
    api_key = _get_api_key()
    if not api_key:
        return (
            "⚠️ **API Key Missing.**\n\n"
            "Please set `ANTHROPIC_API_KEY` in your environment:\n"
            "```bash\nexport ANTHROPIC_API_KEY=your_key_here\n```\n"
            "Or add it to `.streamlit/secrets.toml`:\n"
            "```toml\nANTHROPIC_API_KEY = \"your_key_here\"\n```"
        )

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Build system prompt with current session context
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(language=language, topic=topic)

        # Build conversation messages (sliding window for token efficiency)
        messages = []
        for msg in history[-HISTORY_WINDOW:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": query})

        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text

    except anthropic.AuthenticationError:
        return (
            "❌ **Authentication Failed.**\n\n"
            "Your API key is invalid or expired. Please check and update it."
        )
    except anthropic.RateLimitError:
        return (
            "⏳ **Rate Limit Reached.**\n\n"
            "Too many requests. Please wait a moment and try again, "
            "or switch to **Offline Mode** in the sidebar."
        )
    except anthropic.APIConnectionError:
        return (
            "🌐 **Connection Error.**\n\n"
            "Cannot reach the AI server. Check your internet connection, "
            "or enable **Offline Mode** to use cached responses."
        )
    except Exception as e:
        return (
            f"⚠️ **Unexpected Error:** `{str(e)}`\n\n"
            "Please try again or switch to Offline Mode."
        )


def search_cache(query: str, cache: dict) -> str | None:
    """
    Search the offline response cache using Jaccard similarity.

    Args:
        query : The farmer's question.
        cache : Dict of {previous_query: ai_response}.

    Returns:
        Cached response string if match found above threshold, else None.
    """
    if not cache:
        return None

    query_words = set(query.lower().split())
    best_match = None
    best_score = 0.0

    for cached_query, cached_response in cache.items():
        cached_words = set(cached_query.lower().split())
        intersection = query_words & cached_words
        union = query_words | cached_words
        score = len(intersection) / len(union) if union else 0.0

        if score > best_score and score >= CACHE_MATCH_THRESHOLD:
            best_score = score
            best_match = cached_response

    return best_match
