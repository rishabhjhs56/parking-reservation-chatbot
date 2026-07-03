import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

# Database path
DB_PATH = "database/parking.db"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# -------------------------------
# Create Parking Slots Table
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    zone TEXT,
    block TEXT,
    slot_number TEXT,
    vehicle_type TEXT,
    is_available INTEGER DEFAULT 1
)
""")

# -------------------------------
# Create Reservations Table
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    vehicle_number TEXT,
    vehicle_type TEXT,
    location TEXT,
    reservation_date TEXT,
    start_time TEXT,
    end_time TEXT,
    slot_id INTEGER,
    status TEXT,
    driving_license TEXT,
    zone TEXT,
    block TEXT,
    slot_number TEXT,         
    FOREIGN KEY(slot_id) REFERENCES parking_slots(slot_id)
)
""")

conn.commit()
conn.close()

print("✅ Database and tables created successfully.")