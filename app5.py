# app4.py

import streamlit as st
import requests
from dotenv import load_dotenv
import os

# ── Load environment variables ───────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("WAQI_API_KEY")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India AQI Monitor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ─────────────────────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.block-container {
    padding: 2.5rem 3rem 2rem 3rem !important;
    max-width: 1200px !important;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.app-header { margin-bottom: 2rem; }
.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem; font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-color);
    line-height: 1.1; margin: 0;
}
.app-subtitle {
    font-size: 0.95rem;
    color: var(--text-color);
    opacity: 0.55;
    margin-top: 0.4rem; font-weight: 300; letter-spacing: 0.01em;
}

/* ── Search label ────────────────────────────────────────────────────────── */
.search-label {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-color);
    opacity: 0.5;
    margin-bottom: 0.5rem;
}

/* ── Search input — dark mode (default) ──────────────────────────────────── */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: var(--text-color) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important; padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(99,220,169,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,220,169,0.08) !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: var(--text-color) !important;
    opacity: 0.35 !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #63dca9, #3ab88a) !important;
    color: #0a0a0a !important; border: none !important;
    border-radius: 10px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.9rem !important;
    letter-spacing: 0.04em !important; padding: 0.75rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover { opacity: 0.85 !important; }
div[data-testid="stButton"] button:not([kind="primary"]) {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(128,128,128,0.18) !important;
    border-radius: 10px !important;
    color: var(--text-color) !important;
    opacity: 0.8;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important;
    text-align: left !important; justify-content: flex-start !important;
    padding: 0.6rem 1rem !important; transition: all 0.15s !important; width: 100% !important;
}
div[data-testid="stButton"] button:not([kind="primary"]):hover {
    background: rgba(99,220,169,0.1) !important;
    border-color: rgba(99,220,169,0.35) !important;
    color: #2d9e6e !important;
    opacity: 1 !important;
}

/* ── Note box ────────────────────────────────────────────────────────────── */
.note-box {
    background: rgba(255,200,87,0.07); border-left: 3px solid #e8b84b;
    border-radius: 0 8px 8px 0; padding: 0.6rem 1rem;
    font-size: 0.82rem; color: #c9a040; margin: 0.75rem 0 1.25rem 0; line-height: 1.5;
}

/* ── AQI main card — dark mode (default) ─────────────────────────────────── */
.aqi-main-card {
    background: linear-gradient(160deg, #141e30 0%, #0d1b2a 60%, #0a1628 100%);
    border: 1px solid rgba(255,255,255,0.07); border-radius: 20px;
    padding: 2.5rem 2rem; position: relative; overflow: hidden;
}
.aqi-main-card::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, var(--aqi-glow, rgba(99,220,169,0.12)) 0%, transparent 70%);
    pointer-events: none;
}
.aqi-station {
    font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(255,255,255,0.4); font-family: 'Syne', sans-serif; margin-bottom: 1rem;
}
.aqi-big-number {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3.5rem, 15vw, 5.5rem);
    font-weight: 800; line-height: 1; letter-spacing: -0.04em; white-space: nowrap;
}
.aqi-card-label {
    font-size: 0.72rem; color: rgba(255,255,255,0.3); letter-spacing: 0.1em;
    text-transform: uppercase; margin-top: 0.2rem; font-family: 'Syne', sans-serif;
}
.aqi-category-badge {
    display: inline-flex; align-items: center; gap: 0.4rem; margin-top: 0.75rem;
    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.82rem;
    font-weight: 600; font-family: 'Syne', sans-serif; letter-spacing: 0.02em;
}

/* ── Info cards — dark mode (default) ────────────────────────────────────── */
.feedback-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1.25rem 1.5rem;
}
.feedback-card-title {
    font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(255,255,255,0.35); margin-bottom: 0.6rem;
}
.feedback-card-text { font-size: 0.95rem; color: rgba(255,255,255,0.78); line-height: 1.6; }
.eco-card {
    background: rgba(99,220,169,0.06); border: 1px solid rgba(99,220,169,0.18);
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-top: 1rem;
}
.eco-card-title {
    font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(99,220,169,0.6); margin-bottom: 0.6rem;
}
.eco-card-text { font-size: 0.95rem; color: rgba(255,255,255,0.78); line-height: 1.6; }

