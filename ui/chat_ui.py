"""
ui/chat_ui.py
─────────────
Chat bubble rendering with accuracy badges on user answers.
"""

import streamlit as st


def render_header(stage_label: str, progress: int) -> None:
    """Render the sticky branded header and animated progress bar."""
    st.markdown(f"""
    <div class="ts-header">
        <div class="ts-logo">TalentScout <span>AI</span></div>
        <div class="ts-status">
            <span class="status-dot"></span>Hiring Assistant · Active
        </div>
    </div>
    <div class="ts-progress">
        <div class="progress-label">
            <span>{stage_label}</span>
            <span>{progress}%</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {progress}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_topbar(stage_label: str, progress: int) -> None:
    """Render the top bar (used in two-column layout)."""
    st.markdown(f"""
    <div class="ts-topbar">
      <div class="ts-topbar-logo">TalentScout <span>AI Hiring Assistant</span></div>
      <div class="ts-topbar-status">
        <span class="status-dot"></span> {stage_label} · {progress}%
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_message(role: str, content: str, timestamp: str = "", accuracy: int = None) -> None:
    """
    Render a single chat bubble.

    Parameters
    ----------
    role     : 'assistant' or 'user'
    content  : message text
    timestamp: HH:MM string
    accuracy : 0-100 score shown only on user messages during tech questions
    """
    is_user = role == "user"
    avatar_html = (
        '<div class="msg-avatar user">You</div>'
        if is_user else
        '<div class="msg-avatar bot">TS</div>'
    )
    bubble_cls = "user" if is_user else "bot"
    row_cls    = "user" if is_user else ""

    content_html = content.replace("\n", "<br>")
    time_html    = f'<span class="msg-time">{timestamp}</span>' if timestamp else ""

    # Accuracy badge logic
    badge_html = ""
    if is_user and accuracy is not None:
        if accuracy >= 75:
            cls, icon = "high", "✓"
        elif accuracy >= 45:
            cls, icon = "mid", "~"
        else:
            cls, icon = "low", "✗"
        badge_html = f'<span class="acc-badge {cls}">{icon} {accuracy}% accuracy</span>'

    meta_html = f'<div class="msg-meta">{time_html}{badge_html}</div>' if (time_html or badge_html) else ""

    st.markdown(f"""
    <div class="msg-row {row_cls}">
      {avatar_html}
      <div class="msg-body">
        <div class="bubble {bubble_cls}">{content_html}</div>
        {meta_html}
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_ended_banner() -> None:
    """Render the completion banner shown when a session ends."""
    st.markdown("""
    <div class="ended-banner">
      <h3>✓ Screening Complete</h3>
      <p>
        Thank you for your time. Our team will review your profile and reach out
        within <strong>2–3 business days</strong>.<br>
        Click <strong>Start Over</strong> in the sidebar to begin a new session.
      </p>
    </div>
    """, unsafe_allow_html=True)
