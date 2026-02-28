"""
ui/sidebar.py
─────────────
Renders the sidebar panel containing:
  - Avatar with conic-gradient progress ring
  - Live candidate profile (updates as data is extracted)
  - Current session stage
  - "Start Over" reset button
  - Privacy notice
"""

import streamlit as st
from services.state_manager import get_stage_progress, get_stage_label

_PROFILE_FIELDS: list[tuple[str, str]] = [
    ("Name",       "full_name"),
    ("Email",      "email"),
    ("Phone",      "phone"),
    ("Experience", "years_experience"),
    ("Position",   "desired_position"),
    ("Location",   "location"),
    ("Tech Stack", "tech_stack"),
]


def render_sidebar() -> None:
    with st.sidebar:
        data     = st.session_state.get("candidate_data", {})
        stage    = st.session_state.get("stage", "greeting")
        progress = get_stage_progress(stage)
        name     = data.get("full_name", "Candidate")
        position = data.get("desired_position", "Tech Role")

        # Avatar with conic-gradient progress ring
        st.markdown(f"""
        <div style="text-align:center;padding:16px 0 8px">
          <div class="avatar-ring" style="--prog:{progress}%">
            <div class="avatar-inner">🧑‍💼</div>
          </div>
          <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0">{name}</div>
          <div style="font-size:0.72rem;color:#2dd4bf;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px">{position}</div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div style="margin-bottom:16px">
          <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#64748b;margin-bottom:5px">
            <span>{get_stage_label(stage)}</span><span>{progress}%</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{progress}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(
            '<p style="font-size:0.68rem;color:#64748b;text-transform:uppercase;'
            'letter-spacing:0.09em;margin-bottom:10px;">Candidate Profile</p>',
            unsafe_allow_html=True
        )

        # Profile fields
        if data:
            for label, key in _PROFILE_FIELDS:
                value = data.get(key)
                if value:
                    if isinstance(value, list):
                        value = ", ".join(value)
                    st.markdown(f"""
                    <div class="info-card">
                        <div class="label">{label}</div>
                        <div class="value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<p style="color:#64748b;font-size:0.85rem;">'
                "Profile will fill in as you chat.</p>",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Session info
        msg_count = len(st.session_state.get("messages", []))
        st.markdown(
            f'<p style="color:#64748b;font-size:0.8rem;">'
            f"Messages exchanged: {max(0, msg_count - 1)}</p>",
            unsafe_allow_html=True,
        )

        # Reset button
        if st.button("↺  Start Over", use_container_width=True):
            _reset_session()
            st.rerun()

        # Privacy notice
        st.markdown("""
        <div style="margin-top:12px;font-size:0.68rem;color:#64748b;
                    line-height:1.65;text-align:center;padding-top:12px;
                    border-top:1px solid #232840;">
            🔒 Data handled per GDPR standards.<br>
            Type <code>exit</code> to end session.
        </div>
        """, unsafe_allow_html=True)


def _reset_session() -> None:
    """Clear all session-state keys to start a fresh screening."""
    for key in ["messages", "candidate_data", "stage", "ended", "started", "scores"]:
        st.session_state.pop(key, None)
