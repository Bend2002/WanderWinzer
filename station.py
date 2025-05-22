# station.py – Voting + Reveal 2.0 (Slider & Dropdowns)
import streamlit as st, sqlite3, os

DB = os.path.join(os.getcwd(), "wander.db")


# Vollständige Stations­liste – nur Auswahl-Felder sind relevant für Dropdowns
STATIONS = [
   
   {"id": 1,  "name": "Lenotti Custoza", "jahrgang": 2023, "herkunft":"Italien", "rebsorte": "Garganega / Trebbiano / Cortese (Cuvée)", "farbe": "Weiß", "preis": 6.95, "alkohol": 12.0, "koerper": "Federleicht", "saeure": "Frisch", "geschmack": "Apfel, Melone, Limette, Mineral", "abgang": "", "food_pairing": "Meeresfrüchte, Pasta, gereifter Käse, Weißfisch", "bild":""},
    {"id": 2,  "name": "Rio Lindo Syrah", "jahrgang": 2023, "herkunft":"Spanien", "rebsorte": "Syrah", "farbe": "Rot", "preis": 6.95, "alkohol": None, "koerper": "Mittel", "saeure": "Mild", "geschmack": "Brombeere, Pflaume, Würze", "abgang": "Kurz–mittel", "food_pairing": "Grillfleisch, Tapas", "bild":""},
    {"id": 3,  "name": "Trebbiano d’Abruzzo Bio (Cantina Tollo)", "jahrgang": 2024, "herkunft":"Italien", "rebsorte": "Trebbiano", "farbe": "Weiß", "preis": 8.0, "alkohol": None, "koerper": "Leicht", "saeure": "Frisch", "geschmack": "Apfel, Zitrus, Mandel", "abgang": "Kurz", "food_pairing": "Antipasti, Fisch", "bild":""},
    {"id": 4,  "name": "Mario Collina Primitivo Rosato", "jahrgang": 2023, "herkunft":"Italien", "rebsorte": "Primitivo", "farbe": "Rosé", "preis": 2.29, "alkohol": None, "koerper": "Leicht", "saeure": "Weich", "geschmack": "Erdbeere, Kirsche, Himbeere", "abgang": "Kurz", "food_pairing": "Fisch, Pizza, Pasta", "bild":""},
    {"id": 5,  "name": "Alegrete Vinho Verde", "jahrgang": 2023, "herkunft":"Portugal", "rebsorte": "Loureiro / Trajadura / Arinto (Cuvée)", "farbe": "Weiß", "preis": 2.95, "alkohol": None, "koerper": "Leicht", "saeure": "Hoch", "geschmack": "Zitrone, Ananas, Mango, Mineral", "abgang": "Sehr kurz", "food_pairing": "Käseplatte, Meeresfrüchte", "bild":""},
    {"id": 6,  "name": "Pierre Amadieu Ventoux “La Claretière”", "jahrgang": 2021, "herkunft":"Frankreich", "rebsorte": "Grenache & Syrah", "farbe": "Rot", "preis": 8.95, "alkohol": 14.0, "koerper": "Mittel-kräftig", "saeure": "Mäßig", "geschmack": "Kirsche, schwarze Johannisbeere, Garrigue-Kräuter, Pfeffer", "abgang": "Mittel-lang", "food_pairing": "Ratatouille, Grillsteak", "bild":""},
    {"id": 7,  "name": "Margarethenhof Saar Riesling", "jahrgang": 2022, "herkunft":"Deutschland", "rebsorte": "Riesling", "farbe": "Weiß", "preis": 9.95, "alkohol": 11.0, "koerper": "Leicht", "saeure": "Hoch", "geschmack": "Grüner Apfel, Pfirsich, Schiefermineral", "abgang": "Mittel", "food_pairing": "Asiatische Küche, Fisch", "bild":""},
    {"id": 8,  "name": "Kühling-Gillot “Hase” Sauvignon Blanc", "jahrgang": 2023, "herkunft":"Deutschland", "rebsorte": "Sauvignon Blanc", "farbe": "Weiß", "preis": 8.95, "alkohol": 11.5, "koerper": "Leicht", "saeure": "Hoch", "geschmack": "Stachelbeere, Johannisbeere, frisches Gras", "abgang": "Kurz", "food_pairing": "Fisch, Meeresfrüchte, Salat", "bild":""},
    {"id": 9,  "name": "Château La Genestière Côtes du Rhône blanc", "jahrgang": 2022, "herkunft":"Frankreich", "rebsorte": "Grenache Blanc / Viognier / Clairette (Cuvée)", "farbe": "Weiß", "preis": 6.95, "alkohol": 13.5, "koerper": "Mittel", "saeure": "Moderat", "geschmack": "Steinobst, weiße Blüten, Honig", "abgang": "Mittel", "food_pairing": "Geflügel, Quiche", "bild":""},
    {"id": 10,  "name": "Vino Blanco de España (Bag-in-Box)", "jahrgang": 2022, "herkunft":"Spanien", "rebsorte": "Blend (Airén / Macabeo, o. ä.)", "farbe": "Weiß", "preis": 1.25, "alkohol": None, "koerper": "Leicht", "saeure": "Mäßig", "geschmack": "Zitrus, Apfel", "abgang": "Kurz", "food_pairing": "Partybowle, Tapas", "bild":""}

]

