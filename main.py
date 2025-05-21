# main.py – stabiler Einstieg mit Login, Team-Check, Fehlerbehandlung
import streamlit as st
import os
import sqlite3

from auth import auth_page
from team import team_page
from station import station_page

st.set_page_config(page_title="Weinwanderung", page_icon="🍇", layout="centered")

DB_NAME = os.path.join(os.getcwd(), "wander.db")
# Sicherheits-Setup bei frischer App
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
    params = st.query_params
    if "user" in params:
        st.session_state["user"] = params["user"]

# Routing
if "user" not in st.session_state:
    auth_page()
else:
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute(
        "SELECT team FROM users WHERE username = ?", (st.session_state["user"],)
    ).fetchone()
    conn.close()

    # Wenn der User nicht mehr existiert (z. B. nach DB-Reset)
    if not row:
        del st.session_state["user"]
        st.query_params.pop("user", None)
        st.rerun()

    team = row[0]

    if not team:
        team_page()
    else:
        st.sidebar.success(f"Eingeloggt als {st.session_state['user']}  |  Team: {team}")
        station_page()

        if st.sidebar.button("Logout"):
            del st.session_state["user"]
            st.query_params.pop("user", None)
            st.rerun()
