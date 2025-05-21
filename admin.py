# admin.py – Stationen verwalten & Excel-Import
import streamlit as st
import pandas as pd
import sqlite3, os, pathlib

DB_NAME = os.path.join(os.getcwd(), "wander.db")
EXCEL_FILE = pathlib.Path(__file__).parent / "blindverkostung_weine.xlsx"

def init_tables():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            bild TEXT,
            jahrgang TEXT,
            herkunftsland TEXT,
            rebsorte TEXT,
            preis_euro TEXT,
            alkohol_prozent TEXT,
            revealed INTEGER DEFAULT 0
        )
    """)
    conn.commit(); conn.close()

def import_excel():
    df = pd.read_excel(EXCEL_FILE)
    df.columns = [c.strip().lower().replace(" ", "_").replace("€","euro").replace("%","prozent") for c in df.columns]

    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM stations")  # clean slate
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO stations 
            (id,name,bild,jahrgang,herkunftsland,rebsorte,preis_euro,alkohol_prozent,revealed)
            VALUES (?,?,?,?,?,?,?,?,0)
        """, (
            int(row["nr"]),
            row["weinname"],
            row.get("bild",""),
            row.get("jahrgang",""),
            row.get("herkunftsland",""),
            row.get("rebsorte",""),
            row.get("preis_euro",""),
            row.get("alkohol_prozent","")
        ))
    conn.commit(); conn.close()

def get_stations():
    conn = sqlite3.connect(DB_NAME)
    out = conn.execute("SELECT id,name,revealed FROM stations ORDER BY id").fetchall()
    conn.close()
    return out

def reveal(sid:int):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE stations SET revealed = 1 WHERE id = ?", (sid,))
    conn.commit(); conn.close()

# ──────────────────────────────────────────────
def admin_page():
    st.header("🛠️ Admin – Stationen")
    init_tables()

    # Excel-Import nur anbieten, wenn noch keine Stationen existieren
    if len(get_stations()) == 0:
        if st.button("📥 Excel importieren"):
            import_excel()
            st.success("Excel erfolgreich importiert.")
            st.experimental_rerun()

    st.divider()
    st.subheader("📋 Stationen")

    for sid, name, rev in get_stations():
        col1, col2 = st.columns([5,1])
        col1.write(f"**#{sid} – {name}**  {'✅' if rev else '❌'}")
        if not rev and col2.button("Freigeben", key=f"rel{sid}"):
            reveal(sid)
            st.experimental_rerun()
