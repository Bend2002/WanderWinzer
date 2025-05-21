# main.py – minimaler Einstieg mit Home-Seite
import streamlit as st
import os
import sqlite3

from auth import auth_page

# ──────────────────────────────────────────────
# Seiteneinstellungen
# ──────────────────────────────────────────────
st.set_page_config(page_title="Weinwanderung", page_icon="🍇", layout="centered")

# Datenbank bei erstem Start anlegen (nur users-Tabelle)
DB_NAME = os.path.join(os.getcwd(), "wander.db")
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """
    )
    conn.commit()
    conn.close()

# ──────────────────────────────────────────────
# Persistenter Login über ?user= in der URL
# ──────────────────────────────────────────────
if "user" not in st.session_state:
    params = st.query_params          # neue API
    if "user" in params:
        st.session_state["user"] = params["user"]

# ──────────────────────────────────────────────
# Navigation
# ──────────────────────────────────────────────
if "user" not in st.session_state:
    # Kein Login → Auth-Seite anzeigen
    auth_page()
else:
    # Eingeloggt → einfache Home-Seite
    st.sidebar.success(f"Eingeloggt als {st.session_state['user']}")
    st.title("🍷 Weinwander-App (in Entwicklung)")
    st.info("Hier kommt bald die Wein-Bewertung. Genieße solange einen Schluck!")

    # Logout
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.query_params.pop("user", None)
        st.rerun()