/* ── Stat boxes — dark mode (default) ────────────────────────────────────── */
.stat-box {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1rem; text-align: center;
}
.stat-val {
    font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700;
    color: var(--text-color); line-height: 1;
}
.stat-key {
    font-size: 0.7rem; color: var(--text-color); opacity: 0.45;
    letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.3rem;
}

/* ── Misc ────────────────────────────────────────────────────────────────── */
.dym-header {
    font-family: 'Syne', sans-serif; font-size: 0.75rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--text-color); opacity: 0.4;
    margin: 1.5rem 0 0.75rem 0;
}
.thin-divider {
    border: none; border-top: 1px solid rgba(128,128,128,0.12); margin: 1.5rem 0;
}
.app-footer { font-size: 0.75rem; color: var(--text-color); opacity: 0.28; margin-top: 2.5rem; }

/* ════════════════════════════════════════════════════════════════════════════
   LIGHT MODE OVERRIDES
   Uses prefers-color-scheme: light. Streamlit also applies the theme via its
   own CSS variables, so we target both the OS media query and Streamlit's
   data-theme attribute to ensure reliable detection in all browsers.
   ════════════════════════════════════════════════════════════════════════════ */
@media (prefers-color-scheme: light) {

    /* ── Search input ──────────────────────────────────────────────────────── */
    div[data-testid="stTextInput"] input {
        background: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.14) !important;
        color: #1a1a1a !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #1a1a1a !important;
        opacity: 0.38 !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(42,158,100,0.55) !important;
        box-shadow: 0 0 0 3px rgba(42,158,100,0.09) !important;
    }

    /* ── AQI main card ─────────────────────────────────────────────────────── */
    .aqi-main-card {
        background: linear-gradient(160deg, #f0f7f4 0%, #e8f5ef 60%, #dff2ea 100%);
        border: 1px solid rgba(0,0,0,0.07);
    }
    .aqi-station { color: rgba(0,0,0,0.45); }
    .aqi-card-label { color: rgba(0,0,0,0.35); }

    /* ── Feedback card ─────────────────────────────────────────────────────── */
    .feedback-card {
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.08);
    }
    .feedback-card-title { color: rgba(0,0,0,0.4); }
    .feedback-card-text { color: rgba(0,0,0,0.78); }

    /* ── Eco card ──────────────────────────────────────────────────────────── */
    .eco-card {
        background: rgba(42,158,100,0.06);
        border: 1px solid rgba(42,158,100,0.2);
    }
    .eco-card-title { color: rgba(28,120,75,0.75); }
    .eco-card-text { color: rgba(0,0,0,0.75); }

    /* ── Stat boxes ────────────────────────────────────────────────────────── */
    .stat-box {
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.08);
    }

    /* ── AQI scale reference table ─────────────────────────────────────────── */
    .aqi-table-wrap table { color: rgba(0,0,0,0.75) !important; }
    .aqi-table-wrap thead tr { border-bottom: 1px solid rgba(0,0,0,0.1) !important; }
    .aqi-table-wrap th { color: rgba(0,0,0,0.45) !important; }
    .aqi-table-wrap td { color: rgba(0,0,0,0.72) !important; }

    /* ── Note box ──────────────────────────────────────────────────────────── */
    .note-box {
        background: rgba(232,184,75,0.1);
        color: #7a5c10;
    }
}

/* ════════════════════════════════════════════════════════════════════════════
   MOBILE RESPONSIVE  (≤ 768 px)
   Streamlit renders columns as flex children. On mobile we override that flex
   layout so every column becomes a full-width block stacked vertically.
   ════════════════════════════════════════════════════════════════════════════ */
