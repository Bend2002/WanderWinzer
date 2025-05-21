# station.py – Bewertungsmodul
import sqlite3
import os
import streamlit as st

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# Tabelle 'stations' automatisch erstellen, falls sie fehlt
conn = sqlite3.connect(DB_NAME)
conn.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        revealed INTEGER DEFAULT 0
    )
""")
conn.commit()
conn.close()

def get_current_station():
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute("SELECT MAX(id) FROM stations WHERE revealed = 0").fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def save_rating(user, station_id, data: dict):
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user, station_id, data["geschmack"], data["alkohol"], data["preis"],
         data["land"], data["rebsorte"], data["farbe"],
         data["körper"], data["säure"], data["abgang"], data["kommentar"])
    )
    conn.commit()
    conn.close()

def station_page():
    user = st.session_state["user"]
    station_id = get_current_station()

    if not station_id:
        st.info("Noch keine Station freigegeben.")
        return

    st.header(f"🍇 Bewertung – Station {station_id}")

    st.markdown("**Wie hat dir der Wein geschmeckt?**")
    geschmack = st.slider("Geschmack", 0, 10, 5, format="%d", help="0 = Plörre, 10 = Göttlich")
    alkohol = st.slider("Geschätzter Alkoholgehalt (%)", 8.0, 16.0, 12.0, step=0.1)
    preis = st.number_input("Geschätzter Preis (€)", min_value=0.0, max_value=100.0, step=0.5)

    col1, col2, col3 = st.columns(3)
    with col1:
        farbe = st.radio("Farbe", ["Weiß", "Rosé", "Rot"])
    with col2:
        land = st.selectbox("Herkunftsland", ["Deutschland", "Frankreich", "Italien", "Spanien", "Andere"])
    with col3:
        rebsorte = st.text_input("Rebsorte")

    körper = st.slider("Körper", 0, 10, 5, help="0 = leicht, 10 = kräftig")
    säure = st.slider("Säure", 0, 10, 5, help="0 = weich, 10 = sauer")
    abgang = st.slider("Abgang", 0, 10, 5, help="0 = kurz, 10 = lang")

    kommentar = st.text_area("Freitext (optional)", placeholder="Wie war dein Eindruck?")

    if st.button("Bewertung speichern"):
        save_rating(user, station_id, {
            "geschmack": geschmack,
            "alkohol": alkohol,
            "preis": preis,
            "land": land,
            "rebsorte": rebsorte,
            "farbe": farbe,
            "körper": körper,
            "säure": säure,
            "abgang": abgang,
            "kommentar": kommentar,
        })
        st.success("Deine Bewertung wurde gespeichert!")
