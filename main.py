# main.py – minimaler Einstieg + Team-Check
import streamlit as st
import os
import sqlite3

from auth import auth_page
from team import team_page

# ──────────────────────────────────────────────
# Seiteneinstellungen
# ──────────────────────────────────────────────
st.set_page_config(page_title="Weinwanderung", page_icon="🍇", layout="centered")

DB_NAME = os.path.join(os.getcwd(), "wander.db")
# Users-Tabelle sicherstellen
if not os.path.exists(DB_NAME):
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

# ──────────────────────────────────────────────
# Persistenter Login über ?user=
# ──────────────────────────────────────────────
if "user" not in st.session_state:
    params = st.query_params
    if "user" in params:
        st.session_state["user"] = params["user"]

# ──────────────────────────────────────────────
# Routing
# ──────────────────────────────────────────────
if "user" not in st.session_state:
    auth_page()  # noch nicht eingeloggt
else:
    # Prüfen, ob User schon ein Team hat
    conn = sqlite3.connect(DB_NAME)
    team = conn.execute(
        "SELECT team FROM users WHERE username = ?", (st.session_state["user"],)
    ).fetchone()[0]
    conn.close()

    if not team:
        team_page()  # erst Team wählen/erstellen
    else:
        # Home-Seite
        st.sidebar.success(f"Eingeloggt als {st.session_state['user']}  |  Team: {team}")
        st.title("🍷 Weinwander-App (in Entwicklung)")
        st.info("Hier kommt bald die Wein-Bewertung. Genieße solange einen Schluck!")

        # Logout
        if st.sidebar.button("Logout"):
            del st.session_state["user"]
            st.query_params.pop("user", None)
            st.rerun()
