# station.py – Bewertungsformular mit festen Wein‑Infos
import streamlit as st
import sqlite3, os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# ───── Feste Stationsliste (aus Excel zusammengefasst) ─────
STATIONS = [
   
   {"id": 1,  "name": "Lenotti Custoza", "jahrgang": 2023, "herkunft":"Italien", "rebsorte": "Garganega / Trebbiano / Cortese (Cuvée)", "farbe": "Weiß", "preis": 6.95, "alkohol": 12.0, "koerper": "Federleicht", "saeure": "Frisch", "geschmack": "Apfel, Melone, Limette, Mineral", "abgang": "", "food_pairing": "Meeresfrüchte, Pasta, gereifter Käse, Weißfisch", "bild":""},
    {"id": 2,  "name": "Rio Lindo Syrah", "jahrgang": 2023, "herkunft":"Spanien", "rebsorte": "Syrah", "farbe": "Rot", "preis": 6.95, "alkohol": null, "koerper": "Mittel", "saeure": "Mild", "geschmack": "Brombeere, Pflaume, Würze", "abgang": "Kurz–mittel", "food_pairing": "Grillfleisch, Tapas", "bild":""},
    {"id": 3,  "name": "Trebbiano d’Abruzzo Bio (Cantina Tollo)", "jahrgang": 2024, "herkunft":"Italien", "rebsorte": "Trebbiano", "farbe": "Weiß", "preis": 8.0, "alkohol": null, "koerper": "Leicht", "saeure": "Frisch", "geschmack": "Apfel, Zitrus, Mandel", "abgang": "Kurz", "food_pairing": "Antipasti, Fisch", "bild":""},
    {"id": 4,  "name": "Mario Collina Primitivo Rosato", "jahrgang": 2023, "herkunft":"Italien", "rebsorte": "Primitivo", "farbe": "Rosé", "preis": 2.29, "alkohol": null, "koerper": "Leicht", "saeure": "Weich", "geschmack": "Erdbeere, Kirsche, Himbeere", "abgang": "Kurz", "food_pairing": "Fisch, Pizza, Pasta", "bild":""},
    {"id": 5,  "name": "Alegrete Vinho Verde", "jahrgang": 2023, "herkunft":"Portugal", "rebsorte": "Loureiro / Trajadura / Arinto (Cuvée)", "farbe": "Weiß", "preis": 2.95, "alkohol": null, "koerper": "Leicht", "saeure": "Hoch", "geschmack": "Zitrone, Ananas, Mango, Mineral", "abgang": "Sehr kurz", "food_pairing": "Käseplatte, Meeresfrüchte", "bild":""},
    {"id": 6,  "name": "Pierre Amadieu Ventoux “La Claretière”", "jahrgang": 2021, "herkunft":"Frankreich", "rebsorte": "Grenache & Syrah", "farbe": "Rot", "preis": 8.95, "alkohol": 14.0, "koerper": "Mittel-kräftig", "saeure": "Mäßig", "geschmack": "Kirsche, schwarze Johannisbeere, Garrigue-Kräuter, Pfeffer", "abgang": "Mittel-lang", "food_pairing": "Ratatouille, Grillsteak", "bild":""},
    {"id": 7,  "name": "Margarethenhof Saar Riesling", "jahrgang": 2022, "herkunft":"Deutschland", "rebsorte": "Riesling", "farbe": "Weiß", "preis": 9.95, "alkohol": 11.0, "koerper": "Leicht", "saeure": "Hoch", "geschmack": "Grüner Apfel, Pfirsich, Schiefermineral", "abgang": "Mittel", "food_pairing": "Asiatische Küche, Fisch", "bild":""},
    {"id": 8,  "name": "Kühling-Gillot “Hase” Sauvignon Blanc", "jahrgang": 2023, "herkunft":"Deutschland", "rebsorte": "Sauvignon Blanc", "farbe": "Weiß", "preis": 8.95, "alkohol": 11.5, "koerper": "Leicht", "saeure": "Hoch", "geschmack": "Stachelbeere, Johannisbeere, frisches Gras", "abgang": "Kurz", "food_pairing": "Fisch, Meeresfrüchte, Salat", "bild":""},
    {"id": 9,  "name": "Château La Genestière Côtes du Rhône blanc", "jahrgang": 2022, "herkunft":"Frankreich", "rebsorte": "Grenache Blanc / Viognier / Clairette (Cuvée)", "farbe": "Weiß", "preis": 6.95, "alkohol": 13.5, "koerper": "Mittel", "saeure": "Moderat", "geschmack": "Steinobst, weiße Blüten, Honig", "abgang": "Mittel", "food_pairing": "Geflügel, Quiche", "bild":""},
    {"id": 10,  "name": "Vino Blanco de España (Bag-in-Box)", "jahrgang": 2022, "herkunft":"Spanien", "rebsorte": "Blend (Airén / Macabeo, o. ä.)", "farbe": "Weiß", "preis": 1.25, "alkohol": null, "koerper": "Leicht", "saeure": "Mäßig", "geschmack": "Zitrus, Apfel", "abgang": "Kurz", "food_pairing": "Partybowle, Tapas", "bild":""}


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
