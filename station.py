# station.py – Bewertungsformular für feste Stationsliste
import streamlit as st, sqlite3, os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# 👉 Feste Reihenfolge der Weine
STATIONS = [
    {"id": 1,  "name": "Bruusj Parelwijn 2023"},
    {"id": 2,  "name": "Vino Blanco de España (ALDI)"},
    {"id": 3,  "name": "Vivino 180519297"},
    {"id": 4,  "name": "Vivino 180033129"},
    {"id": 5,  "name": "Vivino 174062918"},
    {"id": 6,  "name": "Vivino 149749196"},
    {"id": 7,  "name": "Vivino 170858727"},
    {"id": 8,  "name": "Vivino 145037313"},
    {"id": 9,  "name": "Vivino 145037139"},
    {"id": 10, "name": "Vivino 172026356"},
    {"id": 11, "name": "Vivino 173329582"},
    {"id": 12, "name": "Vivino 177083944"},
    {"id": 13, "name": "Vivino 151706143"},
    {"id": 14, "name": "Vivino Extra Reserve"},
]

# ── Hilfsfunktionen ───────────────────────────
def get_current_station_id() -> int:
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value INTEGER)"
    )
    row = conn.execute(
        "SELECT value FROM app_state WHERE key = 'current_station'"
    ).fetchone()
    conn.close()
    return row[0] if row else 0

def save_rating(user, sid, data: tuple):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            user TEXT,
            station_id INTEGER,
            geschmack INTEGER,
            alkohol REAL,
            preis REAL,
            land TEXT,
            rebsorte TEXT,
            farbe TEXT,
            körper INTEGER,
            säure INTEGER,
            abgang INTEGER,
            kommentar TEXT,
            PRIMARY KEY (user, station_id)
        )
        """
    )
    conn.execute(
        """
        INSERT OR REPLACE INTO ratings 
        (user, station_id, geschmack, alkohol, preis, land, rebsorte, farbe, körper, säure, abgang, kommentar)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (user, sid, *data),
    )
    conn.commit(); conn.close()

# ── Streamlit-Seite ───────────────────────────
def station_page():
    user = st.session_state["user"]
    sid = get_current_station_id()

    if sid == 0:
        st.info("Noch keine Station freigegeben.")
        return

    station = next(s for s in STATIONS if s["id"] == sid)
    st.header(f"🍷 Station {sid}: {station['name']}")

    # Formular
    geschmack = st.slider("Geschmack (0 Plörre – 10 Göttlich)", 0, 10, 5)
    alkohol   = st.slider("Alkohol %", 8.0, 16.0, 12.0, step=0.1)
    preis     = st.number_input("Preis-Schätzung €", 0.0, 100.0, step=0.5)
    farbe     = st.radio("Farbe", ["Weiß", "Rosé", "Rot"])
    land      = st.selectbox("Land", ["Deutschland","Frankreich","Italien","Spanien","Andere"])
    rebsorte  = st.text_input("Rebsorte (vermutet)")
    körper    = st.slider("Körper", 0, 10, 5)
    säure     = st.slider("Säure", 0, 10, 5)
    abgang    = st.slider("Abgang", 0, 10, 5)
    kommentar = st.text_area("Notiz")

    if st.button("Bewertung speichern"):
        save_rating(
            user, sid,
            (geschmack, alkohol, preis, land, rebsorte, farbe, körper, säure, abgang, kommentar)
        )
        st.success("Bewertung gespeichert!")
