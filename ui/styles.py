"""
ui/styles.py
────────────
All custom CSS for the TalentScout interface.

Keeping styles in a dedicated module means:
  - app.py stays clean and logic-only.
  - Designers can update visuals without touching Python logic.
  - CSS variables are defined once in :root and reused everywhere.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');
/* ── Design Tokens ────────────────────────────────────────────────────── */
:root {
    --bg:          #0d0f14;
    --surface:     #161921;
    --surface2:    #1e2230;
    --border:      #2a2f3d;
    --accent:      #6ee7b7;
    --accent2:     #818cf8;
    --text:        #e2e8f0;
    --text-muted:  #8892a4;
    --user-bubble: #1e2a45;
    --bot-bubble:  #161921;
}

/* ── Copy-Paste Prevention ── */
.ts-chat {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

/* ── Accuracy Badges ── */
.acc-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    border-radius: 99px;
    font-size: 0.68rem;
    font-weight: 600;
}
.acc-badge.high { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
.acc-badge.mid  { background: rgba(250,204,21,0.12);  color: #facc15; border: 1px solid rgba(250,204,21,0.25); }
.acc-badge.low  { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }

/* ── Avatar Ring ── */
.avatar-ring {
    width: 110px; height: 110px;
    border-radius: 50%;
    background: conic-gradient(#2dd4bf var(--prog, 10%), #2a2f3d 0);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 12px;
}
.avatar-inner {
    width: 92px; height: 92px;
    border-radius: 50%;
    background: #161921;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.4rem;
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide default Streamlit chrome ───────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Layout ───────────────────────────────────────────────────────────── */
.main .block-container {
    padding: 0 !important;
    max-width: 820px !important;
    margin: 0 auto;
}

/* ── Header ───────────────────────────────────────────────────────────── */
.ts-header {
    background: linear-gradient(135deg, #0d0f14 0%, #161921 100%);
    border-bottom: 1px solid var(--border);
    padding: 20px 32px 16px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.ts-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--accent);
    letter-spacing: -0.5px;
}
.ts-logo span { color: var(--text-muted); font-style: italic; }
.ts-status {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 2px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    margin-right: 6px;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── Progress Bar ─────────────────────────────────────────────────────── */
.ts-progress {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 12px 32px;
}
.progress-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
}
.progress-bar-bg {
    background: var(--border);
    border-radius: 99px;
    height: 4px;
    overflow: hidden;
}
.progress-bar-fill {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 99px;
    height: 100%;
    transition: width 0.6s ease;
}

/* ── Chat Area ────────────────────────────────────────────────────────── */
.ts-chat {
    padding: 28px 32px;
    min-height: 60vh;
}

/* ── Message Bubbles ──────────────────────────────────────────────────── */
.msg-wrap { display: flex; margin-bottom: 20px; align-items: flex-start; gap: 12px; }
.msg-wrap.user { flex-direction: row-reverse; }

.avatar {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    font-family: 'DM Serif Display', serif;
}
.avatar.bot  { background: linear-gradient(135deg, #1a2e2a, #0d1f1b); border: 1px solid var(--accent);  color: var(--accent); }
.avatar.user { background: linear-gradient(135deg, #1a1e35, #0d1120); border: 1px solid var(--accent2); color: var(--accent2); }

.bubble {
    max-width: 78%;
    padding: 14px 18px;
    border-radius: 16px;
    font-size: 0.93rem;
    line-height: 1.65;
}
.bubble.bot  { background: var(--bot-bubble);  border: 1px solid var(--border);  border-top-left-radius: 4px;  color: var(--text); }
.bubble.user { background: var(--user-bubble); border: 1px solid #2a3a5e;        border-top-right-radius: 4px; color: var(--text); }

.bubble p:last-child { margin-bottom: 0; }
.bubble strong { color: var(--accent); font-weight: 600; }
.bubble em { color: var(--text-muted); }
.bubble code {
    background: var(--surface2);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
    color: var(--accent);
    font-family: 'SF Mono', 'Fira Code', monospace;
}

.msg-time { font-size: 0.68rem; color: var(--text-muted); margin-top: 5px; text-align: right; }
.msg-wrap.user .msg-time { text-align: left; }

/* ── Ended Banner ─────────────────────────────────────────────────────── */
.ended-banner {
    background: linear-gradient(135deg, #1a2e2a, #161921);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    margin: 24px 32px;
}
.ended-banner h3 { font-family: 'DM Serif Display', serif; color: var(--accent); margin: 0 0 8px; }
.ended-banner p  { color: var(--text-muted); margin: 0; font-size: 0.9rem; }

/* ── Sidebar ──────────────────────────────────────────────────────────── */
div[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
.info-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.85rem;
}
.info-card .label { color: var(--text-muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; }
.info-card .value { color: var(--text); font-weight: 500; margin-top: 3px; }
.sidebar-title {
    font-family: 'DM Serif Display', serif;
    color: var(--accent);
    font-size: 1.05rem;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* ── Chat Input ───────────────────────────────────────────────────────── */
.stChatInput > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
.stChatInput > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(110, 231, 183, 0.08) !important;
}
.stChatInput input { color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }

</style>
<script>
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('copy', function(e) {
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') e.preventDefault();
    });
    document.addEventListener('contextmenu', function(e) {
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') e.preventDefault();
    });
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.ctrlKey && ['c','a','x'].includes(e.key.toLowerCase())) e.preventDefault();
    });
});
</script>


</style>
"""


def load_css() -> None:
    """Inject the custom stylesheet into the Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)