@media (max-width: 768px) {

    /* Tighten global page padding so content breathes on small screens */
    .block-container {
        padding: 1.2rem 1rem 1.5rem 1rem !important;
    }

    /* ── Force ALL Streamlit column rows to stack vertically ───────────────
       Streamlit wraps columns in a [data-testid="stHorizontalBlock"] div.
       Setting flex-direction: column makes every child column take 100% width.
    ── */
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 0 !important;
    }

    /* Each column child should fill the full width */
    [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* ── Header: compact on mobile ─────────────────────────────────────── */
    .app-title { font-size: 2rem; }
    .app-subtitle { font-size: 0.88rem; }
    .app-header { margin-bottom: 1rem; }
    .thin-divider { margin: 1rem 0; }

    /* ── AQI hero number: use vw so it fills the card nicely ──────────── */
    .aqi-big-number { font-size: clamp(4rem, 22vw, 5.5rem) !important; }

    /* ── AQI main card: tighter padding on mobile ─────────────────────── */
    .aqi-main-card { padding: 1.75rem 1.25rem; }

    /* ── Info cards side-by-side row stacks to single column ──────────── */
    .feedback-card, .eco-card { padding: 1rem 1.1rem; }

    /* ── Stat row: 3 cols on mobile is too cramped → make them wrap ───── */
    /* The 3-column stat row uses Streamlit columns; after the global stack
       override above they will each be 100% wide. We give them back a
       compact 3-column grid using a wrapper we inject via the stat-row div */
    .stat-row-mobile {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin-top: 0;
    }
    /* Shrink stat text slightly so 3 cols fit on narrow screens */
    .stat-val { font-size: 1.15rem !important; }
    .stat-key { font-size: 0.62rem !important; }

    /* ── Suggestion buttons: comfortable tap target ───────────────────── */
    div[data-testid="stButton"] button:not([kind="primary"]) {
        padding: 0.75rem 1rem !important;
        font-size: 0.92rem !important;
    }

    /* ── Text inputs: bigger touch target ─────────────────────────────── */
    div[data-testid="stTextInput"] input {
        font-size: 1rem !important;
        padding: 0.85rem 1rem !important;
    }

    /* ── Search button: full-width & chunky ───────────────────────────── */
    div[data-testid="stButton"] button[kind="primary"] {
        padding: 0.9rem 1.5rem !important;
        font-size: 1rem !important;
    }

    /* ── Note box: slightly smaller text ──────────────────────────────── */
    .note-box { font-size: 0.78rem; padding: 0.5rem 0.9rem; }

    /* ── Footer: less top margin on mobile ────────────────────────────── */
    .app-footer { margin-top: 1.5rem; }
}

