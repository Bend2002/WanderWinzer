# station.py  – Voting & Ergebnis-Anzeige
import streamlit as st, sqlite3, os

DB = os.path.join(os.getcwd(), "wander.db")
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

# ---------- DB-Helper ----------
def _conn():
    return sqlite3.connect(DB, check_same_thread=False)

def get_app_state():
    with _conn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT)")
        rows = c.execute("SELECT key,value FROM app_state").fetchall()
    return {k: (int(v) if v.isnumeric() else v) for k,v in rows}

def set_app_state(**kwargs):
    with _conn() as c:
        for k,v in kwargs.items():
            c.execute("INSERT OR REPLACE INTO app_state (key,value) VALUES (?,?)", (k,str(v)))
        c.commit()

def save_rating(user, sid, geschmack, alk, preis, note):
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
              user TEXT, station_id INTEGER,
              geschmack INTEGER, alkohol REAL, preis REAL, kommentar TEXT,
              PRIMARY KEY (user, station_id)
        )""")
        c.execute("""
            INSERT OR REPLACE INTO ratings
            VALUES (?,?,?,?,?,?)
        """, (user, sid, geschmack, alk, preis, note))
        c.commit()

def get_my_rating(user, sid):
    with _conn() as c:
        row = c.execute("""
            SELECT geschmack,alkohol,preis,kommentar
            FROM ratings WHERE user=? AND station_id=?""",
            (user,sid)).fetchone()
    return row

# ---------- Page ----------
def station_page():
    user   = st.session_state["user"]
    state  = get_app_state()
    mode   = state.get("mode", "idle")
    sid    = state.get("current_station", 0)

    if sid == 0:
        st.info("Noch keine Station freigegeben.")
        return

    wine = next(w for w in STATIONS if w["id"] == sid)

    st.header(f"🍷 Station {sid}: {wine['name']}")

    # ── Voting-Modus ───────────────────────────
    if mode == "vote":
        st.subheader("Deine Blind-Bewertung")

        geschmack = st.slider("Geschmack (0 = Plörre, 10 = Göttlich)", 0,10,5)
        alk       = st.slider("Alkohol %", 8.0,16.0,12.0,step=0.1)
        preis     = st.number_input("Preis-Schätzung €", 0.0,100.0,step=0.5)
        note      = st.text_area("Kommentar")

        if st.button("Speichern"):
            save_rating(user,sid,geschmack,alk,preis,note)
            st.success("Danke, Bewertung gespeichert!")

    # ── Reveal-Modus ───────────────────────────
    elif mode == "reveal":
        my = get_my_rating(user,sid)
        if not my:
            st.warning("Du hast für diese Station noch nicht bewertet.")
            return

        st.subheader("🔍 Auflösung")

        col1,col2 = st.columns(2)
        with col1:
            st.write("**Echter Wein**")
            st.write(f"• Jahrgang: {wine['jahrgang']}")
            st.write(f"• Herkunft: {wine['herkunft']}")
            st.write(f"• Farbe: {wine['farbe']}")
            st.write(f"• Alkohol: {wine['alkohol']} %")
            st.write(f"• Preis: {wine['preis']} €")
        with col2:
            st.write("**Dein Tipp**")
            st.write(f"• Alkohol: {my[1]} % → Δ {abs(my[1]-wine['alkohol']):.1f}")
            st.write(f"• Preis:   {my[2]} € → Δ {abs(my[2]-wine['preis']):.2f}")
            st.write(f"• Geschmack-Score: {my[0]}/10")
            st.write("• Kommentar:") 
            st.write(my[3] or "–")

        st.success("Vergleich oben - nächste Station wird freigegeben, sobald der Admin \"Voting starten\" klickt.")

    else:
        st.info("Bitte warte, bis der Admin das Voting startet.")
