"""
database.py - City Hospital Database Setup
Run this file ONCE to create the SQLite database and tables.
Usage: python database.py
"""

import sqlite3
import hashlib

DB_NAME = "city_hospital.db"

def get_connection():
    """Returns a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_tables():
    """Creates all required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Patients / Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            dob TEXT,
            gender TEXT,
            contact TEXT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'patient',
            last_visit TEXT,
            last_priority TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Visits / Triage records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            visit_time TEXT NOT NULL,
            heart_rate INTEGER,
            bp_systolic INTEGER,
            bp_diastolic INTEGER,
            temperature REAL,
            spo2 INTEGER,
            resp_rate INTEGER,
            primary_symptom TEXT,
            other_symptoms TEXT,
            pain_level INTEGER,
            priority TEXT NOT NULL,
            reason TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    # Create default admin account
    cursor.execute("SELECT * FROM patients WHERE username = 'nithish'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO patients (name, age, dob, gender, contact, username, password, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("nithish", 18, "20-05-2007", "Male", "9487776225", "nithish",
              hash_password("nithish123"), "nithish"))
        print("Default admin created: username=admin, password=admin123")

    conn.commit()
    conn.close()
    print("Database and tables created successfully: city_hospital.db")

if __name__ == "__main__":
    create_tables()