
# TalentScout
=======
GITHUT LINK: https://github.com/pragya96009/TalentScout


# 🎯 TalentScout — AI Hiring Assistant

A conversational hiring assistant that handles the first round of candidate screening automatically. It collects candidate details, figures out their tech stack, and fires off relevant technical questions — all through a chat interface.

Built with Streamlit + Groq (LLaMA 3.3 70B).

---

## What It Does

1. Greets the candidate and explains the process
2. Collects name, email, phone, experience, desired role, location, and tech stack
3. Generates 3–5 technical questions per technology declared
4. Scores each answer (0–100%) and shows a live accuracy badge
5. Wraps up and informs the candidate about next steps

The sidebar tracks the candidate's profile in real time as the conversation progresses, and a progress ring shows how far along the screening is.

---

## Project Structure

```
talentscout/
├── app.py                  ← Entry point
├── requirements.txt
├── .env                    ← Your GROQ_API_KEY goes here (never commit this)
├── .gitignore
│
├── config/
│   ├── settings.py         ← Page config, exit keywords, farewell message
│   └── prompt.py           ← System prompt with stage + candidate data injection
│
├── services/
│   ├── llm_service.py      ← Groq API calls + answer scoring
│   └── state_manager.py    ← Stage transitions, progress %, labels
│
├── utils/
│   ├── session.py          ← Session state init
│   ├── validators.py       ← Exit intent detection
│   └── extract_data.py     ← Regex extraction of candidate fields
│
└── ui/
    ├── styles.py           ← All CSS
    ├── chat_ui.py          ← Chat bubbles, header, ended banner
    └── sidebar.py          ← Avatar ring, profile panel, reset button
```

---

## Setup

**Requirements:** Python 3.9+, a free Groq API key from [console.groq.com](https://console.groq.com)

```bash
# Clone the repo
git clone https://github.com/your-username/talentscout.git
cd talentscout

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
# Create a .env file in the project root with this line:
# GROQ_API_KEY=your-key-here

# Run
streamlit run app.py
```

App opens at `http://localhost:8501`.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key — get one free at console.groq.com |

Store it in a `.env` file at the project root. The app loads it automatically via `python-dotenv`. Never commit this file.

---

## Key Features

**Accuracy Scoring** — During the technical questions stage, each candidate answer is scored by a separate LLM call and displayed as a badge (✓ green / ~ yellow / ✗ red) under the message bubble.

**Copy-Paste Prevention** — Right-click and keyboard shortcuts (Ctrl+C, Ctrl+A, Ctrl+X) are disabled on the chat area to keep the assessment honest. The input box itself is unaffected.

**Live Profile Sidebar** — Candidate details populate the sidebar in real time as they're mentioned in conversation. An avatar ring fills up with the screening progress percentage.

**Graceful Exit** — Typing `exit`, `quit`, `bye`, or similar ends the session cleanly with a summary message.

---

## How the Prompt Works

The system prompt in `config/prompt.py` is injected with two runtime values on every API call:

- `{stage}` — the current conversation stage so the model knows what it should be doing
- `{candidate_data}` — everything collected so far so the model doesn't re-ask for it

This is what keeps the conversation coherent across turns without a database.

---

## Data & Privacy

- No candidate data is written to disk
- Everything lives in Streamlit's `session_state` and clears on page refresh
- Data is sent to Groq's API for inference only — governed by their [privacy policy](https://groq.com/privacy-policy)
- For a production deployment, add explicit consent collection before the screening starts

---

## Requirements

```
groq>=0.9.0
streamlit>=1.40.0
python-dotenv>=1.0.0
```

---

## Challenges Worth Mentioning

**Stage management** — Streamlit reruns the entire script on every interaction, so there's no persistent state between turns. Stage is inferred from recent message content rather than stored server-side.

**Keeping the LLM on topic** — Without strong guardrails in the system prompt, the model tends to drift into general conversation. The prompt explicitly handles off-topic inputs with redirect instructions.

**Answer scoring reliability** — The scoring call uses `temperature=0.1` and strict JSON-only output instructions to keep results consistent. A try/except wraps it so a failed score never crashes the main conversation.
```
>>>>>>> ef9bfec (Pragya Pathak)
