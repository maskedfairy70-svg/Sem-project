import sqlite3
from datetime import datetime


    #database file path
DB_PATH = "incidents.db"

def get_all_monthly_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT year, month, overall_score FROM monthly_scores
        ORDER BY year DESC, month DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    scores = []
    for row in rows:
        score_entry = {
            "Year and Month": f"{row[0]}-{row[1]:02d}",
            "Overall Score": row[2]
        }
        scores.append(score_entry)

    return scores

def init_database():
        #initialize the database with required tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

        #create incidents table only if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_name TEXT NOT NULL,
            incident_details TEXT NOT NULL,
            date_time TEXT NOT NULL,
            people_involved TEXT,
            damage_score INTEGER,
            incident_recorded_at TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL
        )
    """)

        #create monthly_scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_scores (
            year INTEGER,
            month INTEGER,
            overall_score REAL,
            PRIMARY KEY (year, month)
        )
    """)

    conn.commit()
    conn.close()

def add_incident_to_db(incident_data):
        #add a new incident to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

        #parse year and month from date_time
    dt_parsed = datetime.strptime(incident_data["Date and Time"], "%Y-%m-%d %I:%M %p")
    year = dt_parsed.year
    month = dt_parsed.month

    cursor.execute("""
        INSERT INTO incidents (
            incident_name, incident_details, date_time, people_involved,
            damage_score, incident_recorded_at, year, month
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        incident_data["Incident name"],
        incident_data["Incident Details"],
        incident_data["Date and Time"],
        incident_data["People involved"],
        incident_data["Damage score"],
        incident_data["Incident recorded at"],
        year,
        month
    ))

    conn.commit()
    conn.close()

def get_incidents_by_month(year, month):
        #get all incidents for a specific year and month
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, incident_name, incident_details, date_time, people_involved,
               damage_score, incident_recorded_at
        FROM incidents
        WHERE year = ? AND month = ?
        ORDER BY date_time
    """, (year, month))

    rows = cursor.fetchall()
    conn.close()

        #convert to dictionary format for compatibility
    incidents = []
    for row in rows:
        incident = {
            "Incident name": row[1],
            "Incident Details": row[2],
            "Date and Time": row[3],
            "People involved": row[4],
            "Damage score": row[5],
            "Incident recorded at": row[6]
        }
        incidents.append(incident)

    return incidents

def get_all_incidents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, incident_name, incident_details, date_time, people_involved,
               damage_score, incident_recorded_at
        FROM incidents
        ORDER BY year, month, date_time
    """)

    rows = cursor.fetchall()
    conn.close()

    incidents = []
    for row in rows:
        incident = {
            "Incident name": row[1],
            "Incident Details": row[2],
            "Date and Time": row[3],
            "People involved": row[4],
            "Damage score": row[5],
            "Incident recorded at": row[6]
        }
        incidents.append(incident)

    return incidents


def get_incident_by_name(incident_name):
        #get incident by name
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, incident_name, incident_details, date_time, people_involved,
               damage_score, incident_recorded_at
        FROM incidents
        WHERE LOWER(incident_name) = LOWER(?)
    """, (incident_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        incident = {
            "Incident name": row[1],
            "Incident Details": row[2],
            "Date and Time": row[3],
            "People involved": row[4],
            "Damage score": row[5],
            "Incident recorded at": row[6]
        }
        return incident
    else:
        return None


def delete_incident_by_name(incident_name):
        #delete a single incident by name
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM incidents WHERE incident_name = ?",
        (incident_name,)
    )
    deleted = cursor.rowcount

    conn.commit()
    conn.close()
    return deleted > 0


def delete_all_incidents():
        #delete all incidents from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM incidents")
    conn.commit()
    conn.close()


def get_monthly_score(year, month):
        #get the overall score for a specific year and month
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT overall_score FROM monthly_scores
        WHERE year = ? AND month = ?
    """, (year, month))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None

def set_monthly_score(year, month, score):
        #set or update the overall score for a specific year and month
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO monthly_scores (year, month, overall_score)
        VALUES (?, ?, ?)
    """, (year, month, score))

    conn.commit()
    conn.close()

def check_month_has_data(year, month):
        #Check if a specific year-month has any incidents
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM incidents
        WHERE year = ? AND month = ?
    """, (year, month))

    count = cursor.fetchone()[0]
    conn.close()

    return count > 0