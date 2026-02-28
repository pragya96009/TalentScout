"""
utils/session.py
────────────────
Streamlit session-state initialisation.

All keys used anywhere in the app are declared here so every module can
safely read session_state without KeyError guards scattered everywhere.
"""

import streamlit as st


def init_session(scores: dict = None) -> None:
    """
    Initialise all session-state keys with safe defaults.

    Called once per page load from app.py. Subsequent calls are no-ops
    because each block checks for key existence before writing.
    """
    defaults: dict = {
        "messages":       [],    
        "candidate_data": {},   
        "stage":          "greeting",
        "ended":          False,
        "started":        False,
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
