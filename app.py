"""
TalentScout — AI Hiring Assistant
Entry point: initialises the app and wires all modules together.
Run with: streamlit run app.py
"""

import streamlit as st
from datetime import datetime

from config.settings import set_page, FAREWELL_MESSAGE
from utils.session import init_session
from utils.validators import detect_exit
from utils.extract_data import extract_candidate_data
from services.llm_service import get_ai_response, score_answer
from services.state_manager import infer_stage, get_stage_progress, get_stage_label
from ui.styles import load_css
from ui.sidebar import render_sidebar
from ui.chat_ui import render_message, render_header, render_ended_banner


def main() -> None:
    """Main application controller."""

    # ── Bootstrap ──────────────────────────────────────────────────────────────
    set_page()
    load_css()
    init_session()
    render_sidebar()

    # ── Header + Progress Bar ──────────────────────────────────────────────────
    progress = get_stage_progress(st.session_state.stage)
    stage_label = get_stage_label(st.session_state.stage)
    render_header(stage_label, progress)

    # ── Auto-Greeting on first load ────────────────────────────────────────────
    if not st.session_state.started:
        st.session_state.started = True
        trigger = {"role": "user", "content": "Hello, I'm here for the screening."}
        st.session_state.messages.append(trigger)

        with st.spinner(""):
            greeting = get_ai_response(st.session_state.messages)

        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.session_state.stage = "greeting"
        st.rerun()

    # ── Render Chat History ────────────────────────────────────────────────────
    st.markdown('<div class="ts-chat">', unsafe_allow_html=True)
    scores = st.session_state.get("scores", {})
    for i, msg in enumerate(st.session_state.messages[1:], start=1):
        accuracy = scores.get(i) if msg["role"] == "user" else None
        render_message(msg["role"], msg["content"], msg.get("time", ""), accuracy)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Ended State ────────────────────────────────────────────────────────────
    if st.session_state.ended:
        render_ended_banner()
        return

    # ── Chat Input ─────────────────────────────────────────────────────────────
    if user_input := st.chat_input("Type your response here…"):
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append(
            {"role": "user", "content": user_input, "time": timestamp}
        )

        # Exit-intent detection
        if detect_exit(user_input):
            st.session_state.messages.append({
                "role": "assistant",
                "content": FAREWELL_MESSAGE,
                "time": timestamp,
            })
            st.session_state.stage = "ended"
            st.session_state.ended = True
            st.rerun()

        # Score answer if in technical questions stage
        msg_index = len(st.session_state.messages) - 1
        if st.session_state.stage == "technical_questions":
            bot_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
            last_question = bot_msgs[-1]["content"] if bot_msgs else ""
            result = score_answer(last_question, user_input)
            if result and "score" in result:
                if "scores" not in st.session_state:
                    st.session_state.scores = {}
                st.session_state.scores[msg_index] = result["score"]

        # Get LLM response
        with st.spinner("TalentScout is thinking…"):
            response = get_ai_response(st.session_state.messages)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "time": datetime.now().strftime("%H:%M"),
        })

        # Update extracted candidate data and conversation stage
        extract_candidate_data(st.session_state.messages)
        st.session_state.stage = infer_stage(st.session_state.messages, st.session_state.stage)

        # Detect if the LLM itself wrapped up the conversation
        if any(phrase in response.lower() for phrase in [
            "recruiter will", "2-3 business days", "2–3 business days",
            "best of luck", "thank you for your time today",
        ]):
            st.session_state.stage = "ended"
            st.session_state.ended = True

        st.rerun()


if __name__ == "__main__":
    main()
