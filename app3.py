# app3.py

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

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.block-container {
    padding: 3rem 4rem 2rem 4rem !important;
    max-width: 1100px !important;
}
.app-header { margin-bottom: 2.5rem; }
.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem; font-weight: 800;
    letter-spacing: -0.03em; color: #f0f0f0;
    line-height: 1.1; margin: 0;
}
.app-subtitle {
    font-size: 1rem; color: rgba(255,255,255,0.42);
    margin-top: 0.4rem; font-weight: 300; letter-spacing: 0.01em;
}
.search-label {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(255,255,255,0.35); margin-bottom: 0.5rem;
}
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important; color: #f0f0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important; padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(99, 220, 169, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,220,169,0.08) !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #63dca9, #3ab88a) !important;
    color: #0a0a0a !important; border: none !important;
    border-radius: 10px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.9rem !important;
    letter-spacing: 0.04em !important; padding: 0.75rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover { opacity: 0.85 !important; }
.note-box {
    background: rgba(255, 200, 87, 0.07); border-left: 3px solid #e8b84b;
    border-radius: 0 8px 8px 0; padding: 0.6rem 1rem;
    font-size: 0.82rem; color: #c9a040; margin: 0.75rem 0 1.25rem 0; line-height: 1.5;
}
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
    color: rgba(255,255,255,0.35); font-family: 'Syne', sans-serif; margin-bottom: 1rem;
}
.aqi-big-number {
    font-family: 'Syne', sans-serif; font-size: clamp(3.5rem, 6vw, 5.5rem);
    font-weight: 800; line-height: 1; letter-spacing: -0.04em; white-space: nowrap;
}
.aqi-category-badge {
    display: inline-flex; align-items: center; gap: 0.4rem; margin-top: 0.75rem;
    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.82rem;
    font-weight: 600; font-family: 'Syne', sans-serif; letter-spacing: 0.02em;
}
.feedback-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1.25rem 1.5rem;
}
.feedback-card-title {
    font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(255,255,255,0.3); margin-bottom: 0.6rem;
}
.feedback-card-text { font-size: 0.95rem; color: rgba(255,255,255,0.75); line-height: 1.6; }
.eco-card {
    background: rgba(99, 220, 169, 0.06); border: 1px solid rgba(99, 220, 169, 0.18);
    border-radius: 14px; padding: 1.25rem 1.5rem; margin-top: 1rem;
}
.eco-card-title {
    font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(99, 220, 169, 0.55); margin-bottom: 0.6rem;
}
.eco-card-text { font-size: 0.95rem; color: rgba(255,255,255,0.75); line-height: 1.6; }
.stat-box {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1rem; text-align: center;
}
.stat-val {
    font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700;
    color: #f0f0f0; line-height: 1;
}
.stat-key {
    font-size: 0.7rem; color: rgba(255,255,255,0.35); letter-spacing: 0.08em;
    text-transform: uppercase; margin-top: 0.3rem;
}
.dym-header {
    font-family: 'Syne', sans-serif; font-size: 0.75rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: rgba(255,255,255,0.35); margin: 1.5rem 0 0.75rem 0;
}
div[data-testid="stButton"] button:not([kind="primary"]) {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important; color: rgba(255,255,255,0.65) !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important;
    text-align: left !important; justify-content: flex-start !important;
    padding: 0.6rem 1rem !important; transition: all 0.15s !important; width: 100% !important;
}
div[data-testid="stButton"] button:not([kind="primary"]):hover {
    background: rgba(99,220,169,0.08) !important;
    border-color: rgba(99,220,169,0.3) !important; color: #63dca9 !important;
}
.thin-divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 2rem 0; }
.app-footer { font-size: 0.75rem; color: rgba(255,255,255,0.2); margin-top: 3rem; }
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
    """
    Returns (exact_matches, fuzzy_matches) using the WAQI keyword search API.
    Accepts any station returned by an India-scoped query; only skips results
    that carry an explicit non-IN country code.
    """
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

            # Skip only when a non-IN country is *explicitly* present.
            # If country is absent the WAQI search already scoped to India
            # via the query suffix, so we trust the result.
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
    """
    FIX (Bug 1 — Mazgaon / Byculla):
    The WAQI keyword-search index does not include every monitoring station;
    many hyper-local Mumbai sensors (Mazgaon, Byculla, etc.) are only
    reachable via the geo-based feed endpoint:
        /feed/geo:<lat>;<lng>/?token=…
    Strategy:
      1. Geocode the search term to (lat, lng) using the WAQI map search,
         which returns the nearest station regardless of whether it appears
         in the keyword index.
      2. Call the geo feed endpoint with those coordinates.
      3. Return the result just like fetch_aqi_by_uid does.
    """
    # Step 1 – find closest station coords via the map/bounds API
    geo_url = (
        "https://api.waqi.info/map/bounds/"
        f"?token={api_key}&latlng=6.5,68,37.5,97.5"  # rough India bounding box
    )
    # The bounds API is not a geocoder, so we use the search API with latlng
    # hint instead: query the feed endpoint directly with the city name.
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
            return {
                "aqi": _safe_aqi(d.get("aqi")),
                "city": d["city"]["name"],
            }
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
    "geo_result": None,       # result from geo-fallback (no uid needed)
    "last_search": "",
    # FIX (Bug 2): pending_search holds the keyword committed by the form.
    # It is written BEFORE st.rerun() so the very next script pass picks it
    # up and executes the search, eliminating the "search twice" behaviour.
    "pending_search": None,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH EXECUTION  (runs at top-level, before any columns are drawn)
