# admin.py – Voting starten & Aufdecken (kompatibel mit aktueller station.py)
import streamlit as st
import sqlite3, os

# Wir importieren nur die Funktionen, die es wirklich gibt
from station import STATIONS, get_state, set_state

DB = os.path.join(os.getcwd(), "wander.db")

# -------------------- Admin‑Page --------------------

def admin_page():
    st.title("🛠️ Admin – Ablauf steuern")

    state   = get_state()
    current = state.get("current_station", 0)
    mode    = state.get("mode", "idle")

    st.write(f"**Aktuelle Station:** {current or '–'}  |  **Modus:** {mode}")

    # Dropdown für nächste Station
    sel = st.selectbox("Station wählen", [f"{w['id']}: {w['name']}" for w in STATIONS], index=(current-1) if current else 0)
    sid = int(sel.split(":")[0])

    # Buttons für Ablaufsteuerung
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚦 Voting starten"):
            set_state(current_station=sid, mode="vote")
            st.success(f"Station {sid} im Voting‑Modus.")
            st.rerun()
    with col2:
        if st.button("🔔 Aufdecken & Auswertung"):
            if current == 0:
                st.warning("Es läuft noch kein Voting.")
            else:
                set_state(mode="reveal")
                st.success("Auswertung freigegeben.")
                st.rerun()
