# main.py – Einstieg und Navigation
import streamlit as st
import os
import sqlite3

from auth import auth_page
from station import station_page
from admin import admin_page

st.set_page_config(page_title="WanderWinzer", page_icon="🍷", layout="centered")

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# Datenbank initialisieren
with sqlite3.connect(DB_NAME) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            team TEXT
        )
    """)

# Wenn nicht eingeloggt → Login anzeigen
if "user" not in st.session_state:
    auth_page()
    st.stop()

# Team abfragen
user = st.session_state["user"]
with sqlite3.connect(DB_NAME) as conn:
    row = conn.execute("SELECT team FROM users WHERE username = ?", (user,)).fetchone()
    team = row[0] if row else "Unbekannt"

# Sidebar mit Logout
with st.sidebar:
    st.success(f"Eingeloggt als **{user}**\nTeam: {team}")
    if st.button("Logout"):
        del st.session_state["user"]
        st.experimental_rerun()

# Weiterleitung: Admin oder User
if user == "admin":
    admin_page()
else:
    station_page()
