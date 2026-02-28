"""
config/settings.py
──────────────────
App-wide constants, Streamlit page configuration, and static text blobs.
Keep all magic strings and configuration values here — never scatter them
across modules.
"""

import streamlit as st


# ── Conversation Stages ────────────────────────────────────────────────────────
CONVERSATION_STAGES: list[str] = [
    "greeting",
    "collecting_info",
    "tech_stack",
    "technical_questions",
    "wrap_up",
    "ended",
]

# ── Exit Intent Keywords ───────────────────────────────────────────────────────
EXIT_KEYWORDS: set[str] = {
    "exit", "quit", "bye", "goodbye", "end",
    "stop", "done", "finish", "close", "cancel",
}

# ── Farewell message shown on exit ────────────────────────────────────────────
FAREWELL_MESSAGE: str = """\
Thank you so much for taking the time to speak with us today! 🎉

It was a pleasure learning about your background and experience. Our recruitment \
team will carefully review your profile and reach out within **2–3 business days** \
with next steps.

**What happens next:**
- Your responses will be reviewed by our recruitment team
- A recruiter will contact you at the email/phone you provided
- If there's a match, you'll be invited for a formal interview

**Best of luck** in your job search — we look forward to potentially working together! 🚀

*This screening session has ended. Click **Start Over** in the sidebar to begin a new session.*
"""

# ── Streamlit Page Config ──────────────────────────────────────────────────────
def set_page() -> None:
    """
    Configure the Streamlit page.
    MUST be called as the very first Streamlit command — before any other
    st.* call or widget render.
    """
    st.set_page_config(
        page_title="TalentScout | AI Hiring Assistant",
        page_icon="🎯",
       layout="wide",                       
       initial_sidebar_state="collapsed",   
    )
