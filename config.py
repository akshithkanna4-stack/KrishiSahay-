# ============================================================
# AgriAssist AI — config.py
# App-wide constants and configuration
# ============================================================

# ── Streamlit page config ──
PAGE_CONFIG = {
    "page_title": "AgriAssist AI 🌾",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ── Claude model ──
CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1500
HISTORY_WINDOW = 6          # Number of past messages to include in API call
CACHE_MATCH_THRESHOLD = 0.25  # Jaccard similarity threshold for offline cache

# ── Supported languages ──
LANGUAGES = [
    "English", "Hindi", "Telugu", "Tamil",
    "Kannada", "Marathi", "Bengali", "Punjabi"
]

# ── Quick topic buttons: label → (topic_name, starter_prompt) ──
TOPICS = {
    "🌾 Crops": (
        "Crops",
        "I have a question about growing crops. Can you help me with best practices, seed selection, and seasonal guidance?"
    ),
    "🐛 Pests & Diseases": (
        "Pests & Diseases",
        "I'm facing a pest or disease problem in my crop. Can you help identify it and suggest treatment?"
    ),
    "💧 Fertilizers": (
        "Fertilizers",
        "I need advice on fertilizers — which type, quantity, and timing for my crop?"
    ),
    "📋 Gov. Schemes": (
        "Government Schemes",
        "What government schemes and subsidies are available for farmers like me?"
    ),
    "🌦️ Weather Advisory": (
        "Weather Advisory",
        "Can you give me weather-based farming advisory and tips for the current season?"
    ),
    "🌱 Organic Farming": (
        "Organic Farming",
        "I want to learn about organic farming methods and how to transition to organic agriculture."
    ),
}

# ── Offline FAQ fallback questions ──
FAQS = [
    "How to treat yellowing leaves in crops?",
    "Best fertilizer for wheat crop?",
    "How to control pests in tomato plants?",
    "What is PM-KISAN scheme and who is eligible?",
    "What is the cost of drip irrigation and any subsidy?",
]

# ── Footer resource links ──
FOOTER_LINKS = [
    ("🏛️ KVK Portal", "https://kvk.icar.gov.in"),
    ("💰 PM-KISAN",    "https://pmkisan.gov.in"),
    ("🛒 eNAM",        "https://www.enam.gov.in"),
    ("📊 Agmarknet",   "https://agmarknet.gov.in"),
    ("🛡️ PMFBY",       "https://pmfby.gov.in"),
]

# ── System prompt template (format with language & topic) ──
SYSTEM_PROMPT_TEMPLATE = """You are AgriAssist, an expert agricultural AI assistant dedicated to helping Indian farmers.

Your expertise covers: crops, seeds, soil health, irrigation, pest & disease management, fertilizers (organic & chemical), post-harvest, government schemes, and market prices.

**Current session settings:**
- Farmer's preferred language: {language}
- Query topic category: {topic}

**Response rules:**
1. If the farmer's language is not English, respond fully in that language (use Devanagari/native script where appropriate).
2. Always structure answers using these sections (use bold headers):
   - 🔍 **Problem Summary**
   - 🌿 **Cause / Reason**
   - ✅ **Solution (Step-by-step)**
   - 💡 **Preventive Tips**
   - 📋 **Relevant Government Schemes** (if applicable — mention PM-KISAN, PMFBY, Kisan Credit Card, eNAM, Pradhan Mantri Krishi Sinchai Yojana, etc.)
3. Keep language simple, practical, and jargon-free — as if talking to a farmer in a village.
4. Mention approximate costs in INR (₹) wherever helpful.
5. If the question is about pests or disease, suggest both chemical and organic/natural remedies.
6. Always end with one encouraging line for the farmer.
7. Do not hallucinate — if unsure, suggest visiting the nearest Krishi Vigyan Kendra (KVK)."""