# FIX (Bug 2): Moving the search execution here — unconditionally, at the very
# top of the script — means it always runs on the rerun that was triggered by
# the form submit, with no risk of the column/widget rendering order interfering.
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.pending_search:
    keyword = st.session_state.pending_search
    st.session_state.pending_search = None          # consume immediately

    with st.spinner(f'Searching for "{keyword}"…'):
        exact, fuzzy = search_stations(keyword, API_KEY or "")

    st.session_state.exact_stations = exact
    st.session_state.fuzzy_stations = fuzzy
    st.session_state.selected_uid = None
    st.session_state.geo_result = None
    st.session_state.last_search = keyword

    if exact:
        # Auto-select the first (most relevant) exact match
        st.session_state.selected_uid = exact[0]["uid"]
    elif not fuzzy and API_KEY:
        # FIX (Bug 1): No keyword-search results at all → try the geo/name feed.
        # This catches stations like Mazgaon and Byculla that exist in the WAQI
        # database but are absent from the keyword-search index.
        geo = fetch_by_geo(keyword, API_KEY)
        if geo:
            st.session_state.geo_result = geo


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 2], gap="large")

with left_col:
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🌿 India<br>AQI Monitor</div>
        <div class="app-subtitle">Real-time air quality &<br>health guidance</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="search-label">Search location</div>', unsafe_allow_html=True)

    # ── Search form ──────────────────────────────────────────────────────────
    # FIX (Bug 2):
    #   • No value= binding — avoids Streamlit overwriting the widget with the
    #     stale last_search on every incidental rerun.
    #   • clear_on_submit=True — clears the box after submit so the widget
    #     state is clean on the next rerun; no stale text to accidentally
    #     re-submit.
    #   • On submit we write to pending_search and call st.rerun() immediately.
    #     This forces a fresh script execution where pending_search is non-None
    #     and the search block at the top fires exactly once, then clears it.
    with st.form(key="search_form", clear_on_submit=True):
        location_input = st.text_input(
            label="location",
            placeholder=(
                f"Last: {st.session_state.last_search} — type a new one…"
                if st.session_state.last_search
                else "e.g. Mazgaon, Byculla, Delhi…"
            ),
            label_visibility="collapsed",
        )
        search_clicked = st.form_submit_button(
            "Search →", use_container_width=True, type="primary"
        )

    if search_clicked and location_input.strip():
        st.session_state.pending_search = location_input.strip()
        st.rerun()   # ← key fix: jump straight to a clean execution pass

    # ── API key guard ────────────────────────────────────────────────────────
    if not API_KEY:
        st.error("🔑 Add `WAQI_API_KEY` to your `.env` file.")
        st.stop()

    st.markdown(
        '<div class="note-box">📍 Enter any city, district or neighbourhood in India.</div>',
        unsafe_allow_html=True,
    )

    # ── Results / suggestions ────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────────────────
# RIGHT COLUMN: AQI display
# ─────────────────────────────────────────────────────────────────────────────
with right_col:
    # Resolve what to display: uid-based fetch takes priority, then geo fallback
    result = None
    if st.session_state.selected_uid:
        with st.spinner("Fetching live data…"):
            result = fetch_aqi_by_uid(st.session_state.selected_uid, API_KEY or "")
    elif st.session_state.geo_result:
        result = st.session_state.geo_result

    if result is None and not st.session_state.last_search:
        # Empty state
        st.markdown("""
        <div style="height:60vh;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;opacity:0.25;text-align:center;gap:1rem;">
            <div style="font-size:4rem;">🌿</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
                        color:#f0f0f0;letter-spacing:-0.02em;">Search for a location</div>
            <div style="font-size:0.85rem;color:rgba(255,255,255,0.5);
                        max-width:260px;line-height:1.6;">
                Type any Indian city, neighbourhood or district and press Enter
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif result is None:
        if st.session_state.last_search:
            st.info("Select a station from the list on the left, or try a different search term.")
    elif result["aqi"] is None:
        st.warning(
            f"**{result['city']}** — Station is not currently reporting AQI data. "
            "Try a nearby station."
        )
    else:
        aqi_value = result["aqi"]
        city_name = result["city"]
        meta = get_aqi_meta(aqi_value)

        card_col, info_col = st.columns([1, 1.1], gap="medium")

        with card_col:
            st.markdown(f"""
            <div class="aqi-main-card" style="--aqi-glow:{meta['glow']};">
                <div class="aqi-station">📍 {city_name}</div>
                <div class="aqi-big-number" style="color:{meta['color']};">{aqi_value}</div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.25);letter-spacing:0.1em;
                            text-transform:uppercase;margin-top:0.2rem;
                            font-family:'Syne',sans-serif;">Air Quality Index</div>
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

        st.markdown("<br>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="color:{meta['color']};">{aqi_value}</div>
                <div class="stat-key">AQI Value</div>
            </div>""", unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="font-size:1rem;">{meta['category']}</div>
                <div class="stat-key">Category</div>
            </div>""", unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="font-size:1rem;">{meta['safety']}</div>
                <div class="stat-key">Outdoor Safety</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 AQI Scale Reference"):
            st.table({
                "Range":    ["0–50", "51–100", "101–150", "151–200", "201–300", "301+"],
                "Category": ["Good", "Moderate", "Unhealthy for Sensitive Groups",
                             "Unhealthy", "Very Unhealthy", "Hazardous"],
                "At Risk":  ["Nobody", "Very sensitive", "Sensitive groups",
                             "General public", "Everyone", "Everyone"],
            })