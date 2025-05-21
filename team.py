# team.py – Team wählen oder neues Team anlegen
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")


def get_all_teams():
    conn = sqlite3.connect(DB_NAME)
    teams = [r[0] for r in conn.execute("SELECT DISTINCT team FROM users WHERE team <> ''")]
    conn.close()
    return teams


def update_user_team(user, team):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE users SET team = ? WHERE username = ?", (team, user))
    conn.commit()
    conn.close()


def team_page():
    st.header("👯‍♀️ Team bilden")
    user = st.session_state["user"]

    teams = get_all_teams()
    mode = st.radio("Team wählen", ("Bestehendem Team beitreten", "Neues Team anlegen"))

    if mode == "Bestehendem Team beitreten":
        if not teams:
            st.info("Noch keine Teams vorhanden – bitte erst eines anlegen.")
            return
        team_choice = st.selectbox("Team auswählen", teams)
        if st.button("Team beitreten"):
            update_user_team(user, team_choice)
            st.success(f"Du bist jetzt im Team „{team_choice}“!")
            st.rerun()

    else:  # Neues Team
        new_team = st.text_input("Neuen Teamnamen eingeben")
        if st.button("Team erstellen & beitreten"):
            if new_team.strip() == "":
                st.error("Teamname darf nicht leer sein.")
            elif new_team in teams:
                st.error("Team existiert bereits – bitte anderen Namen wählen.")
            else:
                update_user_team(user, new_team)
                st.success(f"Team „{new_team}“ erstellt und beigetreten!")
                st.rerun()
