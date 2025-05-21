# populate_stations.py  ─ einmalig starten, dann löschen/ignorieren
import pandas as pd
import sqlite3, os

# ► Pfad zu deiner Excel-Datei
EXCEL_FILE = "blindverkostung_weine.xlsx"   # liegt im Projektverzeichnis
DB_NAME    = os.path.join(os.getcwd(), "wander.db")

# ──────────────────────────────────────────────
# Excel laden (alle Spalten bleiben erhalten)
df = pd.read_excel(EXCEL_FILE)

# Erwartete Pflichtspalten (in der Excel genau so benannt):
# Nr | Weinname | Jahrgang | Herkunftsland | Rebsorte | Farbe |
# Preis (€) | Alkohol (%) | Bild | … (weitere Spalten beliebig)
# Alles, was in der Excel vorhanden ist, wird übernommen.

# Update: Spaltennamen in DB dürfen keine Leer-/Sonderzeichen enthalten
df.columns = [c.strip().lower().replace(" ", "_").replace("€","euro").replace("%","prozent")
              for c in df.columns]

# ──────────────────────────────────────────────
# Stations-Tabelle (dynamisch mit ALLEN Excel-Spalten)
conn = sqlite3.connect(DB_NAME)

# Tabelle drop + neu anlegen (kein Duplikat-Chaos)
conn.execute("DROP TABLE IF EXISTS stations")

# SQL-Schema dynamisch bauen
cols_sql = ",\n    ".join(f"{col} TEXT" for col in df.columns if col != "nr")
create_sql = f"""
CREATE TABLE stations (
    id          INTEGER PRIMARY KEY,      -- nutzt Excel-Nr (nr)
    {cols_sql},
    revealed    INTEGER DEFAULT 0         -- 0 = verdeckt, 1 = aufgedeckt
)
"""
conn.execute(create_sql)

# Excel in DB schreiben (Nutze Nr als id)
for _, row in df.iterrows():
    values = [int(row["nr"])] + [row[c] for c in df.columns if c != "nr"] + [0]  # revealed = 0
    placeholders = ",".join("?" * len(values))
    conn.execute(f"INSERT INTO stations VALUES ({placeholders})", values)

conn.commit(); conn.close()

print(f"🎉  {len(df)} Stationen erfolgreich importiert!")
