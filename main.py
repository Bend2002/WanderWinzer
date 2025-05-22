# main.py – Einstiegspunkt
import streamlit as st
import os
import sqlite3

from auth import auth_page
from station import station_page
from admin import admin_page
from team import team_page


st.set_page_config(page_title="Weinwanderung", page_icon="🍇", layout="centered")

DB_NAME = os.path.join(os.getcwd(), "wander.db")
# Tabelle users immer sicher anlegen
conn = sqlite3.connect(DB_NAME)
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        team     TEXT DEFAULT ''
    )
    """
)
conn.commit()
conn.close()

# Persistenter Login über ?user=
if "user" not in st.session_state:
    qp = st.query_params
    if "user" in qp:
        st.session_state["user"] = qp["user"]

# ──────────────────────────────
# Routing
# ──────────────────────────────
if "user" not in st.session_state:
    auth_page()  # Login / Registrierung
else:
    # Team aus DB holen
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute("SELECT team FROM users WHERE username = ?", (st.session_state["user"],)).fetchone()
    conn.close()

   
if not row:
        del st.session_state["user"]
        st.query_params.pop("user", None)
        st.rerun()
        st.stop()          # <- garantiertes Ende
 
    # team = row[0]          # hier gibt es sicher einen Wert

    if not team:
        team_page()  # Nutzer muss Team wählen / anlegen
    else:
        st.sidebar.success(f"Eingeloggt als {st.session_state['user']} 🟢 Team: {team}")

        if team.lower() == "admin":
            admin_page()
        else:
            station_page()

        if st.sidebar.button("Logout"):
            del st.session_state["user"]
            st.query_params.pop("user", None)
            st.rerun()