/* ── Tablet tweaks (769–1024 px) ─────────────────────────────────────────── */
@media (min-width: 769px) and (max-width: 1024px) {
    .block-container { padding: 2rem 2rem 2rem 2rem !important; }
    .app-title { font-size: 2.2rem; }
    .aqi-big-number { font-size: clamp(3rem, 8vw, 4.5rem) !important; }
}
</style>
""", unsafe_allow_html=True)


# ── AQI metadata ──────────────────────────────────────────────────────────────
def get_aqi_meta(aqi: int) -> dict:
    if aqi <= 50:
        return {
            "color": "#63dca9", "bg": "rgba(99,220,169,0.15)", "glow": "rgba(99,220,169,0.15)",
            "category": "Good", "emoji": "😊", "safety": "✅ Safe",
            "advice": "Great news! Air quality is excellent. Enjoy outdoor activities freely — no restrictions apply.",
            "eco_task": "🚲 Opt for a bicycle ride or a walk today — the air is perfect for it!",
        }
    elif aqi <= 100:
        return {
            "color": "#f7d060", "bg": "rgba(247,208,96,0.15)", "glow": "rgba(247,208,96,0.12)",
            "category": "Moderate", "emoji": "🙂", "safety": "⚠️ Mostly Safe",
            "advice": "Air quality is acceptable for most people. Unusually sensitive individuals should consider reducing prolonged outdoor exertion.",
            "eco_task": "🚌 Choose public transport or carpool today to help keep the air cleaner for everyone.",
        }
    elif aqi <= 150:
        return {
            "color": "#f4a34e", "bg": "rgba(244,163,78,0.15)", "glow": "rgba(244,163,78,0.12)",
            "category": "Unhealthy for Sensitive Groups", "emoji": "😷", "safety": "⚠️ Caution",
            "advice": "If you have respiratory or heart conditions, wear a mask when stepping outdoors. Healthy individuals can generally remain active.",
            "eco_task": "🪴 Place an air-purifying indoor plant like a Snake Plant or Peace Lily near your workspace.",
        }
    elif aqi <= 200:
        return {
            "color": "#ef5350", "bg": "rgba(239,83,80,0.15)", "glow": "rgba(239,83,80,0.12)",
            "category": "Unhealthy", "emoji": "😨", "safety": "🚫 Wear a Mask",
            "advice": "Everyone may begin to experience health effects. Wear a mask outdoors and reduce prolonged or heavy outdoor exertion.",
            "eco_task": "🚗 Carpool or switch to public transport to help cut vehicle emissions in your city.",
        }
    elif aqi <= 300:
        return {
            "color": "#ce93d8", "bg": "rgba(206,147,216,0.15)", "glow": "rgba(206,147,216,0.12)",
            "category": "Very Unhealthy", "emoji": "🚨", "safety": "🚫 Stay Indoors",
            "advice": "Health warnings in effect. Avoid all outdoor activities. Keep windows closed and use air purifiers if available.",
            "eco_task": "🌳 Be the change — pledge to plant a tree in your neighbourhood this weekend.",
        }
    else:
        return {
            "color": "#ff5252", "bg": "rgba(255,82,82,0.15)", "glow": "rgba(255,82,82,0.12)",
            "category": "Hazardous", "emoji": "☠️", "safety": "🚫 Emergency",
            "advice": "Serious health emergency. Everyone should stay indoors, seal gaps in windows and doors, and avoid any outdoor exposure.",
            "eco_task": "📢 Spread awareness — share today's AQI with family and neighbours, and urge local authorities to act on pollution sources.",
        }


# ── API helpers ───────────────────────────────────────────────────────────────
def _safe_aqi(raw) -> int | None:
    try:
        return int(str(raw).strip())
    except (ValueError, TypeError):
        return None


def search_stations(keyword: str, api_key: str) -> tuple[list, list]:
    query = f"{keyword.strip()}, India"
    url = (
        "https://api.waqi.info/search/"
        f"?token={api_key}&keyword={requests.utils.quote(query)}"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            return [], []

        exact, fuzzy = [], []
        kw_lower = keyword.strip().lower()

        for item in data.get("data", []):
            station_info = item.get("station", {})
            name = station_info.get("name", "")
            uid = item.get("uid")
            aqi_raw = item.get("aqi", "-")
            name_lower = name.lower()
            country = station_info.get("country", "").upper()

            if country and country != "IN":
                continue

            entry = {"uid": uid, "name": name, "aqi": _safe_aqi(aqi_raw)}
            if kw_lower in name_lower:
                exact.append(entry)
            else:
                fuzzy.append(entry)

        return exact, fuzzy

    except requests.exceptions.RequestException:
        return [], []


def fetch_by_geo(keyword: str, api_key: str) -> dict | None:
    feed_url = (
        "https://api.waqi.info/feed/"
        f"{requests.utils.quote(keyword.strip() + ', India')}"
        f"/?token={api_key}"
    )
    try:
        resp = requests.get(feed_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "ok":
            d = data["data"]
            return {"aqi": _safe_aqi(d.get("aqi")), "city": d["city"]["name"]}
    except requests.exceptions.RequestException:
        pass
    return None


def fetch_aqi_by_uid(uid: int, api_key: str) -> dict | None:
    url = f"https://api.waqi.info/feed/@{uid}/?token={api_key}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "ok":
            d = data["data"]
            return {"aqi": _safe_aqi(d.get("aqi")), "city": d["city"]["name"]}
    except requests.exceptions.RequestException:
        pass
    return None


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_defaults = {
    "exact_stations": [],
    "fuzzy_stations": [],
    "selected_uid": None,
    "geo_result": None,
    "last_search": "",
    "pending_search": None,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH EXECUTION  (top-level, before any UI is drawn)
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.pending_search:
    keyword = st.session_state.pending_search
    st.session_state.pending_search = None

    with st.spinner(f'Searching for "{keyword}"…'):
        exact, fuzzy = search_stations(keyword, API_KEY or "")

    st.session_state.exact_stations = exact
    st.session_state.fuzzy_stations = fuzzy
    st.session_state.selected_uid = None
    st.session_state.geo_result = None
    st.session_state.last_search = keyword

    if exact:
        st.session_state.selected_uid = exact[0]["uid"]
    elif not fuzzy and API_KEY:
        geo = fetch_by_geo(keyword, API_KEY)
        if geo:
            st.session_state.geo_result = geo


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT  — two columns on desktop, stacked on mobile (via CSS media query)
# ─────────────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 2], gap="large")

# ── LEFT COLUMN: header + search + suggestions ────────────────────────────────
with left_col:
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🌿 India<br>AQI Monitor</div>
        <div class="app-subtitle">Real-time air quality &amp; health guidance</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="search-label">Search location</div>', unsafe_allow_html=True)

    with st.form(key="search_form", clear_on_submit=True):
        location_input = st.text_input(
            label="location",
            placeholder=(
                f"Last: {st.session_state.last_search} — type a new one…"
                if st.session_state.last_search
                else "e.g. Colaba, Mumbai, Delhi…"
            ),
            label_visibility="collapsed",
        )
        search_clicked = st.form_submit_button(
            "Search →", use_container_width=True, type="primary"
        )

    if search_clicked and location_input.strip():
        st.session_state.pending_search = location_input.strip()
        st.rerun()

    if not API_KEY:
        st.error("🔑 Add `WAQI_API_KEY` to your `.env` file.")
        st.stop()

    st.markdown(
        '<div class="note-box">📍 Enter any city, district or neighbourhood in India.</div>',
        unsafe_allow_html=True,
    )

    exact = st.session_state.exact_stations
    fuzzy = st.session_state.fuzzy_stations

    if st.session_state.last_search:
        if not exact and not fuzzy and not st.session_state.geo_result:
            st.warning(
                f"No stations found for **{st.session_state.last_search}**. "
                "Try a broader term."
            )
        elif not exact and fuzzy:
            st.markdown('<div class="dym-header">Did you mean…</div>', unsafe_allow_html=True)
            for s in fuzzy[:6]:
                lbl = f"📍 {s['name']}" + (f"  AQI {s['aqi']}" if s["aqi"] is not None else "")
                if st.button(lbl, key=f"fuzzy_{s['uid']}"):
                    st.session_state.selected_uid = s["uid"]
                    st.session_state.geo_result = None

    if len(exact) > 1 and st.session_state.selected_uid:
        st.markdown('<div class="dym-header">Nearby stations</div>', unsafe_allow_html=True)
        for s in exact:
            lbl = f"📍 {s['name']}" + (f"  AQI {s['aqi']}" if s["aqi"] is not None else "")
            if st.button(lbl, key=f"exact_{s['uid']}"):
                st.session_state.selected_uid = s["uid"]
                st.session_state.geo_result = None

    st.markdown('<div class="app-footer">Data: WAQI · Near real-time</div>', unsafe_allow_html=True)


# ── RIGHT COLUMN: AQI display ─────────────────────────────────────────────────
with right_col:
    result = None
    if st.session_state.selected_uid:
        with st.spinner("Fetching live data…"):
            result = fetch_aqi_by_uid(st.session_state.selected_uid, API_KEY or "")
    elif st.session_state.geo_result:
        result = st.session_state.geo_result

    if result is None and not st.session_state.last_search:
        st.markdown("""
        <div style="height:55vh;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;opacity:0.22;text-align:center;gap:1rem;">
            <div style="font-size:4rem;">🌿</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;
                        color:var(--text-color);letter-spacing:-0.02em;">Search for a location</div>
            <div style="font-size:0.85rem;color:var(--text-color);
                        max-width:260px;line-height:1.6;">
                Type any Indian city, neighbourhood or district above
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif result is None and st.session_state.last_search:
        st.info("Select a station from the list above, or try a different search term.")

    elif result and result["aqi"] is None:
        st.warning(
            f"**{result['city']}** — Station is not currently reporting AQI data. "
            "Try a nearby station."
        )

    elif result:
        aqi_value = result["aqi"]
        city_name  = result["city"]
        meta       = get_aqi_meta(aqi_value)

        # ── AQI card + advisory cards ────────────────────────────────────────
        # On desktop: card_col | info_col side-by-side.
        # On mobile: CSS stacks them vertically automatically.
        card_col, info_col = st.columns([1, 1.15], gap="medium")

        with card_col:
            st.markdown(f"""
            <div class="aqi-main-card" style="--aqi-glow:{meta['glow']};">
                <div class="aqi-station">📍 {city_name}</div>
                <div class="aqi-big-number" style="color:{meta['color']};">{aqi_value}</div>
                <div class="aqi-card-label">Air Quality Index</div>
                <div class="aqi-category-badge"
                     style="background:{meta['bg']};color:{meta['color']};margin-top:1rem;">
                    {meta['emoji']} {meta['category']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with info_col:
            st.markdown(f"""
            <div class="feedback-card">
                <div class="feedback-card-title">Health Advisory</div>
                <div class="feedback-card-text">{meta['advice']}</div>
            </div>
            <div class="eco-card">
                <div class="eco-card-title">🌱 Today's Eco-Task</div>
                <div class="eco-card-text">{meta['eco_task']}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Stat row ─────────────────────────────────────────────────────────
        # We use a pure HTML grid for the stat boxes instead of st.columns so
        # that on mobile they reliably stay in a 3-column grid (matching the
        # design) rather than being forced to 100% width by the column override.
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;">
            <div class="stat-box">
                <div class="stat-val" style="color:{meta['color']};">{aqi_value}</div>
                <div class="stat-key">AQI Value</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="font-size:clamp(0.75rem,2.5vw,1rem);">{meta['category']}</div>
                <div class="stat-key">Category</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="font-size:clamp(0.75rem,2.5vw,1rem);">{meta['safety']}</div>
                <div class="stat-key">Outdoor Safety</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── AQI scale ────────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 AQI Scale Reference"):
            # Pure HTML table so it scrolls horizontally on mobile
            st.markdown("""
            <div class="aqi-table-wrap" style="overflow-x:auto;-webkit-overflow-scrolling:touch;">
            <table style="width:100%;border-collapse:collapse;font-size:0.85rem;
                          font-family:'DM Sans',sans-serif;color:var(--text-color);">
                <thead>
                    <tr style="border-bottom:1px solid rgba(128,128,128,0.15);">
                        <th style="padding:0.5rem 0.75rem;text-align:left;
                                   opacity:0.45;font-weight:600;
                                   font-size:0.7rem;letter-spacing:0.08em;
                                   text-transform:uppercase;">Range</th>
                        <th style="padding:0.5rem 0.75rem;text-align:left;
                                   opacity:0.45;font-weight:600;
                                   font-size:0.7rem;letter-spacing:0.08em;
                                   text-transform:uppercase;">Category</th>
                        <th style="padding:0.5rem 0.75rem;text-align:left;
                                   opacity:0.45;font-weight:600;
                                   font-size:0.7rem;letter-spacing:0.08em;
                                   text-transform:uppercase;">At Risk</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td style="padding:0.45rem 0.75rem;">0–50</td>
                        <td style="padding:0.45rem 0.75rem;color:#1faa72;font-weight:600;">Good</td>
                        <td style="padding:0.45rem 0.75rem;">Nobody</td></tr>
                    <tr><td style="padding:0.45rem 0.75rem;">51–100</td>
                        <td style="padding:0.45rem 0.75rem;color:#c9a030;font-weight:600;">Moderate</td>
                        <td style="padding:0.45rem 0.75rem;">Very sensitive</td></tr>
                    <tr><td style="padding:0.45rem 0.75rem;">101–150</td>
                        <td style="padding:0.45rem 0.75rem;color:#d4782a;font-weight:600;">Sensitive Groups</td>
                        <td style="padding:0.45rem 0.75rem;">Sensitive groups</td></tr>
                    <tr><td style="padding:0.45rem 0.75rem;">151–200</td>
                        <td style="padding:0.45rem 0.75rem;color:#d93025;font-weight:600;">Unhealthy</td>
                        <td style="padding:0.45rem 0.75rem;">General public</td></tr>
                    <tr><td style="padding:0.45rem 0.75rem;">201–300</td>
                        <td style="padding:0.45rem 0.75rem;color:#8e44ad;font-weight:600;">Very Unhealthy</td>
                        <td style="padding:0.45rem 0.75rem;">Everyone</td></tr>
                    <tr><td style="padding:0.45rem 0.75rem;">301+</td>
                        <td style="padding:0.45rem 0.75rem;color:#c0392b;font-weight:600;">Hazardous</td>
                        <td style="padding:0.45rem 0.75rem;">Everyone</td></tr>
                </tbody>
            </table>
            </div>
            """, unsafe_allow_html=True)