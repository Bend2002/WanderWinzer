# station.py – Voting + Reveal 3.0 (klarere Felder, Aromen‑Multi‑Select)
import streamlit as st, sqlite3, os

DB = os.path.join(os.getcwd(), "wander.db")

# Feste Weinliste (Kurzbeispiel – weitere Einträge analog ergänzen)
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

# Dropdown‑Listen automatisch generieren
LÄNDER  = sorted({w["herkunft"] for w in STATIONS})
REBSORT = sorted({w["rebsorte"] for w in STATIONS})
AROMEN  = sorted({a.strip() for w in STATIONS for a in w.get("aromen", "").split(",") if a.strip()})

FLAG = {"Deutschland":"🇩🇪","Frankreich":"🇫🇷","Italien":"🇮🇹","Spanien":"🇪🇸","Portugal":"🇵🇹","Niederlande":"🇳🇱","Chile":"🇨🇱"}

# -------------------- DB‑Helper --------------------

def _conn():
    return sqlite3.connect(DB, check_same_thread=False)

# global app_state key/value

def get_state():
    with _conn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT)")
        return {k: (int(v) if str(v).isdigit() else v) for k,v in c.execute("SELECT key,value FROM app_state")}

def set_state(**kw):
    with _conn() as c:
        for k,v in kw.items():
            c.execute("INSERT OR REPLACE INTO app_state VALUES (?,?)", (k,str(v)))
        c.commit()

# ratings‑Table (nur Felder, die wir wirklich auswerten)

def save_rating(user,sid,geschmack,alk,preis,land,rebsorte,aromen_str,comment):
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS ratings (
            user TEXT, station_id INT,
            geschmack INT, alkohol REAL, preis REAL,
            land TEXT, rebsorte TEXT, aromen TEXT,
            kommentar TEXT,
            PRIMARY KEY(user,station_id))""")
        c.execute("INSERT OR REPLACE INTO ratings VALUES (?,?,?,?,?,?,?,?,?)",
                  (user,sid,geschmack,alk,preis,land,rebsorte,aromen_str,comment))
        c.commit()

def get_rating(user,sid):
    with _conn() as c:
        return c.execute("SELECT * FROM ratings WHERE user=? AND station_id=?",(user,sid)).fetchone()

# -------------------- Page ------------------------

def station_page():
    user  = st.session_state["user"]
    st_state = get_state()
    sid   = st_state.get("current_station",0)
    mode  = st_state.get("mode","idle")

    if sid == 0:
        st.info("Noch keine Station freigegeben.")
        return

    wine = next(w for w in STATIONS if w["id"]==sid)

    # Nummer statt Name, bis Reveal
    st.header(f"🍷 Station {sid}" + ("" if mode=="vote" else f": {wine['name']}"))

    # -------- Voting --------
    if mode == "vote":
        g  = st.slider("Geschmack (0 Plörre – 10 Göttlich)",0,10,5)
        alk= st.slider("Alkohol % – 0 = Autofahren kein Problem … 16 = Tütülülüü",0.0,16.0,12.0,step=0.1)
        preis = st.slider("Preis‑Schätzung (€)",0.0,35.0,10.0,step=0.5)
        land_opt = [f"{FLAG.get(x,'')} {x}" for x in LÄNDER]
        land_sel = st.selectbox("Land", land_opt)
        reb_sel  = st.selectbox("Rebsorte", REBSORT)
        aro_sel  = st.multiselect("Aromen (mehrfach)", AROMEN)
        note     = st.text_area("Kommentar")

        if st.button("Bewertung speichern"):
            # strip Flag Emoji -> Text nach Leerzeichen
            land_clean = land_sel.split(" ",1)[-1]
            save_rating(user,sid,g,alk,preis,land_clean,reb_sel,", ".join(aro_sel),note)
            st.success("Gespeichert!")

    # -------- Reveal --------
    elif mode == "reveal":
        row = get_rating(user,sid)
        if not row:
            st.warning("Du hast für diese Station nicht bewertet.")
            return

        st.subheader("Auflösung")
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("**Echter Wein**")
            st.write({k:v for k,v in wine.items() if k not in {"id"}})
        with col2:
            st.markdown("**Dein Tipp**")
            st.write({
                "geschmack": row[2],
                "alkohol":   row[3],
                "preis":     row[4],
                "land":      row[5],
                "rebsorte":  row[6],
                "aromen":    row[7]
            })

    else:
        st.info("Warte, bis der Admin das Voting startet.")

