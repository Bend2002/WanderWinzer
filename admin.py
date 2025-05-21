# admin.py  – Station freigeben + Ergebnisse aufdecken
import streamlit as st, sqlite3, os
from station import STATIONS, get_app_state, set_app_state

DB = os.path.join(os.getcwd(), "wander.db")

def admin_page():
    st.title("🛠️ Admin – Ablauf steuern")

    # Zeige aktuellen Zustand
    state = get_app_state()
    current = state.get("current_station", 0)
    mode    = state.get("mode", "idle")

    st.write(f"**Aktuelle Station:** {current or '–'}  |  **Modus:** {mode}")

    # Auswahl nächste Station
    next_sel = st.selectbox(
        "Station wählen",
        options=[f"{s['id']}: {s['name']}" for s in STATIONS],
        index=(current-1) if current else 0
    )
    sid = int(next_sel.split(":")[0])

    # Button: Voting starten
    if st.button("🚦 Voting starten"):
        set_app_state(current_station=sid, mode="vote")
        st.success(f"Station {sid} zum Voting freigegeben.")
        st.rerun()

    # Button: Aufdecken
    if st.button("🔔 Aufdecken & Auswertung"):
        if current == 0:
            st.warning("Es ist noch keine Station im Voting.")
        else:
            set_app_state(mode="reveal")
            st.success("Auswertung freigeschaltet.")
            st.rerun()
