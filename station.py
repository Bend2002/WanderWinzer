# station.py – Bewertungsformular mit festen Wein‑Infos
import streamlit as st
import sqlite3, os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# ───── Feste Stationsliste (aus Excel zusammengefasst) ─────
STATIONS = [
   
    {"id": 1,  "name": "Lenotti Custoza", "jahrgang": 2023, "herkunft":"Italien",        "bild":""},
    {"id": 2,  "name": "Rio Lindo Syrah", "jahrgang": 2023, "herkunft":"Spanien",        "bild":""},
    {"id": 3,  "name": "Trebbiano d’Abruzzo Bio (Cantina Tollo)", "jahrgang": 2024, "herkunft":"Italien",        "bild":""},
    {"id": 4,  "name": "Mario Collina Primitivo Rosato", "jahrgang": 2023, "herkunft":"Italien",        "bild":""},
    {"id": 5,  "name": "Alegrete Vinho Verde", "jahrgang": 2023, "herkunft":"Portugal",        "bild":""},
    {"id": 6,  "name": "Pierre Amadieu Ventoux “La Claretière”", "jahrgang": 2021, "herkunft":"Frankreich",        "bild":""},
    {"id": 7,  "name": "Margarethenhof Saar Riesling", "jahrgang": 2022, "herkunft":"Deutschland",        "bild":""},
    {"id": 8,  "name": "Kühling-Gillot “Hase” Sauvignon Blanc", "jahrgang": 2023, "herkunft":"Deutschland",        "bild":""},
    {"id": 9,  "name": "Château La Genestière Côtes du Rhône blanc", "jahrgang": 2022, "herkunft":"Frankreich",        "bild":""}

]

# ────────────────────────────────────────────────────────────
# DB & Helper

def get_current_station_id() -> int:
    conn = sqlite3.connect(DB_NAME)
    conn.execute("CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value INTEGER)")
    row = conn.execute("SELECT value FROM app_state WHERE key = 'current_station'").fetchone()
    conn.close()
    return row[0] if row else 0

def save_rating(user, sid, data):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            user TEXT,
            station_id INTEGER,
            geschmack INTEGER,
            alkohol REAL,
            preis REAL,
            kommentar TEXT,
            PRIMARY KEY (user, station_id)
        )
        """
    )
    conn.execute(
        "INSERT OR REPLACE INTO ratings (user, station_id, geschmack, alkohol, preis, kommentar) VALUES (?,?,?,?,?,?)",
        (user, sid, *data)
    )
    conn.commit(); conn.close()

# ────────────────────────────────────────────────────────────
# Streamlit Seite

def station_page():
    user = st.session_state["user"]
    sid = get_current_station_id()

    if sid == 0:
        st.info("Noch keine Station freigegeben.")
        return

    station = next(s for s in STATIONS if s["id"] == sid)
    st.header(f"🍷 Station {sid}: {station['name']}")

    # Bewertung
    geschmack = st.slider("Geschmack (0 = Plörre, 10 = Göttlich)", 0, 10, 5)
    alkohol   = st.slider("Alkohol %", 8.0, 16.0, 12.0, step=0.1)
    preis     = st.number_input("Preis-Schätzung €", 0.0, 100.0, step=0.5)
    kommentar = st.text_area("Freitext")

    if st.button("Bewertung speichern"):
        save_rating(user, sid, (geschmack, alkohol, preis, kommentar))
        st.success("Bewertung gespeichert!")

    # Debug: Infos anzeigen (nur admin)
    if st.checkbox("Wein-Details anzeigen (Admin)"):
        st.write(station)
