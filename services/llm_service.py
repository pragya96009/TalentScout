"""
Handles all communication with the Groq API (free tier).
"""
from dotenv import load_dotenv
load_dotenv()

import json
import streamlit as st
from groq import Groq, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError


from config.prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()

_MODEL      = "llama-3.3-70b-versatile"   
_MAX_TOKENS = 1024


def get_ai_response(messages: list[dict]) -> str:
    """
    Send the conversation history to Groq and return the assistant reply.

    Parameters
    ----------
    messages : list[dict]
        Full conversation history. Extra keys (e.g. 'time') are stripped.

    Returns
    -------
    str
        The assistant's text response, or a user-friendly error string.
    """
    client = Groq()  

  
    system = SYSTEM_PROMPT.format(
        stage=st.session_state.get("stage", "greeting"),
        candidate_data=json.dumps(
            st.session_state.get("candidate_data", {}), indent=2
        ),
    )

    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
    ]

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=[{"role": "system", "content": system}, *api_messages],
        )
        return response.choices[0].message.content

    except AuthenticationError:
        return (
            "⚠️ Authentication failed. Please check that your "
            "`GROQ_API_KEY` environment variable is set correctly."
        )
    except RateLimitError:
        return "⚠️ Rate limit reached. Please wait a moment and try again."
    except APIConnectionError:
        return (
            "⚠️ Could not reach the Groq API. "
            "Please check your internet connection and try again."
        )
    except APIStatusError as exc:
        return f"⚠️ API error ({exc.status_code}): {str(exc.message)[:120]}. Please try again."

_SCORE_PROMPT = """You are a technical interviewer. Score this answer strictly.
Question: {question}
Answer: {answer}
Respond ONLY with valid JSON, no other text:
{{"score": <integer 0-100>, "feedback": "<one sentence>"}}"""

def score_answer(question: str, answer: str) -> dict | None:
    """Score a candidate's technical answer. Returns dict with 'score' key or None."""
    client = Groq()
    try:
        response = client.chat.completions.create(
            model=_MODEL,
            max_tokens=80,
            temperature=0.1,
            messages=[{"role": "user", "content": _SCORE_PROMPT.format(
                question=question, answer=answer
            )}],
        )
        raw = response.choices[0].message.content.strip().replace("```json","").replace("```","")
        return json.loads(raw)
    except Exception:
        return None