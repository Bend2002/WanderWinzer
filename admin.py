# admin.py – Station freigeben (feste Liste)
import streamlit as st, sqlite3, os
from station import STATIONS, get_current_station_id

DB_NAME = os.path.join(os.getcwd(), "wander.db")

def set_station(sid:int):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value INTEGER)"
    )
    conn.execute(
        "INSERT OR REPLACE INTO app_state (key,value) VALUES ('current_station', ?)",
        (sid,)
    )
    conn.commit(); conn.close()

def admin_page():
    st.title("🛠️ Admin – Station freigeben")

    current = get_current_station_id()
    st.write(f"Aktuell freigegeben: **{current if current else '– keine –'}**")

    # Dropdown aller Stationen
    sel = st.selectbox(
        "Nächste Station wählen",
        [f"{s['id']}: {s['name']}" for s in STATIONS]
    )
    sid = int(sel.split(":")[0])

    if st.button("✅ Freigeben"):
        set_station(sid)
        st.success(f"Station {sid} freigegeben.")
        st.rerun()
