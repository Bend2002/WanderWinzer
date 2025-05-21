# station.py – Bewertungsformular für aktuelle (nicht aufgedeckte) Station
import streamlit as st, sqlite3, os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# Tabelle sicherstellen
conn = sqlite3.connect(DB_NAME)
conn.execute("""
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    revealed INTEGER DEFAULT 0
)""")
conn.execute("""
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
)""")
conn.commit(); conn.close()

def current_station():
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute("SELECT id,name FROM stations WHERE revealed = 0 ORDER BY id LIMIT 1").fetchone()
    conn.close()
    return row  # None wenn keine Station

def save_rating(user, sid, data):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT OR REPLACE INTO ratings
        (user, station_id, geschmack, alkohol, preis, land, rebsorte, farbe, körper, säure, abgang, kommentar)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (user, sid, *data))
    conn.commit(); conn.close()

def station_page():
    user = st.session_state["user"]
    row = current_station()

    if not row:
        st.info("Noch keine Station freigegeben.")
        return

    sid, name = row
    st.header(f"🍷 Station {sid}: {name}")

    # Formular
    geschmack = st.slider("Geschmack (0 Plörre – 10 Göttlich)", 0,10,5)
    alkohol   = st.slider("Alkohol (%)", 8.0,16.0,12.0,step=0.1)
    preis     = st.number_input("Preis-Schätzung €", 0.0,100.0,step=0.5)
    farbe     = st.radio("Farbe",["Weiß","Rosé","Rot"])
    land      = st.selectbox("Land",["Deutschland","Frankreich","Italien","Spanien","Andere"])
    rebsorte  = st.text_input("Rebsorte (vermutet)")
    körper    = st.slider("Körper",0,10,5)
    säure     = st.slider("Säure",0,10,5)
    abgang    = st.slider("Abgang",0,10,5)
    kommentar = st.text_area("Notiz")

    if st.button("Bewertung speichern"):
        save_rating(user, sid, (geschmack,alkohol,preis,land,rebsorte,farbe,körper,säure,abgang,kommentar))
        st.success("Bewertung gespeichert!")
