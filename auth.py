# auth.py – minimalistisches, stabiles Login/Registrierung
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# ──────────────────────────────────────────────
# DB-Helfer
# ──────────────────────────────────────────────
def init_db():
    """legt Tabelle users an, falls nicht vorhanden"""
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


def register_user(username: str, password: str) -> bool:
    init_db()
    if not username or not password:
        return False
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username: str, password: str) -> bool:
    init_db()
    conn = sqlite3.connect(DB_NAME)
    ok = (
        conn.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        is not None
    )
    conn.close()
    return ok

# ──────────────────────────────────────────────
# Streamlit-UI
# ──────────────────────────────────────────────
def auth_page():
    init_db()

    st.header("🔐 Login / Registrierung")
    mode = st.radio("Modus wählen", ("Einloggen", "Registrieren"), horizontal=True)

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort (3 Ziffern)", type="password", max_chars=3)

    if mode == "Registrieren":
        if st.button("Registrieren"):
            if register_user(username, password):
                st.success("Registrierung erfolgreich – bitte jetzt einloggen.")
            else:
                st.error("Benutzername existiert bereits oder Eingabe leer.")
    else:  # Einloggen
        if st.button("Einloggen"):
            if login_user(username, password):
                st.session_state["user"] = username               # in Session
                st.query_params["user"] = username                # in URL
                st.experimental_rerun()
            else:
                st.error("Login fehlgeschlagen.")
