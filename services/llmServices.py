"""
To Handle Communication with the Anthropic API (Claude 3.5 Sonnet). --> Future replacement for llm_service.py as it it Paid

"""
import anthropic
import json
from config.prompt import SYSTEM_PROMPT
import streamlit as st

def get_ai_response(messages):
    client = anthropic.Anthropic()

    system = SYSTEM_PROMPT.format(
        stage=st.session_state.stage,
        candidate_data=json.dumps(st.session_state.candidate_data)
    )

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=system,
        messages=messages
    )

    return response.content[0].text
