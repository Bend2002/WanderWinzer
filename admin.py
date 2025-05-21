# admin.py – Adminoberfläche zum Freischalten & Anlegen von Stationen
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

def init_station_table():
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

def get_all_stations():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT id, name, revealed FROM stations ORDER BY id").fetchall()
    conn.close()
    return rows

def add_station(name):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO stations (name, revealed) VALUES (?, 0)", (name,))
    conn.commit()
    conn.close()

def reveal_station(station_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE stations SET revealed = 1 WHERE id = ?", (station_id,))
    conn.commit()
    conn.close()

def admin_page():
    st.title("🔐 Admin-Bereich")

    init_station_table()
    st.subheader("➕ Neue Station hinzufügen")
    new_name = st.text_input("Name der Station (z. B. 'Wein 1')")
    if st.button("Station anlegen"):
        if new_name.strip():
            add_station(new_name.strip())
            st.success(f"Station '{new_name}' hinzugefügt.")
        else:
            st.warning("Bitte einen Namen angeben.")
        st.experimental_rerun()

    st.subheader("📋 Alle Stationen")
    stations = get_all_stations()
    for id_, name, revealed in stations:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{id_}. {name} – {'✅ sichtbar' if revealed else '❌ versteckt'}")
        with col2:
            if not revealed and st.button(f"Freigeben {id_}"):
                reveal_station(id_)
                st.experimental_rerun()
