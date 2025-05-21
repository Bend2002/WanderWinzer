# admin.py – Stationen verwalten & freigeben
import streamlit as st
import sqlite3, os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

def init_station_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS stations (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT,
            revealed INTEGER DEFAULT 0
        )
        """
    )
    conn.commit(); conn.close()

def get_stations():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT id,name,revealed FROM stations ORDER BY id").fetchall()
    conn.close()
    return rows

def add_station(name):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO stations (name) VALUES (?)", (name,))
    conn.commit(); conn.close()

def reveal(station_id:int):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE stations SET revealed = 1 WHERE id = ?", (station_id,))
    conn.commit(); conn.close()

# ──────────────────────────────────────────────
def admin_page():
    st.title("🛠️ Admin – Stationen")

    init_station_table()

    # Neue Station anlegen
    with st.form("add"):
        new_name = st.text_input("Neue Station / Weinname")
        submitted = st.form_submit_button("➕ anlegen")
        if submitted and new_name.strip():
            add_station(new_name.strip())
            st.success("Station angelegt.")
            st.experimental_rerun()

    st.divider()
    st.subheader("📋 Stationen")

    for sid, name, rev in get_stations():
        col1, col2 = st.columns([5,1])
        col1.write(f"**#{sid} – {name}**  {'✅' if rev else '❌'}")
        if not rev and col2.button("Freigeben", key=f"rel{sid}"):
            reveal(sid)
            st.experimental_rerun()
