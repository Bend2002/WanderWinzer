# admin.py – Stationen verwalten & freigeben
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

def reveal_station(station_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE stations SET revealed = 1 WHERE id = ?", (station_id,))
    conn.commit()
    conn.close()

def admin_page():
    st.header("🛠️ Adminbereich – Stationen freigeben")

    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT id, name, revealed FROM stations ORDER BY id").fetchall()
    conn.close()

    for id_, name, revealed in rows:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**#{id_}** – {name}")
        with col2:
            if not revealed:
                if st.button(f"✅ Freigeben", key=f"reveal_{id_}"):
                    reveal_station(id_)
                    st.experimental_rerun()
            else:
                st.success("✅ Freigegeben")