# → Dropdown-Optionen automatisch aus den Weindaten ableiten
LÄNDER  = sorted({w["herkunft"]  for w in STATIONS})
REBSORT = sorted({w["rebsorte"]  for w in STATIONS})
AROMEN  = sorted({w["geschmack"] for w in STATIONS})

# Ländercode zu Flagge (ISO‑Land → Emoji, simple Map)
FLAG = {
    "Deutschland": "🇩🇪", "Frankreich": "🇫🇷", "Italien": "🇮🇹", "Spanien": "🇪🇸",
    "Portugal": "🇵🇹",    "Niederlande": "🇳🇱",  "Chile": "🇨🇱"
}

# ------------------------ DB‑Helper

def _conn():
    return sqlite3.connect(DB, check_same_thread=False)

def get_state():
    with _conn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT)")
        return {k: (int(v) if v.isdigit() else v) for k,v in c.execute("SELECT key,value FROM app_state")}

def set_state(**kw):
    with _conn() as c:
        for k, v in kw.items():
            c.execute("INSERT OR REPLACE INTO app_state VALUES (?,?)", (k, str(v)))
        c.commit()

# ▶️ Alias für Admin-Kompatibilität
get_app_state = get_state
set_app_state = set_state

# Ratings

def save_rating(u,sid,g,a,p,l,r,f,k,s,ab,c,note):
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS ratings (user TEXT, station_id INT, geschmack INT, alkohol REAL, preis REAL, land TEXT, rebsorte TEXT, farbe TEXT, körper INT, säure INT, abgang INT, kommentar TEXT, PRIMARY KEY(user,station_id))""")
        c.execute("INSERT OR REPLACE INTO ratings VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (u,sid,g,a,p,l,r,f,k,s,ab,note))
        c.commit()

def my_rating(u,sid):
    with _conn() as c:
        return c.execute("SELECT * FROM ratings WHERE user=? AND station_id=?",(u,sid)).fetchone()

# ------------------------ Seite

def station_page():
    user  = st.session_state["user"]
    st_state = get_state()
    sid   = st_state.get("current_station",0)
    mode  = st_state.get("mode","idle")

    if sid == 0:
        st.info("Noch keine Station freigegeben.")
        return

    wine = next(w for w in STATIONS if w["id"]==sid)

    # Anzeige: Nummer statt Name im Voting
    if mode=="vote":
        st.header(f"🍷 Station {sid}")
    else:
        st.header(f"🍷 Station {sid}: {wine['name']}")

    # ----- Voting -----
    if mode=="vote":
        # Geschmacksskala bleibt Slider 0‑10
        g = st.slider("Geschmack (0 = Plörre, 10 = Göttlich)",0,10,5)
        a = st.slider("Alkohol %  (0 = Autofahren kein Problem … 16 = Tütülülüü)",0.0,16.0,12.0,step=0.1)
        p = st.slider("Preis‑Schätzung €",0.0,35.0,10.0,step=0.5)
        l = st.selectbox("Land", [f"{FLAG.get(x,'')} {x}" for x in LÄNDER])
        r = st.selectbox("Rebsorte", REBSORT)
        f = st.selectbox("Farbe", ["Weiß","Rosé","Rot"])
        k = st.slider("Körper",0,10,5)
        s = st.slider("Säure",0,10,5)
        ab= st.slider("Abgang",0,10,5)
        note = st.text_area("Kommentar")
        if st.button("Speichern"):
            save_rating(user,sid,g,a,p,l.strip()[2:],r,f,k,s,ab,note)
            st.success("Gespeichert!")

    # ----- Reveal -----
    elif mode=="reveal":
        row = my_rating(user,sid)
        if not row:
            st.warning("Du hast nicht bewertet.")
            return
        st.subheader("Auflösung")
        col1,col2= st.columns(2)
        with col1:
            st.write("**Weinfakten**")
            st.write(wine)
        with col2:
            st.write("**Dein Tipp**")
            st.write({
                "geschmack": row[2],
                "alkohol":   row[3],
                "preis":     row[4],
                "land":      row[5],
                "rebsorte":  row[6]
            })
    else:
        st.info("Warte auf Voting‑Start durch Admin.")
